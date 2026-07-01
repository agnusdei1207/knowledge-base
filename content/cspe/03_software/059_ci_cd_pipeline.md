---
title: "CI/CD 파이프라인 (CI/CD Pipeline)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 59
---

# 📖 【암기용】 개념 완전 이해

> 목적: CI/CD 파이프라인을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 코드 변경을 자동으로 빌드, 테스트, 패키징, 검증, 배포하는 소프트웨어 전달 흐름
- **왜 필요한가**: 수동 빌드와 배포는 누락, 환경 차이, 배포 재현성 문제를 만든다. 파이프라인은 같은 절차를 자동 실행해 변경을 작은 단위로 검증한다.
- **핵심 직관**: 개발자의 commit이 운영 배포 가능한 artifact가 되기까지의 컨베이어 벨트이다.

## 깊이 이해
- **배경·문제의식**: 통합을 미루면 merge conflict와 회귀 오류가 뒤늦게 발견되고, 수동 배포는 담당자별 절차 차이를 만든다.
- **작동 원리**: Git 이벤트가 파이프라인을 트리거하고, build, unit test, static analysis, security scan, package, deploy, rollback 단계를 순차 또는 병렬로 실행한다.
- **비유**: 공장 품질 검사 라인처럼 원재료가 들어오면 조립, 검사, 포장, 출하 승인을 자동으로 거친다.
- **구체 예시**: PR 생성 시 10분 내 unit test와 SAST를 수행하고, main merge 후 container image를 registry에 저장하며, staging 배포 후 승인 게이트를 거쳐 production에 배포한다.
- **흔한 오해·주의점**: CI/CD는 도구 설치가 아니다. artifact 불변성, 품질 게이트, 환경 승격, rollback 기준이 함께 있어야 한다.

## 연결 개념
- Git 형상 관리: commit과 tag가 파이프라인 입력
- DevSecOps: 보안 스캔과 정책 게이트 내재화
- DORA Metrics: lead time, deployment frequency, change failure rate, MTTR 측정

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CI/CD는 빌드 자동화가 아니라 artifact, quality gate, environment promotion, rollback을 포함한 전달 체계이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CI/CD 파이프라인은 코드 변경을 자동 검증하고 불변 artifact로 패키징해 환경별 배포까지 연결하는 전달 자동화 체계이다.
> 2. **가치**: 통합 오류를 PR 단계에서 조기 발견하고, 배포 절차를 표준화하여 lead time과 rollback 시간을 측정 가능하게 한다.
> 3. **판단 포인트**: 파이프라인 품질은 단계 수가 아니라 품질 게이트, artifact 추적성, 자동 rollback, 보안 스캔 통합 수준으로 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 소프트웨어 전달 자동화 이해 확인 | build, test, package, scan, deploy, rollback | CI와 CD를 단순 배포 자동화로 설명 |
| 품질 게이트 판단 확인 | unit test, SAST, SCA, coverage, approval gate | 테스트 자동화 없는 배포만 제시 |
| 운영 지표 연결 확인 | DORA metric, artifact, environment promotion | 지표와 rollback 기준 누락 |
> 요약: 출제자는 코드 변경이 검증된 artifact로 배포되는 전 과정을 통제하는지를 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 코드 변경부터 배포까지 자동 검증
- 배경: 수동 통합과 배포는 절차 누락, 환경 차이, 승인 대기, 복구 지연을 만들어 변경 리드타임과 변경 실패율을 증가시킴.
- 필요성: Build, Test, SAST, Artifact, Deploy stage로 품질 게이트와 artifact 추적성을 확보하고 lead time, failure rate, rollback time을 관리해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Git Commit -> CI Trigger -> Build
Build -> Unit Test / Static Analysis / Security Scan
Quality Gate -> Package Artifact -> Artifact Registry
Registry -> Deploy Dev / Staging / Production
Monitoring -> Rollback / Hotfix
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source Trigger | commit, PR, tag 기반 실행 | branch policy와 연결 |
| Build/Test | 컴파일, 단위 테스트, 정적 분석 | 10분 이하 피드백 목표 |
| Security Scan | SAST, SCA, Secret Scan, Image Scan | CVSS 기준 차단 |
| Artifact Registry | 불변 산출물 저장 | version, digest 보관 |
| Deploy/Rollback | 환경 승격과 복구 | blue-green, canary 활용 |
> 요약: CI/CD는 Git 이벤트, 품질 검증, artifact 저장, 환경 배포, 복구 단계로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
개발자 commit -> PR 생성
PR -> CI 실행 -> 테스트 / 스캔 / 품질 게이트
main merge -> artifact build -> registry push
staging deploy -> smoke test -> approval
production deploy -> monitoring -> rollback 판단
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | PR 단위 CI 트리거 | 빌드 10분 이하 |
| 2 | 테스트와 정적 분석 실행 | coverage 80% 이상, blocker 0건 |
| 3 | 보안 스캔 수행 | Critical CVE 0건, secret 0건 |
| 4 | artifact 생성과 registry 저장 | digest, SBOM, tag 매핑 |
| 5 | 환경별 배포와 모니터링 | smoke test 통과, rollback 10분 이하 |
> 요약: 파이프라인은 PR 검증에서 artifact 생성, 환경 승격, 운영 모니터링까지 연결된다.

---

## Ⅳ. 특징

| 구분 | 수동 빌드·배포 | CI/CD 파이프라인 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 통합 | 릴리스 직전 통합 | commit·PR마다 통합 | CI 10분 이하 |
| 품질 | 담당자 수동 확인 | 자동 테스트·스캔 | coverage 80% 이상 |
| 산출물 | 서버에서 직접 빌드 | 불변 artifact 배포 | digest 매핑 100% |
| 배포 | 절차서 기반 | pipeline as code | 배포 이력 자동 저장 |
| 복구 | 수동 재배포 | 자동 rollback | rollback 10분 이하 |
> 요약: CI/CD는 자동 검증과 불변 artifact를 통해 배포 재현성과 복구 시간을 통제한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | CI 중심 | CI/CD 통합 | 선택 기준 |
|:---|:---|:---|:---|
| 범위 | build, test | deploy, rollback 포함 | 운영 배포 자동화 필요 여부 |
| 승인 | 개발자 검증 | 품질·보안·운영 게이트 | 규제·감사 요구 |
| artifact | 선택 저장 | 필수 저장 | 재현 배포 필요 |
| 지표 | 테스트 성공률 | DORA metric | lead time 관리 목표 |
> 요약: 운영 배포와 복구까지 자동화해야 CI/CD 통합 체계라고 볼 수 있다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| flaky test | 비결정 테스트·외부 의존 | 격리, retry 제한, quarantine | flaky 비율 2% 이하 |
| 보안 취약 배포 | 스캔 게이트 부재 | SAST, SCA, image scan 차단 | Critical CVE 0건 |
| artifact 불일치 | 환경별 재빌드 | build once deploy many | digest 매핑률 100% |
| rollback 실패 | DB migration 비가역 | expand-contract, 백업 | rollback 성공 시간 |
> 요약: 파이프라인 위험은 테스트 신뢰도, 보안 게이트, artifact 불변성, rollback 가능성으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Lead Time | commit부터 production까지 1일 이하 | DORA dashboard |
| 품질 | change failure rate 15% 이하 | 장애·배포 연계 |
| 복구 | MTTR 30분 이하 | incident record |
| 보안 | Critical CVE 0건, secret 0건 | scanner report |
> 요약: CI/CD 성과는 DORA 지표와 보안 게이트 통과 결과로 측정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. PR 단계에서 unit test, static analysis, SAST, SCA, secret scan을 10분 이하로 실행하고 blocker 0건을 merge 조건으로 둔다.
2. main merge 후 container image와 SBOM을 생성하고 tag, commit SHA, image digest를 artifact registry에 매핑한다.
3. staging smoke test 후 production은 canary 또는 blue-green으로 배포하고 error rate 1% 초과 시 자동 rollback한다.

**결론 (2줄):**
- 기술사 판단: CI만으로는 배포 품질을 보장하기 어렵고, artifact 추적성과 rollback까지 포함해야 실질적 CI/CD임
- 향후 방향: CI/CD는 DevSecOps, GitOps, SLSA 공급망 보안과 결합해 정책 기반 배포 체계로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CI/CD를 설명하시오" | commit부터 배포까지 단계 흐름 | 수동 배포 대비 특징 |
| 요구사항 명시형 | "구축 방안을 제시하시오", "운영 방안을 제시하시오" | 품질 게이트와 rollback 흐름 | DORA·보안·artifact 지표 |
> 요약: 설명형은 파이프라인 단계, 방안형은 품질 게이트와 운영 지표를 중심으로 작성한다.
