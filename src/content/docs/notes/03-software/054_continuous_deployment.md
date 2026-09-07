---
sidebar:
  order: 54
  label: "054. 지속적 배포 (CD)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "지속적 배포 (Continuous Deployment)"
date: "2026-09-07T10:00:00+09:00"
tags:
  - "notes-software"
weight: 54
extra:
  question_no: "054"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "138회 기출, 자동 배포•검증 흐름"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Continuous Deployment(지속적 배포)**: 개발자가 작성한 코드가 CI 테스트 및 품질 게이트를 통과하면 사람의 수동 개입(No-Touch) 없이 즉시 프로덕션 환경에 자동 릴리즈되는 체계.
- **가드레일 지표(Guardrail Metrics)**: 배포 직후 P99 응답시간, HTTP 5xx 에러율 등 핵심 지표를 실시간 감시하여 비정상 시 자동 롤백을 트리거하는 안전 장치.

</details>

- 정의/개념: CI 검증을 통과한 아티팩트를 사람의 수동 개입 없이 **프로덕션 환경에 즉각 릴리즈(No-Touch)** 하는 완전 자동화 배포 전략
- 배경/필요성: 수동 승인 절차가 유발하는 **대규모 배치(Batch) 배포 누적, 릴리즈 리드타임 지연 및 장애 원인 특정 난항 한계**

#### 한줄 요약
- 품질 게이트, 점진적 카나리 노출, 자동 롤백을 갖춘 무인 자동 배포 체계다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **점진적 전달(Progressive Delivery)**: 전체 사용자에게 일괄 배포하지 않고 카나리(1% $\to$ 10% $\to$ 100%) 및 기능 플래그로 위험을 제어하며 점진 배포하는 기법.
- **Auto-Rollback**: 프로덕션 이상 감지 시 사람의 판단 대기 없이 이전 안정 버전으로 수 초 내 자동 롤백하는 메커니즘.

</details>

- 수동 승인 단계를 완전히 제거한 **No Human Touch** 무인 자동 배포
- **소규모 배치(Small Batch)** 단위의 고빈도 배포를 통한 장애 파급 범위(Blast Radius) 극소화
- **Argo Rollouts 기반 가드레일 감시 및 이상 시 Auto-Rollback** 즉시 수행

#### 한줄 요약
- 무인 배포는 리드타임을 줄이는 대신 사람의 판단을 지표와 가드레일에 위임하므로, 관측 품질이 곧 배포 안전성의 상한이 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Argo Rollouts**: Kubernetes 환경에서 Blue/Green, Canary, 실험적 배포 및 메트릭 기반 자동 롤백을 지원하는 고급 배포 컨트롤러.

</details>

```text
[지속적 배포 CD 체계]
  │
  ├─ [GitOps 배포 엔진] (ArgoCD·선언적 K8s 자동 동기화)
  │
  ├─ [카나리 트래픽 제어기] (Ingress/Service Mesh 점진 개방)
  │
  ├─ [관측성 플랫폼] (Prometheus·5xx 에러율 및 P99 감시)
  │
  └─ [자동 롤백 엔진] (Argo Rollouts·가드레일 위반 시 복구)
```
- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| GitOps 배포 엔진 (ArgoCD) | Git 저장소의 매니페스트 변경을 감지하여 **프로덕션 클러스터에 즉시 자동 배포** |
| 카나리 트래픽 제어기 | 신규 버전에 트래픽을 **1% $\to$ 10% $\to$ 100% 점진적으로 개방** |
| 관측성 플랫폼 (Prometheus) | 프로덕션 환경의 **HTTP 5xx 에러율 및 P99 지연시간 실시간 수집** |
| 자동 롤백 엔진 (Argo Rollouts) | 가드레일 지표 위반 시 즉시 트래픽을 차단하고 **이전 안정 Pod로 즉각 롤백** |

#### 한줄 요약
- 관측 플랫폼이 배포 판정의 근거를 만들고 롤백 엔진이 그 판정을 집행하므로, 지표가 없으면 자동 배포는 자동 사고로 바뀐다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **AnalysisTemplate**: Argo Rollouts에서 프로메테우스 쿼리(`http_requests_total{status=~"5.*"}`)를 주기적으로 실행해 배포 성공 여부를 판정하는 매트릭 정의서.

</details>

```text
개발자 Git 커밋 푸시 -> CI 파이프라인 및 품질 게이트 통과 완료
        │
   ArgoCD가 프로덕션 K8s 클러스터에 신규 버전 컨테이너 자동 배포
        │
   Argo Rollouts가 전체 트래픽의 5%를 신규 카나리 Pod로 라우팅
        │
   Prometheus가 5분간 카나리 Pod의 에러율 및 지연시간 수집
        │
   에러율이 가드레일 임계치(0.1% 이하)를 충족하는가?
   ┌────┴─────┐
  예           아니오 (에러율 급증)
   │             │
트래픽 20% -> 100%   [Auto-Rollback 실행]
점진 확대 후 승격 완료  신규 Pod 즉시 제거 및 구버전 100% 복구
```

#### 한줄 요약
- 카나리 비율이 낮을수록 노출 위험은 줄지만 통계적 판정에 필요한 시간은 늘어나므로, 배포 속도와 판정 신뢰도가 이 지점에서 맞바뀐다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Continuous Delivery vs Continuous Deployment**: 수동 승인 버튼을 누르는 Delivery와 모든 과정이 100% 무인 자동화된 Deployment.

</details>

| 비교 항목 | Continuous Delivery (지속적 제공) | Continuous Deployment (지속적 배포) |
|:---|:---|:---|
| 프로덕션 배포 방식 | **관리자/운영자 수동 승인 후 배포** | **무인 완전 자동 배포 (No-Touch)** |
| 배포 빈도 | 주 1~2회 또는 격주 정기 배포 | **일 수십 회~수백 회 수시 배포** |
| 장애 복구 전략 | 수동 롤백 및 핫픽스 빌드 | **Prometheus 메트릭 기반 자동 롤백** |
| 전제 조건 | 단위/통합 테스트 자동화 | **고도화된 관측성, 카나리 및 자동 롤백 체계** |
| 주 도메인 | 은행, 증권, 원전, 의료 등 고위험군 | **글로벌 SaaS, 이커머스, OTT 스트리밍** |

#### 한줄 요약
- 고위험 규제 환경은 수동 승인의 Delivery, 고속 혁신 SaaS는 무인 자동 배포 Deployment를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Expand-Contract 패턴**: DB 스키마 변경 시 구버전과 신버전이 동시에 작동할 수 있도록 컬럼을 추가(Expand)한 후 구버전이 제거되면 정리(Contract)하는 무중단 마이그레이션 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| DB 스키마 변경 시 롤백 시점의 하위 호환성 파괴 | **Expand-Contract 패턴 기반 2단계 무중단 DB 마이그레이션** | 신/구버전 동시 수용 및 롤백 시 2차 장애 방지 |
| 미검증 코드의 무인 배포로 인한 대규모 장애 위험 | **Argo Rollouts 기반 카나리 점진 배포 및 에러율 자동 롤백** | 장애 영향 범위 5% 이내 국소화 |
| 특정 고객 그룹 대상 사전 검증 불가 | **기능 플래그(Feature Flag: LaunchDarkly)** 결합 | 내부 임직원/베타 테스터 선별 노출 |
| 배포 성공 여부 판단 기준의 모호성 | **P99 레이턴시, 5xx 에러율 기반 SLO 가드레일 정의** | 정량적 데이터 기반 무인 승격/롤백 자동화 |

#### 한줄 요약
- 지속적 배포는 배포 단위를 줄여 위험을 낮추는 대신 판단을 자동 검증에 전부 위임하므로, SLO 가드레일과 자동 롤백이 사람의 승인을 대신할 만큼 촘촘해야 성립한다.

## Ⅶ. 결론

- 빅테크 및 고빈도 클라우드 네이티브 서비스의 **최상위 지속적 가치 전달(Continuous Deployment) 표준 패러다임**으로 확립되었으며, 실무 구축 시에는 **GitOps(ArgoCD) 기반 무인 자동 배포, 점진적 카나리 롤아웃(Argo Rollouts), 실시간 SLO(5xx 에러율/P99 지연시간) 가드레일 감시 및 Auto-Rollback, DB 하위 호환성을 보장하는 Expand-Contract 패턴**을 필수적으로 결합하여 안전성을 담보

#### 한줄 요약
- 지속적 배포(Continuous Deployment)는 무인 자동화와 점진적 전달(Progressive Delivery)을 통해 출시 속도와 안정성을 동시에 극대화하는 최신 배포 패러다임이다.
