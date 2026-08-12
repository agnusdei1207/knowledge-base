---
sidebar:
  order: 63
  label: "063. 카나리 배포•블루-그린 배포 (Canary Blue-Green Deployment)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "카나리 배포•블루-그린 배포 (Canary Blue-Green Deployment)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 63
extra:
  question_no: "063"
  source_status: "기출"
  source_history: "132회, 138회"
  priority: 70
  priority_note: "132•138회 반복, 점진 배포 전략 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Zero-Downtime Deployment (무장애 배포)**: 신규 버전 서비스 배포 시, 기존 서비스의 중단 시간(Downtime) 없이 24x365 가용성을 유지하며 버전을 전환하는 배포 기술.
- **Canary Deployment**: 광산의 탄광 새(Canary) 위험 감지 원리에서 유래하여, 신규 버전을 전체 트래픽 중 소수(e.g., 5% $\rightarrow$ 10% $\rightarrow$ 100%) 유저에게 점진적으로 노출시키는 가중치 배포 방식.
- **Blue-Green Deployment**: 현재 가동 중인 구버전 환경(Blue)과 동일한 규모의 신버전 환경(Green)을 1:1로 띄워두고, 로드밸런서의 L7/L4 라우팅 스위칭을 통해 1초 만에 일괄 전환하는 배포 방식.

</details>

- 정의/개념: 클라우드 컴퓨팅 및 컨테이너 오케스트레이션 환경에서 서비스를 중단하지 않고 신버전으로 유연하게 이행하기 위한 2대 대표 무장애 배포 전략인 **Canary & Blue-Green Deployment**
- 배경/필요성: 단일 서버 일괄 덮어쓰기(Re-deploy)로 인한 서비스 장애 타격 방지, 배포 실패 시 1초 만에 구버전으로 스위칭 원복하는 고가용성 확보 요구성

#### 한줄 요약

- 카나리 배포의 점진 노출과 블루-그린 배포의 병렬 환경 전환이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Blast Radius (장애 영향 반지름)**: 신규 버전 배포 시 버그가 발생했을 때 영향을 받는 유저 및 시스템의 범위로, Canary 배포는 이 영향 범위를 극도로 제어.
- **Routing Switch**: 로드밸런서(Nginx, ALB)나 Service Mesh(Istio)를 활용하여 엔드포인트 트래픽 방향을 순간적으로 100% 교체하는 작업.

</details>

- **Blast Radius (장애 타격 범위)** 극소화 및 가중치 트래픽 라우팅 (**Canary**)
- 인프라 자원 2배 동시 점유 및 순간 100% 라우팅 스위칭 (**Blue-Green**)
- 배포 실패 시 L4/L7 라우터 전환만으로 **1초 만에 Instant Rollback** 달성

#### 한줄 요약

- 점진 노출과 즉시 전환의 위험 통제 방식 차이가 핵심이다.

## Ⅲ. 구조 및 구성요소 (Blue-Green 대 Canary)

<details><summary>핵심 용어</summary>

- **Ingress Controller / Service Mesh**: Kubernetes 환경에서 Blue/Green Pod 또는 Canary Pod 군으로 트래픽 비율(Weight)을 정밀하게 분사 제어하는 엣지 라우팅 엔진.

</details>

```text
[Blue-Green 배포 구조]
Load Balancer (Switch 100%)
   ├──► Blue Environment (Old Version 1.0 - Active)
   └──► Green Environment (New Version 2.0 - Idle ──► Active)

[Canary 배포 구조]
Ingress Router (Weight Split)
   ├──► 95% Traffic ──► Stable Pods (v1.0)
   └──►  5% Traffic ──► Canary Pods (v2.0 - Prometheus 감시중)
```

선의 의미: Blue-Green은 로드밸런서가 Blue/Green 전체를 100% 스위칭하고, Canary는 Ingress가 95:5 비율로 트래픽을 분사 노출시키는 구조.

| 배포 아키텍처 | 핵심 구조 및 동작 원리 | 장점 및 한계점 |
|:---|:---|:---|
| **Blue-Green** | 구버전(Blue)과 신버전(Green) 인프라 1:1 구성 후 **Router 100% 스위칭** | **장점: 롤백 1초 완결, 배포 절차 단순 / 한계: 인프라 자원 비용 2배 소요** |
| **Canary** | 전체 트래픽 중 소수(5%)만 신버전에 쏠리게 **Weight Routing** 후 점진 확장 | **장점: 장애 타격 범위(Blast Radius) 극소화 / 한계: 트래픽 제어 복잡도 증가** |

#### 한줄 요약

- 배포 제어기, 트래픽 라우터, 관측 시스템의 폐루프 제어 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Automated Canary Analysis (ACA)**: Kayenta/Flagger 도구를 사용하여 Canary Pod의 런타임 지표(Error rate, Latency)를 정상 Pod 지표와 실시간 통계 비교하는 자동 분석 기법.

</details>

```text
┌──────────────────────────────┐
│ 신규 버전 바이너리 빌드      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ [Blue-Green] Green 100% 스위치│ [Canary] 5% 가중치 노출
│ 1. 롤백 시 Blue 100% 원복    │ 1. ACA 지표 비교 (Kayenta)
│ 2. 정상 시 Blue 환경 파기    │ 2. 이상 발생 시 5% 즉시 차단
└──────────────┬───────────────┘ 3. 정상 시 10% $\rightarrow$ 100% 노출
               ▼
     [무장애 릴리스 완결]
```

### 동작 원리

1. **Canary 동작**: Canary Pod 1개 배치 후 Ingress Weight 5% 설정 $\rightarrow$ 10분간 에러율 관측 $\rightarrow$ 이상 없을 시 10%, 25%, 50%, 100% 점진 승격 $\rightarrow$ 기존 v1.0 Pod 삭제.
2. **Blue-Green 동작**: Green 환경에 v2.0 미리 100% 프로비저닝 $\rightarrow$ 헬스체크 Pass 확인 $\rightarrow$ Load Balancer 타깃 그룹을 Blue에서 Green으로 100% 순간 스위칭 $\rightarrow$ 문제 시 Blue로 즉시 스위칭 원복.

#### 한줄 요약

- 카나리 확대•복귀와 블루-그린 전환•복귀의 제어 흐름이 핵심이다.

## Ⅴ. 종류 및 비교 (무장애 배포 3대 기법 비교)

<details><summary>핵심 용어</summary>

- **Rolling Update vs Blue-Green vs Canary**: Rolling은 Pod를 하나씩 순차 교체(자원 추가 0), Blue-Green은 1:1 일괄 전환(자원 추가 100%), Canary는 소수 비율 노출 후 확대(자원 추가 소량).

</details>

| 비교 항목 | Rolling Update (롤링 배포) | Blue-Green Deployment | Canary Deployment |
|:---|:---|:---|:---|
| 배포 방식 | 기존 Pod를 하나씩 인플레이스 순차 교체 | 1:1 별도 환경 생성 후 **100% 순간 스위칭**| **소수(5%) 트래픽 노출 후 단계적 확대** |
| 자원 오버헤드 | 매우 낮음 (추가 자원 불필요) | **매우 높음 (동일 자원 2배 100% 필요)** | 소량 필요 (Canary Pod 분량만큼) |
| 구/신버전 공존| 배포 진행 중 **구/신버전 트래픽 혼재** | **공존 없음 (순간 100% 스위칭)** | **배포 기간 동안 intentional 공존** |
| 롤백 속도 | 느림 (역순으로 하나씩 되돌려야 함) | **매우 빠름 (1초 만에 Router 스위칭)** | **매우 빠름 (Canary 라우팅 0% 변경)** |

#### 한줄 요약

- 점진 위험 검증에는 카나리 배포, 환경 전환 복구에는 블루-그린 배포가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Expand-Contract Pattern (DB 스키마 하위 호환)**: 구버전과 신버전이 트래픽 전환 과정에서 DB를 공유할 때, 칼럼 삭제/변경 시 구버전 애플리케이션이 파괴되지 않게 2단계로 나누어 DB 스키마를 변경하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 무장애 배포 중 DB 스키마 변경 시 구버전 앱 붕괴 | **Expand-Contract Pattern (2단계 DB 스키마 변경)** | DB 트랜잭션 호환성 보장 |
| Blue-Green 배포 시 인프라 비용 2배 폭증 | **Kubernetes 기반 HPA & 배포 완료 후 Blue 환경 파기** | 자원 비용 최적화 |
| Canary 배포 시 유저 세션 튕김 현상 | **Redis 세션 외부화 (Stateless Architecture)** | 유저 경험(UX) 보존 |

> 사례: **Kubernetes + Argo Rollouts + Istio + Flagger (Automated Canary Analysis)** 조화 구축

#### 한줄 요약

- 확장-축소 변경, 최소 표본, 버전별 지표, 보상 절차가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **무장애 배포 선택 기준(Zero-Downtime Deployment Standards)**: 인프라 자원 예산, 롤백 속도 요건 및 무장애 가용성에 의거한 체계.

</details>

- **무장애 배포 선택 기준**에 따라 인프라 예산 충분 시 **Blue-Green**, 트래픽 리스크 최소화 시 **Argo Rollouts Canary** 수용

#### 한줄 요약

- 관찰 방식과 복구 방식에 맞는 배포 전략 선택 기준이 핵심이다.
