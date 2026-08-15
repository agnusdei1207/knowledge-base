---
sidebar:
  order: 156
  label: "156. 쿠버네티스 NetworkPolicy•CNI (Kubernetes NetworkPolicy CNI)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "쿠버네티스 NetworkPolicy•CNI (Kubernetes NetworkPolicy CNI)"
date: "2026-08-14T02:16:00+09:00"
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

<details><summary>용어 설명</summary>

- **CNI(Container Network Interface)**: 파드(Pod) 간 IP 할당 및 네트워크(VXLAN 등) 통신을 가능하게 하는 네트워크 드라이버 표준 인터페이스(Calico, Cilium, AWS VPC CNI).
- **네트워크 정책(NetworkPolicy)**: 파드 간 통신을 L3/L4 계층에서 IP 및 포트(Port) 단위로 차단하거나 허용하는 미세 격리(Micro-segmentation) 객체.
- **제로 트러스트 보안(Zero-Trust Security)**: 기본적으로 모든 파드 통신을 차단(Default Deny)하고, 승인된 허용(Allow) 규칙만 적용하는 보안 모델.

</details>

- 정의/개념: Pod 연결과 통신 정책을 분리하는 **CNI•NetworkPolicy**
- 배경/필요성: Flat Pod Network는 침해 후 **Lateral Movement** 허용

#### 한줄 요약

- CNI가 모든 파드 사이에 길을 놓은 뒤 네트워크 정책가 출발지와 도착지의 허용 목록을 적용해 필요한 통신만 남긴다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **eBPF (Extended Berkeley Packet Filter)**: Linux 커널 레벨에서 iptables 오버헤드 없이 초고속 패킷 필터링 및 NetworkPolicy 방화벽을 처리하는 Cilium CNI 핵심 기술.

</details>

- **CNI**: Pod IP 할당 및 오버레이 네트워크 터널링(Calico, Cilium, AWS CNI).
- **NetworkPolicy**: L3/L4 인그레스(Ingress) 및 이그레스(Egress) 트래픽 격리 규칙 집행.
- **기본 거부 정책(Default Deny All)**: 전체 트래픽 차단 후 핀포인트 허용 규칙(Allow Rule)을 통한 통신 제한.

#### 한줄 요약

- 정책 객체만 작성하고 CNI가 그 기능을 집행하지 않으면 문서상의 출입 명단만 있고 실제 문에는 잠금장치가 없는 상태가 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Cilium (eBPF CNI)**: iptables 대신 리눅스 커널 eBPF 바이패스로 초고속 성능 및 L7 (HTTP/gRPC) 방화벽까지 지원하는 대표 CNI.

</details>

```text
[NetworkPolicy 객체] ─── [정책 제어기]
                              │
[CNI Runtime] ────────── [Data Plane]
      │                       │
   [Pod 주소]              [통신 집행]
```

| 구성요소 | 책임 |
|---|---|
| NetworkPolicy 객체 | Selector•Port 기반 **허용 의도** 선언 |
| 정책 제어기 | 정책을 읽어 **집행 규칙**으로 변환 |
| CNI Runtime | Pod의 **Network Namespace•주소** 구성 |
| Data Plane | Packet 경로에서 **Ingress•Egress** 집행 |

#### 한줄 요약

- 런타임과 CNI가 파드에 주소와 경로를 만들면 정책 제어기가 선택자 규칙을 실제 패킷 검사 지점에 배포한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Default Deny All Ingress**: Namespace 내부의 모든 Pod 유입 트래픽을 일단 100% 차단하는 보안 첫걸음 YAML 패턴.

</details>

```text
[Pod 통신 요청]
      │
      ▼
1. Source•Destination 식별
      │
      ▼
2. Pod•Namespace Selector 대조
      │
      ▼
3. Ingress•Egress Rule 평가
      │
      ▼
4. Protocol•Port 확인
      │
      ▼
5. Packet 허용•차단
      │
      ▼
[통신 결과 반환]
```

### 동작 원리

1. **Source•Destination 식별**: 양쪽 Pod와 Namespace 확인
2. **Pod•Namespace Selector 대조**: 정책 적용 대상 판정
3. **Ingress•Egress Rule 평가**: 송신•수신 허용 조건 결합
4. **Protocol•Port 확인**: L4 범위 일치 여부 확인
5. **Packet 허용•차단**: Data Plane에서 최종 집행

#### 한줄 요약

- API 파드에서 데이터베이스 파드로 가는 요청은 송신 측 출구 규칙과 수신 측 입구 규칙을 모두 통과해야 실제 업무 처리까지 도달한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Flannel CNI**: 초창기 극도로 단순한 Overlay CNI로 NetworkPolicy 보안 기능을 전혀 지원하지 않는 단점 보유.

</details>

| 비교 항목 | Flannel CNI | Calico CNI | Cilium CNI (eBPF) |
|:---|:---|:---|:---|
| **네트워크 기술** | VXLAN / UDP Overlay | BGP / VXLAN | **eBPF (Kernel Layer)** |
| **NetworkPolicy** | 별도 정책 Engine 필요 | **L3/L4 정책** 지원 | 표준 정책과 확장 정책 지원 |
| **Data Plane** | 단순 Overlay 중심 | iptables•eBPF 선택 가능 | **eBPF 중심** |
| **선택 기준** | 단순 연결 요구 | Routing•정책 운용 | 관측•정책 확장 요구 |

#### 한줄 요약

- CNI 장애는 주소와 경로 자체를 끊고 네트워크 정책 오류는 길이 있는 상태에서 특정 통신만 허용하거나 차단한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **AWS VPC CNI IP Exhaustion**: AWS VPC CNI 사용 시 EC2 노드당 Pod IP가 서브넷 CIDR에서 대량 고갈되는 현상.

</details>

| 3대 CNI/보안 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. AWS Subnet IP 고갈** | AWS VPC CNI가 ENI마다 Pod IP 대량 선점| **Custom Networking (Pod 전용 Secondary Subnet)**|
| **2. Rule 처리 병목** | Pod•정책 증가로 규칙 평가 비용 상승 | **규모 측정 후 eBPF Data Plane 검토**|
| **3. Policy Misconfiguration**| NetworkPolicy 오기재로 전체 서비스 불통 | **Cilium Hubble UI로 패킷 Drop 실시간 시각화** |

> 사례: **토스 / 당근마켓 / 카카오 Cilium eBPF CNI & NetworkPolicy 기반 미세 격리 보안 적용**

#### 한줄 요약

- 기본 거부를 먼저 적용한 뒤 DNS, API, DB 순서로 한 흐름씩 열어 보면 어느 정책이 업무 통신을 막았는지 즉시 찾을 수 있다.

## Ⅶ. 결론

- 단순 연결은 CNI, **Default Deny•허용 목록**은 정책 Engine 적용

#### 한줄 요약

- 통신 경로를 만든 뒤 집행 가능한 CNI와 정책 조합으로 필요한 흐름만 명시적으로 연다.
