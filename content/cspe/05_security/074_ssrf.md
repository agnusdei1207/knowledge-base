---
title: "SSRF 서버측 요청 위조 (Server-Side Request Forgery, SSRF)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 74
---

# 📖 【암기용】 개념 완전 이해

> 목적: SSRF를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 서버가 공격자가 지정한 내부·외부 URL로 대신 요청을 보내는 취약점
- **왜 필요한가**: 이미지 가져오기, 웹훅, URL 미리보기, 파일 import 기능은 서버가 네트워크 요청을 수행한다. URL 검증이 없으면 내부 관리자 API, 클라우드 metadata, 사내망으로 접근할 수 있다.
- **핵심 직관**: 공격자가 직접 못 들어가는 내부망에, 접근 권한을 가진 서버를 프록시처럼 이용하는 공격임.

## 깊이 이해
- **배경·문제의식**: 클라우드와 마이크로서비스 환경은 서버에서 다른 서비스로 나가는 요청이 많다. 입력 URL을 allowlist 없이 처리하면 DNS rebinding, redirect, IP 변형으로 내부 대역 차단을 우회할 수 있다.
- **작동 원리**: 사용자가 URL을 제출하고 서버가 이를 fetch한다. 서버는 내부망 라우팅과 IAM 권한을 갖기 때문에 metadata IP, Kubernetes API, Redis, Elasticsearch 같은 내부 자원에 접근할 수 있다.
- **비유**: 외부인은 사무실 안 금고에 못 들어가지만, 사무실 직원에게 "이 주소로 택배 좀 보내 달라"고 시켜 내부 문서를 밖으로 보내게 하는 상황임.
- **구체 예시**: 클라우드 서버에서 `169.254.169.254` metadata endpoint 접근이 가능하면 임시 자격 증명, instance profile 정보가 유출될 수 있다.
- **흔한 오해·주의점**: URL에서 `localhost` 문자열만 차단하면 부족하다. 사설 IP, IPv6, DNS 재해석, redirect, URL 인코딩, open redirect 경유를 함께 차단해야 한다.

## 연결 개념
- Egress Control — 서버 outbound 목적지를 allowlist로 제한
- Cloud Metadata Protection — IMDSv2, metadata IP 차단, IAM 최소권한
- URL Validation — scheme, host, DNS, resolved IP, redirect 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SSRF 답안은 내부 URL 예시 나열이 아니라 URL 입력 위치, 서버 outbound 권한, egress 통제, metadata 방어를 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SSRF는 서버가 신뢰되지 않은 URL을 요청해 내부망·metadata·관리 API 접근을 대행하는 취약점이다.
> 2. **가치**: allowlist, DNS/IP 재검증, redirect 제한, egress control을 적용하면 서버의 네트워크 권한 남용을 통제할 수 있다.
> 3. **판단 포인트**: URL 검증은 문자열이 아니라 최종 resolved IP와 redirect chain, scheme, 포트, outbound 로그 기준으로 수행해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 서버측 요청 공격 이해 확인 | URL 입력 기능과 서버 outbound 권한 연결 | XSS·CSRF처럼 브라우저 공격으로 설명 |
| 방어 설계 역량 확인 | allowlist, metadata IP 차단, DNS 재검증, redirect 제한 | localhost 문자열 차단만 제시 |
| 클라우드 운영 통제 확인 | IMDSv2, IAM 최소권한, egress 로그 | 클라우드 자격 증명 유출 경로 누락 |

> 요약: SSRF는 서버 네트워크 권한 문제이며, 최종 목적지 검증과 outbound 통제가 답안의 중심이다.

---

## Ⅰ. 개요 및 필요성

SSRF는 서버 요청 대행 취약점이다. URL 미리보기, 이미지 import, 웹훅 검증 기능에서 발생하며 클라우드 metadata와 내부 API 노출로 이어질 수 있다. 방어는 입력 검증보다 서버 outbound 경로를 allowlist로 제한하는 구조가 우선이다.

---

## Ⅱ. 구조 및 구성요소

```text
User URL Input -> Server Fetch Function -> DNS Resolve -> HTTP Client -> Target Resource
                  / Internal API
                  / Cloud Metadata
                  / External Host
Defense -> Scheme/Host Allowlist -> Resolved IP Check -> Redirect Limit -> Egress Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| URL 입력 기능 | 미리보기, 웹훅, 파일 import 요청 수신 | 신뢰 경계 밖 목적지 |
| 서버 HTTP client | 대상 URL로 outbound 요청 수행 | 내부망 라우팅 가능 |
| 이름해석·리다이렉트 | DNS, CNAME, 30x 이동 처리 | DNS rebinding과 redirect 우회 지점 |
| 네트워크 통제 | 방화벽, proxy, service mesh egress | allowlist와 로그 수집 위치 |

> 요약: SSRF 구조는 입력 URL, 서버 HTTP client, 이름해석, egress 통제의 연결로 파악한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
URL 제출 -> scheme/host 1차 검증 -> DNS resolve -> IP 대역 재검증
-> redirect chain 확인 -> 서버 outbound 요청 -> 응답 처리 -> egress 로그 상관분석
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자가 외부 URL을 제출 | `http/https` 외 scheme 차단 |
| 2 | DNS 결과와 최종 IP를 확인 | RFC 1918, loopback, link-local 차단 |
| 3 | redirect와 재해석을 반복 검증 | redirect 3회 이하, 최종 host allowlist |
| 4 | egress proxy가 outbound를 기록 | 목적지 IP, 포트, 응답 코드 로그 |

> 요약: SSRF 방어 흐름은 URL 문자열보다 DNS 이후 최종 IP와 redirect chain을 검증하는 방식이다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | SSRF 대응 | 수치·기술 판단 |
|:---|:---|:---|:---|
| 검증 방식 | denylist 문자열 차단 | 도메인 allowlist와 resolved IP 검증 | 사설·loopback·link-local 차단 |
| 클라우드 | metadata endpoint 노출 | IMDSv2, hop limit, metadata IP 차단 | `169.254.169.254` 접근 0건 |
| 네트워크 | 서버 outbound 자유 | egress proxy, firewall, service mesh | 허용 목적지 목록 기반 |
| 요청 처리 | redirect 자동 추적 | redirect 횟수·목적지 재검증 | 30x chain마다 IP 재검증 |

> 요약: SSRF 대응은 입력 검증과 네트워크 egress 제한을 이중으로 적용해야 우회 기법을 줄일 수 있다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 애플리케이션 URL 필터 | 애플리케이션 검증+egress proxy | 내부망 접근 가능 서버에 필수 |
| 비용/성능 | direct outbound | 중앙 proxy 경유와 캐시 | 외부 호출 p95 지연 허용치 100ms 이내 |
| 운영/위험 | 개발자별 예외 | 도메인 allowlist 승인 workflow | 웹훅·미리보기 기능 변경 시 보안 리뷰 |

> 요약: SSRF 위험이 있는 기능은 애플리케이션 필터 단독보다 중앙 egress 통제를 표준 경로로 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Metadata 탈취 | link-local IP 접근 허용 | IMDSv2 적용, metadata IP 차단, IAM 최소권한 | metadata 요청 0건 |
| 내부 API 접근 | 서버가 사내망 라우팅 보유 | RFC 1918, loopback, Kubernetes service CIDR 차단 | 내부 IP outbound 0건 |
| DNS 우회 | DNS rebinding, CNAME, redirect | 요청 직전 resolved IP 재검증 | DNS/IP 불일치 탐지 건수 |

> 요약: SSRF 리스크는 metadata, 내부 API, DNS 우회이며 최종 IP 기준 로그로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| URL 검증 | scheme, host, port, IP 대역 100% 검증 | 단위 테스트, 보안 테스트 케이스 |
| Egress 통제 | outbound allowlist 100% 경유 | proxy 로그, firewall 정책 |
| 클라우드 권한 | instance role 최소권한과 IMDSv2 적용 | CSPM, IAM Access Analyzer |

> 요약: SSRF 통제 효과는 URL 검증률, egress 경유율, metadata 접근 차단 지표로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 코드 레벨: URL parser로 scheme·host·port를 정규화하고 DNS resolve 후 사설·loopback·link-local·metadata IP 차단
2. 네트워크 레벨: egress proxy와 firewall allowlist 적용, redirect chain마다 최종 IP 재검증, timeout 3초와 응답 크기 제한
3. 클라우드 레벨: AWS IMDSv2, GCP/Azure metadata header 요구, IAM 최소권한, metadata 접근 로그 알림 설정

**결론 (2줄):**
- 기술사 판단: URL fetch 기능은 allowlist가 가능한 업무만 허용하고, 불특정 URL 수집 기능은 격리 worker와 egress proxy를 필수로 적용함
- 향후 방향: 서비스 메시와 클라우드 보안 형상관리로 outbound 정책을 코드 리뷰와 배포 파이프라인에 연결함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SSRF를 설명하시오", "기술하시오" | URL 제출부터 서버 outbound까지 공격 흐름 | metadata, 내부망, DNS 우회와 대응 |
| 요구사항 명시형 | "방안을 제시하시오", "설계하시오", "비교하시오" | resolved IP 검증, redirect 제한, egress 흐름 | allowlist, proxy, IMDSv2 선택 기준 |

> 요약: 설명형은 서버 대행 요청 원리를, 설계형은 최종 목적지 검증과 egress 통제 구조를 중심으로 쓴다.
