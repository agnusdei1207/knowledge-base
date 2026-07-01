---
title: "서브네팅·CIDR (Subnetting CIDR)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 6
---

# 📖 【암기용】 개념 완전 이해

> 목적: 서브네팅과 CIDR을 주소 낭비 감소와 라우팅 집계 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, prefix 계산의 의미를 설명한다.

## 한눈에
- **개요**: 서브네팅은 큰 네트워크를 작은 네트워크로 나누고, CIDR은 prefix 길이로 주소 범위를 표현하는 방식이다.
- **왜 필요한가**: 조직·서비스·보안 구역별로 네트워크를 분리하고 라우팅 테이블 규모를 줄이기 위함이다.
- **핵심 직관**: 큰 우편 구역을 동·층·호수 단위로 나누고, 공통 prefix로 여러 구역을 한 줄로 묶는 방식이다.

## 깊이 이해
- **배경·문제의식**: classful 주소 체계는 A/B/C 클래스 단위 배정으로 주소 낭비와 라우팅 테이블 증가를 초래했다. CIDR은 가변 길이 prefix로 필요한 크기만 할당하고 경로를 집계한다.
- **작동 원리**: prefix length가 길수록 네트워크가 작아지고 호스트 수가 줄어든다. 라우터는 longest prefix match로 가장 구체적인 경로를 선택한다.
- **비유**: `/16`은 큰 도시, `/24`는 동네, `/28`은 작은 사무실처럼 범위가 좁아지는 구조이다.
- **구체 예시**: `192.168.1.0/24`를 `/26`으로 나누면 64개 주소 단위 4개 서브넷이 생기고, 각 서브넷은 사용 가능 호스트 62개를 가진다.
- **흔한 오해·주의점**: CIDR은 단순 표기법이 아니라 주소 할당, 라우팅 집계, ACL 범위 설정을 동시에 좌우한다.

## 연결 개념
- IP 주소 체계: prefix와 host part의 기본 구조
- VLSM: 서로 다른 크기의 서브넷 할당
- 라우팅 집계: 여러 prefix를 상위 prefix로 요약

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 준수한다.
> 핵심: 서브네팅·CIDR은 prefix 계산, 주소 수, longest prefix match, 라우팅 집계를 수치로 보여야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 서브네팅은 IP 네트워크를 더 작은 prefix로 분할하는 기법이고, CIDR은 class 경계를 버리고 prefix length로 주소 범위를 표현하는 방식이다.
> 2. **가치**: 주소 낭비를 줄이고, 보안 구역을 분리하며, 라우팅 집계로 라우팅 테이블 규모를 줄인다.
> 3. **판단 포인트**: 필요한 호스트 수, 성장 여유, VLAN·보안 구역, route summarization 가능성을 함께 계산해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| IP 주소 설계 역량 확인 | prefix length, subnet mask, host count | `/24` 같은 표기만 쓰고 주소 수 누락 |
| 라우팅 관점 확인 | CIDR, longest prefix match, route aggregation | classful A/B/C 설명에 머무름 |
| 운영·보안 분리 판단 확인 | VLAN, ACL, broadcast domain 분리 | 서브넷과 VLAN을 동일 개념으로 단정 |

> 요약: 서브네팅 답안은 주소 계산과 라우팅·보안 설계 기준을 동시에 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

서브네팅·CIDR은 IP 주소를 prefix length 기준으로 분할·집계하는 주소 설계 기법이다. classful 주소 체계는 주소 낭비와 라우팅 테이블 증가 문제가 있었다. CIDR 기반 설계는 필요한 크기만 할당하고 보안 구역과 라우팅 범위를 명확히 분리한다.

---

## Ⅱ. 구조 및 구성요소

```text
IP Address
-> Network Prefix /n
-> Subnet Bits
-> Host Bits
-> Subnet Mask / CIDR Notation
-> Routing Aggregation
```

| 구성요소 | 역할 | 대표 예시 |
|:---|:---|:---|
| prefix length | 네트워크 비트 수 지정 | IPv4 /24, IPv6 /64 |
| subnet mask | IPv4 네트워크 범위 표시 | 255.255.255.0 |
| host bits | 서브넷 내 호스트 수 결정 | /26은 6bit, 64개 주소 |
| route aggregation | 여러 서브넷 경로 요약 | 10.1.0.0/16으로 /24 집계 |

> 요약: 서브네팅은 prefix, mask, host bits, 집계 가능성을 함께 계산해 주소 범위와 라우팅 범위를 정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요구 호스트 수 산정
-> 필요한 host bits 계산
-> prefix length 결정
-> subnet boundary 산출
-> gateway / DHCP / ACL / route 반영
-> longest prefix match 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 부서·서비스별 호스트 수와 증가율 산정 | 현재 수+30% 여유 |
| 2 | host bits 계산 | 사용 가능 호스트 2^h-2 |
| 3 | prefix와 subnet boundary 결정 | /24, /26, /28 |
| 4 | gateway, DHCP scope, ACL 적용 | gateway 1개, DHCP pool 범위 |
| 5 | route summarization과 충돌 확인 | 중복 prefix 0건 |

> 요약: CIDR 설계는 호스트 수에서 prefix를 역산하고 라우팅·DHCP·ACL까지 일관되게 반영하는 절차이다.

---

## Ⅳ. 특징

| 구분 | Classful | CIDR/VLSM | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 주소 단위 | A/B/C 고정 | /n 가변 prefix | RFC 4632 |
| 주소 활용 | 큰 블록 낭비 | 필요한 크기별 할당 | /26 사용 가능 62개 |
| 라우팅 | 경로 증가 | route summarization | longest prefix match |
| 운영 | 보안 구역 단순 | VLAN·ACL 단위 분리 | broadcast domain 축소 |

> 요약: CIDR은 가변 prefix와 경로 집계를 통해 주소 설계와 라우팅 운영을 동시에 개선한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 큰 단일 서브넷 | 세분 서브넷/CIDR | 선택 기준 |
|:---|:---|:---|:---|
| 브로드캐스트 | ARP·broadcast 범위 큼 | 구역별 범위 제한 | 단말 500대 이상이면 분리 검토 |
| 보안 | ACL 경계 불명확 | 부서·서비스별 정책 적용 | Zero Trust segment 기준 |
| 라우팅 | 경로 단순 | 경로 수 증가 가능 | 상위 prefix 집계 가능성 확인 |

> 요약: 세분 서브넷은 보안·장애 범위를 줄이지만, 경로 수와 운영 복잡도를 집계 설계로 통제해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 주소 고갈 | host bits 과소 산정 | 30% 성장 여유, IPAM 관리 | pool utilization 80% 경보 |
| prefix 중복 | 수작업 주소 배정 | IPAM 승인 절차, 중복 검사 | duplicate subnet 0건 |
| 라우팅 누락 | 집계 경로 오류 | route table audit, blackhole test | unreachable prefix count |

> 요약: 주소 설계 리스크는 고갈, 중복, 라우팅 누락이며 IPAM과 route audit로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 주소 사용률 | subnet utilization 70~80% 유지 | IPAM, DHCP lease |
| 중복 여부 | duplicate IP/subnet 0건 | ARP scan, IPAM validation |
| 라우팅 | route summarization 적용률 90% 이상 | routing table analysis |

> 요약: 서브네팅 운영 품질은 사용률, 중복, 집계 적용률을 정기 점검해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 설계 기준: 사용자망 /24, 서버 소규모망 /26, point-to-point /31 또는 /30, IPv6 LAN /64 기준 수립
2. 운영 통제: IPAM 기반 prefix 승인, DHCP scope 자동 검증, subnet utilization 80% 초과 시 증설 검토
3. 라우팅 최적화: 지점별 /24를 상위 /16 또는 /20으로 집계하고 longest prefix match 충돌을 route audit로 점검

**결론 (2줄):**
- 기술사 판단: 주소 수가 고정된 소규모망은 단순 /24, 다부서·다서비스 환경은 VLSM과 CIDR 집계를 선택함
- 향후 방향: IPv6 /64 표준 운영과 클라우드 VPC CIDR 충돌 방지를 위해 중앙 IPAM 기반 설계가 확대됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "서브네팅과 CIDR을 설명하시오" | prefix 계산과 longest prefix match | classful 대비 CIDR 특징 |
| 요구사항 명시형 | "주소 설계 방안을 제시하시오", "계산하시오" | host bits, mask, boundary 산출 | 주소 고갈·중복·집계 기준 |

> 요약: 설명형은 개념과 구조를, 설계형은 prefix 계산과 IPAM·라우팅 적용 기준을 중심으로 전환한다.
