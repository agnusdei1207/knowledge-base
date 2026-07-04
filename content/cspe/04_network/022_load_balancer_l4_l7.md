---
title: "로드 밸런서 L4·L7 (Load Balancer L4 L7)"
date: "2026-07-05"
author: "Claude Opus 4.6"
tags:
  - "cspe-network"
weight: 22
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: 로드 밸런서(LB)는 클라이언트 요청을 다수의 백엔드 서버로 분산하여 **가용성**과 **수평 확장(Scale-out)**을 구현하는 트래픽 중재 장비이며, 참조 계층에 따라 L4(IP·Port)와 L7(HTTP 헤더·URI·쿠키)로 구분됨.
- **왜 필요한가**: 단일 서버는 트래픽 증가 시 자원 임계를 초과하고 단일 장애점(SPOF)이 되므로, 다수 서버로 요청을 분산하고 장애 서버를 자동 우회하는 중재 장치가 필수임.
- **핵심 직관**: L4는 톨게이트 직원이 차 번호판(IP)과 차종(Port)만 보고 차로를 배정하는 것이고, L7은 세관원이 짐 내용물(Payload·URL)까지 확인한 뒤 목적지를 결정하는 것.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| SLB (Server Load Balancing, 상위 키워드) | 다수 서버로 트래픽을 분산하는 기능 — L4/L7 로드밸런서의 핵심 목적 | 상담 전화를 대기 중 상담원에게 배분 |
| VIP (Virtual IP) | 클라이언트가 접근하는 LB의 단일 진입점 IP, 실제 서버 IP를 은닉 | 대표 전화번호 |
| RIP (Real IP) | 실제 서비스를 제공하는 백엔드 서버의 IP | 내선 번호 |
| Health Check | ICMP·TCP·HTTP 등으로 서버 생존을 주기적으로 확인하여 장애 서버를 풀에서 제외 | 직원 출근 체크 |
| Round Robin | 서버 풀을 순서대로 돌아가며 배분하는 알고리즘 | 카운터 순번표 |
| Least Connection | 현재 연결 수가 가장 적은 서버에 우선 배분 | 줄이 가장 짧은 계산대로 안내 |
| Sticky Session | 동일 클라이언트를 동일 서버에 지속 배분(Source IP Hash 또는 쿠키) | 단골 고객의 지정석 |
| DSR (Direct Server Return) | 응답 패킷이 LB를 거치지 않고 서버에서 클라이언트로 직접 전송 | 주문은 카운터에서, 음식은 주방에서 직접 전달 |
| TLS Termination | LB가 SSL/TLS 암호화를 해독하여 백엔드 서버의 CPU 부하를 절감 | 입구 보안검색대에서 한 번만 통과 |

## 깊이 이해
- **배경·문제의식**: 초기 DNS 라운드 로빈은 서버 장애를 감지하지 못해 다운된 서버로 계속 요청을 보내는 치명적 한계가 있었음. Health Check로 장애 서버를 자동 제외하고, 알고리즘으로 부하를 균등 분산하는 전용 장비(로드 밸런서)가 등장함.
- **L4 로드밸런서 작동 원리**: 클라이언트가 VIP로 요청 → LB가 TCP/UDP 4-tuple(Src IP·Src Port·Dst IP·Dst Port)을 기준으로 서버를 선택 → DNAT(VIP→RIP)로 패킷 헤더를 변환해 서버로 전달 → 서버 응답을 SNAT(RIP→VIP)로 변환해 클라이언트에 반환함. 패킷 내용을 보지 않으므로 처리 속도가 매우 빠름(수백만 CPS).
- **L7 로드밸런서 작동 원리**: 클라이언트와 LB 간 TCP 세션을 완전히 확립(Reverse Proxy)한 뒤, HTTP 헤더·URI·쿠키를 파싱하여 백엔드 서버를 선택하고 LB-서버 간 별도 TCP 세션을 확립함. TLS Termination으로 암호화를 해독한 뒤 Payload를 검사할 수 있음. 대신 패킷 재조립·분석에 CPU 비용이 큼.
- **DSR 모드**: 대용량 스트리밍 서비스에서 응답 트래픽(수 Gbps)이 LB를 병목시키는 문제를 해결하기 위해, 서버가 응답 패킷을 LB를 거치지 않고 클라이언트로 직접 전송함. 인바운드(요청)만 LB를 통과하므로 LB 대역폭 부담이 크게 경감됨.
- **비유**: L4는 톨게이트에서 차량 번호(IP)와 차종(Port)만 보고 즉시 차로를 배정하므로 빠르지만, 짐(Payload)에 따라 다른 창고로 보내는 건 못 함. L7은 세관에서 짐을 풀어 검사하므로 느리지만, "/api/video"는 비디오 서버로, "/api/auth"는 인증 서버로 정밀 배분이 가능함.
- **구체 예시**: 이커머스 서비스에서 앞단 L4 LB가 100만 CPS 트래픽을 10대의 L7 LB(NGINX)로 1차 분산하고, 각 L7 LB가 URI(/product, /cart, /payment)별로 각각의 MSA 서비스 그룹에 2차 분산하는 2-Tier 구성이 대표적임.
- **흔한 오해·주의점**: "L7이 L4를 완전 대체한다"는 오해가 흔하나, L7은 패킷 재조립·TLS 해독으로 CPU 소모가 크므로, 대규모 트래픽 환경에서는 L4를 앞단에 두는 2-Tier 구성이 필수임. 또 Sticky Session은 부하 불균형을 유발하므로, 궁극적으로는 애플리케이션을 Stateless로 재설계하고 세션 데이터를 외부 저장소(Redis 등)로 분리해야 함.

## 연결 개념
- **스위칭 계층(021)**: L4/L7 스위치의 SLB 기능에서 발전한 전용 장비·소프트웨어.
- **방화벽(023)**: NGFW가 L7 분석·WAF 기능을 통합하면서 L7 LB와 기능이 일부 중첩됨.
- **Service Mesh**: Envoy Sidecar 패턴으로 L7 프록시 기능을 MSA 내부까지 확장.

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라이언트 트래픽을 L4(IP·Port) 또는 L7(HTTP 헤더·URI) 기준으로 다수 서버에 분산하여 SPOF를 제거하고 Scale-out을 구현하는 중재 아키텍처임.
> 2. **가치**: Health Check 기반 장애 서버 자동 우회로 가용성을 확보하고, 알고리즘 기반 부하 균등 분산으로 SLA 99.99% 달성이 가능함.
> 3. **판단 포인트**: 대용량 단순 분산은 L4(NAT/DSR), MSA API 라우팅·모바일 세션 유지는 L7(Reverse Proxy)을 선택하며, 2-Tier 병용이 대규모 서비스의 표준 구성임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| L4·L7 동작 계층·식별 정보 차이 | L4: 4-tuple NAT, L7: Reverse Proxy, URI 파싱 | "L7이 L4보다 좋다" 식 비기술적 서술 |
| 알고리즘·세션 유지 기법 | RR, Least Conn, Source IP Hash vs 쿠키 Sticky | Sticky Session의 부하 불균형 단점 누락 |
| 아키텍처 배치·성능 트레이드오프 | L4+L7 2-Tier, DSR, TLS Termination 오버헤드 | L4/L7 단일 구성만 서술, DSR 누락 |

> 요약: 트래픽 특성에 맞춘 계층(L4/L7) 선택, 알고리즘·세션 유지 기법, 2-Tier 배치 전략을 서술해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 클라이언트 트래픽을 다수 백엔드 서버로 분산하여 가용성과 수평 확장을 구현하는 트래픽 중재 장비임.
- 배경: 단일 서버의 자원 임계 도달과 DNS 라운드 로빈의 장애 서버 우회 불가 한계를 극복하기 위해 등장함.
- 필요성: MSA 환경에서 서비스별 라우팅, TLS 오프로딩, Health Check 기반 SPOF 제거로 SLA 99.99%를 달성해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> VIP(LB 진입점) -> [스케줄링 알고리즘] -> Server Pool
                              |                      +-> Server A (Active)
                              +-> L4: 4-tuple NAT    +-> Server B (Active)
                              +-> L7: URI/Header      +-> Server C (Down - 풀 제외)
                              +-> Health Check(주기적 생존 확인)
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| VIP | 클라이언트가 접근하는 단일 진입점 IP | 서버 IP 은닉, DNS에 VIP 등록 |
| Server Pool | Health Check 통과 서버의 동적 목록 | Auto Scaling 연동 시 자동 증감 |
| Health Check | ICMP·TCP·HTTP로 서버 생존 확인 | 실패 시 3초 이내 풀에서 자동 제외 |
| 스케줄링 알고리즘 | RR, Least Conn, Hashing 등 분산 규칙 | Weighted RR로 서버 스펙 차이 반영 |

> 요약: LB는 VIP로 트래픽을 수신하고, Health Check로 검증된 서버 풀 내에서 알고리즘에 따라 분산함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Client(CIP) -> VIP 요청 -> LB 서버 선택 -> DNAT(VIP->RIP) -> Server 처리
Server 응답 -> LB 수신 -> SNAT(RIP->VIP) -> Client 응답
(DSR 모드: Server 응답 -> Client 직접 전송, LB 우회)
```

1. VIP 수신: 클라이언트는 VIP에 요청을 전송하며, 실제 서버 IP(RIP)는 인지하지 못함.
2. 서버 선택: LB가 스케줄링 알고리즘과 Sticky Session 설정에 따라 대상 서버를 결정함. L4는 4-tuple 기반, L7은 URI·쿠키 기반으로 선택함.
3. 패킷 변환·전달: L4는 DNAT(VIP→RIP)로 헤더만 변환하여 전달하고, L7은 Reverse Proxy로 클라이언트-LB·LB-서버 간 별도 TCP 세션을 확립함.
4. 응답 반환: NAT 모드에서는 LB가 SNAT(RIP→VIP)로 변환 후 반환하고, DSR 모드에서는 서버가 LB를 거치지 않고 클라이언트에 직접 응답함.

> 요약: L4는 NAT 헤더 조작으로 고속 분산하고, L7은 Reverse Proxy로 세션을 분리해 콘텐츠 기반 라우팅을 수행함.

---

## Ⅳ. 특징

- L4 고속 처리: 패킷 내용을 보지 않고 4-tuple NAT만 수행하므로 수백만 CPS 처리가 가능하며, DSR로 응답 대역폭 병목을 제거할 수 있음.
- L7 정밀 라우팅: URI·HTTP 헤더·쿠키를 분석하여 MSA 서비스별 라우팅·A/B 테스트·카나리 배포가 가능함.
- TLS Termination: L7 LB가 SSL/TLS를 해독하여 백엔드 서버 CPU 부하를 절감하고, 인증서를 LB에서 중앙 관리함.
- Sticky Session 한계: 동일 클라이언트를 동일 서버에 고정하면 특정 서버에 부하가 편중되므로, Stateless 설계+외부 세션 저장소(Redis)로 전환이 권장됨.
- 2-Tier 구성: 대규모 서비스에서 앞단 L4가 트래픽을 N대의 L7으로 1차 분산하고, L7이 URI별 2차 분산하는 계층 구성이 표준임.

> 요약: L4는 속도, L7은 정밀 제어에 강하며, 대규모 환경에서는 L4+L7 2-Tier 구성이 필수임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | L4 Load Balancing | L7 Load Balancing | 선택 기준 |
|:---|:---|:---|:---|
| 동작 방식 | NAT(DNAT/SNAT), DSR | Reverse Proxy(세션 분리) | 응답 대역폭 부담 수준 |
| 프로토콜 | TCP·UDP 전반(DB·게임) | HTTP·HTTPS·gRPC | 앱 프로토콜 의존성 |
| 세션 유지 | Source IP Hash | 쿠키 기반 Sticky Session | 모바일(IP 변동) 환경 |
| 보안 기능 | SYN Flood 기본 방어 | WAF 연동, SQLi·XSS 차단 | L7 위협 노출 수준 |

> 요약: 스트리밍·게임은 L4 DSR, API 서비스는 L7 Reverse Proxy가 표준이며, 대규모 환경은 2-Tier 병용이 필수임.

**리스크·대응:**
- Sticky 세션 쏠림: 소수 IP의 대량 트래픽이 특정 서버에 편중 → 타임아웃 최소화, Stateless 재설계+Redis 세션 분리 (지표: 서버별 CPU 사용률 편차)
- L7 LB 병목: TLS 해독·정규식 매칭 오버헤드 → NPU 가속, L4+L7 2-Tier 분산 (지표: LB p95 Latency)
- LB SPOF: 단일 LB 하드웨어 장애 → LB 이중화(VRRP Active-Standby), DNS GSLB 연동 (지표: VIP Failover 소요 시간)

**점검 지표:**
- 성능: LB의 CPS(Connections Per Second), p99 Latency — L4 기준 수백만 CPS 목표
- 가용성: Health Check 장애 감지 시간 — 3초 이내 풀 제외, VIP Failover 5초 이내

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. L4/L7 2-Tier 아키텍처: 외곽 L4(NLB)가 100만 CPS 트래픽을 N대의 L7(NGINX·Envoy)으로 1차 분산하고, L7이 URI별로 MSA 서비스 그룹에 2차 분산함.
2. DSR 적용: 스트리밍·CDN 등 아웃바운드 대역폭이 큰 서비스에서 응답 패킷이 LB를 우회하도록 DSR을 구성하여 LB 병목을 제거함.
3. Stateless 전환: 세션 데이터를 Redis Cluster로 외부화하고, LB의 Sticky 설정을 제거하여 완전한 Least Connection 분산을 달성함.

**결론:**
- 기술사 판단: 클라우드 네이티브 환경에서는 HW L4보다 Kubernetes Ingress Controller·Envoy 등 SW L7 LB가 MSA 라우팅의 핵심이며, L4는 앞단 대용량 분산 전담으로 역할이 분리됨.
- 향후 방향: 단순 트래픽 분산을 넘어 Service Mesh(Istio·Linkerd)의 Sidecar Proxy 패턴으로 MSA 내부까지 L7 관측성·mTLS·트래픽 제어가 확장되는 추세임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "로드 밸런싱 기술을 설명하시오" | VIP·Server Pool·알고리즘, NAT/DSR 흐름 | L4 vs L7 비교, Health Check·Sticky 한계 |
| 요구사항 명시형 | "L4와 L7을 비교하시오", "LB 병목 해결 방안" | NAT vs Reverse Proxy 패킷 흐름 차이 | 2-Tier 분산·DSR·Stateless 전환 방안 |
