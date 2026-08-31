---
sidebar:
  order: 86
  label: "086. 네트워크 스푸핑 (ARP•IP•DNS)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "네트워크 식별자 위변조 방어 : ARP, IP, DNS 스푸핑"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-network"
weight: 86
extra:
  question_no: "86"
  source_status: "기출"
  source_history: "128회, 134회"
  priority: 70
  priority_note: "L2 ARP 스푸핑(DAI), L3 IP 스푸핑(uRPF/BCP 38), L7 DNS 스푸핑(DNSSEC) 및 캐시 오염 방어"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Network Spoofing (스푸핑)**: MAC, IP, DNS 등 네트워크 식별자를 위변조하여 권한 획득, 도청(MITM), DDoS를 유발하는 기만 공격.
- **Cache Poisoning (캐시 포이즈닝)**: ARP/DNS 캐시 테이블에 위조된 바인딩 정보를 주입하여 악성 서버로 트래픽을 유도하는 공격.

</details>

- 정의/개념: 계층별 식별자 위조를 **DAI·uRPF·DNSSEC**으로 검증
- 배경/필요성: 초기 인터넷 프로토콜(TCP/IP) 설계 시 보안성과 신원 검증 메커니즘의 부재로 인해, 공격자가 L2의 MAC 주소(ARP), L3의 IP 주소(IP), L7의 도메인 질의(DNS) 등 네트워크 식별자를 임의로 위변조(Spoofing)하여 중간자 공격(MITM), 세션 하이재킹 및 반사 증폭 분산 서비스 거부 공격(DRDoS)을 감행할 때 정상 발신지 추적이 불가능하고 트래픽이 악성 사이트로 우회되는 심각한 보안 위협을 초래함에 따라, 계층별 발신지 신원 무결성을 실시간 검증하는 L2 DAI(Dynamic ARP Inspection), L3 uRPF(Unicast Reverse Path Forwarding)/BCP 38 및 L7 DNSSEC 공개키 전자서명 체계를 도입하여 **위조 식별자 기반 패킷 유입 원천 차단, 트래픽 도청·변조 방어 및 네트워크 가용성과 기밀성**을 달성할 필요

#### 한줄 요약
- 계층별 다중 취약점 악용을 차단하고, DAI, uRPF, DNSSEC을 통해 발신지 무결성을 검증한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **MITM (Man-In-The-Middle, 중간자 공격)**: 통신하는 두 호스트 사이에 끼어들어 트래픽을 가로채 도청하거나 데이터를 변조하는 공격 형태.
- **Traceback 무력화**: 패킷의 Source IP를 위조함으로써 실제 공격자의 물리적 위치와 발신지 추적을 불가능하게 만드는 특성.

</details>

- **계층별 다중 공격 벡터**: L2 브로드캐스트 도메인(ARP), L3 라우팅 경계(IP), L7 네임 서비스(DNS) 악용
- **중간자 공격(MITM) 및 도청(Sniffing)**: 정상 트래픽 경로를 공격자 호스트로 우회시켜 **자격 증명 및 세션 탈취**
- **발신지 역추적(Traceback) 무력화**: 위조된 IP를 기반으로 **반사 증폭(DRDoS) 공격을 수행하여 공격자 은닉**

#### 한줄 요약
- 계층별 다중 취약점 악용, 중간자 공격(MITM)을 통한 도청, IP 위조를 통한 공격자 은닉을 특징으로 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DHCP Snooping & DAI**: 신뢰할 수 없는 포트의 가짜 DHCP를 차단하고 생성된 바인딩 DB로 비인가 ARP를 필터링하는 L2 보안.
- **uRPF (Unicast Reverse Path Forwarding)**: 패킷 수신 시 FIB 라우팅 테이블의 역경로를 검사하여 위조된 출발지 IP 패킷을 즉시 드롭하는 L3 보안.

</details>

```text
[계층별 스푸핑 공격 및 방어 아키텍처]
|-- L7 Application Layer (DNS Spoofing / Cache Poisoning)
|   `-- Defense: DNSSEC (공개키 전자서명 RRSIG 검증, 신뢰 체인 DS/DNSKEY)
|-- L3 Network Layer (IP Spoofing / DRDoS 반사 공격)
|   `-- Defense: uRPF (Strict/Loose 역경로 검사) + BCP 38 (Ingress Filtering)
`-- L2 Data Link Layer (ARP Spoofing / Gratuitous ARP 변조)
    `-- Defense: DAI (Dynamic ARP Inspection) + DHCP Snooping Binding Table
```

선의 의미: L2부터 L7까지 발생하는 계층별 식별자 위조 공격을 각 계층의 전용 검증 엔진(DAI, uRPF, DNSSEC)으로 차단하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **DAI·DHCP Snooping** | ARP와 신뢰 바인딩 대조 |
| **uRPF·BCP 38** | 출발지 주소의 역경로·대역 검증 |
| **DNSSEC 검증기** | 서명된 DNS 데이터의 무결성 검증 |

#### 한줄 요약
- L2는 DAI/DHCP Snooping, L3는 uRPF/BCP 38, L7은 DNSSEC을 통해 계층별 위변조를 방어한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Gratuitous ARP (GARP)**: 자신의 IP-MAC 정보를 네트워크에 브로드캐스트하여 캐시를 갱신시키는 ARP 패킷으로 악의적 오염에 악용됨.

</details>

```text
계층별 스푸핑 패킷 검증 및 차단 파이프라인
        │
   1. [L2 ARP 패킷 인입] 스위치의 DAI 엔진이 Untrusted 포트의 ARP 패킷을 인터셉트
        │
   2. [DHCP Snooping 대조] IP-MAC 바인딩 불일치 시 즉각 ARP 패킷 드롭 및 포트 보안 위반 경보
        │
   3. [L3 IP 패킷 인입] 라우터가 수신 인터페이스와 Source IP의 FIB 역경로 일치 여부(uRPF) 검사
        │
   4. [FIB 불일치 패킷 폐기] 비인가 대역 및 비대칭 경로 위조 패킷을 하드웨어 레벨에서 드롭
        │
   ▼
5. [L7 DNS 서명 검증] DNSSEC 리졸버가 RRSIG 전자서명을 검증하여 위조 응답 거부 및 정상 IP 해석
```

- 1. L2 ARP 패킷 인입: 비신뢰 포트 ARP 검사
- 2. DHCP Snooping 대조: IP·MAC 바인딩 검증
- 3. L3 IP 패킷 인입: 출발지 역경로 검사
- 4. FIB 불일치 패킷 폐기: 정책 위반 패킷 차단
- 5. L7 DNS 서명 검증: DNSSEC 신뢰 체인 확인

#### 한줄 요약
- 상위 계층으로 갈수록 검증 비용이 커지므로, 위조 트래픽은 발신지에 가까운 지점에서 걸러낼수록 방어 단가가 낮아진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ARP Spoofing vs IP Spoofing vs DNS Spoofing**: LAN 도청(ARP), WAN 반사 공격(IP), 전역 피싱 유도(DNS).

</details>

| 비교 항목 | ARP 스푸핑 (L2 Spoofing) | IP 스푸핑 (L3 Spoofing) | DNS 스푸핑 (L7 Spoofing) |
|:---|:---|:---|:---|
| 위조 대상 | IP·MAC 바인딩 | 출발지 IP 주소 | DNS 자원 레코드 |
| 공격 범위 | 동일 L2 도메인 | 라우팅 경계와 반사 서비스 | 오염된 캐시 이용자 |
| 공격 목적 | MITM·세션 도청 | 반사 공격·발신지 은닉 | 악성 목적지 유도 |
| 핵심 방어 | **DAI·DHCP Snooping** | **uRPF·BCP 38** | DNSSEC 서명 검증 |

#### 한줄 요약
- ARP는 LAN 내부 도청용, IP는 WAN 증폭 공격용, DNS는 전역 피싱 사이트 유도용으로 악용된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Asymmetric Routing (비대칭 라우팅)**: 송신 경로(ISP A)와 수신 경로(ISP B)가 상이한 멀티호밍 환경으로, Strict uRPF 적용 시 정상 트래픽이 오차단될 수 있어 Loose uRPF를 적용해야 하는 환경.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| LAN 내부 호스트의 GARP 오염으로 인한 게이트웨이 트래픽 탈취(MITM) | 스위치 전 포트에 **`DHCP Snooping 활성화 및 DAI` 적용** | 비인가 ARP 변조 패킷 100% 드롭 및 도청 원천 차단 |
| 위조된 Source IP를 악용한 **NTP/DNS 반사 증폭 공격(DRDoS)** 유입 | 네트워크 경계 라우터에 **`BCP 38 인그레스 필터링 및 uRPF` 구성** | 위조 발신지 패킷 사전 폐기 및 DRDoS 트래픽 95% 차단 |
| DNS 캐시 포이즈닝으로 인한 전사 사용자의 악성 파밍 사이트 유도 | 재귀 리졸버에 **`DNSSEC 유효성 검증` 활성화 및 소스 포트 무작위화** | 위조 DNS 응답 패킷 거부 및 도메인 무결성 100% 보장 |
| 멀티홈 ISP 환경에서 Strict uRPF 오동작으로 정상 트래픽 드롭 | 비대칭 라우팅 구간에 **`Loose uRPF 모드` 적용** | 정상 패킷 오차단 방지 및 출발지 IP 유효성 검증 유지 |

#### 한줄 요약
- DAI로 내부 ARP 도청을 막고, uRPF/BCP 38로 IP 위조를 차단하며, DNSSEC으로 캐시 포이즈닝을 방어한다.

## Ⅶ. 결론

- 내부망 도청(ARP), 글로벌 DRDoS 공격의 근원지 은닉(IP), 전사 파밍 유도(DNS) 등 모든 사이버 침해 사고의 시발점이 되는 식별자 위변조를 계층별 심층 방어로 차단하는 **엔터프라이즈 및 ISP 네트워크 보안의 가장 기초적이며 핵심적인 필수 방어 아키텍처**로 확립되었으며, 제로 트러스트(Zero Trust) 아키텍처 및 mTLS 상호 인증과 융합하는 가운데, 실무 인프라 보안 구축 시에는 **스위치 전 포트 대상 DHCP Snooping 바인딩 기반 DAI 활성화, 멀티홈 환경 비대칭 라우팅 오차단을 방지하는 Loose uRPF 튜닝 및 BCP 38 인그레스 필터링 의무화, 도메인 하이재킹을 방지하는 DNSSEC 전자서명 검증 체계 구축**을 결합하여 완벽한 네트워크 식별자 무결성을 완성

#### 한줄 요약
- DAI, uRPF, DNSSEC과 제로 트러스트 mTLS를 결합하여 다계층 스푸핑 방어 체계를 구현한다.
