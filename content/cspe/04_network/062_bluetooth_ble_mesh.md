---
title: "블루투스 — BLE·Mesh (Bluetooth BLE Mesh)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 62
---

# 📖 【암기용】 개념 완전 이해

> 목적: Bluetooth BLE Mesh를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: BLE 저전력 무선 통신에 다중 홉 Mesh 전달 구조를 결합한 근거리 IoT 네트워크
- **왜 필요한가**: 조명, 센서, 비콘처럼 배터리 기반 기기가 수년 단위로 동작하면서 건물 전체에 메시지를 전달해야 함
- **핵심 직관**: 한 사람이 멀리 외치지 않고, 가까운 사람에게 짧게 전달해 건물 전체에 소식을 퍼뜨리는 방식임

## 깊이 이해
- **배경·문제의식**: Classic Bluetooth는 오디오·주변기기 연결 중심이고, BLE는 저전력 센서 통신 중심임. BLE Mesh는 BLE 광고 채널 위에서 메시지를 Flooding 방식으로 전달해 다수 노드 제어를 지원함.
- **작동 원리**: Provisioner가 노드에 NetKey·AppKey·주소를 부여하고, Relay Node가 메시지를 재전송함. Low Power Node는 Friend Node에 메시지 저장을 맡겨 배터리 소모를 줄임.
- **비유**: 야간 경비원이 각 층마다 무전으로 짧은 메시지를 이어 전달하고, 잠자는 근무자는 대리 수신자가 메시지를 보관해 깨면 전달받는 구조와 같음.
- **구체 예시**: 사무실 조명 300개를 BLE Mesh로 구성하면 스위치 메시지가 Relay를 거쳐 그룹 주소로 전파되고, TTL 5로 재전송 범위를 제한함.
- **흔한 오해·주의점**: BLE Mesh는 IP 라우팅 Mesh가 아님. BLE 광고 기반 Managed Flooding이며, 대용량 데이터 전송보다 소형 제어 메시지에 적합함.

## 연결 개념
- Bluetooth LE — 2.4GHz ISM 대역 저전력 근거리 통신
- Zigbee/Thread — IEEE 802.15.4 기반 저전력 Mesh 대안
- Matter — 스마트홈 상호운용 애플리케이션 계층

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: BLE와 Mesh를 구분하고, 저전력·다중 홉·키 기반 보안·Friend/Relay 구조를 적용 조건과 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Bluetooth BLE Mesh는 BLE 광고 채널과 Managed Flooding으로 다수 IoT 노드를 제어하는 저전력 Mesh 네트워크이다.
> 2. **가치**: Relay, Friend, Low Power Node 구조로 건물 조명·센서·비콘의 배터리 수명과 커버리지를 동시에 설계한다.
> 3. **판단 포인트**: 데이터 크기, 메시지 빈도, TTL, Relay 밀도, NetKey/AppKey 분리, 2.4GHz 간섭을 기준으로 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| BLE와 Classic Bluetooth 구분 확인 | 저전력 GATT/Advertising, 2.4GHz, 소형 데이터 | 이어폰 연결 기술로만 설명 금지 |
| BLE Mesh 구조 이해 확인 | Provisioner, Relay, Friend, Low Power Node | IP 라우팅 Mesh로 오해 금지 |
| IoT 적용 판단 확인 | TTL, 그룹 주소, 키 분리, 간섭 관리 | Wi-Fi 대체 대용량 전송으로 단정 금지 |

> 요약: 이 문제는 BLE 저전력 특성과 Mesh 전달 구조를 분리해 설명하고, IoT 제어망 적용 기준을 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

Bluetooth BLE Mesh는 BLE 기반 저전력 단말을 다중 홉으로 연결하는 IoT 제어망이다. 스마트 조명·센서·비콘은 수바이트~수십바이트 상태 메시지를 긴 주기로 송수신하므로 전력 소모와 설치 범위가 핵심 조건이다. BLE Mesh는 2.4GHz BLE 생태계를 활용하면서 Relay와 Friend 기능으로 건물 단위 확장을 지원함.

---

## Ⅱ. 구조 및 구성요소

```text
Provisioner -> Node Provisioning -> NetKey/AppKey Distribution
Sensor/Switch -> Advertising Bearer -> Relay Node -> Group Address
Low Power Node -> Friend Node -> Stored Message -> Wakeup Receive
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Provisioner | 노드 가입, 주소·키 배포 | NetKey, AppKey, Device Key 관리 |
| Relay Node | 메시지 재전송 | TTL 기반 전파 범위 제어 |
| Friend Node | LPN 메시지 대기 저장 | Poll Timeout, Friend Queue |
| Low Power Node | 배터리 기반 절전 노드 | 주기적 Poll로 메시지 수신 |
| Model | 기능 단위 표준 인터페이스 | Generic OnOff, Lightness 등 |

> 요약: BLE Mesh는 Provisioning, Relay, Friend/LPN, Model이 결합해 저전력 다중 노드 제어를 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
기기 등록 -> Provisioning -> Key/Address 설정
-> Publish Message -> Relay 재전송 -> Subscribe Group 수신
-> LPN Sleep -> Friend Queue 저장 -> Poll 후 수신
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Provisioner가 노드 인증·주소·키 설정 | Device Key, NetKey, AppKey |
| 2 | 노드가 Model 기반 메시지 발행 | Opcode, Source, Destination |
| 3 | Relay Node가 TTL 감소 후 재전송 | TTL, Replay Protection List |
| 4 | 구독 노드가 그룹 주소 메시지 처리 | Subscribe Address 매칭 |
| 5 | LPN은 Friend Poll로 대기 메시지 수신 | Poll Interval, Queue Depth |

> 요약: BLE Mesh는 가입-키배포-발행-중계-구독-절전 수신 순서로 다수 기기 제어 메시지를 전달한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | BLE Mesh | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 물리 대역 | Wi-Fi 2.4/5GHz | BLE 2.4GHz ISM | Bluetooth Mesh Profile |
| 전달 방식 | 중앙 AP 경유 | Managed Flooding | TTL, Relay Retransmit |
| 전력 구조 | 상시 수신 필요 | LPN/Friend 절전 | 코인셀 기반 센서 적용 |
| 데이터 유형 | 영상·파일 전송 | 상태·제어 메시지 | 수바이트~수십바이트 제어 |

> 요약: BLE Mesh는 대용량 전송보다 저전력 제어 메시지와 다수 노드 상태 동기화에 맞춘 구조이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | BLE Mesh | 선택 기준 |
|:---|:---|:---|:---|
| 스마트홈 | Zigbee/Thread | Bluetooth 생태계 활용 | BLE 칩 탑재 기기, 스마트폰 직접 연동 |
| 커버리지 | 단일 BLE 연결 | Relay 다중 홉 | 건물 내 조명·센서 수십~수백대 |
| 상호운용 | 벤더 전용 프로파일 | 표준 Model 기반 | Generic/Lighting Model 지원 여부 |

> 요약: BLE Mesh는 스마트폰 접근성과 BLE 칩 보급을 활용할 때 선택 가치가 높다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 메시지 중복 | Flooding 재전송 | TTL, Relay Retransmit Count 제한 | Duplicate Packet Ratio |
| 2.4GHz 간섭 | Wi-Fi, Zigbee와 채널 경쟁 | 채널 스캐닝, 재전송 파라미터 조정 | Packet Error Rate |
| 키 관리 오류 | NetKey/AppKey 혼용 | 키 계층 분리, Key Refresh 절차 | Failed Auth Count |

> 요약: BLE Mesh 운영 리스크는 중복 전송, 2.4GHz 간섭, 키 관리이며 파라미터와 키 절차로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전달 지연 | 조명 제어 p95 300ms 이하 | 현장 패킷 캡처, 이벤트 로그 |
| 배터리 | LPN 1년 이상 동작 | 전류 프로파일 측정 |
| 네트워크 품질 | Packet Delivery Ratio 99% 이상 | Relay별 수신율, RSSI 맵 |

> 요약: BLE Mesh 도입 평가는 제어 지연, 배터리 수명, 패킷 전달률을 설치 환경별로 검증해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 사무실 조명망은 구역별 그룹 주소와 TTL 3~5를 설정해 불필요한 층간 재전송을 제한함
2. 배터리 센서는 LPN으로 구성하고 Friend Queue 크기와 Poll Interval을 트래픽 주기에 맞게 산정함
3. 보안 운영은 NetKey/AppKey 분리, Key Refresh, Replay Protection List 점검을 배포 절차에 포함함

**결론 (2줄):**
- 기술사 판단: 소형 상태·제어 메시지와 배터리 기기가 중심이면 BLE Mesh, IP 기반 상호운용이 우선이면 Thread·Matter를 검토함
- 향후 방향: BLE Mesh는 스마트 조명·자산 추적·비콘과 결합되고, Matter 연동 게이트웨이와 공존 구조가 필요함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "BLE Mesh를 설명하시오" | Provisioning, Relay, Friend/LPN 흐름 | BLE·Zigbee·Thread 비교 |
| 요구사항 명시형 | "스마트 조명망 설계 방안을 제시하시오" | 그룹 주소, TTL, LPN 수신 흐름 | 지연·배터리·간섭 지표와 리스크 |

> 요약: 설명형은 BLE Mesh 구성 원리, 설계형은 실제 건물 제어망의 TTL·Relay·전력 지표 중심으로 전개한다.
