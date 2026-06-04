---
title: "501. IaC Pulumi CDK 프로그래밍 언어 기반 (IaC Pulumi CDK Programming Language Based)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Pulumi는 TypeScript, Python, Go, Java, .NET 등 범용 프로그래밍 언어(General-Purpose Language, GPL)로 인프라를 선언적(Declarative)하게 정의하되, 코드는 명령형(Imperative)·함수형 프로그래밍으로 작성되는 **"Program Synthesis 방식의 IaC"** 이다. Pulumi 엔진이 프로그램 실행 결과의 Resource Graph를 자동 합성하여 상태(State)를 비교·적용한다.
> 2. **가치**: HCL/JSON DSL 대비 **테스트 프레임워크(Jest, pytest)**, **패키지 매니저(npm, pip)**, **IDE 자동완성**, **타입 시스템**, **기존 라이브러리 재사용**이 가능하여, 인프라 변경 시 **MTTR 40~60% 단축**, **DRY 원칙 준수율 향상**, **Policy as Code(CrossGuard)** 기반의 거버넌스 자동화를 달성할 수 있다.
> 3. **판단 포인트**: 단순 정적 인프라 선언은 Terraform HCL이 우위, **동적 로직·복합 조건·외부 API 연동**이 많거나 **소프트웨어 엔지니어링 표준(테스트, 모듈화, CI/CD)**을 인프라에 강제해야 하는 조직에서는 Pulumi CDK가 합리적이다. 단, 러닝커브와 State Backend 운영 부담, 그리고 언어별 Provider 성숙도(예: Java/.NET은 AWS·Azure 중심)를 반드시 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

기존 IaC 도구(Terraform, CloudFormation, Ansible)는 각 도구 고유의 **DSL(Domain Specific Language)** 을 사용해왔다. HCL, JSON, YAML로 작성된 DSL은 단순한 키-값 구조라서 "변수 정의 -> 모듈 호출 -> 정적 선언" 패턴에는 적합하지만, 다음과 같은 한계가 명확해졌다.

- **조건 분기·반복·상태 변수** 등 프로그래밍 로직을 표현하려면 Terraform의 `count`/`for_each`/`dynamic block` 같은 우회적 메커니즘을 사용해야 함
- **타입 안전성 부재**로 `terraform plan` 시점까지 오류를 알 수 없어, 대규모 멀티 클라우드 환경에서 장애 비용 증가
- **단위 테스트·모킹·리팩터링**이 어려워 DevOps와 SRE가 별도 검증 절차(보통 수동 PR 리뷰)에 의존
- **모노레포 마이크로서비스**처럼 코드베이스가 거대해질수록 인프라 코드도 라이브러리화·패키지화가 필요

이에 Pulumi는 *"Infrastructure as Code, but real code"* 라는 슬로건으로, 인프라 정의를 **기존 프로그래밍 언어의 임포트(import) 체계**에 통합시켰다. 이로써 `npm install pulumi` 후 즉시 인프라도 "소프트웨어"로 다룰 수 있게 되었다.

특히 한국 공공·금융 SI 환경에서 멀티 클라우드(AWS + NCP + Azure), DR(Disaster Recovery) 구성, 보안 컴플라이언스(CSAP, ISMS-P) 자동화가 요구되면서, DSL의 한계를 넘어서는 도구의 필요성이 대두되었다.

```text
   [Legacy IaC: DSL 기반]                     [Modern IaC: Pulumi CDK 기반]
  +----------------------+                 +------------------------------+
  | *.tf (HCL)           |                 | index.ts / __main__.py / main.go
  | {                    |                 | --------------------------- |
  |   resource "aws_vpc" |   ----> 진화 ---->| import * as aws from "@pulumi/aws";
  |   cidr_block = var.x |                 | const vpc = new aws.ec2.Vpc("main",
  |   tags = local.t     |                 |   { cidrBlock: "10.0.0.0/16" });|
  | }                    |                 | export const vpcId = vpc.id;  |
  +----------+-----------+                 +--------------+---------------+
             | static text                               | real program
             v                                            v
     [HCL Parser -> DAG]                          [Pulumi Engine -> Resource Graph]
```

**기존 패러다임 vs 새로운 패러다임**

| 항목 | 기존 DSL (HCL/JSON/YAML) | Pulumi CDK |
| :--- | :--- | :--- |
| 언어 | 도구별 전용 문법 | TS/Python/Go/Java/.NET (5종) |
| 변수·로직 | 제한적(count, for_each) | 완전한 제어문(if/for/while/try-catch) |
| 테스트 | `terraform plan` 의존 | Jest, pytest, go test 네이티브 |
| 패키지화 | Module(재사용 한계) | npm/pip/Maven 패키지로 자유 배포 |
| IDE 지원 | 기본 자동완성 | IntelliSense, tsc, mypy, go vet |
| 멀티 클라우드 | Provider별 분리 | 단일 코드로 AWS+Azure+GCP+K8s 혼합 |

- **📢 섹션 요약 비유**: DSL이 "아이들이 블록으로만 집 짓기" 였다면, Pulumi는 **"성인용 LEGO Technic + 프로그래밍 가능한 모터·센서 세트"** 를 주는 것과 같다. 같은 부품을 쓰지만 실제 엔지니어링 도구(컴파일러, 디버거, 테스트 러너)까지 함께 사용 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Pulumi는 **3-Tier 아키텍처**로 동작하며, 핵심은 **사용자 코드 -> Resource Graph -> State 비교 -> Provider API 호출**의 파이프라인이다.

```text
                        +--------------------------------------------+
                        |            Pulumi Engine (Go)              |
                        |  +------------------------------------+    |
                        |  | 1. Language Host (gRPC over stdio)|    |
                        |  |    - node / python3 / go / dotnet |    |
                        |  +---------------+--------------------+    |
                        |                  | serialization           |
                        |  +---------------v--------------------+    |
                        |  | 2. Resource Monitor (RPC)          |    |
                        |  |    - RegisterResource (CRUD)        |    |
                        |  |    - Invoke (data source)            |    |
                        |  |    - Call (provider function)       |    |
                        |  +---------------+--------------------+    |
                        |                  | desired state (proto)    |
                        |  +---------------v--------------------+    |
                        |  | 3. Diff Engine (State vs Desired)   |    |
                        |  |    - Replacement detection           |    |
                        |  |    - Property-level diff             |    |
                        |  +---------------+--------------------+    |
                        |                  | plan                     |
                        |  +---------------v--------------------+    |
                        |  | 4. Deployment Executor              |    |
                        |  |    - Parallel dependency resolver    |    |
                        |  |    - Checkpoint to State Backend     |    |
                        |  +------------------------------------+    |
                        +--------+--------------+-------------------+
                                 |              |
                +----------------v-+        +--v----------------------+
                | State Backend     |        | Cloud Provider SDKs     |
                | - Pulumi Cloud    |        | - AWS / Azure / GCP     |
                | - S3 / Azure Blob |        | - Kubernetes            |
                | - Local FS        |        | - NCP / NHN / Naver     |
                | - OSS Backends    |        | - Pulumi Provider Schema|
                +-------------------+        +-------------------------+
```

**Resource Graph 합성 원리 (Program Synthesis)**

사용자가 작성한 `new aws.ec2.Vpc(...)` 같은 명령형 호출은 Pulumi가 다음 순서로 처리한다.

1. **RegisterResource**: `Resource Monitor`에 `(type, name, props, dependencies)` 등록
2. **Object Construction**: `URN`(Uniform Resource Name) 생성 = `urn:pulumi:<stack>::<project>::<type>::<name>`
3. **Dependency Inference**: 입력 props에 다른 Resource의 Output이 참조되면 자동으로 **DAG 의존성**을 형성
4. **Execution Plan**: `pulumi up` 시점에 DAG를 위상 정렬하여 **병렬 실행**, 단 dependency 순서는 보장
5. **Checkpoint**: 각 Resource의 최종 상태를 State Backend에 JSON Snapshot으로 저장

### 핵심 구성 요소

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Language Host** | 사용자 코드를 별도 프로세스로 실행, RPC로 Engine과 통신 | `pulumi-language-node`, `pulumi-language-python` 등 5개 바이너리. gRPC over stdio로 직렬화 효율 극대화 |
| **Resource Monitor** | 모든 Resource 작업을 RPC로 노출하는 핵심 추상화 계층 | `RegisterResourceOutput`, `GetProvider`, `Invoke` 3개 API. **CSP(Cloud Service Provider)별 SDK를 자동 라우팅** |
| **State Backend** | `*.json` 형태의 Snapshot 저장 및 Lock 관리 | Pulumi Cloud(SaaS, 기본), S3+DynamoDB(자가 호스팅), Azure Blob+CosmosDB, Terraform State 호환 가능(`-tf-state` 옵션) |
| **Provider Plugin** | 클라우드 API를 Pulumi Protocol로 wrap | Terraform Provider를 그대로 재사용하는 **Terraform Bridge** 아키텍처 -> 생태계 200+ Provider 즉시 사용 가능 |
| **Stack** | 단일 코드베이스에 대한 환경별 인스턴스(예: dev/stg/prod) | `Pulumi.<stack>.yaml`로 config 주입, StackReference로 다른 Stack의 Output 참조(마이크로 스택 패턴) |
| **Pulumi Automation API** | IaC를 라이브러리화하여 다른 프로그램에서 호출 | REST API 서버, GitOps 컨트롤러, SRE 도구를 Pulumi로 **메타 프로그래밍** |
| **Policy as Code (CrossGuard)** | 배포 전 Compliance 검증 | OPA(Open Policy Agent) Rego 또는 TypeScript로 정책 정의, 위반 시 배포 차단 |

**핵심 파라미터와 알고리즘**

- **Parallelism**: 기본 `-j 10` (병렬 작업 수), 의존성 DAG 기반 스케줄링
- **Replace vs Update 결정 알고리즘**: Property 변경이 `requiresReplace=true`로 마킹된 필드면 **삭제 후 재생성**(downtime 발생). `aws.ec2.Instance`의 `subnetId`, `instanceType` 변경 시 해당
- **State Locking**: Pulumi Cloud는 자동, S3 Backend는 **DynamoDB Lock Table** 필요 -> 동시성 제어
- **Secrets Handling**: `pulumi config set --secret` 시 **AES-256-GCM**으로 암호화, State 파일에 평문 저장 안 함. KMS 통합 가능
- **Output Promises**: `vpc.id`는 `Output<T>` 타입 -> 런타임 미평가 Promise. `apply()`, `all()`, `interpolate`로 체이닝

- **📢 섹션 요약 비유**: Pulumi Engine은 **"지휘자"** 이고, 사용자 코드는 **"악보"** 다. 악보에 적힌 음표(코드)를 그대로 연주하되(명령형), 지휘자가 실시간으로 음들을 모아 **"어울리는 화성(Resource Graph)"** 을 만들고, 그 화성을 기존 오케스트라(클라우드 API)에 넘긴다.

---

## Ⅲ. 비교 및 연결

### Pulumi vs Terraform vs AWS CDK vs Ansible

| 구분 | **Pulumi** | **Terraform (HCL)** | **AWS CDK (CloudFormation)** | **Ansible** |
| :--- | :--- | :--- | :--- | :--- |
| **언어** | TS/Python/Go/Java/.NET | HCL (DSL) | TS/Python/Java/Go/.NET | YAML + Jinja2 |
| **상태 모델** | Resource Graph (synthesized) | Plan/Apply + State File | CloudFormation Stack (synthesized) | Stateless (선언형 + 절차형 혼합) |
| **멀티 클라우드** | 200+ Provider (TF Bridge) | 3000+ Provider | AWS only | 거의 모든 시스템 |
| **타입 안전성** | ◎ (네이티브) | △ (partial) | ◎ (TS/Python) | ✕ |
| **테스트 도구** | `@pulumi/pulumi`의 `mock` + 표준 프레임워크 | `terraform test`(1.6+ 부분적) | Jest 네이티브 | ansible-lint + Molecule |
| **상태 관리** | Pulumi Cloud/S3/Local | Terraform Cloud/S3/Consul | CloudFormation Stack(자동) | 없음 (수동) |
| **러닝커브** | 중 (개발자 친화) | 중 (DSL 학습) | 중 (CFN 변환 학습) | 낮음 |
| **DRY/모듈화** | ◎ (npm package) | ○ (module variable) | ◎ (construct library) | △ (role/playbook) |
| **Policy as Code** | CrossGuard (TS/Rego) | Sentinel / OPA | cdk-nag | ansible-lint |
| **적합 시나리오** | 동적 로직, 멀티 클라우드, 플랫폼 팀 | 표준 인프라, 대규모 팀, IaC 전문가 | AWS 단일, 개발자 친화 | Config Mgmt, OS 레벨 작업 |

### 상호 보완 아키텍처

```text
   +------------------------------------------------------------------+
   |                    Enterprise IaC 전략 (Hybrid)                    |
   |                                                                   |
   |   Application Tier       Infrastructure Tier       Ops Tier       |
   |   (App Code)             (Cloud Resources)         (OS/Config)   |
   |        |                       |                       |         |
   |        v                       v                       v         |
   |   +---------+           +----------+            +----------+    |
   |   |  Pulumi |           | Terraform|            |  Ansible  |    |
   |   |  (CDK)  |           |  (HCL)   |            | (YAML)   |    |
   |   +----+----+           +-----+----+            +-----+----+    |
   |        |                      |                       |         |
   |        +---------- State Sharing (S3/Pulumi Cloud) ----+         |
   |                            |                                    |
   |                            v                                    |
   |                  +------------------+                            |
   |                  |  GitOps Engine   |  (ArgoCD/Flux)             |
   |                  +------------------+                            |
   +------------------------------------------------------------------+
```

**연계 포인트**

- **Terraform -> Pulumi 마이그레이션**: `pulumi convert --from terraform` 로 HCL을 자동 변환 (단, 100% 호환은 아님)
- **Terraform Bridge**: Pulumi 내부적으로 TF Provider를 그대로 호출하므로 `terraform import`한 리소스를 `pulumi import`로 재사용 가능
- **CI/CD**: GitHub Actions `pulumi/actions`, GitLab CI, Jenkins 등 모든 도구와 통합. `pulumi preview --save` 로 PR 코멘트 자동 게시
- **Kubernetes**: Pulumi의 K8s Provider는 **Helm Chart를 `k8s.helm.v3.Chart` 객체로** 그대로 사용 -> Helm + Pulumi 하이브리드 가능
- **State Sharing**: `terraform_remote_state` ↔ Pulumi의 `StackReference`로 양방향 교차 참조

- **📢 섹션 요약 비유**: 세 도구는 **"건축 현장의 3가지 도구"** 다. Pulumi는 **3D 프린터로 자유 형태 빌딩**, Terraform은 **조립식 키트(레고)**, Ansible은 **인테리어 공사 도구** 다. 큰 골조는 Terraform/CloudFormation, 마감재와 앱 주변은 Pulumi, OS 환경은 Ansible
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 501 / 800

<- **이전**: [500. IaC 테라폼 모듈 상태 관리](/studynote/13_cloud_architecture/06_exam_summary/500_iac_terraform_module_state_management/)
**다음**: [502. IaC Ansible 구성 관리 자동화](/studynote/13_cloud_architecture/06_exam_summary/502_iac_ansible_configuration_management_automati/) ->

---
