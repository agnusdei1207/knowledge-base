---
sidebar:
  order: 133
  label: "133. 스마트팩토리 OT 보안 (OT Security Smart Factory)"
  badge:
    text: "기출 • 70%"
    variant: note
title: 스마트팩토리 OT 보안 (OT Security Smart Factory)
date: "2026-08-13T22:28:00+09:00"
tags:
  - notes-security
weight: 133
extra:
  question_no: "133"
  source_status: "기출"
  source_history: "126회"
  priority: 70
  priority_note: "126회 기출이며 안전•가용성 중심 OT 설계가 독립적임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **OT(Operational Technology)**: 물리 공정•산업 설비를 감시•제어하는 운영기술이다.
- **MES(Manufacturing Execution System)**: 생산 실행을 계획•추적하는 제조실행시스템이다.
- **스마트팩토리**: 센서•제어장치•MES•분석을 연결한 제조 체계이다.

</details>

- 정의/개념: **스마트팩토리**의 제어망•산업 프로토콜•현장 장치를 보호하는 **OT** 보안 체계이다.
- 배경/필요성: IT 보안 통제를 그대로 적용하면 공정 중단•물리 사고가 발생할 수 있다.

#### 한줄 요약

- 공정 중단·인명 사고를 막는 **가용성·안전성 우선**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **영역•통로**: 자산을 보안 영역으로 묶고 영역 간 허용 통신 경로를 통제하는 모델이다.
- **정비창**: 공정 영향을 검토한 변경을 승인된 시간대에 적용하는 운영 구간이다.
- **IT(Information Technology)**: 업무 정보를 처리•저장•전송하는 기술이다.
- **IT•OT 경계**: 업무망과 공정망 사이에 승인 통신만 허용하는 기준이다.

</details>

- 안전•가용성•실시간성을 우선 보호한다.
- **영역**•**통로**와 **IT•OT 경계**로 통신을 분리한다.
- 공정 영향을 검토하고 **정비창**에서 변경한다.

#### 한줄 요약

- 패치 전 검증과 **정비창 적용**, 사전 통신 제한

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **IDMZ(Industrial Demilitarized Zone)**: IT와 OT의 직접 연결을 막는 중계 영역이다.
- **SCADA(Supervisory Control and Data Acquisition)**: 산업 공정을 원격 감시•제어하는 체계이다.
- **PLC(Programmable Logic Controller)**: 산업 장치의 논리 제어를 수행하는 제어기이다.
- **DCS(Distributed Control System)**: 공정 제어를 여러 제어기에 분산한 체계이다.
- **SIS(Safety Instrumented System)**: 위험 시 공정을 안전 상태로 전환하는 독립 체계이다.

</details>

```text
스마트팩토리 OT 보안 경계
├─ 기업 IT 영역
├─ 산업 DMZ•원격접속
├─ MES•SCADA 운영 영역
├─ PLC•DCS 제어 영역
└─ 현장 장치•독립 SIS
```

| 구성요소 | 책임 |
|:---|:---|
| 기업 IT 영역 | **IT** 외부 연결•사용자 관리 |
| 산업 DMZ•원격접속 | **IDMZ**로 직접접속 차단 |
| MES•SCADA 운영 영역 | **MES**•**SCADA** 접근 통제 |
| PLC•DCS 제어 영역 | **PLC**•**DCS** 명령 허용목록 |
| 현장 장치•독립 SIS | **SIS**로 안전 상태 보호 |

#### 한줄 요약

- **IDMZ**를 거쳐 승인된 PLC 명령만 전달

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SL-T(Security Level-Target)**: 위험평가로 정한 영역•통로의 목표 보안수준이다.
- **설비•프로토콜•의존성 식별**: 자산•통신•소유자와 공정 의존성을 파악하는 단계이다.
- **침해•차단의 공정 영향 분석**: 보안 사건과 통제 적용이 안전•가용성에 미치는 영향을 평가하는 단계이다.
- **영역•통로•SL-T 검토**: 통신 경계와 목표 보안수준의 안전 영향을 확인하는 단계이다.
- **보상통제 적용•복구 시험**: 즉시 변경할 수 없는 위험을 줄이고 롤백•복구를 시험하는 단계이다.

</details>

```text
설비•통신 현황
   │
   ▼
1. 설비·프로토콜·의존성 식별
   │
   ▼
2. 침해·차단의 공정 영향 분석
   │
   ▼
3. 영역·통로·SL-T 검토
   ├─ 즉시 변경 위험 ──► 격리•보상통제
   └─ 정비창 변경 가능 ─► 승인된 단계 변경
                           │
                           ▼
4. 보상통제 적용·복구 시험
   │
   ▼
안전 전환•복구 시험 결과
```

### 동작 원리

1. 설비·프로토콜·의존성 식별: 자산·통신·소유자 파악
2. 침해·차단의 공정 영향 분석: 안전·가용성 평가
3. 영역·통로·SL-T 검토: 목표 수준·안전 영향 확인
4. 보상통제 적용·복구 시험: 단계 적용·롤백 검증

#### 한줄 요약

- 안전 승인 후 통제하고 **오프라인 복구 시험**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IIoT(Industrial Internet of Things)**: 산업 장치와 원격 플랫폼을 연결한 사물인터넷이다.

</details>

| 운영 환경 보안 | OT 환경 | IT 환경 | IIoT 연계 |
|:---|:---|:---|:---|
| 적용 기준 | 정지 영향•안전 승인 필요 | 재부팅 가능한 업무계 | 원격 분석•예지정비 |
| 핵심 특징 | **OT**의 물리 공정 제어 | **IT**의 정보•업무 처리 | **IIoT**의 산업 장치 연결 |
| 한계 | 차단•패치의 공정 영향 | 정보 유출•업무 중단 | 침해의 현장 확산 |

> 요약: OT는 보안 조치의 물리 안전 영향부터 판단하는 것이 핵심이다.

#### 한줄 요약

- OT는 통제보다 **공정 안전 영향**을 우선 판단

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IEC(International Electrotechnical Commission)**: 국제전기기술위원회이다.
- **IACS(Industrial Automation and Control Systems)**: 산업자동화•제어시스템이다.
- **IEC 62443-3-2**: IACS 영역•통로 위험평가 표준이다.
- **IEC 62443-3-3**: IACS 시스템 보안 요구사항 표준이다.
- **NIST(National Institute of Standards and Technology)**: 미국 국립표준기술연구소이다.
- **SP(Special Publication)**: NIST가 발행하는 특별간행물이다.
- **NIST SP 800-82**: 안전•신뢰성을 고려한 OT 보안 지침이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 자산 연결을 모르면 위험이 다른 영역으로 전파됨 | **IEC**의 **IACS** 표준 **IEC 62443-3-2** 적용 | SL-T•경계 근거 확보 |
| 목표 수준만으로는 구현 요구를 정할 수 없음 | **IEC 62443-3-3** 적용 | 기능•보안수준 구체화 |
| IT 통제가 공정 안전•가용성을 해칠 수 있음 | **NIST**의 **SP**, **NIST SP 800-82** 적용 | 보상통제•복구 정합성 |

#### 한줄 요약

- PLC 패치는 복제 환경에서 공정 영향과 롤백을 확인한 뒤 안전 담당자가 승인한 정비창에 단계 적용한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **보상통제**: 즉시 패치하기 어려운 설비의 위험을 격리•허용목록•감시 등으로 줄이는 통제이다.

</details>

- 공정 영향이 크면 격리 후 **보상통제**를 적용하고 정비창에서 단계 변경한다.

#### 한줄 요약

- 공정 영향에 따라 **보상통제** 후 정비창 변경
