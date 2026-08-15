---
sidebar:
  order: 54
  label: "054. 지속적 배포 (Continuous Deployment)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "지속적 배포 (Continuous Deployment)"
date: "2026-08-13T15:42:00+09:00"
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

- **Continuous Deployment (CD, 지속적 배포)**: 파이프라인의 모든 자동화 테스트 및 품질 게이트(Quality Gate)를 성공적으로 통과한 소스코드가 사람의 수동 개입 없이(No Human Touch) 실운영(Production) 환경에 즉시 자동 출시 배포되는 프로세스.
- **Continuous Delivery vs Continuous Deployment**: Continuous Delivery는 운영 배포 직전 '사람의 수동 승인(Manual Gate)' 절차가 존재하는 반면, Continuous Deployment는 이 과정까지 100% 자동화된 최종 단계.
- **Fail-Safe Mechanism**: 지속적 배포 중 오류 발생 시, 모니터링 시스템과 연동되어 자동으로 배포를 중단하고 이전 버전으로 복구(Auto-Rollback)시키는 안전장치.

</details>

- 정의/개념: CI 테스트 및 검증 단계를 통과한 코드 커밋을 인위적 수동 승인 없이 실운영(Prod) 환경으로 상시 자동 배포 완결하는 최상위 자동화 절차인 **Continuous Deployment**
- 배경/필요성: 수동 승인은 **대기 병목•누락**으로 피드백 지연 유발

#### 한줄 요약

- 자동 검증과 운영 반영을 연결한 지속적 배포가 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Small Batch Deployment**: 수개월 분량의 거대한 릴리스 대신, 1~2개 커밋 단위의 아주 작은 단위(Small Batch)로 배포하여 장애 영향 범위를 최소화하는 기법.
- **Guardrail Metrics**: 자동 배포 후 오류율(Error Rate), 지연시간(P99 Latency), CPU 사용량이 지정한 임계치(Threshold)를 초과 시 자동으로 배포를 롤백시키는 핵심 가드레일 모니터링 지표.

</details>

- 정책 게이트 기반 **No Human Touch (무개입 자동 배포)**
- **Small Batch Deployment**를 통한 장애 파괴력 최소화
- **Guardrail Metrics** 기반 자동 모니터링 및 **Auto-Rollback** 메커니즘 필수 결합

#### 한줄 요약

- 작은 변경, 가드레일 지표, 가역적 데이터 변경이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Auto-Rollback Engine**: Prometheus/Grafana 지표를 런타임에 가동 감시하여, 배포 후 이상 징후 감지 시 1초 이내에 이전 Pod 버전으로 트래픽을 자동 원복시키는 엔진.

</details>

```text
[품질 게이트 (Quality Gate Pass)]
       |
[버전 아티팩트 (Docker Image)]
       |
 [배포 제어기 (ArgoCD Automation)]
       |
[트래픽 제어기 (Canary Router)]
       |
 [관측 시스템 (Prometheus Alert)] ──► [이상 발생 시 Auto-Rollback]
```

선의 의미: Quality Gate 통과 아티팩트가 ArgoCD로 자동 디스패치되고, Prometheus가 Guardrail 지표 모니터링을 수행하여 실패 시 Auto-Rollback을 트리거하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 품질 게이트 | 자동 시험•분석 결과로 승격 허용 판정 |
| 버전 아티팩트 | 검증된 불변 실행물과 버전 식별자 보관 |
| 배포 제어기 | 승인된 버전을 대상 환경에 자동 배치 |
| 트래픽 제어기 | 신규 버전의 노출 비율을 점진 조절 |
| 관측 시스템 | 오류율•지연시간 등 가드레일 측정 |
| 자동 롤백 엔진 | 임계치 위반 시 이전 버전으로 복귀 |

#### 한줄 요약

- 게이트•아티팩트•배포•관측•복귀 연결이 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Progressive Delivery (점진적 전달)**: Canary 배포와 Feature Flag를 결합하여, 유저 군별/트래픽 비율별로 신규 기능을 점진적으로 안전하게 노출시키는 현대적 배포 기술.

</details>

```text
┌──────────────────────────────┐
│ Git Main Branch Commit       │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 품질 게이트 판정          │
│ 2. 운영 환경 자동 배치       │
│ 3. 카나리 트래픽 노출        │
│ 4. 가드레일 지표 감시        │
│ 5. 확대•복귀 판정            │
├──────────────┬───────────────┤
│ (정상)       │ (이상 감지)   │
│              ▼               ▼
│  [Full Rollout 배포]   [Auto-Rollback 원복]
└──────────────────────────────┘
```

### 동작 원리

1. **품질 게이트 판정**: 자동 시험•분석으로 승격 가능 여부 판정.
2. **운영 환경 자동 배치**: 배포 제어기가 신규 버전 배치.
3. **카나리 트래픽 노출**: 일부 트래픽을 신규 버전으로 전달.
4. **가드레일 지표 감시**: 오류율•지연시간을 기준선과 비교.
5. **확대•복귀 판정**: 정상은 노출 확대, 이상은 자동 복귀.

#### 한줄 요약

- 가드레일 판정에 따른 노출 비율 확대와 롤백이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Manual Approval Gate vs Continuous Deployment**: Continuous Delivery는 수동 승인을 거치므로 규제/보안 준수(Compliance)에 유리하나 배포 속도가 느림. Continuous Deployment는 완전 자동화로 속도가 극대화되나 철저한 자동화 테스트와 관측성 필수.

</details>

| 비교 항목 | Continuous Delivery (지속적 전달) | Continuous Deployment (지속적 배포) |
|:---|:---|:---|
| 수동 승인 개입 | **수동 승인 게이트 적용** | **정책 기반 무개입 승격** |
| 배포 속도 / 리드 타임 | 승인 대기 시간 포함 | **자동 승격으로 대기 시간 축소** |
| 필수 요구사항 | 빌드•시험 자동화와 승인 통제 | **자동 시험•관측성•자동 복귀** |
| 적용 조직 성격 | 금융, 의료, 공공 (규제 준수 중시) | **빅테크, 모바일/웹 SaaS (속도 및 UX 중시)** |

#### 한줄 요약

- 자동 복구 가능 시 배포, 승인 필요 시 지속적 전달이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Backward Compatibility (하위 호환성)**: DB 스키마 변경 시, 구버전 애플리케이션과 신버전 애플리케이션 모두가 문제없이 동작하도록 Expand-Contract 패턴으로 스키마를 변경하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| DB 스키마 컬럼 삭제로 애플리케이션 복귀 제약 | **Expand-Contract Pattern** 단계 적용 | 버전 간 DB 호환성 유지 |
| 시험 미비로 결함 커밋이 운영에 자동 유입 | 위험 기반 **Quality Gate** 강화 | 결함 유입 가능성 축소 |
| 자동 배포 후 잠재적 지연 에러 발생 | **Prometheus + Argo Rollouts 기반 Auto-Rollback** | 장애 피해 최소화 |

> 사례: 넷플릭스 / 아마존의 **Spinnaker + Kayenta (자동 카나리아 분석)** 지속적 배포 아키텍처

#### 한줄 요약

- 버전별 관측, 확장-축소 변경, 자동 복귀의 안정성 통제가 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **지속적 배포 도입 기준(Continuous Deployment Selection Criteria)**: 자동화 테스트 성숙도, Observability 구현 수준 및 도메인 가역성에 의거한 체계.

</details>

- 자동 복귀 가능 도메인은 **지속적 배포**, 승인 의무 환경은 **지속적 전달** 선택

#### 한줄 요약

- 가역성•관측성•복귀 가능성에 따른 지속적 배포 적용 기준이 핵심이다.
