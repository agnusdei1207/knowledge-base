---
title: "쿠버네티스 서비스·인그레스 (Kubernetes Service Ingress)"
date: "2026-07-04"
tags:
  - "cspe-software"
weight: 176
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: 쿠버네티스에서 변동성이 심한 파드(Pod)들에게 고정된 진입점을 제공(Service)하고, 외부의 HTTP/HTTPS 트래픽을 도메인/경로 기반으로 라우팅(Ingress)하는 네트워크 리소스이다.
- **왜 필요한가**: 파드는 수시로 죽고 새로 생기면서 IP가 계속 바뀐다. 클라이언트가 파드의 임시 IP를 직접 바라보면 통신이 끊어지므로 고정된 연락처(Service)와 외부 접수창구(Ingress)가 필수적이다.
- **핵심 직관**: Service는 회사 내 부서별 "대표 내선번호"(고정 IP)이고, Ingress는 회사 밖에서 들어오는 요청을 내선번호로 연결해 주는 "건물 로비 안내데스크"(L7 라우팅)이다.

## 핵심 용어 정리

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| ClusterIP (서비스 기본형) | 클러스터 내부에서만 통신 가능한 고정 가상 IP | "회사 내부망 전용 내선번호" |
| NodePort (서비스) | 클러스터의 모든 워커 노드의 동일한 포트를 열어 외부 노출 | "어느 층(노드)이든 특정 번호 누르면 연결" |
| LoadBalancer (서비스) | 클라우드 제공자의 외부 로드밸런서(ELB 등)를 동적 할당 | "외부망 직통 대표 번호 신설" |
| 인그레스 (Ingress) | L7 기반(HTTP/HTTPS) 외부 트래픽 라우팅 및 SSL 종단 규칙 모음 | "로비 안내데스크 및 간판" |

## 깊이 이해
- **배경·문제의식**: MSA 환경에서 파드 A가 파드 B와 통신하려 할 때 파드 B의 IP는 매번 바뀐다. 이를 해결하기 위해 DNS 이름과 고정 IP를 묶어주는 Service가 등장했다. 그러나 외부로 노출할 웹 서비스가 수십 개인데 모두 LoadBalancer 서비스로 열면 클라우드 비용이 폭증하고 관리(SSL 등)가 파편화되는 문제가 생겼다.
- **작동 원리**:
  - **Service**: Label Selector를 통해 뒤에 연결될 파드들을 묶는다. Kube-proxy가 노드의 iptables/IPVS 규칙을 갱신해 고정 IP(VIP)로 들어온 트래픽을 살아있는 파드들로 분산(L4 로드밸런싱)한다.
  - **Ingress**: 컨트롤러(예: Nginx Ingress Controller)가 1개의 외부 LoadBalancer만 점유한 뒤, 들어오는 HTTP 헤더(도메인 `api.com` 또는 경로 `/auth`)를 분석해 알맞은 내부 Service로 트래픽을 넘긴다 (L7 라우팅).
- **비유**: 쇼핑몰 서버 10개마다 각각 비싼 외부 간판(LoadBalancer)을 다는 대신, 건물 입구에 큰 안내데스크(Ingress) 하나만 두고 "옷은 1층(Service A), 신발은 2층(Service B)"으로 길을 안내하는 것이 효율적이다.
- **구체 예시**: 사용자가 `https://myapp.com/api`로 접속 -> Ingress Controller(80/443 포트 수신) -> `/api` 규칙 매칭 -> `api-service` (ClusterIP)로 전달 -> `api-pod`에 도달.
- **흔한 오해·주의점**: Ingress 객체 자체는 단순한 "설정 파일(규칙)"일 뿐이다. 이 규칙을 읽고 실제로 동작하는 프로세스인 "Ingress Controller(Nginx 등)"를 별도로 배포하지 않으면 아무 일도 일어나지 않는다.

## 연결 개념
- Kube-Proxy — 노드 넷단에서 서비스 IP 패킷을 실제 파드로 가로채서 넘겨주는 핵심 컴포넌트
- 엔드포인트 (Endpoints) — 서비스 셀렉터에 매칭된 살아있는 파드의 실제 IP:Port 목록
- 서비스 디스커버리 (CoreDNS) — 서비스 이름(`my-svc.default.svc.cluster.local`)을 ClusterIP로 변환

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 쿠버네티스 네트워킹은 파드의 휘발성 IP를 추상화하는 L4 밸런서(Service)와 외부 HTTP 트래픽을 쪼개주는 L7 라우터(Ingress)의 결합이다.
> 2. **가치**: 파드 재생성 시 통신 단절을 막고, 서비스 디스커버리를 제공하며, 단일 진입점(Ingress)을 통한 인프라 비용 절감과 SSL 중앙 관리를 가능하게 한다.
> 3. **판단 포인트**: 클러스터 내부 통신, 외부 단순 노출, 복잡한 URL 라우팅 요구에 따라 ClusterIP, NodePort, LoadBalancer, Ingress를 단계적으로 선택 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컨테이너 네트워크 추상화 기법 이해 | Service(L4, IP/Port) vs Ingress(L7, Domain/Path) 역할 차이 | Ingress를 단순히 또 다른 Service 타입 중 하나로 잘못 분류 |

> 요약: 변동성이 큰 파드 환경에서 안정적 내부 통신을 보장하는 Service의 구조와, 외부 트래픽을 효율적으로 통제하는 Ingress의 차별화된 역할을 설계 관점에서 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 동적 파드 묶음에 고정된 접근 IP/도메인을 부여하는 Service와 외부 HTTP(S) 트래픽을 이 서비스들로 스마트하게 라우팅하는 Ingress 리소스
- 배경: 컨테이너 생명주기 특성상 파드 IP는 지속 변경되므로 클라이언트가 파드에 직접 의존할 수 없는 네트워크 단절 문제 발생
- 필요성: 클러스터 내/외부 서비스 디스커버리(DNS) 자동화, 로드밸런싱, 그리고 다중 웹 서비스 노출 시 비용 및 SSL 인증서 관리의 일원화

---

## Ⅱ. 구조 및 구성요소

```text
External Client -> LoadBalancer (클라우드 인프라)
                     |
                   Ingress Controller (L7 규칙 판단: 도메인/경로)
                     |-> 매칭 -> Service A (ClusterIP: L4 가상 IP) -> Pod 1, Pod 2
                     |-> 매칭 -> Service B (ClusterIP: L4 가상 IP) -> Pod 3
```

| 구성요소 | 프로토콜 | 주요 역할 및 특징 |
|:---|:---|:---|
| Service (ClusterIP) | L4 (TCP/UDP) | 클러스터 내부용 기본 고정 IP, CoreDNS 자동 등록 |
| Service (LoadBalancer) | L4 (TCP/UDP) | 클라우드 벤더의 ELB 연동을 통한 외부 직접 노출 |
| Ingress Resource | L7 (HTTP/S) | 도메인, URL 경로 라우팅 규칙 및 SSL 설정 명세서 |
| Ingress Controller | L7 (HTTP/S) | Ingress 규칙을 읽어 실제 리버스 프록시(Nginx 등) 수행 |

> 요약: 외부 트래픽은 Ingress 컨트롤러의 L7 라우팅을 거쳐 내부 Service의 고정 L4 VIP로 분배된 후 최종 엔드포인트 파드로 전달된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 생성 -> CoreDNS 등록 -> Kube-proxy 규칙 갱신 -> Ingress 라우팅 -> 파드 도달
```

- 1단계 [엔드포인트 동기화]: `selector` 라벨에 맞는 파드가 생성/삭제되면, K8s 컨트롤러가 `Endpoints` 객체의 파드 IP 목록을 자동 갱신
- 2단계 [가상 IP 맵핑]: 노드별 Kube-proxy 데몬이 iptables/IPVS 규칙을 조작하여 Service VIP로 들어오는 패킷을 실제 파드 IP로 NAT 변환
- 3단계 [외부 트래픽 유입]: Ingress Controller가 도메인 주소(`host`)나 URL 경로(`/api`)를 분석하여 백엔드 Service 지정
- 4단계 [최종 라우팅]: Ingress -> Service(VIP) -> Kube-proxy 분산 -> 정상 Readiness Probe를 통과한 파드에 트래픽 전달

> 요약: 상태 변화는 Endpoints를 통해 실시간 동기화되며, Kube-proxy의 커널 네트워크 제어(iptables)를 통해 트래픽 분산이 투명하게 일어난다.

---

## Ⅳ. 심화 비교 및 적용 판단

| 비교 축 | NodePort / LoadBalancer | Ingress | 선택 기준 |
|:---|:---|:---|:---|
| 라우팅 계층 | L4 중심 (IP 및 포트 매핑) | L7 중심 (HTTP 도메인, 헤더, 경로) | 취급 프로토콜 특성 |
| 배포 비용 | 서비스 노출마다 LB 비용 별도 발생 | 1개의 LB로 여러 웹 서비스 통합 노출 | 클라우드 인프라 운영 비용 |
| 기능 확장성 | 단순 분산 | SSL 종단(Termination), 리다이렉트, Auth | L7 페이로드 조작 필요 여부 |

> 요약: TCP/UDP 등 비-웹 트래픽은 LoadBalancer 서비스로 노출하고, 복수의 HTTP 마이크로서비스 노출과 SSL 관리는 Ingress로 일원화한다.

**리스크·대응:**
- Kube-proxy(iptables) 병목: 수만 개의 서비스 등록 시 iptables의 순차 검색 구조(O(N))로 인해 네트워크 지연 급증 → O(1) 해시 기반의 IPVS 모드로 Kube-proxy 전환 (지표: 서비스 간 통신 레이턴시 5ms 이하)
- Ingress 단일 장애점(SPOF): 컨트롤러 파드 장애 시 클러스터 외부 진입 전면 마비 → Nginx Ingress Controller를 다중 복제(ReplicaSet) 및 Anti-affinity로 노드 분산 배치 (지표: 외부 인입 가용성 99.99%)

---

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 아키텍처별 계층 노출: Frontend 웹 서버는 Ingress로 외부 노출 및 SSL 처리, Backend API와 DB 파드는 보안을 위해 ClusterIP 서비스로 내부에서만 격리 통신
2. 블루-그린/카나리 배포 제어: Nginx Ingress Controller의 Annotations(`canary-weight: 10%`)를 활용해 신버전 Service로 외부 트래픽의 10%만 가중치 기반 라우팅
3. 차세대 API Gateway(Gateway API) 전환: 기존 Ingress 리소스의 단일화된 한계를 극복하기 위해, 인프라 관리자와 개발자 권한이 분리된 K8s Gateway API 도입으로 네트워크 제어권 분산

**결론 (2줄):**
- 기술사 판단: 서비스와 인그레스 설계는 단순한 연결을 넘어, 클라우드 비용 효율성(단일 LB), L7 라우팅 통제, 사설망 격리 보안을 결정짓는 핵심 아키텍처 요소이다.
- 향후 방향: 전통적인 Ingress 방식에서 벗어나 롤 기반 관리가 뛰어난 Gateway API 규격이 새로운 K8s 트래픽 라우팅 표준으로 대체될 것이다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | Service와 Ingress의 연결 구성도, Endpoints 원리 | 4가지 서비스 타입 비교, Gateway API 진화 |
| 요구사항 명시형 | "외부 노출 방안을 설계하시오" | L7 라우팅 흐름과 Kube-proxy 처리 | 비용 효율적인 Ingress 통제, 카나리 트래픽 분산 방안 |
