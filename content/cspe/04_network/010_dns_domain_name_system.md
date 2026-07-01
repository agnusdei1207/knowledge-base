---
title: "DNS 구조·동작 (DNS Domain Name System)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 10
---

# 📖 【암기용】 개념 완전 이해

> 목적: DNS를 이름을 IP 주소로 바꾸는 전역 분산 데이터베이스로 이해하게 만든다. 시험 답안 양식이 아니라, 질의 흐름과 캐시의 의미를 설명한다.

## 한눈에
- **개요**: DNS는 도메인 이름을 IP 주소와 서비스 정보로 변환하는 계층형 분산 시스템이다.
- **왜 필요한가**: 사용자는 IP 주소보다 이름을 사용하고, 서비스 운영자는 IP 변경·로드 분산·메일 라우팅을 이름 기반으로 관리해야 한다.
- **핵심 직관**: 전 세계 전화번호부를 root, TLD, authoritative 서버가 나누어 관리하고 resolver가 대신 찾아주는 구조이다.

## 깊이 이해
- **배경·문제의식**: hosts 파일 방식은 인터넷 규모에서 관리 한계가 있었다. DNS는 도메인 계층과 위임, 캐시를 이용해 전역 이름 해석을 분산 처리한다.
- **작동 원리**: 클라이언트는 recursive resolver에 질의하고, resolver는 root, TLD, authoritative DNS를 순차 조회한다. 결과는 TTL 동안 캐시에 저장되어 반복 질의 지연과 부하를 줄인다.
- **비유**: 회사 대표 번호로 전화하면 부서 안내, 팀 안내, 담당자 번호를 차례로 받아 최종 연결되는 구조와 같다.
- **구체 예시**: `www.example.com`의 A 레코드는 IPv4 주소를, AAAA 레코드는 IPv6 주소를, MX 레코드는 메일 서버를 제공한다.
- **흔한 오해·주의점**: DNS는 단순 IP 변환만 수행하지 않는다. CNAME, MX, TXT, SRV, NS, SOA 등 서비스 운영과 검증 레코드를 포함한다.

## 연결 개념
- DHCP: 단말에 DNS resolver 주소를 배포
- CDN/GSLB: DNS 응답을 이용한 위치 기반 서비스 분산
- DNSSEC: DNS 응답 위변조 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 준수한다.
> 핵심: DNS는 계층 구조, recursive/iterative 질의, 주요 레코드, TTL 캐시, 보안 리스크를 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DNS는 도메인 이름을 IP 주소와 서비스 레코드로 해석하는 계층형·분산형 이름 시스템이다.
> 2. **가치**: 사용자는 사람이 읽는 이름을 사용하고, 운영자는 TTL, 레코드, 위임으로 서비스 이전·분산·검증을 관리한다.
> 3. **판단 포인트**: root-TLD-authoritative 구조, recursive resolver, TTL 캐시, DNSSEC·DoH·DoT 보안 이슈를 포함해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DNS 계층 구조 이해 확인 | root, TLD, authoritative, resolver | DNS 서버를 단일 서버로 설명 |
| 질의·캐시 동작 확인 | recursive query, iterative query, TTL | TTL과 propagation 지연 누락 |
| 보안·운영 리스크 인식 확인 | cache poisoning, DNSSEC, DoH/DoT | A 레코드만 설명하고 레코드 유형 누락 |

> 요약: DNS 답안은 이름 해석 흐름과 캐시·보안·운영 지표를 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 정의: 도메인 이름을 IP 주소·서비스 레코드로 변환하는 분산 이름 시스템
- 배경: IP 주소는 사람이 기억하기 어렵고 서비스 이전 시 변경될 수 있음
- 필요성: 계층 위임과 TTL 캐시로 전역 규모 이름 해석과 운영 변경(서비스 이전·장애 조치)을 지원

---

## Ⅱ. 구조 및 구성요소

```text
Client Stub Resolver
-> Recursive Resolver
-> Root DNS
-> TLD DNS
-> Authoritative DNS
-> DNS Cache with TTL
-> Application Connection
```

| 구성요소 | 역할 | 대표 예시 |
|:---|:---|:---|
| Stub Resolver | 단말의 DNS 질의 시작 | OS resolver |
| Recursive Resolver | 클라이언트 대신 전체 조회 수행 | ISP DNS, public DNS |
| Root DNS | TLD 위치 안내 | root zone |
| TLD DNS | .com, .kr 등 zone 위임 | NS referral |
| Authoritative DNS | 실제 레코드 보유 | A, AAAA, MX, TXT |
| Cache | TTL 동안 응답 저장 | TTL 60~86400초 |

> 요약: DNS는 단말 resolver부터 authoritative 서버까지 계층 위임으로 동작하고 TTL 캐시로 반복 질의를 줄인다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Application이 www.example.com 요청
-> Stub resolver가 recursive resolver 질의
-> resolver가 root -> TLD -> authoritative 순서 조회
-> A/AAAA record와 TTL 수신
-> cache 저장
-> client가 IP로 TCP/UDP 연결
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 클라이언트가 resolver로 질의 | UDP/TCP 53, DoH 443 |
| 2 | root가 TLD NS를 응답 | referral, NS record |
| 3 | TLD가 authoritative NS를 응답 | delegation, glue record |
| 4 | authoritative가 record 반환 | A, AAAA, CNAME, MX, TXT |
| 5 | resolver가 TTL 동안 cache 저장 | cache hit ratio, TTL 만료 |

> 요약: DNS 질의는 recursive resolver가 계층 위임을 따라 최종 레코드를 얻고 TTL 동안 캐시하는 흐름이다.

---

## Ⅳ. 특징

| 구분 | hosts 파일 | DNS | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 구조 | 단일 파일 | 계층형 분산 DB | RFC 1034, RFC 1035 |
| 변경 | 단말별 수정 | zone file과 TTL 기반 반영 | TTL 60~86400초 |
| 레코드 | 이름-IP 중심 | A, AAAA, CNAME, MX, TXT, SRV | UDP/TCP 53 |
| 보안 | 파일 변조 | cache poisoning, DNSSEC 필요 | DNSSEC RRSIG, DS |

> 요약: DNS는 hosts 파일 한계를 계층 위임과 TTL 캐시로 해결하지만 캐시 위변조와 설정 오류 통제가 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Recursive Resolver | Authoritative DNS | 선택 기준 |
|:---|:---|:---|:---|
| 역할 | 클라이언트 대신 조회·캐시 | zone의 원본 레코드 제공 | 사용자 질의는 resolver, 도메인 운영은 authoritative |
| 운영 지표 | cache hit, latency, SERVFAIL | zone serial, query rate, availability | 장애 원인에 따라 분리 점검 |
| 보안 | DoH/DoT, filtering | DNSSEC signing, ACL | 내부 사용자 보호와 도메인 무결성 분리 |

> 요약: DNS 장애 분석은 resolver 문제와 authoritative zone 문제를 분리해야 조치 시간이 줄어든다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| cache poisoning | 위조 응답 주입 | DNSSEC validation, source port randomization | bogus validation count |
| propagation 지연 | TTL 과다 | 변경 전 TTL 60~300초 조정 | old record hit ratio |
| 단일 장애점 | authoritative 이중화 부족 | multi-NS, multi-region DNS | DNS availability 99.99% |

> 요약: DNS 리스크는 캐시 위변조, TTL 지연, authoritative 가용성이며 보안 검증과 다중화로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 응답 지연 | DNS query p95 50ms 이하 | dig, synthetic monitoring |
| 오류율 | SERVFAIL/NXDOMAIN 비정상 증가 0건 | resolver log |
| 무결성 | DNSSEC validation 성공률 99.9% 이상 | DNSSEC validator, SIEM |

> 요약: DNS 운영 품질은 p95 응답, 오류율, DNSSEC 검증률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 변경 관리: 서비스 이전 24시간 전 TTL을 60~300초로 낮추고, 변경 후 A/AAAA/CNAME 응답을 여러 resolver에서 검증
2. 가용성: authoritative DNS를 2개 이상 NS와 multi-region으로 구성하고 zone serial, SOA, glue record를 배포 전 점검
3. 보안 통제: DNSSEC 서명, resolver filtering, DoH/DoT 정책, query log 기반 DGA·tunneling 탐지를 적용

**결론 (2줄):**
- 기술사 판단: 서비스 가용성 문제는 DNS TTL·resolver·authoritative를 분리해 보고, 도메인 무결성 요구가 있으면 DNSSEC를 적용함
- 향후 방향: DoH/DoT 확산으로 네트워크 장비 기반 DNS 가시성이 낮아져 endpoint·resolver 로그 중심 관측이 필요함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DNS 구조와 동작을 설명하시오" | root -> TLD -> authoritative 질의 흐름 | 주요 레코드와 TTL 캐시 |
| 요구사항 명시형 | "DNS 장애 대응 방안을 제시하시오", "보안 대책을 설명하시오" | resolver와 authoritative 분리 절차 | DNSSEC, TTL, multi-NS, 지표 |

> 요약: 설명형은 질의 흐름을, 장애·보안형은 resolver/authoritative 분리와 TTL·DNSSEC 대응을 중심으로 전환한다.
