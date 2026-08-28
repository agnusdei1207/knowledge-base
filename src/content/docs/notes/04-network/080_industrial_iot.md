---
sidebar:
  order: 80
  label: "080. 산업용 사물인터넷 (IIoT)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "스마트 제조 및 산업 인프라 혁신 : IIoT (Industrial IoT)"
date: "2026-08-26T14:07:54+09:00"
tags:
  - "notes-network"
weight: 80
extra:
  question_no: "80"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "Purdue 모델 기반 계층 구조, IT-OT 융합, 예지보전(PdM) 및 안전 연동(Safety Interlock)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IIoT (Industrial Internet of Things)**: 제조 공정, 발전소 등 산업 현장(OT)의 설비와 IT 클라우드 분석 플랫폼을 융합하여 예지보전을 실현하는 기술.
- **Purdue Model (ISA-95)**: 산업 제어 시스템을 레벨 0(물리 공정)부터 레벨 5(기업 네트워크)까지 계층화하여 보안 격리와 통신을 통제하는 모델.

</details>

- 정의/개념: OT 설비와 IT 분석을 융합한 **예지보전·공정 최적화 기술**
- 배경/필요성: 폐쇄형 OT망은 현장 데이터를 반출하지 않아 **고장 예측과 전사 최적화를 사람의 경험으로 대체하는 비용**을 치르므로, OT DMZ와 엣지 게이트웨이를 경계에 세워 제어 경로는 격리한 채 데이터만 상위로 올림

#### 한줄 요약
- **IT-OT 융합·Purdue 격리·Safety Interlock** 구현

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Predictive Maintenance (예지보전, PdM)**: 진동, 전류, 온도 시계열 데이터를 AI로 분석하여 부품 고장 징후를 사전에 감지하고 최적 교체 시점을 도출하는 기술.
- **Safety Interlock (안전 연동)**: 상위 IT 시스템의 제어 명령이 내려오더라도 현장 안전 한계치를 위반할 경우 하드웨어 레벨에서 명령을 차단하는 보호 기제.

</details>

- **24x7 가용성**: 미션 크리티컬 공정의 연속성 보장
- **Purdue IT-OT 분리**: OT DMZ로 악성코드 확산 차단
- **Safety Interlock**: 상태 노후화 시 PLC 안전 제어 우선

#### 한줄 요약
- 24x7 고가용성 보증, Purdue 모델 기반 IT-OT 보안 격리, 현장 최우선 안전 연동(Interlock)을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OT DMZ**: IT 엔터프라이즈망과 OT 제어망 사이에 위치하여 프록시, 데이터 Historian, 점프 호스트만을 배치하는 보안 완충 지대 (Purdue Level 3.5).

</details>

```text
[IIoT 정적 구성]
|-- IT 클라우드 분석계
|-- OT DMZ 완충구역
|-- 엣지 게이트웨이
|-- PLC / SCADA
`-- 센서 / 액추에이터
```

선의 의미: 현장 센서 데이터가 OT DMZ를 거쳐 IT 클라우드로 안전하게 수집되고 검증된 제어 명령만 현장 PLC로 하향 전달되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| IT 클라우드 분석계 | **RUL 예측·공정 최적화** | Level 4/5 |
| OT DMZ 완충구역 | **IT 침해의 OT 확산 차단** | Level 3.5 |
| 엣지 게이트웨이 | **OPC UA·MQTT 변환·추론** | Edge Computing |
| PLC / SCADA | **결정론적 공정 제어** | Level 1/2 |
| 센서 / 액추에이터 | **계측·Safety Interlock** | Field Hardware |

#### 한줄 요약
- OT DMZ가 IT망과 제어망 사이의 단일 관문 자리를 차지해 데이터는 위로 통과시키되 제어 명령은 현장 재검증을 거치게 하므로, 연결성과 안전이 같은 경로에서 분리된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **State Staleness (상태 노후화)**: IT 클라우드의 분석 지연으로 인해 과거 데이터 기반의 제어 명령이 현재 현장 상태와 맞지 않아 발생하는 오제어 위험.

</details>

```text
센서 데이터
    |
1. 현장 데이터 정제
    |
2. 클라우드 AI 분석
    |
3. 운영자 명령 승인
    |
4. PLC 안전 조건 검증
    +-- 충족: 명령 집행
    `-- 초과: Interlock 차단
    |
5. 현장 상태 확인
    |
공정 결과
```

- 1. 현장 데이터 정제
- 2. 클라우드 AI 분석
- 3. 운영자 명령 승인
- 4. PLC 안전 조건 검증
- 5. 현장 상태 확인

#### 한줄 요약
- AI 분석 결과가 곧바로 집행되지 않고 현장 안전 재검증에서 실행과 차단으로 갈리므로, 최적화 이득보다 오동작 회피를 먼저 지불하는 구조가 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IIoT (산업용)** vs **Consumer IoT (소비자용)**: 산업 공정/안전 최우선 인프라와 편의성/저비용 중심 스마트홈.

</details>

| 비교 항목 | 산업용 사물인터넷 (IIoT) | 소비자 사물인터넷 (Consumer IoT) |
|:---|:---|:---|
| 최우선 설계 목표 | **작업자 안전·설비 가용성** | 편의성·경제성 |
| 오동작 발생 파급력 | **셧다운·인명 피해** | 일시 장애 |
| 동작 환경 및 수명 | **가혹 환경·10~20년** | 실내·1~3년 |
| 네트워크 보안 체계 | **Purdue 분리·OT DMZ** | 클라우드 직접 연결 |
| 주요 적용 영역 | 공장·발전·화학 공정 | 스마트홈·가전·헬스케어 |

#### 한줄 요약
- IIoT는 안전과 무중단 가용성을 최우선으로 하며, 소비자 IoT는 사용 편의성과 경제성을 중심으로 설계된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Passive Network Monitoring**: 능동적인 패킷 송신(Active Scan) 없이 스위치 미러링(SPAN) 포트를 통해 지나가는 패킷만을 수동 캡처하여 구형 PLC의 중단을 방지하는 관제 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| IT 악성코드의 OT 확산 | **OT DMZ·데이터 다이오드** | 제어망 격리 |
| 상태 노후화에 따른 오제어 | **PLC 재검증·Safety Interlock** | 설비 파손 차단 |
| 능동 스캔으로 구형 PLC 정지 | **SPAN 수동 모니터링** | 무중단 위협 탐지 |
| EMI·EMC로 패킷 유실 | **STP·광통신·5G 특화망** | 노이즈 간섭 완화 |

#### 한줄 요약
- **OT DMZ·Interlock·수동 관제**로 안전 운영

## Ⅶ. 결론

- 안전·가용성 우선 공정은 **Purdue·OT DMZ**, 제어는 **Interlock** 적용

#### 한줄 요약
- **IT 분석·OT 안전 제어** 결합으로 공정 자율화
