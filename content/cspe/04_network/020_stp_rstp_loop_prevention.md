---
title: "STP·RSTP·PVST+ 루프 방지 (STP RSTP Loop Prevention)"
date: "2026-07-05"
author: "Claude Opus 4.6"
tags:
  - "cspe-network"
weight: 20
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: STP(Spanning Tree Protocol)는 **L2 스위치** 이중화 환경에서 물리적 루프 경로를 감지하고, 특정 포트를 논리적으로 차단(Blocking)하여 **루프 프리 트리(Loop-Free Tree)** 토폴로지를 구성하는 IEEE 802.1D 표준 프로토콜임.
- **왜 필요한가**: 이더넷 프레임(018 참조)에는 IP 패킷의 TTL 같은 수명 필드가 없어, 스위치 간 원형 경로가 존재하면 브로드캐스트가 무한 순환하며 수초 내에 망이 마비됨(브로드캐스트 스톰).
- **핵심 직관**: 삼각형으로 연결된 골목(이중화)에서 차가 원형으로 돌아 막히는 걸 막기 위해, 바리케이드(Blocking)를 세워 강제로 막다른 길(Tree)을 만들고, 메인 도로가 끊기면 바리케이드를 치워 우회시키는 것.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| 브로드캐스트 스톰 (상위 키워드) | 프레임이 루프 경로를 무한 순환하며 망 대역폭을 잠식하는 현상 | 원형 교차로에서 차가 빠져나가지 못하고 영원히 도는 것 |
| BPDU (Bridge Protocol Data Unit) | 스위치 간 2초 주기로 교환하는 제어 프레임, Root ID·Cost 포함 | 스위치끼리 주고받는 명함·투표 용지 |
| Root Bridge | BPDU 선출로 결정된 트리의 최상위 중심 스위치 | 마을 이장(Priority 가장 낮은 스위치) |
| Root Port (RP) | Non-Root 스위치에서 Root로 가는 최소 Cost 포트, Forwarding 상태 | Root까지 가장 가까운 출구 |
| Designated Port (DP) | 세그먼트당 하나 존재하는 데이터 전달 포트, Forwarding 상태 | 도로 구간의 공식 출입구 |
| Non-Designated Port (NDP) | 루프 방지를 위해 차단된 잉여 포트, Blocking 상태 | 바리케이드가 세워진 골목 |
| Path Cost | 링크 대역폭에 반비례하는 경로 비용(1Gbps=4, 10Gbps=2) | 도로 통행료(넓은 도로일수록 저렴) |
| RSTP (802.1w) | STP의 50초 수렴 한계를 1초 이내로 단축한 개선 프로토콜 | 바리케이드를 5초 만에 치우는 긴급 대응반 |

## 깊이 이해
- **배경·문제의식**: 스위치 하나가 고장 나면 전체 망이 끊기므로 이중화(Redundancy)를 구성함. 그러나 이중화는 물리적 루프를 만들고, L2 프레임에 TTL이 없어 브로드캐스트가 무한 순환함. 단 1초의 루프로도 스위치 CPU 100%, MAC 테이블 오염, 정상 통신 불가 상태에 빠짐.
- **STP 작동 원리**: ① 모든 스위치가 BPDU를 2초 간격으로 멀티캐스트하여 서로의 Bridge ID(Priority + MAC)를 교환함. ② Priority가 가장 낮은(기본 32768) 스위치가 Root Bridge로 선출됨. ③ 각 Non-Root 스위치는 Root까지의 Path Cost가 최소인 포트를 Root Port로 지정함. ④ 각 세그먼트에서 Root로의 Cost가 가장 낮은 포트가 Designated Port가 됨. ⑤ 나머지 포트는 Non-Designated(Blocking)로 차단되어 루프가 제거됨.
- **STP 상태 천이와 50초 문제**: 장애 발생 시 Blocking 포트가 Forwarding으로 전환되기까지 Blocking(Max Age 20초) → Listening(Forward Delay 15초) → Learning(Forward Delay 15초) → Forwarding 총 50초가 소요됨. 이 동안 해당 경로는 데이터 전달이 불가하여 서비스 단절이 발생함.
- **RSTP 개선점**: ① 포트 상태를 5단계에서 3단계(Discarding→Learning→Forwarding)로 간소화함. ② 타이머 대기 대신 Proposal/Agreement 핸드셰이크로 이웃 스위치와 즉각 협상하여 1초 이내 절체함. ③ Alternate Port(백업 Root Port)·Backup Port(백업 Designated Port)를 미리 계산해두어 장애 시 즉시 활성화함.
- **비유**: STP는 사고(장애) 후 경찰(타이머)이 도착해 50초간 조사한 뒤 우회로를 열어주는 방식이고, RSTP는 이미 우회 도로에 대기 중인 응급반이 즉각 바리케이드를 치우는 방식임.
- **구체 예시**: 3대의 스위치(A·B·C)가 삼각형으로 연결된 환경에서, A가 Root(Priority 4096)로 선출되면 B-C 간 링크 중 하나가 Blocking됨. B-A 간 링크가 끊기면, RSTP에서는 B의 Alternate Port가 1초 내에 Forwarding으로 전환되어 C를 거쳐 Root에 도달함.
- **흔한 오해·주의점**: Blocking 포트는 물리적으로 비활성화된 것이 아님 — 데이터 프레임만 폐기할 뿐 BPDU는 계속 수신하여 링크 상태를 모니터링함. 또한 PC가 직접 연결되는 포트에 STP를 그대로 적용하면 부팅 시 30초간 네트워크 연결이 안 되므로 PortFast(즉시 Forwarding)를 설정해야 함.

## 연결 개념
- **VLAN(019)**: VLAN별 독립 스패닝 트리를 구성하는 PVST+, 다수 VLAN을 인스턴스로 묶는 MSTP.
- **스위칭 계층(021)**: L2 스위치의 기본 루프 방지 메커니즘으로, L3 패브릭 전환 시 STP가 불필요해짐.
- **VXLAN/EVPN(069·072)**: L3 패브릭 기반으로 STP의 경로 절반 낭비를 없애는 Active-Active 대안.

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: L2 이중화 환경에서 BPDU 교환으로 Root를 선출하고 잉여 경로를 Blocking하여 루프 프리 트리를 구성하는 프로토콜임.
> 2. **가치**: 링크 이중화(가용성)를 유지하면서 브로드캐스트 스톰에 의한 망 마비를 원천 차단함.
> 3. **판단 포인트**: STP(802.1D)의 50초 수렴 한계를 RSTP(802.1w)의 Proposal/Agreement로 1초 이내로 단축한 구조적 차이가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| L2 루프 발생 원리와 STP 방지 메커니즘 | L2 프레임 TTL 부재, BPDU 교환, Root 선출, 포트 역할(RP·DP·NDP) | STA 알고리즘만 나열하고 RSTP 개선점 누락 |
| STP→RSTP 진화의 구조적 차이 | 50초 타이머 vs Proposal/Agreement, 포트 상태 5→3단계 | STP와 RSTP를 동일 프로토콜로 혼동 |

> 요약: 이중화의 딜레마(루프)를 설명하고, BPDU 기반 포트 차단(STP)과 고속 절체(RSTP)의 구조적 차이를 대비해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 다중 L2 스위치 환경에서 BPDU 교환으로 루프를 감지하고 잉여 포트를 차단하여 트리 토폴로지를 구성하는 IEEE 802.1D 프로토콜임.
- 배경: 이더넷 프레임에 TTL 필드가 없어 이중화 경로에서 브로드캐스트가 무한 순환하며 수초 내 스위치 CPU·대역폭을 포화시킴.
- 필요성: HA(High Availability)를 위한 링크 이중화와 브로드캐스트 스톰 방지를 동시에 달성해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
[스위치 A (Root, Priority 4096)] <-- Cost 4 --> [스위치 B]
         |                                         |
      Cost 4                                    Cost 4
         |                                         |
         +----------> [스위치 C] <-- (Blocking) ----+
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| BPDU | 2초 주기 멀티캐스트 제어 프레임, Root ID·Cost 전달 | Blocking 포트도 BPDU 수신 가능 |
| Root Bridge | 트리 최상위 중심 스위치 | 1순위 Priority(기본 32768), 2순위 MAC 낮은 값 |
| Root Port (RP) | Non-Root에서 Root로 가는 최소 Cost 포트 | Forwarding 상태 |
| Designated Port (DP) | 세그먼트당 1개, 데이터 포워딩 담당 | Forwarding 상태 |
| Non-Designated Port (NDP) | 루프 방지를 위해 차단된 잉여 포트 | Blocking 상태(데이터 폐기, BPDU 수신) |

> 요약: BPDU 교환으로 Root를 선출하고, Root까지의 최단 경로(RP·DP)를 제외한 잉여 포트(NDP)를 모두 차단하여 트리를 구성함.

---

## Ⅲ. 동작원리 및 흐름도

```text
BPDU 교환 -> Root Bridge 선출 -> RP/DP 결정 -> NDP Blocking -> 장애 감지(BPDU 누락) -> 차단 포트 활성화 -> Forwarding 재개
```

1. Root 선출: 모든 스위치가 BPDU를 교환하여 Priority·MAC이 가장 낮은 스위치를 Root Bridge로 선출함.
2. 포트 역할 결정: 각 Non-Root 스위치에서 Root까지 Path Cost가 최소인 포트를 RP로, 각 세그먼트에서 Cost가 최소인 포트를 DP로 지정함.
3. 잉여 포트 차단: RP·DP가 아닌 포트를 NDP(Blocking)로 설정하여 루프를 논리적으로 제거함.
4. 장애 복구: Root로부터 BPDU가 Max Age(20초) 동안 도달하지 않으면 토폴로지를 재계산하고, Blocking 포트를 Listening→Learning→Forwarding(STP: 50초, RSTP: 1초 이내)으로 전환함.

> 요약: BPDU 기반 선출 → 최단 경로 유지 → 잉여 차단 순서로 트리를 구성하며, 장애 시 차단 포트를 활성화하여 우회 경로를 확보함.

---

## Ⅳ. 특징

- STP 수렴 지연: Blocking→Forwarding 전환에 Max Age(20초)+Forward Delay(15초)×2 = 최대 50초가 소요되어 서비스 단절이 발생함.
- RSTP 고속 절체: Proposal/Agreement 핸드셰이크로 타이머 대기 없이 1초 이내 절체하며, Alternate/Backup 포트를 미리 계산해 즉시 활성화함.
- PVST+: Cisco 전용, VLAN별 독립 STP 트리를 구성하여 트래픽 로드밸런싱이 가능하나 스위치 CPU·메모리 부하가 증가함.
- MSTP(802.1s): 다수 VLAN을 인스턴스(Instance)로 묶어 STP 트리 수를 줄여 PVST+의 자원 부담을 경감함.
- 경로 낭비 한계: Blocking된 포트는 장애 시에만 활성화되므로 평시 대역폭의 약 절반이 유휴 상태로 낭비됨.

> 요약: STP의 50초 지연은 RSTP로 해결하였고, VLAN별 자원 낭비는 MSTP로 경감하나, 경로 절반 낭비의 근본 한계는 L3 패브릭 전환으로 극복함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | STP (802.1D) | RSTP (802.1w) | 선택 기준 |
|:---|:---|:---|:---|
| 포트 상태 | 5단계(Block-Listen-Learn-Forward-Disable) | 3단계(Discarding-Learning-Forwarding) | 상태 천이 간소화 |
| 수렴 방식 | 타이머 대기(20+15+15=50초) | Proposal/Agreement 핸드셰이크(1초 이내) | 서비스 단절 허용 시간 |
| 백업 포트 | 별도 지정 없음(재계산 필요) | Alternate·Backup 포트 사전 계산 | 장애 복구 속도 |
| 적용 현황 | 레거시, 현재 거의 미사용 | 현대 스위치 기본 프로토콜 | 신규 구축 시 RSTP 필수 |

> 요약: 신규 환경은 RSTP를 기본 적용하고, VLAN별 로드밸런싱이 필요하면 Rapid-PVST+ 또는 MSTP를 선택함.

**리스크·대응:**
- 단말 연결 지연: PC 부팅 시 STP Listening/Learning(30초) 대기로 DHCP 할당 실패 → 종단 포트에 PortFast 설정(즉시 Forwarding) (지표: 연결 후 통신 개시 시간)
- Root Bridge 탈취 공격: 공격자가 Priority 0인 BPDU를 유포하여 Root를 가로챔 → BPDU Guard 설정(PortFast 포트에서 BPDU 수신 시 err-disable) (지표: err-disable 로그 발생 건수)

**점검 지표:**
- 수렴 시간: 링크 절체 후 Forwarding 복구까지 소요 시간 — RSTP 기준 1초 이내 목표
- 토폴로지 변경 빈도: TCN(Topology Change Notification) 발생 횟수 — 스위치 로그 모니터링

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Root 강제 지정: 백본 스위치 2대의 Priority를 4096(Primary Root)·8192(Secondary Root)로 고정하여, 저사양 액세스 스위치가 Root로 선출되는 토폴로지 불안정을 방지함.
2. 엣지 포트 최적화: PC·서버 연결 포트에 `spanning-tree portfast edge`를 설정하고, BPDU Guard를 병행 적용하여 30초 대기 제거와 동시에 루프 유발 장비 연결을 자동 차단함.
3. VLAN 로드밸런싱: 홀수 VLAN(10·30)은 백본 A를 Root, 짝수 VLAN(20·40)은 백본 B를 Root로 구성(MSTP/Rapid-PVST+)하여 Blocking 포트를 교차 분산시키고 업링크 대역폭을 최대 활용함.

**결론:**
- 기술사 판단: 액세스 계층은 RSTP+PortFast+BPDU Guard 조합으로 빠른 절체와 보안을 동시에 확보하고, 코어 계층은 MSTP로 자원 효율을 최적화함.
- 향후 방향: 데이터센터 코어망은 STP의 경로 절반 낭비를 근본적으로 제거하기 위해 L3 패브릭(VXLAN/EVPN, Spine-Leaf) 기반 Active-Active 구성으로 전환하는 추세임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "STP의 동작 원리를 설명하시오" | BPDU 교환, Root 선출, 포트 역할, 상태 천이 | STP vs RSTP 수렴 차이, L3 패브릭 전환 |
| 요구사항 명시형 | "STP와 RSTP를 비교하시오", "VLAN 로드밸런싱" | Proposal/Agreement 핸드셰이크 동작 | PVST+/MSTP 로드밸런싱, 보안 설정 방안 |
