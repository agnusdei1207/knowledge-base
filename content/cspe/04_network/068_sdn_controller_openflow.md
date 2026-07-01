---
title: "SDN 컨트롤러 — OpenFlow (SDN Controller OpenFlow)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 68
---

# 📖 【암기용】 개념 완전 이해

> 목적: SDN Controller와 OpenFlow를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: SDN Controller가 OpenFlow로 스위치 Flow Table을 제어해 패킷 처리 규칙을 설치하는 구조
- **왜 필요한가**: 장비별 분산 제어만으로는 세밀한 경로, ACL, 실험망, 테넌트 정책을 중앙에서 일관되게 제어하기 어려움
- **핵심 직관**: 스위치는 교통 표지판 역할만 하고, 관제센터가 어느 차량을 어느 차선으로 보낼지 규칙표를 내려주는 방식임

## 깊이 이해
- **배경·문제의식**: 기존 스위치는 제어와 전달이 결합되어 벤더별 구현에 의존함. OpenFlow는 Controller가 Match-Action 규칙을 Flow Table에 설치해 패킷 처리를 프로그램할 수 있게 함.
- **작동 원리**: 스위치에 매칭 규칙이 없으면 Packet-In을 Controller로 보내고, Controller는 정책을 계산해 Flow-Mod로 규칙을 설치함. 이후 같은 흐름의 패킷은 스위치가 로컬에서 처리함.
- **비유**: 출입 게이트가 처음 보는 방문객을 보안실에 문의하고, 보안실이 출입 규칙을 게이트에 등록하면 다음 방문부터 게이트가 즉시 처리하는 구조와 같음.
- **구체 예시**: 출발지 IP, 목적지 IP, TCP Port, VLAN을 Match 조건으로 삼고 Action을 Output Port 3 또는 Drop으로 설치해 세밀한 ACL과 경로 제어를 수행함.
- **흔한 오해·주의점**: OpenFlow는 SDN 구현 방식 중 하나임. 최신 상용망은 OpenFlow 외에도 BGP EVPN, NETCONF, gNMI, P4Runtime 기반 제어를 병행함.

## 연결 개념
- Flow Table — Match-Action 규칙이 저장되는 스위치 전달 테이블
- Packet-In/Flow-Mod — Controller와 스위치 간 핵심 OpenFlow 메시지
- TCAM — 고속 Match 처리에 사용되는 스위치 하드웨어 자원

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Controller와 OpenFlow 메시지, Flow Table Match-Action, TCAM 한계, 장애 시 Fail Mode를 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SDN Controller-OpenFlow 구조는 Controller가 스위치 Flow Table에 Match-Action 규칙을 설치하는 Southbound 제어 방식이다.
> 2. **가치**: Packet-In과 Flow-Mod로 초기 흐름은 중앙 정책 판단, 이후 패킷은 스위치 로컬 전달로 처리한다.
> 3. **판단 포인트**: Controller 지연, Flow Table 용량, TCAM 사용률, Secure Channel, Fail-secure/Fail-standalone 모드를 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| OpenFlow 동작 이해 확인 | Match-Action, Packet-In, Flow-Mod | OpenFlow를 라우팅 프로토콜로 설명 금지 |
| Controller 역할 확인 | 정책 계산, 토폴로지 관리, Flow 설치 | 스위치가 모든 경로를 독자 판단한다고 서술 금지 |
| 운영 한계 판단 확인 | TCAM, Controller 장애, Secure Channel | 중앙 제어 지연과 Flow 폭증 누락 금지 |

> 요약: 이 문제는 OpenFlow 메시지 흐름과 Flow Table 제어 한계를 함께 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

SDN Controller-OpenFlow는 중앙 Controller가 스위치 전달 규칙을 설치하는 SDN Southbound 구조이다. 네트워크 정책을 장비별 CLI가 아니라 프로그램 가능한 Flow Table로 관리하기 위해 필요하다. OpenFlow는 Match-Action 기반으로 ACL, 경로, 실험망, 테넌트 격리를 세밀하게 구현함.

---

## Ⅱ. 구조 및 구성요소

```text
SDN Application -> Controller Policy Engine -> OpenFlow Channel
-> OpenFlow Switch -> Flow Table -> Match/Action -> Packet Forwarding
Unknown Flow -> Packet-In -> Controller -> Flow-Mod -> Switch
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| SDN Controller | 정책 계산·Flow 설치 | ONOS, OpenDaylight 등 |
| OpenFlow Switch | Flow Table 기반 패킷 처리 | TCAM 자원 제약 |
| Secure Channel | Controller-Switch 연결 | TLS 적용 가능 |
| Flow Table | Match-Action 규칙 저장 | Priority, Timeout, Counter |
| OpenFlow Message | 제어 메시지 교환 | Packet-In, Flow-Mod, Stats |

> 요약: Controller는 OpenFlow 채널로 스위치 Flow Table을 제어하고, 스위치는 설치된 Match-Action 규칙으로 패킷을 처리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
패킷 수신 -> Flow Table 조회 -> Match 있음 -> Action 실행
Match 없음 -> Packet-In -> Controller 정책 계산
-> Flow-Mod 설치 -> 다음 패킷부터 스위치 로컬 처리
-> Stats 수집 -> 정책 조정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 스위치가 수신 패킷의 헤더를 Flow Table과 비교 | Match Field, Priority |
| 2 | 미매칭 패킷을 Packet-In으로 Controller 전달 | Packet-In Rate |
| 3 | Controller가 정책·토폴로지 기준으로 Action 계산 | ACL, Path, QoS |
| 4 | Flow-Mod로 규칙 설치 | Flow Install Success, Timeout |
| 5 | Stats 메시지로 Counter 수집 | Packet/Byte Counter, Drop |

> 요약: OpenFlow는 미매칭 흐름을 Controller가 판단하고, 규칙 설치 후 동일 흐름을 스위치가 직접 처리하는 방식이다.

---

## Ⅳ. 특징

| 구분 | 기존 스위치 제어 | OpenFlow 기반 제어 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 제어 위치 | 장비 내 제어 평면 | Controller 중앙 제어 | Southbound API |
| 처리 단위 | MAC/IP 라우팅 테이블 | Flow Match-Action | L2~L4 Header Match |
| 운영 지표 | 포트·라우팅 상태 | Flow Counter, Table Usage | TCAM 사용률 |
| 장애 모드 | 장비 자체 수렴 | Controller 연결 영향 | Fail-secure, Fail-standalone |

> 요약: OpenFlow는 세밀한 Flow 제어를 제공하지만 Flow 폭증과 Controller 연결 장애를 운영 설계에 반영해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | OpenFlow | 선택 기준 |
|:---|:---|:---|:---|
| 제어 방식 | CLI, SNMP | 프로그래머블 Flow 제어 | 연구망, 캠퍼스, 세밀한 ACL |
| 상용 DC | EVPN/VXLAN | OpenFlow Fabric | 벤더 지원, 운영 성숙도 |
| 데이터 평면 | 고정 Pipeline | Match-Action Table | TCAM 용량, Packet-In Rate |

> 요약: OpenFlow는 세밀한 중앙 제어가 필요한 환경에 맞고, 대규모 상용망은 EVPN·NETCONF와 비교 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Packet-In 폭증 | 미설치 Flow 증가 | Proactive Flow, Rate Limit | Packet-In per second |
| TCAM 고갈 | 세밀한 Match 규칙 과다 | Rule Aggregation, Timeout 조정 | Table Usage 80% 이하 |
| Controller 단절 | Secure Channel 장애 | Controller Cluster, Fail Mode 설정 | Disconnect Count, RTO |

> 요약: OpenFlow 운영은 Packet-In, TCAM, Controller 연결을 핵심 리스크로 관리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Flow 설치 | Flow-Mod 성공률 99.9% 이상 | Controller Audit, Switch Log |
| 제어 지연 | Packet-In to Flow-Mod p95 50ms 이하 | Controller Metric |
| 테이블 용량 | TCAM 사용률 80% 이하 | OpenFlow Stats, 장비 Telemetry |

> 요약: OpenFlow 품질은 Flow 설치 성공률, 제어 지연, TCAM 사용률로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 초기 트래픽은 Proactive Flow로 기본 경로를 설치하고, 예외 트래픽만 Reactive Packet-In으로 처리해 Controller 부하를 제한함
2. Flow Rule은 Prefix·Port 범위로 집계하고 Idle/Hard Timeout을 설정해 TCAM 사용률을 80% 이하로 관리함
3. Controller는 3노드 Cluster와 TLS Secure Channel을 구성하고 Fail-secure/Fail-standalone 모드를 서비스별로 지정함

**결론 (2줄):**
- 기술사 판단: 세밀한 Flow 제어와 실험망 요구가 있으면 OpenFlow, 대규모 상용 DC는 EVPN/VXLAN·NETCONF 기반 SDN을 함께 검토함
- 향후 방향: OpenFlow 경험은 P4Runtime, programmable ASIC, Intent 기반 Controller로 확장되어 데이터 평면 제어 정밀도를 높임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OpenFlow 기반 SDN을 설명하시오" | Packet-In, Flow-Mod, Stats 흐름 | Match-Action 구조와 기존 스위치 차이 |
| 요구사항 명시형 | "OpenFlow 운영 방안을 제시하시오" | Proactive/Reactive Flow 제어 | TCAM, Controller, 보안 채널 지표 |

> 요약: 설명형은 메시지 흐름, 운영형은 Packet-In과 TCAM 관리 중심으로 전개한다.
