---
title: "네트워크 스푸핑 — ARP·IP·DNS (Network Spoofing)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 108
---

# 📖 【암기용】 개념 완전 이해

> 목적: ARP·IP·DNS 스푸핑을 계층별 공격 원리와 탐지 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 네트워크 식별 정보를 속여 트래픽을 가로채거나 잘못된 목적지로 보내는 공격
- **왜 필요한가**: LAN, IP, DNS는 빠른 연결을 위해 신뢰 기반 동작이 많고, 검증이 없으면 공격자가 주소·이름·출발지를 조작할 수 있다.
- **핵심 직관**: 우편 주소록을 몰래 바꿔 편지가 공격자 집으로 가게 하거나, 발신자 이름을 남의 이름으로 적는 행위와 같다.

## 깊이 이해
- **배경·문제의식**: ARP는 IP와 MAC 매핑을 검증 없이 갱신할 수 있고, IP는 출발지 주소를 패킷에 적는 구조라 위조가 가능하다. DNS는 캐시와 응답 신뢰성이 깨지면 사용자를 가짜 서버로 유도한다.
- **작동 원리**: ARP spoofing은 피해자 ARP cache에 공격자 MAC을 게이트웨이 MAC처럼 등록한다. IP spoofing은 출발지 IP를 위조해 반사 공격이나 세션 우회를 시도한다. DNS spoofing은 위조 응답이나 캐시 오염으로 도메인을 잘못 해석하게 한다.
- **비유**: 아파트 안내 데스크의 호수별 이름표를 바꿔 택배가 다른 집으로 가게 만드는 것과 같다.
- **구체 예시**: 공격자가 "게이트웨이 IP는 내 MAC"이라는 ARP reply를 반복 송신하면 피해자 트래픽이 공격자 장비를 거쳐 외부로 전달된다.
- **흔한 오해·주의점**: 스푸핑은 한 가지 공격이 아니라 계층별 식별자 위조이다. ARP는 L2, IP는 L3, DNS는 애플리케이션 이름 해석 계층으로 대응 위치가 다르다.

## 연결 개념
- DAI — Dynamic ARP Inspection
- BCP 38 — 송신지 주소 위조 방지 필터링
- DNSSEC — DNS 응답 무결성 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 스푸핑은 공격 원리와 대응 지표를 분리하고 ARP·IP·DNS 계층별 통제 위치를 정확히 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 네트워크 스푸핑은 MAC, IP, DNS 이름 등 식별 정보를 위조해 트래픽 경로·출처·목적지를 속이는 공격이다.
> 2. **가치**: 계층별 위조 원리를 구분하면 DAI, uRPF/BCP 38, DNSSEC, DHCP Snooping 등 대응 위치가 명확해진다.
> 3. **판단 포인트**: 공격 차단은 장비 설정뿐 아니라 ARP table 변동, spoofed packet, DNS validation failure 같은 지표 확인이 필요하다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 계층별 공격 원리 확인 | ARP cache poisoning, IP source spoofing, DNS cache poisoning | 세 공격을 동일 방화벽 규칙으로만 설명 |
| 대응 기술 매핑 확인 | DAI, DHCP Snooping, uRPF, DNSSEC, DoH 정책 | 보안 강화 같은 추상 문장 사용 |
| 탐지 지표 확인 | ARP 변동, spoofed source, DNS 응답 불일치 | 공격 원리와 지표를 섞어 서술 |

> 요약: 스푸핑 답안은 위조 대상, 공격 흐름, 대응 통제, 탐지 지표를 계층별로 나눠야 한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **네트워크 스푸핑 — ARP·IP·DNS** | 네트워크 스푸핑 — ARP·IP·DNS (Network Spoofing)의 핵심 개념 | "이 주제의 본질" |
| **프로토콜** | 통신 규칙의 표준화된 집합 | "공용 언어" |
| **패킷** | 네트워크를 통해 전송되는 데이터의 단위 | "택배 상자" |

---

## Ⅰ. 개요 및 필요성

- 개요: 식별자 위조 공격
- 배경: ARP·IP·DNS는 연결 편의와 호환성을 위해 일부 구간에서 송신자 정보를 신뢰함.
- 필요성: 위조 식별자는 MITM, 세션 탈취, 피싱, DDoS 반사 공격으로 이어지므로 계층별 검증이 필요함.
- 범위: ARP, IP, DNS 스푸핑 공격 원리와 DAI, uRPF, DNSSEC 대응을 포함함.

---

## Ⅱ. 구조 및 구성요소

```text
Attacker -> forged ARP/IP/DNS message -> Victim/Resolver/Router
ARP: Gateway IP -> Attacker MAC
IP: forged source IP -> reflection or bypass
DNS: domain -> fake IP response
Control: DAI / uRPF / DNSSEC / monitoring
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 공격자 | 위조 ARP·IP·DNS 메시지 생성 | MITM, 반사, 피싱 목적 |
| 피해 호스트 | 위조 정보를 캐시·수용 | ARP cache, DNS cache |
| 네트워크 장비 | 프레임·패킷 전달과 필터링 | switch, router, firewall |
| 이름해석 시스템 | 도메인과 IP 매핑 | resolver, authoritative DNS |
| 보안 통제 | 위조 식별자 검증·차단 | DAI, uRPF, DNSSEC |

> 요약: 스푸핑 구조는 공격자가 계층별 식별자를 위조하고 피해 시스템이 이를 신뢰할 때 성립한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
정상 식별자 탐색 -> 위조 메시지 생성 -> 피해 캐시/라우터 수용
-> 트래픽 경로 변경 또는 출처 은닉 -> 탐지 로그 발생
-> 계층별 검증 정책 적용
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 공격자가 게이트웨이·도메인·출발지 정보를 파악 | scan, sniffing 흔적 |
| 2 | ARP reply, forged IP, fake DNS response를 전송 | packet signature |
| 3 | 피해자가 위조 정보를 캐시에 반영 | ARP/DNS cache 변경 |
| 4 | 트래픽이 공격자 또는 가짜 서버로 이동 | route, flow log |
| 5 | DAI/uRPF/DNSSEC가 위조를 차단·기록 | drop count, validation fail |

> 요약: 스푸핑은 위조 메시지가 캐시나 라우팅 판단에 반영되는 순간 효과가 발생하며, 대응은 수용 지점에서 검증해야 한다.

---

## Ⅳ. 특징

| 구분 | ARP Spoofing | IP Spoofing | DNS Spoofing |
|:---|:---|:---|:---|
| 위조 대상 | IP-MAC 매핑 | 출발지 IP 주소 | 도메인-IP 응답 |
| 공격 효과 | LAN MITM | 반사 DDoS, 우회 | 피싱, 악성 서버 유도 |
| 대응 위치 | L2 Switch | Router/ISP Edge | Resolver/DNS |
| 기술 포인트 | DHCP Snooping, DAI | uRPF, BCP 38 | DNSSEC, cache policy |

> 요약: ARP·IP·DNS 스푸핑은 위조 대상과 통제 위치가 달라 하나의 대응 장비로 모두 해결되지 않는다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 계층별 대응 | 선택 기준 |
|:---|:---|:---|:---|
| LAN 내부 | 정적 ARP 일부 적용 | DHCP Snooping+DAI | 사용자 단말 많은 VLAN |
| 경계 라우팅 | ACL 수동 적용 | uRPF, BCP 38 필터 | 출발지 위조 차단 |
| DNS 보호 | 캐시 TTL 조정 | DNSSEC validation | 도메인 무결성 요구 |

> 요약: 대응 기술은 공격이 발생하는 계층과 운영 범위에 맞춰 LAN, 라우터, DNS 계층으로 배치한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 내부 MITM | ARP cache poisoning | DAI, static binding, NAC | ARP change rate |
| 반사 공격 참여 | source IP 필터 미적용 | uRPF, egress ACL | spoofed source drop |
| 가짜 사이트 유도 | DNS cache poisoning | DNSSEC, resolver hardening | validation failure |

> 요약: 보안 항목은 공격 원인과 대응 지표를 분리해 ARP 변동률, spoofed drop, DNS 검증 실패로 확인한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| ARP 무결성 | 게이트웨이 MAC 변동 0건 | switch DAI 로그 |
| IP 출처 검증 | bogon·spoofed packet drop | router ACL/uRPF 로그 |
| DNS 검증 | DNSSEC validation failure 추적 | resolver 로그 |

> 요약: 스푸핑 대응은 차단 설정 존재 여부가 아니라 위조 시도 차단 건수와 캐시 변동 지표로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 사용자 VLAN에 DHCP Snooping binding table을 구성하고 Dynamic ARP Inspection으로 gateway MAC 위조를 차단함.
2. 라우터 경계에 uRPF와 BCP 38 기반 egress filtering을 적용해 내부·외부 출발지 위조 패킷을 차단함.
3. 내부 resolver에 DNSSEC validation, cache hardening, RPZ 정책을 적용하고 validation failure와 NXDOMAIN 급증을 모니터링함.

**결론 (2줄):**
- 기술사 판단: ARP는 스위치, IP는 라우터, DNS는 resolver에서 검증해야 하며 통제 위치를 혼동하면 우회가 발생함.
- 향후 방향: Zero Trust 네트워크와 암호화 DNS 환경에서도 내부 이름해석 정책과 L2 식별자 검증은 지속 관리 대상임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "스푸핑 공격을 설명하시오" | ARP·IP·DNS 공격 흐름 | 계층별 차이 |
| 요구사항 명시형 | "대응 방안을 제시하시오" | DAI/uRPF/DNSSEC 적용 흐름 | 탐지 지표와 감점 회피 포인트 |

> 요약: 설명형은 공격 원리, 보안형은 통제 위치와 탐지 지표 중심으로 목차를 전환한다.
