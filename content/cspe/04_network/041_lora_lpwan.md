---
title: "LoRa/LPWAN (Low Power Wide Area Network)"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 41
---

## Ⅰ. 개요
- **정의**: 저전력으로 수 km 이상 장거리 통신을 지원하는 IoT 전용 무선 네트워크 기술임
- **배경/필요성**: IoT 센서는 배터리 교체가 어렵고 소량 데이터를 넓은 범위로 전송해야 하므로 저전력·광역 통신이 필요함
- **비유**: 작은 목소리로도 산 너머까지 울려 퍼지는 확성기와 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| IoT 통신 기술 비교 능력 | LoRa(물리계층)와 LoRaWAN(프로토콜) 구분 | LPWAN 범주에 Sigfox·NB-IoT 등 포함됨을 언급 |

> 요약: 저전력·광역·저속 특성으로 IoT 대규모 센서망에 적합한 통신 기술임

## Ⅱ. 구성요소
```text
End Device ---(LoRa RF)---> Gateway ---(IP)---> Network Server ---> App Server
   |                           |                      |
 Sensor/Actuator         Multi-channel RX        Join/MAC 관리
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| End Device | 센서 데이터를 LoRa 변조하여 전송하는 단말 | 편지를 쓰는 발신자 |
| Gateway | LoRa 신호를 수신해 IP 네트워크로 중계하는 장비 | 우체국 집배원 |
| Network Server | 단말 인증·중복 제거·MAC 명령을 처리하는 서버 | 우편 분류 센터 |
| Application Server | 수집 데이터를 비즈니스 로직으로 처리하는 서버 | 수신자의 사무실 |

> 요약: 단말-게이트웨이-네트워크서버-앱서버의 스타형 토폴로지로 구성됨

## Ⅲ. 절차
```text
Device -> Join Request -> Network Server -> Join Accept -> Device
Device -> Uplink Data -> Gateway -> Network Server -> App Server
App Server -> Downlink Data -> Network Server -> Gateway -> Device
```
- 1단계: 단말이 Join Request(DevEUI, AppEUI)를 전송하여 네트워크 참여를 요청함
- 2단계: Network Server가 인증 후 Join Accept와 세션 키를 발급함
- 3단계: 단말이 Chirp Spread Spectrum 변조로 센서 데이터를 Uplink 전송함
- 4단계: 수신 확인(ACK) 또는 제어 명령을 Downlink으로 단말에 전달함

> 요약: OTAA 방식 인증 후 비대칭적 Uplink 위주 통신을 수행함

## Ⅳ. 문제점
- 저속 데이터 전송: 최대 수십 kbps로 영상·음성 등 대용량 데이터 처리 불가
- Downlink 제약: Class A 기준 수신 창이 Uplink 직후로 한정되어 실시간 제어 곤란
- 비면허 대역 간섭: ISM 대역 공유로 타 기기와 주파수 충돌 시 패킷 손실 발생

> 요약: 저속·비대칭·비면허 대역 특성에서 오는 한계가 존재함

## Ⅴ. 개선방안
1. 단기: Class C 모드 적용으로 상시 수신 창을 열어 Downlink 지연 감소
2. 중기: LR-FHSS(주파수 호핑) 도입으로 간섭 회피 및 동시 접속 단말 수 확대
3. 장기: 위성 LoRa 연동(NTN)으로 지상 게이트웨이 사각지대 해소

> 요약: 수신 모드 확장·주파수 호핑·위성 연동으로 한계를 극복함

## Ⅵ. 전망
- 발전 방향: LoRaWAN 릴레이 기능으로 실내·지하 커버리지 확장 추진 중임
- 기술사적 판단: 5G mMTC와 상호보완 관계로 공존하며 저가 센서 시장 유지 전망
- 기술사 제언: 보안(AES-128 키 관리)과 로밍 표준화가 대규모 배포의 선결 과제임
