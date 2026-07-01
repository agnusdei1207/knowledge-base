---
title: "802.1X EAP 인증 (802.1X EAP Authentication)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 147
---

# 📖 【암기용】 개념 완전 이해

> 목적: 802.1X EAP 인증을 포트 로그인 기능이 아니라 단말, 스위치/AP, 인증 서버가 역할을 나누는 네트워크 접속 인증 흐름으로 이해하게 만든다.

## 한눈에
- **개요**: 802.1X는 유선·무선 포트 접속 전에 EAP 기반으로 사용자 또는 단말을 인증하는 표준
- **왜 필요한가**: 물리 포트에 케이블을 꽂거나 SSID에 붙는 것만으로 내부망 접근을 허용하면 미승인 단말이 업무망에 들어올 수 있다.
- **핵심 직관**: 회의장 입구에서 참가자가 신분증을 제시하고, 안내원이 본부에 확인한 뒤 좌석 구역을 배정하는 절차와 같다.

## 깊이 이해
- **배경·문제의식**: VLAN과 IP ACL만으로는 접속 주체의 신원과 단말 상태를 확인하기 어렵고, 포트 위치만으로 권한을 부여하는 한계가 있다.
- **작동 원리**: Supplicant가 EAP 메시지를 보내고, Authenticator가 이를 RADIUS 서버로 중계하며, Authentication Server가 인증 결과를 반환한다.
- **비유**: 스위치/AP는 문지기, RADIUS는 출입 명부, 단말 인증서는 신분증 역할을 한다.
- **구체 예시**: EAP-TLS는 클라이언트 인증서와 서버 인증서를 상호 검증해 패스워드 탈취 위험을 줄이고 기업 무선망에서 널리 사용된다.
- **흔한 오해·주의점**: 802.1X는 암호화 자체가 아니라 접속 인증 프레임워크이며, 무선 암호화는 WPA2/WPA3 Enterprise와 함께 구성된다.

## 연결 개념
- EAP-TLS - 인증서 기반 상호 인증 방식
- RADIUS - EAP 결과와 VLAN/ACL 속성을 전달하는 AAA 프로토콜
- NAC - 802.1X 결과를 접근 정책과 단말 상태 점검에 활용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 802.1X 답안은 Supplicant, Authenticator, Authentication Server 역할과 EAP 메시지 흐름을 분리해 작성한다.
> 핵심: 출제자는 포트 기반 접근 통제와 EAP-TLS 인증 흐름을 정확히 구분하는지 확인한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 802.1X는 네트워크 포트 접속 전에 Supplicant, Authenticator, Authentication Server가 EAP 기반 인증을 수행하는 표준이다.
> 2. **가치**: EAP-TLS, RADIUS, 동적 VLAN/ACL을 통해 사용자·단말 신원에 따라 접속 권한을 부여한다.
> 3. **판단 포인트**: 인증 방식, 인증서 관리, RADIUS 가용성, 실패 시 게스트·격리 정책, 로그 지표를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 802.1X 역할 구분 확인 | Supplicant, Authenticator, Authentication Server | 스위치가 직접 사용자 DB를 인증한다고 설명 |
| EAP 인증 흐름 확인 | EAPOL, RADIUS, EAP-TLS, Access-Accept | EAP와 RADIUS의 전달 역할 혼동 |
| 운영 리스크 판단 확인 | 인증서 만료, RADIUS 장애, fallback 정책 | 인증 실패 시 업무 영향과 예외 처리 누락 |

> 요약: 802.1X 문제는 3개 주체와 EAP/RADIUS 메시지 경계를 정확히 쓰는 것이 채점 핵심이다.

---

## Ⅰ. 개요 및 필요성

- 개요: 포트 접속 전 EAP 기반 인증
- 배경: 내부망 포트와 기업 SSID에 접속한 단말을 신원 확인 없이 허용하면 미승인 장비가 업무망에 접근함.
- 필요성: 사용자·단말 인증 결과에 따라 업무 VLAN, 게스트 VLAN, 격리 VLAN을 동적으로 할당해야 함.
- 판단 기준: EAP-TLS 적용률, 인증서 만료율, RADIUS 응답시간, Access-Reject 원인을 기준으로 운영함.

---

## Ⅱ. 구조 및 구성요소

```text
Supplicant -> EAPOL -> Authenticator(Switch / AP)
            -> RADIUS -> Authentication Server
            -> Access-Accept / Reject -> VLAN / ACL 적용
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Supplicant | 단말에서 EAP 인증 요청 수행 | OS 내장 또는 NAC agent |
| Authenticator | 스위치/AP가 EAPOL을 수신하고 RADIUS로 중계 | 포트 authorized 상태 전환 |
| Authentication Server | 인증서·계정·정책 검증 | RADIUS, AD, PKI 연동 |
| EAP Method | 인증 방식 결정 | EAP-TLS, PEAP, EAP-TTLS |

> 요약: 802.1X는 단말이 EAPOL을 보내고 스위치/AP가 RADIUS 서버에 인증 판단을 위임하는 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Link up -> EAPOL-Start -> EAP Request / Response
-> RADIUS Access-Request -> EAP-TLS 검증
-> Access-Accept -> Port authorized -> VLAN / ACL 적용
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 포트 link up 또는 무선 association 발생 | port event, WLAN association |
| 2 | Supplicant와 Authenticator가 EAPOL 메시지를 교환 | EAPOL timeout count |
| 3 | Authenticator가 EAP payload를 RADIUS로 캡슐화 | RADIUS request/response time |
| 4 | Authentication Server가 인증서 또는 계정을 검증 | cert chain, credential result |
| 5 | Access-Accept 결과로 포트 상태와 VLAN/ACL을 적용 | authorized session count |

> 요약: 802.1X 인증은 EAPOL 구간과 RADIUS 구간이 나뉘며 인증 성공 후 포트가 authorized 상태로 전환된다.

---

## Ⅳ. 특징

| 구분 | MAC/IP 기반 접속 | 802.1X EAP 인증 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 인증 주체 | 단말 주소 중심 | 사용자·단말 인증서 또는 계정 | EAP-TLS, PEAP |
| 메시지 경로 | 스위치 로컬 정책 | EAPOL + RADIUS | IEEE 802.1X, RFC 2865 |
| 권한 부여 | 고정 VLAN | 동적 VLAN/ACL | RADIUS attribute |
| 운영 리스크 | MAC 위조 | 인증서 만료, RADIUS 장애 | CRL/OCSP, RADIUS HA |

> 요약: 802.1X는 포트 접속 권한을 신원 기반으로 전환하지만 인증서와 RADIUS 가용성 관리가 필수이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 고정 포트 VLAN | 인증 결과 기반 포트 제어 | 사용자 이동성과 무선 접속이 많은 환경에 적용 |
| 비용/성능 | 별도 인증 인프라 적음 | PKI, RADIUS, Supplicant 설정 필요 | 인증서 운영 역량과 장비 지원 여부로 판단 |
| 운영/위험 | 미승인 단말 접근 가능 | 인증 실패 시 업무 접속 차단 | 게스트·격리·MAB fallback 정책 필요 |

> 요약: 802.1X는 관리 단말과 인증서 운영 체계가 준비된 환경에서 NAC의 기본 인증 방식으로 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 인증서 만료 | 단말 인증서 갱신 실패 | MDM/PKI 자동 갱신, 만료 알림 | cert expiry count |
| RADIUS 장애 | AAA 서버 단일 구성 | RADIUS 이중화, server dead action | RADIUS availability |
| IoT 미지원 | Supplicant 부재 | MAB, Profiling, 제한 VLAN | fallback session count |

> 요약: 운영 리스크는 인증서, RADIUS 가용성, supplicant 미지원 단말로 나누어 대응한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 인증 성공 | Access-Accept 비율과 실패 원인 추적 | RADIUS log |
| 접속 지연 | 인증 완료까지의 시간 관리 | EAPOL/RADIUS timestamp |
| 정책 적용 | VLAN/ACL 할당 결과 일치 | switch session table, NAC report |

> 요약: 802.1X 운영은 인증 결과, 인증 지연, 정책 적용 일치도를 함께 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 임직원 노트북과 모바일은 EAP-TLS, 내부 PKI, MDM 인증서 배포를 기준으로 표준화함.
2. 스위치와 AP는 RADIUS 이중화, 동적 VLAN, server dead action, accounting 로그를 설정함.
3. 프린터와 IoT는 MAB fallback과 제한 ACL을 적용하고 예외 목록을 CMDB와 대조함.

**결론 (2줄):**
- 기술사 판단: 관리 단말 중심 환경은 EAP-TLS 기반 802.1X를 기본값으로 적용하고, 미관리 단말은 MAB·격리망으로 분리함.
- 향후 방향: 802.1X는 NAC, ZTNA, EDR 신호와 결합되어 접속 후 지속 검증 정책으로 확장됨.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "802.1X를 설명하시오" | EAPOL-RADIUS 인증 흐름 | 3개 주체와 EAP 방식 |
| 요구사항 명시형 | "인증 방안을 제시하시오", "비교하시오" | EAP-TLS와 fallback 흐름 | 인증서, RADIUS, IoT 예외 리스크 |

> 요약: 설명형은 표준 메시지 흐름을, 방안형은 인증서·RADIUS·fallback 운영 기준을 중심으로 전환한다.
