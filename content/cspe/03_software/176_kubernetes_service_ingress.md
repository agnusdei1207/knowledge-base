---
title: "쿠버네티스 서비스·인그레스 (Kubernetes Service Ingress)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 176
---

# 📖 【암기용】 개념 완전 이해

> 목적: Kubernetes Service와 Ingress를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Service·Ingress는 계속 바뀌는 Pod 위치를 클라이언트가 몰라도 되게 하는 **서비스 디스커버리** 계층으로, Service는 클러스터 내부 **L4** 접근을, Ingress는 외부 **L7(HTTP/HTTPS)** 라우팅을 담당한다.
- **왜 필요한가**: Pod는 생성·삭제될 때마다 IP가 바뀐다. 클라이언트가 Pod IP를 직접 캐싱해 호출하면, 배포나 장애 복구로 Pod가 교체되는 순간 연결이 끊어진다.
- **핵심 직관**: Service는 팀원이 바뀌어도 번호는 그대로인 대표 전화번호이고, Ingress는 건물 입구에서 회사명·부서명(URL)을 보고 방문객을 안내하는 안내 데스크다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 서비스 디스커버리 | 계속 바뀌는 Pod 위치를 클라이언트가 몰라도 접근할 수 있게 하는 추상화 — 이 개념이 속한 **상위 개념** | 이사를 가도 안 바뀌는 대표번호 |
| L4 / L7 | L4는 IP·포트 기준으로 패킷을 전달, L7은 HTTP 경로·헤더까지 읽고 라우팅 — Service/Ingress의 **역할 구분 기준** | 우편번호만 보고 배달 vs 사람이 주소를 읽고 안내 |
| ClusterIP | 클러스터 내부에서만 접근 가능한 가상 IP(Service의 기본 타입) | 사내 전용 내선번호 |
| NodePort | 모든 Node의 지정 포트(30000~32767)로 외부에서 접근 가능하게 여는 방식 | 각 지점의 대표 외선번호 |
| LoadBalancer | 클라우드 로드밸런서를 자동 생성해 공인 IP로 노출하는 방식 | 전용 안내 데스크 |
| EndpointSlice | selector에 매칭되는 **Ready** Pod의 IP·포트 목록 | 실시간으로 갱신되는 전화 연결부 |
| kube-proxy / eBPF | Service IP로 들어온 트래픽을 실제 Pod로 전달하는 데이터 경로(iptables·IPVS·eBPF 구현) | 자동 전화 교환기 |
| Ingress | host/path 규칙으로 HTTP(S) 트래픽을 어느 Service로 보낼지 정의하는 API 객체(규칙 선언일 뿐 실행체가 아님) | 글로 적힌 안내판 |
| Ingress Controller | Ingress 규칙을 읽어 실제로 프록시·라우팅을 수행하는 프로그램(NGINX, ALB, HAProxy 등) | 안내판을 보고 실제로 안내하는 직원 |
| Gateway API | Ingress보다 세분화된 차세대 L4/L7 라우팅 표준 | 안내판의 다음 세대 버전 |

## 깊이 이해

### 왜 IP 대신 이름으로 접근해야 하나 (배경)
- Deployment가 롤링 업데이트나 장애 복구로 Pod를 교체하면 Pod IP가 계속 바뀐다(예: 배포 전 `10.244.1.5` → 배포 후 `10.244.2.9`). Kubernetes는 label selector로 지금 Ready 상태인 Pod들을 EndpointSlice에 묶고, 클라이언트는 절대 바뀌지 않는 Service 이름/IP로만 접근하게 한다.

### Service 내부 동작 — 수치 워크드 예제
- label `app=api`인 Pod 3개가 모두 Ready라고 하자. EndpointSlice에는 이 3개의 IP:포트가 등록된다. 클라이언트가 ClusterIP `10.96.0.5:80`으로 요청을 보내면, kube-proxy(또는 eBPF datapath)가 3개 중 하나로 트래픽을 분산한다.
- 이 중 Pod 1개가 readinessProbe 실패로 Ready를 잃으면, EndpointSlice에서 **즉시** 제외된다 — 결과적으로 남은 2개 Pod가 각각 받던 트래픽 비중이 약 33%에서 50%로 재분배된다.

### 노출 방식 비교 — 비용 관점 수치
- ClusterIP는 클러스터 내부 전용이라 비용이 없다. NodePort는 30000~32767 범위 포트를 모든 노드에 열어야 해서 방화벽 관리 부담이 크다. LoadBalancer는 Service 1개당 클라우드 LB를 1개씩 만드는데, LB 하나에 월 수십 달러 수준의 고정 비용이 들어 서비스가 10개면 LB 10개 비용이 그대로 청구된다.
- 이 비용 문제 때문에, HTTP 서비스가 여러 개면 공인 IP/LB 1개를 여러 Service가 공유하는 Ingress 구조를 쓴다.

### Ingress 라우팅 — 수치 워크드 예제
- `api.example.com/v1` 요청이 들어오면 Ingress Controller가 ① TLS 인증서로 암호화를 해제(TLS 종료)하고 ② host/path 규칙을 매칭해 `api-service:80`으로 프록시하며 ③ 다시 그 Service가 Ready Pod 3개 중 하나로 로드밸런싱한다.
- 같은 Ingress 안에서 path `/v1`은 `api-service`로, `/admin`은 `admin-service`로 나누는 것처럼, 하나의 도메인·IP로 여러 백엔드를 나눠 안내할 수 있다.

### DNS로 서비스 이름 해석하기
- 클러스터 내부에서는 CoreDNS가 `api-service.namespace.svc.cluster.local` 형태의 이름을 ClusterIP로 해석해준다. 내부 통신은 IP를 직접 쓰지 않고 이 DNS 이름을 쓰는 것이 표준이다.

### 비유
- Service는 팀원이 바뀌어도 대표 번호로 걸면 현재 근무자에게 연결되는 구조이고, Ingress는 건물 입구에서 회사명·부서명을 보고 방문자를 해당 사무실로 안내하는 안내 데스크다.

### 흔한 오해·주의점
- Ingress 객체 자체는 트래픽을 처리하지 않는다. NGINX, HAProxy, 클라우드 ALB 같은 Ingress Controller가 클러스터에 실제로 배포돼 있어야만 규칙이 실제 트래픽 경로로 동작한다.

## 연결 개념
- Pod 생명주기(174) — Ready 상태인 Pod만 EndpointSlice에 등록되어 트래픽 대상이 됨
- Pod 스케줄링(175) — Bind된 후 Ready가 되어야 이 접근 계층에 편입됨
- NetworkPolicy/CNI(177) — Service로 전달된 트래픽이 실제로 Pod 간에 허용되는지는 여기서 추가로 통제됨

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Service와 Ingress 답안은 내부 서비스 발견과 외부 L7 라우팅의 역할을 분리해 설명해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Service는 Pod 접근 추상화, Ingress는 HTTP/HTTPS 외부 진입과 라우팅 규칙임.
> 2. **가치**: Pod IP 변동을 Service DNS와 endpoint로 감추고, Ingress로 host/path 기반 접속을 표준화함.
> 3. **판단 포인트**: ClusterIP, NodePort, LoadBalancer, Ingress는 노출 범위와 L4/L7 요구로 선택함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 서비스 발견 구조 확인 | Service, DNS, EndpointSlice | Pod IP 직접 접근으로 설명 |
| 외부 노출 방식 비교 확인 | NodePort, LoadBalancer, Ingress | Service와 Ingress 역할 혼동 |
| 운영 설계 역량 확인 | TLS, path routing, health check | Ingress Controller 필요성 누락 |

> 요약: 이 문제는 내부 접근 추상화와 외부 L7 라우팅을 분리해 선택 기준을 제시해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Service와 Ingress는 Pod 접근 추상화 계층임.
- 배경: Pod는 생성과 삭제에 따라 IP가 바뀌므로 고정 접속점이 필요하다.
- 필요성: Service는 내부 L4 접근, Ingress는 외부 HTTP/HTTPS 라우팅 기준으로 트래픽 진입점을 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> Ingress Controller -> Service -> EndpointSlice -> Ready Pod
  / 내부 호출 -> Service DNS
  / 외부 호출 -> Host/Path Rule
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Service | Pod 집합에 가상 IP/DNS 제공 | ClusterIP, NodePort, LoadBalancer |
| EndpointSlice | Ready Pod 주소 목록 관리 | selector 기반 |
| Ingress | host/path 라우팅 규칙 | Controller 필요 |
| Ingress Controller | 실제 L7 프록시 수행 | NGINX, ALB, HAProxy |

> 요약: Service는 Pod 집합을 추상화하고 Ingress Controller는 외부 HTTP 요청을 Service로 전달함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Pod label 지정 -> Service selector 매칭 -> EndpointSlice 생성 -> DNS 등록 -> 트래픽 전달
외부 요청 -> Ingress host/path 매칭 -> Service 선택 -> Ready Pod 전달
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Service selector가 Pod label 매칭 | endpoints 존재 |
| 2 | CoreDNS가 service name 해석 | DNS 응답 |
| 3 | kube-proxy/eBPF가 L4 전달 | connection success |
| 4 | Ingress Controller가 host/path 라우팅 | 2xx/3xx 비율 |
| 5 | TLS 종료와 인증 정책 적용 | 인증 실패 로그 |

> 요약: 내부는 Service DNS와 endpoint, 외부는 Ingress rule과 Controller가 트래픽 경로를 만든다.

---

## Ⅳ. 특징

| 구분 | Service | Ingress | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 계층 | L4 | L7 HTTP/HTTPS | path, host 필요 여부 |
| 범위 | Cluster 내부/외부 | 외부 진입 | 공인 IP 수 |
| 기능 | 로드밸런싱, service discovery | TLS, routing, rewrite | 인증 연동 |
| 한계 | L7 규칙 제한 | Controller 의존 | p95 latency |

> 요약: Service는 연결 대상을 추상화하고 Ingress는 외부 HTTP 정책을 집행함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Pod IP 직접 호출 | Service/Ingress 추상화 | Pod 교체 빈도 |
| 비용/처리 | 서비스별 LoadBalancer | Ingress 공통 진입 | 공인 IP 비용 |
| 운영/위험 | 라우팅 분산 | 중앙 L7 정책 | TLS, WAF, 인증 |

> 요약: 다수 HTTP 서비스는 Ingress 공통 진입으로 공인 IP와 TLS 정책을 통합함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Endpoint 누락 | label selector 불일치 | label 표준, admission 검증 | endpoints 0건 |
| 외부 장애 | Controller 단일 장애 | replica 2개 이상, PDB | ingress 5xx rate |
| 인증 우회 | 경로 규칙 누락 | default backend 차단, WAF | 401/403 로그 |

> 요약: 접근 계층 리스크는 selector, Controller 가용성, L7 정책 누락으로 발생함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | ingress p95 100ms 이하 | ingress metric |
| 오류율 | 5xx 0.1% 이하 | access log, APM |
| 인증/암호화 | TLS 1.2 이상, 인증 우회 0건 | scanner, audit |

> 요약: Service/Ingress 운영은 지연, 오류율, TLS와 인증 지표로 검증함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 내부 통신: ClusterIP와 CoreDNS를 기본으로 사용하고 selector/label 표준으로 endpoint 누락을 방지
2. 외부 진입: HTTP 서비스는 Ingress Controller 2개 이상 replica와 TLS 1.2 이상 인증서를 적용
3. 운영 통제: ingress 5xx rate, p95 latency, endpoints 0건 알림을 SLO dashboard에 등록

**결론 (2줄):**
- 기술사 판단: 내부 L4 접근은 Service, 외부 L7 라우팅은 Ingress로 분리 설계해야 함
- 향후 방향: Gateway API가 역할 기반 라우팅과 다중 테넌트 정책으로 Ingress 기능을 세분화함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Service와 Ingress를 설명하시오" | Service DNS, endpoint, Ingress routing 흐름 | L4/L7 역할 차이 |
| 요구사항 명시형 | "외부 노출 방안을 설계하시오", "비교하시오" | TLS, host/path, Controller 흐름 | NodePort, LoadBalancer, Ingress 선택 기준 |

> 요약: 설명형은 접근 흐름, 설계형은 노출 범위와 L7 정책 중심으로 전환함.
