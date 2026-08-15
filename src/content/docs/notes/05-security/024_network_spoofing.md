---
sidebar:
  order: 24
  label: "024. 네트워크 스푸핑 - ARP•IP•DNS (Network Spoofing)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "네트워크 스푸핑 - ARP•IP•DNS (Network Spoofing)"
date: "2026-08-13T18:48:54+09:00"
tags:
  - "notes-security"
weight: 24
extra:
  question_no: "024"
  source_status: "기출"
  source_history: "128회, 134회"
  priority: 70
  priority_note: "128•134회 반복된 계층별 스푸핑 비교 주제임"
---

## Ⅰ. 개요

<details>
<summary>용어 설명</summary>

- **스푸핑(Spoofing)**: 프로토콜 상의 정당한 주소, 신원, 응답 헤더 정보를 위변조하여 자신이 정직한 통신 대상인 것처럼 속이는 공격.
- **중간자 공격(Man-In-The-Middle Attack, MITM)**: 송수신자 사이의 데이터 흐름에 몰래 개입하여 암호화되지 않은 패킷을 도청, 위변조, 세션 가로채기를 수행하는 공격.

</details>

- 정의/개념: MAC•IP•DNS 정보를 위조해 정상 주체로 가장하는 **스푸핑**
- 배경/필요성: ARP•IP•DNS에는 **기본 신원 검증 결여**가 있다.

#### 한줄 요약

- Data-Link(MAC), Network(IP), Application(DNS) 계층별 신원 주소를 위변조하여 중간자 공격(MITM) 및 도청을 수행하는 기법

## Ⅱ. 특징

<details>
<summary>용어 설명</summary>

- **ARP(Address Resolution Protocol)**: L2 인접 네트워크에서 IP 주소를 해당하는 물리적 MAC 주소로 매핑 도출하는 프로토콜.
- **IP(Internet Protocol)**: L3 패킷에 출발지/목적지 논리 IP 주소를 부여하여 엔드-투-엔드 라우팅을 지원하는 프로토콜.
- **MAC(Media Access Control) 주소**: L2 통신을 위해 네트워크 인터페이스 카드에 부여된 48비트 주소.
- **DNS(Domain Name System)**: 사람이 읽을 수 있는 도메인 이름을 L3 IP 주소로 상호 해석 변환하는 분산 네임 시스템.
- **반사 공격(Reflective Attack)**: 출발지 IP를 피해자로 위조해 대용량 응답을 피해자에게 집중시키는 공격.
- **ARP 스푸핑(ARP Spoofing)**: 거짓 ARP Reply 패킷을 주기적으로 브로드캐스트/유니캐스트하여 게이트웨이 및 호스트의 ARP 테이블을 오염시키는 L2 공격.
- **IP 스푸핑(IP Spoofing)**: IP 헤더의 출발지 IP 주소를 타깃 주소로 변조하여 신분을 숨기거나 반사 공격 및 IP 기반 필터링을 회피하는 L3 공격.
- **DNS 스푸핑(DNS Spoofing)**: DNS 쿼리에 대해 정당한 네임서버보다 먼저 위변조된 IP 주소의 DNS Reply 패킷을 주입하여 파밍(Phishing) 사이트로 우회시키는 L7 공격.

</details>

- **ARP 스푸핑**은 동일 세그먼트 내 IP-**MAC 주소** 대응 테이블을 오염시켜 스위칭 환경에서의 **중간자 공격(MITM)** 유도
- **IP 스푸핑**은 출발지 IP를 변조하여 라우터의 IP 기반 접근 통제(ACL)를 회피하고 **반사 공격**에 악용
- **DNS 스푸핑**은 DNS 캐시 포이즈닝을 유발하여 전사 사용자를 피싱/악성코드 유포 사이트로 강제 유도

#### 한줄 요약

- L2 ARP 캐시 포이즈닝, L3 IP 출발지 위조 반사 공격(Reflective DDoS) 및 L7 DNS 캐시 포이즈닝 기법

## Ⅲ. 구조 및 구성요소

<details>
<summary>용어 설명</summary>

- **동적 ARP 검사(Dynamic ARP Inspection, DAI)**: L2 스위치에서 DHCP Snooping 데이터베이스를 검증하여 위조된 거짓 ARP 패킷을 물리 포트 단위에서 드롭 차단하는 보안 기술.
- **uRPF(Unicast Reverse Path Forwarding)**: 라우터 입력 인터페이스로 수신된 패킷의 출발지 IP 주소가 라우팅 테이블(FIB)의 역방향 경로와 일치하지 않으면 위조 패킷으로 간주하여 차단하는 L3 방어 기술.
- **DNSSEC(Domain Name System Security Extensions)**: 공개키 암호화 비대칭 서명 기술을 DNS 프로토콜에 결합하여 DNS 응답의 출처 인증 및 데이터 무결성을 보장하는 L7 표준.
- **TLS 종단 상호 인증(mTLS)**: 주소 스푸핑으로 통신 경로가 우회되더라도 디지털 인증서 상호 검증을 통해 최종 통신 상대의 신원을 무결성 검증하는 기술.

</details>

```text
스푸핑 방어 구조
├─ 신뢰 정보
├─ 검증 통제
├─ 위조 주입점
├─ 주소 캐시•필터
└─ 공격 감시•종단 인증
```

가지의 의미: 계층별 주소 테이블 관리, 스위치/라우터/DNS 차원 패킷 검증 및 TLS 종단 상호 인증 책임을 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| 신뢰 정보 | DHCP Snooping 바인딩, 라우팅 테이블(FIB), DNSSEC 신뢰 앵커(Trust Anchor) 관리 |
| 검증 통제 | L2 DAI, L3 uRPF/Ingress 필터링, L7 DNSSEC 서명 검증 엔진 동작 |
| 위조 주입점 | 공격자가 악의적으로 주입하는 거짓 ARP Reply, IP 패킷, DNS 쿼리 응답 탐지 |
| 주소 캐시•필터 | 정제된 유효 IP-MAC 매핑 및 무결성이 검증된 DNS A 레코드만 신뢰 저장 |
| 공격 감시•종단 인증 | Promiscuous 모드 탐지 및 mTLS(Mutual TLS) 기반 종단 간 개별 상호 신원 입증 |


#### 한줄 요약

- L2 DAI(Dynamic ARP Inspection), L3 uRPF/Ingress 필터링, L7 DNSSEC 및 L7 TLS 종단 상호 인증 방어 아키텍처

## Ⅳ. 흐름도

<details>
<summary>용어 설명</summary>

- **캐시 오염(Cache Poisoning)**: 검증되지 않은 위조 주소 매핑으로 피해 호스트의 캐시를 부정 갱신하는 공격.
- **출발지 위조(Source IP Spoofing)**: IP 헤더의 Source Address 필드를 임의의 타깃 주소로 위조하여 트래픽을 가공 전송하는 단계.
- **위조 주소•응답 주입**: 거짓 ARP/DNS 응답 패킷을 정상 응답보다 빠른 타이밍에 피해자에게 전달하는 단계.
- **위조 대응 캐시 저장**: 오염된 ARP/DNS 매핑 결과가 피해자 시스템 캐시에 저장되는 단계.
- **공격자 경로로 트래픽 전환**: 오염된 MAC/IP 주소로 인해 피해자의 모든 패킷이 공격자 노드로 집중(MITM)되는 단계.
- **위조 출발지 패킷 전송**: 타깃 IP로 출발지를 속인 통신 패킷을 대용량 반사 서버로 전송하는 단계.

</details>

```text
스푸핑 공격 경로
├─ ARP•DNS 응답 위조
│      │
│      ▼
│  1. 위조 주소•응답 주입
│      │
│      ▼
│  2. 위조 대응 캐시 저장
│      │
│      ▼
│  3. 공격자 경로로 트래픽 전환
│
└─ IP 출발지 위조
       │
       ▼
   4. 위조 출발지 패킷 전송
       │
       └── 피해자에게 반사 응답
```

### 동작 원리

1. **위조 주소•응답 주입**: 공격자가 L2 거짓 ARP Reply 및 L7 위조 DNS Response 패킷 송신
2. **위조 대응 캐시 저장**: 피해 호스트/서버의 ARP Cache Table 및 DNS Cache가 오염 갱신
3. **공격자 경로로 트래픽 전환**: 피해자의 인터넷 트래픽이 게이트웨이가 아닌 공격자 PC로 우회 세션 하이재킹
4. **위조 출발지 패킷 전송**: L3 출발지 IP를 피해자 주소로 변조하여 반사 DDoS 공격 자원 활용


#### 한줄 요약

- 위조 ARP/DNS 응답 주입, 캐시 오염(Poisoning), 도청 경로(MITM) 우회 및 IP 출발지 위조 반사 공격 흐름

## Ⅴ. 종류 및 비교

| 네트워크 스푸핑 종류 | **ARP 스푸핑 (L2)** | **IP 스푸핑 (L3)** | **DNS 스푸핑 (L7)** |
|:---|:---|:---|:---|
| 위변조 대상 필드 | L2 Ethernet MAC 주소 | L3 IPv4/IPv6 출발지 IP 주소 | L7 DNS A/AAAA 레코드 응답 IP |
| 공격 도달 범위 | 동일 브로드캐스트 세그먼트(LAN) | 인터넷 전체 라우팅 가능 영역 | DNS 쿼리를 수행하는 전사 클라이언트 |
| 주요 피해 및 위협 | 세션 하이재킹, 패킷 도청(MITM) | 반사 DDoS(DRDoS), ACL 통제 회피 | 파밍 사이트 우회, 계정 정보 피싱 유출 |
| 핵심 대응 기술 | **L2 DAI (Dynamic ARP Inspection)** | **L3 uRPF (BCP 84) & Ingress Filtering** | **L7 DNSSEC (RFC 4033) & mTLS** |

> 요약: 스푸핑 계층(L2 vs L3 vs L7) 및 공격 목적에 부합하는 계층별 방어 기법의 차등 적용

#### 한줄 요약

- 공격 계층, 위변조 대상(MAC vs IP vs Domain), 주된 피해(MITM vs DDoS vs 피싱)에 따른 스푸핑 공격 비교

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>용어 설명</summary>

- **IETF BCP 84(Best Current Practice 84)**: 이종 네트워크 경계 라우터에서 출발지 IP 주소 위변조 패킷을 차단하기 위한 Ingress/uRPF 필터링 지침.
- **IETF RFC 4033~4035(DNSSEC Specifications)**: DNS 데이터 무결성 및 출처 인증을 제공하는 DNSSEC 표준 규격 문서.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| L3 출발지 IP 변조 반사 공격 | **IETF BCP 84 기반 uRPF 및 Ingress Filtering** | 불법 출발지 IP 패킷 경계 단 차단 |
| L7 DNS 캐시 포이즈닝 | **IETF RFC 4033~4035 기반 DNSSEC** 적용 | DNS 응답 서명 무결성 검증으로 피싱 차단 |
| L2 LAN 내부 ARP 캐시 오염 | **DHCP Snooping 연동 L2 DAI 및 Static ARP** | 스위치 포트 수준의 위조 ARP 드롭 |
| 중간자 경로 우회 도청 | **mTLS(Mutual TLS) 종단 상호 인증** | 통신 경로 오염에도 데이터 암호화 및 신원 입증 |

#### 한줄 요약

- IETF BCP 84(uRPF) 준수, RFC 4033~4035(DNSSEC) 적용, 스위치 DAI 및 TLS 종단 상호 인증 연동

## Ⅶ. 결론

<details>
<summary>용어 설명</summary>

- **계층별 스푸핑 방어 체계(Layered Anti-Spoofing Architecture)**: L2 스위치, L3 라우터, L7 DNS 및 애플리케이션에 걸친 다계층 주소 검증 아키텍처.

</details>

- 네트워크 계층에 따라 L2는 **DAI**, L3는 **uRPF**, L7은 **DNSSEC 및 TLS 상호 인증**을 계층별 심층 방어 적용

#### 한줄 요약

- L2는 **DAI**, L3는 **uRPF**, L7은 **DNSSEC•mTLS** 적용
