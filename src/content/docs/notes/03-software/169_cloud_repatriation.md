---
sidebar:
  order: 169
  label: "169. 클라우드 회귀 (Cloud Repatriation)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "클라우드 회귀 (Cloud Repatriation)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **Cloud Repatriation (클라우드 회귀)**: 퍼블릭 클라우드(AWS, Azure)에 배포했던 워크로드와 데이터를 높은 비용(TCO)이나 보안 규제, 벤더 종속성 등의 이유로 다시 온프레미스(자체 IDC)나 프라이빗 클라우드로 되돌려오는(Repatriate) IT 인프라 이전 전략.
- **Data Gravity (데이터 중력)**: 클라우드에 쌓인 데이터의 양이 기가바이트(GB)에서 페타바이트(PB) 수준으로 거대해지면, 막대한 네트워크 Egress(데이터 반출) 비용과 이관 지연 시간 때문에 다른 인프라로 옮기기 불가능해지는 종속 현상.
- **Vendor Lock-in (벤더 종속성)**: AWS DynamoDB, Lambda 같은 특정 퍼블릭 클라우드의 관리형(Managed) 고유 기술에 시스템이 과도하게 결합되어, 인프라 이전 시 천문학적인 코드 재작성(Refactoring) 비용이 발생하는 상태.

</details>

- 정의/개념: 퍼블릭 클라우드 도입 후 예상치 못한 TCO 폭발, 데이터 중력, 컴플라이언스 한계에 직면한 기업이 특정 워크로드를 자체 온프레미스로 선택적 원대복귀 시키는 인프라 재배치 전략인 **Cloud Repatriation**
- 배경/필요성: 초기 도입 시의 장밋빛 기대와 달리, 지속되는 고정 부하(Steady State) 워크로드에서 클라우드 요금이 자체 IDC 구축 비용을 압도하는 TCO 역전 현상 극복 요구성

#### 한줄 요약

- 계속 빌리는 비용보다 직접 운영하는 전체 비용이 낮고 통제 편익이 큰 설비만 골라 자체 환경으로 되가져오는 선택이다.

## Ⅱ. 특징 (클라우드 회귀를 촉발하는 3대 페인 포인트)

<details><summary>핵심 용어</summary>

- **TCO (Total Cost of Ownership, 총소유비용)**: 단순 하드웨어 구매/렌탈 비용뿐만 아니라 5년간의 전력(PUE), 소프트웨어 라이선스, 운영 인건비, 네트워크 Egress 요금 등 겉으로 드러나지 않는 숨은 유지 유지비용의 총합.

</details>

- **Unpredictable TCO (숨겨진 Egress 데이터 전송료 및 예측 불가한 과금 폭탄)**
- **Data Gravity & Lock-in (벤더 고유 PaaS 종속 및 페타바이트급 데이터 이관 한계)**
- **Sovereignty & Compliance (소버린 클라우드 요건 및 데이터 역외 이전 금지 등 로컬 규제)**

#### 한줄 요약

- 월 사용료만 비교하면 자체 인력과 장애 복구 비용을 놓치므로 이전 뒤 다시 맡게 될 운영 책임까지 TCO에 포함해야 한다.

## Ⅲ. 구조 및 구성요소 (클라우드 회귀 이관 아키텍처)

<details><summary>핵심 용어</summary>

- **Exit Strategy (출구 전략)**: 클라우드 회귀 결정 시, 무중단으로 기존 데이터를 긁어오고 라우팅을 스위칭하기 위한 이관 마이그레이션(Migration) 역방향 파이프라인.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Cloud Repatriation (Exit) Architecture               │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Assessment: [TCO 분석] ──► [종속성(Lock-in) 제거 및 오픈소스 전환]  │
│                      │                                                 │
│                      ▼                                                 │
│ 2. Synchronization: [Public Cloud] ──(데이터 지속 복제)──► [On-Premise]│
│                      │ (AWS RDS)                           (PostgreSQL)│
│                      ▼                                                 │
│ 3. Switchover: [DNS Routing 스위칭] ──► [On-Premise IDC로 트래픽 인입] │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 퍼블릭 클라우드의 의존성을 걷어내고 온프레미스로 데이터를 양방향 동기화한 뒤, DNS 라우팅을 완전히 로컬로 꺾어 회귀를 완성하는 구조.

| 회귀 이관 단계 | 핵심 수행 과제 | 실무 구현 및 툴 |
|:---|:---|:---|
| **1. 종속성 제거 (De-coupling)** | **클라우드 고유 PaaS를 오픈소스 기술로 대체** | DynamoDB $\rightarrow$ MongoDB |
| **2. 인프라 프로비저닝** | **베어메탈 수급 및 K8s 프라이빗 클라우드 구축**| Terraform, OpenStack |
| **3. 데이터 동기화 (Sync)** | **다운타임 최소화를 위한 CDC 실시간 데이터 복제**| Kafka, AWS DMS (역방향) |
| **4. 트래픽 전환 (Switch)** | **카나리 테스트 후 온프레미스 인그레스로 전환**| Route53, F5 GSLB |

#### 한줄 요약

- 이사 후보를 고르고 새 집을 준비한 뒤 짐과 변경분을 계속 맞추며 손님을 조금씩 옮기고 마지막에 이전 집의 열쇠와 사본을 정리한다.

## Ⅳ. 흐름도 (무중단 데이터 동기화 및 컷오버 흐름)

<details><summary>핵심 용어</summary>

- **CDC (Change Data Capture)**: 클라우드 DB의 변경분(Insert/Update) 로그를 실시간으로 낚아채어, 새로 구축한 온프레미스 DB에 0.1초 지연(Latency)으로 밀어 넣는 무중단 마이그레이션 핵심 기술.

</details>

```text
[AWS Public Cloud (Source)]            [On-Premise IDC (Target)]
        │                                        │
        ▼ 1. 초기 덤프(Snapshot) 마이그레이션    ▼
[AWS RDS (Aurora)] ────────────────────► [Local PostgreSQL]
        │                                        │
        ▼ 2. CDC 실시간 변경분 동기화(Sync)      ▼
[AWS RDS (Aurora)] ──────(Kafka/Debezium)──────► [Local PostgreSQL]
        │                                        │
        ▼ 3. DNS 컷오버 (트래픽 전환)            ▼
[User Traffic] ───X (AWS로 가던 트래픽 차단) ──► [User Traffic (On-Prem)]
```

### 동작 원리

1. **Snapshot**: 퍼블릭 DB의 대용량 스냅샷을 덤프 떠서 온프레미스 DB로 초기 적재 (네트워크 비용 주의).
2. **CDC Sync**: 초기 적재 이후 발생하는 실시간 트랜잭션을 CDC 솔루션으로 온프레미스 DB에 무중단 복제.
3. **Cutover**: 양측 DB가 완벽히 동기화(정합성 일치)된 순간 DNS 라우팅을 온프레미스로 꺾고 퍼블릭 인프라 파기 (**Repatriation 완결**).

#### 한줄 요약

- 원본 서비스를 계속 운영하면서 새 환경에 변경 데이터를 따라붙인 뒤 일부 사용자만 보내 성능과 자료가 맞을 때 전환 비중을 높인다.

## Ⅴ. 종류 및 비교 (퍼블릭 유지 대 클라우드 회귀 1:1 비교)

<details><summary>핵심 용어</summary>

- **Steady-State Workload (안정 부하 워크로드)**: 블랙프라이데이처럼 트래픽이 널뛰는 게 아니라, 1년 내내 일정한 서버 수(예: 100대)를 유지하는 고정 트래픽 워크로드(회귀 시 TCO 절감 극대화).

</details>

| 비교 항목 | Public Cloud Retention (퍼블릭 유지) | Cloud Repatriation (클라우드 회귀) |
|:---|:---|:---|
| **적합한 워크로드 패턴** | **예측 불가능한 스파이크(Spike) 트래픽** | **1년 내내 일정한 안정 부하 (Steady-State)**|
| **핵심 편익** | **무한한 탄력적 확장 (Auto-Scaling) 및 민첩성**| **3~5년 장기 TCO 50% 이상 절감 및 데이터 주권**|
| **운영 인력 (Ops)** | 퍼블릭 CSP가 장애 복구 등 인프라 관리 대행 | **자체 SRE/DBA 인력 대거 고용 필수 (인건비 증가)**|
| **CAPEX / OPEX** | 초기 비용 0원, 월 구독료 지불 (OPEX 위주) | **초기 장비 구축 막대한 투자 (CAPEX 위주)** |

#### 한줄 요약

- 급격히 변하는 부하는 퍼블릭 탄력성을 사용하고 일정한 대규모 부하는 직접 운영의 순편익과 통제 요구를 다시 계산한다.

## Ⅵ. 실무 고려사항 및 대책 (클라우드 회귀 3대 파행 대책)

<details><summary>핵심 용어</summary>

- **Hidden Egress Cost Shock**: 회귀를 위해 AWS에서 페타바이트(PB)급 데이터를 온프레미스로 내려받는 순간 수억 원의 아웃바운드(Egress) 네트워크 트래픽 요금 폭탄을 맞는 파행.

</details>

| 3대 회귀 이전 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. TCO 계산 착오** | 퍼블릭 요금과 베어메탈 깡통 가격만 1차원적 비교| **데이터센터 전력(PUE), 자체 방화벽, 인건비 포함**|
| **2. Egress 요금 폭탄** | 퍼블릭에서 대량 데이터 반출 시 요금 폭주 | **AWS Snowball(물리 하드디스크 배송) 장비 활용** |
| **3. 자체 운영 역량 미달**| 클라우드가 대행하던 DB 이중화를 자체 구현 못함| **K8s 기반 사내 표준 PaaS 구축 및 DBA 인력 선행 확보**|

> 사례: **Basecamp(37signals)의 700만 달러 TCO 절감을 위한 AWS 전면 철수(Repatriation) 성공 사례**

#### 한줄 요약

- 본 데이터만 국내에 두지 말고 지원 로그와 백업의 처리 위치까지 추적하고 정기적으로 다른 환경에 복원해 출구 계획의 실행 가능성을 확인해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Repatriation 수립 기준**: TCO 예측, Data Gravity (Egress 회피), Steady-State 분석 및 자체 SRE 역량에 의거한 체계.

</details>

- **Repatriation 수립 기준**에 따라 안정 부하 워크로드 최적화 시 **TCO 검증 기반 Cloud Repatriation** 선별 적용

#### 한줄 요약

- 안정 부하의 전체 비용과 규제 편익이 이전·운영 위험보다 클 때만 부분 회귀하고 데이터 동기화·롤백·잔여 사본 폐기까지 출구 계획에 포함해야 한다.
