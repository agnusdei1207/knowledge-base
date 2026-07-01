---
title: "플랫폼 엔지니어링 IDP (Platform Engineering IDP)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 92
---

# 📖 【암기용】 개념 완전 이해

> 목적: 플랫폼 엔지니어링과 IDP를 개발자 self-service와 운영 거버넌스를 동시에 제공하는 체계로 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: IDP는 개발자가 표준 경로로 앱 생성, 배포, 관측, 권한 요청을 self-service로 수행하는 내부 플랫폼
- **왜 필요한가**: 팀마다 CI/CD, Kubernetes, 보안 설정을 직접 만들면 중복, 편차, 운영 부담이 커진다.
- **핵심 직관**: 개발자에게 도로와 표지판을 깔아주고, 중앙팀은 교통법규와 안전장치를 제공하는 방식임.

## 깊이 이해
- **배경·문제의식**: DevOps를 모든 팀이 각자 구현하면 플랫폼 지식 격차, 도구 난립, 배포 품질 편차가 발생함.
- **작동 원리**: 플랫폼팀이 템플릿, golden path, CI/CD, IaC, observability, secret, policy를 제품처럼 제공하고 개발팀은 포털이나 CLI로 사용함.
- **비유**: 회사 식당이 재료 구매, 위생, 결제를 표준화해 직원이 매번 주방을 만들지 않고 식사를 해결하게 하는 것과 같음.
- **구체 예시**: 신규 서비스 생성 버튼을 누르면 Git 저장소, Dockerfile, Helm chart, CI 파이프라인, SLO 대시보드가 10분 안에 생성됨.
- **흔한 오해·주의점**: IDP는 도구 포털만이 아니라 개발자 경험, 운영 표준, 보안 정책, 플랫폼 SLO를 제품처럼 관리하는 체계임.

## 연결 개념
- Golden Path: 표준 개발·배포 경로
- Developer Experience: 개발자 작업 흐름의 마찰 측정
- Platform SLO: 플랫폼 제공 기능의 신뢰도 목표

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: IDP 답안은 포털 설명이 아니라 self-service, paved road, SLO, scorecard, governance를 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IDP는 개발팀이 표준화된 도구·템플릿·파이프라인·운영 기능을 self-service로 사용하는 내부 개발자 플랫폼이다.
> 2. **가치**: 개발팀의 반복 인프라 작업을 줄이고 플랫폼팀은 보안, 배포, 관측성, 비용 정책을 공통 경로에 내장한다.
> 3. **판단 포인트**: IDP는 도구 모음이 아니라 내부 제품이므로 사용자 여정, SLO, adoption, scorecard로 운영해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 플랫폼 엔지니어링 이해 확인 | IDP, self-service, golden path, paved road | Kubernetes 포털만으로 설명하지 않음 |
| DevEx·거버넌스 판단 확인 | SLO, scorecard, 정책 내장, 표준 템플릿 | 중앙 통제와 개발자 자율성 균형을 누락하지 않음 |
| 운영 성과 측정 확인 | lead time, adoption, MTTR, compliance | 도구 도입 건수만 성과로 제시하지 않음 |
> 요약: IDP는 개발자가 표준 경로로 배포하고 플랫폼팀이 정책·관측·비용을 내장하는 제품형 운영체계이다.

---

## Ⅰ. 개요 및 필요성

- 개요: IDP는 내부 개발자 셀프서비스 플랫폼이다.
- 배경: 클라우드, Kubernetes, CI/CD를 팀별로 구현하면 중복 파이프라인과 보안 설정 편차가 발생한다.
- 필요성: Golden Path, Service Catalog, SLO, Scorecard로 신규 서비스 생성 리드타임과 표준 준수율을 측정해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Developer Portal/CLI -> Service Catalog -> Golden Path Template
-> CI/CD/IaC/Policy -> Runtime Platform
-> Observability/SLO/Scorecard -> Feedback Loop
```

| 구성요소 | 역할 | 산정 포인트 |
|:---|:---|:---|
| Developer Portal | 서비스 생성·문서·요청 창구 | Backstage 등 포털 |
| Service Catalog | 서비스 소유자·의존성 관리 | owner, tier, SLO |
| Golden Path | 표준 템플릿과 파이프라인 | paved road, 예외 승인 |
| Platform Governance | 정책·보안·비용 통제 | Policy as Code, scorecard |
> 요약: IDP는 포털, 카탈로그, 표준 경로, 정책·관측 계층이 결합된 내부 플랫폼이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
개발자 요청 -> 템플릿 선택 -> 저장소/파이프라인 생성
-> IaC로 런타임 구성 -> 배포 -> 관측성 대시보드 생성
-> scorecard 점검 -> 피드백으로 golden path 개선
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서비스 카탈로그 등록 | owner·tier·SLO 필수 |
| 2 | Golden path 템플릿 적용 | 표준 파이프라인 생성률 |
| 3 | CI/CD와 IaC 실행 | 배포 실패율 15% 이하 |
| 4 | Observability와 SLO 연결 | dashboard·alert 자동 생성 |
| 5 | Scorecard로 준수 점검 | 정책 준수율 95% 이상 |
> 요약: IDP는 서비스 생성부터 배포, 관측, 점검까지 표준 경로를 자동 제공한다.

---

## Ⅳ. 특징

| 구분 | 전통 DevOps 도구 운영 | IDP 기반 플랫폼 엔지니어링 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 제공 방식 | 도구별 교육·요청 | self-service 포털·CLI | 신규 서비스 생성 10분 목표 |
| 표준화 | 팀별 파이프라인 편차 | golden path 내장 | 표준 템플릿 사용률 80% |
| 거버넌스 | 사후 점검 | policy as code와 scorecard | 준수율 95% |
| 한계 | 자율성 높음 | 플랫폼팀 제품 운영 필요 | 플랫폼 SLO 99.9% |
> 요약: IDP는 개발자 자율성을 유지하면서 표준 경로에 보안·배포·관측 정책을 내장한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 도구 나열형 DevOps | 제품형 내부 플랫폼 | 개발팀 5개 이상 |
| 비용/규모 | 팀별 중복 구축 | 플랫폼팀 중앙 제공 | 중복 파이프라인·템플릿 제거 |
| 운영/위험 | 표준 이탈 사후 발견 | scorecard 사전 점검 | 컴플라이언스 요구 존재 |
| 품질 | 배포 편차 큼 | golden path 품질 내장 | DORA 지표 개선 목표 |
> 요약: IDP는 개발팀 수가 늘고 클라우드 운영 복잡도가 커질 때 플랫폼팀의 제품 운영 방식으로 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 포털 방치 | 개발자 니즈 미반영 | 제품관리와 분기 로드맵 | 활성 사용자 비율 |
| 중앙 병목 | 모든 요청 승인 필요 | self-service와 예외 승인 분리 | 요청 처리 리드타임 |
| 표준 저항 | 팀별 특수 요구 | paved road와 escape hatch 제공 | 표준 경로 채택률 |
| 플랫폼 장애 | 공통 플랫폼 단일 장애점 | 플랫폼 SLO와 DR 설계 | IDP 가용성 99.9% |
> 요약: IDP 리스크는 제품관리, self-service, 예외 경로, 플랫폼 SLO로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| DevEx | 신규 서비스 생성 10분 이하 | portal telemetry |
| Adoption | 표준 템플릿 사용률 80% 이상 | catalog 분석 |
| Reliability | 플랫폼 SLO 99.9% | SLI/SLO 대시보드 |
| Governance | scorecard 준수율 95% 이상 | 정책 검사 결과 |
> 요약: IDP 성과는 개발자 경험, 채택률, 플랫폼 SLO, 정책 준수율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 상위 3개 개발자 여정인 신규 서비스 생성, 배포, 장애 확인을 먼저 IDP golden path로 구현함.
2. Service catalog에 owner, tier, dependency, SLO를 필수 필드로 두고 scorecard를 PR·배포 게이트와 연결함.
3. 플랫폼팀은 월간 adoption, lead time, 플랫폼 SLO, 개발자 만족도 점수를 제품 지표로 관리함.

**결론 (2줄):**
- 기술사 판단: 개발팀과 서비스 수가 많고 클라우드 운영 편차가 크면 IDP를 적용하고, 소규모 조직은 핵심 템플릿부터 시작함.
- 향후 방향: IDP는 AI 보조, FinOps, security guardrail, service catalog를 통합하는 개발자 운영 허브로 발전함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "플랫폼 엔지니어링과 IDP를 설명하시오" | 서비스 생성부터 scorecard까지 흐름 | 전통 DevOps 대비 차이 |
| 요구사항 명시형 | "IDP 구축 방안을 제시하시오", "운영 방안을 설계하시오" | golden path와 SLO 운영 | 채택률·거버넌스·플랫폼 장애 대응 |
> 요약: 설명형은 IDP 구조를, 구축·운영형은 developer journey와 scorecard 지표 중심으로 작성한다.
