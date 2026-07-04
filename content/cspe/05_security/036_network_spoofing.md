---
title: "네트워크 스푸핑 ARP·IP·DNS (Network Spoofing)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 36
---

# 📖 【암기용】 개념 완전 이해

> 목적: 네트워크 스푸핑을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 통신 상대·주소·이름을 위조해 트래픽을 가로채거나 우회시키는 공격
- **왜 필요한가**: 네트워크는 MAC, IP, DNS 같은 식별자를 믿고 전달한다. 이 식별자가 위조되면 정상 서버로 가야 할 패킷이 공격자에게 향한다.
- **핵심 직관**: 택배 송장 주소나 발신자 이름을 바꿔 중간에서 물건을 받는 행위와 같다.

## 깊이 이해
- **배경·문제의식**: ARP는 LAN에서 IP와 MAC을 연결하지만 인증이 없다. IP는 출발지 주소를 쉽게 조작할 수 있고, DNS는 이름을 IP로 바꾸는 과정이 오염되면 사용자가 위조 사이트로 이동한다.
- **작동 원리**: ARP 스푸핑은 게이트웨이 MAC을 공격자 MAC으로 속여 MITM을 만든다. IP 스푸핑은 출발지 IP를 위조해 ACL 우회나 반사 공격에 쓴다. DNS 스푸핑은 캐시 오염, 가짜 응답, 레코드 변조로 도메인을 다른 IP에 매핑한다.
- **비유**: 회사 안내데스크가 방문자의 명함만 보고 신원을 믿으면, 위조 명함을 든 사람이 회의실 출입과 우편 수령을 동시에 할 수 있다.
- **구체 예시**: 같은 VLAN에서 공격자가 `192.168.10.1 is-at aa:bb:cc` ARP 응답을 초당 5회 전송하면 PC의 ARP 캐시가 오염되고 HTTP 세션 쿠키가 평문 구간에서 노출될 수 있다.
- **흔한 오해·주의점**: 스푸핑은 암호화만으로 끝나지 않는다. TLS는 콘텐츠를 보호하지만 ARP/DNS 오염, 인증서 경고 무시, 메일 도메인 위조는 별도 통제가 필요하다.

## 연결 개념
- MITM - 스푸핑으로 트래픽 경로를 공격자에게 통과시키는 중간자 공격
- DHCP Snooping/DAI - 스위치에서 ARP 위조를 차단하는 L2 통제
- DNSSEC/SPF-DKIM-DMARC - DNS·메일 위조 검증 체계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 스푸핑 답안은 공격 종류 나열이 아니라 위조 지점, 탐지 로그, 차단 위치, 인증 검증을 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 네트워크 스푸핑은 ARP·IP·DNS 식별자를 위조해 인증되지 않은 신뢰 관계를 악용하는 공격임.
> 2. **가치**: 대응은 L2 스위치, 라우터, DNS, 메일 인증 지점별로 차단 위치를 나누어 설계해야 함.
> 3. **판단 포인트**: DAI, uRPF/BCP 38, DNSSEC, SPF-DKIM-DMARC, SIEM 상관분석을 함께 제시해야 채점 포인트 충족.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 스푸핑 유형 구분 확인 | ARP, IP, DNS, 메일 위조의 계층·공격면 차이 | 스푸핑을 피싱이나 스니핑과 혼동 |
| 통제 위치 판단 확인 | L2 DAI, L3 uRPF, DNSSEC, 메일 DMARC | 암호화만 제시하고 네트워크 차단 지점 누락 |
| 탐지·대응 운영 확인 | ARP 테이블 변동, DNS NXDOMAIN, SPF fail 로그 | 공격 절차·침해 지표 없이 방어 제품만 나열 |

> 요약: 스푸핑 문제는 위조 계층별 공격 절차와 차단 위치를 대응시켜야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 네트워크 식별자 위조 공격
- 배경: ARP, IP, DNS, 메일 발신자는 네트워크 신뢰의 기준이지만 인증 없는 응답과 캐시 신뢰 때문에 조작될 수 있음.
- 필요성: DAI, uRPF/BCP 38, DNSSEC, DMARC를 계층별로 적용하고 MAC 변경·SPF fail·DNSSEC 실패 로그를 SIEM에서 상관분석해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
공격자 -> 식별자 위조
  / ARP: Gateway IP를 공격자 MAC에 매핑
  / IP: Source IP 위조로 ACL 우회·반사 유발
  / DNS: 도메인 응답·캐시 오염
사용자 트래픽 -> 공격자 경유/위조 목적지 -> 정보 탈취/세션 변조
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| ARP 스푸핑 | IP-MAC 매핑 위조 | 같은 VLAN, MITM, DAI로 차단 |
| IP 스푸핑 | 출발지 IP 주소 위조 | uRPF, ingress/egress filtering 적용 |
| DNS 스푸핑 | 도메인-IP 응답 조작 | DNSSEC, DoT/DoH, resolver hardening |
| 메일 스푸핑 | 발신 도메인·헤더 위조 | SPF, DKIM, DMARC 검증 |

> 요약: 스푸핑은 계층별 식별자를 위조하므로 L2, L3, DNS, 메일 인증 통제를 분리해야 함.

---

## Ⅲ. 동작원리 및 흐름도

```text
대상 식별자 선택 -> 위조 패킷/응답 전송 -> 캐시·라우팅·정책 오염
-> 트래픽 경로 변경 -> 세션 탈취/피싱/반사 공격 -> 로그 상관분석
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 공격자가 ARP/IP/DNS 위조 대상 식별 | 동일 VLAN, DNS resolver, 메일 도메인 확인 |
| 2 | 위조 응답·패킷을 정상 응답보다 먼저 전달 | ARP reply 급증, DNS TTL 불일치 |
| 3 | 피해자의 캐시·정책·경로가 오염 | MAC 변동, source IP bogon, SPF fail |
| 4 | 트래픽 탈취·우회·피싱 발생 | 프록시 로그, NetFlow, SIEM 경보 |
| 5 | DAI, uRPF, DNSSEC, DMARC로 차단 | 차단율, 오탐, 재시도 횟수 점검 |

> 요약: 공격은 위조 응답으로 신뢰 캐시를 오염시키고, 대응은 위조 입력을 차단한 뒤 로그로 경로 변조를 확인함.

---

## Ⅳ. 특징

| 구분 | 단순 네트워크 신뢰 | 스푸핑 대응 체계 | 수치·로그 포인트 |
|:---|:---|:---|:---|
| ARP | 호스트 캐시 신뢰 | DHCP Snooping + Dynamic ARP Inspection | MAC 변경 이벤트 1분 3회 이상 경보 |
| IP | 출발지 주소 신뢰 | uRPF, BCP 38 ingress filtering | bogon source 0건 목표 |
| DNS | 응답 캐시 신뢰 | DNSSEC validation, resolver ACL | SERVFAIL/NXDOMAIN 비율 기준선 관리 |
| 메일 | From 헤더 신뢰 | SPF, DKIM, DMARC p=quarantine/reject | DMARC fail 보고서 일 단위 분석 |

> 요약: 스푸핑 대응은 식별자 신뢰를 암묵 신뢰에서 검증 기반 신뢰로 바꾸는 통제임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 평면 VLAN, 캐시 신뢰 | VLAN 분리, DAI, DNSSEC | 동일 브로드캐스트 도메인 사용자 50명 이상 |
| 탐지 | 단일 장비 로그 | ARP, DNS, NetFlow, 메일 로그 상관 | SIEM correlation rule 적용 |
| 운영/위험 | 사후 사용자 신고 | 차단 정책과 인증 검증 | 업무 DNS·메일 오탐률 1% 이하 |

> 요약: 내부망은 DAI와 VLAN 분리, 인터넷 구간은 uRPF와 DNSSEC·DMARC를 우선 적용함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 내부 MITM | ARP 캐시 오염 | DHCP Snooping, DAI, static ARP for gateway | ARP spoof 차단 로그 |
| 반사 공격 악용 | 출발지 IP 위조 | uRPF, BCP 38, egress ACL | spoofed packet drop count |
| 도메인 탈취 | DNS 캐시 오염·위조 응답 | DNSSEC validation, resolver 접근통제 | DNSSEC validation fail |
| 메일 사칭 | SPF/DKIM/DMARC 미구성 | DMARC p=reject, rua 보고서 분석 | spoof mail quarantine count |

> 요약: 주요 리스크는 MITM, 반사 공격, 도메인·메일 사칭이며 차단 로그와 검증 실패 로그로 확인함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| ARP 통제 | DAI 적용 VLAN 100%, gateway MAC 변경 0건 | 스위치 로그, NAC 점검 |
| IP 통제 | 사설·bogon source drop 100% | 라우터 ACL/uRPF 카운터 |
| DNS/메일 | DNSSEC 검증, DMARC reject 적용 | resolver 로그, DMARC aggregate report |

> 요약: 성공 여부는 계층별 위조 차단율, 정상 서비스 오탐률, 검증 로그 완전성으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 내부망 통제: DHCP Snooping, DAI, IP Source Guard를 사용자 VLAN 100%에 적용하고 ARP 변동 로그를 SIEM으로 전송함.
2. 경계망 통제: uRPF strict/loose mode와 BCP 38 ingress/egress filtering으로 위조 source IP 패킷을 라우터에서 차단함.
3. 이름·메일 검증: DNSSEC validation, resolver ACL, SPF-DKIM-DMARC p=quarantine/reject를 적용하고 fail 보고서를 일 단위 분석함.

**결론 (2줄):**
- 기술사 판단: 내부 MITM 위협은 L2 DAI, 인터넷 반사 공격은 L3 uRPF, 도메인·메일 사칭은 DNSSEC와 DMARC로 분리 대응해야 함.
- 향후 방향: Zero Trust 네트워크에서는 IP·MAC 신뢰보다 mTLS, device posture, identity 기반 정책으로 통신 주체를 검증함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "스푸핑 공격을 설명하시오" | ARP/IP/DNS/메일 위조 절차 | 계층별 차단 위치와 탐지 로그 |
| 요구사항 명시형 | "대응 방안을 제시하시오" | 공격 절차별 DAI, uRPF, DNSSEC, DMARC 적용 | 차단 정책, 오탐 기준, 재발 방지 |

> 요약: 설명형은 유형 구분을, 방안형은 차단 위치·검증 로그·정책 지표를 중심으로 작성함.
