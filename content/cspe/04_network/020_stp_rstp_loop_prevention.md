---
title: "STP·RSTP·PVST+ 루프 방지 (STP RSTP Loop Prevention)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 20
---

# 📖 【암기용】 개념 완전 이해

> 목적: STP, RSTP, PVST+를 처음 봐도 L2 루프가 왜 치명적이고 BPDU로 어떻게 루프를 막는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 스위치 이중화 링크에서 루프를 방지하기 위해 일부 포트를 차단하고 장애 시 대체 경로를 여는 L2 프로토콜
- **왜 필요한가**: 이더넷 프레임에는 IP TTL 같은 수명 제한이 없다. L2 루프가 생기면 broadcast storm, MAC table flapping, CPU 과부하가 발생한다.
- **핵심 직관**: 여러 다리가 있는 섬에서 평소에는 한 다리를 막아 순환도로를 없애고, 주 다리가 끊기면 막아둔 다리를 여는 방식이다.

## 깊이 이해
- **배경·문제의식**: 스위치망은 장애 대비를 위해 중복 링크를 구성한다. 그러나 L2는 루프를 자동 폐기하지 못하므로 STP가 루트 브리지를 선출하고 포트 역할을 정해 루프 없는 트리를 만든다.
- **작동 원리**: 스위치들은 BPDU를 교환해 가장 낮은 Bridge ID를 가진 장비를 root bridge로 선택한다. 각 스위치는 root port, designated port, blocked port를 정하고, RSTP는 포트 역할과 상태 전환을 단순화해 수렴 시간을 줄인다.
- **비유**: 교통 관제소가 여러 우회도로 중 하나만 열어 교차로 순환 정체를 막고, 사고 시 예비도로 신호를 바꾸는 구조다.
- **구체 예시**: IEEE 802.1D STP는 listening 15초, learning 15초, max age 20초로 수렴이 30~50초 걸릴 수 있다. IEEE 802.1w RSTP는 proposal/agreement로 수 초 이내 전환을 목표로 한다.
- **흔한 오해·주의점**: STP를 끄면 이중화 링크가 즉시 모든 대역폭을 쓰는 것이 아니라, L2 루프와 broadcast storm 위험이 커진다. 대역폭 활용은 LACP, MLAG, L3 ECMP로 설계해야 한다.

## 연결 개념
- BPDU — STP 제어 프레임, root bridge와 포트 역할 결정
- VLAN/PVST+ — VLAN별 별도 spanning tree로 경로 분산
- LACP/MLAG — 루프 없는 링크 집계와 이중화 대안

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: STP 답안은 root bridge 선출, 포트 역할, BPDU guard, RSTP 수렴 차이, PVST+ VLAN별 트리까지 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: STP는 BPDU를 교환해 root bridge를 선출하고 일부 포트를 차단해 L2 루프 없는 spanning tree를 만드는 프로토콜이다.
> 2. **가치**: 중복 링크를 유지하면서 broadcast storm, MAC flapping, frame duplication을 방지한다.
> 3. **판단 포인트**: 802.1D, 802.1w, PVST+, root priority, port cost, BPDU Guard, convergence time을 비교해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| L2 루프 원인 이해 확인 | TTL 없음, broadcast storm, MAC flapping | 라우팅 루프와 동일하게 서술 |
| STP 동작 원리 확인 | Root bridge, BPDU, root/designated/blocked port | 포트 역할 없이 차단만 설명 |
| RSTP/PVST+ 비교 확인 | 802.1D vs 802.1w, VLAN별 tree | STP를 대역폭 집계 기술로 서술 |

> 요약: STP 문제는 루프 피해, BPDU 기반 트리 구성, RSTP·PVST+ 차이를 수렴 시간과 VLAN 관점으로 써야 한다.

---

## Ⅰ. 개요 및 필요성

- 정의: 이더넷 스위치망의 L2 루프를 방지하는 프로토콜
- 배경: 중복 링크가 있는 LAN에서 일부 포트를 차단해 loop-free tree를 구성함
- 필요성: RSTP는 수렴 지연을 줄이고, PVST+는 VLAN별 spanning tree로 경로를 분산해야 함

---

## Ⅱ. 구조 및 구성요소

```text
Switches Exchange BPDU -> Elect Root Bridge
  / Root Port
  / Designated Port
  / Alternate or Blocked Port
Loop-Free Tree -> Data Forwarding
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| BPDU | STP 제어 정보 교환 | root ID, bridge ID, cost 포함 |
| Root Bridge | 트리 기준점 | 낮은 priority와 MAC 기준 |
| Port Role | 전달·차단 역할 결정 | root, designated, alternate |
| Port State | 프레임 전달 상태 | blocking, learning, forwarding |

> 요약: STP 구조는 BPDU, root bridge, 포트 역할·상태 결정으로 루프 없는 트리를 만든다.

---

## Ⅲ. 동작원리 및 흐름도

```text
BPDU Receive -> Root Bridge Election -> Root Path Cost Compare
  -> Port Role Assign -> Non-Selected Port Block
  -> Link Failure -> Recalculate and Forward
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 스위치가 BPDU를 교환해 root bridge 선출 | lowest bridge ID |
| 2 | 각 스위치가 root port 결정 | lowest root path cost |
| 3 | 세그먼트별 designated port 선정 | port cost, bridge ID |
| 4 | 대체 포트 차단 및 장애 시 전환 | convergence time |

> 요약: STP는 root를 기준으로 최저 cost 경로만 forwarding 상태로 두고 나머지 경로를 차단한다.

---

## Ⅳ. 특징

| 구분 | STP 802.1D | RSTP 802.1w | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 수렴 방식 | listening, learning 단계 | proposal/agreement | STP 30~50초 가능 |
| 포트 역할 | root, designated, blocked | root, designated, alternate, backup | RSTP 수 초 목표 |
| VLAN 처리 | 공통 tree | 구현별 VLAN 연계 | PVST+는 VLAN별 tree |
| 운영 보호 | 기본 BPDU 처리 | edge port, BPDU guard | root guard, loop guard |

> 요약: RSTP는 802.1D보다 포트 전환 절차를 줄이고, PVST+는 VLAN별 경로 분산을 가능하게 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | STP/RSTP | LACP/MLAG/L3 ECMP | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 일부 링크 차단 | 링크 병렬 사용 | L2 단순 이중화는 RSTP, 대역폭 활용은 LACP/MLAG |
| 비용/성능 | 구성 단순, 차단 링크 발생 | 장비 기능 요구 | 회선 활용률과 장비 지원 비교 |
| 운영/위험 | root 오설정, BPDU 공격 | split-brain, L3 설계 필요 | 보호 기능과 장애 도메인 기준 |

> 요약: 루프 방지만 필요하면 RSTP, 대역폭 활용과 수 초 이내 이중화 전환이 필요하면 LACP, MLAG, L3 ECMP를 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Broadcast Storm | STP 차단 실패, BPDU 손실 | storm-control, loop guard | broadcast pps |
| Root 탈취 | 낮은 priority 장비 접속 | root guard, priority 고정 | root bridge 변경 로그 |
| Edge 포트 루프 | 사용자 스위치 연결 | BPDU guard, portfast 제한 | err-disable event |

> 요약: STP 운영 리스크는 storm, root 변경, edge 루프이며 guard 기능과 포트 정책으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Root 일관성 | 지정 core switch가 root | show spanning-tree root |
| 수렴 시간 | 장애 후 목표 시간 이내 | link failover test |
| 보호 기능 | access port BPDU guard 적용 | config audit, event log |

> 요약: STP 품질은 root 일관성, 수렴 시간, BPDU 보호 기능 적용률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Core 스위치의 bridge priority를 낮게 설정해 VLAN별 root bridge를 의도한 장비로 고정함
2. 사용자 access port에는 portfast와 BPDU guard를 적용하고 trunk에는 root guard, loop guard를 적용함
3. 대역폭 활용이 필요한 uplink는 STP 차단 링크 대신 LACP, MLAG 또는 L3 ECMP 구조로 설계함

**결론 (2줄):**
- 기술사 판단: 단순 L2 이중화는 RSTP, VLAN별 경로 분산은 PVST+, 대역폭 병렬 활용은 LACP/MLAG/L3 ECMP를 선택함
- 향후 방향: Fabric 기반 EVPN/VXLAN 환경에서도 loop guard, storm-control, telemetry로 L2 장애 전파를 지속 감시해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "STP를 설명하시오" | root 선출, port role, BPDU 흐름 | STP/RSTP/PVST+ 비교 |
| 요구사항 명시형 | "L2 루프 방지 방안을 제시하시오" | BPDU guard, root guard, storm-control | LACP/MLAG/L3 ECMP 선택 기준 |

> 요약: STP는 설명형이면 BPDU 기반 트리 구성, 방안형이면 보호 기능과 대체 이중화 구조 중심으로 전환한다.
