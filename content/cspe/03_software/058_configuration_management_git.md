---
title: "형상 관리 Git·브랜치 전략 (Configuration Management Git)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 58
---

# 📖 【암기용】 개념 완전 이해

> 목적: Git 기반 형상 관리와 브랜치 전략을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 소스코드 변경 이력, 버전, 배포 산출물의 추적성을 Git으로 관리하는 활동
- **왜 필요한가**: 여러 개발자가 동시에 코드를 바꾸면 충돌, 배포 버전 혼선, 장애 원인 추적 문제가 생긴다. 형상 관리는 누가, 언제, 무엇을, 왜 바꿨는지 남긴다.
- **핵심 직관**: Git은 단순 저장소가 아니라 변경 이력과 릴리스 근거를 연결하는 감사 로그이다.

## 깊이 이해
- **배경·문제의식**: 압축파일, 공유 폴더, 수동 배포는 변경 근거와 복구 지점이 불명확해 장애 분석 시간이 증가한다.
- **작동 원리**: Git은 commit DAG로 변경 이력을 저장하고, branch는 병렬 작업 흐름을 만들며, tag는 릴리스 버전을 고정한다.
- **비유**: 실험실 연구노트처럼 실험 과정, 변경 이유, 결과물을 시간순으로 남겨 같은 결과를 재현하게 한다.
- **구체 예시**: GitHub Flow는 `main`에서 feature branch를 만들고 PR 리뷰와 CI 통과 후 merge한다. trunk-based는 하루 1회 이상 main에 통합하고 feature flag로 미완성 기능을 숨긴다.
- **흔한 오해·주의점**: 브랜치가 많다고 관리 수준이 높아지는 것은 아니다. 장수 브랜치는 merge conflict와 통합 지연을 늘린다.

## 연결 개념
- CI/CD: Git 이벤트를 빌드·테스트·배포 파이프라인으로 연결
- 코드 리뷰: 변경 품질과 지식 공유 통제
- 릴리스 관리: tag, changelog, rollback 기준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Git 명령어 나열이 아니라 브랜치 전략, 리뷰, 릴리스 태그, 추적성 통제를 함께 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Git 형상 관리는 소스 변경 이력, 병렬 개발, 릴리스 버전, 감사 추적을 commit·branch·tag로 통제하는 활동이다.
> 2. **가치**: 변경 원인 추적과 복구 기준을 명확히 하여 장애 발생 시 특정 commit과 릴리스 tag로 영향 범위를 좁힌다.
> 3. **판단 포인트**: Git Flow, GitHub Flow, Trunk-based는 팀 규모, 배포 빈도, 릴리스 승인 수준에 따라 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 형상 관리 기본 역량 확인 | commit, branch, merge, tag, release, rollback | Git 명령어만 나열 |
| 브랜치 전략 선택 확인 | Git Flow, GitHub Flow, Trunk-based 비교 | 하나의 전략을 모든 팀에 적용 |
| 추적성·감사 대응 확인 | PR, code review, issue link, signed commit | 배포 산출물과 소스 이력 연결 누락 |
> 요약: 출제자는 개발 흐름과 릴리스 추적성을 브랜치 전략으로 통제하는지를 본다.

---

## Ⅰ. 개요 및 필요성

- 개요: 소스 변경 이력과 릴리스 통제
- 배경: 동시 개발, 배포 오류, 장애 분석 상황에서는 변경 근거, 승인 기록, 복구 지점이 필요하고 브랜치 충돌은 릴리스 지연으로 이어짐.
- 필요성: Git branch strategy, pull request review, tag, release note로 변경 추적성, merge conflict rate, rollback 기준을 관리해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Issue -> Branch -> Commit -> Pull Request
Pull Request -> Review -> CI Check -> Merge
Merge -> Main / Release Branch
Release Branch -> Tag -> Artifact -> Deploy
Incident -> Tag / Commit -> Rollback / Hotfix
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Commit | 변경 단위와 메시지 기록 | 이슈 ID, 변경 이유 포함 |
| Branch | 병렬 작업 흐름 제공 | feature, release, hotfix |
| Pull Request | 리뷰와 자동 검증 관문 | 승인자 1~2명 지정 |
| Tag/Release | 배포 기준점 고정 | Semantic Versioning 적용 |
| Audit Trail | 변경 추적 근거 | signed commit, issue link |
> 요약: Git 형상 관리는 commit에서 tag까지 변경과 배포 산출물을 연결하는 추적 체계이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요구사항 등록 -> 이슈 생성
이슈 -> 브랜치 생성 -> 커밋 작성
커밋 -> PR 생성 -> 리뷰 / CI
승인 -> merge -> tag / release
장애 -> commit 추적 -> rollback / hotfix
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 이슈와 브랜치 연결 | 브랜치명에 이슈 ID 포함 |
| 2 | 기능 단위 commit 작성 | commit message 규칙 준수 |
| 3 | PR 리뷰와 CI 수행 | 테스트·정적 분석 통과 |
| 4 | main 또는 release branch 병합 | merge conflict 해결 시간 |
| 5 | tag 생성과 릴리스 노트 작성 | artifact digest와 tag 매핑 |
> 요약: Git 흐름은 이슈, 브랜치, 커밋, 리뷰, 태그를 연결하여 변경 추적성을 확보한다.

---

## Ⅳ. 특징

| 구분 | Git Flow | GitHub Flow | Trunk-based |
|:---|:---|:---|:---|
| 구조 | develop, release, hotfix 다중 브랜치 | main + short feature branch | main 중심, 짧은 수명 브랜치 |
| 적합 | 정기 릴리스, 승인 절차 | 웹 서비스 지속 배포 | 대규모 CI와 feature flag |
| 통합 주기 | 수일~수주 | 수시간~수일 | 하루 1회 이상 |
| 리스크 | 장수 브랜치 충돌 | main 품질 의존 | 자동 테스트 미흡 시 장애 |
| 지표 | 릴리스 안정성 | PR 리드타임 | merge conflict 시간 |
> 요약: 배포 빈도가 높을수록 GitHub Flow와 trunk-based가 적합하며, 승인형 릴리스는 Git Flow가 적합하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 장수 브랜치 | 짧은 브랜치·Trunk | 선택 기준 |
|:---|:---|:---|:---|
| 충돌 | merge conflict 누적 | 충돌 조기 발견 | 하루 1회 이상 통합 가능 여부 |
| 배포 | 릴리스 묶음 | 작은 변경 자주 배포 | DORA lead time 목표 |
| 품질 | 통합 후 검증 | PR마다 검증 | CI 10분 이하 |
| 통제 | 승인 단계 많음 | 자동 게이트 중심 | 규제·감사 요구 수준 |
> 요약: 통합 주기를 줄일수록 충돌 비용은 낮아지지만 자동 테스트와 feature flag가 필요하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| merge conflict | 장수 브랜치와 대형 PR | PR 400라인 이하, 일 단위 rebase | conflict 해결 시간 |
| 리뷰 병목 | 승인자 부족 | CODEOWNERS, 리뷰 SLA | PR 대기 시간 |
| 추적성 누락 | 이슈·tag 미연결 | branch naming, release note 자동화 | 이슈 링크 누락률 |
| 릴리스 혼선 | artifact와 tag 불일치 | immutable artifact, checksum 저장 | tag-artifact 매핑률 |
> 요약: 형상 관리 리스크는 충돌, 리뷰 병목, 추적성 누락, 릴리스 혼선이며 PR 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| PR 리드타임 | 생성부터 merge까지 24시간 이하 | GitHub API |
| 충돌 비용 | conflict 해결 30분 이하 | PR 이벤트 로그 |
| 추적성 | commit-issue-release 연결 100% | ALM 리포트 |
| 릴리스 | tag와 artifact digest 매핑 100% | CI/CD metadata |
> 요약: 형상 관리 수준은 PR 리드타임, 충돌 시간, 추적성, tag-artifact 매핑으로 측정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 웹 서비스는 GitHub Flow 또는 trunk-based로 운영하고 PR 크기 400라인 이하, CI 10분 이하, 승인자 1명 이상을 기준으로 둔다.
2. 규제 승인형 제품은 Git Flow로 release branch와 hotfix branch를 운영하며 tag, changelog, artifact digest를 함께 보관한다.
3. 모든 commit은 issue ID, signed commit, CODEOWNERS 리뷰, protected branch 정책을 적용해 감사 추적성을 확보한다.

**결론 (2줄):**
- 기술사 판단: 월 단위 릴리스는 Git Flow, 일 단위 배포는 GitHub Flow, 하루 여러 번 배포는 trunk-based가 타당함
- 향후 방향: Git 형상 관리는 SBOM, SLSA, 서명된 artifact와 결합해 공급망 추적성 중심으로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "형상 관리를 설명하시오" | 이슈부터 tag까지 흐름 | 브랜치 전략별 특징 |
| 요구사항 명시형 | "브랜치 전략을 비교하시오", "방안을 제시하시오" | PR·CI·release 흐름 | 팀·배포 빈도별 선택 기준 |
> 요약: 설명형은 추적 흐름, 비교형은 브랜치 전략 선택 기준과 지표를 중심으로 작성한다.
