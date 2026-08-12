---
sidebar:
  order: 136
  label: "136. 마스터 데이터 관리 (Master Data Management, MDM)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "마스터 데이터 관리 (Master Data Management, MDM)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 136
extra:
  question_no: "136"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "기준정보 일관성•중복 통제 설계 가치"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **MDM (Master Data Management / 마스터 데이터 관리)**: 기업 전사의 파편화된 핵심 비즈니스 개체(고객, 상품, 계좌, 공급업체) 데이터를 단일한 표준 기준정보(Golden Record / Single Version of Truth)로 매칭, 통합, 정제하여 전 시스템에 동기화 전파하는 프로세스 및 플랫폼.
- **Golden Record (골든 레코드)**: 이종 DB의 동일 인물/상품 중 가장 최신의 높은 신뢰성을 지닌 속성값만을 병합 추출하여 완성한 전사 최고 품질 단일 레코드.
- **Survivorship Rule (생존 규칙)**: 여러 소스 DB의 동일 컬럼 값이 충돌할 때(예: A시스템 주소 vs B시스템 주소), 최신성/우선순위에 따라 최종 Golden Record에 채택될 값을 판정하는 합사 규칙.

</details>

- 정의/개념: 각 시스템에 파편화된 핵심 기준정보(고객, 상품)를 매칭/병합 알고리즘으로 단일 단일 진실 고리(Golden Record)로 통합 정제하여 전사에 전파하는 관리 체계인 **MDM (Master Data Management)**
- 배경/필요성: CRM, ERP, 주문 DB 간 동일 고객/상품 식별 불가로 인한 마케팅 오발송, 재고 오계산 및 수불 정산 파행 문제 해결 요구성

#### 한줄 요약

- 여러 장부의 같은 사람이나 상품을 찾아 하나의 기준 신분표로 연결한다.

## Ⅱ. 특징 (MDM 3대 핵심 관리 사상)

<details><summary>핵심 용어</summary>

- **Matching & Merging (매칭 및 병합)**: 핑거프린트/유사도 알고리즘으로 중복 레코드 파악 후 병합.
- **Cross-Referencing (교차 참조 맵핑)**: MDM의 Master ID와 각 원천 DB의 Local ID 간의 n:1 매핑 관리.

</details>

- **Single Version of Truth (전사 단일 골든 레코드 생성)**
- **Deterministic & Probabilistic Matching (확정적 및 확률적 디두플리케이션 매칭)**
- **Cross-Referencing & Real-Time Sync (원천 시스템 간 Master-Local ID 맵핑 및 2way 동기화)**

#### 한줄 요약

- 비슷하다고 무조건 합치지 않고 값의 우선순위와 애매한 경우의 사람 검토가 필요하다.

## Ⅲ. 구조 및 구성요소 (MDM 4대 아키텍처 토폴로지)

<details><summary>핵심 용어</summary>

- **Consolidation vs Transactional Architecture**: Consolidation은 수집/분석용 단방향 모음, Transactional은 중앙 MDM에서 CUD를 직접 수행하는 양방향 권위형 구조.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        MDM Architecture Topologies                     │
├────────────────────────────────────────────────────────────────────────┤
│ [1. Registry Style]      ──► Master-Local ID 맵핑 관리 (가장 가벼움)   │
│ [2. Consolidation Style] ──► DW/분석용 골든 레코드 단방향 집적         │
│ [3. Coexistence Style]   ──► 소스 DB와 MDM 간 양방향 동기화 (가장 보편적) │
│ [4. Transactional Style] ──► 중앙 MDM에서 마스터 데이터 직접 CUD 생성  │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터 통합 및 동기화 강도에 따라 Registry부터 Transactional까지 4가지 패턴으로 분류되는 MDM 구현 아키텍처.

| MDM 토폴로지 스타일 | 동작 원리 및 특징 | 장점 및 단점 비교 |
|:---|:---|:---|
| **1. Registry Style** | **원천 DB 데이터 복제 없이 Master ID 맵핑만 유지**| **구축 빠르고 저비용**, 속성 병합 불가 |
| **2. Consolidation** | **원천에서 수집하여 분석용 Golden Record 생성** | **분석/DW 용도 적합**, 원천 DB 갱신 불가 |
| **3. Coexistence** | **Golden Record 생성 후 원천 DB로 양방향 동기화**| **운영/분석 모두 우수**, 동기화 복잡도 증가 |
| **4. Transactional** | **모든 마스터 데이터의 CUD 생성을 MDM이 전담** | **데이터 무결성 100%**, 시스템 응답 지연 |

#### 한줄 요약

- 여러 장부의 같은 사람을 하나의 기준 신분표에 연결한다.

## Ⅳ. 흐름도 (MDM Data Cleansing & Matching 5단계 흐름)

<details><summary>핵심 용어</summary>

- **Blocking Key (차단 키)**: 수백만 건 레코드 전체를 N*N으로 무차별 비교하지 않고, `BirthDate_ZipCode` 형태로 차단 키를 묶어 매칭 비교군을 1/1,000 수준으로 축소하는 성능 최적화 기법.

</details>

```text
[Multi-Source Ingest] ──► [Standardization (전처리)] ──► [Blocking Key Grouping]
                                                                  │
                                                                  ▼
 [Golden Record Output] ◄── [Survivorship Rule] ◄── [Matching Engine (Deterministic / Probabilistic)]
```

### 동작 원리

1. **Standardization**: 전화번호, 주소 포맷을 공통 표준 규격으로 일체화.
2. **Blocking Key & Matching**: Blocking Key로 비교군 좁힌 후 자카드/레벤슈타인 확률 매칭 수행.
3. **Survivorship & Merge**: 생존 규칙에 따라 가장 신뢰도 높은 최신 속성값을 뽑아 **Golden Record 완성**.

#### 한줄 요약

- 기록 형식을 맞추고 같은 사람 후보를 찾은 뒤 애매한 건을 확인해 기준 신분표와 원래 장부 번호를 연결한다.

## Ⅴ. 종류 및 비교 (Deterministic Matching 대 Probabilistic Matching)

<details><summary>핵심 용어</summary>

- **Deterministic vs Probabilistic**: Deterministic은 주민번호/사업자번호 100% 일치 시 병합, Probabilistic은 이름+생년월일+주소 유사도 점수(85점 이상)로 병합.

</details>

| 비교 항목 | Deterministic Matching (확정적 매칭) | Probabilistic Matching (확률적 매칭) |
|:---|:---|:---|
| **매칭 조건 기준** | **주민등록번호, 사업자번호 등 고유키 100% 일치** | **이름, 주소, 전화번호 등의 복합 유사도 점수** |
| **오탐(False Positive)**| **0% (오류 병합 위험 없음)** | 오탐 발생 가능 (이름/주소 유사인 병합 위험) |
| **미탐(False Negative)**| 높음 (고유키 오기재 시 절대 매칭 불가) | **낮음 (오타가 있어도 유사 점수로 매칭 성공)** |
| **적용 도메인** | 금융 계좌, 주민번호 보유 시스템 | **커머스 회원, 유통 상품 마스터** |

#### 한줄 요약

- 중앙이 번호만 연결할지, 사본을 모을지, 서로 고칠지, 원본 자체가 될지에 따라 나뉜다.

## Ⅵ. 실무 고려사항 및 대책 (MDM 3대 장애 및 해복 조치)

<details><summary>핵심 용어</summary>

- **Un-Merge Mechanism (병합 분리)**: 확률 매칭 오류로 타인이 동일인으로 오병합(Over-Merge)되었을 때, 이를 원복하여 2개 레코드로 즉시 분리하는 트랜잭션 롤백 기능.

</details>

| 3대 MDM 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Over-Merge (오병합)** | 확률 매칭 스코어가 높아 쌩판 남이 합쳐짐 | **Un-Merge 분리 기능 및 Steward 수동 검토 큐** |
| **2. Under-Merge (과소병합)**| 띄어쓰기 오타로 동일인이 2개 계정 분리 | **주소/이름 전처리 인핸서(Address Cleanser) 강화**|
| **3. Real-Time Sync Lag** | MDM 갱신 후 소스 DB로 2way 동기화 지연 | **Kafka CDC 기반 비동기 양방향 동기화 파이프라인**|

> 사례: **삼성전자 / LG전자 글로벌 통합 상품 MDM & 금융사 고객 MDM 아키텍처**

#### 한줄 요약

- 잘못 합친 고객과 놓친 중복 고객, 사람이 확인한 시간까지 함께 재야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **MDM 수립 기준(MDM Architecture Standards)**: Coexistence Style, Probabilistic Matching, Blocking Key, Survivorship Rule 및 Un-Merge 기능성에 의거한 체계.

</details>

- **MDM 수립 기준**에 따라 전사 통합 고객/상품 마스터 구축 시 **MDM & Probabilistic Matching & Golden Record** 필수 적용

#### 한줄 요약

- 기준 신분표가 많다는 것보다 왜 합쳤고 어느 값이 어디서 왔으며 잘못되면 되돌릴 수 있는지가 중요하다.
