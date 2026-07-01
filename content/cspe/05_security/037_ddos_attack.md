---
title: "DDoS 공격·대응 SYN Flood·반사 증폭 (DDoS Attack)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 37
---

# 📖 【암기용】 개념 완전 이해

> 목적: DDoS 공격과 대응을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 다수의 공격원이 대역폭, 세션, 애플리케이션 자원을 소진시키는 서비스 거부 공격
- **왜 필요한가**: 서비스가 침해되지 않아도 네트워크 회선, 방화벽 세션, 웹 스레드가 고갈되면 사용자는 접속하지 못한다.
- **핵심 직관**: 매장 입구, 계산대, 상담 창구를 동시에 막아 실제 고객이 들어오지 못하게 만드는 방식이다.

## 깊이 이해
- **배경·문제의식**: 인터넷 서비스는 공개 IP와 80/443 포트를 열어야 하므로 완전 차단이 어렵다. 공격자는 봇넷, 오픈 리졸버, NTP/SSDP/Memcached 반사 증폭을 이용해 원천보다 큰 트래픽을 만든다.
- **작동 원리**: L3/L4 공격은 회선·세션 자원을 소진하고, L7 공격은 정상 HTTP 요청처럼 보여 웹·DB 처리 자원을 소모한다. 방어는 ISP, scrubbing center, CDN/WAF, 서버 rate limit 계층에서 나누어 수행한다.
- **비유**: 전화 상담센터에 자동 발신기가 초당 수천 통을 걸면 상담원은 통화 내용을 확인하기 전에 회선과 대기열을 모두 잃는다.
- **구체 예시**: SYN Flood가 초당 200k SYN을 보내면 서버의 half-open backlog가 고갈된다. SYN cookie, firewall SYN proxy, upstream scrubbing으로 정상 3-way handshake만 내부로 전달한다.
- **흔한 오해·주의점**: 방화벽만 증설하면 해결된다는 답은 부족하다. 회선 용량보다 큰 공격은 내부 장비에 도달하기 전 ISP·BGP·scrubbing에서 흡수해야 한다.

## 연결 개념
- SYN Flood - TCP 3-way handshake의 half-open 상태를 악용
- 반사 증폭 - 출발지 IP를 피해자로 위조해 증폭 서버가 응답을 보내게 함
- Scrubbing Center - 대규모 트래픽을 원격 정화 후 정상 트래픽만 전달

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: DDoS 답안은 L3/L4/L7 공격 분류, 차단 위치, 복구 목표, 재발 방지까지 이어져야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DDoS는 다수 공격원이 네트워크 대역폭, TCP 상태, 애플리케이션 처리량을 소진시키는 가용성 침해임.
> 2. **가치**: 대응은 라우터, ISP, scrubbing, CDN/WAF, 서버 rate limit을 계층화해야 공격 규모별로 흡수 가능함.
> 3. **판단 포인트**: L3/L4/L7 구분, SYN cookie, BGP blackhole, RTBH, scrubbing 우회, RTO/RPO가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 공격 유형 분류 확인 | Volumetric, Protocol, Application 공격 차이 | SYN Flood와 HTTP Flood를 같은 계층으로 처리 |
| 차단 위치 판단 확인 | ISP scrubbing, ACL, WAF, rate limit, autoscale | 내부 방화벽 증설만 제시 |
| 대응 절차 확인 | 탐지, 우회, 차단, 복구, 사후 튜닝 | 복구 목표·로그 지표·재발 방지 누락 |

> 요약: DDoS는 공격 계층별 병목과 차단 위치를 맞추고 서비스 RTO를 지표로 관리해야 함.

---

## Ⅰ. 개요 및 필요성

DDoS는 분산 서비스 거부 공격이다. 봇넷과 반사 증폭으로 정상 서비스의 회선, 세션, CPU, DB 연결을 소진해 가용성을 침해함. 전자상거래·금융·공공 서비스는 매출 손실과 SLA 위반이 발생하므로 사전 우회·정화 체계가 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Botnet/Reflector -> Internet -> ISP/Transit -> Scrubbing/CDN
  / L3: UDP flood, ICMP flood
  / L4: SYN flood, ACK flood
  / L7: HTTP GET/POST flood, Slowloris
정상 트래픽 -> WAF/Rate Limit -> Origin Server -> Service
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 공격원 | 봇넷·반사 서버로 대량 트래픽 생성 | source IP 위조, C2 제어 |
| 경계 라우터/ISP | 대역폭 기반 차단·우회 | ACL, FlowSpec, RTBH |
| Scrubbing/CDN | 악성 트래픽 정화 후 정상 요청 전달 | GRE tunnel, Anycast |
| WAF/서버 | L7 요청 검증·rate limit | challenge, bot score, queue limit |

> 요약: DDoS 방어는 공격원 근처가 아니라 병목보다 앞단인 ISP·scrubbing·CDN에서 먼저 흡수해야 함.

---

## Ⅲ. 동작원리 및 흐름도

```text
트래픽 기준선 수집 -> 임계치 초과 탐지 -> 공격 계층 분류
-> ISP/scrubbing 우회 -> ACL/WAF/rate limit 차단 -> 서비스 복구
-> 로그 분석 -> 룰 튜닝·모의훈련
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | NetFlow, pps, bps, HTTP rps 기준선 수집 | 평시 대비 3배 이상 이상징후 |
| 2 | SYN, UDP, HTTP 패턴으로 L3/L4/L7 분류 | SYN/ACK 비율, 5xx, p95 지연 |
| 3 | ISP scrubbing, BGP blackhole, FlowSpec 적용 | 정상 사용자 영향 범위 확인 |
| 4 | WAF rule, rate limit, SYN cookie 적용 | 차단 로그, 오탐률 1% 이하 |
| 5 | 서비스 복구 후 원인·IoC·룰 보완 | RTO 30분, 재발 룰 반영 |

> 요약: DDoS 대응은 탐지 지표로 계층을 구분하고 upstream 정화와 L7 필터링을 순서대로 적용함.

---

## Ⅳ. 특징

| 구분 | 단일 장비 대응 | 계층형 DDoS 대응 | 수치·로그 포인트 |
|:---|:---|:---|:---|
| L3 대역폭 | 내부 방화벽 포화 | ISP scrubbing, Anycast CDN | bps, pps, NetFlow |
| L4 프로토콜 | 서버 backlog 소진 | SYN cookie, SYN proxy | SYN/ACK ratio, half-open |
| L7 애플리케이션 | 정상 요청과 구분 난도 | WAF, bot score, rate limit | HTTP rps, 4xx/5xx, URI별 rps |
| 복구 | 수동 차단 | runbook, RTBH, DNS/CDN 우회 | RTO 30분 이내 |

> 요약: DDoS는 회선·세션·애플리케이션 병목이 달라서 L3/L4/L7별 지표와 통제를 분리해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | On-prem 방화벽 중심 | ISP scrubbing + CDN/WAF | 공격 트래픽이 회선 용량의 70% 초과 시 |
| 비용/성능 | 상시 scrubbing | On-demand scrubbing | 활성화 시간 5분, p95 지연 100ms 기준 |
| 운영/위험 | BGP blackhole | FlowSpec/clean pipe | 전체 서비스 차단 허용 여부 |

> 요약: 회선 초과 공격은 upstream 정화, L7 공격은 CDN/WAF와 애플리케이션 rate limit을 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 정상 사용자 차단 | 과도한 rate limit | 사용자·ASN·URI별 예외 정책 | 오탐률 1% 이하 |
| Origin 우회 | 공격자가 원본 IP 직접 공격 | origin ACL, CDN only ingress | 비인가 source drop |
| 반사 증폭 지속 | 오픈 리졸버·NTP 악용 | BCP 38, ISP 협조, abuse report | reflector IP 재사용률 |
| 복구 지연 | 대응 runbook 부재 | 모의훈련, 연락망, 자동 우회 | RTO 30분 준수율 |

> 요약: DDoS 리스크는 오탐, 원본 우회, 반사 증폭, 복구 지연이며 사전 정책과 훈련으로 줄임.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지 | 평시 대비 3배 이상 bps/pps/rps 알림 | NetFlow, CDN, WAF 로그 |
| 차단 | 악성 트래픽 drop 95% 이상, 오탐 1% 이하 | scrubbing report, WAF sample |
| 복구 | RTO 30분, 장애 공지 10분 이내 | incident timeline, SLA 보고 |

> 요약: 성공 여부는 탐지 시간, 정화율, 오탐률, RTO를 동시에 보아야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 사전 준비: CDN/WAF, ISP scrubbing 계약, BGP FlowSpec/RTBH 절차, origin ACL을 구축하고 분기 1회 모의훈련 수행함.
2. 공격 중 대응: NetFlow와 WAF 로그로 L3/L4/L7을 분류하고, volumetric은 scrubbing, SYN Flood는 SYN cookie/proxy, L7은 rate limit·challenge를 적용함.
3. 사후 개선: 공격 ASN, URI, user-agent, reflector IP를 IoC로 등록하고 threshold, WAF 룰, runbook RTO 30분 기준을 갱신함.

**결론 (2줄):**
- 기술사 판단: 회선 용량 초과 공격은 내부 장비가 아니라 upstream scrubbing으로, 정상 요청형 공격은 WAF와 애플리케이션 큐 제한으로 통제해야 함.
- 향후 방향: Anycast CDN, ML bot score, 자동 FlowSpec 연동으로 탐지에서 차단까지 시간을 5분 이하로 줄이는 운영이 필요함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DDoS 공격을 설명하시오" | L3/L4/L7 공격 흐름과 탐지 지표 | SYN Flood, 반사 증폭, HTTP Flood 차이 |
| 요구사항 명시형 | "대응 방안을 제시하시오" | scrubbing, BGP blackhole, rate limit 순서 | RTO, 오탐률, 원본 보호, 재발 방지 |

> 요약: 설명형은 공격 계층을, 방안형은 차단 위치와 복구 목표를 중심으로 작성함.
