---
sidebar:
  order: 4
  label: "004. IP 주소 체계: IPv4•IPv6 (IP Addressing IPv4 IPv6)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "IP 주소 체계: IPv4•IPv6 (IP Addressing IPv4 IPv6)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 4
extra:
  question_no: "004"
  source_status: "기출"
  source_history: "128회"
  priority: 30
  priority_note: "설명형: 128회 주소 구조 문항의 IP 핵심축"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **인터넷 프로토콜 주소(Internet Protocol Address, IP Address)**: 네트워크 및 노드 인터페이스를 식별하여 데이터 패킷의 송수신 위치를 지정하는 논리적 주소.
- **IPv4(Internet Protocol version 4)**: 32비트 길이의 주소를 8비트씩 4개 옥텟으로 나누어 10진수로 표기하는 IP 규격.
- **IPv6(Internet Protocol version 6)**: IPv4 주소 고갈을 해결하기 위해 128비트 주소를 16비트씩 8개 그룹으로 나누어 16진수로 표기하는 차세대 IP 규격.

</details>

- 정의/개념: 네트워크 및 노드 인터페이스를 식별하는 계층적 **인터넷 프로토콜 주소(Internet Protocol Address, IP Address)**.
- 배경/필요성: 32비트 **IPv4(Internet Protocol version 4)** 주소 고갈 대응 및 주소 공간 확장을 위한 **IPv6(Internet Protocol version 6)** 전환 필요성 대두.

#### 한줄 요약

- 우편번호와 상세 주소처럼 앞부분은 네트워크를, 뒷부분은 그 안의 인터페이스를 가리킨다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **최장 프리픽스 일치(Longest Prefix Match, LPM)**: 라우팅 테이블 내 다수의 라우팅 경로 중 라우팅 대상 IP와 비트가 가장 길게 일치하는 경로를 선택하는 메커니즘.
- **무상태 주소 자동 설정(Stateless Address Autoconfiguration, SLAAC)**: 별도의 DHCP 서버 없이 라우터의 프리픽스 정보를 바탕으로 호스트가 주소를 자동 생성하는 기술.

</details>

- 계층형 프리픽스 기반 라우팅 경로의 집약적 관리.
- **최장 프리픽스 일치(Longest Prefix Match, LPM)** 규칙을 활용한 최적 경로 선택.
- **IPv6(Internet Protocol version 6)** 및 **무상태 주소 자동 설정(Stateless Address Autoconfiguration, SLAAC)** 기반 호스트 주소의 효율적 관리.

#### 한줄 요약

- 목적지와 프리픽스가 가장 길게 일치하는 경로가 더 구체적인 서브넷을 가리킨다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **네트워크 프리픽스(Network Prefix)**: IP 주소의 상위 비트 영역으로, 해당 주소가 속한 전체 서브넷 및 네트워크 구역을 식별하는 파트.
- **인터페이스 식별자(Interface Identifier)**: 네트워크 프리픽스 하위 영역으로, 서브넷 내부에서 단일 인터페이스를 유일하게 식별하는 파트.

</details>

```text
IP 주소
├── 네트워크 프리픽스
└── 인터페이스 식별자
```

선의 의미: IP 주소 프리픽스(네트워크 영역)와 인터페이스 식별자(호스트 영역)의 계층적 구조를 통한 라우팅 효율성 확보 표시.

| 구성요소 | 책임 |
|:---|:---|
| **네트워크 프리픽스** | 계층형 주소 구조에서의 서브넷 및 네트워크 범위 식별 |
| **인터페이스 식별자** | 특정 네트워크 내 단일 인터페이스의 논리적 식별 |

#### 한줄 요약

- 주소 앞부분으로 목적지 네트워크를 찾고 뒷부분으로 그 안의 인터페이스를 구분한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **주소 결정 프로토콜(Address Resolution Protocol, ARP)**: IPv4 환경에서 IP 주소를 인접 데이터링크 계층의 MAC 주소로 매핑하는 프로토콜.
- **이웃 탐색 프로토콜(Neighbor Discovery Protocol, NDP)**: ICMPv6 기반으로 이웃 탐색, 라우터 발견, 주소 중복 검사(DAD) 등을 수행하는 IPv6 프로토콜.
- **다음 홉(Next Hop)**: 목적지 패킷 전송 시 전달해야 하는 인접 라우터 또는 최종 목적지의 논리적 주소.
- **경로 프리픽스 비교(Prefix Comparison)**: 목적지 IP와 라우팅 테이블 entry 비트 간 대조 과정.
- **다음 홉 결정(Next-Hop Selection)**: 라우팅 테이블 검색 결과에 기초한 출구 인터페이스 및 인접 장치 지정 과정.
- **링크 주소 해석(Link Address Resolution)**: ARP 또는 NDP를 통한 물리적 L2 MAC 주소 획득 처리.

</details>

```text
목적지 IP 주소
      |
      v
1. 경로 프리픽스 비교
      |
      v
2. 다음 홉 결정
      |
      +-- 같은 네트워크 ---- 목적지 IP
      |
      `-- 다른 네트워크 ---- 게이트웨이 IP
                                  |
                                  v
                         3. 링크 주소 해석
                                  |
                                  +-- IPv4 ---- ARP
                                  `-- IPv6 ---- NDP
                                               |
                                               `-- 링크 프레임 전송
```

### 동작 원리

1. **경로 프리픽스 비교(Prefix Comparison)**: 목적지 IP와 라우팅 비트 간 최장 일치 검증 수행.
2. **다음 홉 결정(Next-Hop Selection)**: 최적 경로 선택을 통한 인접 **다음 홉(Next Hop)** 지정.
3. **링크 주소 해석(Link Address Resolution)**: **주소 결정 프로토콜(Address Resolution Protocol, ARP)** 또는 **이웃 탐색 프로토콜(Neighbor Discovery Protocol, NDP)**을 활용한 L2 MAC 주소 획득.

#### 한줄 요약

- 목적지와 가장 길게 맞는 주소 앞부분을 선택한 뒤 바로 다음 장치의 링크 주소로 보낸다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **네트워크 주소 변환(Network Address Translation, NAT)**: 사설 IP 주소를 공인 IP 주소로 변환하여 주소 부족 문제를 완화하고 내부망 보안을 확보하는 기술.

</details>

| IP 주소 체계 | **IPv4(Internet Protocol version 4)** | **IPv6(Internet Protocol version 6)** |
|:---|:---|:---|
| 적용 기준 | IPv4 전용 기존망과 호환 | 주소 확장•자동 구성이 필요한 망 |
| 핵심 특징 | 32비트•점 구분 10진수 | 128비트•콜론 구분 16진수 |
| 한계 | 주소 고갈•**네트워크 주소 변환(Network Address Translation, NAT)** 의존 | 기존 IPv4 장비와 전환 복잡도 |

> 요약: IPv4 주소 고갈 한계 극복을 위한 IPv6 구조 전환 및 이웃 탐색 메커니즘 변화.

#### 한줄 요약

- IPv4는 주소가 좁어 변환이 잦고 IPv6는 주소가 넓지만 운영 규칙을 함께 바꿔야 한다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **듀얼 스택(Dual Stack)**: 단일 네트워크 장비 및 노드에서 IPv4와 IPv6 프로토콜 스택을 동시 지원하는 공존 및 전환 기술.
- **라우터 광고(Router Advertisement, RA)**: 라우터가 주기적으로 네트워크 프리픽스 및 호스트 설정 정보를 멀티캐스트로 전송하는 ICMPv6 메시지.
- **동적 호스트 구성 프로토콜 버전 6(Dynamic Host Configuration Protocol version 6, DHCPv6)**: IPv6 환경에서 상태보존형(Stateful) 방식으로 IP 및 추가 옵션을 자동 할당하는 프로토콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| IPv4 주소 풀이 서비스 수요보다 작음 | 수요 산정 후 NAT•IPv6 단계 전환 | 공인 주소 부족 완화 |
| IPv6 경로•필터 정책이 IPv4와 불일치 | **듀얼 스택(Dual Stack)** 경로•필터 검증 | 비인가 트래픽 허용 방지 |
| 이름 해석이 IPv4 주소만 반환 | IPv4•IPv6 주소 응답과 응용 지원 시험 | 전환 호환성 확보 |
| 비인가 장치가 자동 구성 정보를 배포 | **라우터 광고(Router Advertisement, RA)**•**DHCPv6** 신뢰 경계 설정 | 비인가 주소 설정 차단 |

#### 한줄 요약

- 기존 IPv4 서비스를 유지하면서 IPv6 주소를 함께 제공해 두 주소 체계의 연결을 검증한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **IPv6 전환(IPv6 Transition)**: IPv4 기반 네트워크를 듀얼 스택, 터널링, 변환 메커니즘을 적용하여 IPv6 환경으로 이행하는 과정.
- **전환 방식 결정(Transition Strategy Selection)**: 서비스 호환성과 주소 고갈 위기 수준을 종합 고려하여 최적의 전환 방안을 채택하는 판단.

</details>

- **전환 방식 결정(Transition Strategy Selection)**에 근거한 **듀얼 스택(Dual Stack)** 환경 검증 및 단계적 **IPv6 전환(IPv6 Transition)** 추진.

#### 한줄 요약

- 기존 장비가 남아 있으면 두 주소 체계를 함께 검증하며 단계적으로 전환해야 한다.

