---
title: "IPv4-IPv6 전환 (IPv4-IPv6 Transition)"
date: "2026-06-30"
weight: 41
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> IPv4와 IPv6가 비호환인 상황에서 양 프로토콜의 점진적 공존과 상호 연동을 위한 전환 기술의 총칭으로, 듀얼스택·터널링·주소변환의 세 가지 접근으로 구분된다.

## Ⅱ. 구성요소 / 원리
- 듀얼스택(Dual Stack): 단말·라우터가 IPv4/IPv6 스택을 동시 구동, 목적지에 맞게 선택
- 터널링(Tunneling): IPv6 패킷을 IPv4로 캡슐화 전달(6to4, ISATAP, Teredo, GRE)
- 변환(Translation): NAT64+DNS64로 IPv6 전용 호스트가 IPv4 자원 접근
- ISATAP: 사이트 내 IPv4망 위에서 IPv6 자동 터널
- DNS64: IPv4 A레코드를 IPv6 AAAA로 합성하여 NAT64 유도

## Ⅲ. 흐름도 / 구조
```text
[듀얼스택]  IPv4 ↔ 단말(v4+v6) ↔ IPv6  (양 스택 동시)
[터널링]   IPv6패킷 ─캡슐화→ [IPv4망] ─역캡슐화→ IPv6
           6to4 / ISATAP / Teredo
[변환]     IPv6호스트 → NAT64 ─→ IPv4서버
           DNS64가 AAAA 합성 제공
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | IPv4 자산을 유지하며 IPv6로의 단계적·무중단 전환 실현 |
| 장점 | 점진 도입 가능, 환경별(듀얼/터널/변환) 선택적 적용 |
| 한계 | 듀얼스택은 운영 이중화 비용, 터널은 오버헤드·MTU 문제, 변환은 E2E 훼손 |

## Ⅴ. 기술사적 적용
- 코어 백본은 듀얼스택, 고립 IPv6 섬은 터널링, 신규 IPv6-only망은 NAT64로 단계 적용
- 전환 우선순위: 듀얼스택 → 터널링 → 변환 순으로 권장(IETF 일반 가이드)
- 모바일·IoT의 IPv6-only 환경 확산으로 464XLAT 등 변환 기술 병행 적용
