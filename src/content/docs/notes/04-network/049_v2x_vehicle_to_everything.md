---
sidebar:
  order: 49
  label: "049. V2X 차량사물통신 (V2X Vehicle-to-Everything)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "V2X 차량사물통신 (V2X Vehicle-to-Everything)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 49
extra:
  question_no: "049"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "보안•설계형: 138회 V2X 위협 대응 장문"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **차량·사물 통신(Vehicle-to-Everything, V2X)**: 차량이 다른 차량(V2V), 도로 인프라(V2I), 보행자(V2P) 및 네트워크(V2N)와 주행 상태, 위험 경고, 도로 정보를 실시간 교환하는 협력형 주행 무선 통신 기술이다.
- **PC5·Uu(PC5 Direct Link & Uu Cellular Interface)**: 기지국을 경유하지 않는 근거리 직접 무선 통신 인터페이스(PC5)와 기지국/코어망을 경유하는 광역 셀룰러 인터페이스(Uu)의 통신 규격이다.

</details>

- 정의/개념: **차량·사물 통신(V2X, Vehicle-to-Everything)**은 차량이 다른 차량(V2V), 도로 인프라(V2I), 보행자(V2P), 네트워크망(V2N)과 유무선 통신 인터페이스(PC5 Direct / Uu Cellular)를 이용하여 주행 상태, 센서 데이터 및 도로 위험 정보를 실시간 교환하는 자율주행 협력 통신 체계이다.
- 배경/필요성: 차량 내부 온보드 센서(카메라, 라이다, 레이더)의 비가시 영역(NLOS) 섀도잉 및 악천후 인식 한계를 극복하고, 자율주행 4단계 이상 협력형 주행(Cooperative ADAS)을 실현하기 위해 도입되었다.

#### 한줄 요약

- 차량(V)이 타 차량, 도로 인프라, 보행자, 네트워크(V2X)와 PC5/Uu 통신으로 주변 안전 및 주행 정보를 실시간 공유하는 자율주행 무선 통신 기술.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **위치·센서 개연성(Plausibility & Sensor Cross-Check)**: 수신된 V2X 위치/속도 정보가 실제 차량 라이다/카메라 센서의 물리적 측정치와 대조하여 유효한지 판정하는 검증 기법이다.
- **공개키 기반구조(Public Key Infrastructure, PKI / SCMS)**: V2X 메시지 기밀성, 무결성, 비부인성을 보장하고 인증서를 주기적으로 발급/관리하는 보안 자격증명 체계이다.

</details>

- **이중 무선 경로 제공 (PC5 / Uu)**: 10ms 이하 초저지연을 보장하는 PC5 직접 사이드링크(Sidelink)와 넓은 커버리지를 제공하는 Uu 셀룰러 광역 경로를 병행 활용한다.
- **SCMS PKI 가명 기반 프라이버시 보호**: 개인 위치 정보 추적을 차단하기 위해 유효 기간이 짧은 가명 인증서(Pseudonym Certificate)를 기반으로 전자서명을 발행·검증한다.
- **다중 레이어 보안 및 개연성(Plausibility) 검증**: PKI 기반 전자서명 검증 외에 수신 메시지(BSM/CAM)의 시공간 위치와 자체 센서 관측 간의 개연성을 다중 검증하여 허위 위조 메시지를 차단한다.

#### 한줄 요약

- PC5/Uu 커버리지 통합, SCMS PKI 가명 인증서 기반 프라이버시 보호, 위치-센서 플라우저빌리티 교차 검증 제공.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **차량 탑재 장치(On-Board Unit, OBU)**: 차량 내부에 설치되어 차량 센서 상태(속도, 방향, 위치)를 V2X 메시지로 변환·서명하여 전송하는 무선 통신 모듈이다.
- **노변 장치(Roadside Unit, RSU)**: 신호등, 교차로, 도로 구조물에 설치되어 주변 OBU 단말과 메시지를 교환하고 백엔드 C-ITS 서버와 연동하는 인프라 장치이다.

</details>

```text
V2X 통신 아키텍처
├─ 직접 통신 경로 (PC5 Direct Link: OBU ── RSU ── OBU)
├─ 셀룰러 광역 경로 (Uu Cellular: OBU ── 5G gNB ── V2X Server)
└─ 보안 인증 체계 (V2X PKI System / SCMS)
```

선의 의미: OBU 및 RSU가 PC5 사이드링크 직접 무선 채널로 통신하거나, 5G gNB를 거치는 Uu 인터페이스로 V2X 서버와 연동되고 SCMS PKI가 인증서를 제공하는 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 차량 탑재 장치 (OBU) | 차량 CAN 버스 데이터 및 위치 정보를 수집하여 BSM/CAM 메시지를 생성하고 PC5/Uu로 전송 |
| 노변 장치 (RSU) | 교차로 신호등 제어기, 노변 센서와 연동하여 V2I 안전 메시지(MAP/SPaT)를 수율 및 브로드캐스팅 |
| 5G 이동통신망 (gNB) | Uu 인터페이스 기반으로 광역 차량 트래픽을 라우팅하고 C-V2X 서비스 품질(5QI)을 차등 보장 |
| V2X 서버 / C-ITS | 전역 도로 상황을 수집하여 돌발 상황(사고, 공사) 메시지를 해당 셀 커버리지 내 차량에 다중 방송 |
| SCMS PKI 인증 체계 | 등록 기관(EA) 및 가명 기관(AA)을 통해 OBU/RSU에 가명 인증서를 발급하고 CRL 폐기 관리 |

#### 한줄 요약

- OBU, RSU, 5G 네트워크 및 V2X 서버가 PC5 및 Uu 경로로 메시지를 교환하고 SCMS PKI 시스템이 가명 인증서를 발급·검증하는 구조.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **전자서명(Digital Signature)**: 메시지 송신 OBU의 가명 개인키로 생성한 서명값으로, 수신 OBU가 가명 공개키로 검증하여 위변조를 방지한다.
- **최신성(Freshness & Anti-Replay)**: 수신 메시지의 타임스탬프와 시퀀스 번호를 분석하여 이전 수신 메시지의 재전송(Replay Attack)을 차단하는 속성이다.

</details>

```text
1. PC5 사이드링크 수신 메시지 (BSM / CAM Message)
      │
      v
2. SCMS PKI 가명 인증서 서명 및 CRL/CRL-Check 검증 (Certificate Verify)
      │
      ├─ 서명 실패 ---- 메세지 즉시 폐기 (Discard)
      └─ 서명 성공
            │
            v
      3. 타임스탬프 및 시퀀스 넘버 최신성 검증 (Freshness & Anti-Replay)
            │
            v
      4. 차량 센서 데이터와 위치-속도 개연성 검증 (Plausibility Cross-Check)
            │
            v
      5. 차량 제어기(ECU/ADAS) 경고 발송 및 충돌 회피 자율 제어
```

### 동작 원리

1. **V2X 안전 메시지 수신**: 주변 OBU 또는 RSU가 송신한 기본 안전 메시지(BSM/CAM)를 PC5 무선 채널을 통해 수신한다.
2. **PKI 서명 및 폐기 상태 검증**: 메시지에 첨부된 가명 인증서 유효성을 검증하고, CRL(인증서 폐기 목록)을 대조하여 무단 서명을 차단한다.
3. **최신성(Freshness) 검증**: 타임스탬프를 대조하여 100ms 이상 지연되었거나 중복 수신된 재 replay 공격 메시지를 분리 폐기한다.
4. **개연성(Plausibility) 교차 검증**: 메시지에 적힌 수신 대상의 GPS 좌표 및 속도 수치가 자체 라이다/카메라 관측치와 물리적으로 부합하는지 최종 판정한다.
5. **ADAS 제어 전달**: 검증을 모두 통과한 안전 메시지만 차량 전자제어기(ECU)로 하향 전달하여 자동 긴급 제동(AEB) 및 충돌 경고를 실행한다.

#### 한줄 요약

- 메시지 수신, PKI 가명 서명 검증, 타임스탬프 최신성 확인, 센서 개연성(Plausibility) 검증 후 ADAS 제어기에 경고를 하향 전달하는 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **PC5 직접 통신(PC5 Direct Communication / Sidelink)**: 기지국을 경유하지 않고 5.9GHz 대역 무선 채널로 근거리 앤드포인트 간 파형을 직접 전송하는 기술이다.
- **Uu 망 경유 통신(Uu Cellular Communication)**: 기지국과 백본 코어망을 거쳐 V2X 서버와 데이터를 전송하는 세션 기반 이동통신 방식이다.

</details>

| 비교 항목 | **PC5 직접 통신 (Sidelink / Direct)** | **Uu cellular 통신 (Network-based)** |
|:---|:---|:---|
| 무선 전달 경로 | 기지국 미경유 차량 간(V2V/V2I) 직접 전송 | 5G/LTE 기지국 및 코어망 경유 전송 |
| 무선 지연시간 | 10ms 이내 (초저지연, 긴급 안전 메시지) | 30ms ~ 100ms 이상 (광역 교통 정보) |
| 통신 커버리지 | 근거리 직접 통신 (수백 미터 이내, Line-of-Sight) | 광역 기지국 셀 커버리지 (수 km ~ 수십 km) |
| 주요 교환 메시지 | BSM(기본 안전 메시지), CAM(차량 정기 메시지), DENM | C-ITS 광역 교통 표지, 날씨, 맵 업데이트 정보 |
| 기지국 음영 대응 | 기지국 없는 오지/터널에서도 직접 무선 통신 가능 | 기지국 음영 지역 통신 불가 |

> 요약: PC5는 기지국 미경유 근거리 초저지연 긴급 위험 통신에 특화되고, Uu는 광역 기지국 경유 장거리 교통 정보 전송에 특화.

#### 한줄 요약

- PC5는 기지국 미경유 근거리 초저지연 긴급 위험 통신에 특화되고, Uu는 광역 기지국 경유 장거리 교통 정보 전송에 특화.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **가명 인증서(Pseudonym Certificate / PCA)**: 차량 추적을 차단하기 위해 수 분~수 일 주기로 무작위 교체되는 V2X 전용 단기 발급 인증서이다.
- **혼잡 제어(Congestion Control / DCC)**: 차량 밀집 지역에서 무선 채널 점유율(CBR)이 높아질 때 메시지 전송 주기를 동적으로 늘려 채널 마비를 예방하는 기술이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| GPS 위치 정보 위조 공격 | Sybil 및 GPS Spoofing을 통해 허위 BSM 위치 발송 | 센서(LiDAR/Radar) 연동 Plausibility 교차 검증 | 유효 서명 기반 위치 위조 공격 완벽 차단 |
| PC5 사이드링크 무선 혼잡 | 도심 교차로 차량 밀집 시 PC5 주파수 채널 충돌 | 분산 혼잡 제어(DCC - Decentralized Congestion Control) | 안전 메시지 무선 패킷 손실률 급감 |
| 가명 인증서에 의한 추적 | 동일 가명 인증서를 장시간 사용할 시 이동 경로 추적 | 5분/10km 주기로 가명 인증서 자동 갱신 및 파기 | 차량 운전자 개인정보 및 위치 프라이버시 보호 |
| 메시지 재반복 공격 | 무선 채널의 구 메시지 도청 후 재전송 시도 | 타임스탬프 및 100ms 이내 Anti-Replay 윈도우 검증 | 중복 및 과거 지연 메시지 자동 필터링 |

#### 한줄 요약

- 센서-위치 Plausibility 다중 검증, DCC(분산 혼잡 제어) 알고리즘, SCMS 연동 가명 인증서 회전으로 V2X 통신 보안성 확보.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **다중 검증(Multi-Layer Message Verification)**: PKI 가명 서명 검증, 타임스탬프 최신성 및 라이다 센서 Plausibility 검증을 연쇄 실행하는 통합 무결성 체계이다.

</details>

- 차세대 자율주행 C-ITS 구축 시 **PC5/Uu 하이브리드 V2X 도입**, **SCMS PKI 기반 보안 검증 체계 구축**, **센서 연동 Plausibility 검증 구현 필수**.

#### 한줄 요약

- PC5/Uu 하이브리드 통신망 구축 및 PKI-센서 다중 검증 기반 자율주행 보안 체계 구현 필수.
