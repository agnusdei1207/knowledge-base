---
sidebar:
  order: 207
  label: "207. 차량•사물 통신 (V2X)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "차량•사물 통신 (Vehicle-to-Everything, V2X)"
date: "2026-08-31T15:08:00+09:00"
tags:
  - "notes-latest-tech"
weight: 207
extra:
  question_no: "207"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "V2X 통신•신뢰 경계 설계가 138회 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **차량•사물 통신(Vehicle-to-Everything, V2X)**: 차량이 다른 차량•인프라•보행자•망과 위험 및 교통 정보를 교환하는 협력 통신 체계이다.

</details>

- 정의: 차량이 주변 참여자•인프라•망과 위험 정보를 교환하는 **V2X 체계**
- 배경/필요성: 카메라, 레이더, 라이다 등 차량 자체 탑재 센서(In-vehicle Sensors)에만 의존하는 자율주행 인지 시스템은 가시선(Line-of-Sight, LoS) 영역에만 국한되어, 교차로 사각지대(Blind Spot), 대형 트럭 후방, 커브길, 악천후(폭설, 폭우, 안개) 등 물리적 시야 차단(Non-Line-of-Sight, NLoS) 상황에서 잠재적 충돌 위험을 사전에 인지할 수 없는 근본적 물리적 한계에 직면함에 따라, 차량이 주변의 모든 사물(차량, 인프라, 보행자, 네트워크)과 무선으로 안전/교통 정보를 실시간 교환하는 Vehicle-to-Everything(V2X / IEEE 802.11p DSRC/WAVE vs 3GPP C-V2X: LTE-V2X & 5G-V2X / V2V: Vehicle-to-Vehicle, V2I: Vehicle-to-Infrastructure, V2P: Vehicle-to-Pedestrian, V2N: Vehicle-to-Network / Direct PC5 Sidelink & Cellular Uu / SCMS Security Credential Management System, BSM, SPaT, MAP, Cooperative Driving & Sensor Sharing) 통신 체계를 도입하여 **PC5 사이드링크(Sidelink) 직접 통신을 통한 10ms 이하 초저지연 NLoS 위험 상황(전방 급제동, 교차로 충돌 경고) 사전 인지 및 협력 주행(Cooperative Autonomous Driving) 구현, 5G-V2X 기반의 고용량 센서 공유(Sensor Sharing) 및 군집 주행(Platooning) 지원, SCMS 공개키 기반구조(PKI) 익명 인증서를 통한 강력한 메시지 무결성/인증 및 차량 프라이버시 보호**를 달성할 필요

#### 한줄 요약

- 앞차와 신호기가 보이지 않는 위험까지 미리 알려 주되, 수신 정보는 차량 센서와 함께 검증하여 사용하는 방식이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **셀룰러 차량•사물 통신(Cellular Vehicle-to-Everything, C-V2X)**: 셀룰러 기술로 차량의 직접 통신과 광역 망 통신을 지원하는 방식이다.
- **차량 간 통신(Vehicle-to-Vehicle, V2V)**: 차량끼리 위치•속도•위험 정보를 직접 교환하는 통신이다.
- **차량•인프라 통신(Vehicle-to-Infrastructure, V2I)**: 차량과 도로•신호 인프라가 정보를 교환하는 통신이다.
- **차량•보행자 통신(Vehicle-to-Pedestrian, V2P)**: 차량과 보행자 단말이 위치•위험 정보를 교환하는 통신이다.
- **차량•네트워크 통신(Vehicle-to-Network, V2N)**: 차량이 기지국•서버를 통해 광역 서비스를 이용하는 통신이다.

</details>

- V2V•V2I•V2P•V2N **다중 교통 참여자 통신**
- PC5•Uu 기반 **저지연 직접•광역 망 통신**
- 서명•시간•위치•센서 일치성 기반 **메시지 신뢰 검증**
#### 한줄 요약

- 차량 센서 밖의 위험 정보를 주변 차량•도로 시설•통신망에서 미리 받는다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **차량 탑재 장치(On-Board Unit, OBU)**: 차량에 탑재되어 V2X 메시지를 생성•송수신•검증하고 센서 정보와 융합하는 장치이다.
- **노변 장치(Roadside Unit, RSU)**: 도로 인프라와 차량 사이에서 교통•안전 메시지를 중계하는 통신 장치이다.
- **V2V•V2I•V2P•V2N**: 차량이 차량•인프라•보행자•네트워크와 정보를 교환하는 V2X의 주요 통신 관계이다.
- **V2X 공개키 기반구조(Public Key Infrastructure, PKI)**: 단기 인증서와 서명으로 메시지의 발신 신뢰와 무결성을 검증하는 체계이다.

</details>

V2X•RSU의 메시지 전달과 **PKI 신뢰 관리**

```text
                 [차량 OBU]
                      |
              [주변 차량•보행자]
                      |
              [RSU•교통 인프라]
                      |
             [셀룰러 망•V2X 서버]
                      |
                  [V2X PKI]
```

선의 의미: 주변•인프라•광역 통신과 PKI 신뢰 경계 관계

| 구성요소 | 책임 |
|:---|:---|
| 차량 OBU | **메시지 생성•검증•센서 융합** |
| 주변 차량•보행자 | **위치•속도•위험 상태 제공** |
| RSU•교통 인프라 | **도로•신호•교차로 정보 제공** |
| 셀룰러 망•V2X 서버 | **광역 교통•서비스 정보 제공** |
| V2X PKI | **인증서 발급•폐기•신뢰 관리** |

#### 한줄 요약

- 직접•망 통신 메시지의 **PKI•센서 기반 신뢰 검증**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **신뢰 검증**: 인증서•서명•신선도•물리 가능성을 확인해 메시지 수용 여부를 정하는 절차이다.

</details>

**OBU•RSU**의 V2X 메시지 교환과 신뢰 검증

```text
[송신 OBU•RSU]
       │ 1. 서명 상태•위험정보
       ▼
  [PC5•Uu 통신]
       │ 2. V2X 메시지
       ▼
    [수신 OBU]
       │ 3. 인증서•신선도
       ▼
    [V2X PKI] ── 신뢰 검증 결과 ──▶ [수신 OBU]
                                         │ 4. 검증•융합 정보
                                         ▼
                                      [차량 판단]
```

### 동작 원리

1. 서명 상태•위험정보: 위치•속도•사건•발생 시각 구성•서명
2. V2X 메시지: 인접은 PC5, 광역은 Uu 경로로 교환
3. 인증서•신선도: 인증서•서명•시각•재전송 여부 검사
4. 검증•융합 정보: 차량 센서와 대조해 경고•보조 결정

#### 한줄 요약

- 메시지 **서명•신선도 검증** 후 센서 융합•제한 사용

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **PC5 인터페이스**: 기지국을 거치지 않고 인접 차량과 단말이 직접 통신하는 C-V2X 인터페이스이다.
- **근거리 전용 통신(Dedicated Short-Range Communications, DSRC)**: 차량 안전 메시지를 위한 근거리 직접 통신 방식이다.
- **지능형 교통 시스템 G5(Intelligent Transport Systems G5, ITS-G5)**: 유럽의 차량•도로 인프라 직접 통신 규격이다.
- **국제전기전자공학회(Institute of Electrical and Electronics Engineers, IEEE)**: 전기•전자•컴퓨팅 기술 표준을 개발하는 전문 단체이다.

</details>

DSRC•ITS-G5•C-V2X의 **직접•망 접속** 비교

| V2X 접속 방식 | DSRC•ITS-G5 | C-V2X PC5 | C-V2X Uu |
|:---|:---|:---|:---|
| 적용 기준 | 근거리 **직접 안전 통신** | 근거리 **셀룰러 직접 통신** | **광역 망 기반 서비스** |
| 핵심 특징 | IEEE 802.11 계열 **직접 통신** | 기지국 비경유 **PC5 통신** | 기지국•서버 경유 **Uu 통신** |
| 한계 | 별도 **노변 인프라** 필요 | 단말•자원 **운용 복잡도** | 망 **지연•가용성 의존** |

#### 한줄 요약

- 두 통신은 지연과 도달 범위를 맞바꾼 선택이므로, 충돌 회피처럼 수십 밀리초가 중요한 정보는 직접 통신이, 넓은 구간을 다루는 **광역 교통 서비스**는 망 통신이 감당한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **신선도 검증**: 메시지 발생 시각과 재전송 여부를 확인해 오래되거나 재사용된 위험 정보를 거부하는 절차이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 통신 품질 미검증 시 혼잡•음영의 **지연•손실** | 채널 부하 제어•다중 경로•**성능 시험** | 통신 **지연•손실률** 감소 |
| 메시지 신뢰 미검증 시 위조•재전송•**위치 조작** | PKI•신선도•물리 가능성 **교차 검증** | 위조•재전송 **수용률** 감소 |
| 차량 융합 미검증 시 외부 정보의 **오경보•오제어** | 탑재 센서 대조•신뢰도•**안전한 실패** | **오경보•오제어** 방지 |

#### 한줄 요약

- 통신 품질•인증서 검증과 **탑재 센서 교차 확인** 후 제한 사용

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Uu 인터페이스**: 차량 단말이 기지국과 서버를 경유해 광역 교통 서비스를 이용하는 셀룰러 인터페이스이다.

</details>

- 개별 차량의 국소적 인지를 초월하여 집단 지성 기반의 협력형 자율주행(Cooperative Automated Driving)을 실현하는 **차세대 지능형 교통 시스템(C-ITS) 및 커넥티드 자율주행 통신의 최고 핵심 인프라(Vehicle-to-Everything: V2X / 5G NR C-V2X Sidelink Standard / V2V-V2I-V2P-V2N Convergence / SCMS PKI Trust Framework / Cooperative Perception Standard)의 확고한 표준**으로 확고히 자리 잡았으며, 5G-Advanced 및 6G 기반의 초정밀 측위(Positioning)와 결합 발전하는 가운데, 실무 V2X 인프라 구축 시에는 **초저지연 안전 제어에는 PC5 사이드링크를, 광역 동적 지도(HD Map) 다운로드에는 Uu 셀룰러를 이원화 배치하고, SCMS 기반 인증서 유효성 검증 및 차량 탑재 센서(In-vehicle)와의 교차 융합 필터링(Plausibility Check)**을 결합하여 완벽한 교통 안전성과 통신 기만 공격 방어를 완성

#### 한줄 요약

- **PKI•신선도**와 물리 가능성•센서를 교차 검증한 뒤 제한 사용
