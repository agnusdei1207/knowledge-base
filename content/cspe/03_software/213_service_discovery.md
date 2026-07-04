---
title: "서비스 디스커버리 (Service Discovery)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 213
---

# 📖 【암기용】 개념 완전 이해

> 목적: 서비스 디스커버리를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 서비스 디스커버리는 **마이크로서비스 아키텍처(MSA)**에서 끊임없이 바뀌는 서비스 인스턴스의 네트워크 위치를 **서비스 레지스트리(Service Registry)**로 실시간 추적해 호출자가 살아있는 대상만 부르게 하는 **동적 위치 해석** 메커니즘이다.
- **왜 필요한가**: 컨테이너·오토스케일링 환경은 인스턴스가 초 단위로 생성·삭제·교체되어 IP가 고정되지 않는다. 호출자가 정적 설정 파일에 IP를 박아두면 배포마다 수정해야 하고, 죽은 인스턴스로도 트래픽이 계속 간다.
- **핵심 직관**: 실시간으로 갱신되는 전화번호부다. 지금 영업 중인 지점만 올라오고, 폐업한 지점은 자동으로 지워진다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| MSA(마이크로서비스 아키텍처) | 서비스를 잘게 쪼개 독립 배포하는 구조 — 디스커버리가 필요해지는 상위 배경 | 백화점 하나 대신 개별 매장 여럿 |
| 서비스 레지스트리(Service Registry) | 서비스명과 살아있는 endpoint 목록을 보관하는 중앙 저장소 | 실시간으로 갱신되는 전화번호부 |
| 등록(Register) | 인스턴스가 시작할 때 자신의 IP·포트·메타데이터를 레지스트리에 올리는 행위 | 신규 지점이 번호부에 전화번호를 등록 |
| 하트비트(Heartbeat) | 인스턴스가 주기적으로 "나 살아있다"를 레지스트리에 보내는 신호 | 지점이 매시간 "영업 중" 신호를 본사에 보냄 |
| 헬스 체크(liveness/readiness) | 인스턴스가 살아있는지(liveness)와 요청 받을 준비가 됐는지(readiness)를 확인하는 절차 | 문을 열었는지 + 손님 받을 준비가 됐는지 이중 확인 |
| TTL(Time To Live) | 클라이언트가 조회 결과를 캐시해 두는 최대 시간 | 번호부 사본을 믿고 쓰는 유효기간 |
| Client-side Discovery | 클라이언트가 직접 레지스트리를 조회해 대상을 고르는 방식 | 손님이 직접 번호부를 펴서 지점을 고름 |
| Server-side Discovery | 로드밸런서·게이트웨이가 레지스트리를 대신 조회해 골라주는 방식 | 안내데스크 직원이 번호부를 보고 연결해줌 |
| Stale Endpoint | 이미 죽었지만 캐시·레지스트리에 아직 남아있는 낡은 endpoint | 폐업했는데 아직 번호부에 남은 가게 |
| Split Brain | 레지스트리 노드 간 정보가 갈려 서로 다른 endpoint 목록을 신뢰하는 상태 | 본사 번호부와 지사 번호부 내용이 서로 다름 |

## 깊이 이해

### 왜 필요했나 (배경)
- 전통적 3-tier 아키텍처는 서버 대수가 적고 배포도 드물어 `/etc/hosts`나 정적 설정 파일에 IP를 적어도 충분했다.
- MSA·Kubernetes 환경에서는 오토스케일링으로 Pod가 하루에도 수십~수백 번 생성·삭제된다. 예를 들어 Pod 100개 클러스터에서 트래픽 변동에 따라 하루 20%가 재배치되면 인스턴스 20개의 IP가 매일 바뀐다. 정적 설정으로는 감당이 안 되어, "이름으로 부르면 현재 살아있는 주소를 돌려주는" 동적 해석 계층이 필요해졌다.

### 등록-하트비트-조회 흐름을 수치로 이해하기
- 인스턴스가 뜨면 자신을 레지스트리에 등록하고, 이후 주기적으로 하트비트를 보낸다. 예: 하트비트 주기 10초, 연속 3회 실패 시 down 판정이면, 장애 인스턴스를 레지스트리에서 제거하는 데 최대 30초(10초 × 3회)가 걸린다.
- 그 30초 동안 클라이언트가 여전히 이 인스턴스로 요청을 보내면 실패한다. 그래서 TTL(클라이언트 캐시 유지 시간)이 이 감지 지연보다 훨씬 길면 죽은 endpoint를 더 오래 붙들게 되므로, 보통 TTL을 30초 이하로 짧게 맞춰 감지 지연과 균형을 맞춘다.

### Client-side vs Server-side 판별 원리
- 판별 기준은 "레지스트리를 누가 직접 조회하고 대상을 고르는가"다.
- Client-side(예: Netflix Eureka): 클라이언트 SDK가 레지스트리를 캐시해 두고 스스로 로드밸런싱까지 수행한다. 중간 홉이 하나 줄어 지연이 낮지만, 언어마다 SDK를 배포·관리해야 해 여러 언어를 쓰는(polyglot) 환경에서는 부담이 커진다.
- Server-side(예: Kubernetes Service, Envoy): 클라이언트는 이름만 부르고, 중간 로드밸런서·게이트웨이가 레지스트리 조회와 대상 선택을 대신한다. 언어와 무관하게 동작하지만, 그 중앙 LB가 병목이나 단일 장애점이 될 수 있다.
- 실무 판단: 언어가 여러 개면 Server-side, 단일 스택이고 SDK 통제가 가능하면 Client-side가 유리하다.

### 레지스트리 자체의 가용성 - 수치로 보는 Split Brain 위험
- 레지스트리도 죽으면 전체 디스커버리가 멈춘다. 그래서 여러 노드로 이중화하고 과반수(quorum) 합의로 운영한다.
- 예: etcd 5노드 클러스터는 quorum이 3(⌊5/2⌋+1)이므로 2노드까지 장애를 견디지만, 3노드 클러스터는 quorum이 2라서 1노드 장애만 견딘다. 노드 수가 적을수록, 또는 네트워크가 분할될수록 split brain(서로 다른 목록을 신뢰)이나 전체 조회 불가 위험이 커진다.

### 비유와 흔한 오해
- **비유**: 실시간 전화번호부다. 폐업한 가게는 자동으로 빠지고, 신규 개업 가게는 곧바로 올라온다.
- **오해**: "DNS만 있으면 서비스 디스커버리가 끝난다." 실제로는 DNS 자체에 헬스 체크 개념이 약해, TTL 캐시·헬스 체크·endpoint 갱신(EndpointSlice) 로직이 함께 있어야 죽은 대상을 걸러낼 수 있다.

## 연결 개념
- Load Balancing - 디스커버리로 찾은 endpoint 중 실제 호출 대상을 고르는 다음 단계
- Service Mesh - Sidecar가 발견·라우팅·mTLS를 데이터플레인 수준에서 통합 처리
- Kubernetes Service - 클러스터 내부 디스커버리의 기본 구현체(Label Selector + EndpointSlice + CoreDNS)

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 서비스 위치 조회뿐 아니라 등록, 상태 확인, 캐시, 장애 제거까지 답안에 포함한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Service Discovery는 서비스명으로 현재 사용 가능한 인스턴스 endpoint를 찾는 동적 위치 해석 체계이다.
> 2. **가치**: 오토스케일링·무중단 배포 환경에서 설정 변경 없이 호출 경로를 유지한다.
> 3. **판단 포인트**: Client-side, Server-side, DNS-based, Registry-based 방식은 운영 책임과 장애 전파 범위가 다르다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 클라우드 네이티브 호출 구조 이해 확인 | 등록, 조회, health check, TTL, endpoint 갱신 | "IP를 찾는 기술" 수준 설명 |
| 방식별 선택 역량 확인 | Client-side vs Server-side, DNS vs Registry | Kubernetes Service와 Consul 차이 누락 |
| 장애 통제 확인 | stale endpoint, split brain, registry 장애 | Registry 장애 시 fallback 미작성 |

> 요약: 서비스 디스커버리는 이름 해석과 상태 검증을 결합해 살아 있는 대상만 호출하게 하는 운영 메커니즘이다.

---

## Ⅰ. 개요 및 필요성

- 개요: 서비스명 기반 주소 해석 기능
- 배경: MSA와 Kubernetes 환경에서는 인스턴스 생성·삭제가 빈번하여 정적 IP 설정이 장애 원인이 된다.
- 필요성: 서비스명 호출, health check, TTL 제어로 동적 인스턴스 변경을 반영해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Service Instance -> Register/Heartbeat -> Service Registry
Client/Gateway -> Lookup Service Name -> Endpoint List
Endpoint List -> Load Balancer -> Healthy Instance -> Metric/Trace
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Service Registry | 서비스명과 endpoint 목록 저장 | Consul, Eureka, etcd, Kubernetes API |
| Health Checker | 인스턴스 생존과 준비 상태 확인 | liveness/readiness probe |
| Discovery Client | 조회·캐시·재시도 수행 | TTL과 stale 제거 정책 필요 |
| Load Balancer | endpoint 선택과 장애 제외 | round robin, least request, zone aware |

> 요약: 디스커버리는 Registry, 상태 확인, 조회 캐시, 로드 밸런싱이 결합되어 동작한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Instance Start -> Register Endpoint -> Heartbeat Update
-> Client Lookup -> Endpoint Cache -> Request Route
-> Health Fail -> Deregister -> Retry Other Endpoint
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 인스턴스 시작과 메타데이터 등록 | service, version, zone 포함 |
| 2 | heartbeat와 health probe 수행 | interval 10초, failure threshold 3회 |
| 3 | 호출자가 endpoint 조회·캐시 | TTL 30초 이하 |
| 4 | 장애 endpoint 제거와 재시도 | 5xx rate, connection error 기준 |

> 요약: 등록보다 health 상태 반영 속도와 캐시 만료 정책이 장애 전파를 줄인다.

---

## Ⅳ. 특징

| 구분 | Client-side Discovery | Server-side Discovery | 판단 수치 |
|:---|:---|:---|:---|
| 호출 책임 | 클라이언트가 조회·선택 | LB/Gateway가 조회·선택 | 언어별 SDK 부담 여부 |
| 예시 | Netflix Eureka client | Kubernetes Service, Envoy | polyglot 환경은 server-side 유리 |
| 장애 영향 | 클라이언트 캐시 stale 가능 | 중앙 LB 병목 가능 | TTL 30초, failover 10초 목표 |
| 운영 포인트 | SDK 배포 관리 | LB와 Registry 관측 | endpoint change latency 측정 |

> 요약: 다언어 MSA는 Server-side, SDK 통제가 가능한 환경은 Client-side 선택 가능하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | Service Discovery | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 정적 IP, hosts 파일 | 동적 registry와 health 기반 endpoint | 배포 빈도 일 1회 이상이면 필요 |
| 비용/성능 | 수동 변경, 장애 호출 | lookup cache와 health exclusion | endpoint 갱신 p95 10초 이하 |
| 운영/위험 | 설정 drift | registry 장애·stale cache | multi-AZ registry, local cache |

> 요약: 인스턴스 변동성과 배포 빈도가 높을수록 디스커버리 체계가 필수이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Stale Endpoint | TTL 과다, deregister 지연 | TTL 30초, readiness gate | failed connection rate |
| Registry 장애 | 단일 노드, quorum 손실 | 3/5 노드 quorum, local cache | registry availability 99.9% |
| 잘못된 라우팅 | 버전·zone 메타데이터 누락 | version label, canary subset | wrong-version request count |

> 요약: 핵심 리스크는 오래된 endpoint와 registry 장애이며 TTL, quorum, 메타데이터로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 발견 지연 | endpoint 갱신 p95 10초 이하 | registry event log |
| 호출 품질 | 5xx 1% 이하, retry 3회 이하 | gateway metric |
| 운영 추적 | service/version/zone 라벨 100% | CMDB, Kubernetes label audit |

> 요약: 발견 지연, 실패율, 메타데이터 완전성을 통해 운영 품질을 측정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Kubernetes 환경: Service, EndpointSlice, CoreDNS, readinessProbe로 기본 디스커버리 구성
2. 멀티클러스터: Consul 또는 service mesh registry federation으로 zone-aware routing 적용
3. 장애 통제: TTL 30초 이하, health failure threshold 3회, local cache fallback, registry quorum 3노드 이상 구성

**결론 (2줄):**
- 기술사 판단: 단일 Kubernetes 내부는 Service/DNS, 멀티런타임·멀티클러스터는 Registry 또는 Service Mesh 기반을 선택
- 향후 방향: eBPF·service mesh가 디스커버리와 로드 밸런싱을 dataplane 수준에서 결합하는 방향으로 발전

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "서비스 디스커버리를 설명하시오" | 등록, 조회, health, TTL 흐름 | Client-side와 Server-side 비교 |
| 요구사항 명시형 | "MSA 호출 구조를 설계하시오" | Registry 장애, 캐시, 라우팅 설계 | Kubernetes/Consul/mesh 선택 기준 |

> 요약: 설명형은 구성 원리, 설계형은 장애와 운영 책임 배치를 중심으로 작성한다.
