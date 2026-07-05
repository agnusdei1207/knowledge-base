---
title: "DDoS 공격 기법·대응 — SYN Flood·증폭 (DDoS Attack Mitigation)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 109
---

# 📖 【암기용】 개념 완전 이해

> 목적: DDoS 공격을 트래픽 유형과 대응 지표 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 다수 공격원이 네트워크·서버 자원을 소진시켜 정상 요청을 처리하지 못하게 하는 공격
- **왜 필요한가**: 서비스 장애 원인이 회선 포화인지, SYN backlog 소진인지, L7 요청 폭증인지에 따라 대응 장비와 지표가 달라진다.
- **핵심 직관**: 가게 입구를 사람으로 막는 공격, 주문 전화만 계속 걸어 직원 시간을 뺏는 공격, 남의 주소로 대량 택배를 보내는 공격이 모두 DDoS의 다른 형태이다.

## 깊이 이해
- **배경·문제의식**: 봇넷, 오픈 리졸버, 클라우드 자원을 이용하면 공격자는 적은 비용으로 큰 트래픽을 만든다. 방어자는 ISP, scrubbing center, CDN/WAF, 서버 커널 설정을 연계해야 한다.
- **작동 원리**: SYN Flood는 TCP 3-way handshake의 half-open 상태를 늘려 SYN backlog를 소진한다. 증폭 공격은 DNS, NTP, SSDP 등 반사 서버에 피해자 IP를 위조해 큰 응답을 피해자에게 보낸다.
- **비유**: 예약 전화를 걸고 오지 않는 사람을 대량으로 만들어 예약 장부를 꽉 채우거나, 여러 음식점에 피해자 주소로 배달을 시키는 방식과 같다.
- **구체 예시**: DNS 증폭은 작은 query가 EDNS0 큰 응답으로 커질 수 있어 공격 트래픽이 회선 대역폭을 먼저 소진한다.
- **흔한 오해·주의점**: DDoS 대응은 방화벽 한 대로 끝나지 않는다. 회선 포화 이전 단계에서 ISP diversion, BGP RTBH, scrubbing, CDN 분산을 계획해야 한다.

## 연결 개념
- SYN Cookie — SYN backlog 소진 대응
- Scrubbing Center — 대용량 공격 트래픽 정화
- BCP 38 — 출발지 IP 위조 차단

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: DDoS 답안은 공격 유형, 병목 자원, 대응 위치, 확인 지표를 분리해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DDoS는 다수 공격원이 회선 대역폭, TCP 상태 테이블, 애플리케이션 처리 자원을 소진시키는 가용성 공격이다.
> 2. **가치**: SYN Flood, UDP/DNS 증폭, HTTP Flood를 구분하면 SYN cookie, scrubbing, CDN/WAF 등 대응 위치가 정해진다.
> 3. **판단 포인트**: 방어 성공은 차단 장비 유무가 아니라 pps/bps, SYN backlog, 5xx, 정상 사용자 성공률 지표로 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 공격 기법 이해 확인 | SYN Flood, 증폭, L7 Flood 원리 | 모든 DDoS를 트래픽 폭주로만 설명 |
| 대응 체계 판단 확인 | ISP, scrubbing, CDN/WAF, 서버 커널 | 내부 방화벽만 제시 |
| 지표 기반 운영 확인 | bps, pps, SYN backlog, 5xx, SLA | 공격 원리와 대응 지표 혼동 |

> 요약: DDoS 문제는 병목 자원을 먼저 특정하고 그 위치에서 트래픽을 우회·정화·차단하는 구조로 답해야 한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **DDoS 공격 기법·대응 — SYN Flood·증폭** | DDoS 공격 기법·대응 — SYN Flood·증폭 (DDoS Attack Mitigation)의 핵심 개념 | "이 주제의 본질" |
| **프로토콜** | 통신 규칙의 표준화된 집합 | "공용 언어" |
| **패킷** | 네트워크를 통해 전송되는 데이터의 단위 | "택배 상자" |

---

## Ⅰ. 개요 및 필요성

- 개요: 분산 가용성 소진 공격
- 배경: 봇넷과 반사 서버는 피해자 회선·장비·애플리케이션 용량을 초과하는 트래픽을 생성함.
- 필요성: 공격 유형별 병목이 달라 ISP, scrubbing, CDN/WAF, 서버 튜닝을 단계별로 적용해야 함.
- 범위: SYN Flood, UDP/DNS 증폭, HTTP Flood, BGP diversion, RTBH, SYN cookie를 포함함.

---

## Ⅱ. 구조 및 구성요소

```text
Botnet/Reflector -> Internet -> ISP Edge -> Scrubbing Center/CDN -> WAF/LB -> Server
SYN Flood -> SYN backlog
Amplification -> bandwidth
HTTP Flood -> application worker
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 공격원 | 봇넷·반사 서버로 트래픽 생성 | source spoofing, open resolver |
| ISP Edge | 대용량 트래픽 우회·차단 | BGP diversion, RTBH |
| Scrubbing Center | 정상/공격 트래픽 분리 | signature, rate limit |
| CDN/WAF | L7 요청 흡수·검증 | challenge, bot rule |
| Origin Server | 서비스 처리 | SYN backlog, worker pool |

> 요약: DDoS 대응 구조는 인터넷 경계에서 대용량 트래픽을 정화하고, L7 요청은 CDN/WAF와 서버 지표로 통제한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
공격 징후 탐지 -> 유형 분류 -> 회선/상태/L7 병목 식별
-> ISP 우회 또는 scrubbing -> WAF/CDN 정책 적용 -> 서버 커널 튜닝
-> 정상 사용자 성공률 확인
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | bps, pps, SYN rate, URI hit 급증 탐지 | baseline 대비 배수 |
| 2 | SYN Flood, 증폭, HTTP Flood 유형 분류 | packet header, flow |
| 3 | ISP·scrubbing·CDN으로 우회·정화 | diversion time |
| 4 | SYN cookie, rate limit, WAF rule 적용 | backlog, drop count |
| 5 | 정상 사용자 응답과 오류율 확인 | 2xx rate, 5xx rate |

> 요약: DDoS 대응은 탐지, 유형 분류, 우회·정화, 서버 보호, 정상 사용자 지표 확인 순서로 실행한다.

---

## Ⅳ. 특징

| 구분 | SYN Flood | UDP/DNS 증폭 | HTTP Flood |
|:---|:---|:---|:---|
| 병목 자원 | SYN backlog, state table | 회선 bps, pps | WAS worker, DB connection |
| 공격 원리 | half-open 연결 증가 | 피해자 IP로 반사 응답 유도 | 정상 형태 요청 반복 |
| 대응 위치 | LB/Server/Firewall | ISP, scrubbing | CDN/WAF, application |
| 확인 지표 | SYN_RECV, SYN cookie | inbound bps, reflector IP | URI RPS, 5xx, CPU |

> 요약: DDoS는 병목 자원별로 대응 위치가 다르며 증폭 공격은 내부 장비 도달 전에 회선에서 처리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | DDoS 대응 | 선택 기준 |
|:---|:---|:---|:---|
| 온프레미스 장비 | 방화벽·IPS | scrubbing+CDN 연계 | 회선 용량 초과 공격 |
| 네트워크 계층 | ACL·RTBH | BGP diversion, Flowspec | 대용량 pps/bps |
| 애플리케이션 | rate limit | WAF bot rule, challenge | 정상 요청과 유사한 L7 공격 |

> 요약: 대용량 공격은 ISP·scrubbing, 정상 요청형 공격은 CDN/WAF와 애플리케이션 지표를 결합한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 차단 | 정상 트래픽을 공격으로 분류 | allowlist, staged rule | false positive rate |
| 우회 지연 | BGP diversion 수동 절차 | runbook, 자동 알림 | mitigation time |
| 원본 노출 | CDN 우회 직접 접속 | origin ACL, private link | direct origin hit |

> 요약: 대응 리스크는 오탐, 우회 지연, 원본 노출이며 오탐률과 완화 시간으로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 네트워크 | bps/pps 용량 대비 임계치 | NetFlow, sFlow |
| 서버 상태 | SYN backlog overflow 0건 | kernel metric |
| 서비스 품질 | 정상 사용자 2xx 비율 유지 | APM, synthetic check |

> 요약: DDoS 대응 성과는 공격 차단량보다 정상 사용자 성공률과 병목 자원 회복으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. ISP와 BGP diversion, RTBH, Flowspec 절차를 사전 합의하고 공격 징후 기준 bps/pps 임계값을 정의함.
2. Scrubbing center, CDN/WAF, origin ACL을 연계해 증폭 트래픽과 HTTP Flood를 서로 다른 계층에서 처리함.
3. 서버에 SYN cookie, backlog 파라미터, connection timeout, rate limit을 적용하고 SYN_RECV·5xx·2xx 지표를 대시보드화함.

**결론 (2줄):**
- 기술사 판단: DDoS 대응은 공격 유형별 병목 위치가 다르므로 회선, 상태 테이블, 애플리케이션 계층을 나누어 설계함.
- 향후 방향: 대규모 봇넷과 암호화 트래픽 증가에 따라 행동 기반 탐지, CDN edge 방어, ISP 협업 자동화가 확대됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DDoS 공격을 설명하시오" | 유형별 공격 흐름 | SYN·증폭·HTTP 비교 |
| 요구사항 명시형 | "DDoS 대응 방안을 제시하시오" | 탐지-우회-정화-복구 절차 | 지표·오탐·완화 시간 |

> 요약: 설명형은 공격 원리, 방안형은 계층별 대응과 정상 사용자 지표 중심으로 전개한다.
