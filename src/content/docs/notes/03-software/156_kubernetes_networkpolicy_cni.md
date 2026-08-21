---
sidebar:
  order: 156
  label: "156. 쿠버네티스 NetworkPolicy•CNI (Kubernetes NetworkPolicy CNI)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "쿠버네티스 NetworkPolicy•CNI (Kubernetes NetworkPolicy CNI)"
date: "2026-08-18T02:00:00+09:00"
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

- **CNI(Container Network Interface)**: 파드 간 고유 IP를 할당하고 오버레이(VXLAN/eBPF) 통신을 제공하는 표준 네트워크 드라이버(Calico, Cilium, AWS VPC CNI).
- **네트워크 정책(NetworkPolicy)**: 파드 간의 트래픽을 L3/L4 계층(라벨, 네임스페이스, IP/Port)에서 차단/허용하는 쿠버네티스 미세 격리(Micro-segmentation) 방화벽.

</details>

- 정의/개념: 파드 간 네트워크 연결과 IP를 할당하는 **CNI 플러그인과 L3/L4 미세 격리(Micro-segmentation)를 수행하는 NetworkPolicy** 보안 체계
- 배경/필요성: 쿠버네티스의 기본 평면 네트워크(Flat Network)로 인한 **단일 파드 침해 시 클러스터 전체로의 측면 이동(Lateral Movement) 위험** 직면

#### 한줄 요약

- CNI가 파드 간 통신 망을 구성하고 NetworkPolicy가 제로 트러스트 기반의 방화벽 격리를 집행

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **기본 거부 정책(Default Deny All)**: 네임스페이스 내 모든 인그레스/이그레스 트래픽을 기본 차단하고 명시적으로 승인된 파드 통신만 화이트리스트로 허용하는 수칙.
- **eBPF 커널 바이패스(eBPF Kernel Bypass)**: iptables 규칙 누적에 따른 성능 저하 없이 리눅스 커널 소켓 레벨에서 초고속으로 패킷을 필터링하는 Cilium CNI 기술.

</details>

- 모든 파드가 별도의 NAT 없이 상호 통신할 수 있는 **CNI 기반 평면 네트워크 제공**
- 파드 라벨(Pod Selector) 및 포트 기반의 **L3/L4 인그레스·이그레스 트래픽 제어**
- 제로 트러스트(Zero Trust) 모델을 실현하는 **Default Deny 및 화이트리스트 정책**

#### 한줄 요약

- CNI의 라우팅 인프라와 NetworkPolicy의 소프트웨어 정의 방화벽을 결합하여 클러스터 내부 보안을 완성

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NetworkPolicy 및 CNI 데이터 플레인 계층**: NetworkPolicy YAML 정의, 정책 컨트롤러(Calico/Cilium Agent), 커널 eBPF/iptables 필터링 엔진.

</details>

```text
[ 쿠버네티스 CNI 및 NetworkPolicy 패킷 필터링 구조도 ]

 1. [ 프론트엔드 파드 (Frontend Pod) ]
    • IP: `10.244.1.10` (CNI 할당) ──► [ GET /api/orders ] 송신
                                            │
                                            ▼
 2. [ CNI Data Plane (Cilium eBPF / Calico iptables) ] ───────────┐
    • NetworkPolicy 검증: `app=frontend` ➔ `app=backend` 허용 여부 │
    • Default Deny 정책 대조 (Port 8080 허용)                     │
    └───────────────────────────────────────┬─────────────────────┘
                                            │ (인가된 패킷 통과)
                                            ▼
 3. [ 백엔드 파드 (Backend Pod) ] ──► [ DB 파드로의 임의 접속은 차단 ]
```

선의 의미: 프론트엔드 파드의 송신 패킷이 CNI Data Plane의 NetworkPolicy 룰셋을 거쳐 인가된 백엔드 파드로만 전달되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| CNI 플러그인 (Calico/Cilium) | 파드 생성 시 **네트워크 네임스페이스를 생성하고 고유 IP 및 라우팅 경로 할당** |
| NetworkPolicy 오브젝트 | `podSelector`, `ingress`, `egress`를 정의하여 **허용 대상 트래픽을 선언** |
| 정책 제어기 (Policy Controller) | 선언된 NetworkPolicy를 감지하여 **각 노드의 CNI 에이전트에 방화벽 규칙 전파** |
| 데이터 플레인 (eBPF/iptables)| 커널 계층에서 **실제 패킷의 출발지/도착지 IP와 포트를 실시간 검사하여 차단/허용** |

#### 한줄 요약

- CNI 플러그인, NetworkPolicy 명세, 정책 제어기, eBPF 데이터 플레인이 결합

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **NetworkPolicy 패킷 검사 5단계 절차**: 통신 패킷 발생 $\to$ 출발지/도착지 라벨 식별 $\to$ Ingress/Egress 정책 대조 $\to$ 포트 번호 검증 $\to$ 패킷 전달 또는 Drop.

</details>

```text
[ 쿠버네티스 NetworkPolicy 실시간 패킷 검사 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 송신 파드에서 통신 패킷 생성 송출   │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. CNI: 출발지 및 목적지 Pod 라벨 식별 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. NetworkPolicy Ingress/Egress 룰 대조 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. 대상 프로토콜(TCP) 및 포트(8080) 검증│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. 인가 시 패킷 전달, 불일치 시 Drop 차단│
 └────────────────────────────────────────┘
```

### 동작 원리

1. 패킷 송출: Frontend 파드가 Backend 파드로 API 요청 TCP SYN 패킷을 전송.
2. 라벨 식별: 노드의 CNI 에이전트(Cilium/Calico)가 송신 파드와 수신 파드의 메타데이터 라벨(`app=backend`)을 확인.
3. 정책 대조: 해당 백엔드 네임스페이스에 적용된 `NetworkPolicy` 명세의 `from` 허용 목록을 대조.
4. 포트 검증: 타깃 포트가 허용된 `8080/TCP`인지 일치 여부를 검사.
5. 통신 집행: 정책과 일치하면 즉시 커널 레벨에서 패킷을 전달하고, 미승인 접근이면 패킷을 즉시 Drop 폐기.

#### 한줄 요약

- 패킷 생성 $\to$ 라벨 식별 $\to$ 정책 대조 $\to$ 포트 검증 $\to$ 허용/Drop의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Calico vs Cilium vs AWS VPC CNI**: 전통적 BGP/iptables(Calico), 차세대 eBPF(Cilium), AWS 클라우드 네이티브(AWS VPC CNI).

</details>

| 구분 | Calico CNI | Cilium CNI (eBPF) | AWS VPC CNI |
|:---|:---|:---|:---|
| **적용 기준** | 대규모 온프레미스 및 BGP 라우팅 통합 환경 | 대규모 고성능 마이크로서비스, eBPF L7 보안 관측 | AWS EKS 전용 환경 및 VPC 직접 통신 |
| **핵심 특징** | **BGP 라우팅, iptables 및 eBPF 선택 지원** | **eBPF 커널 바이패스, L7 방화벽, 초고속 처리** | **EC2 ENI 보조 IP 직접 할당, VPC 통신 네이티브** |
| **한계** | 대규모 파드 급증 시 iptables 룰 테이블 비대화 | 리눅스 최신 커널(v5.4+) 요구 및 러닝커브 | 서브넷 가용 IP 고갈 위험 (Secondary CIDR 필요) |

#### 한줄 요약

- 온프레미스 표준은 Calico, 최고 성능의 차세대 보안은 Cilium eBPF, AWS 네이티브는 VPC CNI를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **AWS VPC CNI IP 고갈(Subnet IP Exhaustion)**: 노드에 파드가 뜰 때마다 실제 VPC 서브넷 IP를 점유하여 서브넷 CIDR이 고갈되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AWS VPC 서브넷 IP 고갈로 신규 파드 생성 불가 | **Custom Networking 구성 및 파드 전용 Secondary CIDR 서브넷 할당** | 수천 개 파드 확장용 IP 완벽 확보 |
| 수천 개 파드 운영 시 iptables 규칙 폭증으로 네트워크 레이턴시 증가 | **Cilium eBPF 기반 CNI로 마이그레이션하여 커널 소켓 직결 처리** | 패킷 필터링 지연시간 80% 단축 |
| NetworkPolicy 설정 오류로 인한 정상 파드 간 통신 마비 | **Cilium Hubble UI를 도입하여 패킷 Drop 및 흐름 실시간 가시화** | 정책 오류 디버깅 시간 수 분 단축 |

#### 한줄 요약

- Secondary CIDR 할당, Cilium eBPF 도입, Hubble UI 시각화를 통해 네트워크 정책의 안정성을 확보

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **서비스 메시와의 공존(NetworkPolicy vs Service Mesh)**: L3/L4 인프라 격리는 CNI NetworkPolicy가 전담하고, L7 mTLS 암호화 및 트래픽 분기는 Istio 서비스 메시가 담당하는 다계층 방어(Defense-in-Depth).

</details>

- **쿠버네티스 CNI 및 NetworkPolicy** 기반 클라우드 네이티브 제로 트러스트 보안의 출발점이며, 고성능 eBPF 기반 CNI를 바탕으로 Default Deny 미세 격리를 적용하여 클러스터 내부의 침해 확산을 원천 차단해야 함

#### 한줄 요약

- CNI 연결 인프라와 NetworkPolicy 미세 격리를 통해 제로 트러스트 클러스터 보안을 완성
