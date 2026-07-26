---
sidebar:
  order: 200
  label: "200. Digital Twin 디지털 트윈 (Digital Twin)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "Digital Twin 디지털 트윈 (Digital Twin)"
date: "2026-07-25T03:29:00+09:00"
tags:
  - "notes-latest-tech"
weight: 200
extra:
  question_no: "200"
  source_status: "기출"
  source_history: "125회, 128회"
  priority: 70
  priority_note: "디지털 트윈의 동기화·예측 구조가 반복 출제됨"
---

## 미리 알고가기

- **Digital Twin**: Digital Twin은 물리 대상과 동기화되는 가상 모델을 통해 상태 분석과 예측과 제어를 수행하는 구조임
- **구별 기준**: 단순 3D 모델이나 정적 시뮬레이션과 달리 실시간 데이터 동기화가 핵심임
- **효과 결정 요인**: 효과는 센서 품질과 모델 정확도와 피드백 제어 수준에 크게 좌우됨


## Ⅰ. 개요

- **정의/개념**: 물리 대상과 동기화되는 가상 표현·서비스
- **배경/필요성**: 중단 없이 상태·고장·변경 영향을 예측

### 쉽게 이해하기 (학습용)

- 실제 기계와 동일한 정보를 가진 가상 복제본이 센서를 통해 현재 상태를 추종하고, 운전·정비 결정을 지원함

## Ⅱ. 특징

- 물리·가상 동기화가 현재 상태를 추정한다.
- 모델·시뮬레이션 결합이 변경 영향을 예측한다.
- 수명주기 버전이 상태·이력 재현을 가능하게 한다.
- 안전 경계가 권고의 물리 반영 위험을 통제한다.

### 쉽게 이해하기 (학습용)

- 가상 복제본도 실제 설비의 노후화를 반영해야 하며, 예측 결과는 안전장치와 승인 절차를 거쳐 현장에 적용함

## Ⅲ. 아키텍처 및 구성요소

```text
[Physical Entity]
      │ sensor·event
      ↓
[Twin State·Context]
├─ [Model·Simulation]
└─ [Analytics·Service]
             ↓
     [Action·Governance]
             └─ 승인 action → [Physical Entity]
```

| 설계 요소 | 설명 |
|:---|:---|
| physical entity·lifecycle ID | 실물과 생애주기 이력을 식별함 |
| sensing·event integration | 센서·사건으로 실물 상태를 갱신함 |
| twin state·context store | 현재 상태·맥락·이력을 보존함 |
| model·simulation engine | 상태를 모사해 변화 영향을 예측함 |
| analytics·twin service | 분석·예측을 업무 서비스로 제공함 |
| action·governance loop | 승인된 조치만 실물에 반영함 |

> 요약: 물리 상태 동기화와 승인된 현실 환류를 연결

### 쉽게 이해하기 (학습용)

- 실제 기계 기록이 복제본을 갱신하고 실험 결과가 안전 검사를 거쳐 작업 지시로 돌아가며 실제 결과로 재학습함

## Ⅳ. 원리 및 절차 흐름도

```text
entity 등록·model 연결
          ↓
data 수집·시간 동기화
          ↓
state 추정·model 보정
          ↓
simulation·예측
          ↓
승인·안전 조치
          ↓
실제 결과 feedback ──→ state·model 재보정
```

| 절차 | 설명 |
|:---|:---|
| entity 등록·model 연결 | entity 등록·model 연결을 수행하고 결과를 검증함 |
| data 수집·시간 동기화 | data 수집·시간 동기화을 수행하고 결과를 검증함 |
| state 추정·model 보정 | state 추정·model 보정을 수행하고 결과를 검증함 |
| simulation·예측 | simulation·예측을 수행하고 결과를 검증함 |
| 승인·action·feedback | 승인·action·feedback을 수행하고 결과를 검증함 |

> 요약: 상태 동기화·오차 검증·안전 환류로 폐루프 완성

### 쉽게 이해하기 (학습용)

- 기계와 가상 복제본의 정보를 맞추고 센서로 보정·검증한 뒤 승인된 조치 결과로 복제본을 재보정함

## Ⅴ. 종류 및 비교

| 판단 기준 | Digital Model | Digital Shadow | Digital Twin |
|:---|:---|:---|:---|
| 핵심 특징 | 수동 갱신 가상 모델 | 물리→가상 자동 갱신 | 양방향 동기화·서비스 |
| 적용 기준 | 설계·offline 검증 | 현황 가시화·상태 추적 | 예측·최적화·승인 조치 |
| 주요 위험 | 실제 상태와 모델 불일치 | 현실 환류·조치 부재 | 모델 오류의 현실 전파 |

> 요약: 자동 갱신 방향과 폐루프 여부로 유형 구분

### 쉽게 이해하기 (학습용)

- 수동 관리 설계도, 자동 표시 계기판, 운전·정비를 돕는 가상 복제본의 차이임

## Ⅵ. 실무 사례

1. 대상 환경의 도입 조건과 설계를 검증함
2. 운영 위험과 성과 지표를 검증함

### 쉽게 이해하기 (학습용)

- 풍력 터빈 twin은 진동·온도·풍속과 정비 이력을 동기화해 bearing 수명을 예측하고 정비 창을 추천하되 turbine 보호 제어와 작업자 승인을 우선함
- 조립 공정 twin은 설비 cycle·buffer·불량 data로 병목 what-if simulation을 수행하고 검증된 MES schedule 변경 후 실제 생산 결과로 model을 보정함

## Ⅶ. 결론

- 동기화 방향·안전 경계로 twin 수준과 조치 권한 결정

### 쉽게 이해하기 (학습용)

- 닮은 그림보다 실제 기계 상태를 정확히 따라가고 안전하게 의사결정을 돕는지가 중요함
