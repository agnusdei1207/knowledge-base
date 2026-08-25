---
sidebar:
  order: 24
  label: "024. 네트워크 스푸핑 - ARP•IP•DNS"
  badge:
    text: "기출 · 70%"
    variant: note
title: "네트워크 주소 위변조 및 중간자 공격 : 계층별 스푸핑"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 24
extra:
  question_no: "24"
  source_status: "기출"
  source_history: "128회, 134회"
  priority: 70
  priority_note: "L2(ARP Spoofing/DAI), L3(IP Spoofing/uRPF BCP 84), L7(DNS Spoofing/DNSSEC), MITM 및 세션 하이재킹"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Spoofing (스푸핑, 주소 위장)**: 정상 호스트나 게이트웨이의 식별자(MAC, IP, DNS)를 위조하여 트래픽을 가로채는 공격.
- **MITM (Man-in-the-Middle, 중간자 공격)**: 통신 경로 중간에 침투하여 송수신 데이터를 도청하거나 변조하는 공격.

</details>

- 정의/개념: L2(ARP), L3(IP), L7(DNS)의 주소 해석 무인증 취약점을 악용해 주소를 위조하고 **트래픽 경로를 장악하는 계층별 위변조 공격 및 방어 기술**
- 배경/필요성: 초기 인터넷 프로토콜의 상호 신뢰 설계로 인한 **주소 헤더 내 신원 검증 부재, 무차별 캐시 오염 및 중간자 도청/반사 DDoS 방어 불가**

#### 한줄 요약
- L2 MAC, L3 IP, L7 DNS 주소 위변조를 차단하여 중간자 가로채기와 반사 DDoS를 방어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DAI (Dynamic ARP Inspection)**: DHCP Snooping 바인딩 테이블을 참조하여 위조된 가짜 ARP 응답을 스위치 하드웨어에서 즉시 폐기하는 L2 보안.
- **uRPF (Unicast Reverse Path Forwarding, IETF BCP 84)**: 패킷의 출발지 IP가 라우팅 테이블 상의 역방향 인터페이스와 일치하지 않으면 패킷을 드롭하는 L3 보안.

</details>

- **계층별 독립적인 공격 벡터(Layer-Specific)**: L2(LAN 내 MAC 변조), **L3(인터넷 IP 변조/반사), L7(DNS 캐시 오염/피싱)로 다변화**
- **비대칭적 캐시 오염 취약성**: 단 1개의 위조된 응답 패킷을 **정상 패킷보다 먼저 도달(Race Condition)시켜 캐시 테이블 변조**
- **계층별 전용 하드웨어 방어 기제**: L2 스위치(DAI), **L3 라우터(uRPF/BCP 38), L7 네임서버(DNSSEC/mTLS)의 통합 적용 필수**

#### 한줄 요약
- 계층별 독립 벡터, 비대칭 캐시 오염 취약성, DAI/uRPF/DNSSEC 계층형 방어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DNSSEC (RFC 4033)**: DNS 응답 데이터에 전자서명(RRSIG)을 부착하고 루트 도메인부터의 신뢰 체인(DS 레코드)으로 위변조를 검증하는 표준.

</details>

```text
[계층별 스푸핑 공격 및 하드웨어 방어 아키텍처]
|-- L2 Layer (ARP Spoofing 방어: L2 Switch DAI + DHCP Snooping DB -> 게이트웨이 보호)
|-- L3 Layer (IP Spoofing 방어: Boundary Router uRPF Strict Mode BCP 84 -> 위조 패킷 드롭)
`-- L7 Layer (DNS Spoofing 방어: Local Resolver DNSSEC RRSIG 검증 -> Root/TLD 신뢰 체인)
`-- End-to-End Encryption (mTLS 1.3: 경로가 장악되어도 페이로드 암호화로 도청 차단)
```

선의 의미: L2 스위치에서는 DAI가 MAC을 검증하고 L3 라우터에서는 uRPF가 출발지 IP를 검증하며 L7 DNS에서는 DNSSEC이 전자서명을 검증하여 계층별 스푸핑을 차단하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **ARP 방어 (L2 DAI)** | DHCP Snooping 바인딩 DB를 대조하여 **위조된 ARP 응답 패킷 하드웨어 드롭** | IEEE 802.1Q |
| **IP 방어 (L3 uRPF)** | 라우팅 FIB를 역방향 대조하여 **위조된 출발지 IP 패킷 폐기(BCP 84)** | IETF BCP 84 |
| **DNS 방어 (L7 DNSSEC)**| DNS 응답의 **RRSIG 전자서명 체인을 검증하여 캐시 포이즈닝 원천 차단** | IETF RFC 4033 |
| **종단 세션 보호 (mTLS)**| 네트워크 경로가 장악되어도 **전 구간 암호화로 페이로드 기밀성/무결성 보증** | RFC 8446 |

#### 한줄 요약
- L2 DAI(스위치), L3 uRPF(라우터), L7 DNSSEC(네임서버), 종단 mTLS(인증서)가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DNS Cache Poisoning**: 캐시 DNS 리졸버에 무작위 트랜잭션 ID(TXID)를 추측하여 가짜 IP 매핑 응답을 선제 주입하는 공격.

</details>

```text
스푸핑 패킷 인입, 캐시 오염 시도 및 계층별 방어 검증 파이프라인
        │
   1. [위조 패킷 선제 송출] 공격자가 정상 응답보다 빠른 타이밍에 위조된 응답(ARP Reply/DNS Answer) 송출
        │
   2. [캐시 오염 시도] 피해 호스트의 ARP Table 또는 리졸버 DNS Cache에 위조 매핑 주입 시도
        │
   3. [경로 장악 시도] 피해자 트래픽을 공격자 노드로 강제 라우팅하여 중간자(MITM) 통신 유도
        │
   4. [평문 도청/변조 시도] 암호화 부재 시 쿠키 및 자격증명 스니핑 시도
        │
   ▼
5. [계층형 방어 집행] DAI 포트 차단, uRPF 역방향 경로 불일치 드롭, DNSSEC RRSIG 검증 실패로 패킷 폐기
```

#### 한줄 요약
- 위조 패킷 송출 → 캐시 오염 시도 → MITM 경로 장악 시도 → 평문 도청 시도 → 계층별 검증 차단 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ARP 스푸핑 (L2)** vs **IP 스푸핑 (L3)** vs **DNS 스푸핑 (L7)**.

</details>

| 비교 항목 | ARP 스푸핑 (L2) | IP 스푸핑 (L3) | DNS 스푸핑 (L7) |
|:---|:---|:---|:---|
| **동작 계층** | **L2 (데이터 링크 계층)** | **L3 (네트워크 계층)** | **L7 (애플리케이션 계층)** |
| **위조 식별자** | **하드웨어 MAC 주소** | **논리적 출발지 IP 주소** | **도메인 해석 결과 (A/AAAA 레코드)**|
| **공격 유효 범위** | **동일 브로드캐스트 도메인(LAN)**| **인터넷 광역망 전역 (WAN/Internet)** | **글로벌 인터넷 전역 (DNS 리졸버 캐시)**|
| **주요 공격 목적** | **사내망 MITM 스니핑, 세션 하이재킹**| **반사 DDoS 증폭(DRDoS), 방화벽 우회**| **피싱/파밍 사이트 유도, 계정 탈취** |
| **주요 방어 기제** | **DAI, DHCP Snooping, Static ARP** | **uRPF (Strict Mode), BCP 38/84 ACL** | **DNSSEC, DoH(DNS over HTTPS), mTLS**|

#### 한줄 요약
- ARP는 LAN 내부 MITM용, IP는 광역망 반사 DDoS용, DNS는 글로벌 피싱 파밍용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IETF BCP 38 / BCP 84**: ISP 및 경계 라우터에서 위조된 출발지 IP 패킷이 인터넷 백본으로 유출되지 않도록 인그레스 필터링을 강제하는 표준 권고안.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 사내 LAN 내부 ARP Spoofing으로 인한 **사내망 패킷 도청 및 자격증명 탈취** | **L2 스위치에 `DHCP Snooping 바인딩 기반 Dynamic ARP Inspection(DAI)` 활성화** | 위조된 ARP 패킷 하드웨어 100% 폐기 및 사내 MITM 원천 차단 |
| 출발지 IP를 피해자 IP로 위조하여 유발하는 **대규모 반사 증폭 DDoS(DRDoS) 공격** | **경계 라우터에 `IETF BCP 84 표준 uRPF Strict Mode 및 인그레스 ACL` 적용** | 위조된 출발지 IP 패킷 유입 즉시 드롭 및 반사 공격 악용 차단 |
| DNS 캐시 포이즈닝으로 사용자가 피싱 사이트로 납치되는 **전사 계정 유출 사고** | **`RFC 4033 DNSSEC 서명 검증 강제 및 종단 간 상호 인증(mTLS 1.3)` 전면 적용** | 위조된 DNS 응답 무효화 및 암호학적 통신 진본성 보장 |
| 비대칭 라우팅 환경에서 uRPF Strict 모드 적용 시 정상 패킷 드롭 | **비대칭 라우팅 구간에는 `uRPF Loose Mode 또는 특정 ACL 예외`** 적용 | 정상 패킷 손실 없는 안정적인 스푸핑 방어 달성 |

#### 한줄 요약
- L2 스위치 DAI로 ARP를 막고, 라우터 uRPF로 IP 위조를 차단하며, DNSSEC/mTLS로 DNS를 보호한다.

## Ⅶ. 결론

- 네트워크 통신의 근간인 주소 체계의 신뢰성을 위협하는 **스푸핑(Spoofing) 공격은 단일 솔루션으로 방어할 수 없으며**, 실무 구현 시 **L2 스위치의 DAI 및 DHCP Snooping 구축, L3 라우터의 uRPF Strict 모드 적용, L7 네임서버의 DNSSEC 및 전 구간 mTLS 상호 인증**을 결합한 계층형 다중 검증 체계를 확립하여 무결점 네트워크 주소 보안 완성

#### 한줄 요약
- 네트워크 스푸핑은 L2 DAI, L3 uRPF, L7 DNSSEC 및 종단 mTLS 상호 인증을 통해 주소 위변조와 중간자 도청을 원천 차단해야 한다.