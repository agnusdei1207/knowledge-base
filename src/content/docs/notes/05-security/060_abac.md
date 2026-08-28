---
sidebar:
  order: 60
  label: "060. ABAC 속성 기반 접근 제어 (Attribute-Based Access Control)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "동적 다차원 속성 평가 및 세분화 인가 모델 : ABAC (Attribute-Based Access Control & NIST SP 800-162)"
date: "2026-08-26T14:46:51+09:00"
tags:
  - "notes-security"
weight: 60
extra:
  question_no: "060"
  source_status: "기출"
  source_history: "122회, 135회"
  priority: 70
  priority_note: "NIST SP 800-162, 4대 속성(주체/객체/행위/환경), PEP-PDP-PIP-PAP 표준 XACML 3.0 아키텍처, 제로 트러스트 문맥(Context-Aware) 인가, Hybrid RBAC-ABAC"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ABAC(Attribute-Based Access Control, 속성 기반 접근 제어 / NIST SP 800-162)**: 정적인 역할(Role) 대신, 요청 주체(Subject), 대상 자원 객체(Object), 요청 행위(Action), 실시간 환경(Environment)의 다차원 **속성(Attributes)** 들을 사전에 정의된 논리적 정책(Policy) 규칙과 대조하여 런타임에 동적으로 접근 허용/거부(Permit/Deny)를 결정하는 차세대 인가 모델.
- **정적 권한 모델의 문맥 부재 한계(Context Blindness Defect)**: 전통적인 RBAC은 사용자의 직무만 평가할 뿐 접속 시간, 지리적 위치, 디바이스 보안 상태(MDM/EDR 점수), 데이터 기밀 등급 등 실시간 위험 문맥(Context)을 반영하지 못하여 제로 트러스트 환경에서 과도한 신뢰를 부여하는 근본 한계를 내포.

</details>

- 정의/개념: NIST SP 800-162 및 OASIS XACML 3.0 표준에 입각하여 **4대 속성 결합 $\rightarrow$ PEP(정책집행점) 트래픽 차단 $\rightarrow$ PDP(정책결정점) 논리식 평가 $\rightarrow$ PIP(속성정보점) 실시간 속성 동기화 $\rightarrow$ PAP(정책저장소) 룰셋 대조** 를 집행하는 **세분화 동적 인가(Fine-Grained Dynamic Authorization) 아키텍처**
- 배경/필요성: RBAC은 인가 근거를 사전에 고정된 역할에 담아 두는 대신 요청 시점의 위치·시간·단말 상태를 판정에 넣지 못하고 예외마다 역할을 늘리는 비용을 치르므로, 판정 자체를 자원 앞의 **PDP(정책 결정점)** 로 빼내 요청마다 4대 속성을 조회해 계산하는 계층으로 옮길 필요

#### 한줄 요약
- 주체/객체/행위/환경의 4대 속성과 PEP-PDP-PIP-PAP 엔진을 통해 실시간 문맥 인식 동적 인가를 집행한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ABAC 4대 핵심 속성 범주**:
  - **Subject**: 요청자 ID, 부서, 직급, 보안 클리어런스 등.
  - **Object**: 자원 유형, 데이터 기밀성 등급(Secret/Public), 소유자 ID 등.
  - **Action**: `READ`, `WRITE`, `DELETE`, `APPROVE` 등 수행 연산.
  - **Environment**: 접속 시간(Time), 클라이언트 IP/국가, 디바이스 패치 상태, 네트워크 위험도.

</details>

- **극도로 세분화된 인가(Fine-Grained Authorization)**: 논리 연산자(AND, OR, NOT)를 활용하여 "영업부서 과장 AND 사내망 IP AND 업무시간(09~18시) AND 비인가 USB 미연결" 등의 복합 조건 집행
- **표준화된 컴포넌트 분리 (XACML / OPA)**: PEP(게이트웨이), PDP(평가 엔진), PIP(데이터 소스), PAP(정책 저장소)의 느슨한 결합으로 시스템 확장성 보장
- **기본 거부(Default Deny) 원칙 내재화**: 정책 평가 시 속성 누락, 타임아웃, 예외 에러 발생 시 즉시 접근 차단(Deny-Overrides)

#### 한줄 요약
- ABAC은 판정을 사전 계산에서 요청 시점 계산으로 옮겨 표현력을 얻은 대가로 매 요청마다 속성 조회와 정책 평가 비용을 새로 치르며, 그 비용이 곧 캐싱과 하이브리드 설계를 부르는 이유가 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **XACML 3.0 / OPA Rego 표준 컴포넌트**:
  - **PEP (Policy Enforcement Point)**: 트래픽을 가로채어 PDP에 결정을 요청하고 그 결과를 집행하는 게이트웨이.
  - **PDP (Policy Decision Point)**: 정책과 속성을 평가하여 Permit/Deny를 판정하는 핵심 두뇌.
  - **PIP (Policy Information Point)**: HR DB, EDR, CMDB에서 실시간 속성 값을 조회하여 PDP에 제공하는 모듈.
  - **PAP (Policy Administration Point)**: 관리자가 접근 제어 정책을 작성하고 관리하는 저장소.

</details>

```text
[ 클라이언트 접근 요청 (HTTP / API / gRPC) ]
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. PEP (Policy Enforcement Point: API 게이트웨이 / 프록시) ]          │
│  └─ [ 요청 트래픽 인터셉트 ➔ 인가 요청(Authorization Decision Request) 생성]│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (1. 결정 요청)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. PDP (Policy Decision Point: OPA / XACML 평가 엔진) ]               │
│  ├─ PAP 정책 로드: `PAP.getPolicy(Resource_Target)`                     │
│  ├─ PIP 속성 질의: `PIP.getAttributes(Subject, Device, Time)`           │
│  └─ [ 4대 속성 논리 조건식 평가 ➔ Permit / Deny 판정 ]                  │
└──────────────┬──────────────────────────────────────────┬───────────────┘
               │ (2. 속성 조회)                           │ (3. 정책 로드)
               ▼                                          ▼
┌──────────────────────────────┐           ┌──────────────────────────────┐
│ [ 3. PIP (속성 정보점) ]     │           │ [ 4. PAP (정책 저장소) ]     │
│  ├─ 인사 DB (부서/직급)      │           │  ├─ XACML 3.0 정책 XML       │
│  ├─ MDM/EDR (단말 무결성)    │           │  └─ OPA Rego 정책 코드       │
│  └─ 시계열/GeoIP (환경 속성) │           └──────────────────────────────┘
└──────────────────────────────┘
               │ (4. 판정 결과 반환: Permit)
               ▼
[ PEP ➔ 자원 서버(Resource Server)로 트래픽 라우팅 및 감사 로그 기록 ]
```

선의 의미: PEP가 요청을 가로채 PDP로 넘기고, PDP가 PAP 정책과 PIP 속성을 결합하여 평가한 후 PEP가 최종 트래픽을 제어하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **PEP (정책 집행점)** | 자원 진입점에서 트래픽을 가로채 PDP에 결정을 의뢰하고 최종 Permit/Deny를 집행 | Gateway / Agent|
| **PDP (정책 결정점)** | 정책 규칙(PAP)과 속성 데이터(PIP)를 로드하여 불리언 논리식 평가 및 결정 도출 | Engine (OPA/XACML)|
| **PIP (속성 정보점)** | IdP, 인사 DB, MDM, SIEM 등 속성 권위자(Authority)로부터 실시간 속성 동기화 | Attribute Source|
| **PAP (정책 저장소)** | 보안 관리자가 XACML 또는 Rego 언어로 선언한 접근 통제 정책을 저장 및 배포 | Policy Store |
| **속성 권위자 (Authority)** | 주체 및 기기의 진실된 원천 데이터를 보관하는 외부 시스템(Active Directory 등) | Authority |

#### 한줄 요약
- 집행·결정·속성·정책을 떼어 놓은 덕에 애플리케이션 코드를 고치지 않고 정책만 갈아 끼울 수 있지만, 그 대가로 인가 경로에 네트워크 호출이 끼어들어 지연과 장애 전파의 새 지점이 생긴다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **XACML 충돌 해결 알고리즘(Rule Combining Algorithm)**:
  - **Deny-Overrides**: 여러 규칙 중 단 하나라도 `Deny`가 발생하면 최종 결정을 `Deny`로 판정 (보안상 가장 안전).
  - **Permit-Overrides**: 단 하나의 `Permit`이 존재하면 허용.

</details>

```text
1. [요청 수신 및 인터셉트] 사용자가 `GET /api/v1/patient/records/100` 호출 ➔ PEP가 트래픽을 가로채고 요청 정보 추출
            │
            ▼
2. [결정 요청 생성] PEP가 주체(User-ID), 객체(Record-100), 행위(READ), 환경(IP, Time) 정보를 PDP로 전달
            │
            ▼
3. [속성 동기화 (PIP 조회)] PDP가 부족한 동적 속성(사용자의 보안 인가 등급, 단말 백신 가동 여부)을 PIP에 질의하여 확보
            │
            ▼
4. [정책 평가 (PAP 대조)]
    ├─ PDP가 PAP에서 해당 자원 정책 로드: `IF Subject.Dept == 'Medical' AND Env.Time in (09:00..18:00) AND Device.Health == 'OK'`
    └─ 충돌 해결 알고리즘(Deny-Overrides)을 적용하여 전체 룰셋 계산 ➔ [조건 완전 일치 시 Permit 판정]
            │
            ▼
5. [인가 집행 및 감사] PDP가 PEP로 `Permit` 결과 응답 ➔ PEP가 백엔드 데이터베이스로 요청을 중계하고 SIEM 로그 기록
```

**동작 원리**

1. **상시 검증 및 가로채기**: 모든 인바운드 트래픽이 비즈니스 로직에 도달하기 전 PEP를 통과하도록 강제
2. **동적 속성 주입**: 정적 토큰에 기록되지 않은 실시간 컨텍스트(단말 보안 상태 등)를 PIP를 통해 런타임 결합
3. **선언적 정책 분리**: 애플리케이션 소스코드 수정 없이 PAP 정책 파일만 변경하여 전사 인가 룰 갱신
4. **엄격한 실패 안전성(Fail-Safe)**: PIP 통신 단절이나 속성 불일치 시 즉각 Deny로 처리하여 비인가 접근 방지
5. **엔터프라이즈 감사 추적**: 판정에 사용된 4대 속성 스냅샷 전체를 감사 로그에 기록하여 사후 추적성 확보

#### 한줄 요약
- 판정이 토큰에 담긴 과거 정보가 아니라 요청 순간 조회한 속성으로 이루어지므로 정확성이 속성의 신선도에 종속되고, 조회가 실패하면 안전한 쪽인 Deny로 기울어 가용성을 대가로 치른다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **접근 제어 모델 3대 패러다임 비교**: RBAC(역할 기반), ABAC(속성 기반), 하이브리드(Hybrid RBAC-ABAC)의 비교.

</details>

| 비교 항목 | 역할 기반 접근 제어 (RBAC) | 속성 기반 접근 제어 (ABAC) | 하이브리드 모델 (Hybrid RBAC-ABAC) |
|:---|:---|:---|:---|
| **핵심 통제 기준** | **사용자에게 할당된 정적 직무 역할(Role)**| **주체, 객체, 행위, 환경 속성의 논리식** | **1차 거시적 Role + 2차 미시적 Context** |
| **정책 유연성 및 정밀도**| 보통 (정적 직무 위주 세밀한 조건 제약) | **최상 (시간, 위치, 기기 등 무제한 표현)** | **최상 (역할의 간결함 + 속성의 정밀함)** |
| **관리 오버헤드** | 역할 폭발(Role Explosion) 발생 위험 | 정책 문법(XACML/Rego) 설계 난이도 높음 | **역할 개수 80% 감축 및 정책 복잡도 완화**|
| **엔진 성능 오버헤드**| **극히 낮음 (단순 역할-권한 맵핑 조회)** | 높음 (매 요청마다 실시간 PIP/PDP 연산) | **보통 (Role 1차 필터링으로 PDP 부하 분산)**|
| **제로 트러스트 적합성**| 낮음 (문맥 인식 불가) | **완벽 (실시간 동적 신뢰 평가 최적)** | **매우 높음 (엔터프라이즈 실무 최적 표준)**|

#### 한줄 요약
- 셋은 인가 근거를 언제 계산하느냐의 스펙트럼이며, 사전 고정은 싸고 거칠고 요청 시점 계산은 정밀하고 비싸므로 실무는 역할로 1차를 걸러 PDP 부하를 줄이는 하이브리드로 수렴한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cloud-Native ABAC: OPA (Open Policy Agent) & Rego**: 복잡한 XML 기반 XACML의 성능 한계를 극복하기 위해, 경량 Go 엔진 기반으로 JSON 데이터를 평가하는 선언형 정책 언어(Rego)를 사용하는 클라우드 네이티브 표준 인가 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수백 개의 속성을 실시간 평가(PDP)하고 PIP를 매번 호출하여 **API 응답 지연(Latency 500ms 이상) 장애 발생** | **OPA(Open Policy Agent) 기반 로컬 인메모리 캐싱 도입 및 1차 RBAC 필터링 후 2차 ABAC 적용(Hybrid)** | 인가 판정 시간 5ms 이내로 단축 및 대용량 트래픽 처리 성능 99% 확보 |
| PIP가 외부 인사 DB나 MDM 정보를 장기 캐싱하여 **퇴사 직후의 직원이 여전히 시스템에 접근 승인되는 오류** | **속성 캐시 TTL을 1~5분 이내로 단축하고, 퇴사/격리 이벤트 수신 시 웹훅(Webhook) 기반 캐시 즉시 무효화** | 속성 신선도(Freshness) 100% 보장 및 구형 데이터 기반 비인가 접근 완전 차단 |
| 벤더별로 상이한 비표준 조건문 문법으로 인해 **멀티 클라우드 및 이종 시스템 간 정책 연동이 불가능한 파편화** | **OASIS XACML 3.0 및 OPA Rego 표준 규격 채택, PEP-PDP 간 RESTful 표준 API 통신 인터페이스 강제** | 벤더 종속성(Lock-in) 탈피 및 전사 통합 제로 트러스트 인가 거버넌스 확립 |

#### 한줄 요약
- OPA/하이브리드로 성능 지연을 단축하고, 캐시 무효화로 속성 신선도를 보장하며, OPA Rego 표준으로 파편화를 극복한다.

## Ⅶ. 결론

- 안정적 직무는 RBAC, 동적 위험은 **ABAC**으로 판정하고 기본 거부 적용

#### 한줄 요약
- 4대 속성 다차원 결합과 PEP-PDP 아키텍처 및 하이브리드 OPA 모델을 통해 제로 트러스트 동적 인가를 완성한다.
