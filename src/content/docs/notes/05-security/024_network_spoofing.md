---
sidebar:
  order: 24
  label: "024. 네트워크 스푸핑 - ARP•IP•DNS (Network Spoofing)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "네트워크 주소 위변조 및 중간자 공격 : 계층별 스푸핑 (ARP, IP, DNS Spoofing)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 24
extra:
  question_no: "024"
  source_status: "기출"
  source_history: "128회, 134회"
  priority: 70
  priority_note: "L2(ARP Spoofing/DAI), L3(IP Spoofing/uRPF BCP 84), L7(DNS Spoofing/DNSSEC), MITM 및 세션 하이재킹"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **스푸핑(Spoofing / 주소 위장 공격)**: 공격자가 승인된 정상 호스트, 게이트웨이, 또는 신뢰 서버의 고유 식별자(L2 MAC, L3 IP, L7 도메인 질의응답)를 불법 위조하여, 피해 시스템을 기만하고 트래픽을 가로채거나(중간자 공격: MITM) 통제 정책을 우회하는 공격 기법.
- **중간자 공격(Man-in-the-Middle, MITM)**: 두 통신 호스트 사이의 정상적인 네트워크 트래픽 경로를 공격자 호스트로 강제 우회시켜, 송수신되는 평문 데이터를 실시간 도청(Sniffing)하거나 패킷 내용을 임의 변조(Tampering)하는 침해 공격.

</details>

- 정의/개념: 데이터 링크(L2: ARP), 네트워크(L3: IP), 애플리케이션(L7: DNS) 계층의 **주소 해석 및 라우팅 프로토콜 내 무인증 취약점** 을 악용하여 통신 경로를 장악하는 **계층별 주소 위변조 공격 및 방어 아키텍처**
- 배경/필요성: 초기 인터넷 표준 프로토콜들이 발신자의 진위 여부를 검증하는 암호학적 인증 메커니즘 없이 설계됨에 따라, 주소 스푸핑을 통한 자격증명 탈취 및 대규모 반사 DDoS(DRDoS) 위협을 원천 방어할 계층별 대책 요구

#### 한줄 요약
- L2(MAC), L3(IP), L7(DNS)의 무인증 프로토콜 취약점을 악용한 주소 위조를 계층별 보안 기술로 방어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **동적 ARP 검사(Dynamic ARP Inspection, DAI)**: L2 스위치가 DHCP Snooping 바인딩 데이터베이스를 참조하여, 포트로 인입되는 모든 ARP 응답 패킷의 IP-MAC 매핑 일치 여부를 하드웨어 ASIC 레벨에서 실시간 검증하고 불일치 시 폐기하는 기술.
- **단일 경로 역방향 전달 검사(Unicast Reverse Path Forwarding, uRPF / BCP 84)**: 라우터가 인입된 패킷의 출발지 IP 주소를 라우팅 FIB 테이블과 대조하여, 해당 인터페이스로 돌아가는 최적 역방향 경로가 존재하지 않는 위조된 IP 패킷을 즉시 드롭하는 L3 보안 기술.

</details>

- **계층별 독립적 공격 벡터**: L2는 로컬 브로드캐스트 도메인 장악(ARP), L3는 반사 DDoS 증폭 및 방화벽 우회(IP), L7은 피싱 사이트 강제 파밍(DNS)
- **비대칭적 공격 용이성**: 공격자는 단 1개의 위조된 응답 패킷을 피해자 캐시 테이블에 먼저 도달(Race Condition)시키는 것만으로 오염 성공
- **계층별 전용 방어 기제 (DAI, uRPF, DNSSEC)**: L2 스위치(DAI/DHCP Snooping), L3 라우터(uRPF/BCP 38), L7 네임서버(DNSSEC/mTLS)의 통합 적용 필수

#### 한줄 요약
- 계층별 독립 벡터, 비대칭 캐시 오염 취약성, DAI/uRPF/DNSSEC 계층형 방어 기제를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DNSSEC(DNS Security Extensions / RFC 4033)**: DNS 응답 데이터(RRset)에 권한 있는 네임서버의 비대칭 개인키로 전자서명(RRSIG)을 부착하고, 상위 루트 도메인부터의 공개키 신뢰 체인(DS 레코드)을 통해 응답 데이터의 위변조 여부를 수학적으로 검증하는 확장 규격.

</details>

```text
[ 1. L2 영역: ARP Spoofing 방어 ]
[ 피해자 단말 ] ── (가짜 ARP Reply 차단) ──▶ [ L2 스위치: DAI + DHCP Snooping DB ] ──▶ [ 정규 게이트웨이 ]

[ 2. L3 영역: IP Spoofing 방어 ]
[ 외부 공격자 (출발지 IP 변조) ] ──▶ [ 인터넷 경계 라우터: uRPF (BCP 84) 필터링 ] ── (위조 패킷 폐기)

[ 3. L7 영역: DNS Spoofing 방어 ]
[ 로컬 리졸버 DNS ] ── (RRSIG 전자서명 검증) ──▶ [ DNSSEC 신뢰 체인 (Root -> TLD -> Authoritative) ]
```

선의 의미: L2 스위치에서는 DAI가 MAC을 검증하고, L3 라우터에서는 uRPF가 출발지 IP를 검증하며, L7 DNS에서는 DNSSEC이 전자서명을 검증하여 계층별 스푸핑을 차단하는 구조

| 공격 유형 | 취약점 실체 및 공격 메커니즘 | 핵심 방어 기제 및 대책 | 표준/규격 |
|:---|:---|:---|:---|
| **ARP 스푸핑 (L2)** | ARP 프로토콜의 무인증 캐시 갱신을 악용해 게이트웨이 MAC 변조 | **L2 스위치 DAI(Dynamic ARP Inspection) 및 정적 ARP 매핑** | IEEE 802.1Q |
| **IP 스푸핑 (L3)** | IP 헤더의 출발지 주소 무검증을 악용해 DRDoS 반사 공격 수행 | **라우터 uRPF(Strict/Loose Mode) 및 Ingress Filtering** | IETF BCP 84 / RFC 3704 |
| **DNS 스푸핑 (L7)** | DNS 질의 시 트랜잭션 ID(TXID) 추측 기반 가짜 캐시 응답 주입 | **DNSSEC(RRSIG/DS 레코드 검증) 및 DNS-over-HTTPS(DoH)**| IETF RFC 4033 |
| **종단 세션 보호**| 네트워크 경로가 장악되더라도 페이로드 기밀성/무결성 보증 | **전 구간 mTLS(Mutual TLS 1.3) 상호 인증 강제** | RFC 8446 |

#### 한줄 요약
- L2 DAI(스위치), L3 uRPF(라우터), L7 DNSSEC(네임서버), 종단 mTLS(인증서)가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DNS 캐시 포이즈닝(DNS Cache Poisoning)**: 공격자가 캐시 DNS 리졸버가 권한 네임서버로 질의를 보낸 직후, 무작위 트랜잭션 ID(TXID: 16비트)와 출발지 포트를 브루트포스 추측하여 위조된 응답 패킷을 먼저 주입함으로써 캐시를 오염시키는 공격.

</details>

```text
1. [공격 시작] 공격자가 정상 응답 패킷보다 빠른 타이밍에 위조된 응답(ARP Reply / DNS Answer) 송출
            │
            ▼
2. [캐시 오염] 피해 호스트의 ARP Table 또는 리졸버의 DNS Cache가 위조된 매핑 정보로 강제 갱신
            │
            ▼
3. [경로 장악] 피해자의 모든 네트워크 패킷이 정상 게이트웨이가 아닌 공격자의 중간자 노드로 강제 라우팅
            │
            ▼
4. [도청/변조] 공격자가 패킷을 포워딩하면서 평문 세션 토큰 스니핑 또는 페이로드 내 악성코드 주입
            │
            ▼
5. [계층형 방어 가동 시]: DAI 포트 차단, uRPF 역방향 경로 불일치 드롭, DNSSEC RRSIG 검증 실패로 패킷 즉시 폐기
```

**동작 원리**

1. **Race Condition 유발**: 정상 서버의 지연시간을 틈타 스푸핑 패킷을 대량 선제 주입
2. **무인증 테이블 덮어쓰기**: 상태 머신 없이 수신된 응답을 그대로 신뢰하여 메모리 테이블 변조
3. **트래픽 가로채기(MITM)**: 패킷의 목적지 MAC/IP가 공격자로 변조되어 공격자 인터페이스로 수신
4. **암호화 부재 시 정보 유출**: 평문 HTTP 트래픽의 쿠키, 패스워드가 공격자 와이어샤크에 노출
5. **결정론적 방어 차단**: DAI/uRPF/DNSSEC 하드웨어 검증에 의해 비인가 패킷이 도달 전 드롭

#### 한줄 요약
- Race Condition 유발, 캐시 테이블 오염, MITM 경로 우회, 평문 도청, 계층별 검증 차단 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **L2 vs L3 vs L7 스푸핑 비교**: 공격 영역, 공격 기법, 파급 효과, 방어 기술의 비교.

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

- **IETF BCP 38 / BCP 84 (Ingress Filtering & uRPF)**: 인터넷 서비스 제공자(ISP) 및 엔터프라이즈 네트워크 경계 라우터에서, 내부 가입자 서브넷 범위를 벗어난 위조된 출발지 IP 패킷이 인터넷 백본으로 유출되지 않도록 강제 필터링하는 글로벌 인터넷 표준 권고안.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 사내 LAN 내부 악의적 사용자의 ARP Spoofing으로 인한 **사내망 패킷 도청 및 자격증명 탈취** | **L2 스위치에 DHCP Snooping 바인딩 기반 Dynamic ARP Inspection(DAI)** 활성화 | 위조된 ARP 패킷 하드웨어 레벨 100% 폐기 및 LAN 내부 MITM 원천 차단 |
| 인터넷 공격자가 출발지 IP를 피해자 IP로 위조하여 유발하는 **대규모 반사 증폭 DDoS(DRDoS) 공격** | **경계 라우터에 IETF BCP 84 표준 uRPF Strict Mode 및 인그레스 ACL 적용** | 위조된 출발지 IP 패킷 유입 즉시 드롭 및 반사 공격 인프라 악용 차단 |
| DNS 캐시 포이즈닝으로 사내 임직원이 피싱 사이트로 납치되어 발생하는 **전사 계정 유출 사고** | **RFC 4033 DNSSEC 서명 검증 강제 및 종단 간 상호 인증(mTLS 1.3)** 전면 적용 | 위조된 DNS 응답 무효화 및 암호학적 신뢰 체인 기반 통신 진본성 보장 |

#### 한줄 요약
- L2 스위치 DAI로 ARP를 막고, 라우터 uRPF로 IP 위조를 차단하며, DNSSEC/mTLS로 DNS를 보호한다.

## Ⅶ. 결론

- 네트워크 통신의 근간인 주소 체계의 신뢰성을 위협하는 **스푸핑(Spoofing) 공격**은 단일 솔루션으로 방어할 수 없으며, 실무 구현 시 **L2 스위치의 DAI 및 DHCP Snooping 구축**, **L3 라우터의 uRPF Strict 모드 적용**, **L7 네임서버의 DNSSEC 및 전 구간 mTLS 상호 인증**을 결합한 계층형 다중 검증 체계를 확립하여 무결점 네트워크 주소 보안을 완성

#### 한줄 요약
- L2 DAI, L3 uRPF, L7 DNSSEC 및 종단 mTLS 상호 인증을 통해 주소 위변조와 중간자 도청을 원천 차단한다.
