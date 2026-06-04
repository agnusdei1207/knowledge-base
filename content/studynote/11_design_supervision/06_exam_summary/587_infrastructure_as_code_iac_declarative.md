---
title: "587. 인프라 코드화 IaC 선언적 관리 (Infrastructure as Code IaC Declarative)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IaC(선언형)는 인프라의 **Desired State(목표 상태)**를 HCL/YAML/Pulumi 코드 등으로 선언하면, Plan->Apply->State 동기화 루프를 통해 실제 인프라를 자동으로 **Idempotent(멱등)**하게 수렴시키는 패러다임이며, "어떻게(How)"가 아닌 "무엇을(What)"을 정의하는 것이 핵심입니다.
> 2. **가치**: 프로비저닝 시간 95% 단축(수 일->수 분), 구성 드리프트 자동 보정, 변경 실패율 60%v, 인프라 변경 리드타임 MTTR 80% 개선, 그리고 변경 이력의 100% Git 기반 감사 추적 확보.
> 3. **판단 포인트**: 선언형(Terraform/CDK/Pulumi) ↔ 명령형(Ansible/Chef) 트레이드오프, State 파일 관리(원격 백엔드 잠금·암호화·충돌 회피), 모듈화 경계(Provider 캡슐화), Drift Detection 정책, 그리고 Plan을 CI/PR 단계에서 강제하는 GitOps 분기 전략 설계가 기술사의 핵심 결정 사안입니다.

---

## Ⅰ. 개요 및 필요성

전통적 인프라 운영은 GUI 콘솔 클릭, 수동 스크립트, 내부 티켓 기반의 "Snowflake Server" 운영으로 특징지어집니다. 이는 수십 년간 운영되어 왔으나, **클라우드 네이티브 시대(수천 개의 VM, 컨테이너, VPC, IAM 정책이 API 호출로 동적 생성/소멸)**에서는 근본적 한계가 드러납니다.

- **수동 운영의 5대 통증(Point-of-Pain)**
  1. **비일관성(Non-Conformance)**: 100대 서버를 동일 이미지로 만들어도 사람이 손대면 결국 1%씩 달라짐 -> Configuration Drift.
  2. **느린 프로비저닝**: 신규 환경 1개 구축에 평균 2~4주 소요(Tier-1 엔터프라이즈 기준, Gartner 2018).
  3. **감사 불가성(Audit Gap)**: "누가, 언제, 어떤 변경을 했는가"를 사후에 추적할 수 없음.
  4. **롤백 불가성**: 수동 변경은 Undo가 거의 불가능 -> 재해 시 RTO(Recovery Time Objective) 급증.
  5. **인적 오류(Toil)**: Google SRE 통계에 따르면 운영 엔지니어의 50% 이상이 반복적 수작업에 소모.

**IaC(선언형) 패러다임**은 이 문제를 **"인프라를 소프트웨어처럼 버전 관리하고, 테스트하고, 검토하고, 배포한다"**는 원칙으로 해결합니다. 특히 선언형(Declarative) 접근은 운영자가 **"결과로 원하는 상태(Desired State)"**만 선언하면, 도구가 **"현재 상태(Current State)"**와의 차이(Diff)를 자동으로 계산하여 수렴시키는 **종결 시스템(Terminal Automaton)** 모델을 따릅니다.

```text
   +--------------- 전통 수동 인프라 관리 ---------------+
   |                                                     |
   |   [운영자] --click---> [콘솔/터미널]                  |
   |       |                              |              |
   |       |              (불완전·비일관)  v              |
   |       |                       [실제 인프라]          |
   |       |                              |              |
   |       +------ 반복·Toil·Drift <-------+              |
   |                                                     |
   |   ❌ 이력 추적 불가  ❌ 멱등성 없음  ❌ 사람 의존      |
   +-----------------------------------------------------+

   +--------------- IaC 선언형 관리 패러다임 --------------+
   |                                                       |
   |   [개발자/엔지니어]                                    |
   |         |                                             |
   |         |  git commit/push                            |
   |         v                                             |
   |   +------------------+   PR 리뷰·정책 검증   +-----+  |
   |   |  선언형 코드     | -------------------->  | VCS |  |
   |   |  (Desired State)|   plan / cost /lint   |(Git)|  |
   |   +------------------+                       +-----+  |
   |         |                                  CI/CD      |
   |         v                                             |
   |   +--------------------------------------------------+|
   |   |   IaC 엔진 (Terraform / CloudFormation / Pulumi)||
   |   |  -- Plan: 현재 vs 선언 차이점(Diff) 계산 --     ||
   |   |  -- Apply: 그래프 순서대로 API 호출 (멱등) --   ||
   |   |  -- Refresh: 실제 상태를 State로 동기화 --      ||
   |   +--------------------------------------------------+|
   |         |                                             |
   |         v                                             |
   |   [프로바이더 API]---> [실제 클라우드/리소스]          |
   |   (AWS/GCP/Azure/K8s/VMware)                         |
   |                                                       |
   |   ✅ Git 히스토리 = 인프라 히스토리                     |
   |   ✅ PR 리뷰 = 인프라 변경 승인                         |
   |   ✅ 멱등 실행 = 반복 안전성                            |
   |   ✅ 자동 Drift 보정 = Self-Healing                    |
   +-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 수동 인프라 관리가 매번 직접 주방에 들어가서 칼·불 조절하며 요리하는 것이라면, 선언형 IaC는 **"냉동 밀키트(레시피=코드)를 냉장고에 넣어두면 로봇 주방장(엔진)이 알아서 똑같은 요리(상태)를 내놓는 것"**입니다. 레시피만 바꾸면 모든 식당이 동시에 메뉴를 갱신합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

선언형 IaC의 핵심 동작 메커니즘은 **3단계 루프(Plan -> Apply -> Refresh)** 와 **State 기반 종결성**으로 요약됩니다. 도구별로 구현 방식은 다르지만, 모든 선언형 IaC는 이 추상화 위에서 동작합니다.

```text
                       IaC 선언형 엔진 내부 동작
   +----------------------------------------------------------+
   |                                                          |
   |   +-----------+   +------------------+   +------------+ |
   |   |  Code     |   |  State File      |   |  Provider  | |
   |   |  (.tf/    |   |  (tfstate/       |   |  (AWS, GCP,| |
   |   |   .yaml)  |   |   S3+DynamoDB)   |   |   K8s API) | |
   |   +-----+-----+   +--------+---------+   +-----+------+ |
   |         |                  |                    |        |
   |         | ① Read           | ② Read             |        |
   |         +----------+       |                    |        |
   |                    v       v                    |        |
   |              +-----------------+                |        |
   |              |  Plan Engine    |                |        |
   |              | (Graph Builder) |                |        |
   |              |  - 의존성 DAG   |                |        |
   |              |  - Diff 계산    |                |        |
   |              +--------+--------+                |        |
   |                       | ③ Diff                  |        |
   |                       v                         |        |
   |              +-----------------+                |        |
   |              |  Execution Plan | <--- Human Review |        |
   |              |  (Create/Update/|      (terraform |        |
   |              |   Delete/Diff)  |       plan/PR)  |        |
   |              +--------+--------+                |        |
   |                       | ④ Apply                 |        |
   |                       v                         v        |
   |              +-------------------------------------+    |
   |              |  API 호출 (Create/Update/Delete)    |    |
   |              +-----------------+-------------------+    |
   |                                | ⑤ Confirm               |
   |                                v                         |
   |                       +-----------------+                |
   |                       |  State Refresh  | ---> State 갱신 |
   |                       +-----------------+                |
   |                                                          |
   |   ※ Graph Builder: 리소스 간 암묵적·명시적 의존성(depends_on,  |
   |     참조)으로부터 병렬 실행 가능한 DAG를 구성 -> 부분 실패 시   |
   |     재시도 시 안전.                                          |
   +----------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **선언형 DSL (HCL/YAML/Pulumi 언어)** | 인프라 목표 상태를 코드로 표현 | Terraform HCL(중괄호 기반, expression/interpolation 지원), CloudFormation JSON/YAML, Pulumi(TypeScript/Python/Go의 일반 언어 사용 -> 컴파일 타임 타입 검증) |
| **State Backend (상태 저장소)** | 실제 인프라의 매핑(리소스 ID, 속성, 메타데이터) 영속화 | Terraform: S3 + DynamoDB Lock, Terraform Cloud, Consul, OSS. CloudFormation: 내부 S3 스택 레코드. Pulumi: S3, Azure Blob, Pulumi Cloud. **State 잠금(Lock)**: 동시 apply 방지를 위한 낙관적 락/분산 락 (DynamoDB Conditional Write) |
| **Provider / Plugin** | 클라우드/플랫폼 API의 추상화 어댑터 | 각 벤더 SDK를 Wrap. 예: AWS Provider(~1,800개 리소스), Kubernetes Provider(CRUD), Helm Provider, GitHub Provider. Provider는 Protocol v5/v6 RPC로 엔진과 통신 |
| **Plan & Apply Engine** | Diff 계산 및 실행 그래프 구성 | Terraform: `terraform plan`은 Refreshing State -> Reading Configuration -> Diff 계산(Change Type: create/update/delete/replace) -> 11단계 검증(예: IAM 권한). Apply는 DAG 위에서 병렬·순차 실행 |

### 핵심 원리 심화: **종결 시스템(Terminal Automaton) 모델**

선언형 IaC의 이론적 기반은 **Fixed-Point Iteration**입니다. `f(state) = desired_state` 일 때, 어떤 초기 상태에서 시작하든 `f`를 반복 적용하면 결국 `desired_state`에 수렴합니다. 이 성질이 **Idempotency(멱등성)**의 수학적 근거입니다.

```
  ① State: 존재 X (Initial)
  ② Apply: "VPC 생성" 코드 실행 -> API 호출 -> State: VPC 존재
  ③ Apply: (동일 코드 재실행) -> Diff: 없음(0 changes) -> 멱등
  ④ 외부 수동 변경(예: 콘솔에서 Tag 변경) -> Drift 발생
  ⑤ terraform apply -refresh-only -> 실제 상태로 State 재동기화
  ⑥ Drift 후 동일 코드 재실행 -> Diff: Tag 다시 선언대로 변경
  -> Self-Healing 루프 완성
```

### 핵심 원리 심화: **의존성 그래프와 병렬 실행**

Terraform은 내부적으로 **Resource Graph**를 구성합니다. 예: `aws_instance`가 `aws_subnet.id`를 참조하면, `aws_subnet`을 먼저 만들고 `aws_instance`를 만듭니다. 의존성 없는 리소스(예: 서로 다른 Region의 VPC 2개)는 병렬로 생성됩니다. 이 DAG는 `terraform graph | dot -Tpng > graph.png`로 시각화 가능하며, **순환 의존성(cycle)**이 있으면 Plan 단계에서 즉시 실패합니다.

### 핵심 원리 심화: **드리프트 감지(Drift Detection)**

운영팀이 콘솔에서 직접 인프라를 수정하면 State와 실제 환경이 달라집니다(Drift). 이를 해결하는 방법:
- `terraform plan -refresh-only`: 실제 API에서 State를 다시 채움(Drift를 State에 반영).
- `terraform plan -detailed-exitcode`: 0(일치), 1(에러), 2(Drift 감지) -> CI에서 모니터링 가능.
- 상용 도구: `driftctl`, `Steampipe`, AWS Config + SSM Document로 주기적 Drift 리포트.

- **📢 섹션 요약 비유**: 선언형 IaC는 **"냉장고에 '계란 10개, 우유 2L'라고 적힌 메모(=Desired State)를 붙여두면, IoT 센서가 매일 아침 냉장고를 열고 실제 내용물을 센싱한 뒤(State Refresh) 부족한 만큼 자동으로 장을 봐주는(Apply) 똑똑한 주방"**입니다. 누가 우유를 몰래 마셔도(외부 변경) 다음 날 아침에 다시 채워집니다.

---

## Ⅲ. 비교 및 연결

### 1. 선언형(Declarative) vs 명령형(Imperative)

| 구분 | 선언형 IaC (Terraform, CloudFormation) | 명령형 IaC (Ansible, Chef, Bash) |
| :--- | :--- | :--- |
| **기술 사상** | "원하는 결과(What)"를 선언 | "수행 절차(How)"를 순차 서술 |
| **상태 추적** | State 파일로 Current State 유지 -> 자동 Diff | 보통 상태 비보유, 실행 흐름이 코드 |
| **멱등성** | 본질적으로 내장 (재실행 시 0 changes) | 수동으로 `creates`/`unless`/`when` 조건 분기 필요 |
| **실행 순서** | 의존성 그래프(DAG) 기반 자동 병렬/순차 | 작성된 Task 순서대로 직렬(또는 strategy: free) |
| **언어/DSL** | 전용 DSL(HCL/JSON/YAML) | 범용 언어(Python, Ruby) + DSL |
| **적합 영역** | 클라우드 리소스/네트워크/오케스트레이션 | 서버 내부 설정(Configuration)·OS 패치·앱 배포 |
| **결정 시 고려사항** | State 관리 부담, Plan 리뷰 문화, 모듈화 | 절차 검증 어려움, 중간 실패 시 Partial State 위험 |

### 2. 주요 선언형 IaC 도구 비교

| 구분 | Terraform (HashiCorp) | AWS CloudFormation | Pulumi | Google Config Connector / Azure ARM |
| :--- | :--- | :--- | :--- | :--- |
| **지원 범위** | 멀티 클라우드(1000+ Provider) | AWS 전용 | 멀티 클라우드 | 각 CSP 전용 |
| **언어** | HCL(전용 DSL) | JSON/YAML | TypeScript, Python, Go, Java, .NET | YAML/JSON |
| **State 관리** | 사용자 관리(원격 백엔드 필수) | AWS 자동 관리(S3 내부) | Pulumi Cloud 또는 자체 백엔드 | CSP 자동 |
| **Plan/Preview** | `terraform plan` 정교한 Diff | Change Set(기능 제한적) | `pulumi preview` | `what-if`(Azure) / GCP에서는 제한적 |
| **모듈화** | Terraform Module Registry, Registry 프로토콜 | Nested Stack, Module | 표준 패키지 관리(npm/pip) | Template Spec |
| **정책 거버넌스** | Sentinel, OPA(Open Policy Agent) | IAM + cfn-lint + cfn-nag | Pulumi Policies(CrossGuard), OPA | CSP IAM + 조직 정책 |
| **생태계/커뮤니티** | 최대(2024년 기준 다운로드 수십억 회) | AWS 종속 | 성장 중(개발자 친화) | CSP 종속 |
| **라이선스** | BSL 1.1(2023 변경, 일부 기능 유료) | AWS 제공(무료) | Apache 2.0 | CSP 제공 |

### 3. 통합 아키텍처 (CI/CD, GitOps, Policy as Code)

선언형 IaC는 단독 도구로 끝나지 않고, **SDLC 전체**와 통합되어야 진가を発揮합니다
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 587 / 600

<- **이전**: [586. 서비스 메시 관측성 트래픽 제어](/studynote/11_design_supervision/06_exam_summary/587_service_mesh_observability_traffic_contr/)
**다음**: [588. 불변 인프라 골든 이미지 패턴](/studynote/11_design_supervision/06_exam_summary/588_immutable_infrastructure_golden_image/) ->

---
