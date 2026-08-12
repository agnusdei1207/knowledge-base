---
sidebar:
  order: 156
  label: "156. 쿠버네티스 NetworkPolicy•CNI (Kubernetes NetworkPolicy CNI)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "쿠버네티스 NetworkPolicy•CNI (Kubernetes NetworkPolicy CNI)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-software"
weight: 156
extra:
  question_no: "156"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "통신 연결과 정책 집행 구조가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **CNI (Container Network Interface)**: Pod 간 IP 할당 및 네트워크(VXLAN) 통신을 가능하게 하는 네트워크 드라이버 표준 인터페이스(Calico, Cilium, AWS VPC CNI).
- **네트워크 정책(NetworkPolicy)**: Pod 간 통신을 L3/L4 계층에서 IP 및 Port 단위로 차단/허용하는 미세 격리(Micro-segmentation) 객체.
- **제로 트러스트 보안(Zero-Trust Security)**: 기본적으로 모든 Pod 통신을 차단(Default Deny)하고, 승인된 허용(Allow) 규칙만 적용하는 보안 모델.

</details>

- 정의/개념: CNI 드라이버(Cilium, Calico)가 Pod 간 IP 통신 오버레이 망을 구성하고, NetworkPolicy가 Zero-Trust 미세 격리(Micro-segmentation) 방화벽 룰을 집행하는 아키텍처 체계인 **NetworkPolicy & CNI**
- 배경/필요성: 평면적(Flat) Pod 네트워크에서 특정 Web Pod가 해킹당했을 때, DB Pod 및 타 Namespace로 횡적 이동(Lateral Movement) 공격 파행을 차단하는 요구성

#### 한줄 요약

- CNI가 모든 파드 사이에 길을 놓은 뒤 네트워크 정책가 출발지와 도착지의 허용 목록을 적용해 필요한 통신만 남긴다.

## Ⅱ. 특징 (CNI 대 NetworkPolicy 역할 분담)

<details><summary>핵심 용어</summary>

- **eBPF (Extended Berkeley Packet Filter)**: Linux 커널 레벨에서 iptables 오버헤드 없이 초고속 패킷 필터링 및 NetworkPolicy 방화벽을 처리하는 Cilium CNI 핵심 기술.

</details>

- **CNI**: Pod IP 할당 및 오버레이 네트워크 터널링(Calico, Cilium, AWS CNI).
- **NetworkPolicy**: L3/L4 인그레스(Ingress) 및 이그레스(Egress) 트래픽 격리 규칙 집행.
- **기본 거부 정책(Default Deny All)**: 전체 트래픽 차단 후 핀포인트 허용 규칙(Allow Rule)을 통한 통신 제한.

#### 한줄 요약

- 정책 객체만 작성하고 CNI가 그 기능을 집행하지 않으면 문서상의 출입 명단만 있고 실제 문에는 잠금장치가 없는 상태가 된다.

## Ⅲ. 구조 및 구성요소 (CNI 드라이버 3대 주요 인프라 비교)

<details><summary>핵심 용어</summary>

- **Cilium (eBPF CNI)**: iptables 대신 리눅스 커널 eBPF 바이패스로 초고속 성능 및 L7 (HTTP/gRPC) 방화벽까지 지원하는 대표 CNI.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Kubernetes Network & Security Layer                  │
├────────────────────────────────────────────────────────────────────────┤
│ [Pod A (Web)] ──► [NetworkPolicy: Ingress / Egress Allow Rule]         │
│                         │ (eBPF Kernel Filtering by Cilium CNI)        │
│                         ▼                                              │
│ [CNI Overlay Network: VXLAN / AWS Secondary IP Tunneling]              │
│                         │                                              │
│                         ▼                                              │
│ [Pod B (DB)] ──► [Allowed Port 5432 Only]                              │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: NetworkPolicy 명세서가 CNI(Cilium eBPF)를 통해 리눅스 커널 패킷 레벨에서 인가된 포트(5432)만 통과시키는 구조.

| CNI 드라이버 | 네트워크 방식 | NetworkPolicy 지원 | 실무 특징 |
|:---|:---|:---|:---|
| **AWS VPC CNI** | AWS Native Secondary IP | 기본 미지원 | ENI 직결로 Latency 최적 |
| **Calico CNI** | BGP, VXLAN | 지원 (iptables) | 온프레미스 대세 도구 |
| **Cilium CNI** | eBPF (Kernel Bypass) | 최상 지원 (L3/L4/L7) | 차세대 초고속 CNI |

#### 한줄 요약

- 런타임과 CNI가 파드에 주소와 경로를 만들면 정책 제어기가 선택자 규칙을 실제 패킷 검사 지점에 배포한다.

## Ⅳ. 흐름도 (NetworkPolicy Default Deny & Allow Rule 적용 흐름)

<details><summary>핵심 용어</summary>

- **Default Deny All Ingress**: Namespace 내부의 모든 Pod 유입 트래픽을 일단 100% 차단하는 보안 첫걸음 YAML 패턴.

</details>

```text
[Default Deny All Policy Applied] ──► Web Pod ──(Port 5432 Blocked)──► DB Pod
                                           │
                                           ▼ (Apply Allow YAML: app=web -> app=db:5432)
[Traffic Allowed Only for Web-to-DB] ──────┴──────────────────────────► DB Pod (Success)
```

### 동작 원리

1. **Default Deny**: Namespace 전체에 Default Deny All Ingress YAML 적용 시 모든 Pod 간 통신 정지.
2. **Targeted Allow**: `podSelector: matchLabels: app: db` 및 `from: app: web`, `port: 5432` 핀포인트 허용 명세 추가.
3. **eBPF Enforcement**: Cilium CNI가 커널 eBPF 테이블에 등록하여 Web $\rightarrow$ DB 5432 통신만 개방 (**NetworkPolicy 완결**).

#### 한줄 요약

- API 파드에서 데이터베이스 파드로 가는 요청은 송신 측 출구 규칙과 수신 측 입구 규칙을 모두 통과해야 실제 업무 처리까지 도달한다.

## Ⅴ. 종류 및 비교 (Flannel vs Calico vs Cilium 3대 CNI 비교)

<details><summary>핵심 용어</summary>

- **Flannel CNI**: 초창기 극도로 단순한 Overlay CNI로 NetworkPolicy 보안 기능을 전혀 지원하지 않는 단점 보유.

</details>

| 비교 항목 | Flannel CNI | Calico CNI | Cilium CNI (eBPF) |
|:---|:---|:---|:---|
| **네트워크 기술** | VXLAN / UDP Overlay | BGP / VXLAN | **eBPF (Kernel Layer)** |
| **NetworkPolicy** | **미지원 (Security 0%)** | **지원 (L3/L4 iptables)** | **최상 지원 (L3/L4/L7 HTTP)** |
| **패킷 처리 성능** | 보통 | 높음 | **최상 (iptables 오버헤드 0%)** |
| **추천 배치 환경** | 테스트/로컬 K8s | 온프레미스 대규모 K8s | **클라우드 네이티브 엔터프라이즈**|

#### 한줄 요약

- CNI 장애는 주소와 경로 자체를 끊고 네트워크 정책 오류는 길이 있는 상태에서 특정 통신만 허용하거나 차단한다.

## Ⅵ. 실무 고려사항 및 대책 (NetworkPolicy & CNI 3대 실무 지침)

<details><summary>핵심 용어</summary>

- **AWS VPC CNI IP Exhaustion**: AWS VPC CNI 사용 시 EC2 노드당 Pod IP가 서브넷 CIDR에서 대량 고갈되는 현상.

</details>

| 3대 CNI/보안 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. AWS Subnet IP 고갈** | AWS VPC CNI가 ENI마다 Pod IP 대량 선점| **Custom Networking (Pod 전용 Secondary Subnet)**|
| **2. iptables Bottleneck** | Pod 1만 개 시 iptables 룰 십만 개로 CPU 과부하| **iptables 버리고 eBPF Cilium CNI 전면 교체**|
| **3. Policy Misconfiguration**| NetworkPolicy 오기재로 전체 서비스 불통 | **Cilium Hubble UI로 패킷 Drop 실시간 시각화** |

> 사례: **토스 / 당근마켓 / 카카오 Cilium eBPF CNI & NetworkPolicy 기반 미세 격리 보안 적용**

#### 한줄 요약

- 기본 거부를 먼저 적용한 뒤 DNS, API, DB 순서로 한 흐름씩 열어 보면 어느 정책이 업무 통신을 막았는지 즉시 찾을 수 있다.

## Ⅶ. 결론

- **Cilium eBPF 기반 제로 트러스트 네트워크 보안 체계 구축**
