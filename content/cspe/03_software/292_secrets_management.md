---
title: "비밀 관리 (Secrets Management)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 292
---

# 📖 【암기용】 개념 완전 이해

> 목적: 비밀 관리를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: API 키, DB 비밀번호, 인증서, 토큰을 코드 밖 금고에 저장하고 접근·교체·감사를 통제하는 체계
- **왜 필요한가**: Git 커밋, 컨테이너 이미지, 환경변수에 남은 비밀값은 침해 후 lateral movement의 출발점이 된다.
- **핵심 직관**: 집 열쇠를 소스코드에 붙여 두지 않고 출입 권한과 사용 기록이 남는 금고에서 빌려 쓰는 방식이다.

## 깊이 이해
- **배경·문제의식**: 하드코딩된 비밀번호는 회수·교체가 어렵고 복제된 저장소마다 남는다. 클라우드와 MSA 환경에서는 서비스 수만큼 비밀값 수가 증가한다.
- **작동 원리**: 애플리케이션은 IAM·Kubernetes SA·OIDC로 자신을 증명하고 Vault·AWS Secrets Manager에서 필요한 비밀값을 단기 토큰으로 조회한다. DB 계정은 동적 발급 후 TTL 만료로 회수한다.
- **비유**: 회사 출입카드를 복사해 배포하지 않고, 방문 목적과 시간에 맞춰 임시 출입증을 발급하는 절차와 같다.
- **구체 예시**: Vault Dynamic Secret은 PostgreSQL 계정을 TTL 1시간으로 발급하고, 만료 시 계정을 폐기해 유출 토큰의 사용 시간을 제한한다.
- **흔한 오해·주의점**: 비밀값을 암호화해 Git에 넣으면 해결된다는 생각은 위험하다. 복호화 키, 접근 로그, 교체 자동화까지 포함해야 비밀 관리가 성립한다.

## 연결 개념
- KMS - 암호화 키 생성·보관·회전의 기반
- IAM - 서비스가 비밀 저장소에 접근할 권한 결정
- Git Secret Scanning - 저장소 유출 비밀값 탐지

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 저장소 선택보다 접근 제어, 교체, 감사 기준을 중심으로 답한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 비밀 관리는 민감 자격증명을 중앙 저장소에 보관하고 인증·인가·교체·감사를 통제하는 운영 보안 체계이다.
> 2. **가치**: 하드코딩 비밀값을 제거하고 TTL, rotation, audit log로 유출 피해 시간을 제한한다.
> 3. **판단 포인트**: 정적 secret 저장과 동적 secret 발급을 업무 위험도에 따라 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 자격증명 유출 통제 역량 확인 | Vault, AWS Secrets Manager, KMS, IAM, rotation | 암호화 저장만 쓰고 접근·감사 누락 |
| 클라우드 네이티브 운영 판단 확인 | OIDC, Kubernetes SA, dynamic secret, TTL | 환경변수 주입을 최종 통제로 오해 |
| 사고 대응 기준 확인 | 강제 회전, 감사 로그, blast radius 축소 | 유출 후 수동 교체 절차만 제시 |

> 요약: 이 문제는 비밀값 저장 위치가 아니라 생명주기와 접근 권한을 어떻게 통제하는지 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 비밀 관리는 자격증명의 저장·조회·교체·폐기 통제이다.
- 배경: API 키와 DB 비밀번호가 코드·이미지·로그에 남으면 권한 탈취와 내부 확산이 발생한다.
- 필요성: Vault·AWS Secrets Manager와 KMS를 결합해 최소 권한, TTL, rotation, 감사 로그를 적용해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Application -> Workload Identity -> Secret Manager -> KMS Encryption -> Secret Value
                                      / Rotation Job
                                      / Audit Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Secret Manager | 비밀값 저장·버전 관리 | Vault, AWS Secrets Manager |
| KMS/HSM | envelope encryption 키 보호 | 키 회전 90~365일 정책 |
| Workload Identity | 애플리케이션 신원 증명 | IAM Role, OIDC, Kubernetes SA |
| Audit Log | 조회·변경·폐기 기록 | SIEM 연동, 1년 이상 보관 |

> 요약: 비밀 관리는 저장소, 키 관리, 워크로드 신원, 감사 로그가 결합되어 자격증명 생명주기를 통제한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 시작 -> 신원 토큰 발급 -> Secret 조회 요청 -> 정책 평가 -> 복호화 반환 -> TTL 만료/회전
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 애플리케이션이 IAM·OIDC로 신원 증명 | 서비스별 Role 분리 |
| 2 | Secret Manager가 정책·경로 권한 확인 | 최소 권한 policy |
| 3 | KMS로 암호문 복호화 후 secret 반환 | TLS 1.2 이상, mTLS 선택 |
| 4 | rotation·TTL 만료 시 재발급 또는 폐기 | rotation 성공률 99% 이상 |

> 요약: 동작은 신원 증명, 권한 평가, 복호화, 회전 순서이며 TTL과 감사 로그가 피해 범위를 제한한다.

---

## Ⅳ. 특징

| 구분 | 파일·환경변수 방식 | Vault·Secrets Manager | 수치·판단 기준 |
|:---|:---|:---|:---|
| 저장 | 서버·이미지에 분산 | 중앙 저장·버전 관리 | secret 중복 저장 0건 목표 |
| 접근 | OS 권한 의존 | IAM·policy 기반 | 서비스별 권한 1:1 매핑 |
| 교체 | 수동 배포 필요 | 자동 rotation | DB secret 30~90일 회전 |
| 감사 | 조회 기록 부족 | API 단위 감사 로그 | 보관 1년 이상 |

> 요약: 중앙 비밀 관리는 분산 저장을 제거하고 권한·교체·감사를 API 단위로 통제한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | .env, config file | Secret Manager + KMS | 서비스 5개 이상, 배포 환경 2개 이상 |
| 비용/성능 | 조회 지연 없음 | 캐시·TTL로 조회 제어 | p95 조회 100ms 이하 |
| 운영/위험 | 유출 시 전체 교체 | 범위별 rotation | blast radius 서비스 단위 제한 |

> 요약: 운영 규모가 커질수록 파일 방식보다 중앙 저장소와 자동 교체가 자격증명 통제에 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 단일 장애점 | Secret Manager 장애 | local cache, multi-AZ, break-glass | 조회 실패율 0.1% 이하 |
| 권한 과다 | wildcard policy | 경로 기반 RBAC, policy review | 과권한 policy 0건 |
| 회전 실패 | 애플리케이션 재연결 미흡 | dual credential, canary rotation | rotation 실패 건수 |

> 요약: 주요 위험은 장애, 과권한, 회전 실패이며 캐시·RBAC·이중 자격증명으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 유출 방지 | Git secret 탐지 0건 | pre-commit, repository scan |
| 교체 준수 | 중요 secret 90일 이하 회전 | rotation report |
| 접근 감사 | secret 조회 로그 100% 수집 | CloudTrail, Vault audit device |

> 요약: 성공 여부는 저장소 유출 건수, 회전 주기, 조회 로그 수집률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Git secret scanning과 pre-commit hook으로 AWS Access Key, JWT private key, DB password 커밋을 차단
2. Vault 또는 AWS Secrets Manager에 secret을 저장하고 KMS CMK, IAM Role, path policy로 서비스별 접근 범위 제한
3. DB 계정은 dynamic secret 또는 dual credential rotation으로 30~90일 회전 및 감사 로그 SIEM 전송

**결론 (2줄):**
- 기술사 판단: 규제·감사 대상 시스템은 중앙 Secret Manager와 KMS를 기본 선택, 소규모 내부 도구는 관리형 클라우드 Secret으로 운영 부담 축소
- 향후 방향: OIDC 기반 workload identity와 short-lived credential로 정적 비밀값 보관 자체를 줄이는 방향 필요

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | 신원 증명, 정책 평가, 복호화, 회전 흐름 | 파일 방식과 중앙 저장소 비교 |
| 요구사항 명시형 | "설계하시오", "방안을 제시하시오", "보안 대책" | IAM·KMS·rotation 설계와 사고 대응 | 과권한, 회전 실패, 감사 지표 |

> 요약: 설명형은 생명주기, 보안형은 최소 권한·회전·감사 기준을 중심으로 답안을 전환한다.
