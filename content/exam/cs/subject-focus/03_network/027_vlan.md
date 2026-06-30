---
title: "VLAN (Virtual LAN)"
date: "2026-06-30"
weight: 27
tags:
  - "exam-cspe-network"
---

## Ⅰ. 1교시 핵심 답안

> VLAN은 하나의 물리 LAN을 논리적으로 분할하여 별도의 브로드캐스트 도메인을 구성하는 기술로, `802.1Q 태깅`, `Access/Trunk`, `Inter-VLAN Routing`이 핵심이다.

- **목적**: 브로드캐스트 범위 축소, 보안 분리, 관리 효율
- **구성**: VLAN ID, Access Port, Trunk Port
- **표준**: `IEEE 802.1Q`
- **출제 포인트**: VLAN 분리와 라우팅의 관계

## Ⅱ. 구조 및 동작 원리

```text
[VLAN10 PC] -- Access -- SW1 == Trunk(802.1Q) == SW2 -- Access -- [VLAN10 PC]
[VLAN20 PC] -- Access -- SW1 == Trunk(802.1Q) == SW2 -- Access -- [VLAN20 PC]

VLAN 간 통신 -> Router 또는 L3 Switch 필요
```

- **Access Port**: 단일 VLAN 단말 접속
- **Trunk Port**: 여러 VLAN 프레임을 태그로 구분해 전달
- **VID**: VLAN 식별자
- **Inter-VLAN Routing**: 서로 다른 VLAN 간 통신은 L3 장비 필요

## Ⅲ. 비교표

| 구분 | VLAN 미적용 | VLAN 적용 |
|:---|:---|:---|
| 브로드캐스트 도메인 | 단일 | 다중 분리 |
| 보안 분리 | 낮음 | 높음 |
| 확장성 | 물리 분리 의존 | 논리 분리 가능 |
| 운영 포인트 | 단순 | 태깅/트렁크 관리 필요 |

## Ⅳ. 기술사 답안 포인트

- **설계 포인트**: 사용자, 서버, 관리, 음성 VLAN 분리
- **보안 포인트**: `Native VLAN` 불일치, `VLAN Hopping` 대응
- **확장 포인트**: 대규모 환경에서는 `VXLAN`과 비교 가능
- **연계 주제**: STP, Link Aggregation, Inter-VLAN Routing

## Ⅴ. 결론

VLAN은 단순 분할 기술이 아니라 `브로드캐스트 제어와 정책 분리`의 기본 단위다.  
802.1Q 태깅은 논리망 식별을 담당하고, Inter-VLAN Routing은 분리된 브로드캐스트 도메인 간 제어된 통신을 제공해 보안성과 운영 유연성을 함께 확보한다.
