---
sidebar:
  order: 137
  label: "137. 데이터 품질 관리: 완전성•정확성•일관성 (Data Quality Management)"
  badge:
    text: "미출 · 70%"
    variant: note
title: "데이터 품질 관리: 완전성•정확성•일관성 (Data Quality Management)"
date: "2026-08-14T00:37:00+09:00"
tags:
  - "notes-software"
weight: 137
extra:
  question_no: "137"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "완전성•정확성•일관성 품질 관리 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **DQM (Data Quality Management / 데이터 품질 관리)**: 기업이 보유한 데이터 자산의 유용성 및 신뢰성을 확보하기 위해, 6대 품질 진단 차원(완전성, 정확성, 일관성, 유효성, 유일성, 적시성)을 정의하고 지속 측정, 개선, 격리하는 프로세스.
- **Completeness (완전성)**: 필수 데이터 항목이 널(Null)이나 공백 없이 100% 입력되었는지에 관한 품질 차원.
- **Accuracy (정확성)**: 데이터 수치가 실제 현실 세계의 상응하는 참값(Real World Fact) 및 허용 표준 규칙과 100% 일치하는 정도.
- **Consistency (일관성)**: 시스템 간 동일 데이터가 서로 상충하지 않고 항상 동일한 형태와 의미를 유지하는 정도.

</details>

- 정의/개념: 품질 차원을 측정•개선하는 **DQM(Data Quality Management)**
- 배경/필요성: 검증 없는 데이터는 **지표 왜곡•오판•재작업** 유발

#### 한줄 요약

- 쓸 자료가 빠졌거나 틀렸거나 서로 모순되는지 검사하고 고친 뒤 같은 기준으로 다시 확인한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **6 Data Quality Dimensions**: Complete(완전성), Accurate(정확성), Consistent(일관성), Valid(유효성), Unique(유일성), Timely(적시성).

</details>

- **6대 핵심 데이터 품질 평가 차원 보유 (Completeness, Accuracy, Consistency 등)**
- **Closed-Loop Quality Improvement (프로파일링 $\rightarrow$ 진단 $\rightarrow$ Quarantine 격리 $\rightarrow$ 피드백 순환)**
- **Automated Data Quality Gate & Expectation Enforcement (자동화된 규칙 기반 차단)**

#### 한줄 요약

- 참고 통계와 결제 금액은 같은 오류라도 피해가 달라 서로 다른 합격선을 써야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Great Expectations**: Python/Spark 기반 오픈소스 대표 데이터 품질 진단 검증 프레임워크.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   DQM 6-Dimensional Quality Framework                  │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Completeness (완전성) ──► Null / Blank 0% 미입력 누락 방지           │
│ 2. Accuracy (정확성)     ──► 실제 참값 및 허용 도메인 값 일치          │
│ 3. Consistency (일관성)  ──► 시스템 간 동일 데이터 형식/의미 상충 0%   │
│ 4. Validity (유효성)     ──► 주민번호/전화번호 포맷 및 범위 규칙 준수  │
│ 5. Uniqueness (유일성)   ──► PK 중복 레코드 0% (Deduplication)          │
│ 6. Timeliness (적시성)   ──► 요구된 SLA 시간 내 즉시 서빙 반영         │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터의 유용성을 판가름하는 6가지 세부 데이터 품질 평가 지표 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| Completeness | 필수 값의 누락 비율 측정 |
| Accuracy | 참조값•현실값과의 일치 정도 측정 |
| Consistency | 시스템•시점 간 의미•값 모순 측정 |
| Validity | 형식•범위•도메인 규칙 준수 측정 |
| Uniqueness | 업무 키의 의도치 않은 중복 측정 |
| Timeliness | 요구 시점까지 데이터 반영 여부 측정 |

#### 한줄 요약

- 불합격 자료를 격리하고 원인을 고친 뒤 같은 시험을 다시 본다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Data Quality Gate**: 파이프라인 중간(Spark DLT)에 배치되어 품질 검증 미달 레코드를 하류 시스템으로 가지 못하도록 차단 및 Quarantine 테이블로 격리하는 관문.

</details>

```text
[수집 데이터]
      │
      ▼
1. 품질 프로파일링
      │
      ▼
2. 위험별 합격선 적용
      │
  ┌───┴────┐
  │통과    │실패
  ▼        ▼
3. 하류 반영  4. 격리•알림
      │        │
      └───┬────┘
          ▼
5. 원인 개선•재검증
```

### 동작 원리

1. 품질 프로파일링: 누락•중복•범위•분포 통계 생성
2. 위험별 합격선 적용: 데이터 중요도별 규칙•임계치 판정
3. 하류 반영: 통과 데이터와 품질 증거를 함께 공개
4. 격리**•**알림: 실패 행•배치를 사유와 함께 분리
5. 원인 개선•재검증: 상류 수정 후 동일 규칙 재실행

#### 한줄 요약

- 현재 상태로 합격선을 정하고 불합격 자료는 따로 두며 원인을 고친 뒤 같은 시험을 다시 본다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Automated DQ Profiler**: 수동 SQL 쿼리가 아닌 AI 기반 프로파일러로 대용량 데이터 품질 자동 측정.

</details>

| 구분 | Manual DQ Management (수동 점검) | Automated DQM Platform (자동화) |
|:---|:---|:---|
| 품질 검증 시점 | **사후 분석 (사용자가 오류 보고 시 수동 쿼리)** | **사전/실시간 (Quality Gate 파이프라인 탑재)** |
| 오류 레코드 처리 | 타깃 DB에 이미 오염 데이터 저장됨 | **Quarantine 테이블로 즉시 자동 격리 차단** |
| 프로파일링 방식 | 개발자가 일회성 `COUNT(1)` 쿼리 작성 | **프로파일러가 전 컬럼 통계 자동 추출** |
| 대표 표준 도구 | Excel, 수동 SQL 쿼리 | **Great Expectations, Soda, Databricks DLT** |

#### 한줄 요약

- 완전성은 빠짐, 정확성은 틀림, 일관성은 서로 다름을 다룬다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **DQ Alert Fatigue**: 품질 임계치를 너무 빡빡하게 설정하여 무의미한 에러 경보가 매일 폭증하여 무시되는 안티패턴.

</details>

| 3대 DQM 위험 요소 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Alert Fatigue | 노이즈성 알림 폭증으로 엔지니어가 무시 | **경보 임계치(Threshold) 단계별 상향 및 재조정** |
| 2. Pipeline Stalls | 1건의 오류로 전체 대용량 파이프라인 멈춤 | **`ON VIOLATION DROP ROW` (오류행만 격리 후 계속)**|
| 3. Lack of Root Cause | 어디서 데이터가 찌그러졌는지 추적 불가 | **Data Lineage (계보) 연동으로 상류 소스 역추적** |

> 사례: **카카오 / 당근마켓 Great Expectations & Soda 기반 자동 데이터 품질 검증**

#### 한줄 요약

- 주문 번호가 없는 주문은 매출에 넣지 않고 따로 보관해 원본을 고친 뒤 다시 검사한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **DQM 수립 기준(DQM Architecture Standards)**: 6대 품질 차원, Great Expectations 프레임워크, Quality Gate 및 Quarantine 격리성에 의거한 체계.

</details>

- 고위험 데이터는 **차단 Gate**, 저위험은 경고•관찰로 운영

#### 한줄 요약

- 모든 결함을 평균내지 말고 피해가 큰 오류부터 막고 고쳐 같은 시험을 통과시킨다.
