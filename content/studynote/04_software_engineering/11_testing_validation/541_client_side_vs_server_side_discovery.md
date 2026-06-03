+++
title = "541. 클라이언트 사이드 디스커버리 vs 서버 사이드 디스커버리"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 서비스 디스커버리(Service Discovery)의 두 방식인 클라이언트 사이드(Client-Side)는 호출자가 직접 서비스 레지스트리를 조회해 인스턴스를 선택하는 방식이고, 서버 사이드(Server-Side)는 로드 밸런서가 대신 서비스 위치를 결정하는 방식이다.
> 2. **가치**: 마이크로서비스 환경에서 서비스 인스턴스가 동적으로 생성·소멸하므로 하드코딩된 주소로는 통신이 불가능하여, 서비스 디스커버리는 동적 서비스 위치 확인의 필수 메커니즘이다.
> 3. **판단 포인트**: 클라이언트 사이드는 유연하지만 클라이언트에 로직이 추가되고, 서버 사이드는 단순하지만 로드 밸런서가 단일 실패 지점이 될 수 있으므로 팀의 기술 역량과 인프라 환경에 맞게 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 모놀리식 시스템에서는 서버의 IP 주소와 포트가 고정되어 있었다. 그러나 마이크로서비스와 컨테이너 기반 배포 환경에서는 서비스 인스턴스가 동적으로 시작되고 종료되며, IP 주소와 포트가 매 배포마다 바뀐다. 쿠버네티스(Kubernetes)에서 파드(Pod)가 재시작되면 IP가 변경되고, 오토스케일링으로 인스턴스가 늘어나거나 줄어든다.

이런 동적 환경에서 서비스 A가 서비스 B를 호출하려면 "지금 서비스 B가 어디서 실행되고 있는가?"를 알아야 한다. 이를 해결하는 메커니즘이 서비스 디스커버리다. 서비스 인스턴스는 시작 시 서비스 레지스트리(Service Registry)에 자신을 등록하고, 종료 시 등록을 해제한다. 호출자는 레지스트리를 조회하여 현재 가용한 인스턴스를 찾는다.

서비스 디스커버리 구현 방식은 크게 두 가지로 나뉜다. <strong>클라이언트 사이드 디스커버리</strong>는 클라이언트(호출자 서비스)가 레지스트리를 직접 조회하고 로드 밸런싱 로직을 포함하는 방식이다. <strong>서버 사이드 디스커버리</strong>는 클라이언트가 로드 밸런서(또는 인그레스)에 요청하면, 로드 밸런서가 레지스트리를 조회하고 적절한 인스턴스로 전달하는 방식이다. 쿠버네티스의 Service 리소스가 서버 사이드 디스커버리의 대표 구현이다.

- **📢 섹션 요약 비유**: 맛집을 찾을 때, 직접 맛집 앱을 열어 검색하고 선택하는 것(클라이언트 사이드)과, 안내 데스크에 "맛집 알려줘"라고 하면 직원이 대신 예약해 주는 것(서버 사이드)의 차이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 클라이언트 사이드 디스커버리 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">클라이언트 사이드 디스커버리</div></div>
<div class="kb-diagram-note">클라이언트 서비스 (Service A)</div>
<div class="kb-diagram-tree-item" style="--depth:2">1. 서비스 레지스트리 조회</div>
<div class="kb-diagram-note">(Eureka/Consul에 "Service B 인스턴스 목록?" 요청)</div>
<div class="kb-diagram-tree-item" style="--depth:2">2. 인스턴스 목록 수신</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">B:192.168.1.10:8080, B:192.168.1.11:8080</div></div>
<div class="kb-diagram-tree-item" style="--depth:2">3. 로드 밸런싱 알고리즘 적용</div>
<div class="kb-diagram-note">(클라이언트 내 Ribbon/Spring Cloud LoadBalancer)</div>
<div class="kb-diagram-tree-item" style="--depth:2">4. 선택된 인스턴스 직접 호출</div>
<div class="kb-diagram-note">→ Service B Instance 1 (192.168.1.10:8080)</div>
<div class="kb-diagram-note">핵심 도구: Netflix Eureka + Ribbon, Consul + 클라이언트 라이브러리</div>
</div>
</div>



### 서버 사이드 디스커버리 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">서버 사이드 디스커버리</div></div>
<div class="kb-diagram-note">클라이언트 서비스 (Service A)</div>
<div class="kb-diagram-tree-item" style="--depth:2">1. 로드 밸런서에 요청 (service-b로 요청)</div>
<div class="kb-diagram-note">(고정된 DNS 또는 가상 IP)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">로드 밸런서 / 인그레스</div>
<div class="kb-diagram-note">(Kubernetes Service / Nginx / HAProxy)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">2. 레지스트리 조회 + 인스턴스 선택</div>
<div class="kb-diagram-note">(kube-proxy가 iptables 규칙 관리)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">3. 적절한 인스턴스로 요청 전달</div>
<div class="kb-diagram-note">→ Service B Instance 2 (10.0.0.5:8080)</div>
<div class="kb-diagram-note">핵심 도구: Kubernetes Service + kube-proxy, AWS ALB, Nginx</div>
</div>
</div>



### 두 방식 핵심 비교

| 비교 항목 | 클라이언트 사이드 디스커버리 | 서버 사이드 디스커버리 |
|:---|:---|:---|
| 레지스트리 조회 주체 | 클라이언트 서비스 | 로드 밸런서/프록시 |
| 로드 밸런싱 주체 | 클라이언트 내 로직 | 인프라 계층 |
| 클라이언트 복잡도 | 높음 (레지스트리 조회 코드 필요) | 낮음 (단순 호출만) |
| 언어/프레임워크 의존 | 높음 (라이브러리 필요) | 없음 (언어 무관) |
| 유연성 | 높음 (커스텀 로드 밸런싱 가능) | 보통 (인프라 설정으로만 제어) |
| 단일 실패 지점 | 없음 (분산 처리) | 있음 (LB 장애 시 전체 영향) |
| 대표 구현 | Netflix Ribbon + Eureka | Kubernetes Service, AWS ALB |

### 서비스 레지스트리 도구 비교

| 도구 | 유형 | 특징 | 적합 환경 |
|:---|:---|:---|:---|
| Netflix Eureka | AP (고가용성 우선) | REST API, Spring Cloud 통합 | Spring Boot MSA |
| HashiCorp Consul | CP (일관성 우선) | DNS, HTTP, 헬스체크, KV Store | 다중 DC, 멀티 클라우드 |
| Apache ZooKeeper | CP | 강한 일관성, 분산 코디네이션 | Kafka, Hadoop 생태계 |
| etcd | CP | Kubernetes 기본 저장소 | Kubernetes |
| Kubernetes DNS | 내장 | CoreDNS 기반, 자동 등록 | Kubernetes 클러스터 내 |

### 헬스 체크(Health Check) 메커니즘

서비스 레지스트리는 등록된 인스턴스의 상태를 주기적으로 확인한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">헬스 체크 흐름</div></div>
<div class="kb-diagram-note">서비스 인스턴스 시작</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">서비스 레지스트리에 등록</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">레지스트리 주기적 헬스 체크 (GET /health)</div>
<div class="kb-diagram-tree-item" style="--depth:2">정상 응답 (200 OK) → 레지스트리에 유지</div>
<div class="kb-diagram-tree-item" style="--depth:2">응답 없음 (3회 연속) → 레지스트리에서 제거</div>
<div class="kb-diagram-note">장점: 비정상 인스턴스 자동 제거</div>
<div class="kb-diagram-note">주의: 헬스체크 주기 설정이 너무 길면 장애 인스턴스가 오래 유지됨</div>
</div>
</div>



- **📢 섹션 요약 비유**: 회사 내부 전화번호부(서비스 레지스트리)에 각 팀의 번호가 등록된다. 직접 전화번호부를 보고 전화하는 것(클라이언트 사이드)과, 교환원(로드 밸런서)에게 "마케팅팀 연결해줘"라고 부탁하는 것(서버 사이드)의 차이다.

---

## Ⅲ. 비교 및 연결

### 쿠버네티스의 서비스 디스커버리

쿠버네티스 환경에서는 서버 사이드 디스커버리가 기본이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">쿠버네티스 서비스 디스커버리</div></div>
<div class="kb-diagram-note">파드 A (클라이언트)</div>
<div class="kb-diagram-note">↓ DNS 조회: order-service.default.svc.cluster.local</div>
<div class="kb-diagram-note">CoreDNS</div>
<div class="kb-diagram-note">↓ VIP (Virtual IP) 반환: 10.96.100.50</div>
<div class="kb-diagram-note">kube-proxy (iptables/ipvs 규칙)</div>
<div class="kb-diagram-note">↓ 실제 파드 IP로 NAT</div>
<div class="kb-diagram-note">파드 B1 또는 B2 (랜덤 또는 라운드 로빈)</div>
</div>
</div>



쿠버네티스에서는 서비스 이름으로 DNS 조회만 하면 kube-proxy가 모든 디스커버리와 로드 밸런싱을 처리한다.

### 서비스 메시(Service Mesh)와의 관계

서비스 메시(Istio, Linkerd)는 서버 사이드 디스커버리의 발전된 형태이다.

| 비교 항목 | 기본 쿠버네티스 서비스 | 서비스 메시 (Istio) |
|:---|:---|:---|
| 로드 밸런싱 | L4 (IP/포트 기반) | L7 (HTTP 헤더, 가중치 기반) |
| 트래픽 제어 | 제한적 | 카나리, A/B 테스트, 서킷 브레이커 |
| 관측성 | 기본 메트릭 | 분산 추적, 서비스 그래프 |
| 보안 | 네트워크 정책 | mTLS 자동 적용 |

- **📢 섹션 요약 비유**: 기본 전화 교환기(쿠버네티스 Service)는 그냥 연결만 해주지만, 고급 교환 시스템(서비스 메시)은 통화 품질 모니터링, 특정 통화에 가중치 부여, 자동 암호화까지 제공한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 환경별 디스커버리 방식 권장



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">환경에 따른 디스커버리 방식 선택</div></div>
<div class="kb-diagram-note">쿠버네티스 환경</div>
<div class="kb-diagram-note">→ 서버 사이드 (쿠버네티스 Service + CoreDNS)</div>
<div class="kb-diagram-note">→ 고급 요구사항: 서비스 메시 (Istio/Linkerd)</div>
<div class="kb-diagram-note">On-Premise 또는 VM 기반 MSA</div>
<div class="kb-diagram-note">→ Consul + 클라이언트 사이드 (HashiCorp Consul)</div>
<div class="kb-diagram-note">→ 또는 HAProxy/Nginx 로드 밸런서 (서버 사이드)</div>
<div class="kb-diagram-note">Spring Boot 기반 MSA (클라우드 미사용)</div>
<div class="kb-diagram-note">→ Netflix Eureka + Ribbon (클라이언트 사이드)</div>
<div class="kb-diagram-note">→ Spring Cloud Gateway (서버 사이드)</div>
<div class="kb-diagram-note">클라우드 네이티브 (AWS/GCP/Azure)</div>
<div class="kb-diagram-note">→ 관리형 LB (ALB, Cloud Load Balancing)</div>
<div class="kb-diagram-note">→ 서비스 메시 관리형 (AWS App Mesh, GKE Anthos)</div>
</div>
</div>



### 설계 판단 체크리스트

1. **배포 환경 일치**: 선택한 디스커버리 방식이 배포 환경(쿠버네티스, VM, 클라우드)에 적합한가?
2. **클라이언트 복잡도 수용**: 클라이언트 사이드 선택 시 팀이 각 언어별 디스커버리 라이브러리를 관리할 역량이 있는가?
3. **단일 실패 지점 대응**: 서버 사이드 선택 시 로드 밸런서의 고가용성(HA) 구성이 되어 있는가?
4. **헬스 체크 설정**: 서비스 레지스트리의 헬스 체크 주기와 실패 임계값이 적절히 설정되어 있는가?
5. **서비스 등록/해제 자동화**: 서비스 시작·종료 시 레지스트리 등록/해제가 자동으로 이루어지는가?
6. **라우팅 정책 제어**: 카나리 배포, 가중치 기반 트래픽 분산 등 고급 라우팅이 필요한가?

### 안티패턴

- **하드코딩된 서비스 주소**: IP 주소나 호스트명을 코드나 설정 파일에 직접 기입하면 동적 환경에서 서비스 재시작마다 설정을 변경해야 한다. 반드시 서비스 레지스트리나 DNS 기반 디스커버리를 사용해야 한다.
- **레지스트리 단일 인스턴스 운영**: 서비스 레지스트리를 단일 인스턴스로 운영하면 레지스트리 장애 시 전체 서비스 디스커버리가 마비된다. Eureka, Consul은 클러스터링을 통해 고가용성을 보장해야 한다.
- **헬스 체크 생략**: 헬스 체크 없이 서비스를 레지스트리에 등록하면, 비정상 인스턴스도 계속 요청을 받아 오류가 발생한다. /health 또는 /actuator/health 엔드포인트를 반드시 구현하고 레지스트리에 등록해야 한다.
- **클라이언트 사이드에 복잡한 라우팅 로직 집중**: 클라이언트 측 로드 밸런싱 코드가 복잡해지면 모든 서비스가 동일 라이브러리에 의존하게 된다. 복잡한 트래픽 관리는 서비스 메시(인프라 계층)로 이관해야 한다.

- **📢 섹션 요약 비유**: 직접 길을 찾는(클라이언트 사이드) 경우 길을 잘 알아야 하고, 네비게이션(서버 사이드)에 맡기는 경우 네비게이션 오류 시 막막해진다. 중요한 것은 어느 방식이든 경로가 항상 최신으로 유지되어야 한다는 점이다.

---

## Ⅴ. 기대효과 및 결론

올바른 서비스 디스커버리 전략을 채택하면 마이크로서비스의 동적 환경에서도 서비스 간 통신이 안정적으로 유지되고, 오토스케일링·롤링 배포·카나리 배포가 클라이언트 코드 변경 없이 투명하게 동작한다.

**쿠버네티스 환경에서의 실제 효과**: 쿠버네티스의 서버 사이드 디스커버리(Service + CoreDNS)를 통해 개발자는 서비스 디스커버리 코드를 전혀 작성하지 않아도 된다. 서비스 이름(order-service)으로 호출하면 쿠버네티스가 자동으로 적절한 파드로 라우팅한다. 이 추상화는 클라우드 이식성을 높이고 개발 생산성을 크게 향상시킨다.

결론적으로, 현대 클라우드 네이티브 환경에서는 서버 사이드 디스커버리(쿠버네티스 Service 또는 서비스 메시)가 기본 선택이다. 고급 트래픽 제어가 필요하면 서비스 메시를, 복잡한 환경에서 클라이언트 제어가 필요하면 클라이언트 사이드 방식을 선택한다. 핵심은 "서비스 위치를 동적으로 확인하는 메커니즘 없이는 마이크로서비스는 동작하지 않는다"는 점이다.

- **📢 섹션 요약 비유**: 스스로 길 찾기(클라이언트 사이드)는 자유롭지만 길을 알아야 하고, 자율 주행차(서버 사이드)는 편하지만 자율 주행 시스템을 믿어야 한다. 현대 도시(쿠버네티스)는 자율 주행에 최적화되어 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 마이크로서비스 분해 패턴 (532) | 분해 후 서비스 간 위치 확인에 디스커버리 필요 |
| 서비스 간 동기 통신 (535) | 동기 호출 시 서비스 디스커버리로 대상 주소 결정 |
| 사이드카 프록시 패턴 (546) | 서비스 메시가 서버 사이드 디스커버리를 구현 |
| 트래픽 라우팅 및 카나리 배포 (547) | 서비스 디스커버리 + 트래픽 가중치 제어 결합 |
| 서킷 브레이커 (572) | 비정상 인스턴스 감지와 결합하여 장애 격리 |
| 외부화 설정 (544) | 디스커버리 설정(레지스트리 주소 등)의 외부화 |
| 컨테이너 기반 배포 (561) | 컨테이너 동적 IP로 인해 디스커버리가 더욱 중요해짐 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">하드코딩된 서비스 주소 (모놀리식 시대)</div>
<div class="kb-diagram-note">(서버 IP/포트 고정, 정적 설정)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">DNS 기반 서비스 위치 확인</div>
<div class="kb-diagram-note">(hostname → IP, 그러나 캐싱 문제)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">서비스 레지스트리 등장</div>
<div class="kb-diagram-note">(Netflix Eureka, 2012 / HashiCorp Consul, 2014)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">클라이언트 사이드 LB (Netflix Ribbon + Eureka)</div>
<div class="kb-diagram-note">(Spring Cloud Netflix 생태계)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">쿠버네티스 Service + kube-proxy</div>
<div class="kb-diagram-note">(서버 사이드 디스커버리 표준화, 2015~)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">서비스 메시 (Istio, Linkerd) 등장</div>
<div class="kb-diagram-note">(L7 트래픽 관리 + 디스커버리 통합, 2017~)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">eBPF 기반 차세대 서비스 디스커버리</div>
<div class="kb-diagram-note">(Cilium - 커널 수준 패킷 처리, 초저지연)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 학교에서 친구 교실을 찾을 때, 직접 층마다 돌아다니며 찾는 것(클라이언트 사이드)과, 선생님한테 "3학년 2반 어디야?" 물어보면 바로 알려주는 것(서버 사이드)처럼, 서비스도 다른 서비스 위치를 찾는 방법이 두 가지예요.
2. 친구가 교실을 자주 옮기면(쿠버네티스의 파드 재시작) 직접 찾기가 어려워지니, 항상 최신 위치를 알고 있는 교무실(서비스 레지스트리)에 물어보는 게 훨씬 편리해요.
3. 요즘 학교(쿠버네티스)는 자동으로 교실 배정을 관리하니까, 학생(서비스)은 그냥 "3학년 2반에 가줘"라고만 하면 학교 시스템이 알아서 데려다줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 673 / 973

← **이전**: [540. 서비스 디스커버리 (Service Discovery) - 동적 IP/Port 레지스트리 (Eureka, Consul)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/540_service_discovery/)
**다음**: [541. 클라이언트 사이드 디스커버리 vs 서버 사이드 디스커버리](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/541_service_discovery_client_vs_server/) →

---
