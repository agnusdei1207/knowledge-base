---
sidebar:
  order: 62
  label: "062. 쿠버네티스 네트워킹 - CNI•Ingress (Kubernetes Networking)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "쿠버네티스 네트워킹 - CNI•Ingress (Kubernetes Networking)"
date: "2026-08-13T16:20:00+09:00"
tags:
  - "notes-network"
weight: 62
extra:
  question_no: "062"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "설계형: 137회 CNI•Ingress•Policy 장문"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **쿠버네티스 네트워킹(Kubernetes Networking)**: 파드(Pod) 간 직접 통신, 서비스 발견, 인그레스 노출, 보안 정책을 제공하는 가상 네트워크 모델.
- **쿠버네티스(Kubernetes, K8s)**: 컨테이너 자동 배포, 스케일링, 복구를 관리하는 오픈소스 오케스트레이션 플랫폼.
- **인터넷 프로토콜(Internet Protocol, IP)**: 패킷의 논리적 주소 지정과 3계층 라우팅을 담당하는 프로토콜.
- **파드(Pod)**: 하나 이상의 컨테이너가 리눅스 네트워크 네임스페이스와 IP를 공유하는 최소 배포 단위.
- **CNI(Container Network Interface)**: 파드 생성 시 인터페이스 생성, IP 할당, 라우팅 테이블 구성을 담당하는 플러그인 표준.
- **서비스(Service)**: 동적 파드 집합 전면에 고정 가상 IP(ClusterIP) 및 DNS를 제공하는 L4 로드밸런싱 객체.
- **인그레스(Ingress)**: 외부 HTTP/HTTPS 트래픽의 서비스 라우팅 규칙을 선언하는 API 객체.

</details>

- **개념**: **쿠버네티스 네트워킹**은 모든 **파드(Pod)**가 NAT 없이 1:1 통신 가능한 IP를 보유하도록 **CNI**로 구성, **서비스(Service)**와 **인그레스(Ingress)**로 가상 IP 로드밸런싱과 외부 L7 경로를 제공하는 체계.
- **필요성**: 파드 IP 유동성에 따른 고정 접근점 제공과 오버레이/언더레이 L2/L3 통신 격리 및 보안 정책 수립 필수.

#### 한줄 요약
- CNI 및 가상 IP 기반 파드 동적 생명주기 관리와 인그레스 트래픽 수용 네트워킹 아키텍처 적용.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **가상 IP(Virtual IP, VIP)**: 프록시(kube-proxy/eBPF)가 제어하며 파드 종단으로 분산되는 고정 대표 IP.
- **준비 상태(Readiness Probe)**: 파드 내부 통신 가능 여부를 진단하여 서비스 로드밸런싱 엔드포인트 등록을 결정하는 지표.

</details>

- 모든 파드는 고유 **IP**를 할당받아 포트 충돌 없이 1:1 직접 통신 수행.
- **서비스**는 **가상 IP(VIP)**를 부여하여 **준비 상태(Readiness)**인 파드로 자동 로드밸런싱.
- **인그레스**는 L7에서 TLS 종단(Termination), 호스팅, 경로 기반 라우팅을 일관 실행.

#### 한줄 요약
- CNI 기반 Flat IP 모델과 VIP 서비스, L7 인그레스 라우팅으로 서비스 연속성을 확보하는 기본 원칙 준수.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **엔드포인트슬라이스(EndpointSlice)**: 파드의 IP•포트•준비 상태 정보를 단위별 분할 관리하여 대규모 클러스터 성능을 향상하는 개체.
- **네트워크 정책(NetworkPolicy)**: 파드 라벨(Label) 기반 Ingress/Egress 트래픽을 허용/차단하여 Zero-Trust를 구현하는 보안 객체.
- **TLS(Transport Layer Security)**: 외부 사용자 및 인그레스 게이트웨이 간 패킷 암호화 및 인증을 수행하는 프로토콜.
- **eBPF(extended Berkeley Packet Filter)**: 리눅스 커널 이벤트 영역에서 iptables 오버헤드 없이 고성능 라우팅 및 정책을 실행하는 기술.

</details>

- **EndpointSlice**는 파드 Scale-Out 시 API 서버와 프록시 간 데이터를 최적화하고, **NetworkPolicy**는 L3/L4 격리 정책을 선언.
- 고성능 CNI는 **eBPF** 엔진으로 iptables 병목 없이 바이패스 포워딩을 수행하며, 인그레스는 **TLS** 암호화를 지원.

```text
쿠버네티스 네트워킹 아키텍처
├─ 인그레스 컨트롤러
├─ 서비스 탐색 계층
│  ├─ 서비스(Service)
│  └─ EndpointSlice
└─ 파드 데이터 경로 및 보안
   ├─ NetworkPolicy
   └─ CNI Data Path
```

| 구성요소 | 역할 및 핵심 기능 |
|:---|:---|
| **인그레스 컨트롤러** | 외부 L7 라우팅 및 TLS Termination 실행 |
| **서비스(Service)** | 고정 VIP 제공 및 로드밸런싱 |
| **EndpointSlice** | 준비 상태의 Pod IP/Port 매핑 정보를 분할 수용 |
| **NetworkPolicy** | Pod Label 기반 트래픽 L3/L4 접근제어 |
| **CNI Data Path** | eBPF/iptables 기반 터널링 및 커널 패킷 포워딩 |

#### 한줄 요약
- Ingress, EndpointSlice, eBPF 기반 고성능 클라우드 네이티브 네트워크 아키텍처 구현 필수.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **데이터 경로(Data Path)**: 패킷이 파드 간/외부 통신 시 eBPF/iptables를 거치는 경로.
- **kube-proxy**: 서비스 VIP 요청을 탐지하여 파드로 라우팅 규칙을 갱신하는 데몬.
- **API 서버(kube-apiserver)**: 클러스터 상태 변경 요청 검증 및 etcd 수용 컨트롤 플레인.
- **Ingress 통지**: 인그레스 설정 변경을 인그레스 컨트롤러로 알리는 단계.
- **외부 경로 설치**: 프록시에 L7 가상 호스트 구성을 동적 반영하는 단계.
- **EndpointSlice/정책 통지**: 파드 상태 및 보안 정책 업데이트 이벤트를 감지하는 단계.
- **종단/정책 규칙 설치**: eBPF 맵 또는 iptables에 룰셋을 적용하는 단계.
- **종단 전달**: 정책 검사를 통과한 요청을 파드로 포워딩하는 단계.

</details>

```text
1. Ingress 통지
        │
        ▼
2. 외부 경로 설치
        │
        ▼
3. EndpointSlice/정책 통지
        │
        ▼
4. 종단/정책 규칙 설치
        │
        ▼
외부 웹 트래픽 요청 진입
        │
        ▼
정책 검사 및 준비 상태 점검
        ├─ [비정상] 차단/503 오류
        └─ [정상] 5. 파드 전달
```

### 동작 원리

1. **Ingress 통지**: 규칙 생성 시 **API 서버**가 이벤트를 감지하여 컨트롤러에 전달.
2. **경로 설치**: 컨트롤러가 내부 라우팅 테이블 및 **TLS**를 갱신.
3. **EndpointSlice/정책 통지**: 파드 변동과 정책을 CNI 데몬에 전달.
4. **규칙 설치**: CNI 데몬이 커널 **eBPF** 맵이나 iptables에 규칙 반영.
5. **종단 전달**: 요청 진입 시 L7 라우팅 및 보안 검사를 통과한 요청을 최종 **파드**로 전달.

#### 한줄 요약
- Control Plane 관측 기반 프록시 및 eBPF 맵 동적 업데이트 프로세스 준수.
## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **게이트웨이 응용 프로그래밍 인터페이스(Gateway Application Programming Interface, Gateway API)**: 역할(Role-oriented) 기반 구조로 L4/L7 라우팅을 유연하게 선언하는 차세대 K8s 네트워크 표준 API.

</details>

| 비교 항목 | Ingress API | Gateway API (차세대 K8s 표준) |
|:---|:---|:---|
| **적용 목적** | 단일 팀 환경의 단순 HTTP/HTTPS 웹 서비스 외부 노출 | 멀티 테넌트, 다중 팀(인프라/개발) 역할 분리 및 L4~L7 고급 라우팅 |
| **리소스 모델** | 단일 Ingress 리소스 내 모든 규칙 기술 | GatewayClass, Gateway, HTTPRoute, TLSRoute 등 역할별 객체 분리 |
| **지원 프로토콜** | HTTP, HTTPS 중심 (L7) | HTTP, HTTPS, gRPC, TCP, UDP (L4~L7 통합 지원) |
| **트래픽 제어** | 벤더 전용 주석(Annotation) 의존 | 가중치 기반 트래픽 분할(Splitting), 헤더 수정 표준 지원 |
| **주요 한계** | 벤더 간 주석 호환성 부재, 복잡한 정책 표현 한계 | 초기 학습 곡선 존재, CNI/컨트롤러의 Gateway API 지원 확인 필요 |

> 요약: 단순 웹 애플리케이션 외부 노출에는 **Ingress**, 대규모 조직의 역할 분리 및 gRPC/L4 다중 트래픽 제어에는 **Gateway API** 적용.

#### 한줄 요약
- 단순 인그레스와 역할 기반 L4~L7 확장성을 제공하는 Gateway API 비교 모델 수용.
## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **서비스 불가(Service Unavailable, HTTP 503)**: 백엔드 파드가 준비 상태를 달성하지 못했거나 Endpoint가 비어있을 때 프록시가 클라이언트에 반환하는 에러 응답 코드.

</details>

| 실무 문제점 | 발생 원인 | 해결 대책 | 기대 효과 |
|:---|:---|:---|:---|
| **보안 정책 미작동** | NetworkPolicy 적용 시 미지원 CNI(Flannel 등) 사용 | Calico, Cilium 등 **NetworkPolicy** 지원 **CNI** 선택 및 eBPF 검증 | 파드 간 무단 통신 차단 및 Zero-Trust 보안 격리 달성 |
| **503 에러 발생** | 파드 생성 직후 Readiness Probe 설정 누락으로 미준비 파드에 요청 전송 | 적절한 **Readiness Probe** 딜레이 설정 및 **EndpointSlice** 동기화 | 트래픽 핑퐁 및 서비스 503 오류 발생 방지 |
| **Ingress 설정 혼선** | 단일 Ingress 파일에 개발팀과 인프라팀 설정이 뒤섞여 충돌 발생 | **Gateway API** 도입을 통한 역할별(Gateway/HTTPRoute) 권한 분리 | 운영 조직 간 변경 간섭 제거 및 유연한 라우팅 제어 |
| **대규모 커널 병목** | 파드 증가에 따른 iptables 규칙 탐색 부하 | **eBPF** 기반 CNI 적용 가능성 검증 | 커널 패킷 처리 지연 완화 |

#### 한줄 요약
- eBPF 기반 보안 검증과 Readiness Probe 최적화, Gateway API 도입을 통한 실무 운영성 확보 체계 구축.
## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **외부 경로 선택(External Routing Model Selection)**: 조직의 가용 역량과 라우팅 복잡도에 따라 Ingress 또는 Gateway API 모델을 체계적으로 결정하는 설계 원칙.

</details>

- **외부 경로 선택** 시 단순 L7은 **Ingress**, 멀티테넌트 및 gRPC 제어에는 **Gateway API**를 표준 채택하고, **eBPF** CNI를 연동하여 보안과 데이터 패스 성능을 확보하는 체계 적용.

#### 한줄 요약
- eBPF 기반 CNI 패스트 패스 및 Gateway API 적용 차세대 네트워킹 구축 체계 적용.
