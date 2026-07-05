---
title: "DHCP (Dynamic Host Configuration Protocol)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-network"
weight: 9
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **DHCP** | DHCP (Dynamic Host Configuration Protocol)의 핵심 개념 | 이 주제의 본질 |

---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: 호스트가 네트워크에 접속할 때 IP 주소, 서브넷 마스크, 기본 게이트웨이 등을 **자동으로 할당(임대)**해주는 프로토콜입니다.
- **필요성**: 수백 대의 PC에 관리자가 일일이 수동으로 IP를 입력하는 것은 불가능에 가깝고, 실수로 인한 IP 충돌도 잦습니다. 이를 자동화하여 관리 부하를 획기적으로 줄여줍니다.
- **핵심 직관**: **"IP 주소 렌탈 서비스"**. 정해진 시간 동안 주소를 빌려 쓰고, 다 쓰면 반납하거나 연장합니다.

## 깊이 이해
- **배경 (왜 UDP 67/68번인가?)**: DHCP는 클라이언트가 아직 IP가 없는 상태에서 시작됩니다. 그래서 상대방의 IP를 지정해서 보내는 TCP 대신, 일단 모두에게 뿌리고 보는 UDP 브로드캐스트 방식을 사용합니다.
- **작동 원리 (DORA 4단계)**:
  1.  **Discover**: "IP 빌려줄 서버 있나요?" (Client -> Server, Broadcast)
  2.  **Offer**: "이 IP(예: 192.168.1.10) 어때요?" (Server -> Client, Unicast/Broadcast)
  3.  **Request**: "좋아요! 그 IP로 쓸게요." (Client -> Server, Broadcast)
  4.  **Acknowledgment (ACK)**: "승인합니다. 설정값들과 함께 잘 쓰세요." (Server -> Client, Unicast/Broadcast)
- **Lease Time (임대 시간)**: IP는 영구적인 것이 아니라 빌려주는 것입니다. 임대 시간의 50%가 지나면 갱신(Renewal)을 시도하고, 87.5%가 지나면 재바인딩(Rebinding)을 시도합니다.
- **Relay Agent**: DHCP 서버가 다른 네트워크 대역에 있을 때, 브로드캐스트 패킷을 가로채서 서버에 전달해주는 '중계자' 역할을 합니다.

## 연결 개념
- **DHCP Snooping**: 가짜 DHCP 서버(Rogue DHCP)가 엉뚱한 IP를 뿌리지 못하게 스위치 포트 수준에서 차단하는 보안 기술.
- **APIPA (Automatic Private IP Addressing)**: DHCP 서버가 응답하지 않을 때 장치가 스스로 `169.254.x.x` 대역의 주소를 갖는 기능. (인터넷 안 됨)

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 네트워크 자원의 효율적 배분과 관리를 위해 호스트에 IP 구성 정보를 동적으로 할당하는 UDP 기반 클라이언트-서버 프로토콜임.
> 2. **가치**: IP 관리 자동화로 휴먼 에러를 방지하고, 한정된 IP 자원을 재사용(Lease/Release)함으로써 주소 활용 효율을 극대화함.
> 3. **판단 포인트**: 대규모 망 설계 시 DHCP Relay Agent를 통한 서버 중앙화와 DHCP Snooping을 통한 비인가 서버 차단 보안 설계가 병행되어야 함.

## Ⅰ. DHCP의 정의 및 주요 역할
- **정의**: TCP/IP 통신을 위해 필요한 설정 파라미터(IP, Mask, GW, DNS 등)를 중앙 서버가 호스트에 자동으로 배포하는 규약.
- **주요 역할**:
  - **자동 프로비저닝**: 관리자 개입 없는 제로터치 네트워크 접속 지원.
  - **주소 자원 회수**: 사용하지 않는 IP를 회수하여 주소 고갈 문제 완화.
  - **이동성 보장**: 단말이 다른 네트워크로 이동해도 별도 설정 없이 즉시 통신 가능.

## Ⅱ. DHCP 동작 메커니즘: DORA 4단계 프로세스

### 1. 할당 절차 (Initial Allocation)
| 단계 | 메시지명 | 전송 방식 | 주요 내용 |
|:---:|:---|:---:|:---|
| **1** | **Discover** | Broadcast | 클라이언트가 망 내의 DHCP 서버 탐색 |
| **2** | **Offer** | Uni/Broad | 서버가 가용한 IP 및 설정 정보 제안 |
| **3** | **Request** | Broadcast | 선택한 서버에 IP 할당 최종 요청 (타 서버에 알림 겸용) |
| **4** | **ACK** | Uni/Broad | 서버가 임대 확정 및 옵션 정보(Lease Time 등) 전송 |

### 2. 임대 갱신 및 만료 프로세스
- **Renewal (T1, 50%)**: 임대 시간 절반 경과 시 기존 서버에 갱신 요청(Unicast).
- **Rebinding (T2, 87.5%)**: 응답 없을 시 다른 모든 서버에 갱신 요청(Broadcast).
- **Expiration (100%)**: 응답 없이 시간 만료 시 IP 반납 후 재탐색(Discover).

## Ⅲ. 엔터프라이즈 환경의 DHCP 아키텍처

### 1. DHCP Relay Agent (ip helper-address)
- **필요성**: DHCP Discover는 브로드캐스트이므로 라우터를 통과하지 못함.
- **동작**: 라우터가 Discover 패킷을 수신하면 이를 유니캐스트로 변환하여 원격지의 중앙 DHCP 서버로 전달.
- **장점**: 분산된 네트워크의 IP를 한 곳에서 통합 관리 가능.

### 2. DHCP Option 필드 활용
- **Option 43**: 무선 AP가 WLC(Wireless LAN Controller) 주소를 찾을 때 사용.
- **Option 150**: IP Phone이 TFTP 서버 주소를 찾을 때 사용.

## Ⅳ. DHCP 관련 보안 위협 및 대응 방안

### 1. Rogue DHCP Server (가짜 서버)
- **위협**: 비인가 서버가 가짜 게이트웨이 정보를 배포하여 데이터 패킷 가로채기(MITM) 수행.
- **대응**: **DHCP Snooping** 적용. 스위치에서 정식 서버가 연결된 포트만 'Trusted'로 설정하고 나머지는 차단.

### 2. DHCP Starvation (고갈 공격)
- **위협**: 공격자가 MAC 주소를 위조하여 수천 개의 IP를 요청해 서버의 주소 풀을 고갈시킴.
- **대응**: 포트별 최대 학습 MAC 주소 수를 제한(Port Security)하거나 할당 속도 제한.

## Ⅴ. IPv4 DHCP vs IPv6 SLAAC/DHCPv6 비교

| 비교 항목 | IPv4 DHCP | IPv6 SLAAC | DHCPv6 (Stateful) |
|:---:|:---|:---|:---|
| **할당 방식** | 서버 중심 (Stateful) | 단말 중심 (Stateless) | 서버 중심 (Stateful) |
| **의존성** | 서버 필수 | 라우터 광고(RA) 기반 | 서버 필수 |
| **관리 부하** | 중간 | 매우 낮음 | 중간 |
| **특징** | DORA 과정 | NDP 기반 자동 생성 | 상세 옵션 관리 용이 |

## Ⅵ. 기술사적 통찰: '동적 관리'와 '가시성'의 균형
- **IPAM의 필요성**: DHCP는 할당을 자동화해주지만, 전체 망의 가시성(Visibility)을 제공하지는 않음. 따라서 실시간 할당 현황을 관리하는 IPAM(IP Address Management) 솔루션 연동이 실무적으로 매우 중요함.
- **클라우드 네이티브**: SDN 기반 클라우드 환경에서는 물리 서버가 아닌 가상 컨트롤러가 DHCP 기능을 수행하며, 이는 마이크로서비스의 빠른 확장(Scale-out)을 지원하는 핵심 동력이 됨.
- **결론**: DHCP는 단순한 주소 할당 도구를 넘어, 네트워크의 유연성과 보안, 그리고 운영 효율성을 결정짓는 인프라의 '혈액 순환계'와 같은 역할을 수행함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 (구조 중심) | Ⅳ·Ⅴ 강조 (실무 중심) |
|:---:|:---|:---|:---|
| **설명형** | "DHCP의 동작 원리와 절차" | DORA 4단계, 임대 갱신 타이머 | Relay Agent의 역할 및 구성 |
| **보안형** | "DHCP 취약점과 보안 강화 방안" | Rogue DHCP, Starvation 메커니즘 | DHCP Snooping, Port Security 연동 |
| **설계형** | "대규모 전산망 IP 관리 설계" | 중앙 서버화(Relay), 이중화 설계 | IPAM 연동 및 IPv6 대응 방안 |
