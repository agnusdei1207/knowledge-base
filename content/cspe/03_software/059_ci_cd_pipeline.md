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
- **개요**: **CI/CD 파이프라인**은 **지속적 통합(Continuous Integration)**과 **지속적 전달/배포(Continuous Delivery/Deployment)**를 자동화한 소프트웨어 전달 흐름이다. 코드가 커밋될 때마다 빌드·테스트·검증을 자동 실행(CI)하고, 검증을 통과한 산출물을 운영 환경까지 자동으로 내보낸다(CD).
- **왜 필요한가**: 사람이 수동으로 빌드하고 배포하면 절차를 빠뜨리거나, 개발 환경과 운영 환경의 설정 차이 때문에 "내 컴퓨터에서는 됐는데" 문제가 생긴다. 파이프라인은 매번 똑같은 절차를 기계가 실행하므로, 변경을 작은 단위로 자주, 같은 방식으로 검증할 수 있다.
- **핵심 직관**: 개발자의 commit이 운영에 배포 가능한 artifact(산출물)가 되기까지 지나가는 공장의 컨베이어 벨트다. 벨트 중간중간의 검사 게이트(품질 게이트)를 통과하지 못하면 다음 단계로 넘어가지 못한다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| CI (지속적 통합) | 코드를 커밋·PR할 때마다 자동으로 빌드하고 테스트해 통합 문제를 즉시 찾아내는 것 | 부품을 만들 때마다 바로바로 조립해 맞는지 확인 |
| Continuous Delivery (지속적 전달) | 언제든 배포할 수 있는 상태(검증된 artifact)까지는 자동으로 만들되, 실제 운영 배포는 사람이 승인 | 완제품을 포장까지 끝내놓고, 출고는 담당자 승인 후 진행 |
| Continuous Deployment (지속적 배포) | 검증을 통과하면 사람의 개입 없이 운영 환경까지 자동으로 배포 | 검사만 통과하면 바로 출고까지 자동 진행 |
| Artifact (산출물) | 빌드로 만들어진, 다시 빌드하지 않고 그대로 배포에 쓰는 불변(Immutable) 결과물(컨테이너 이미지 등) | 한 번 구운 빵 — 이후엔 다시 반죽하지 않고 그대로 사용 |
| Quality Gate (품질 게이트) | 다음 단계로 넘어가기 위해 반드시 통과해야 하는 기준선(테스트 성공률, 커버리지 등) | 다음 검문소를 통과해야 다음 구간으로 진입 |
| SAST / SCA / Secret Scan | 소스코드 자체 취약점 분석(SAST), 사용 중인 오픈소스 라이브러리 취약점 분석(SCA), 코드에 노출된 비밀번호·키 탐지(Secret Scan) | 건강검진(SAST), 수입 재료 원산지 검사(SCA), 지갑에 적어둔 비밀번호 쪽지 찾기(Secret Scan) |
| Blue-Green 배포 | 기존 버전(Blue)을 살려둔 채 새 버전(Green)을 통째로 띄우고, 트래픽을 한 번에 전환하는 배포 방식 | 옆 매장을 새로 오픈해 완성되면 간판만 바꿔 달기 |
| Canary 배포 | 새 버전에 트래픽 일부(예: 5%)만 먼저 흘려보내 문제가 없는지 확인한 뒤 점차 비율을 늘리는 배포 방식 | 광부가 탄광에 카나리아를 먼저 들여보내 위험을 확인 |
| Rollback | 배포한 새 버전에 문제가 생기면 직전의 안정 버전으로 되돌리는 것 | 잘못 튼 수도꼭지를 되돌려 잠그기 |
| DORA Metrics | 배포 성숙도를 측정하는 4대 지표(Lead Time, Deployment Frequency, Change Failure Rate, MTTR) | 성적표의 4개 과목 점수 |

## 깊이 이해

### 왜 필요했나 — 통합을 미루면 벌어지는 일
- 여러 개발자가 각자 코드를 몇 주씩 붙들고 있다가 한 번에 합치면(빅뱅 통합), merge conflict와 회귀 오류가 한꺼번에 쏟아져 원인을 찾기 어렵다. 예를 들어 10명이 각자 2주씩 작업한 코드를 마지막 날 한 번에 합치면, 충돌 지점이 수백 곳에 달할 수 있다. 반대로 매일 커밋마다 자동으로 통합·테스트하면, 충돌이나 회귀가 생겨도 "오늘 아침에 누가 무엇을 고쳤는지"만 확인하면 되므로 원인 파악이 몇 분 안에 끝난다.
- 배포도 마찬가지다. 사람이 매번 수동으로 서버에 접속해 파일을 올리면, 담당자마다 절차가 조금씩 달라 "스테이징에서는 됐는데 운영에서는 안 되는" 환경 차이 문제가 반복된다.

### CI 단계 — commit에서 artifact까지 (수치로 이해)
- 개발자가 PR을 올리면 파이프라인이 자동으로 트리거된다. 우선 컴파일(Build), 그다음 단위 테스트(Unit Test)와 정적 분석(Static Analysis)을 수행한다. 이 전체 과정은 보통 10분 이내에 끝나도록 설계한다 — 그래야 개발자가 다른 작업으로 넘어가기 전에 피드백을 받을 수 있다. 10분을 넘기기 시작하면 개발자들이 결과를 기다리지 않고 다음 커밋을 쌓아버려 문제 추적이 다시 어려워진다.
- 테스트 커버리지 기준(예: 80% 이상)과 정적 분석에서 심각한(blocker) 결함 0건을 품질 게이트로 걸어, 이 기준을 못 넘으면 애초에 merge 자체가 막힌다.
- 보안 스캔(SAST·SCA·Secret Scan)에서 치명적(Critical) 취약점이나 노출된 비밀 값이 하나라도 발견되면 파이프라인을 실패시켜 병합을 차단한다. 이렇게 개발 초기 단계(왼쪽)에서 보안을 검증하는 것을 "Shift-Left 보안"이라 부른다.

### CD 단계 — artifact를 안전하게 운영까지 옮기기
- CI를 통과하면 코드를 다시 빌드하지 않고, 한 번 만든 컨테이너 이미지(artifact)에 커밋 해시와 버전 태그를 매핑해 레지스트리에 저장한다. 이후 개발(dev)→스테이징(staging)→운영(production) 환경에는 이 "같은" artifact를 그대로 옮겨 배포한다. 이 원칙을 "Build Once, Deploy Many(한 번 빌드해 여러 환경에 배포)"라 한다 — 환경마다 다시 빌드하면 컴파일러·라이브러리 버전 차이로 "스테이징에서는 되는데 운영에서는 안 되는" 문제가 재발하기 때문이다.
- 운영 배포는 한 번에 100% 트래픽을 바꾸지 않고 점진적으로 진행한다. 예를 들어 Canary 배포는 새 버전에 트래픽 5%만 먼저 흘려 오류율을 관찰하고, 문제가 없으면 25%, 50%, 100% 순으로 늘려간다. 도중에 에러율이 기준치(예: 1%)를 넘으면 자동으로 트래픽을 이전 버전으로 되돌린다(Rollback).
- Rollback 목표 시간을 수치로 정해둔다(예: 10분 이내). 이 시간을 지키려면 배포 자체를 자동화해 두어야 하며, 데이터베이스 스키마 변경처럼 되돌리기 어려운 작업은 한 번에 바꾸지 않고 "새 컬럼을 추가만 하고(expand) 나중에 옛 컬럼을 제거하는(contract)" 방식으로 나눠 진행해 언제든 안전하게 되돌릴 수 있게 한다.

### Continuous Delivery vs Deployment — 헷갈리는 두 용어의 판별 원리
- 두 용어를 가르는 기준은 딱 하나, "운영 배포를 사람이 최종 승인하는가"이다. 검증까지는 완전히 자동이지만 실제 운영 반영은 담당자 승인을 거치면 Continuous Delivery, 승인 절차 없이 품질 게이트만 통과하면 바로 운영까지 자동으로 나가면 Continuous Deployment다. 규제 산업(금융 등)은 감사 요건 때문에 Delivery까지만 자동화하고 최종 승인은 사람이 하는 경우가 많다.

### DORA 지표로 파이프라인의 성숙도를 재는 법
- Lead Time(커밋부터 운영 배포까지 걸리는 시간), Deployment Frequency(배포 빈도), Change Failure Rate(배포 중 장애가 발생하는 비율), MTTR(장애 발생 후 복구까지 걸리는 시간) 4가지로 파이프라인의 성숙도를 정량 평가한다.
- 예: Lead Time이 며칠 단위인 조직은 배포마다 수동 승인·수동 테스트가 많이 남아있다는 뜻이고, Lead Time이 1시간 이내인 조직은 대부분의 검증이 자동화돼 있다는 뜻이다. Change Failure Rate가 15%를 넘으면(배포 6~7번에 1번꼴로 장애) 품질 게이트가 느슨하다는 신호로 본다.

### 비유와 흔한 오해
- **비유**: 공장의 품질 검사 라인. 원재료(코드)가 들어오면 조립(빌드), 검사(테스트·보안 스캔), 포장(artifact 패키징), 출하 승인(배포)을 거쳐야 제품이 나간다. 중간 검사(품질 게이트)를 통과하지 못한 제품은 다음 라인으로 넘어가지 못한다.
- **오해**: "젠킨스나 GitHub Actions 같은 도구만 설치하면 CI/CD를 한 것"이라는 생각은 틀렸다. 도구가 있어도 artifact 불변성(한 번 빌드해 여러 환경에 배포), 품질 게이트, 자동 rollback 기준이 함께 갖춰져야 실질적인 CI/CD 체계라 할 수 있다.

## 연결 개념
- Git 형상 관리: commit·PR·tag가 파이프라인을 실행시키는 입력(트리거)이다.
- DevSecOps: 보안 스캔과 정책 게이트를 파이프라인 안에 내재화하는 접근이다.
- GitOps: 인프라 설정까지 Git으로 관리해 파이프라인이 인프라 배포까지 자동화하도록 확장한 개념이다.

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

| 구분 | CI 중심 | CI/CD 통합 | 선택 기준 |
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
