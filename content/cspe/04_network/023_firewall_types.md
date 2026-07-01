---
title: "방화벽 — 패킷 필터·상태기반·NGFW (Firewall Types)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 23
---

# 📖 【암기용】 개념 완전 이해

> 목적: 패킷 필터, 상태기반 방화벽, NGFW를 처음 봐도 어떤 정보를 기준으로 허용·차단하는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 네트워크 경계에서 트래픽을 정책과 상태에 따라 허용·차단·기록하는 보안 통제 장치
- **왜 필요한가**: 내부망과 외부망 사이에는 허용된 업무 트래픽만 통과해야 한다. 방화벽은 IP, port, session state, application, user, threat signature를 기준으로 접근을 제한한다.
- **핵심 직관**: 건물 출입문에서 방문자 신분증, 출입 목적, 예약 여부, 위험 물품을 순서대로 확인하는 구조다.

## 깊이 이해
- **배경·문제의식**: 초기 패킷 필터는 출발지·목적지 IP와 port만 보았다. 그러나 공격은 정상 port 80/443을 이용하고 세션 흐름을 악용하므로 stateful inspection과 애플리케이션 인식, IPS, URL filtering이 결합된 NGFW가 등장했다.
- **작동 원리**: 패킷 필터는 각 패킷을 독립적으로 ACL과 비교한다. 상태기반 방화벽은 SYN으로 시작한 연결을 state table에 저장하고 응답 패킷을 허용한다. NGFW는 애플리케이션 ID, 사용자 ID, TLS 복호화, 위협 시그니처를 정책에 반영한다.
- **비유**: 패킷 필터는 주소만 보는 경비원, 상태기반은 방문 예약표까지 보는 경비원, NGFW는 방문 목적과 위험 물품 검사까지 하는 통합 관제소다.
- **구체 예시**: 외부에서 내부 DB `TCP 3306`은 deny, 내부 WAS에서 DB로 가는 `TCP 3306`은 allow, 인터넷으로 나가는 `TCP 443`은 애플리케이션이 `Office365`일 때만 허용하는 식이다.
- **흔한 오해·주의점**: 방화벽 허용 정책이 있으면 침해가 0건이라는 뜻은 아니다. 허용된 `TCP 443` 내부에서도 C2, 악성 파일, 계정 탈취가 발생할 수 있어 로그, IDS/IPS, EDR 연계가 필요하다.

## 연결 개념
- ACL — 패킷 필터링의 기본 정책 형식
- IDS·IPS — 탐지와 차단을 수행하는 보안 장비
- Zero Trust — 네트워크 위치보다 사용자·기기·애플리케이션 신뢰를 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 방화벽 답안은 패킷 필터, stateful, NGFW의 판단 정보와 로그·정책·성능 지표를 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 방화벽은 네트워크 트래픽을 정책 테이블과 세션 상태, 애플리케이션 식별 결과에 따라 허용·차단하는 경계 통제 장치이다.
> 2. **가치**: 최소 허용 정책으로 공격면을 줄이고, connection log와 deny log로 보안 감사 근거를 남긴다.
> 3. **판단 포인트**: 패킷 필터는 5-tuple, stateful은 session table, NGFW는 app/user/threat intelligence를 기준으로 구분한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 방화벽 유형 구분 확인 | packet filter, stateful inspection, NGFW | 모든 방화벽을 ACL 장비로만 서술 |
| 보안 정책 설계 역량 확인 | default deny, least privilege, logging | allow 정책과 감사 로그 기준 누락 |
| 운영 리스크 이해 확인 | rule shadowing, state table exhaustion, TLS inspection | NGFW를 만능 차단 장비로 표현 |

> 요약: 이 문제는 방화벽 유형별 판단 정보와 정책 운영 지표를 연결하는 능력을 요구한다.

---

## Ⅰ. 개요 및 필요성

방화벽은 네트워크 경계에서 트래픽을 정책에 따라 통제하는 보안 장치이다. 패킷 필터는 IP·port, 상태기반 방화벽은 세션 상태, NGFW는 애플리케이션·사용자·위협 정보를 판단에 사용한다. 기업망은 업무 트래픽 허용과 공격면 축소를 동시에 달성하기 위해 방화벽 정책을 계층화한다.

---

## Ⅱ. 구조 및 구성요소

```text
Traffic In -> Zone/Interface Identify
  -> 5-Tuple Policy Match
  -> State Table Check
  -> App/User/Threat Inspection
  -> Allow/Deny/Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Rule Base | 허용·차단 정책 저장 | source, destination, service, action |
| State Table | 연결 상태 추적 | SYN, established, timeout |
| NAT Policy | 주소 변환 처리 | SNAT, DNAT, PAT |
| NGFW Engine | 앱·사용자·위협 식별 | App-ID, URL filter, IPS signature |
| Logging | 감사와 분석 근거 | allow, deny, threat log |

> 요약: 방화벽 구조는 정책 매칭, 세션 추적, 심층 검사, 로그 기록을 순차적으로 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Packet Receive -> Zone Match -> Rule Lookup
  -> Existing Session Check
  -> New Session Validate -> Threat Inspect
  -> Forward or Drop -> Log Export
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 인터페이스와 zone으로 정책 범위 결정 | zone pair, policy order |
| 2 | 5-tuple과 서비스 객체로 rule match | first match, shadow rule |
| 3 | state table에서 세션 유효성 확인 | established, timeout, TCP flag |
| 4 | NGFW 기능으로 app, URL, IPS 검사 | signature hit, app-ID confidence |
| 5 | allow, deny, reset 후 로그 전송 | SIEM event, rule hit count |

> 요약: 방화벽은 zone과 rule을 먼저 적용하고, 세션 상태와 위협 검사를 거쳐 최종 action을 결정한다.

---

## Ⅳ. 특징

| 구분 | 패킷 필터 | 상태기반·NGFW | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 판단 정보 | source/destination IP, port, protocol | session state, app, user, IPS | 5-tuple, TCP flag |
| 처리 단위 | 개별 패킷 | 연결·애플리케이션 흐름 | state timeout, CPS |
| 정책 수준 | ACL 중심 | zone, app-ID, URL, threat profile | TCP 80/443 내부 식별 |
| 운영 부담 | rule 단순 | 인증서, signature, 로그 용량 관리 | log EPS, CPU 사용률 |

> 요약: 패킷 필터는 범위 제어, stateful·NGFW는 세션과 애플리케이션 수준 통제가 판단 기준이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 패킷 필터/ACL | 상태기반/NGFW | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 라우터 ACL, stateless rule | 전용 방화벽, stateful inspection | 경계망·인터넷 구간은 stateful 이상 |
| 비용/성능 | 장비 부하 제한 | TLS inspection·IPS로 CPU 증가 | throughput, CPS, latency 기준 |
| 운영/위험 | rule 누락, 순서 오류 | state table 고갈, signature 오탐 | 변경 승인과 예외 만료일 관리 |

> 요약: 단순 세그먼트 제한은 ACL, 인터넷·DMZ 경계는 stateful 또는 NGFW가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Rule Shadowing | 상위 broad allow가 하위 deny를 가림 | rule hit 분석, 정책 정렬 | shadow rule count |
| State Exhaustion | SYN flood, 세션 누수 | SYN proxy, connection limit | state table usage |
| Blind Spot | TLS 암호화로 payload 미가시 | TLS inspection, EDR 연계 | decrypted session ratio |

> 요약: 방화벽 리스크는 정책 충돌, 세션 자원, 암호화 가시성으로 나누어 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정책 최소화 | any-any allow 0건, 예외 만료일 100% | rule audit, change ticket |
| 처리 용량 | 방화벽 CPU 70% 이하, drop 0건 | device metric, packet drop counter |
| 로그 품질 | deny/threat log SIEM 전송 100% | SIEM parser, log EPS |

> 요약: 방화벽 운영 품질은 최소 권한 정책, 처리 용량, 로그 수집률로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 인터넷·DMZ·내부 zone을 분리하고 default deny, 업무 서비스별 allow, 예외 만료일 정책을 적용함
2. NGFW는 URL filtering, IPS signature, TLS inspection 범위를 개인정보·성능 영향 기준으로 선별 적용함
3. rule hit count, state table usage, deny log, threat log를 SIEM에 연동해 월 1회 정책 정비를 수행함

**결론 (2줄):**
- 기술사 판단: 단순 라우팅 경계는 ACL, 인터넷·DMZ 경계는 stateful, 앱 식별·위협 차단은 NGFW를 선택함
- 향후 방향: Zero Trust, SASE, micro-segmentation과 연동해 네트워크 위치보다 identity와 workload 기준 정책으로 전환해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "방화벽 유형을 설명하시오" | rule, state, app inspection 흐름 | 패킷 필터·stateful·NGFW 비교 |
| 요구사항 명시형 | "보안 경계 설계 방안을 제시하시오" | zone, default deny, 로그 연계 | 리스크와 지표 기반 정책 운영 |

> 요약: 설명형은 유형별 원리, 설계형은 zone 정책과 운영 지표 중심으로 목차를 바꾼다.
