---
title: "로드 밸런싱 전략 (Load Balancing Strategy)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 214
---

# 📖 【암기용】 개념 완전 이해

> 목적: 로드 밸런싱 전략을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 로드 밸런싱은 여러 백엔드 서버에 요청을 나눠 보내는 **트래픽 분산(Traffic Distribution)** 기법으로, 동작하는 **OSI 계층(L4 전송 계층/L7 응용 계층)**에 따라 방식이 갈린다.
- **왜 필요한가**: 하나의 서버가 모든 요청을 받으면 CPU 사용률이 치솟고 요청이 큐에 쌓이며, 그 서버가 죽으면 서비스 전체가 멈추는 단일 장애점이 된다.
- **핵심 직관**: 매장 입구 안내원이 손님 수·처리 속도·계산대 상태를 보고 가장 알맞은 계산대로 안내하는 것과 같다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| OSI L4(전송 계층) | IP·Port·TCP 연결 단위로 분산 — 패킷 내용은 보지 않음 | 우편번호만 보고 배송 트럭을 배정 |
| OSI L7(응용 계층) | HTTP Host·Path·Header·Cookie 내용까지 읽고 라우팅 | 편지 내용까지 읽고 담당 부서를 배정 |
| Round Robin | 서버에 순서대로 돌아가며 하나씩 배정 | 번호표 순서대로 배정 |
| Least Connection(Least Request) | 현재 연결·요청 수가 가장 적은 서버에 배정 | 줄이 가장 짧은 계산대로 안내 |
| Weighted(가중치 분산) | 서버 성능 비율만큼 가중치를 두고 배정 | 숙련 직원에게 더 많은 손님을 배정 |
| Health Check | 서버가 살아있고 요청을 받을 준비가 됐는지 주기적으로 확인 | 계산대가 실제로 열려 있는지 확인 |
| Sticky Session(세션 고정) | 같은 클라이언트의 요청을 항상 같은 서버로 보냄 | 담당 창구 지정제 |
| Retry Storm(재시도 폭주) | 한 서버가 느려지자 클라이언트들이 동시에 재시도해 상황을 더 악화시키는 현상 | 계산대 하나가 밀리자 모두가 동시에 옆 계산대로 몰림 |

## 깊이 이해

### 왜 필요했나 (배경)
- 웹·API 서비스는 시간대별 트래픽 편차가 크다. 서버를 늘리는 것만으로는 부족하고, 어느 서버가 살아있는지, 세션은 어디로 보낼지, 배포 중 트래픽은 어떻게 전환할지까지 함께 다뤄야 한다.

### L4 vs L7 판별 원리
- 판별 기준은 "패킷의 어느 부분까지 읽고 분산하는가"다.
- L4는 IP·Port·TCP 연결만 보고 분산하므로 처리 비용이 낮고 빠르다. TCP 커넥션 단위 서비스(DB 프록시, 순수 TCP 서비스)에 적합하다.
- L7은 HTTP 요청을 파싱해 Host·Path·Header·Cookie까지 읽으므로, `/api`는 백엔드 A로 `/static`은 백엔드 B로 보내는 URL 기반 라우팅이 가능하다. 대신 TLS 복호화·HTTP 파싱 비용이 들어 L4보다 CPU 사용량이 높다.
- 실무 판단: URL·헤더 기반 라우팅이나 카나리 배포가 필요하면 L7, 단순 대량 TCP 처리면 L4를 쓴다.

### 가중치 분산을 수치로 이해하기
- 서버 4대 중 vCPU 8개 서버 2대, vCPU 4개 서버 2대가 있다고 하자. 성능 비례로 가중치를 2:2:1:1로 주면 총 가중치 합은 6이다.
- 전체 트래픽이 1,200RPS라면 가중치 1당 200RPS(1,200÷6)가 배정되어, vCPU 8개 서버는 각각 400RPS, vCPU 4개 서버는 각각 200RPS를 받는다. 이렇게 성능에 비례해 부하를 맞추면 특정 서버만 과부하되는 것을 막는다.

### Health Check 감지 지연을 수치로 이해하기
- Health Check 주기 10초, 연속 실패 3회 기준이면 장애 서버를 제외하는 데 최대 30초(10초 × 3회)가 걸린다. 이 30초 동안 그 서버로 향하는 요청은 계속 실패한다.
- 그래서 감지 지연을 줄이려면 주기를 짧게(예: 5초) 하거나 threshold를 낮추는데, 대신 순간적인 지연(false positive)에도 서버가 제외될 위험이 커지는 트레이드오프가 있다.

### Retry Storm - 왜 재시도가 장애를 키우는가
- 예: timeout 1초, 재시도 2회 정책이면 요청 하나가 최악의 경우 최대 3배(1회 원 요청 + 2회 재시도)의 트래픽을 만든다.
- 백엔드 5xx 오류율이 원래 1%였어도, 모든 클라이언트가 동시에 재시도하면 순간적으로 실질 요청량이 2~3배로 튀어 오히려 서버 부하가 늘고 오류율이 더 올라가는 악순환(retry storm)이 생긴다. jitter(무작위 지연)와 retry budget(전체 재시도 상한)으로 동시 재시도를 흩어야 한다.

### 비유와 흔한 오해
- **비유**: Round Robin은 번호표 순서 배정, Least Connection은 줄이 짧은 창구 배정, Weighted는 숙련도에 따른 손님 배정이다.
- **오해**: "로드 밸런싱은 트래픽을 골고루 나누는 것"만이 아니다. 장애 탐지 지연, 세션 고정, 재시도 폭주, 리전 간(cross-zone) 전송 비용까지 함께 설계해야 한다.

## 연결 개념
- Auto Scaling - 부하 지표를 보고 서버 대수를 늘리고 줄이는 다음 단계
- Circuit Breaker - 장애 서버로의 호출 자체를 차단해 재시도 폭주를 막는 보완 장치
- Service Discovery - 로드 밸런서가 분산할 대상 endpoint 목록을 제공

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 알고리즘 이름 나열이 아니라 L4/L7 위치, 세션, health check, 지표 기반 선택을 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Load Balancing은 요청을 다수 backend로 분산하고 장애 backend를 제외하는 트래픽 제어 계층이다.
> 2. **가치**: p95 지연, 오류율, 자원 사용률, 배포 전환을 운영 지표로 통제한다.
> 3. **판단 포인트**: L4/L7, Round Robin/Least Request/Weighted, 세션 고정, retry 정책을 업무 특성에 맞게 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산 처리 구조 이해 확인 | L4/L7, health check, 알고리즘, failover | Round Robin만 설명하고 장애 제외 누락 |
| 성능·장애 판단 확인 | p95 지연, 5xx, connection count, queue depth | 평균 응답시간만 쓰는 답안 |
| 운영 설계 확인 | sticky session, canary, cross-zone, retry storm | 세션 상태와 재시도 폭주 리스크 누락 |

> 요약: 로드 밸런싱 답안은 분산 알고리즘과 장애 통제를 지표로 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 요청 분산 트래픽 제어 기법
- 배경: 트래픽 집중은 큐 대기와 장애 단일점을 만들며, 서버 증설만으로 해결되지 않는다.
- 필요성: health check, 세션, 재시도, 배포 전략을 함께 설계해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> DNS/GSLB -> L4/L7 Load Balancer
-> Health Check -> Backend Pool
  / Server A
  / Server B
  / Server C
-> Metric/Log/Trace
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| L4 Load Balancer | TCP/UDP 연결 분산 | NAT, DSR, connection 기반 |
| L7 Load Balancer | HTTP 요청 라우팅 | Host, Path, Header, Cookie 활용 |
| Health Check | backend 상태 확인 | interval 10초, 실패 3회 제외 |
| Algorithm | 대상 선택 | Round Robin, Least Request, Weighted |

> 요약: 로드 밸런싱 구조는 진입점, 상태 확인, backend pool, 선택 알고리즘으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request In -> TLS Termination -> Rule Match
-> Backend Health Filter -> Algorithm Select
-> Forward Request -> Response/Retry -> Metric Update
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청 수신과 라우팅 규칙 매칭 | Host/Path rule 충돌 0건 |
| 2 | health check 결과로 대상 필터링 | unhealthy 제외 30초 이내 |
| 3 | 알고리즘으로 backend 선택 | 서버별 부하 편차 20% 이하 |
| 4 | 실패 시 retry·failover 수행 | retry 1~2회, timeout 1초 |

> 요약: 분산 품질은 라우팅 규칙, 상태 필터, 알고리즘, 재시도 제한의 조합으로 결정된다.

---

## Ⅳ. 특징

| 구분 | L4 | L7 | 판단 수치 |
|:---|:---|:---|:---|
| 기준 | IP, Port, TCP 연결 | HTTP Host, Path, Header | URL별 라우팅 필요 시 L7 |
| 처리 비용 | 패킷 수준 처리 | TLS·HTTP 파싱 비용 | TLS termination CPU 60% 이하 |
| 기능 | NAT, DSR, connection balance | WAF, canary, header routing | canary 1/5/10% 전환 |
| 세션 | source IP hash | cookie, header 기반 | 로그인 세션 외부 저장 권장 |

> 요약: L4는 연결 분산, L7은 애플리케이션 라우팅에 적합하며 기능 요구가 선택 기준이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Load Balancing | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 서버, DNS RR | health 기반 backend pool | 5xx 1% 초과 또는 CPU 70% 지속 시 필요 |
| 비용/성능 | 수동 증설 | 오토스케일링 연계 | p95 지연 300ms 이하 목표 |
| 운영/위험 | 단일 장애점 | LB 이중화와 zone 분산 | multi-AZ, active-active 구성 |

> 요약: 트래픽 분산은 서버 수보다 health와 zone 장애를 반영한 라우팅 능력으로 평가한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Retry Storm | backend 지연 시 동시 재시도 | timeout, jitter, retry budget | retry rate 5% 이하 |
| Session Loss | sticky 서버 장애 | Redis session, JWT, stateless 설계 | session error count |
| 불균등 분산 | 가중치·connection 편차 | least request, EWMA latency | backend load skew 20% 이하 |

> 요약: 로드 밸런싱 장애는 재시도 폭주, 세션 손실, 편중 부하를 중심으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연/처리량 | p95 300ms 이하, RPS 목표 충족 | APM, LB metric |
| 장애 제외 | unhealthy 제외 30초 이내 | health check log |
| 배포 전환 | canary 1% 단위, rollback 5분 이내 | release metric, error budget |

> 요약: 성공 여부는 지연, 장애 제외 시간, 배포 전환 지표로 판정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. API 서비스는 L7 ALB/Ingress로 Host·Path 라우팅, TCP 서비스는 L4 NLB로 connection 기반 분산 적용
2. health check interval 10초, failure threshold 3회, timeout 1초, retry 1회와 jitter를 기본값으로 설정
3. 세션은 Redis 또는 JWT로 외부화하고 canary 1%부터 10%까지 오류율 1% 이하 확인 후 확대

**결론 (2줄):**
- 기술사 판단: 단순 TCP 대량 처리면 L4, URL·헤더·배포 제어가 필요하면 L7, 글로벌 장애 대응은 GSLB 병행
- 향후 방향: Service Mesh와 eBPF dataplane이 endpoint discovery, mTLS, 로드 밸런싱을 통합하는 방향으로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "로드 밸런싱을 설명하시오" | 요청 라우팅과 health filter 흐름 | L4/L7·알고리즘 비교 |
| 요구사항 명시형 | "고가용 API 분산 방안을 설계하시오" | retry, timeout, failover 설계 | 지표·세션·배포 전환 기준 |

> 요약: 설명형은 알고리즘과 계층 비교, 설계형은 장애·세션·배포 운영 기준을 전면 배치한다.
