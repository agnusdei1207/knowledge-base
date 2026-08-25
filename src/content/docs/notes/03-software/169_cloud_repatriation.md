---
sidebar:
  order: 169
  label: "169. 클라우드 회귀"
  badge:
    text: "미출 · 50%"
    variant: note
title: "클라우드 회귀 (Cloud Repatriation)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 169
extra:
  question_no: "169"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "비용•규제•종속성에 따른 재배치 판단"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **클라우드 회귀(Cloud Repatriation)**: 퍼블릭 클라우드(AWS, Azure)에 배포했던 워크로드와 데이터를 높은 비용(TCO)이나 보안 규제, 벤더 종속성 해소를 위해 온프레미스 IDC나 프라이빗 클라우드로 되돌리는 인프라 이전 전략.
- **Data Gravity(데이터 중력)**: 클라우드에 저장된 데이터가 거대해질수록 네트워크 Egress 비용과 이관 지연 때문에 다른 인프라로 옮기기 어려워지는 종속 현상.

</details>

- 정의/개념: 퍼블릭 클라우드에 배포했던 워크로드와 데이터를 **비용(TCO) 절감, 데이터 주권 및 종속성 탈피를 위해 온프레미스나 프라이빗 인프라로 재배치하는 전략**
- 배경/필요성: 대규모 상시 워크로드의 퍼블릭 클라우드 장기 운영 시 발생하는 **천문학적인 클라우드 사용료 비용 폭증, 대규모 데이터 반출 비용 및 벤더 종속 해결 불가**

#### 한줄 요약
- 지속적 대규모 부하의 TCO를 절감하고 데이터 통제권을 회복하기 위해 인프라를 자체 환경으로 회귀한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Steady-State Workload**: 스파이크성 변동 없이 1년 내내 일정한 자원을 고정 소비하는 예측 가능한 안정 부하.
- **Exit Strategy**: 클라우드 이전 시 특정 CSP 독점 PaaS 종속을 배제하고 컨테이너 표준을 적용하여 언제든 탈출할 수 있도록 사전 설계하는 전략.

</details>

- 대규모 상시 부하(Steady-State) 환경에서 **서버 직접 구축을 통한 운영 TCO 50% 이상 절감**
- 특정 CSP 독점 API 종속을 해소하고 **데이터 자주권 및 프라이버시 통제권 회복**
- 금융 및 공공 부문의 **국내 데이터 거주성 및 엄격한 규제 컴플라이언정 준수**

#### 한줄 요약
- TCO 절감, 벤더 종속 탈피, 데이터 자주권 확보를 실현한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **클라우드 회귀 4대 아키텍처 계층**: Dependency Decoupling(종속 제거), Target Infra(온프레미스 구축), Data Sync(초기 스냅샷+CDC), Traffic Switching(카나리 컷오버).

</details>

```text
[클라우드 회귀(Cloud Repatriation) 역방향 이관 아키텍처]
|-- 1. Dependency Decoupling Layer (클라우드 전용 DynamoDB/Lambda -> K8s/Postgres 전환)
|-- 2. Target On-Premise Infrastructure Layer
|   `-- Private Bare-metal Nodes + K8s PaaS + Ceph SDS 스토리지 구축
`-- 3. Continuous Data Synchronization Layer
    |-- Initial Baseline Data Loading (AWS Snowball / Direct Connect 대용량 전송)
    `-- Real-time CDC Synchronization (Debezium / Kafka 기반 실시간 변경분 추적)
`-- 4. Traffic Migration & Cutover Layer (DNS Route53 가중치 라우팅 -> IDC 컷오버)
```

선의 의미: 계층 및 클라우드 종속성을 제거하고 온프레미스 인프라 구축 후 CDC 실시간 동기화를 거쳐 트래픽을 안전하게 전환하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **종속성 제거 (Decoupling)**| 공급자 독점 PaaS를 **컨테이너(K8s) 및 오픈소스 DB 인터페이스로 전면 전환** | 표준 기술 적용 |
| **목표 인프라 (Target Infra)**| 베어메탈 서버, 상면, 전력, 네트워크, **사내 K8s PaaS 실행 환경 프로비저닝** | CAPEX 기반 구축 |
| **데이터 동기화 (Data Sync)** | 스냅샷 초기 적재 후 **CDC(Change Data Capture)를 통해 실시간 변경분 동기화** | 무중단 데이터 복제 |
| **트래픽 전환 (Cutover)** | DNS 가중치 기반으로 **카나리 테스트를 거쳐 안전하게 최종 트래픽 컷오버 수행**| 롤백 경로 확보 |

#### 한줄 요약
- 종속성 제거, 목표 인프라, 데이터 동기화, 트래픽 전환이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **클라우드 회귀 5단계**: 인프라 TCO 타당성 검증 $\to$ 초기 데이터 적재 $\to$ CDC 실시간 동기화 $\to$ 카나리 트래픽 분기 $\to$ 최종 컷오버 및 클라우드 자산 정리.

</details>

```text
클라우드 회귀(Repatriation) 프로젝트 승인
        │
   1. [TCO 및 타당성 검증] 전력, 상면비, 인건비를 포함한 5개년 TCO 산정 및 온프레미스 환경 검증
        │
   2. [초기 데이터 적재] 클라우드 DB 스냅샷을 Snowball/전용선으로 온프레미스 스토리지에 복원
        │
   3. [변경분 CDC 동기화] Debezium을 통해 클라우드 운영 DB의 실시간 트랜잭션을 온프레미스로 복제
        │
   4. [카나리 트래픽 전환] DNS 가중치 라우팅으로 5%의 사용자 트래픽을 사내 서버로 분기하여 검증
        │
   5. 최종 트래픽 컷오버를 완료하고 롤백 유예 기간 경과 후 잔여 클라우드 자산 영구 삭제
```

#### 한줄 요약
- TCO 검증 → 초기 적재 → CDC 동기화 → 카나리 전환 → 최종 컷오버 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Cloud Retention vs Repatriation**: 트래픽 변동이 심한 워크로드의 퍼블릭 클라우드 유지(Retention)와 일정한 대규모 부하의 자체 환경 회귀(Repatriation).

</details>

| 비교 항목 | 퍼블릭 클라우드 유지 (Retention) | 클라우드 회귀 (Repatriation) |
|:---|:---|:---|
| 최적 워크로드 패턴 | **예측 불가능한 스파이크 트래픽, 신규 PoC** | **1년 내내 일정한 대규모 안정 부하 (Steady-State)**|
| 비용 과금 모델 | 사용량 기반의 운영비용 (OPEX) | **서버 장비 투자비(CAPEX) + 운영비용(OPEX)** |
| 인프라 운영 주체 | 클라우드 서비스 제공자 (CSP 관리형) | **사내 자체 SRE, 인프라 및 DBA 전담 엔지니어** |
| 락인 및 데이터 주권| 특정 벤더 API 종속 및 국외 반출 위험 | **자체 데이터센터 내 완벽한 데이터 주권 확보** |

#### 한줄 요약
- 급변하는 부하는 퍼블릭 유지, 일정한 대규모 부하는 TCO가 검증된 클라우드 회귀를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Egress Cost Surge**: 페타바이트(PB)급 대용량 데이터를 클라우드 외부로 반출할 때 발생하는 막대한 네트워크 전송 비용.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단순 서버 가격만 비교하여 TCO 계산 착오 발생 | **데이터센터 전력(PUE), 상면비, 라이선스, 인건비 종합 산정** | 정확한 회귀 타당성 평가 달성 |
| 대용량 데이터 반출 시 네트워크 Egress 비용 폭증 | **AWS Direct Connect 전용선 활용 및 물리 어플라이언스(Snowball) 전송** | 네트워크 전송 비용 70% 이상 절감 |
| 관리형 서비스 부재로 인한 사내 운영 역량 부족 | **표준 쿠버네티스 PaaS 구축 및 사내 SRE 자동화 역량 내재화** | 자체 인프라 운영 무중단 안정성 확보 |
| 회귀 중 발생한 결함으로 인한 서비스 장애 | **CDC 양방향 동기화 및 즉시 롤백 가능한 DNS Failover 파이프라인 유지** | 마이그레이션 다운타임 리스크 제로화 |

#### 한줄 요약
- 포괄적 TCO 검증, 물리 전송 장비 활용, 사내 SRE 역량 내재화, 롤백 파이프라인으로 대응한다.

## Ⅶ. 결론

- 성공적인 클라우드 회귀를 추진하기 위해 **안정 부하(Steady-State) 워크로드를 대상으로 전력·인건비를 포함한 5개년 TCO 타당성을 철저히 검증하고, 오픈소스 쿠버네티스 표준화와 CDC 무중단 동기화 체계를 적용**하여 비용 최적화와 데이터 주권을 완벽히 양립시키는 하이브리드 인프라 전략 완성

#### 한줄 요약
- 클라우드 회귀는 대규모 안정 부하 워크로드의 TCO 절감과 데이터 주권 회복을 위해 인프라를 자체 환경으로 안전하게 재배치하는 현대 인프라 최적화 전략이다.