---
title: "VLAN·트렁크·액세스 포트 (VLAN Trunk Access Port)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 19
---

# 📖 【암기용】 개념 완전 이해

> 목적: VLAN, trunk, access port를 처음 봐도 같은 스위치 안에서 논리적 LAN을 나누는 원리를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 하나의 물리 스위치 인프라를 VLAN ID 기준으로 여러 L2 브로드캐스트 도메인으로 분리하는 기술
- **왜 필요한가**: 모든 단말이 같은 L2 도메인에 있으면 ARP, broadcast, 장애 영향 범위가 커진다. VLAN은 부서·서비스·보안 구역별로 L2 범위를 나누고, trunk는 여러 VLAN을 스위치 간 한 링크로 전달한다.
- **핵심 직관**: 같은 건물에 여러 회사가 입주해도 출입증 색상으로 층과 구역을 구분하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 물리 스위치를 부서별로 따로 두면 포트와 케이블이 늘어난다. VLAN은 같은 물리 장비를 공유하면서 논리적 브로드캐스트 도메인을 분리한다. 서로 다른 VLAN 간 통신은 L3 라우팅이 필요하다.
- **작동 원리**: Access port는 하나의 VLAN에 속하며 단말 프레임은 보통 tag 없이 들어온다. Trunk port는 802.1Q tag 4바이트를 삽입해 여러 VLAN 프레임을 한 링크로 전달한다. Native VLAN은 tag 없는 프레임 처리에 사용된다.
- **비유**: Access port는 한 부서 전용 출입문이고, trunk는 여러 부서 물품을 색상 라벨로 구분해 나르는 공용 엘리베이터다.
- **구체 예시**: VLAN ID는 12비트로 1~4094 범위를 사용한다. 802.1Q tag는 TPID 0x8100과 TCI를 포함하며, PCP 3비트로 우선순위를 표시한다.
- **흔한 오해·주의점**: VLAN은 L2 분리 기술이지 완전한 보안 경계가 아니다. inter-VLAN 라우팅, ACL, DHCP snooping, DAI 같은 통제를 함께 적용해야 한다.

## 연결 개념
- IEEE 802.1Q — VLAN tagging 표준
- Inter-VLAN Routing — 서로 다른 VLAN 간 L3 통신
- STP/RSTP — VLAN trunk 환경의 L2 루프 방지

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: VLAN 답안은 access와 trunk의 tag 처리 차이, VLAN ID 범위, native VLAN, inter-VLAN routing까지 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: VLAN은 802.1Q VLAN ID로 L2 브로드캐스트 도메인을 논리 분리하고, trunk는 여러 VLAN을 tag로 식별해 전달한다.
> 2. **가치**: 물리 인프라를 공유하면서 부서·서비스별 ARP/broadcast 범위와 장애 영향을 제한한다.
> 3. **판단 포인트**: VLAN ID 1~4094, 802.1Q tag 4B, access/trunk mode, native VLAN, inter-VLAN ACL을 확인해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| VLAN 기본 원리 확인 | 브로드캐스트 도메인 분리, VLAN ID | 서브넷과 VLAN을 동일 개념으로 서술 |
| 포트 모드 이해 확인 | access untagged, trunk tagged | trunk에 단일 VLAN만 흐른다고 서술 |
| 운영 리스크 판단 확인 | native VLAN, allowed VLAN, VLAN hopping | VLAN만으로 보안 경계 완성이라고 서술 |

> 요약: VLAN 문제는 L2 분리 원리와 802.1Q tag 처리, L3 통제 필요성을 함께 써야 한다.

---

## Ⅰ. 개요 및 필요성

- 정의: 스위치 인프라에서 L2 브로드캐스트 도메인을 논리적으로 분리하는 기술
- 배경: access port는 단말을 단일 VLAN에 연결하고, trunk port는 여러 VLAN 프레임을 802.1Q tag로 구분해 전달함
- 필요성: 대규모 LAN은 VLAN과 L3 ACL로 업무 구역을 분리해야 함

---

## Ⅱ. 구조 및 구성요소

```text
End Host -> Access Port VLAN 10 -> Switch
Switch -> Trunk Port 802.1Q Tag -> Switch
  / VLAN ID
  / Native VLAN
  / Allowed VLAN List
Inter-VLAN Routing -> L3 Gateway
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| VLAN ID | 논리 LAN 식별자 | 12비트, 1~4094 |
| Access Port | 단일 VLAN 단말 연결 | 일반적으로 untagged |
| Trunk Port | 복수 VLAN 전달 | 802.1Q tag 사용 |
| L3 Gateway | VLAN 간 라우팅 | SVI, router-on-a-stick |

> 요약: VLAN 구조는 access 단말 연결, trunk 다중 VLAN 전달, L3 gateway를 통한 VLAN 간 통신으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Host Frame In -> Access Port Assign VLAN ID
  -> Switch MAC Table Lookup per VLAN
  -> Trunk Add 802.1Q Tag -> Remote Switch Remove Tag
  -> Inter-VLAN Traffic -> L3 Gateway and ACL
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Access port가 수신 프레임에 VLAN ID 부여 | port VLAN 설정 |
| 2 | 스위치가 VLAN별 MAC table 조회 | MAC address table VLAN |
| 3 | Trunk 구간에서 802.1Q tag 삽입 | TPID 0x8100 |
| 4 | 다른 VLAN 목적지는 L3 gateway로 전달 | SVI, ACL hit count |

> 요약: VLAN은 포트에서 VLAN ID를 부여하고 trunk에서 tag로 보존하며, VLAN 간 통신은 L3에서 제어한다.

---

## Ⅳ. 특징

| 구분 | Access Port | Trunk Port | 수치·표준 포인트 |
|:---|:---|:---|:---|
| VLAN 수 | 단일 VLAN | 복수 VLAN | VLAN ID 1~4094 |
| 프레임 처리 | 보통 untagged | 802.1Q tagged | tag 4바이트 |
| 연결 대상 | PC, 프린터, AP 단말 | 스위치, 라우터, 서버 NIC | allowed VLAN list |
| 위험 | 잘못된 VLAN 배정 | native VLAN mismatch | DTP 비활성 권장 |

> 요약: Access는 단말용 단일 VLAN, trunk는 장비 간 복수 VLAN 전달이며 tag와 native VLAN 정책이 다르다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 물리 분리 | VLAN 논리 분리 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 스위치·케이블 별도 | 동일 인프라에서 VLAN 분리 | 일반 업무망은 VLAN, 고위험망은 물리 분리 |
| 비용/성능 | 장비 수 증가 | 포트 활용률 증가 | 장애 영향과 규제 기준 비교 |
| 운영/위험 | 구성 단순 | trunk, ACL, DHCP 보안 필요 | 변경 관리 체계 필요 |

> 요약: VLAN은 일반 업무 구역 분리에 적합하지만 고위험 구역은 물리 분리와 방화벽 통제를 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| VLAN Hopping | native VLAN, DTP 악용 | native VLAN 미사용 대역, DTP off | 비인가 VLAN 통신 0건 |
| Broadcast 확산 | VLAN 범위 과대 | VLAN 크기 제한, storm-control | broadcast pps |
| Trunk 오류 | allowed VLAN 누락 | trunk allowed list 표준화 | VLAN mismatch log |

> 요약: VLAN 리스크는 hopping, broadcast, trunk 오류이며 native VLAN과 allowed list 관리로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| VLAN 배정 | 포트별 업무 VLAN 100% 일치 | switch config audit |
| Trunk 정책 | 허용 VLAN 목록 문서 일치 | show interface trunk |
| L3 통제 | VLAN 간 ACL hit 검증 | SVI ACL log |

> 요약: VLAN 운영 품질은 포트 배정, trunk 허용 목록, inter-VLAN ACL로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 사용자, 서버, 관리, 무선, 음성 VLAN을 분리하고 VLAN ID와 IP subnet을 1:1로 매핑해 운영 문서화함
2. Trunk는 필요한 VLAN만 allowed list에 포함하고 native VLAN은 사용자 VLAN과 분리된 미사용 대역으로 설정함
3. Inter-VLAN 통신은 L3 gateway ACL, DHCP snooping, Dynamic ARP Inspection으로 제어함

**결론 (2줄):**
- 기술사 판단: 일반 사무망은 VLAN 기반 논리 분리, 규제·고위험 구간은 물리 분리 또는 방화벽 zone 분리를 선택함
- 향후 방향: NAC, SDN fabric, microsegmentation과 연계해 VLAN 중심 분리를 사용자·애플리케이션 정책 기반으로 확장해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "VLAN을 설명하시오" | access, trunk, inter-VLAN 흐름 | 포트 모드와 802.1Q 비교 |
| 요구사항 명시형 | "망 분리 방안을 제시하시오" | VLAN ID, ACL, trunk 정책 | VLAN hopping, broadcast 대응 |

> 요약: VLAN은 설명형이면 tag 처리, 설계형이면 업무 구역 분리와 L3 통제 중심으로 전환한다.
