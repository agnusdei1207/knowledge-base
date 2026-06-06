---
title: "Service Discovery Registry Pattern"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 마이크로서비스 아키텍처(MSA)에서 동적 IP/포트/위치를 가진 서비스 인스턴스를 자동 등록(Register)·탐색(Discover)·상태 점검(Health Check)하여, 클라이언트가 하드코딩 없이 런타임에 서비스 엔드포인트를 해석하도록 하는 분산 시스템 패턴이다. Consul, Eureka, etcd, ZooKeeper, Kubernetes DNS/CoreDNS가 대표 구현체이며, AP/CP 트레이드오프와 Self-registration vs Third-party registration 모델의 선택이 핵심 설계 결정점이다.
> 2. **가치**: 서비스 인스턴스의 평균 탐지 시간(MTTD)을 5분(수동 DNS) -> 1~3초(Heartbeat 기반)로 단축하며, Auto-scaling으로 인한 churn rate(시간당 100% 이상) 환경에서도 무중단 라우팅을 보장한다. Netflix Eureka는 전사적으로 5,000+ 서비스, 100,000+ 인스턴스를 단일 레지스트리로 운영한 실증 사례이며, Istio Service Mesh와 결합 시 L7 트래픽 관리까지 통합 가능하다.
> 3. **판단 포인트**: ① **Client-side vs Server-side discovery** (프록시 부담 vs 라우팅 유연성), ② **Self-registration vs Third-party registration** (결합도 vs 운영 복잡도), ③ **AP vs CP** (Consul CP 모드 vs Eureka AP 우선), ④ **Pull vs Push** (캐시 일관성 vs 네트워크 부하), ⑤ **DNS-based vs API-based** (언어 중립성 vs 메타데이터 풍부함) — 다섯 가지 트레이드오프를 트래픽 패턴·팀 규모·SLA 요구사항 기준으로 의사결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통 모놀리식 아키텍처에서는 서비스 인스턴스가 1~3개로 고정되어 `/etc/hosts`나 L4 로드밸런서 하드코딩만으로 충분했다. 그러나 컨테이너 오케스트레이션(Kubernetes, Nomad) 환경에서는 **Pod의 평균 수명이 5~15분에 불과**하고, Auto-scaling Group은 수십~수천 개의 인스턴스를 탄력적으로 생성/소멸시킨다. AWS의 EC2 인스턴스 메타데이터(`169.254.169.254`)는 24시간 내 50% 이상의 IP가 변경될 수 있으며, K8s의 Deployment Rolling Update 시 구버전과 신버전이 동시에 존재하는 **과도기(Transition) 상태**가 빈번하다.

이런 환경에서 클라이언트가 `http://order-service:8080`과 같이 고정 호스트명을 기대하면, **Stale Endpoint 문제**(죽은 인스턴스로의 라우팅으로 5xx 에러율 폭증)가 발생한다. 2014년 Netflix가 AWS US-EAST 리전 장애 시 Eureka 없이 리전 페일오버를 시도했다가 5시간 동안 서비스를 잃은 사례(Netflix Postmortem, 2014)는 이 패턴의 필요성을 산업계에 각인시킨 결정적 사건이다.

```text
  +-------------------- 전통적 모놀리식 환경 (정적 환경) --------------------+
  |                                                                         |
  |   Client --DNS Lookup---> Load Balancer(HAProxy/L4) ---> App1, App2     |
  |            (TTL 5분)        (VIP 고정)                 (고정 IP 3대)   |
  |                                                                         |
  |   문제점: 인스턴스 추가 시 LB 수동 등록, 장애 시 5분 이상 Stale         |
  +-------------------------------------------------------------------------+

                       v 서비스 디스커버리 도입 (동적 환경) v

  +------------------- MSA + Container 환경 (동적 환경) --------------------+
  |                                                                         |
  |   Service Provider                Registry              Consumer       |
  |   +------------+                  +----------+         +----------+    |
  |   | order-svc  |--Register/Heart-->|          |<--Query--| gateway  |    |
  |   | 10.0.1.12  |   beat(3s)       |  Eureka  |         |  SDK     |    |
  |   +------------+                  |  Consul  |         | Client    |    |
  |   | order-svc  |--Register/Heart-->|  etcd    |         |  -side   |    |
  |   | 10.0.1.13  |                  |          |<--Load---| Balancer |    |
  |   +------------+                  +----------+  balance+----------+    |
  |        |                              ^                                 |
  |        |                              | Health Check (TCP/HTTP/gRPC)   |
  |        v                              | (5~30s 주기)                    |
  |   (Status: UP/DOWN/OUT_OF_SERVICE)    |                                 |
  |                                                                         |
  |   ✦ Heartbeat 중단 시 30s 후 자동 Eviction, 5초 이내 Failover 가능     |
  +-------------------------------------------------------------------------+
```

**왜 필요한가 — 4대 핵심 동기**

1. **동적 토폴로지(Dynamic Topology)**: K8s Pod IP는 `ephemeral`하며 재기동 시 변경됨. CNI(Flannel/Calico)가 10.244.x.x 대역을 재할당.
2. **탄력적 스케일링(Elasticity)**: HPA가 트래픽 피크 시 10->50 인스턴스로 확장할 때, LB 풀(pool)이 이를 즉시 반영해야 함.
3. **고가용성(HA)**: 단일 인스턴스 장애 시 수동 개입 없이 트래픽이 정상 인스턴스로 우회되어야 함(RTO < 30초).
4. **다중 환경(Multi-Environment)**: dev/staging/prod가 동일 클라이언트 코드를 사용하면서 다른 엔드포인트로 라우팅(Blue-Green, Canary).

- **📢 섹션 요약 비유**: 택배 기사가 택배상자 주소를 외워두는 것(하드코딩)이 아니라, **중앙 물류센터(레지스트리)에 "지금 3층 집배소에서 5명의 집배원이 일하고 있다"고 실시간으로 조회**하며 배달하는 시스템과 같다. 집배원이 아프면 센터가 즉시 다른 집배원에게 라우팅한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

서비스 디스커버리 레지스트리는 **4가지 핵심 액터**와 **3단계 라이프사이클**으로 구성된다.

```text
  +-------------------------------- 아키텍처 상세도 -------------------------------+
  |                                                                              |
  |  +-------------------+         +-------------------+        +---------------+  |
  |  |  Service Provider |         |   Service         |        |   Service     |  |
  |  |  (Producer)       |         |   Registry        |        |   Consumer    |  |
  |  |                   |         |                   |        |   (Client)    |  |
  |  |  +-------------+  |         |  +-------------+ |        |               |  |
  |  |  |OrderService |  | ①Register|  | Registry DB | | ③Query  |  +--------+  |  |
  |  |  | Pod-A       |--+---------->|  |  - key: svc |<-+---------|--| Order  |  |  |
  |  |  | 10.244.1.5  |  |  {IP,    |  |    name     | | {인스턴스}  |  | Client |  |  |
  |  |  | :8080       |  |   port,  |  |  - value:   | |  목록}     |  |        |  |  |
  |  |  | metadata}   |  |   health}|  |    [inst1,  | |        |  +----+---+  |  |
  |  |  +-------------+  |         |  |     inst2]  | |        |       |      |  |
  |  |  +-------------+  |         |  |  - TTL: 30s | |        |       v      |  |
  |  |  |OrderService |  | ②Heart |  |  - lastBeat | |   ④LB  |  +--------+  |  |
  |  |  | Pod-B       |--+--------->|  |  : timestamp| +--------->|-|Client  |  |  |
  |  |  | 10.244.1.6  |  |  (3s)   |  +-------------+ |  Pick   |  |Side LB |  |  |
  |  |  +-------------+  |         |  +-------------+ |  (RR/   |  |  RR    |  |  |
  |  |                   |         |  |HealthChecker|-╫--------->|  |  Random|  |  |
  |  |                   |         |  | (Active)    | |  Probe  |  |  Least |  |  |
  |  |                   |         |  | /health     | |  (10s)  |  |  Conn  |  |  |
  |  |                   |         |  +-------------+ |        |  +----+---+  |  |
  |  +-------------------+         +-------------------+        |       |      |  |
  |                                                           |       v      |  |
  |                                                           |  ⑤HTTP/gRPC  |  |
  |                                                           |    Call      |  |
  |                                                           +---------------+  |
  |                                                                              |
  |  ※ Server-side discovery의 경우 ③~⑤를 LB/API Gateway가 처리                |
  +------------------------------------------------------------------------------+
```

### 핵심 메커니즘 — 단계별 상세

**① Registration (등록)**
- **Self-registration**: 서비스 인스턴스가 시작 시 SDK(Eureka Client, Consul Agent)를 통해 레지스트리에 `POST /eureka/v2/apps/ORDER-SVC`로 자신을 등록. IP, port, `instanceId`, `leaseInfo` (renewalIntervalInSecs=30, durationInSecs=90) 포함.
- **Third-party registration**: 별도의 Registrator/Consul-Template/Sidecar가 K8s API, AWS ASG API를 Polling(5s)하여 자동 등록. **결합도 v, 운영 복잡도 ^**.
- 등록 시 `Data Plane`(실제 메타데이터)과 `Control Plane`(상태/정책) 분리 설계 권장.

**② Health Check & Heartbeat (상태 점검)**
- **Active Probe**: Registry가 직접 `GET /health`, TCP `SYN-ACK`, gRPC `Health.Check`를 10~30초 주기로 수행.
- **Passive Heartbeat**: 클라이언트가 30초마다 `PUT /eureka/v2/apps/ORDER-SVC/i-001/heartbeat`을 갱신. **3회 연속 누락 시(90초) 자동 Eviction**.
- Netflix의 "**Red Black Tree 기반 Eviction**"은 30만 인스턴스에서도 O(log n) 성능 보장.

**③ Service Discovery (탐색)**
- **Client-side**: 클라이언트가 `GET /eureka/v2/apps/ORDER-SVC`로 인스턴스 목록을 받고, 로컬에서 Ribbon/Resilience4j로 LB 결정. -> **장점**: 제로 네트워크 홉, **단점**: 클라이언트 SDK 종속.
- **Server-side**: 클라이언트는 단일 VIP(Consul DNS `order-svc.service.consul`) 또는 Envoy/Istiod에 질의, Envoy가 클러스터 내 LB 수행. -> **장점**: 언어 중립, **단점**: 홉 1개 추가.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Service Registry** | 서비스 인스턴스의 위치/메타데이터 저장소 | Eureka(AP, In-memory + Async Replicate), Consul(Raft 합의, CP 기본/AP 옵션), etcd(Raft, CP, K8s 내부), ZooKeeper(ZAB, CP), Nacos(AP+CP 듀얼모드) |
| **Service Provider** | 비즈니스 로직 수행, 자기 상태 등록 | `@EnableEurekaClient` (Spring Cloud), `consul agent -register`, gRPC `ServiceRegistration` |
| **Service Consumer** | 레지스트리 조회, 인스턴스 선택 후 호출 | Netflix Ribbon(Client-side LB, RoundRobin/Random/WeightedResponseTime), Spring Cloud LoadBalancer, Istio Envoy Sidecar |
| **Health Checker** | 인스턴스 활성/비활성 판단 | TCP connect, HTTP `/health/ready` (K8s Liveness/Readiness), gRPC `health.v1.Health.Check`, 커스텀 Lambda(메모리/CPU 임계치) |
| **Lease Manager (선택)** | TTL/만료 관리, Eviction 처리 | Guava `ExpirationMap`, Netflix `EvictionTask` (15분 주기 Daemon) |

### 핵심 파라미터 & 알고리즘

**1. CAP 트레이드오프**
- **Eureka (AP 우선)**: Self-preservation 모드 — 네트워크 파티션 시 모든 인스턴스를 유지(과대 라우팅 허용)하여 가용성 극대화. 클라이언트가 레지스트리 변경분을 **30초마다 Pull**.
- **Consul (CP 우선)**: Raft 합의로 강한 일관성, 5개 노드 quorum에서 3개 이상 응답 필요. 단, 분할 시 Leader Election으로 10~30초 동안 쓰기 거부.

**2. Cache Coherence & Eventual Consistency**
- Eureka 클라이언트는 **3단계 캐시** 보유: `ReadOnlyCacheMap(30s TTL) -> ReadWriteCacheMap(실시간) -> Full Registry(180s)`. 빈번한 Registry API 호출을 줄여 Registry 부하 90% 절감.
- 갱신 방식: `Delta Fetch`(변경분만) — Eureka `GET /eureka/v2/apps/delta`는 전체 대비 트래픽 95% 절감.

**3. Consistent Hashing (고급 LB)**
- Ribbon의 `ZoneAwareLoadBalancer`는 동일 AZ(AZ affinity) 인스턴스 우선 선택 후, **Weighted Response Time** 알고리즘으로 응답 지연이 낮은 인스턴스에 가중치 부여. Eureka 인스턴스 메타데이터에 `zone`, `region` 태그를 추가하면 Cross-AZ 트래픽 70% 절감.

**4. Session Affinity (Sticky Session)**
- gRPC의 경우 HTTP/2 커넥션 멀티플렉싱 특성상 **Sticky LB 필수**. Consul Connect의 L4 LB는 Consistent Hashing으로 동일 클라이언트 -> 동일 백엔드 매핑.

- **📢 섹션 요약 비유**: 레지스트리는 **학교 출석부**와 같다. 학생(서비스)이 매일 아침(Heartbeat) "출석합니다!" 라고 도장을 찍고, 담임(Health Checker)이 직접 등교 여부를 확인한다. 3일 연속 결석(Eviction)하면 자동 퇴학 처리. 선생님(Consumer)은 출석부를 보고 어느 반에 어느 학생이 있는지 즉시 파악하여 과제를 맡긴다.

---

## Ⅲ. 비교 및 연결

### 비교 1: Client-side vs Server-side Discovery

| 구분 | Client-side Discovery (Eureka+Ribbon) | Server-side Discovery (Consul DNS + Envoy) |
| :--- | :--- | :--- |
| **LB 위치** | 클라이언트 프로세스 내 (In-Process) | 별도 Proxy/LB (Envoy, AWS ALB) |
| **네트워크 홉** | 1홉 (Direct Call) | 2홉 (Consumer -> LB -> Provider) |
| **언어 종속성** | 언어별 SDK 필요 (Java Ribbon, Python pyribbon) | 언어 중립 (HTTP
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 458 / 600

<- **이전**: [457. API 게이트웨이 패턴 라우팅 인증](/studynote/04_software_engineering/05_devops_ci_cd/305_api_gateway_pattern)
**다음**: [459. 사이드카 앰배서더 프록시 패턴](/studynote/11_design_supervision/06_exam_summary/459_sidecar_ambassador/) ->

---
