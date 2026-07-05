---
title: "비밀 관리 - Vault·AWS Secrets (Secrets Management)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 133
---

# 📖 【암기용】 개념 완전 이해

> 목적: 비밀 관리를 처음 봐도 애플리케이션 자격증명 보호와 회전 운영을 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 비밀 관리는 DB 비밀번호, API key, token, 인증서를 중앙 저장·발급·회전·감사하는 보안 운영 체계임
- **왜 필요한가**: 소스코드, 컨테이너 이미지, 환경변수, CI 로그에 비밀이 남으면 공격자는 서비스 계정 권한으로 DB·클라우드 API에 접근함.
- **핵심 직관**: 사무실 열쇠를 개인 책상에 보관하지 않고, 출입증 발급소에서 필요한 시간만 대여하고 반납 기록을 남기는 방식임.

## 깊이 이해
- **배경·문제의식**: 하드코딩된 비밀번호는 커밋 이력과 이미지 레이어에 남고, 한 번 유출되면 모든 배포본을 교체해야 함. 비밀 관리 플랫폼은 저장 위치를 중앙화하고 접근 이력을 남김.
- **작동 원리**: Vault는 secret engine, auth method, policy, lease TTL로 동적 비밀을 발급·폐기함. AWS Secrets Manager는 KMS 암호화, IAM 권한, rotation Lambda, AWSCURRENT·AWSPENDING label로 버전 전환을 수행함.
- **비유**: 호텔 카드키처럼 숙박 기간 동안만 열리고 체크아웃 후 자동 폐기되는 접근권한과 유사함.
- **구체 예시**: 애플리케이션이 Kubernetes ServiceAccount로 Vault에 로그인하고 15분 TTL PostgreSQL 계정을 받아 사용하며, 만료 시 Vault가 DB 계정을 폐기함.
- **흔한 오해·주의점**: 비밀을 중앙 저장소에 넣는 것만으로 충분하지 않음. 접근 정책, 자동 회전, 감사 로그, 장애 시 break-glass 절차가 같이 필요함.

## 연결 개념
- IAM·RBAC: 비밀 조회 주체와 권한 범위 결정
- KMS·HSM: 저장 시 암호화와 루트 키 보호
- Git Secret Scanning: 이미 노출된 비밀 탐지와 폐기 절차

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 비밀 관리는 저장소 도입이 아니라 "발급 주체·TTL·회전·감사·폐기" 생명주기 통제임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Secrets Management는 비밀번호·API key·token·인증서를 중앙 저장하거나 동적으로 발급하고 접근·회전·폐기를 감사하는 통제 체계임.
> 2. **가치**: Vault lease TTL, AWS Secrets Manager rotation label, KMS 암호화, IAM/RBAC로 하드코딩 비밀과 장기 자격증명 노출을 줄임.
> 3. **판단 포인트**: 정적 저장형과 동적 발급형을 구분하고, TTL·rotation 주기·감사 로그·애플리케이션 장애 대응을 함께 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 비밀 생명주기 이해 확인 | 생성, 저장, 조회, 회전, 폐기, 감사 | 암호화 저장만 쓰고 회전·폐기 누락 |
| Vault·AWS Secrets 차이 판단 | 동적 secret, lease TTL, staging label, KMS/IAM | 제품 기능 나열로 끝내고 적용 기준 누락 |
| 운영 리스크 통제 확인 | 장애 시 캐시, break-glass, 권한 최소화 | 모든 secret을 하나의 admin 권한으로 설명 |

> 요약: 비밀 관리 문제는 저장소 선택보다 TTL·회전·감사·장애 대응을 기준으로 설계해야 고득점 답안이 됨.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | 비밀 관리는 DB 비밀번호, API key, token, 인증서를 중앙 저장·발급·회전·감사하는 보안 운영 체계임 | "입장권" |
| **왜 필요한가** | 소스코드, 컨테이너 이미지, 환경변수, CI 로그에 비밀이 남으면 공격자는 서비스 계정 권한으로 DB·클라우드 API에 접근함 | "식당 메뉴판" |
| **핵심 직관** | 사무실 열쇠를 개인 책상에 보관하지 않고, 출입증 발급소에서 필요한 시간만 대여하고 반납 기록을 남기는 방식임 | "이 개념의 핵심" |
| **배경·문제의식** | 하드코딩된 비밀번호는 커밋 이력과 이미지 레이어에 남고, 한 번 유출되면 모든 배포본을 교체해야 함 | "이 개념의 핵심" |
| **작동 원리** | Vault는 secret engine, auth method, policy, lease TTL로 동적 비밀을 발급·폐기함 | "신분증 확인" |
| **비유** | 호텔 카드키처럼 숙박 기간 동안만 열리고 체크아웃 후 자동 폐기되는 접근권한과 유사함 | "이 개념의 핵심" |
| **흔한 오해·주의점** | 비밀을 중앙 저장소에 넣는 것만으로 충분하지 않음 | "이 개념의 핵심" |

---


## Ⅰ. 개요 및 필요성

- 개요: 자격증명 생명주기 통제
- 배경: 애플리케이션과 CI/CD가 DB, 메시지 큐, SaaS API, 클라우드 계정에 접근하면서 Secret이 코드·로그·이미지에 남을 수 있음.
- 필요성: Vault·AWS Secrets Manager로 암호화 저장, 동적 발급, 90일 이내 회전, 감사 로그를 운영해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Application / CI -> Auth Method -> Policy Check -> Secret Engine
                                  +-> KMS / Audit Log / Rotation Job
Secret Issue -> TTL / Version Label -> Use -> Renew / Revoke
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Auth Method | 애플리케이션·사용자·CI 신원 확인 | Kubernetes, OIDC, IAM, AppRole |
| Policy/RBAC | secret path와 action 제한 | least privilege, namespace 분리 |
| Secret Engine | 정적 저장 또는 동적 자격증명 발급 | DB dynamic secret, KV, PKI |
| Rotation/Audit | 주기적 교체와 접근 기록 | CloudTrail, Vault audit device |

> 요약: 비밀 관리 구조는 신원 인증, 정책 확인, 비밀 발급, 회전·감사를 분리해 장기 공유 비밀번호를 줄임.

---

## Ⅲ. 동작원리 및 흐름도

```text
Workload Start -> Identity Authenticate -> Policy Authorize
-> Secret Retrieve / Generate -> TTL Attach -> Application Use
-> Rotate / Renew -> Revoke -> Audit Review
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | workload 신원 인증 | ServiceAccount, IAM role, OIDC subject 일치 |
| 2 | secret path 접근 권한 확인 | read/list/update 최소 권한 |
| 3 | 정적 secret 조회 또는 동적 secret 생성 | TTL 15분~24시간, version label 확인 |
| 4 | 자동 회전·갱신·폐기 수행 | AWSCURRENT 전환, Vault lease revoke |
| 5 | 접근 로그 분석 | 비정상 조회, 실패 인증, 관리자 변경 추적 |

> 요약: 비밀은 신원 기반으로 발급되고 TTL·version·audit으로 운영되며 만료·회전 시 기존 자격증명은 폐기됨.

---

## Ⅳ. 특징

| 구분 | 기존 방식 | Vault·AWS Secrets 적용 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 저장 위치 | 소스코드·환경변수·CI 변수 | 중앙 저장소, KMS 암호화 | git secret 탐지 0건 목표 |
| 발급 방식 | 장기 공유 계정 | 동적 계정·버전 secret | DB credential TTL 15분~24시간 |
| 회전 방식 | 수동 교체, 재배포 필요 | rotation job, staging label | 30/60/90일 주기 정책 |
| 감사 | 로그 산재 | 접근·회전·폐기 이벤트 기록 | SIEM 연동, 관리자 변경 알림 |

> 요약: 비밀 관리는 하드코딩 제거, TTL 단축, 자동 회전, 감사 로그를 통해 자격증명 노출 시간을 관리함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 환경변수·Kubernetes Secret 단독 | Vault 또는 AWS Secrets Manager | 멀티클라우드·동적 DB는 Vault, AWS 단일 계정은 Secrets Manager |
| 비용/성능 | 조회 지연 없음, 노출 범위 큼 | API 조회·캐시 필요 | p95 secret fetch 100ms 이하 목표 |
| 운영/위험 | 교체 시 재배포 | 자동 회전·TTL 운영 | rotation 실패 알림과 rollback 필요 |

> 요약: 동적 발급과 멀티환경 통제가 필요하면 Vault, AWS 관리형 회전과 IAM 통합이 우선이면 Secrets Manager를 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 중앙 저장소 장애 | Vault quorum 장애, AWS API 장애 | local cache TTL 5~15분, HA cluster, retry backoff | secret fetch error rate 1% 이하 |
| 권한 과다 | wildcard path, admin token 공유 | path 분리, policy review, token TTL | wildcard policy 0건 |
| 회전 실패 | 애플리케이션 reconnect 미구현 | dual credential, AWSPENDING 테스트, rollback | rotation failure 월 0건 |

> 요약: 운영 리스크는 중앙 장애, 권한 과다, 회전 실패이므로 캐시·정책 리뷰·이중 자격증명으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 노출 제거 | 신규 커밋 secret 0건 | secret scanning, pre-commit hook |
| 회전 준수 | 중요 secret 30~90일 내 rotation | Secrets Manager report, Vault lease list |
| 감사 탐지 | 비정상 조회 5분 내 알림 | SIEM rule, CloudTrail, Vault audit log |

> 요약: 비밀 관리 성과는 신규 노출 건수, 회전 준수율, 비정상 조회 탐지 시간으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 설계 단계: secret inventory를 DB·API key·token·certificate로 분류하고 중요도별 TTL 15분, 24시간, 90일 회전 기준을 정의함.
2. 구현 단계: Kubernetes workload는 Vault Agent Injector 또는 CSI Driver, AWS workload는 IAM role과 Secrets Manager caching client를 적용함.
3. 운영 단계: secret scanning, rotation failure alarm, break-glass token TTL 1시간, 관리자 변경 CloudTrail/Vault audit SIEM 연계를 구성함.

**결론 (2줄):**
- 기술사 판단: DB·클라우드 권한처럼 피해 범위가 큰 secret은 동적 발급과 짧은 TTL을 우선하고, SaaS API key는 자동 회전과 접근 감사를 우선함.
- 향후 방향: workload identity, SPIFFE/SPIRE, short-lived certificate가 결합되어 비밀번호 저장보다 단기 신원 증명 중심으로 이동함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "비밀 관리를 설명하시오", "Vault를 기술하시오" | 인증·정책·발급·회전 흐름 | 정적 저장형과 동적 발급형 차이 |
| 요구사항 명시형 | "운영 방안을 제시하시오", "설계하시오", "비교하시오" | 장애·회전·폐기 프로세스 | Vault/AWS 선택 기준, TTL, 감사 지표 |

> 요약: 설명형은 생명주기를 넓게 쓰고, 운영·설계형은 TTL·회전·장애 대응·감사 지표 중심으로 목차를 전환함.
