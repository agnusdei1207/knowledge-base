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

- **인터넷 프로토콜(Internet Protocol, IP) 주소**: 네트워크와 인터페이스를 식별하여 패킷의 출발지와 목적지를 나타내는 계층형 논리 주소이다.
- **IPv4(Internet Protocol version 4)**: 32비트 주소를 점으로 구분한 10진수로 표현하는 IP 버전이다.
- **IPv6(Internet Protocol version 6)**: 128비트 주소를 콜론으로 구분한 16진수로 표현하는 IP 버전이다.

</details>

- 정의/개념: 네트워크•인터페이스를 식별하는 **인터넷 프로토콜(Internet Protocol, IP) 주소**이다.
- 배경/필요성: 32비트 **IPv4(Internet Protocol version 4)** 주소 고갈은 공인 주소 할당을 제약한다.

#### 한줄 요약

- 우편번호와 상세 주소처럼 앞부분은 네트워크를, 뒷부분은 그 안의 인터페이스를 가리킨다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **최장 프리픽스 일치**: 목적지 주소와 가장 많은 앞 비트가 일치하는 경로를 선택하는 라우팅 규칙이다.
- **무상태 주소 자동 설정(Stateless Address Autoconfiguration, SLAAC)**: 라우터가 알린 프리픽스를 사용하여 호스트가 자신의 IPv6 주소를 자동으로 구성하는 방식이다.

</details>

- 계층형 프리픽스로 경로를 집약한다.
- **최장 프리픽스 일치**로 가장 구체적인 경로를 선택한다.
- **IPv6(Internet Protocol version 6)**와 **무상태 주소 자동 설정(Stateless Address Autoconfiguration, SLAAC)**을 사용한다.

#### 한줄 요약

- 목적지와 앞자리 비트가 가장 길게 맞는 경로가 더 구체적인 배송 구역을 가리킨다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **네트워크 프리픽스**: 주소 앞부분에서 목적지가 속한 네트워크 범위를 식별하는 영역이다.
- **인터페이스 식별자**: 프리픽스가 나타내는 네트워크 안에서 개별 인터페이스를 구분하는 영역이다.

</details>

```text
IP 주소
├── 네트워크 프리픽스
└── 인터페이스 식별자
```

선의 의미: IP 주소는 네트워크 범위를 나타내는 프리픽스와 그 내부의 인터페이스 식별 영역으로 구성된다.

| 구성요소 | 책임 |
|:---|:---|
| **네트워크 프리픽스** | 계층형 주소의 네트워크 범위 식별 |
| **인터페이스 식별자** | 네트워크 내부의 개별 인터페이스 구분 |

#### 한줄 요약

- 주소 앞부분으로 목적지 네트워크를 찾고 뒷부분으로 그 안의 인터페이스를 구분한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **주소 결정 프로토콜(Address Resolution Protocol, ARP)**: IPv4 주소에 대응하는 같은 링크의 매체 접근 제어 주소를 찾는 프로토콜이다.
- **이웃 탐색 프로토콜(Neighbor Discovery Protocol, NDP)**: IPv6에서 이웃 주소 확인•라우터 탐색•주소 중복 검사를 수행하는 프로토콜이다.
- **다음 홉**: 목적지까지의 경로에서 호스트가 패킷을 직접 전달할 인접 라우터나 장치이다.
- **경로 프리픽스 비교**: 목적지 주소와 라우팅 항목의 앞 비트를 대조하는 단계이다.
- **다음 홉 결정**: 최장 일치 경로에서 직접 전달할 인접 장치를 고르는 단계이다.
- **링크 주소 해석**: ARP 또는 NDP로 다음 홉의 링크 계층 주소를 확인하는 단계이다.

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

1. **경로 프리픽스 비교**: 목적지와 경로의 앞 비트를 비교한다.
2. **다음 홉 결정**: **다음 홉**을 선택한다.
3. **링크 주소 해석**: **주소 결정 프로토콜(Address Resolution Protocol, ARP)** 또는 **이웃 탐색 프로토콜(Neighbor Discovery Protocol, NDP)**로 주소를 확인한다.

#### 한줄 요약

- 목적지와 가장 길게 맞는 주소 앞부분을 선택한 뒤 바로 다음 장치의 링크 주소로 보낸다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **네트워크 주소 변환(Network Address Translation, NAT)**: 경계 장비에서 사설 IPv4 주소와 공인 IPv4 주소를 변환하는 기술이다.

</details>

| IP 주소 체계 | **IPv4(Internet Protocol version 4)** | **IPv6(Internet Protocol version 6)** |
|:---|:---|:---|
| 적용 기준 | IPv4 전용 기존망과 호환 | 주소 확장•자동 구성이 필요한 망 |
| 핵심 특징 | 32비트•점 구분 10진수 | 128비트•콜론 구분 16진수 |
| 한계 | 주소 고갈•**네트워크 주소 변환(Network Address Translation, NAT)** 의존 | 기존 IPv4 장비와 전환 복잡도 |

> 요약: IPv6 전환은 주소 구성•이웃 탐색 변경이 핵심이다.

#### 한줄 요약

- IPv4는 주소가 좁어 변환이 잦고 IPv6는 주소가 넓지만 운영 규칙을 함께 바꿔야 한다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **듀얼 스택(Dual Stack)**: 하나의 장비와 네트워크에서 IPv4와 IPv6를 함께 실행하는 전환 방식이다.
- **라우터 광고**: IPv6 라우터가 호스트에 네트워크 프리픽스와 기본 경로 정보를 전달하는 메시지이다.
- **동적 호스트 구성 프로토콜 버전 6(Dynamic Host Configuration Protocol version 6, DHCPv6)**: 서버가 IPv6 주소와 네트워크 설정을 호스트에 배포하는 프로토콜이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| IPv4 주소 풀이 서비스 수요보다 작음 | 수요 산정 후 NAT•IPv6 단계 전환 | 공인 주소 부족 완화 |
| IPv6 경로•필터 정책이 IPv4와 불일치 | **듀얼 스택(Dual Stack)** 경로•필터 검증 | 비인가 트래픽 허용 방지 |
| 이름 해석이 IPv4 주소만 반환 | IPv4•IPv6 주소 응답과 응용 지원 시험 | 전환 호환성 확보 |
| 비인가 장치가 자동 구성 정보를 배포 | **라우터 광고**•**동적 호스트 구성 프로토콜 버전 6(Dynamic Host Configuration Protocol version 6, DHCPv6)** 신뢰 경계 설정 | 비인가 주소 설정 차단 |

#### 한줄 요약

- 기존 IPv4 서비스를 유지하면서 IPv6 주소와 경로를 함께 제공해 두 주소 체계의 연결을 검증한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **IPv6 전환**: 기존 IPv4 호환성을 유지하면서 주소•경로•보안 정책을 단계적으로 IPv6에 적용하는 과정이다.
- **전환 방식 결정**: 기존망 호환성과 주소 수요를 기준으로 듀얼 스택을 검증한 뒤 단계적으로 IPv6로 전환하는 판단이다.

</details>

- **전환 방식 결정**에 따라 **듀얼 스택(Dual Stack)**을 검증한 뒤 **IPv6 전환**한다.

#### 한줄 요약

- 기존 장비가 남아 있으면 두 주소 체계를 함께 검증하며 단계적으로 전환해야 한다.
