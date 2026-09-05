---
sidebar:
  order: 62
  label: "062. 쿠버네티스 네트워킹 - CNI•Ingress"
  badge:
    text: "기출 · 50%"
    variant: note
title: "쿠버네티스 컨테이너 네트워킹 : CNI•Service•Ingress"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-network"
weight: 62
extra:
  question_no: "62"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "CNI 플러그인(Calico, Cilium), Service VIP(kube-proxy/eBPF), Ingress 및 Gateway API"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **K8s Flat Network**: 모든 파드(Pod)가 NAT 없이 고유 IP를 할당받아 클러스터 전역에서 1:1 직접 통신하는 평면 네트워크 모델.
- **CNI (Container Network Interface)**: Kubelet이 파드 생성/삭제 시 veth 페어를 생성하고 IPAM으로 IP를 할당하는 표준 플러그인 규격.

</details>

- 정의/개념: 파드 간 무손실 직접 통신을 위한 CNI, Service VIP 가상 로드밸런서, Ingress L7 게이트웨이, NetworkPolicy를 아우르는 컨테이너 네트워킹 아키텍처
- 배경/필요성: 전통적인 단일 호스트 도커(Docker) 브리지 네트워크 환경에서는 컨테이너마다 호스트 포트를 수동 매핑(Port Mapping)함에 따른 포트 충돌, 컨테이너 동적 생성/소멸 시 IP 변동에 따른 서비스 디스커버리 단절, 수천 개 이상의 컨테이너가 분산된 멀티 노드 클러스터 간의 안전한 L3/L4/L7 라우팅 및 격리(Multi-Tenancy)가 불가능한 한계를 극복하기 위해, 모든 파드(Pod)에 NAT 없는 고유 IP를 부여하는 평면 네트워크 모델(Flat Network)과 플러그인 인터페이스(**CNI**: Container Network Interface), 영속적 고정 VIP 기반 서비스 로드밸런싱(Service/EndpointSlice) 및 L7 트래픽 라우팅 표준(Ingress/Gateway API)을 집대성한 쿠버네티스 네트워킹 아키텍처를 도입하여 호스트 포트 충돌 없는 직접 파드 통신, 동적 서비스 디스커버리 및 제로 트러스트(NetworkPolicy) 기반 네트워크 격리를 달성할 필요

#### 한줄 요약
- NAT 없는 평면 통신, Service VIP 기반 로드밸런싱, eBPF 커널 가속 및 NetworkPolicy 격리를 지원한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Service VIP & EndpointSlice**: 파드 집합에 고정 VIP를 부여하고 실시간 정상 파드 목록(EndpointSlice)으로 부하를 분산하는 가상 추상화 계층.
- **eBPF Kernel Acceleration (Cilium)**: iptables의 $O(N)$ 순차 룩업 병목을 극복하고 리눅스 커널 BPF 맵을 통해 $O(1)$ 초고속 패킷 포워딩을 수행하는 기술.

</details>

- NAT 없는 평면 네트워크(IP-per-Pod): 모든 파드가 고유 IP를 보유하여 포트 변환 없이 전 노드 파드 간 직접 통신
- 서비스 디스커버리 및 가상 로드밸런싱: CoreDNS와 연계하여 서비스 이름을 VIP로 해석하고 백엔드 파드로 부하 분산
- 커널 레벨 eBPF 가속 (**Cilium** CNI): iptables의 병목을 제거하고 eBPF 맵을 통한 $O(1)$ 초고속 커널 패킷 포워딩 실현

#### 한줄 요약
- NAT 없는 평면 통신, Service VIP 기반 로드밸런싱, eBPF 커널 가속 및 NetworkPolicy 제로 트러스트 격리를 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Gateway API**: 기존 Ingress의 어노테이션 파편화를 극복하고 인프라 관리자(Gateway)와 앱 개발자(HTTPRoute)의 책임을 명확히 분리한 차세대 표준.

</details>

```text
[쿠버네티스 다계층 네트워킹 및 트래픽 라우팅 아키텍처]
|-- Ingress·Gateway API (L7 진입)
|-- Service (고정 VIP·EndpointSlice)
|-- NetworkPolicy (통신 인가)
|-- CNI 플러그인 (파드 연결·IPAM)
`-- eBPF 커널 엔진 (서비스 포워딩)
```

선의 의미: 계층 및 외부 트래픽이 Ingress에서 L7 라우팅된 후 Service VIP를 거쳐 NetworkPolicy 검증을 통과하고 CNI 패브릭을 통해 파드로 전달되는 구조

| 구성요소 | 책임 |
|:---|:---|
| Ingress·**Gateway API** | TLS 종단과 **L7 경로 라우팅** |
| Service | 고정 VIP와 EndpointSlice 부하 분산 |
| NetworkPolicy | 레이블 기반 **인그레스·이그레스 인가** |
| CNI 플러그인 | veth·IPAM과 **노드 간 라우팅** |
| eBPF 커널 엔진 | iptables 대체와 **고속 포워딩** |

#### 한줄 요약
- Service VIP가 수시로 바뀌는 파드 IP 앞의 고정 주소 계층을 맡고 eBPF가 커널 경로에서 iptables 규칙 선형 순회를 대신하므로, 파드 수 증가 비용이 데이터 평면으로 전가되지 않는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **EndpointSlice**: 대규모 클러스터에서 etcd 부하를 줄이기 위해 정상 상태(Readiness Probe 통과)의 파드 IP/포트 목록을 분할 관리하는 리소스.

</details>

```text
쿠버네티스 외부 요청 인입 및 파드 전달 파이프라인
        │
   [외부 요청 인입] 외부 클라이언트가 도메인 주소로 Ingress 공인 VIP에 HTTPS 요청 전송
        │
   [Ingress L7 라우팅] Ingress Controller가 TLS 복호화 및 Host/Path 분석 후 대상 Service 매핑
        │
   [EndpointSlice 조회] Service가 Readiness Probe를 통과한 정상 파드(Pod IP) 목록 조회
        │
   [eBPF / IPVS 부하 분산] 커널 eBPF 맵이 Service ClusterIP를 목적지 Pod IP로 고속 DNAT 변환
        │
   ▼
[CNI 전달 및 수신] NetworkPolicy 검증을 거쳐 노드 내부 veth 인터페이스를 통해 파드 소켓으로 전달
```

#### 한줄 요약
- L7까지 열어 경로를 고르는 비용은 진입점에서 요청당 한 번만 치르고 그 뒤는 커널 eBPF 변환만 남으므로, 판단은 Ingress에 몰고 전달은 커널에 맡기는 배치가 된다.

## Ⅴ. 종류 및 비교


| 비교 항목 | Flannel CNI (기본형) | Calico CNI (보안/BGP) | Cilium CNI (차세대 eBPF) |
|:---|:---|:---|:---|
| 데이터 평면 기술 | Linux Bridge / VXLAN 오버레이 | iptables / Linux Routing (BGP) | eBPF (Extended BPF 커널 가속) |
| NetworkPolicy 지원 | **미지원 (보안 격리 불가)** | 지원 (강력한 L3~L4 방화벽) | 지원 (L3~L7 API 단위 심층 제어)|
| 성능 확장성 | 소규모 적합 (캡슐화 오버헤드)| 중대규모 적합 (BGP 네이티브) | 초대규모 고성능 ($O(1)$ BPF Map)|
| 서비스 프록시 구현 | 표준 kube-proxy (iptables) | 표준 kube-proxy / eBPF 모드 | kube-proxy 완전 대체 (eBPF) |
| 서비스 메시 통합 | 별도 사이드카 프록시 필수 | 별도 사이드카 프록시 필수 | 사이드카 없는(Sidecarless) 메시 |

#### 한줄 요약
- Flannel은 단순 오버레이, Calico는 BGP/NetworkPolicy, Cilium은 eBPF 기반 고성능/L7 보안 CNI이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NodeLocal DNSCache**: 각 노드에 캐시 데몬셋을 배포하여 CoreDNS 질의 폭증 및 conntrack 테이블 고갈로 인한 5초 지연을 방지하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 컨테이너 부팅 중 미준비 상태에서 트래픽 유입으로 503 오류 발생 | Readiness Probe(준비성 검사) 및 initialDelay 정밀 구성 | 미준비 파드 트래픽 유입 차단 및 무중단 배포 보증 |
| 대규모 클러스터에서 수만 개 파드 생성 시 iptables 룩업 CPU 과부하 | iptables를 전면 배제하고 eBPF 기반 Cilium CNI 도입 | 룰 개수 무관 $O(1)$ 초고속 포워딩 및 CPU 70% 절감 |
| CoreDNS 질의 폭증 및 conntrack 경합으로 인한 **간헐적 5초 DNS 지연** | 각 노드에 **NodeLocal DNSCache** 데몬셋 배포 및 TCP 활성화 | DNS 응답 1ms 단축 및 conntrack 테이블 고갈 방지 |
| 기본 설정 시 모든 파드 간 통신이 허용되어 횡적 침투 위협 | 네임스페이스별 Default-Deny NetworkPolicy 선제 적용 | 비인가 파드 간 통신 원천 차단 및 제로 트러스트 달성 |

#### 한줄 요약
- Readiness Probe, Cilium eBPF, NodeLocal DNSCache, Default-Deny 정책으로 운영한다.

## Ⅶ. 결론

- 모놀리식에서 마이크로서비스 아키텍처(MSA)로 전환된 현대 클라우드 네이티브 생태계의 가장 핵심적인 분산 애플리케이션 연결 및 통신 기반 구조로 확립되었으며, 기존 iptables 기반 kube-proxy의 성능 병목을 극복하고 사이드카 없는(Sidecarless) 서비스 메시를 실현하는 Cilium eBPF CNI 및 Ingress를 고도화한 Gateway API로 진화하는 가운데, 실무 프로덕션 클러스터 운영 시에는 대규모 노드에서의 $O(1)$ 초고속 패킷 처리를 위한 eBPF CNI 채택, 간헐적 5초 DNS 지연을 원천 방지하는 NodeLocal DNSCache 구성, 비인가 파드 횡적 이동을 차단하는 Default-Deny NetworkPolicy 선제 적용, 무중단 파드 롤링 업데이트를 위한 Readiness Probe 헬스체크 정밀 튜닝을 결합하여 완벽한 쿠버네티스 네트워킹 가용성과 보안성을 완성

#### 한줄 요약
- 쿠버네티스 네트워킹은 CNI, Service, Gateway API 및 eBPF 가속을 결합하여 고성능 컨테이너 통신을 실현하는 핵심 클라우드 인프라다.
