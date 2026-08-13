---
sidebar:
  order: 136
  label: "136. 마스터 데이터 관리 (Master Data Management, MDM)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "마스터 데이터 관리 (Master Data Management, MDM)"
date: "2026-08-14T00:30:00+09:00"
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

- 정의/개념: 핵심 개체의 기준 레코드를 통합하는 **MDM**
- 배경/필요성: 시스템별 식별자•속성 불일치는 **중복 고객•재고 오차** 유발

#### 한줄 요약

- 여러 장부의 같은 사람이나 상품을 찾아 하나의 기준 신분표로 연결한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Matching & Merging (매칭 및 병합)**: 핑거프린트/유사도 알고리즘으로 중복 레코드 파악 후 병합.
- **Cross-Referencing (교차 참조 맵핑)**: MDM의 Master ID와 각 원천 DB의 Local ID 간의 n:1 매핑 관리.

</details>

- **Single Version of Truth (전사 단일 골든 레코드 생성)**
- **Deterministic & Probabilistic Matching (확정적 및 확률적 디두플리케이션 매칭)**
- **Cross-Referencing & Real-Time Sync (원천 시스템 간 Master-Local ID 맵핑 및 2way 동기화)**

#### 한줄 요약

- 비슷하다고 무조건 합치지 않고 값의 우선순위와 애매한 경우의 사람 검토가 필요하다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Consolidation vs Transactional Architecture**: Consolidation은 수집/분석용 단방향 모음, Transactional은 중앙 MDM에서 CUD를 직접 수행하는 양방향 권위형 구조.

</details>

```text
[원천 레코드] ───── [표준화 규칙]
      │                    │
[매칭 엔진] ─────── [생존 규칙]
      │                    │
[Golden Record] ─── [교차 참조]
```

선의 의미: 원천 정제•동일 개체 판정•속성 선택•식별자 연결 관계.

| 구성요소 | 책임 |
|:---|:---|
| **원천 레코드** | 시스템별 로컬 식별자•속성 제공 |
| **표준화 규칙** | 이름•주소•코드 형식 정규화 |
| **매칭 엔진** | 확정•확률 기준으로 동일 개체 후보 판정 |
| **생존 규칙** | 출처•최신성•신뢰도로 최종 속성 선택 |
| **Golden Record** | 승인된 기준 개체와 변경 이력 보관 |
| **교차 참조** | Master ID와 Local ID 관계 관리 |

#### 한줄 요약

- 여러 장부의 같은 사람을 하나의 기준 신분표에 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Blocking Key (차단 키)**: 수백만 건 레코드 전체를 N*N으로 무차별 비교하지 않고, `BirthDate_ZipCode` 형태로 차단 키를 묶어 매칭 비교군을 1/1,000 수준으로 축소하는 성능 최적화 기법.

</details>

```text
[다중 원천 레코드]
       │
       ▼
1. 값 표준화
       │
       ▼
2. 후보군 차단
       │
       ▼
3. 동일 개체 매칭
       │
       ▼
4. 생존 속성 선택
       │
       ▼
5. 기준•교차 참조 확정
```

### 동작 원리

1. **값 표준화**: 이름•전화•주소•코드를 비교 형식으로 변환
2. **후보군 차단**: Blocking Key로 비교 대상 축소
3. **동일 개체 매칭**: 규칙•유사도•검토로 병합 여부 판정
4. **생존 속성 선택**: 출처 우선순위•최신성으로 값 결정
5. **기준•교차 참조 확정**: Golden Record와 Local ID 연결

#### 한줄 요약

- 기록 형식을 맞추고 같은 사람 후보를 찾은 뒤 애매한 건을 확인해 기준 신분표와 원래 장부 번호를 연결한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Deterministic vs Probabilistic**: Deterministic은 주민번호/사업자번호 100% 일치 시 병합, Probabilistic은 이름+생년월일+주소 유사도 점수(85점 이상)로 병합.

</details>

| 비교 항목 | Deterministic Matching (확정적 매칭) | Probabilistic Matching (확률적 매칭) |
|:---|:---|:---|
| **매칭 조건 기준** | **주민등록번호, 사업자번호 등 고유키 100% 일치** | **이름, 주소, 전화번호 등의 복합 유사도 점수** |
| **오탐(False Positive)** | 키 품질•재사용 오류에 좌우 | 임계값에 따라 오탐 발생 가능 |
| **미탐(False Negative)**| 높음 (고유키 오기재 시 절대 매칭 불가) | **낮음 (오타가 있어도 유사 점수로 매칭 성공)** |
| **적용 도메인** | 금융 계좌, 주민번호 보유 시스템 | **커머스 회원, 유통 상품 마스터** |

#### 한줄 요약

- 중앙이 번호만 연결할지, 사본을 모을지, 서로 고칠지, 원본 자체가 될지에 따라 나뉜다.

## Ⅵ. 실무 고려사항 및 대책

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

- 신뢰 고유키는 **확정 매칭**, 불완전 속성은 확률 매칭•검토 적용

#### 한줄 요약

- 기준 신분표가 많다는 것보다 왜 합쳤고 어느 값이 어디서 왔으며 잘못되면 되돌릴 수 있는지가 중요하다.
