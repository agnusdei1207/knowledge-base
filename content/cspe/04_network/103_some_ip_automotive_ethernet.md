---
title: "SOME/IP 차량 이더넷 (SOME/IP Automotive Ethernet)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 103
---

# 📖 【암기용】 개념 완전 이해

> 목적: SOME/IP를 차량 서비스 통신 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 차량 Ethernet에서 ECU 기능을 서비스로 찾아 호출하는 미들웨어 통신
- **왜 필요한가**: ADAS, 인포테인먼트, OTA가 늘면서 CAN 메시지 ID 방식만으로 대용량·동적 서비스 통신을 표현하기 어렵다.
- **핵심 직관**: SOME/IP는 차량 내부에서 "카메라 서비스가 어디 있나"를 찾고, 필요한 메서드와 이벤트를 Ethernet으로 주고받게 하는 약속이다.

## 깊이 이해
- **배경·문제의식**: 차량 E/E 아키텍처가 도메인 ECU에서 중앙집중·존 기반 구조로 이동하면서 100BASE-T1, 1000BASE-T1 Ethernet 백본이 사용된다. SOME/IP는 AUTOSAR Adaptive와 함께 서비스 지향 통신을 제공한다.
- **작동 원리**: 서비스 제공 ECU는 SOME/IP-SD로 service offer를 광고하고, 소비 ECU는 find service로 탐색한다. 이후 method call, event notification, field access를 UDP 또는 TCP 위에서 수행한다.
- **비유**: 건물 안 직원들이 내선번호표를 외우는 대신 사내 서비스 디렉터리에서 담당 서비스를 검색하고 요청을 보내는 방식과 같다.
- **구체 예시**: 주차 보조 ECU가 카메라 서비스의 service ID를 발견하고, 영상 상태 이벤트를 구독해 100Mbps Ethernet 구간에서 데이터를 처리한다.
- **흔한 오해·주의점**: SOME/IP는 Ethernet 물리 계층 자체가 아니다. 서비스 발견과 메시지 직렬화 규칙이며, 시간 결정성은 TSN·QoS 설계가 별도로 필요하다.

## 연결 개념
- AUTOSAR Adaptive — 서비스 지향 차량 SW 플랫폼
- TSN — 차량 Ethernet의 시간 결정성 보완
- CAN Gateway — 기존 제어망과 Ethernet 백본 연계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SOME/IP는 차량 Ethernet 위 서비스 발견·호출 프로토콜이며, CAN 메시지 ID 방식과 비교해 역할을 분명히 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SOME/IP는 차량 Ethernet에서 서비스 ID, method ID, event ID를 사용해 ECU 기능을 서비스로 호출하는 AUTOSAR 통신 방식이다.
> 2. **가치**: 중앙 컴퓨팅, OTA, ADAS 도메인에서 동적 서비스 발견과 이벤트 구독을 지원하여 CAN 중심 신호 통신 한계를 보완한다.
> 3. **판단 포인트**: SOME/IP는 대용량·서비스 통신에 적용하고, 시간 결정성은 TSN 802.1Qbv/Qci와 QoS 설계로 보완한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 차량 Ethernet 전환 이해 확인 | SOME/IP, SOME/IP-SD, AUTOSAR, 100BASE-T1 | Ethernet 물리 계층과 SOME/IP 혼동 |
| 서비스 지향 통신 판단 확인 | service offer/find, method, event, field | CAN ID 방식으로만 설명 |
| 실시간·보안 리스크 확인 | TSN, VLAN/QoS, SecOC/TLS, Gateway | SD 메시지 남용과 인증 누락 |

> 요약: SOME/IP 답안은 서비스 발견 구조, 호출 방식, TSN·보안 보완책을 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 차량 Ethernet 서비스 통신
- 배경: ADAS·OTA·인포테인먼트는 CAN 1Mbps 구조만으로 대용량·동적 서비스 통신을 처리하기 어려움.
- 필요성: ECU 기능을 서비스로 발견·호출하고 100Mbps~1Gbps 차량 Ethernet 백본에서 이벤트를 전달해야 함.
- 범위: SOME/IP, SOME/IP-SD, AUTOSAR Adaptive, TSN, 보안 게이트웨이를 함께 판단함.

---

## Ⅱ. 구조 및 구성요소

```text
Service Provider ECU -> SOME/IP Service -> Ethernet Switch -> Consumer ECU
Consumer ECU -> SOME/IP-SD Find -> Provider Offer -> Method/Event/Field
Gateway -> CAN Signal / SOME/IP Service Mapping
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Service Provider | 기능을 서비스 ID로 제공 | method, event, field |
| Service Consumer | 필요한 서비스를 탐색·호출 | subscription, request/response |
| SOME/IP-SD | 서비스 발견과 구독 관리 | offer service, find service |
| Ethernet Switch | 차량 백본 패킷 전달 | VLAN, QoS, TSN 연계 |
| Gateway | CAN 신호와 서비스 변환 | legacy ECU 통합 |

> 요약: SOME/IP 구조는 제공자와 소비자가 서비스 발견 후 method 호출과 event 구독을 수행하는 차량 Ethernet 미들웨어 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Provider 서비스 등록 -> SD Offer 송신 -> Consumer Find/Subscribe
-> Method Request 또는 Event Subscribe -> SOME/IP 메시지 전달
-> 응답/이벤트 수신 -> Gateway/Application 반영
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Provider가 service ID와 instance ID를 활성화 | 서비스 매니페스트 |
| 2 | SOME/IP-SD가 offer/find 메시지를 교환 | SD 수신률, TTL |
| 3 | Consumer가 method call 또는 event subscribe 수행 | method ID, event group |
| 4 | Ethernet 스위치가 VLAN/QoS 정책으로 전달 | 지연시간, packet loss |
| 5 | Application이 응답·이벤트를 처리 | timeout, retry count |

> 요약: SOME/IP는 서비스 발견, 구독, 호출, 응답 처리를 통해 차량 기능을 주소가 아닌 서비스 단위로 연결한다.

---

## Ⅳ. 특징

| 구분 | CAN 신호 통신 | SOME/IP 차량 Ethernet | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 통신 단위 | arbitration ID 메시지 | service/method/event | Service ID, Method ID |
| 대역폭 | Classical CAN 1Mbps | 100Mbps~1Gbps Ethernet | 100BASE-T1, 1000BASE-T1 |
| 발견 방식 | 정적 DBC 매핑 | SOME/IP-SD 동적 발견 | offer/find service |
| 적용 영역 | 제어 신호 | ADAS·OTA·인포테인먼트 | AUTOSAR Adaptive |

> 요약: SOME/IP는 CAN의 정적 신호 전달을 대체하기보다 Ethernet 백본에서 서비스 기반 차량 기능 호출을 담당한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | SOME/IP | 선택 기준 |
|:---|:---|:---|:---|
| 아키텍처 | 도메인별 CAN | 중앙·존 기반 Ethernet | 서비스 재사용, OTA |
| 통신 모델 | 신호 중심 | 서비스 중심 | 동적 발견과 구독 필요 |
| 시간성 | CAN ID 우선순위 | QoS/TSN 별도 설계 | ms 단위 보장 필요 시 TSN 결합 |

> 요약: SOME/IP 선택은 대역폭보다 서비스 지향 구조와 동적 발견 필요성으로 판단한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| SD 폭주 | offer/find 주기 설계 오류 | TTL, multicast scope, rate limit | SD 패킷 비율 |
| 지연 변동 | Ethernet 혼잡·우선순위 미설정 | VLAN PCP, TSN 802.1Qbv | p99 latency |
| 서비스 위조 | 인증 없는 서비스 광고 | TLS, SecOC, Gateway allowlist | 비인가 service ID |

> 요약: SOME/IP 리스크는 서비스 발견 트래픽, 지연 변동, 서비스 위조이며 SD 정책과 TSN·인증으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 서비스 발견 | SD timeout 0.1% 이하 | packet capture |
| 전송 품질 | p99 지연 요구치 이내 | 차량 Ethernet analyzer |
| 보안 탐지 | 미승인 service offer 0건 | IDS, Gateway 로그 |

> 요약: SOME/IP 품질은 SD 성공률, 서비스 호출 지연, 미승인 서비스 광고 탐지로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 서비스 카탈로그에 service ID, instance ID, method ID, event group, TTL을 정의하고 AUTOSAR 매니페스트와 일치시킴.
2. Ethernet Switch에 VLAN, PCP, TSN 802.1Qbv/Qci 정책을 적용해 제어 이벤트와 대용량 스트림을 분리함.
3. Gateway allowlist, TLS 또는 SecOC, 차량 IDS를 적용해 비인가 service offer와 비정상 method 호출을 탐지함.

**결론 (2줄):**
- 기술사 판단: 정적 제어 신호는 CAN, 동적 서비스와 대용량 이벤트는 SOME/IP over Ethernet으로 분리함.
- 향후 방향: 차량은 AUTOSAR Adaptive, SOME/IP, TSN 기반 Ethernet 백본을 결합해 SDV 서비스 배포 구조로 이동함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SOME/IP를 설명하시오" | SD, method, event 흐름 | CAN·Ethernet 역할 차이 |
| 요구사항 명시형 | "차량 Ethernet 방안을 제시하시오" | 서비스 설계와 TSN 전달 흐름 | 지연·보안·Gateway 선택 기준 |

> 요약: 설명형은 서비스 발견 원리, 설계형은 VLAN·TSN·보안 게이트웨이까지 포함해 답안을 전개한다.
