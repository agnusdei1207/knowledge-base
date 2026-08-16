---
sidebar:
  order: 63
  label: "063. 카나리 배포•블루-그린 배포 (Canary Blue-Green Deployment)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "카나리 배포•블루-그린 배포 (Canary Blue-Green Deployment)"
date: "2026-08-13T16:31:00+09:00"
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

<details><summary>용어 설명</summary>

- **Zero-Downtime Deployment (무장애 배포)**: 신규 버전 서비스 배포 시, 기존 서비스의 중단 시간(Downtime) 없이 24x365 가용성을 유지하며 버전을 전환하는 배포 기술.
- **Canary Deployment**: 광산의 탄광 새(Canary) 위험 감지 원리에서 유래하여, 신규 버전을 전체 트래픽 중 소수(e.g., 5% $\rightarrow$ 10% $\rightarrow$ 100%) 유저에게 점진적으로 노출시키는 가중치 배포 방식.
- **Blue-Green Deployment**: 현재 가동 중인 구버전 환경(Blue)과 동일한 규모의 신버전 환경(Green)을 1:1로 띄워두고, 로드밸런서의 L7/L4 라우팅 스위칭을 통해 1초 만에 일괄 전환하는 배포 방식.

</details>

- 정의/개념: 클라우드 컴퓨팅 및 컨테이너 오케스트레이션 환경에서 서비스를 중단하지 않고 신버전으로 유연하게 이행하기 위한 2대 대표 무장애 배포 전략인 **Canary & Blue-Green Deployment**
- 배경/필요성: 일괄 덮어쓰기는 **전체 장애•복귀 지연** 위험 유발

#### 한줄 요약

- 카나리 배포의 점진 노출과 블루-그린 배포의 병렬 환경 전환이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Blast Radius (장애 영향 반지름)**: 신규 버전 배포 시 버그가 발생했을 때 영향을 받는 유저 및 시스템의 범위로, Canary 배포는 이 영향 범위를 극도로 제어.
- **Routing Switch**: 로드밸런서(Nginx, ALB)나 Service Mesh(Istio)를 활용하여 엔드포인트 트래픽 방향을 순간적으로 100% 교체하는 작업.

</details>

- **Blast Radius (장애 타격 범위)** 극소화 및 가중치 트래픽 라우팅 (**Canary**)
- 병렬 환경과 일괄 라우팅 전환(**Blue-Green**)
- 배포 실패 시 L4/L7 라우터 기반 **즉시 복귀**

#### 한줄 요약

- 점진 노출과 즉시 전환의 위험 통제 방식 차이가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Ingress Controller / Service Mesh**: Kubernetes 환경에서 Blue/Green Pod 또는 Canary Pod 군으로 트래픽 비율(Weight)을 정밀하게 분사 제어하는 엣지 라우팅 엔진.

</details>

```text
 [배포 제어기] ─── [트래픽 라우터]
        │                   │
        └──── [관측 시스템]
```

선의 의미: Blue-Green은 로드밸런서가 Blue/Green 전체를 100% 스위칭하고, Canary는 Ingress가 95:5 비율로 트래픽을 분사 노출시키는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 배포 제어기 | 신규 버전 배치와 승격•복귀 상태 관리 |
| 트래픽 라우터 | 버전별 트래픽 비율 또는 대상 전환 |
| 관측 시스템 | 버전별 오류율•지연시간과 가드레일 측정 |

#### 한줄 요약

- 배포 제어기, 트래픽 라우터, 관측 시스템의 폐루프 제어 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Automated Canary Analysis (ACA)**: Kayenta/Flagger 도구를 사용하여 Canary Pod의 런타임 지표(Error rate, Latency)를 정상 Pod 지표와 실시간 통계 비교하는 자동 분석 기법.

</details>

```text
┌──────────────────────────────┐
│ 신규 버전 바이너리 빌드      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 배포 전략 선택            │
│ 2. 신규 버전 배치            │
│ 3. 트래픽 노출•전환          │
│ 4. 가드레일 지표 판정        │
│ 5. 확대•확정 또는 복귀       │
└──────────────┬───────────────┘
               ▼
     [무장애 릴리스 완결]
```

### 동작 원리

1. 배포 전략 선택: 자원 여유•영향 범위•복귀 방식 평가.
2. 신규 버전 배치: 카나리 또는 Green 환경에 버전 배치.
3. 트래픽 노출•전환: 점진 비율 또는 대상 환경 전환.
4. 가드레일 지표 판정: 기준 버전과 오류율•지연 비교.
5. 확대•확정 또는 복귀: 정상은 승격, 이상은 구버전 복귀.

#### 한줄 요약

- 카나리 확대•복귀와 블루-그린 전환•복귀의 제어 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Rolling Update vs Blue-Green vs Canary**: Rolling은 Pod를 하나씩 순차 교체(자원 추가 0), Blue-Green은 1:1 일괄 전환(자원 추가 100%), Canary는 소수 비율 노출 후 확대(자원 추가 소량).

</details>

| 비교 항목 | Rolling Update (롤링 배포) | Blue-Green Deployment | Canary Deployment |
|:---|:---|:---|:---|
| 배포 방식 | 기존 Pod를 하나씩 인플레이스 순차 교체 | 1:1 별도 환경 생성 후 **100% 순간 스위칭**| **소수(5%) 트래픽 노출 후 단계적 확대** |
| 자원 오버헤드 | 교체 여유분만 추가 필요 | **병렬 환경만큼 자원 증가** | 카나리 인스턴스만 추가 필요 |
| 구/신버전 공존 | 배포 진행 중 **구•신버전 혼재** | **전환 전 병렬 환경 유지** | **관찰 기간에 의도적 공존** |
| 롤백 방식 | 이전 버전으로 역순 교체 | **라우팅을 Blue로 재전환** | **카나리 노출을 차단** |

#### 한줄 요약

- 점진 위험 검증에는 카나리 배포, 환경 전환 복구에는 블루-그린 배포가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Expand-Contract Pattern (DB 스키마 하위 호환)**: 구버전과 신버전이 트래픽 전환 과정에서 DB를 공유할 때, 칼럼 삭제/변경 시 구버전 애플리케이션이 파괴되지 않게 2단계로 나누어 DB 스키마를 변경하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 무장애 배포 중 DB 스키마 변경 시 구버전 앱 붕괴 | **Expand-Contract Pattern (2단계 DB 스키마 변경)** | DB 트랜잭션 호환성 보장 |
| Blue-Green 병렬 환경으로 인프라 비용 증가 | **HPA와 전환 후 이전 환경 회수 정책** | 복귀 시간과 자원 비용 균형 |
| Canary 배포 시 유저 세션 튕김 현상 | **Redis 세션 외부화 (Stateless Architecture)** | 유저 경험(UX) 보존 |

> 사례: **Kubernetes + Argo Rollouts + Istio + Flagger (Automated Canary Analysis)** 조화 구축

#### 한줄 요약

- 확장-축소 변경, 최소 표본, 버전별 지표, 보상 절차가 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **무장애 배포 선택 기준(Zero-Downtime Deployment Standards)**: 인프라 자원 예산, 롤백 속도 요건 및 무장애 가용성에 의거한 체계.

</details>

- 부분 노출 검증은 **Canary**, 일괄 전환•복귀는 **Blue-Green** 선택

#### 한줄 요약

- 관찰 방식과 복구 방식에 맞는 배포 전략 선택 기준이 핵심이다.
