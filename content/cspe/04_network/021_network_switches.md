---
title: "스위칭 계층 — L2·L3·L4·L7 스위치 (Network Switches)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 21
---

# 📖 【암기용】 개념 완전 이해

> 목적: L2·L3·L4·L7 스위치를 처음 봐도 각 계층이 어떤 정보를 보고 전달 결정을 내리는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: OSI 계층별 헤더 정보를 기준으로 프레임·패킷·세션·애플리케이션 트래픽을 전달하는 장비군
- **왜 필요한가**: 네트워크는 단순 연결만으로 끝나지 않고 VLAN 분리, 라우팅, 포트 기반 분산, HTTP 정책 처리가 필요하다. 계층별 스위치는 처리 위치와 정책 범위를 나눈다.
- **핵심 직관**: 택배 분류가 집 주소, 도시, 접수창구, 물품 내용 순서로 깊게 보는 것처럼 스위칭 계층도 MAC, IP, TCP/UDP, HTTP를 단계적으로 본다.

## 깊이 이해
- **배경·문제의식**: L2 스위치는 MAC table로 LAN 내부를 연결하지만 서브넷 경계를 넘지 못한다. L3 스위치는 하드웨어 라우팅으로 VLAN 간 통신을 처리하고, L4·L7 스위치는 서버팜 앞에서 서비스 단위 정책을 수행한다.
- **작동 원리**: L2는 source MAC 학습 후 destination MAC으로 포트를 선택한다. L3는 목적지 IP와 라우팅 테이블로 next-hop을 고른다. L4는 IP, TCP/UDP port, 세션 테이블을 보고 서버를 선택한다. L7은 HTTP Host, URI, header, cookie, TLS SNI 같은 애플리케이션 속성을 본다.
- **비유**: L2는 같은 건물의 호실 안내, L3는 다른 도시로 가는 고속도로 안내, L4는 창구 번호 배정, L7은 민원 내용별 담당자 배정에 해당한다.
- **구체 예시**: 웹 서비스에서 `10.1.10.0/24` 서버 VLAN은 L2로 묶고, 사용자 VLAN과 서버 VLAN은 L3 SVI로 라우팅하며, `TCP 443` 접속은 L4 VIP가 분산하고 `/api` 경로는 L7 정책이 별도 풀로 보낸다.
- **흔한 오해·주의점**: L7 스위치가 모든 상황의 상위 대체재는 아니다. TLS 복호화, HTTP parsing, WAF 연계가 필요하면 L7, p95 지연 1ms 이하의 단순 전달이 필요하면 L4 또는 L3 경로가 적합하다.

## 연결 개념
- VLAN·Trunk — L2 스위칭의 논리 분리 단위
- 라우팅·SVI — L3 스위치의 VLAN 간 경로 결정
- L4·L7 로드 밸런서 — 서비스 가용성과 정책 기반 분산

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 스위칭 계층 답안은 장비 이름 나열이 아니라 헤더 관찰 범위, 전달 기준, 정책 가능 범위, 지연·처리량 트레이드오프를 계층별로 구분한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: L2·L3·L4·L7 스위치는 각각 MAC, IP, TCP/UDP port, 애플리케이션 정보를 기준으로 트래픽 전달 결정을 수행한다.
> 2. **가치**: 계층별 스위칭은 VLAN 분리, 라우팅, 세션 분산, URI 기반 정책을 장비 위치별로 배치하게 한다.
> 3. **판단 포인트**: 처리 계층이 높아질수록 정책 세밀도는 증가하지만 TLS 복호화, 세션 유지, CPU 사용률, p95 지연을 함께 검토해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 계층별 전달 기준 이해 확인 | MAC, IP, port, HTTP header/URI/SNI | 스위치를 모두 L2 장비로만 서술 |
| 장비 선택 판단 확인 | L3 SVI, L4 VIP, L7 reverse proxy 구분 | L7이 모든 L4 기능을 대체한다고 단정 |
| 운영 지표 연결 확인 | MAC table, route table, session table, p95 latency | 처리량·세션·TLS 부하 지표 누락 |

> 요약: 이 문제는 계층별 헤더 해석 범위와 정책 가능 범위를 기준으로 스위치 선택 근거를 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 계층별 참조 헤더 정보로 전달 결정 방식을 구분한 스위칭 체계
- 배경: L2는 MAC 기반 LAN 전달, L3는 IP 기반 라우팅, L4는 포트·세션 기반 서버 분산, L7은 HTTP 등 애플리케이션 속성 기반 정책 처리를 담당
- 필요성: 데이터센터·기업망은 네트워크 분리, 서버 이중화, 서비스 정책 적용을 위해 계층별 스위치 장비를 조합함

---

## Ⅱ. 구조 및 구성요소

```text
Client Frame/Packet -> L2 Switch: MAC/VLAN
  -> L3 Switch: IP Prefix/SVI
  -> L4 Switch: VIP/TCP Port/Session
  -> L7 Switch: Host/URI/Header/Cookie
  -> Server Pool
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| L2 Switch | MAC table 기반 프레임 전달 | VLAN, STP/RSTP, trunk 처리 |
| L3 Switch | IP prefix 기반 라우팅 | SVI, ACL, ECMP 지원 |
| L4 Switch | IP와 TCP/UDP port 기반 서버 선택 | VIP, SNAT, persistence |
| L7 Switch | HTTP 속성 기반 정책 처리 | URI routing, header rewrite, TLS offload |

> 요약: 스위칭 계층은 L2에서 L7로 갈수록 참조 헤더가 깊어지고 정책 단위가 MAC에서 애플리케이션 속성으로 이동한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Traffic Ingress -> Header Parse -> Table Lookup
  -> Policy Match -> Forward/Route/Balance
  -> Telemetry Collect -> Policy Tune
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | L2에서 source MAC 학습, destination MAC 조회 | MAC table aging, unknown unicast count |
| 2 | L3에서 목적지 IP prefix와 ACL 확인 | route hit, ACL deny log |
| 3 | L4에서 VIP, port, session table 매칭 | concurrent session, SYN rate |
| 4 | L7에서 Host, URI, header, cookie 정책 적용 | p95 latency, HTTP 5xx rate |

> 요약: 스위칭은 헤더 파싱, 테이블 조회, 정책 매칭, 전달 지표 수집 순서로 동작하며 계층별 검증 항목이 다르다.

---

## Ⅳ. 특징

| 구분 | L2·L3 중심 | L4·L7 중심 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 처리 기준 | MAC, VLAN, IP prefix | TCP/UDP port, HTTP header | OSI 2/3/4/7 계층 |
| 정책 단위 | 세그먼트, 서브넷, ACL | VIP, pool, URI, cookie | TCP 80/443, TLS SNI |
| 상태 관리 | MAC/route table 위주 | session table, persistence | session timeout, SYN backlog |
| 지연 요인 | ASIC lookup, ACL hit | TLS offload, HTTP parsing | p95 latency, CPS, RPS |

> 요약: L2·L3는 네트워크 도달성, L4·L7은 서비스 분산과 애플리케이션 정책이 주 판단 기준이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | L2/L3 스위치 | L4/L7 스위치 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 캠퍼스·데이터센터 fabric 내부 | 서버팜·서비스 경계 | VLAN·라우팅이면 L3, 서비스 분산이면 L4/L7 |
| 비용/성능 | ASIC 기반 line-rate 처리 | 세션·TLS·HTTP 처리 비용 발생 | p95 지연 목표와 TLS TPS 기준 |
| 운영/위험 | 루프, VLAN 확산, ACL 누락 | 세션 고갈, 인증서 만료, 정책 충돌 | 장애 도메인과 변경 승인 기준 |

> 요약: 계층 선택은 처리 위치가 아니라 요구 정책이 MAC/IP인지 세션/HTTP인지로 결정한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| L2 루프 | STP 오설정, trunk 확산 | BPDU guard, storm-control | broadcast pps, MAC flapping |
| 세션 고갈 | L4 session table 한계 초과 | SYN cookie, connection limit | active session, SYN drop |
| L7 정책 오류 | URI rule 순서, TLS 인증서 만료 | staging rule test, cert rotation | HTTP 4xx/5xx, cert expiry day |

> 요약: 운영 리스크는 계층별로 루프, 세션, 애플리케이션 정책 오류로 갈리며 지표와 보호 기능을 분리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전달 처리량 | uplink 사용률 70% 이하, drop 0건 | interface counter, SNMP |
| 서비스 지연 | L4 p95 1ms 내외, L7 p95 목표치 준수 | APM, synthetic test |
| 테이블 상태 | MAC/route/session table 80% 이하 | 장비 telemetry, syslog |

> 요약: 스위칭 품질은 처리량, 지연, 테이블 여유율을 계층별로 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 캠퍼스망은 access L2, distribution/core L3 SVI 구조로 설계하고 VLAN trunk 허용 목록을 최소화함
2. 서버팜은 L4 VIP 기준으로 TCP 80/443을 분산하고 session persistence와 health check 주기를 명시함
3. HTTP 경로 분기, TLS offload, header 기반 정책은 L7에 배치하고 p95 latency, RPS, 5xx rate를 배포 기준으로 삼음

**결론 (2줄):**
- 기술사 판단: VLAN·IP 도달성 문제는 L2/L3, 서비스 분산·HTTP 정책 문제는 L4/L7을 선택함
- 향후 방향: EVPN/VXLAN, service mesh, eBPF telemetry와 연계해 계층별 정책과 관측 지표를 일관되게 관리해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "스위칭 계층을 설명하시오" | MAC, IP, port, HTTP 처리 흐름 | L2·L3·L4·L7 차이표 |
| 요구사항 명시형 | "스위치 선택 방안을 제시하시오" | 요구 트래픽별 장비 배치 | p95 latency, session, TLS 기준 |

> 요약: 설명형은 계층별 원리, 방안형은 정책 요구와 검증 지표 중심으로 목차를 전환한다.
