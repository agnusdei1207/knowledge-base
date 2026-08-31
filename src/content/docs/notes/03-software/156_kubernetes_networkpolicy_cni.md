---
sidebar:
  order: 156
  label: "156. 쿠버네티스 NetworkPolicy•CNI"
  badge:
    text: "기출 · 70%"
    variant: note
title: "쿠버네티스 NetworkPolicy•CNI (Kubernetes NetworkPolicy CNI)"
date: "2026-08-31T10:48:00+09:00"
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

- **CNI(Container Network Interface)**: 파드 간 고유 IP를 할당하고 오버레이(VXLAN/eBPF) 통신을 제공하는 표준 네트워크 플러그인.
- **NetworkPolicy**: 파드 간의 트래픽을 L3/L4 계층(라벨, 네임스페이스, IP/Port)에서 차단/허용하는 쿠버네티스 선언적 방화벽 객체.

</details>

- 정의/개념: 파드 간 네트워크 연결과 고유 IP를 할당하는 **CNI와 L3/L4 파드 트래픽 미세 격리(Micro-segmentation)를 수행하는 NetworkPolicy 보안 체계**
- 배경/필요성: 쿠버네티스 기본 평면(Flat) 네트워크 환경에서 모든 파드가 상호 무제한 통신이 가능함에 따라 발생하는 단일 파드 침해 시 공격자의 클러스터 내부 횡적 이동(Lateral Movement) 및 데이터 유출 위험을 원천 차단하기 위해, 파드 간 오버레이/직접 통신을 관장하는 CNI(Container Network Interface) 인프라 위에 파드 라벨, 네임스페이스, IP/Port 단위로 접근을 통제하는 NetworkPolicy를 선언하여 **제로 트러스트(Zero Trust) 기반의 미세 격리(Micro-segmentation) 방화벽을 구축**할 필요

#### 한줄 요약
- CNI가 통신망을 구성하고 NetworkPolicy가 제로 트러스트 기반의 방화벽 격리를 집행한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Default Deny All**: 네임스페이스 내 모든 트래픽을 기본 차단하고 명시적으로 승인된 파드 통신만 화이트리스트로 허용하는 제로 트러스트 규칙.
- **eBPF Kernel Bypass**: iptables 규칙 누적 없이 리눅스 커널 소켓 레벨에서 초고속으로 패킷을 필터링하는 Cilium 기술.

</details>

- 모든 파드가 NAT 없이 상호 통신할 수 있는 **CNI 기반 평면 네트워크 제공**
- 파드 라벨(Pod Selector) 및 포트 기반의 **L3/L4 인그레스·이그레스 트래픽 제어**
- 제로 트러스트(Zero Trust) 모델을 실현하는 **Default Deny 및 화이트리스트 정책**

#### 한줄 요약
- CNI의 라우팅 인프라와 NetworkPolicy의 소프트웨어 정의 방화벽을 결합한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NetworkPolicy & CNI 데이터 플레인**: NetworkPolicy 선언, 정책 컨트롤러(Calico/Cilium Agent), 커널 eBPF/iptables 필터링 엔진.

</details>

```text
[CNI·NetworkPolicy 구성]
|-- CNI 플러그인
|-- NetworkPolicy 오브젝트
|-- 정책 제어기
`-- 데이터 플레인
```

선의 의미: 계층 및 프론트엔드 파드의 송신 패킷이 CNI Data Plane의 NetworkPolicy 룰셋을 거쳐 인가된 백엔드 파드로만 전달되는 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| CNI 플러그인 | 파드 생성 시 **네트워크 네임스페이스를 생성하고 고유 IP 및 라우팅 경로 할당** | Calico, Cilium |
| NetworkPolicy 오브젝트 | `podSelector`, `ingress`, `egress`를 정의하여 **허용 대상 트래픽을 선언** | 선언적 YAML 방화벽 |
| 정책 제어기 (Controller) | 선언된 NetworkPolicy를 감지하여 **각 노드의 CNI 에이전트에 방화벽 규칙 전파** | 실시간 룰 동기화 |
| 데이터 플레인 (eBPF) | 커널 계층에서 **실제 패킷의 출발지/도착지 IP와 포트를 실시간 검사하여 차단/허용**| 초고속 패킷 검사 |

#### 한줄 요약
- 정책 제어기가 선언된 명세를 각 노드 커널의 필터 규칙으로 번역해 내려보내므로, 애플리케이션은 방화벽 코드를 한 줄도 갖지 않고 격리를 얻는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **NetworkPolicy 패킷 검사 5단계**: 패킷 송출 $\to$ CNI 라벨 식별 $\to$ Ingress/Egress 룰 대조 $\to$ 프로토콜/포트 검증 $\to$ 인가 전달 또는 Drop.

</details>

```text
Frontend 파드에서 Backend 파드로 API 요청 전송
        │
   [패킷 생성 송출] Frontend 파드가 TCP SYN 패킷을 생성하여 veth 인터페이스로 방출
        │
   [라벨 식별] 노드의 CNI 에이전트(Cilium)가 송신 파드와 수신 파드의 메타데이터 라벨 확인
        │
   [정책 대조] 수신 파드 네임스페이스의 NetworkPolicy `from` 허용 목록과 대조
        │
   [포트 검증] 타깃 포트가 정책에 허용된 `8080/TCP`인지 일치 여부 검사
        │
   정책과 일치 시 커널 레벨에서 즉시 통과, 비인가 접근 시 패킷을 즉시 Drop 폐기
```

#### 한줄 요약
- 허용 판정은 커널 데이터 플레인에서 끝나 사용자 공간 왕복 비용이 없고, 차단 판정도 목적지 파드에 닿기 전에 내려져 비인가 트래픽이 대상 프로세스를 소모시키지 못한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Calico vs Cilium vs AWS VPC CNI**: 전통적 iptables/BGP(Calico), 차세대 eBPF(Cilium), AWS 클라우드 네이티브(VPC CNI).

</details>

| 비교 항목 | Calico CNI | Cilium CNI (eBPF) | AWS VPC CNI |
|:---|:---|:---|:---|
| 데이터 플레인 기술 | **리눅스 iptables / IPVS (BGP 오버레이)** | **eBPF (커널 소켓 직접 바이패스)** | **EC2 ENI 보조 IP 직접 할당 (VPC 직결)** |
| NetworkPolicy 지원 | 완전 지원 (선언적 L3/L4 방화벽) | **완전 지원 (L3/L4 + L7 HTTP 정책/Hubble)**| 보안 그룹(Security Group for Pod) 연동 |
| 대규모 성능 확장성 | 파드 수만 개 시 iptables 룰 비대화 | **수만 개 파드에서도 O(1) 초고속 패킷 처리**| VPC 서브넷 CIDR 용량에 종속 |
| 최적 적용 환경 | **온프레미스 IDC 및 BGP 네트워크 환경** | **대규모 MSA, 금융권 고성능 보안 클라우드**| **AWS EKS 네이티브 환경** |

#### 한줄 요약
- 온프레미스 표준은 Calico, 최고 성능의 차세대 보안은 Cilium eBPF, AWS 네이티브는 VPC CNI를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **AWS VPC CNI Subnet IP Exhaustion**: 노드에 파드가 생성될 때마다 실제 VPC 서브넷 IP를 점유하여 서브넷 CIDR이 고갈되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AWS VPC 서브넷 IP 고갈로 신규 파드 생성 불가 | **Custom Networking 구성 및 파드 전용 Secondary CIDR 서브넷 할당** | 수천 개 파드 확장용 IP 완벽 확보 |
| 수천 개 파드 운영 시 iptables 규칙 폭증으로 네트워크 레이턴시 증가 | **Cilium eBPF 기반 CNI로 마이그레이션하여 커널 소켓 직결 처리** | 패킷 필터링 지연시간 80% 단축 |
| NetworkPolicy 설정 오류로 인한 정상 파드 간 통신 마비 | **Cilium Hubble UI를 도입하여 패킷 Drop 및 흐름 실시간 가시화** | 정책 오류 디버깅 시간 수 분 단축 |
| 네임스페이스 간 무제한 통신으로 인한 측면 공격 침해 | **모든 네임스페이스에 `Default-Deny-All` NetworkPolicy 기본 배포** | 제로 트러스트 내부 방화벽 확립 |

#### 한줄 요약
- IP 고갈과 규칙 폭증, 정책 오류로 인한 통신 마비는 격리 단위를 파드까지 잘게 쪼갠 대가이며, eBPF 데이터 플레인과 흐름 가시화는 그 운영 비용을 되사는 투자다.

## Ⅶ. 결론

- 엔터프라이즈 컨테이너 보안 및 ISMS-P/금융 망분리 컴플라이언스를 충족하는 **가장 핵심적인 내부 통신 격리 표준**으로 확립되었으며, 실무 구축 시에는 **모든 네임스페이스에 기본 적용하는 Default-Deny-All 화이트리스트 정책, 대규모 파드 통신 시 iptables 오버헤드를 제거하는 eBPF 기반 Cilium CNI 도입, 실시간 패킷 드롭 및 서비스 의존성을 관측하는 Hubble UI 연동, AWS VPC CNI IP 고갈을 방어하는 Secondary CIDR 커스텀 네트워킹**을 결합하여 초고속 패킷 처리 성능과 무결점 제로 트러스트 보안을 완성

#### 한줄 요약
- CNI와 NetworkPolicy는 파드 간 연결성과 제로 트러스트 미세 격리 방화벽을 제공하여 클러스터 내부 보안을 완성하는 핵심 네트워킹 기술이다.
