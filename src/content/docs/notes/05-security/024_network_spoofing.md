---
sidebar:
  order: 24
  label: "024. 네트워크 스푸핑 - ARP•IP•DNS"
  badge:
    text: "기출 · 70%"
    variant: note
title: "네트워크 주소 위변조 및 중간자 공격 : 계층별 스푸핑"
date: "2026-08-26T14:28:24+09:00"
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

- 정의/개념: 주소 식별자를 위조해 경로를 장악하는 **계층별 공격**
- 배경/필요성: ARP·IP·DNS는 응답이 빨리 오는 쪽을 그대로 믿는 대가로 주소 해석 비용을 낮춘 무인증 프로토콜이므로, 각 계층에 바인딩 테이블·라우팅 테이블·전자서명이라는 대조 근거를 쥔 검증 계층을 덧대어 "먼저 온 응답"을 "출처가 증명된 응답"으로 바꿀 필요

#### 한줄 요약
- L2 MAC, L3 IP, L7 DNS 주소 위변조를 차단하여 중간자 가로채기와 반사 DDoS를 방어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DAI (Dynamic ARP Inspection)**: DHCP Snooping 바인딩 테이블을 참조하여 위조된 가짜 ARP 응답을 스위치 하드웨어에서 즉시 폐기하는 L2 보안.
- **uRPF (Unicast Reverse Path Forwarding, IETF BCP 84)**: 패킷의 출발지 IP가 라우팅 테이블 상의 역방향 인터페이스와 일치하지 않으면 패킷을 드롭하는 L3 보안.

</details>

- **계층별 공격 벡터**: ARP·IP·**DNS 식별자 위조**
- **캐시 오염**: 위조 응답의 **Race Condition** 악용
- **계층별 방어**: **DAI·uRPF·DNSSEC** 적용

#### 한줄 요약
- 세 공격은 계층만 다를 뿐 캐시가 응답을 검증 없이 신뢰한다는 같은 결함을 파고들므로, 방어 역시 계층마다 별개 기술을 쓰되 "응답에 출처 근거를 요구한다"는 한 가지 원리를 반복 적용한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DNSSEC (RFC 4033)**: DNS 응답 데이터에 전자서명(RRSIG)을 부착하고 루트 도메인부터의 신뢰 체인(DS 레코드)으로 위변조를 검증하는 표준.

</details>

```text
[계층별 스푸핑 방어]
|-- L2 DAI       : ARP 바인딩 검증
|-- L3 uRPF      : 출발지 역경로 검증
|-- L7 DNSSEC    : DNS 서명 검증
`-- 종단 mTLS    : 세션 상호 인증·암호화
```

선의 의미: L2 스위치에서는 DAI가 MAC을 검증하고 L3 라우터에서는 uRPF가 출발지 IP를 검증하며 L7 DNS에서는 DNSSEC이 전자서명을 검증하여 계층별 스푸핑을 차단하는 구조

| 구성요소 | 책임 |
|:---|:---|
| L2 DAI | DHCP 바인딩으로 **ARP 응답 검증** |
| L3 uRPF | FIB로 **출발지 역경로 검증** |
| L7 DNSSEC | **RRSIG 신뢰 체인** 검증 |
| 종단 mTLS | 세션 **상호 인증·암호화** |

#### 한줄 요약
- DAI·uRPF·DNSSEC은 각 계층의 장비가 이미 들고 있는 테이블을 대조 근거로 재활용해 검증 비용을 낮추는 반면, 어느 계층도 뚫린 경우를 대비한 최종 방어선은 경로를 믿지 않는 종단 mTLS가 맡는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DNS Cache Poisoning**: 캐시 DNS 리졸버에 무작위 트랜잭션 ID(TXID)를 추측하여 가짜 IP 매핑 응답을 선제 주입하는 공격.

</details>

```text
공격자 위조 응답
        |
  1. 식별자 검증
        +-- L2: DAI
        +-- L3: uRPF
        `-- L7: DNSSEC
                 |
       실패: 차단·기록
       성공: 종단 mTLS 검증
                 |
              정상 통신
```

동작 원리

1. 식별자 검증

#### 한줄 요약
- 계층 검증에서 걸린 위조는 장비 하드웨어가 폐기해 비용이 거의 들지 않지만, 통과한 위조는 경로 장악까지 진행되므로 mTLS가 세션 수립 시점에 다시 잡아내는 이중 비용을 치른다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ARP 스푸핑 (L2)**: 게이트웨이 MAC을 사칭한 ARP 응답을 브로드캐스트해 같은 브로드캐스트 도메인 안 단말의 ARP 캐시를 덮어씀으로써, 경로 자체를 공격자 단말로 끌어오는 LAN 한정 공격.
- **IP 스푸핑 (L3)**: 출발지 IP를 피해자 주소로 위조해 응답이 피해자에게 돌아가게 만듦으로써, 출발지 기반 ACL을 우회하거나 증폭 서버를 반사판으로 삼는 광역망 공격.
- **DNS 스푸핑 (L7)**: 리졸버가 정답을 받기 전에 트랜잭션 ID를 맞춘 가짜 응답을 먼저 밀어 넣어 캐시를 오염시킴으로써, 도메인 이름은 그대로 둔 채 접속 목적지만 바꾸는 공격.

</details>

| 비교 항목 | ARP 스푸핑 (L2) | IP 스푸핑 (L3) | DNS 스푸핑 (L7) |
|:---|:---|:---|:---|
| 동작 계층 | **L2** | **L3** | **L7** |
| 위조 식별자 | MAC 주소 | 출발지 IP | A/AAAA 레코드 |
| 공격 유효 범위 | LAN | 인터넷 광역망 | DNS 리졸버 캐시 |
| 주요 공격 목적 | MITM·세션 하이재킹 | 반사 DDoS·ACL 우회 | 피싱·파밍·계정 탈취 |
| 주요 방어 기제 | **DAI·DHCP Snooping** | **uRPF·BCP 38/84** | **DNSSEC·mTLS** |

#### 한줄 요약
- ARP는 LAN 내부 MITM용, IP는 광역망 반사 DDoS용, DNS는 글로벌 피싱 파밍용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IETF BCP 38 / BCP 84**: ISP 및 경계 라우터에서 위조된 출발지 IP 패킷이 인터넷 백본으로 유출되지 않도록 인그레스 필터링을 강제하는 표준 권고안.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| ARP 위조로 **자격증명 탈취** | **DHCP Snooping·DAI** 적용 | LAN MITM 차단 |
| IP 위조로 **반사 DDoS** | **uRPF·인그레스 ACL** 적용 | 위조 출발지 차단 |
| DNS 오염으로 **피싱 유도** | **DNSSEC·mTLS** 적용 | 응답 진본성과 세션 무결성 확보 |
| 비대칭 경로에서 **정상 패킷 차단** | **uRPF Loose·ACL 예외** | 정상 통신과 위조 방어 양립 |

#### 한줄 요약
- L2 스위치 DAI로 ARP를 막고, 라우터 uRPF로 IP 위조를 차단하며, DNSSEC/mTLS로 DNS를 보호한다.

## Ⅶ. 결론

- ARP 위조는 **DAI**, IP 위조는 **uRPF**, DNS 위조는 DNSSEC 적용

#### 한줄 요약
- 네트워크 스푸핑은 L2 DAI, L3 uRPF, L7 DNSSEC 및 종단 mTLS 상호 인증을 통해 주소 위변조와 중간자 도청을 원천 차단해야 한다.
