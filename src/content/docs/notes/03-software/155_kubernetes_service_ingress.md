---
sidebar:
  order: 155
  label: "155. 쿠버네티스 서비스•인그레스"
  badge:
    text: "기출 · 70%"
    variant: note
title: "쿠버네티스 서비스•인그레스 (Kubernetes Service Ingress)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 155
extra:
  question_no: "155"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "서비스 노출과 경로 제어가 최근 설계축임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Service (L4)**: 동적으로 변하는 파드 집합에 고정 가상 IP(VIP)와 CoreDNS 이름을 부여하여 L4 로드밸런싱과 서비스 디스커버리를 제공.
- **Ingress (L7)**: 외부 HTTP/HTTPS 트래픽을 단일 진입점에서 받아 Host 및 URL Path 기반으로 백엔드 Service로 분기하는 L7 게이트웨이.

</details>

- 정의/개념: 동적으로 변하는 파드 IP를 추상화하여 단일 진입 VIP를 제공하는 Service(L4)와 경로 기반 라우팅 및 TLS를 제공하는 Ingress(L7) 네트워킹 아키텍처
- 배경/필요성: 파드 IP의 잦은 변경에 따른 호출 실패 및 서비스 디스커버리 붕괴, 개별 서비스마다 로드밸런서 생성 시의 인프라 비용 폭증 한계

#### 한줄 요약
- L4 가상 IP(Service)와 L7 경로 분기(Ingress)를 결합하여 안정적인 마이크로서비스 네트워킹을 구현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ClusterIP / NodePort / LoadBalancer**: 클러스터 내부 전용(ClusterIP), 노드 포트 개방(NodePort), 외부 클라우드 ELB 연동(LoadBalancer).
- **TLS Termination**: Ingress 계층에서 HTTPS 암호화를 일괄 해제하여 백엔드 파드의 연산 부하를 덜어주는 기능.

</details>

- 파드가 교체되어도 변하지 않는 안정적인 내부 가상 IP(VIP) 및 CoreDNS 도메인 제공
- 단일 IP/로드밸런서 뒤에서 복수의 마이크로서비스로 분기하는 L7 URL 경로 기반 라우팅
- cert-manager 기반의 SSL/TLS 인증서 자동 발급 및 갱신(TLS Termination)

#### 한줄 요약
- 고정 가상 IP 로드밸런싱과 L7 호스트/경로 기반 프록시로 마이크로서비스 트래픽을 제어한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **인그레스 및 서비스 계층**: Ingress Controller(L7 TLS/Path), Service VIP(kube-proxy iptables/IPVS), Endpoints(실제 Pod IP 목록).

</details>

```text
[쿠버네티스 서비스·인그레스 구성]
|-- 인그레스 컨트롤러
|-- 쿠버네티스 서비스
|-- 엔드포인트슬라이스
`-- kube-proxy
```

선의 의미: 계층 및 외부 HTTPS 요청이 Ingress Controller(L7)에서 경로 매핑 후 Service(L4)와 Endpoints를 거쳐 파드로 전달되는 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 인그레스 컨트롤러 (Ingress) | 외부 HTTP/HTTPS 트래픽을 접수하여 TLS 복호화 및 도메인/URL 경로별 분기 라우팅 | NGINX, AWS ALB |
| 쿠버네티스 서비스 (Service) | 파드 집합에 고정 가상 IP(VIP)를 부여하고 내부 CoreDNS 질의를 지원(L4) | ClusterIP, NodePort |
| 엔드포인트슬라이스 | Readiness Probe를 통과한 유효한 백엔드 파드들의 실제 IP/Port 목록 실시간 관리| EndpointSlice |
| kube-proxy (L4 프록시) | 노드의 커널 iptables 또는 IPVS 규칙을 갱신하여 Service VIP 트래픽을 파드로 부하분산| 커널 레벨 L4 분산 |

#### 한줄 요약
- 인그레스가 L7 이름·경로 해석을, 서비스와 kube-proxy가 L4 주소 추상화를 대신 떠맡으므로 파드는 자신의 IP가 언제 바뀌는지 모르는 채로 트래픽을 받는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **인그레스 트래픽 라우팅 5단계**: HTTPS 요청 수신 $\to$ TLS 복호화 $\to$ URL Path 룰 매칭 $\to$ Service/Endpoints IP 선택 $\to$ 파드 수신.

</details>

```text
외부 사용자의 서비스 접근 요청 (HTTPS)
        │
   [HTTPS 도메인 요청 수신] 사용자가 `https://api.com/order` URL로 Ingress ALB에 접속
        │
   [TLS 복호화] Ingress Controller가 보유한 TLS 인증서(Secret)로 HTTPS 암호화 해제
        │
   [URL Path 룰 매칭] Ingress 규칙을 대조하여 `/order` 경로에 지정된 `order-service` 선정
        │
   [Pod IP 선정] EndpointSlice에서 정상 작동 중인 백엔드 파드 IP(`10.244.1.5`)를 IPVS로 선택
        │
   선택된 백엔드 파드 컨테이너의 8080 포트로 평문 HTTP 요청 즉시 프록시 전달
```

#### 한줄 요약
- TLS 복호화와 경로 매칭 비용은 인그레스 한 지점에서 한 번만 치르고 이후 구간은 커널 레벨 L4 전달로 끝나므로, 암호화 연산이 백엔드 파드 수만큼 반복되지 않는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Service(L4) vs Ingress(L7)**: L4 전송 계층 패킷 전달(Service)과 L7 응용 계층 호스트/경로 라우팅(Ingress).

</details>

| 비교 항목 | 쿠버네티스 서비스 (Service: L4) | 쿠버네티스 인그레스 (Ingress: L7) |
|:---|:---|:---|
| OSI 계층 | 4계층 전송 계층 (L4 TCP/UDP) | 7계층 응용 계층 (L7 HTTP/HTTPS) |
| 핵심 라우팅 기준 | 고정 가상 IP (VIP) 및 포트 번호 | 도메인 호스트명(Host) 및 URL 경로(Path) |
| 주요 부가 기능 | 내부 서비스 탐색(CoreDNS), L4 분산 | TLS Termination, 쿠키 기반 세션 고정, Rewrite|
| 최적 적용 대상 | 클러스터 내부 마이크로서비스 간 통신 | 대외 단일 진입점 도메인 및 웹/앱 트래픽 통합 |

#### 한줄 요약
- 내부 통신과 L4 로드밸런싱은 Service, 외부 웹 도메인 통합과 L7 라우팅은 Ingress를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Target-Type IP**: NodePort를 거치는 불필요한 네트워크 점프(Hop)를 생략하고 ALB가 VPC CNI 파드 IP로 직접 트래픽을 쏘아주는 최적화.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NodePort 경유로 인한 2단계 네트워크 점프 및 지연시간 증가 | AWS ALB Ingress의 `target-type: ip` 설정으로 파드 직접 연결 | 네트워크 홉 제거 및 응답 지연 50% 단축 |
| 마이크로서비스마다 LoadBalancer 생성 시 클라우드 비용 폭증 | 단일 Ingress Controller로 통합하고 Host/Path 기반 분기 | 클라우드 로드밸런서 비용 80% 이상 절감 |
| SSL/TLS 인증서 갱신 누락으로 인한 서비스 접속 불가 사고 | `cert-manager` 도입 및 Let's Encrypt 자동 갱신 파이프라인 구축 | 인증서 만료 장애 0건 보장 |
| Ingress 갱신 시 iptables 수만 개 규칙으로 인한 성능 저하 | kube-proxy 모드를 `iptables`에서 `IPVS` 모드로 전환 운영 | 대규모 클러스터 패킷 처리 성능 10배 향상 |

#### 한줄 요약
- 네 대책은 모두 홉·로드밸런서·규칙 수라는 중복 비용을 한 지점으로 접어 얻은 이득이며, 그 대가로 인그레스가 트래픽과 장애가 집중되는 단일 지점이 된다.

## Ⅶ. 결론

- 클라우드 네이티브 마이크로서비스(MSA) 네트워킹 및 외부 트래픽 유입 제어의 핵심 표준 라우팅 아키텍처로 정립되었으며, 실무 구축 시에는 불필요한 네트워크 홉(Hop)을 제거하는 AWS ALB `target-type: ip` 직접 라우팅, 대규모 파드 환경에서 iptables 부하를 극복하는 IPVS/eBPF(Cilium) 기반 kube-proxy 가속, Let's Encrypt 인증서 생명주기를 자동화하는 cert-manager 연동 및 차세대 Gateway API로의 점진적 진화를 결합하여 고성능 통신과 보안 거버넌스를 완벽히 보증

#### 한줄 요약
- 쿠버네티스 서비스와 인그레스는 L4 가상 IP 로드밸런싱과 L7 경로 기반 라우팅을 결합하여 컨테이너 트래픽을 무결점으로 제어하는 핵심 네트워킹 기술이다.
