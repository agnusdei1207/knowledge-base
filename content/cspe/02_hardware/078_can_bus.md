---
title: "CAN 버스 통신 (CAN Bus)"
date: "2026-07-01"
tags:
  - "cspe-hardware"
weight: 78
---

# 📖 【암기용】 개념 완전 이해

> 목적: CAN Bus를 처음 봐도 여러 ECU가 충돌 없이 동시에 신호를 보내는 원리를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 두 가닥 차동 신호선으로 여러 ECU가 메시지 identifier 우선순위에 따라 충돌 없이 통신하는 ISO 11898 멀티마스터 직렬 버스
- **왜 필요한가**: 자동차 한 대에 수십 개 ECU가 실시간으로 센서·제어 데이터를 주고받아야 하는데, point-to-point 배선은 배선량과 고장점이 기하급수적으로 늘어난다.
- **핵심 직관**: 여러 사람이 동시에 말하다가 낮은 번호를 부른 사람이 계속 말하고 나머지는 자동으로 침묵하는 회의실 규칙과 같다.

## 깊이 이해
- **배경·문제의식**: Bosch는 1980년대 자동차 배선 복잡도와 실시간 제어 요구를 해결하려고 CAN을 개발했고 이후 ISO 11898로 표준화되었으며 산업 자동화 설비에도 확산되었다.
- **배경·문제의식**: 기존 이더넷의 CSMA/CD는 충돌이 발생한 뒤 감지하고 재전송하므로 지연이 발생하지만, 차량 제어 신호는 충돌 자체가 없어야 하는 실시간성이 요구된다.
- **작동 원리**: CAN_H와 CAN_L 두 선의 전압 차이로 dominant(논리 0)와 recessive(논리 1) 두 상태를 표현하며, 두 상태가 동시에 나오면 dominant가 항상 우선한다.
- **작동 원리**: 여러 노드가 동시에 송신을 시작하면 각 노드는 자신이 보낸 비트와 버스에서 읽히는 비트를 비교하는 non-destructive bitwise arbitration을 수행한다.
- **작동 원리**: recessive를 보냈는데 버스에서 dominant가 읽히면 그 노드는 즉시 송신을 멈추고 낮은 숫자의 identifier, 즉 높은 우선순위 메시지가 충돌 없이 버스를 점유한다.
- **작동 원리**: 이 방식은 CSMA/CR(Carrier Sense Multiple Access/Collision Resolution)이라 부르며, 충돌 후 재전송하는 이더넷의 CSMA/CD와 달리 충돌 자체를 사전에 회피한다.
- **비유**: dominant 비트는 마이크를 잡고 말하는 사람이고 recessive 비트는 침묵하는 사람이며, 낮은 identifier 번호를 가진 노드가 끝까지 마이크를 쥔다.
- **구체 예시**: 엔진 RPM 센서 메시지가 identifier 0x100, 차체 도어락 메시지가 identifier 0x700이면 두 메시지가 동시에 송신을 시작해도 0x100이 우선순위를 가져 충돌 없이 전송된다.
- **구체 예시**: 표준 CAN 2.0A는 11-bit identifier로 최대 8byte payload를 실어보내고, 확장 CAN 2.0B는 29-bit identifier를 사용하며, CAN FD(Flexible Data-rate)는 payload를 최대 64byte까지 늘리고 data phase에서 더 높은 bit rate로 전환한다.
- **구체 예시**: 버스 양 끝단에는 120Ω 종단 저항을 설치해 신호 반사를 방지하며, 중간 노드에는 종단 저항을 달지 않는다.
- **흔한 오해·주의점**: arbitration에서 지는 노드는 데이터를 잃는 것이 아니라 송신을 잠시 멈췄다가 버스가 idle이 되면 재시도하므로 메시지가 소실되지 않는다.
- **흔한 오해·주의점**: identifier가 낮다고 항상 "중요한 메시지"는 아니며, 설계자가 실시간성 요구에 따라 낮은 identifier를 배정한 결과일 뿐이다.
- **흔한 오해·주의점**: 오류가 계속 발생하는 노드는 error-active에서 error-passive를 거쳐 bus-off 상태로 전이해 스스로 버스 참여를 중단하므로, 고장 노드가 버스 전체를 마비시키지 않도록 설계되어 있다.

## 연결 개념
- ISO 11898 — CAN의 물리 계층·데이터링크 계층 표준
- CAN FD(Flexible Data-rate) — payload 64byte, 이중 bit rate로 확장된 후속 표준
- LIN·FlexRay — CAN보다 저비용 또는 고신뢰 실시간성을 목표로 하는 인접 차량 네트워크 프로토콜

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CAN Bus 답안은 차동 신호, non-destructive bitwise arbitration, CAN 2.0A/2.0B/CAN FD 규격 차이, 오류 상태 전이, 종단 저항을 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CAN Bus는 CAN_H/CAN_L 차동 신호와 identifier 기반 non-destructive bitwise arbitration으로 다중 ECU가 충돌 없이 통신하는 ISO 11898 표준 버스이다.
> 2. **가치**: 충돌 발생 후 재전송하는 CSMA/CD와 달리 충돌 자체를 회피하는 CSMA/CR로 실시간 우선순위 통신을 보장한다.
> 3. **판단 포인트**: payload가 8byte를 넘거나 고속 데이터 전송이 필요하면 CAN FD, 저비용 단순 제어 신호에는 classic CAN을 선택 기준으로 삼는다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 물리 계층 이해 확인 | CAN_H/CAN_L 차동 신호, dominant/recessive, 120Ω 종단 | 차동 신호 원리 없이 "두 선을 쓴다"고만 서술 |
| 충돌 해결 방식 이해 확인 | non-destructive bitwise arbitration, CSMA/CR | CSMA/CD와 혼동하거나 충돌 후 재전송으로 오설명 |
| 규격·오류 처리 역량 확인 | 2.0A/2.0B identifier 길이, CAN FD payload, error state 전이 | 11-bit/29-bit 수치 누락, bus-off 전이 조건 누락 |

> 요약: 이 문제는 두 선 배선 자체보다 identifier 기반 무손실 충돌 회피와 오류 상태 전이 구조를 보여야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: identifier 우선순위로 무충돌 통신하는 ISO 11898 차동 직렬 버스
- 배경: Bosch가 자동차 배선 복잡도와 실시간 제어 요구를 해결하려고 개발했고 ISO 11898로 표준화되어 산업 자동화까지 확산됨
- 필요성: 수십 개 ECU가 동시에 신호를 주고받는 환경에서 배선량 절감과 충돌 없는 실시간 우선순위 전송이 필요함

---

## Ⅱ. 구조 및 구성요소

```text
ECU Node A -> CAN Controller -> CAN Transceiver
  -> CAN_H/CAN_L Bus(Twisted Pair)
     -> Termination 120Ω(양 끝단)
  -> ECU Node B / ECU Node C / ECU Node N (Multi-Drop)
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| CAN Controller | 프레임 생성·수신, error state machine 관리 | error-active/passive/bus-off 카운터 보유 |
| CAN Transceiver | 논리 신호를 CAN_H/CAN_L 차동 전압으로 변환 | dominant/recessive 전압 레벨 생성 |
| Bus(CAN_H/CAN_L) | twisted pair 차동 신호선 | 다중 노드 multi-drop 연결 |
| Termination Resistor | 신호 반사 방지 | 120Ω, 버스 양 끝단에만 설치 |
| Identifier | 메시지 우선순위·arbitration 기준 | CAN 2.0A 11-bit, CAN 2.0B 29-bit |

> 요약: CAN Bus는 controller와 transceiver가 identifier를 담은 프레임을 차동 신호선에 실어 다중 노드가 공유하는 구조다.

---

## Ⅲ. 동작원리 및 흐름도

```text
다수 노드 동시 송신 시도 -> SOF(Start of Frame) 검출
  -> Identifier bit 단위 bitwise arbitration
  -> 패배 노드 송신 중단 / 최저 identifier 노드 송신 지속
  -> CRC/ACK/Form Check -> 정상 수신 또는 error counter 증가
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 다수 노드가 동시에 프레임 송신 시작 | SOF 검출 여부 |
| 2 | identifier bit를 순차 송신하며 버스 상태와 자기 송신 bit 비교 | dominant/recessive 일치 여부 |
| 3 | recessive 송신 중 dominant 감지 시 해당 노드 송신 중단, 최저 identifier 노드만 지속 | arbitration 승패 결정 |
| 4 | CRC, ACK slot, form check로 프레임 검증 후 오류 시 error counter 증가 | error-active/passive/bus-off 전이 여부 |

> 요약: CAN 통신은 identifier bitwise arbitration으로 충돌을 사전 회피한 뒤 CRC·ACK·form check로 프레임 무결성을 검증한다.

---

## Ⅳ. 특징

| 구분 | Classic CAN(2.0A/2.0B) | CAN FD(Flexible Data-rate) | 수치·표준 포인트 |
|:---|:---|:---|:---|
| Identifier | 11-bit(2.0A) 또는 29-bit(2.0B) | 11-bit/29-bit 동일 유지 | ISO 11898 |
| Payload | 최대 8byte | 최대 64byte | Data Length Code 확장 |
| Bit Rate | arbitration·data phase 동일 속도 | data phase에서 고속으로 전환 | dual bit-rate 구조 |
| 오류 처리 | CRC, bit monitoring, stuff bit, ACK, form check | 동일 메커니즘 + 확장 CRC | error-active/passive/bus-off |

> 요약: CAN FD는 identifier 구조는 유지하면서 payload와 data phase 속도만 확장해 대역폭 한계를 완화한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | CAN(CSMA/CR) | Ethernet(CSMA/CD) | 선택 기준 |
|:---|:---|:---|:---|
| 충돌 처리 | bitwise arbitration으로 충돌 사전 회피 | 충돌 발생 후 감지·재전송 | 실시간 우선순위 보장 필요 시 CAN |
| 대역폭 | classic 8byte, FD 64byte 제한 | 가변 프레임, 고대역폭 | 대용량 데이터 전송은 Ethernet(Automotive Ethernet) |
| 적용처 | 차량 ECU, 산업 제어 | IT 네트워크, 차량 백본망 | 실시간 제어는 CAN, 백본 데이터는 Ethernet 병행 |

> 요약: 충돌 없는 실시간 제어 신호는 CAN, 대용량 데이터 전송이 필요한 구간은 Ethernet과 병행 구성한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| bus-off 전이 | 특정 노드 오류 누적으로 error counter 임계치 초과 | 오류 원인 노드 격리, transceiver 하드웨어 점검 | error counter 값, bus-off 발생 횟수 |
| 신호 반사·간섭 | 종단 저항 미설치 또는 배선 임피던스 불일치 | 버스 양 끝단 120Ω 종단 저항 설치 확인 | 반사파 측정, 임피던스 측정값 |
| identifier 설계 오류 | 우선순위 배정 오류로 저priority 신호가 실시간성 미달 | identifier 할당표 재설계, 주기적 신호 우선순위 재검토 | 메시지 지연시간, 버스 부하율 |

> 요약: CAN 운영은 error counter 기반 bus-off 감지, 종단 저항 점검, identifier 우선순위 설계로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 버스 부하율 | bus load 70% 이하 유지 | CAN 분석기(트래픽 캡처) |
| 오류율 | error-active 상태 유지, bus-off 발생 0건 | error counter 로그 모니터링 |
| 물리 계층 품질 | 종단 저항 120Ω 양단 확인 | 저항계 측정, 신호 반사 파형 확인 |

> 요약: 도입 후 성공 여부는 버스 부하율, error counter 기반 오류율, 종단 저항 물리 품질로 판단한다.

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 실시간 제어 신호는 낮은 identifier를 배정하고 classic CAN 8byte payload로 arbitration 우선순위를 설계함
2. 센서 데이터량이 늘어나는 구간은 CAN FD로 전환해 payload 64byte와 고속 data phase를 적용하고 기존 identifier 체계를 유지함
3. 버스 양 끝단 120Ω 종단 저항 설치를 점검하고 error counter 기반 bus-off 감지 로그를 정기 모니터링함

**결론 (2줄):**
- 기술사 판단: 무충돌 실시간 제어는 CAN의 non-destructive bitwise arbitration이 이더넷 CSMA/CD보다 우수하며, 대역폭 확장이 필요하면 CAN FD를 선택함
- 향후 방향: 자율주행·ADAS로 데이터량이 늘면서 CAN FD와 Automotive Ethernet을 병행하는 zonal architecture로 발전해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CAN Bus를 설명하시오" | 차동 신호, bitwise arbitration 흐름 | classic CAN vs CAN FD 규격 차이 |
| 비교형 | "CAN과 Ethernet의 충돌 처리 방식을 비교하시오" | CSMA/CR vs CSMA/CD 처리 순서 | 대역폭, 적용처 비교 |

> 요약: 설명형은 arbitration 원리, 비교형은 CSMA/CR과 CSMA/CD의 충돌 처리 시점 차이 중심으로 답안 축을 바꾼다.
