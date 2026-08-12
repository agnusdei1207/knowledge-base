---
sidebar:
  order: 64
  label: "064. 피처 플래그 (Feature Flag)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "피처 플래그 (Feature Flag)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 64
extra:
  question_no: "064"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "138회 기출, 배포 분리•기능 제어 현안"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Feature Flag (피처 플래그, Feature Toggle)**: 소스코드의 변경이나 재배포(Re-deployment) 없이, 런타임 조건문(if-else) 또는 원격 중앙 통제판(Console)을 통해 특정 기능의 활성화/비활성화(ON/OFF)를 즉각 전환하는 소프트웨어 기법.
- **Decoupling Deployment from Release**: 소스코드를 실운영 환경에 기술적으로 배치하는 '배포(Deployment)'와, 해당 기능을 최종 사용자에게 노출시키는 '릴리스(Release)' 활동을 시점상 완전 분리하는 아키텍처 사상.
- **Kill Switch**: 장애 발생 시 소스 수정이나 CI/CD 재배포 없이, 피처 플래그 콘솔에서 OFF 버튼 클릭 1초 만에 해당 장애 기능을 즉시 비활성화(Disable)시키는 긴급 차단 장치.

</details>

- 정의/개념: 애플리케이션의 재배포 없이 런타임 시점에 특정 기능의 온/오프(ON/OFF) 및 타깃 사용자군별(Cohort) 노출 여부를 동적으로 통제하는 **Feature Flag (Feature Toggle)**
- 배경/필요성: 배포와 릴리스의 시점적 결합으로 인한 릴리스 지연 방지, 장애 발생 시 재배포 없이 즉각 긴급 차단(Kill Switch) 및 A/B 테스트 환경 구축 요구성

#### 한줄 요약

- 피처 플래그로 실행 중 기능 경로를 통제하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Targeting & Segmentation**: 사용자 ID, IP, 지역, 유료 등급 등의 속성에 따라 피처 플래그를 특정 타깃 사용자군(Cohort)에게만 핀포인트로 선별 노출시키는 기법.
- **Trunk-Based Development Enabler**: 미완성된 기능의 코드를 메인(main) 브랜치에 미리 가려놓고(Flag OFF) 지속적으로 통합(CI)할 수 있게 해주는 핵심 토대.

</details>

- **Decoupling Deployment from Release (배포와 릴리스의 완전 분리)**
- 런타임 제어를 통한 **Kill Switch (긴급 차단)** 및 **Targeting / Segmentation**
- **Trunk-Based Development** 촉진 및 **A/B Testing** 기반 수용성 검증

#### 한줄 요약

- 대상 규칙의 유연성과 만료 플래그 누적 방지의 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소 (피처 플래그 4대 유형 및 아키텍처)

<details><summary>핵심 용어</summary>

- **LaunchDarkly / Unleash**: 전사 피처 플래그를 중앙 관리하고 타깃팅 룰셋(Ruleset)을 각 애플리케이션 SDK로 실시간(WebSocket) 분사하는 대표적 SaaS/오픈소스 플래그 플랫폼.

</details>

```text
[개발자 / PM 콘솔] ──► [중앙 Flag 관리 플랫폼 (LaunchDarkly/Unleash)]
                                    │
                                    ▼ (WebSocket / Config Sync)
 [App Client Request] ──► [App Node (Flag SDK Evaluation)]
                                    │
                       ┌────────────┴────────────┐
                       ▼ (Flag ON)               ▼ (Flag OFF)
               [New Feature Path]        [Old / Default Path]
```

선의 의미: 중앙 Console에서 Flag 룰셋이 변경되면 App Node의 SDK가 동적으로 평가(Evaluate)하여 New Feature와 Default 코드 경로 중 하나를 인라인 렌더링하는 아키텍처.

| 분류 (Category) | 피처 플래그 유형 | 유효 수명 (Lifetime) | 주요 용도 및 대표 적용 사례 |
|:---|:---|:---|:---|
| **Release Toggles** | 릴리스 플래그 | 단기 (수일 ~ 수주) | 미완성 기능의 메인 브랜치 안전 병합 및 점진적 릴리스 |
| **Experiment Toggles**| 실험 플래그 | 단기 (수주 ~ 수개월)| **A/B 테스트 및 데이터 기반 유저 반응 실험** |
| **Ops Toggles** | 운영 플래그 | 장기 (시스템 수명 내내)| **장애 시 기능 즉시 억제 (Kill Switch), 성능 튜닝** |
| **Permission Toggles**| 권한 플래그 | 장기 (시스템 수명 내내)| **VIP 유저 / 유료 회원 전용 프리미엄 기능 제한 노출** |

#### 한줄 요약

- 설정 저장소, 평가 모듈, 기능 경로, 감사 기록의 연결 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Flag Evaluation**: 요청을 보낸 사용자의 컨텍스트(Context: user_id, location, plan)를 기반으로 피처 플래그 SDK가 Boolean(true/false) 또는 String(Variant)으로 런타임 평가하는 연산.

</details>

```text
┌──────────────────────────────┐
│ User HTTP Request 수신       │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. User Context 추출 (ID,Role)│
│ 2. Flag SDK 런타임 Evaluation│
│ 3. Target Rule 매칭 (95:5)   │
├──────────────┬───────────────┤
│ (Flag = True)│ (Flag = False)│
│              ▼               ▼
│  [New Feature 로직]   [Legacy 로직]
└──────────────────────────────┘
```

### 동작 원리

1. **Context Extraction**: 요청에서 `user_id`, `client_ip`, `membership_tier` 인출.
2. **Flag SDK Evaluation**: 인메모리 피처 플래그 SDK가 규칙 룰셋 대조.
3. **Branching Execution**: `Flag = True`일 시 신규 결제 UI 실행, `False`일 시 기존 결제 UI 파이프라인 집행.
4. **Kill Switch 발동**: 신규 결제 UI 장애 발생 시, PM이 LaunchDarkly 콘솔에서 Flag `OFF`로 변경 1초 만에 기존 UI로 전원 원복.

#### 한줄 요약

- 요청 속성•대상 규칙 평가와 안전 기본값 기반 기능 경로 실행이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Canary Deployment vs Feature Flag**: Canary는 L7 Ingress/Service Mesh 수준에서 인프라 네트워크 트래픽 비율을 나누는 반면, Feature Flag는 소스코드 내부 if-else 문 단위로 유저 속성(Targeting) 기반 렌더링.

</details>

| 비교 항목 | Canary Deployment (인프라 레벨) | Feature Flag (소프트웨어 코드 레벨) |
|:---|:---|:---|
| 제어 계층 | L7 Ingress Router / Service Mesh 인프라 | **소프트웨어 애플리케이션 코드 (if-else)** |
| 분기 조건 | 단순 IP/네트워크 가중치 비율 (90:10) | **유저 ID, 회원 등급, 국가, 유효 기간 등 세분화** |
| 제어 주체 | DevOps 엔지니어 | **소프트웨어 개발자, 기획자(PM), 마케터** |
| 인프라 의존성 | K8s, Istio 등 고도화 인프라 필요 | **인프라 무관 (코드 및 SDK 설치만으로 즉시 구동)**|

#### 한줄 요약

- 릴리스 플래그와 실험 플래그는 종료 후 제거하고 운영 플래그는 지속 점검한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Technical Debt & Flag Pollution**: 릴리스가 끝난 수십 개의 피처 플래그 조건문을 소스코드에서 삭제하지 않고 방치하여 코드 읽기 가독성을 훼손하고 테스트 수명복잡도를 높이는 기술 부채.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수십 개의 플래그 조건문 방치로 인한 기술 부채 (**Flag Pollution**) | **Flag 만료일(TTL) 지정 및 JIRA 릴리스 완료 시 Cleanup 이슈 자동 생성** | 코드 깔끔성 보장 |
| Flag SDK 평가 통신 장애로 애플리케이션 먹통 | **In-memory Local Caching & Fallback Default 값 설정** | 런타임 안정성 보장 |
| 피처 플래그 조건문 중첩으로 인한 테스트 가짓수 폭증 | **1개 메서드 내 최대 1개 Flag만 사용 (Single Toggle Principle)** | 테스트 복잡도 통제 |

> 사례: **LaunchDarkly / OpenFeature (CNCF 표준) + Spring Boot 3** 피처 플래그 통제 구축

#### 한줄 요약

- 안전 기본값, 역할 기반 접근통제, 의존 제한에 기반한 통제가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **피처 플래그 관리 기준(Feature Flag Management Standards)**: 플래그 수명주기(TTL), 클린업 절차 및 CNCF OpenFeature 표준 수용성에 의거한 체계.

</details>

- **피처 플래그 관리 기준**에 따라 배포-릴리스 분리 및 A/B 테스트 도입 시 **OpenFeature / LaunchDarkly + Flag Cleanup** 수용

#### 한줄 요약

- 임시 플래그 제거와 비상 플래그 유지의 플래그 수명주기 선택 기준이 핵심이다.
