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
- **개요**: Service는 Pod 집합에 고정 접근점을 제공하고, Ingress는 HTTP/HTTPS 외부 진입과 라우팅을 제공하는 계층
- **왜 필요한가**: Pod IP는 생성과 삭제 때 바뀌므로 클라이언트가 Pod를 직접 호출하면 장애 복구와 배포 때 연결이 깨진다.
- **핵심 직관**: Service는 내부 대표 전화번호, Ingress는 외부 안내 데스크와 URL 라우팅 규칙이다.

## 깊이 이해
- **배경·문제의식**: Deployment가 Pod를 교체하면 Pod IP와 개수가 계속 변한다. Kubernetes는 selector로 Ready Pod를 endpoint에 묶고, Service IP 또는 DNS로 접근을 추상화한다.
- **작동 원리**: Service는 label selector로 endpoint slice를 만들고 kube-proxy 또는 eBPF data plane이 트래픽을 Pod로 전달한다. Ingress Controller는 host/path 규칙을 읽어 L7 라우팅, TLS 종료, 인증 연동을 수행한다.
- **비유**: 팀원이 바뀌어도 대표 번호로 전화하면 현재 근무자에게 연결되는 구조와 같다. Ingress는 건물 입구에서 회사명과 부서명으로 방문자를 안내한다.
- **구체 예시**: `api.example.com/v1` 요청은 Ingress Controller에서 TLS 종료 후 `api-service:80`으로 전달되고, Service는 Ready Pod 3개 중 하나로 로드밸런싱한다.
- **흔한 오해·주의점**: Ingress 자체는 컨트롤러가 아니다. NGINX, HAProxy, cloud ALB 같은 Ingress Controller가 있어야 규칙이 실제 트래픽 경로가 된다.

## 연결 개념
- EndpointSlice - Service가 선택한 Pod 접속 목록
- kube-proxy/eBPF - Service 트래픽 전달 데이터 경로
- Gateway API - Ingress보다 세분화된 L4/L7 라우팅 표준

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

Service와 Ingress는 Pod 접근 추상화 계층임. Pod는 생성과 삭제에 따라 IP가 바뀌므로 고정 접속점이 필요하다. Service는 내부 L4 접근을, Ingress는 외부 HTTP/HTTPS 라우팅을 담당한다.

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
