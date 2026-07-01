---
title: "LoRa·LoRaWAN (LoRa LoRaWAN)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 64
---

# 📖 【암기용】 개념 완전 이해

> 목적: LoRa와 LoRaWAN을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: LoRa 변조와 LoRaWAN MAC/네트워크 구조로 장거리 저전력 IoT 통신을 제공하는 LPWAN 기술
- **왜 필요한가**: 수도·전력 검침, 농업 센서, 환경 관측처럼 소량 데이터를 수 km 이상 보내는 배터리 기기가 필요함
- **핵심 직관**: 큰 짐을 자주 나르는 트럭이 아니라, 작은 엽서를 아주 멀리 보내는 우편망에 가까움

## 깊이 이해
- **배경·문제의식**: Wi-Fi와 BLE는 커버리지가 짧고, 셀룰러는 요금·모듈·전력 부담이 있음. LoRaWAN은 비면허 Sub-GHz 대역에서 작은 센서 데이터를 장거리로 전달함.
- **작동 원리**: 단말은 LoRa Chirp Spread Spectrum으로 Gateway에 업링크를 보내고, Gateway는 IP 백홀로 Network Server에 전달함. Network Server는 중복 패킷 제거, ADR, 보안 검증, Application Server 전달을 수행함.
- **비유**: 여러 우체통(Gateway)에 같은 엽서가 들어와도 중앙 우체국(Network Server)이 중복을 제거하고 목적지(Application Server)로 한 장만 보내는 구조임.
- **구체 예시**: 농업 토양 센서가 15분마다 12바이트 수분값을 전송하고, Gateway 2대가 수신한 중복 업링크를 Network Server가 DevAddr·Frame Counter로 정리함.
- **흔한 오해·주의점**: LoRaWAN 주파수, 출력, Duty Cycle, Listen Before Talk 조건은 국가·지역 규제와 주파수 계획에 따라 다르므로 특정 국가 조건으로 단정하면 안 됨.

## 연결 개념
- LPWAN — 저전력 광역 IoT 통신 범주
- NB-IoT/LTE-M — 면허 대역 셀룰러 LPWAN 대안
- ADR — 링크 품질에 따라 Data Rate와 송신 전력을 조정하는 LoRaWAN 기능

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: LoRa는 물리 변조, LoRaWAN은 네트워크 프로토콜임을 구분하고, 지역 규제·ADR·보안 키·Duty Cycle 조건을 명시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LoRaWAN은 LoRa PHY 기반 단말, Gateway, Network Server, Application Server로 구성되는 장거리 저전력 IoT 네트워크이다.
> 2. **가치**: 수바이트 센서 데이터를 km 단위 커버리지로 전송해 검침·농업·환경 모니터링의 배터리 운영을 지원한다.
> 3. **판단 포인트**: 지역 주파수 규제, Duty Cycle, ADR, 다운링크 제한, 보안 키(AppKey/NwkKey) 관리가 적용 판단의 핵심이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| LPWAN 구조 이해 확인 | LoRa PHY와 LoRaWAN MAC/Network 구분 | LoRa와 LoRaWAN 혼용 금지 |
| 장거리 저전력 원리 확인 | CSS, Spreading Factor, ADR, Gateway | 고속·대용량 통신으로 설명 금지 |
| 제도·운영 조건 확인 | 지역별 Sub-GHz 대역, Duty Cycle, 출력 제한 | 특정 국가 주파수를 전세계 기준으로 단정 금지 |

> 요약: 이 문제는 장거리 저전력 구조와 지역 규제 조건을 함께 쓰는 답안이어야 한다.

---

## Ⅰ. 개요 및 필요성

LoRaWAN은 LoRa 변조 기반 LPWAN 네트워크 프로토콜이다. 소량·저빈도 센서 데이터를 수 km 범위로 보내야 하는 검침·농업·환경 관측에서 배터리 수명과 커버리지가 핵심이다. 비면허 Sub-GHz 사용 조건은 지역별 주파수 계획과 전파 규제를 따라야 함.

---

## Ⅱ. 구조 및 구성요소

```text
End Device -> LoRa Uplink -> Gateway -> IP Backhaul
-> Network Server -> Application Server -> IoT Platform
Network Server -> Downlink Scheduling -> Gateway -> End Device
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| End Device | 센서 데이터 송수신 | Class A/B/C, DevEUI, AppKey |
| Gateway | LoRa 패킷 수신 후 IP 전달 | 여러 Gateway 중복 수신 가능 |
| Network Server | 중복 제거, ADR, 보안 검증 | DevAddr, Frame Counter 확인 |
| Join Server | OTAA 가입·세션 키 생성 | NwkSKey, AppSKey 파생 |
| Application Server | 업무 데이터 처리 | 검침, 관측, 알람 연계 |

> 요약: LoRaWAN은 단말과 Gateway가 단순 무선 접속을 담당하고, Network Server가 중복 제거와 보안·ADR을 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
OTAA Join Request -> Join Accept -> Session Key 생성
-> Sensor Payload -> LoRa Uplink -> Gateway 중복 수신
-> Network Server 검증/중복 제거 -> Application 전달
-> Downlink 필요 시 Class Window에 전송
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | OTAA 또는 ABP 방식으로 단말 가입 | DevEUI, JoinEUI, AppKey |
| 2 | 센서 Payload를 LoRa PHY로 송신 | SF7~SF12, BW, Coding Rate |
| 3 | Gateway가 IP 백홀로 패킷 전달 | RSSI, SNR, Gateway ID |
| 4 | Network Server가 MIC·Frame Counter 검증 | Replay 방지, 중복 제거 |
| 5 | ADR과 다운링크 스케줄링 수행 | Data Rate, Tx Power, RX Window |

> 요약: LoRaWAN은 가입-업링크-중복제거-검증-다운링크 창 순서로 소량 데이터를 신뢰성 있게 전달한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | LoRaWAN | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 대역 | 셀룰러 면허 대역 | 비면허 Sub-GHz | 지역별 EU868, US915, AS923 등 |
| 통신량 | Wi-Fi/Cellular 대용량 | 소량·저빈도 Payload | SF 증가 시 Airtime 증가 |
| 전력 | 상시 연결 부담 | Class A 기본 절전 | 업링크 후 RX1/RX2 창 |
| 운영 | 통신사망 의존 | Private/Public LoRaWAN 선택 | Gateway 밀도와 백홀 필요 |

> 요약: LoRaWAN은 장거리·소량·저전력 데이터에 적합하나, 다운링크와 지역 규제 제약을 설계에 반영해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | LoRaWAN | 선택 기준 |
|:---|:---|:---|:---|
| LPWAN 선택 | NB-IoT/LTE-M | Private Gateway 구축 가능 | 자체망 필요, 통신비 구조, 커버리지 |
| 데이터 패턴 | 실시간 스트리밍 | 분 단위 센서 보고 | Payload 수바이트~수십바이트 |
| 지역 조건 | 국가별 셀룰러 커버리지 | 지역별 비면허 대역 규제 | Duty Cycle, 출력, 채널 플랜 확인 |

> 요약: LoRaWAN은 자체 Gateway와 저빈도 센서 데이터가 맞을 때 선택하고, 이동성·QoS는 셀룰러 LPWAN을 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 규제 위반 | 지역별 주파수·출력·Duty Cycle 차이 | Regional Parameter 적용, 현지 인증 확인 | Airtime/Duty Cycle 로그 |
| 다운링크 병목 | Class A 수신창 제한 | 다운링크 최소화, ADR 정책 최적화 | Downlink Queue Length |
| 키 유출 | AppKey/NwkKey 관리 미흡 | OTAA, HSM/키 저장소, 키 교체 절차 | MIC Fail Count |

> 요약: LoRaWAN 리스크는 지역 규제, 다운링크 제한, 키 관리이며 운영 로그로 상시 확인해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 수신 품질 | Packet Delivery Ratio 95% 이상 | Gateway RSSI/SNR, 중복 수신율 |
| 배터리 | 현장 단말 3~5년 목표 | 송신 주기, 전류 프로파일 |
| 규제 준수 | 지역 Duty Cycle·출력 조건 충족 | Network Server Airtime 리포트 |

> 요약: LoRaWAN 성공 여부는 수신 품질, 배터리 수명, 지역 규제 준수를 함께 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 농업·검침망은 현장 RSSI/SNR 측정 후 Gateway 위치를 선정하고, SF7~SF12 분포와 ADR 적용률을 점검함
2. 지역별 Regional Parameter를 적용하고 주파수·송신출력·Duty Cycle 조건을 현지 규제와 장비 인증서로 확인함
3. OTAA 기반 가입, AppKey 보관, Frame Counter 모니터링, MIC Fail 알람을 Network Server 운영 항목에 포함함

**결론 (2줄):**
- 기술사 판단: 저빈도·소량·자체망 조건이면 LoRaWAN, 이동성·면허망 QoS 조건이면 NB-IoT 또는 LTE-M을 선택함
- 향후 방향: LoRaWAN은 스마트시티·농업·검침에서 Private LPWAN으로 지속 활용되며, 위성 LoRaWAN과 하이브리드 수집망으로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "LoRaWAN을 설명하시오" | OTAA, 업링크, 중복 제거, ADR 흐름 | NB-IoT/LTE-M 대비 특징 |
| 요구사항 명시형 | "스마트 검침망 구축 방안을 제시하시오" | Gateway 배치와 Class A 다운링크 제약 | 규제, 배터리, 수신 품질 지표 |

> 요약: 설명형은 LoRaWAN 계층 구조, 방안형은 지역 규제와 현장 수신 품질 중심으로 전개한다.
