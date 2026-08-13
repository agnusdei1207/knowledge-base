---
sidebar:
  order: 165
  label: "165. SLO•SLA•SLI (SLO•SLA•SLI)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "SLO•SLA•SLI (SLO•SLA•SLI)"
date: "2026-08-14T02:52:00+09:00"
tags:
  - "notes-software"
weight: 165
extra:
  question_no: "165"
  source_status: "기출"
  source_history: "123회, 137회"
  priority: 70
  priority_note: "지표•목표•계약의 역할 구분 출제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **SLI (Service Level Indicator)**: 성공한 요청 수를 전체 요청 수로 나눈 비율처럼, 사용자가 체감하는 서비스의 실제 가용성 및 성능 측정 지표(수치).
- **SLO (Service Level Objective)**: 측정된 SLI가 일정 기간(1달) 동안 달성하기로 엔지니어링 팀 내부에서 합의한 타겟 목표치(예: 99.9%).
- **SLA (Service Level Agreement)**: SLO 목표치보다 보수적으로 책정하여(예: 99.5%), 미달성 시 고객에게 금전적 페널티나 크레딧 보상을 지급하기로 한 비즈니스적 외부 계약.

</details>

- 정의/개념: 측정•목표•계약으로 나눈 **SLI•SLO•SLA** 관리 체계
- 배경/필요성: 추상적 안정성 표현은 **운영 행동•고객 보상** 기준 제공 불가

#### 한줄 요약

- 시험 점수가 SLI, 학교의 내부 합격선이 SLO, 학생과 미리 약속한 보상 기준이 SLA인 것처럼 같은 결과를 서로 다른 목적으로 사용한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Error Budget (오류 예산)**: SLO 목표치(99.9%)를 제외한 0.1%의 여유분으로, 신규 기능 배포나 시스템 실험 과정에서 소비할 수 있는 공식적인 실패 허용량.

</details>

- **Measurement of Reality (사용자가 실제로 겪는 지연, 에러율, 트래픽을 정량화한 SLI 측정)**
- **Internal Target & Threshold (SLO 달성 여부 및 Error Budget 소진율 기반 내부 배포 통제)**
- **External Penalty Contract (SLA 위반 시 과금 면제나 크레딧 페널티가 발생하는 외부 계약)**

#### 한줄 요약

- 고객 약속을 어긴 뒤 대응하지 않도록 내부 SLO를 SLA보다 엄격하게 두면 오류 예산 소진 단계에서 먼저 복구와 배포 제한을 시작할 수 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **SLO $\geq$ SLA**: 페널티 방지를 위해 내부 목표(SLO 99.9%)를 항상 외부 계약(SLA 99.5%)보다 엄격하게 설정하는 방어 기제.

</details>

```text
[Service Level Management]
 ├── [SLI]
 ├── [SLO]
 └── [SLA]
```

| 구성요소 | 책임 |
|---|---|
| SLI | 사용자 경험을 나타내는 **실측 지표** 산출 |
| SLO | SLI의 기간별 **내부 운영 목표** 설정 |
| SLA | 측정 범위•제외•보상의 **외부 계약** 정의 |

#### 한줄 요약

- 먼저 어떤 요청을 잴지 정하고 같은 측정 결과를 내부 운영판과 고객 계약판에 각각 대조해야 계산 차이로 인한 분쟁을 막을 수 있다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Burn Rate**: Error Budget이 정상 소진율(1배수) 대비 얼마나 빠르게 고갈되고 있는지를 나타내는 경보 발송의 핵심 근거 수치.

</details>

```text
[서비스 Event]
     │
     ▼
1. SLI 측정
     │
     ▼
2. SLO 달성•예산 평가
     │
     ▼
3. 운영 조치 결정
     │
     ▼
4. SLA 측정 조건 적용
     │
     ▼
5. 위반•보상 판정
     │
     ▼
[운영•계약 결과]
```

### 동작 원리

1. **SLI 측정**: 합의된 성공 Event와 전체 Event 계산
2. **SLO 달성•예산 평가**: 목표와 Error Budget 대조
3. **운영 조치 결정**: 배포 진행•제한과 복구 우선순위 선택
4. **SLA 측정 조건 적용**: 계약 기간•제외 조건 반영
5. **위반•보상 판정**: 계약 기준에 따라 통지•보상 실행

#### 한줄 요약

- 결제 요청을 성공과 실패로 기록한 한 자료에서 운영팀은 오류 예산을 계산하고 계약팀은 제외 조건을 적용해 보상 여부를 판단한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Latency SLO (지연시간 목표)**: "전체 요청의 99%가 300ms 이내에 응답해야 한다"와 같이 꼬리 지연(Tail Latency)을 관리하는 지표.

</details>

| 지표 유형 | SLI 측정 수식 | SLO 적용 예시 |
|:---|:---|:---|
| **Availability (가용성)**| 성공 요청 수 / 전체 요청 수 | 월간 로그인 성공률 **99.9%** 달성 |
| **Latency (지연시간)** | 300ms 이하 요청 수 / 전체 요청 수| 전체 결제 요청의 99%가 **300ms** 이내 응답 |
| **Throughput (처리량)**| 초당 처리된 바이트 / 전체 바이트 | 스트리밍 대역폭 초당 **100MBps** 유지 |
| **Freshness (최신성)** | 업데이트 후 반영 시간 미달 건수 | 상품 DB 갱신 후 캐시에 **1분 이내** 반영 |

#### 한줄 요약

- SLI는 현재 상태를 말하고 SLO는 내부 행동을 정하며 SLA는 고객에게 책임질 선을 정하므로 숫자가 같아도 역할은 다르다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Aspirational SLO**: 현실 불가능한 무결점 100% SLO를 설정하여 개발팀을 과로사로 몰아넣고 1년 내내 배포를 중단시키는 안티패턴.

</details>

| 3대 서비스 수준 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 100% SLO Anti-Pattern**| 무결점 목표로 Error Budget 소멸 | **비용•사용자 기대 기반 달성 목표 합의**|
| **2. Irrelevant SLI** | CPU 사용률을 SLI로 잡아 고객 경험 누락| **고객 관점인 HTTP 응답 코드 및 Latency 로 변경** |
| **3. SLA Dispute** | 정기 점검 시간의 장애 카운팅 여부 논란| **SLA 명세서에 정기 점검은 제외(Exclude) 명문화** |

> 사례: **카카오 / 당근마켓 Datadog 기반 4대 황금 신호(Latency, Traffic, Errors, Saturation) SLI 모니터링 적용**

#### 한줄 요약

- 봇과 점검 요청을 분모에서 제외했다면 그 조건과 원천 자료를 보존해야 운영 계산과 고객 보상 계산이 같은 결과를 낸다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **서비스 수준 관리(SLM) 수립 기준**: 비즈니스 페널티 SLA, 엔지니어링 목표 SLO, 기술적 측정치 SLI의 계층적 연동 및 Error Budget 기반 배포 통제에 의거한 체계.

</details>

- 사용자 경험은 **SLI**, 내부 행동은 SLO, 고객 책임은 SLA로 결정

#### 한줄 요약

- 사용자 경험을 대표하는 SLI를 먼저 정하고 SLA 위반 전에 대응할 SLO 여유와 계약상 제외·보상 조건을 같은 측정 근거에 연결해야 한다.
