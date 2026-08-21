---
sidebar:
  order: 86
  label: "086. 네트워크 스푸핑 (ARP•IP•DNS)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "네트워크 식별자 위변조 공격 및 방어 : ARP, IP, DNS 스푸핑 (Network Spoofing)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
weight: 86
extra:
  question_no: "086"
  source_status: "기출"
  source_history: "128회, 134회"
  priority: 70
  priority_note: "L2 ARP 스푸핑(DAI), L3 IP 스푸핑(uRPF/BCP 38), L7 DNS 스푸핑(DNSSEC) 및 캐시 오염 방어"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **스푸핑(Spoofing)**: 송신자의 신원 식별자(L2 MAC, L3 IP, L7 도메인 질의 ID 등)를 악의적으로 위변조하여 정당한 인가 권한을 획득하거나, 통신 트래픽을 가로채 도청/변조(Man-in-the-Middle)하고 서비스 거부(DDoS)를 유발하는 기만형 사이버 공격.
- **캐시 포이즈닝(Cache Poisoning)**: 로컬 호스트나 DNS/스위치 장비의 주소 해석 캐시 테이블(ARP Table, DNS Cache)에 조작된 바인딩 정보를 주입하여 영구적으로 악성 서버로 트래픽을 유도하는 공격.

</details>

- 정의/개념: 전통적 비인가 TCP/IP 통신 환경의 신뢰성 결함을 악용하여 **L2(ARP), L3(IP), L7(DNS)** 계층의 주소 체계를 위조하는 공격에 대해, 계층별 검증 메커니즘(**DAI, uRPF/BCP 38, DNSSEC**)을 통해 발신지 무결성을 검증하고 방어하는 **네트워크 식별자 방어 체계**
- 배경/필요성: 초기 인터넷 프로토콜의 발신지 인증(Source Authentication) 부재로 인한 내부망 도청, 증폭 DRDoS 공격 및 파밍(Phishing) 위협에 대응하여 제로 트러스트 기반의 패킷 발신지 검증을 구현할 요구

#### 한줄 요약
- L2/L3/L7 계층별 주소 위변조를 탐지하고 DAI, uRPF, DNSSEC을 통해 트래픽 탈취 및 캐시 오염을 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **역경로 포워딩 검사(Unicast Reverse Path Forwarding, uRPF)**: 라우터가 수신한 패킷의 출발지 IP 주소를 자신의 FIB(포워딩 정보 베이스) 라우팅 테이블과 대조하여, 수신된 인터페이스가 해당 출발지로 되돌아가는 최적 경로와 일치하는지 역검증하는 기법 (RFC 3704).
- **동적 ARP 검사(Dynamic ARP Inspection, DAI)**: 스위치 포트로 유입되는 무차별 ARP 응답 패킷을 감시하여, DHCP 스누핑 바인딩 데이터베이스와 일치하지 않는 비인가 ARP 패킷을 하드웨어 드롭하는 L2 보안 기술.

</details>

- **계층별 다중 공격 벡터**: L2 브로드캐스트 도메인(ARP), L3 라우팅 경계(IP), L7 네임 서비스(DNS) 등 네트워크 스택 전반에 걸친 취약점 악용
- **중간자 공격(MITM) 및 도청(Sniffing)**: 정상적인 송수신 경로를 공격자 호스트로 우회시켜 SSL/TLS 세션 탈취 및 자격 증명 유출
- **발신지 역추적(Traceback) 무력화**: 위조된 IP를 기반으로 반사 증폭(DRDoS) 공격을 수행하여 실제 공격자의 물리적 위치 은폐

#### 한줄 요약
- 계층별 다중 취약점 악용, 중간자 공격(MITM)을 통한 도청, IP 위조를 통한 공격자 은닉을 특징으로 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DHCP 스누핑(DHCP Snooping)**: 신뢰할 수 없는(Untrusted) 포트에서 발생하는 비인가 DHCP 서버 응답을 차단하고, 정상 할당된 IP-MAC-Port-VLAN 바인딩 데이터베이스를 생성하는 L2 감시 기능.
- **DNSSEC(DNS Security Extensions)**: 도메인 네임 질의 결과 레코드(RRset)에 공개키 기반 전자서명(RRSIG)과 신뢰 체인(DS/DNSKEY)을 결합하여 위변조를 방지하는 IETF 표준 (RFC 4033~4035).

</details>

```text
[ 계층별 스푸핑 공격 및 방어 아키텍처 ]

[ L7 계층: DNS Spoofing ] ────▶ [ 방어: DNSSEC (전자서명 RRSIG 검증 / DANE) ]
 ├─ 가짜 DNS 응답 주입             └─ 캐시 포이즈닝 원천 차단
 │
[ L3 계층: IP Spoofing ] ─────▶ [ 방어: uRPF (Strict/Loose Mode) + BCP 38 인그레스 필터링 ]
 ├─ 출발지 IP 변조/반사 공격       └─ FIB 역경로 불일치 패킷 즉시 드롭
 │
[ L2 계층: ARP Spoofing ] ────▶ [ 방어: Dynamic ARP Inspection (DAI) + DHCP Snooping ]
 └─ Gratuitous ARP 오염            └─ 스누핑 바인딩 테이블 대조 후 불일치 ARP 차단
```

선의 의미: L2부터 L7까지 발생하는 계층별 식별자 위조 공격을 각 계층의 전용 검증 엔진(DAI, uRPF, DNSSEC)으로 차단하는 방어 체계

| 계층 | 공격 유형 | 핵심 메커니즘 | 표준 방어 기술 |
|:---|:---|:---|:---|
| **L2 링크 계층** | **ARP Spoofing** | 위조된 MAC 주소를 담은 Gratuitous ARP 전송으로 피해자 ARP 캐시 오염 | **DAI (Dynamic ARP Inspection), IP Source Guard** |
| **L3 네트워크 계층** | **IP Spoofing** | 패킷 헤더의 Source IP를 희생자 IP로 위조하여 DRDoS 반사 공격 수행 | **uRPF (Strict/Loose), BCP 38 (Ingress Filtering)** |
| **L7 응용 계층** | **DNS Spoofing** | 트랜잭션 ID(TXID)를 예측하여 권한 네임서버보다 먼저 가짜 DNS 응답 주입 | **DNSSEC (RRSIG 검증), 0x20 인코딩, DoT/DoH** |

#### 한줄 요약
- L2는 DAI/DHCP Snooping, L3는 uRPF/BCP 38, L7은 DNSSEC을 통해 계층별 위변조를 방어한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Gratuitous ARP(GARP)**: 자신의 IP-MAC 매핑 정보를 로컬 네트워크 전체에 알리거나 IP 중복을 검사하기 위해 송출하는 브로드캐스트 ARP 요청/응답 패킷.

</details>

```text
1. 악성 호스트가 게이트웨이의 IP와 자신의 MAC 주소를 매핑한 악성 Gratuitous ARP 패킷 브로드캐스트
            │
            ▼
2. L2 스위치의 DAI 엔진이 인입 패킷을 인터셉트하여 DHCP Snooping 바인딩 DB 대조
            │
            ├─ [바인딩 일치] ➔ 정상 포워딩
            ▼
3. [바인딩 불일치 (위조 판정)] ➔ 스위치가 악성 ARP 패킷을 즉각 드롭하고 포트 보안 위반 경보 발생
            │
            ▼
4. 외부에서 위조된 Source IP를 가진 L3 패킷이 라우터 인터페이스로 인입 ➔ uRPF 역경로 검사 수행
            │
            ▼
5. FIB 테이블과 불일치 시 라우터 하드웨어에서 패킷 폐기 ➔ DNS 질의 시 DNSSEC 전자서명 검증 완료
```

**동작 원리**

1. **L2 검증(DAI)**: 스위치가 Untrusted 포트의 ARP 패킷을 가로채어 DHCP 스누핑 테이블과 1:1 비교
2. **L2 차단**: 미인가 MAC-IP 쌍은 즉각 폐기하고 포트 셧다운(Err-Disable) 실행
3. **L3 검증(uRPF)**: 라우터가 패킷 수신 인터페이스와 Source IP의 FIB 역방향 경로 일치 여부 확인
4. **L3 차단(BCP 38)**: 고객 네트워크에서 할당되지 않은 비인가 IP 대역의 외부 유출을 엣지에서 차단
5. **L7 검증(DNSSEC)**: 리졸버가 루트 CA부터 권한 네임서버까지의 공개키(DNSKEY) 서명 체인을 추적하여 응답 무결성 검증

#### 한줄 요약
- DAI 바인딩 검증, uRPF 역경로 검사, BCP 38 인그레스 필터링, DNSSEC 암호 서명 검증 순으로 방어한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Strict uRPF vs Loose uRPF**: 패킷이 수신된 인터페이스와 최적 반환 인터페이스가 정확히 1:1 일치해야 하는 엄격 모드와, FIB에 출발지 IP 경로가 존재하기만 하면 통과시키는 완화 모드(비대칭 라우팅 수용).

</details>

| 비교 항목 | ARP 스푸핑 (L2 Spoofing) | IP 스푸핑 (L3 Spoofing) | DNS 스푸핑 (L7 Spoofing) |
|:---|:---|:---|:---|
| **위조 대상 식별자** | **Ethernet MAC 주소** | **IPv4 / IPv6 출발지 주소** | **도메인 네임 A/AAAA 레코드** |
| **공격 유효 범위** | **동일 브로드캐스트 도메인 (LAN 내부)** | **글로벌 전송망 전 구간 (WAN)** | **DNS 캐시 공유 사용자 전원** |
| **주요 공격 목적** | 내부망 세션 도청, 자격증명 탈취 (MITM) | **DDoS 반사 증폭(NTP/DNS/SSDP), 신원 은닉** | 피싱 사이트 유도, 인증서 우회 |
| **핵심 방어 기술** | **DAI, Static ARP, 802.1X 포트 인증** | **uRPF (Strict/Loose), BCP 38** | **DNSSEC, DoH(DNS over HTTPS), 0x20** |

#### 한줄 요약
- ARP는 LAN 내부 도청용, IP는 WAN 증폭 공격용, DNS는 전역 피싱 사이트 유도용으로 악용된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **비대칭 라우팅(Asymmetric Routing)**: 송신 트래픽의 경로(ISP A)와 수신 트래픽의 경로(ISP B)가 상이한 멀티호밍(Multi-homing) 환경으로, Strict uRPF 적용 시 정상 트래픽이 오차단될 수 있는 환경.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| LAN 내부 악성 호스트의 Gratuitous ARP 오염으로 인한 게이트웨이 트래픽 탈취 (MITM) | 스위치 전 포트에 **DHCP Snooping 활성화 및 DAI(Dynamic ARP Inspection)** 적용 | 비인가 ARP 변조 패킷 100% 드롭 및 내부망 도청 차단 |
| 위조된 Source IP를 악용한 NTP/DNS 반사 증폭 분산 서비스 거부 공격(DRDoS) 유입 | 네트워크 경계 라우터에 **BCP 38 인그레스 필터링 및 Loose/Strict uRPF** 구성 | 위조 발신지 패킷 사전 폐기 및 DRDoS 반사 공격 트래픽 95% 억제 |
| DNS 캐시 포이즈닝으로 인한 전사 사용자의 악성 피싱/파밍 사이트 강제 접속 | 재귀 리졸버에 **DNSSEC 유효성 검증(Validation) 활성화 및 소스 포트 무작위화** 적용 | 위조 DNS 응답 패킷 거부 및 도메인 해석 무결성 100% 보장 |

#### 한줄 요약
- DAI로 내부 ARP 도청을 막고, uRPF/BCP 38로 IP 위조를 차단하며, DNSSEC으로 캐시 포이즈닝을 방어한다.

## Ⅶ. 결론

- 네트워크 통신의 신뢰성을 훼손하는 식별자 위조 위협에 대응하여 **L2 DAI**, **L3 uRPF 및 BCP 38**, **L7 DNSSEC**을 결합한 계층별 다중 방어 아키텍처를 구축하고, 종단 간 통신에는 **mTLS(상호 TLS)** 와 **Zero Trust Network Access(ZTNA)** 원칙을 통합 적용하여 주소 위조에 흔들리지 않는 제로 트러스트 보안 인프라를 완성

#### 한줄 요약
- DAI, uRPF, DNSSEC과 제로 트러스트 mTLS를 결합하여 다계층 스푸핑 방어 체계를 구현한다.
