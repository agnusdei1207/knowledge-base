---
title: "OWASP LLM Top 10 (OWASP LLM Top 10)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 145
---

# 📖 【암기용】 개념 완전 이해

> 목적: OWASP LLM Top 10을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: LLM 애플리케이션에서 반복 발생하는 대표 보안 위험 10가지를 정리한 OWASP 가이드
- **왜 필요한가**: LLM 앱은 프롬프트, 검색 데이터, 플러그인, 에이전트 도구, 모델 공급망이 결합된다. 기존 웹 취약점만으로는 프롬프트 주입, 민감정보 노출, 과도한 권한 같은 AI 특화 위험을 설명하기 어렵다.
- **핵심 직관**: 웹 보안의 OWASP Top 10이 웹 취약점 체크리스트라면, LLM Top 10은 AI 앱 설계·검증·운영의 위협 모델 체크리스트다.

## 깊이 이해
- **배경·문제의식**: 생성형 AI가 사내 문서, 고객 데이터, 업무 시스템 API와 연결되면서 LLM은 단순 챗봇이 아니라 권한을 가진 실행 주체가 되었다. 잘못된 프롬프트나 도구 호출은 데이터 유출과 업무 오작동으로 이어진다.
- **작동 원리**: OWASP LLM Top 10은 프롬프트 주입, 민감정보 노출, 공급망, 데이터/모델 오염, 부적절한 출력 처리, 과도한 에이전시 등 위험을 범주화하고 통제 방향을 제시한다.
- **비유**: 새 공장 설비를 들일 때 전기, 안전, 출입, 작업 절차 점검표를 보는 것처럼 LLM 앱의 설계 점검 항목을 제공한다.
- **구체 예시**: RAG 챗봇이 문서 권한 필터 없이 벡터 검색을 수행하면, 사용자가 접근 권한이 없는 계약서 내용을 답변으로 받을 수 있어 "Sensitive Information Disclosure" 위험이 된다.
- **흔한 오해·주의점**: "LLM Top 10을 체크하면 규정 준수 완료"가 아니다. 조직의 데이터 등급, 도구 권한, 로그 보존, 모델 공급망에 맞춰 구체 통제와 지표를 설계해야 한다.

## 연결 개념
- Prompt Injection: LLM 입력을 통해 시스템 지시와 도구 호출을 우회하는 대표 위험
- RAG Security: 검색 권한, 출처 검증, 민감정보 마스킹이 LLM 보안의 핵심 구성
- AI Governance: 정책, 위험 평가, 감사 로그, 승인 절차로 LLM 운영을 통제함

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: OWASP LLM Top 10은 LLM 앱의 위협을 프롬프트·데이터·모델·도구·운영 통제로 구조화하는 보안 기준이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OWASP LLM Top 10은 LLM 애플리케이션의 대표 위험을 식별하고 설계·개발·운영 단계별 통제 항목으로 전환하는 보안 프레임워크이다.
> 2. **가치**: 방어는 입력 필터가 아니라 권한 기반 RAG, 출력 검증, 도구 최소권한, 모델 공급망, 로그·감사를 함께 설계해야 한다.
> 3. **판단 포인트**: 사내 데이터와 업무 API를 연결한 LLM은 Prompt Injection, Sensitive Information Disclosure, Excessive Agency를 우선 통제한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| LLM 보안 위험 체계 이해 | 프롬프트, 데이터, 공급망, 도구, 출력, 운영 위험 | 웹 OWASP Top 10과 동일하게만 설명 |
| 통제 설계 역량 확인 | guardrail, RBAC, DLP, sandbox, logging, red-team | 프롬프트 필터 하나로 대응 제시 |
| 실무 적용 기준 제시 | 위험 평가, 우선순위, 측정 지표, 감사 증적 | 10개 항목 이름 나열 후 판단 기준 누락 |
> 요약: 이 문제는 LLM 위험 목록 암기가 아니라 위험을 아키텍처 통제와 운영 지표로 바꾸는 능력을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: LLM 보안 위험 10대 기준
- 배경: LLM은 자연어 입력, 외부 지식, 도구 호출, 모델 공급망을 결합하므로 기존 웹 취약점과 다른 공격면이 생김.
- 필요성: OWASP LLM Top 10 기준으로 위협 모델, 권한 통제, 출력 검증, 감사 로그를 LLM 애플리케이션 설계에 반영해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
User / Document / Tool -> LLM App -> Model / RAG / Agent
                       +-> Policy / Guardrail / Logging
OWASP LLM Top 10 -> Threat Mapping -> Control Design -> Audit Evidence
```

| 구성요소 | 역할 | 통제 포인트 |
|:---|:---|:---|
| 입력·프롬프트 | 사용자 지시, 문서 내용, 시스템 프롬프트 처리 | prompt injection test, allowlist |
| 데이터·RAG | 벡터 검색, 문서 권한, 민감정보 처리 | RBAC filter, DLP, citation |
| 모델·공급망 | 모델, 플러그인, 어댑터, 학습 데이터 관리 | SBOM/ML-BOM, signature, scan |
| 도구·에이전트 | API 호출, 업무 실행, 외부 연동 | least privilege, sandbox, approval |
| 운영·감사 | 로그, 모니터링, 사고 대응 | SIEM, red-team, audit trail |
> 요약: LLM Top 10은 입력 필터가 아니라 프롬프트, 데이터, 모델, 도구, 운영 전 계층의 통제 구조로 적용해야 한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 범위 정의 -> LLM Top 10 위험 매핑 -> 통제 설계
-> 테스트/레드팀 -> 배포 승인 -> 로그/감사/개선
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용 데이터·모델·도구·권한 범위 식별 | data class, API permission |
| 2 | LLM Top 10 항목별 위협 매핑 | risk register, threat scenario |
| 3 | guardrail, RBAC, DLP, sandbox 통제 설계 | control coverage 100% |
| 4 | prompt injection, leakage, agency red-team 수행 | fail case, ASR, leakage rate |
| 5 | 배포 후 로그·감사·재평가 반복 | MTTR, audit evidence, drift |
> 요약: 적용 흐름은 위험 식별에서 끝나지 않고 통제 설계, 레드팀, 배포 승인, 운영 감사로 이어져야 한다.

---

## Ⅳ. 특징

| 구분 | 기존 웹 OWASP Top 10 | OWASP LLM Top 10 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 대상 | 웹 애플리케이션 취약점 | LLM 앱·모델·도구·데이터 위험 | RAG, Agent, API 연동 여부 |
| 대표 위험 | Injection, XSS, Broken Access | Prompt Injection, Data Leakage, Excessive Agency | leakage rate, ASR |
| 통제 방식 | 입력검증, 세션, 인증·인가 | guardrail, RBAC RAG, sandbox, red-team | control coverage 100% |
| 운영 지표 | 취약점 수, 패치율 | 유출률, 정책위반률, tool misuse, 감사로그 | MTTR, alert precision |
> 요약: LLM Top 10은 웹 보안 항목을 대체하는 것이 아니라 AI 앱의 프롬프트·데이터·도구 위험을 추가로 통제하는 기준이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 범위 | 웹 취약점 진단 | LLM 위험 모델링과 통제 설계 | RAG·Agent·업무 API 연결 시 필수 |
| 검증 | SAST/DAST 중심 | prompt red-team, leakage test, tool sandbox | 자연어 입력이 실행 권한에 영향 |
| 운영 | 배포 전 점검 | 지속 로그·감사·정책 업데이트 | 모델·데이터 변경 주기 1개월 이하 |
> 요약: LLM Top 10은 AI 기능이 업무 권한과 데이터를 다룰 때 설계 기준과 운영 감사 기준으로 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 프롬프트 주입 | 사용자·문서가 지시문을 덮어씀 | system/user/data 분리, instruction hierarchy | prompt ASR |
| 민감정보 노출 | RAG 권한 필터 누락·로그 저장 | RBAC filter, DLP, PII masking | leakage rate |
| 과도한 에이전시 | 도구 권한 과다·승인 절차 없음 | least privilege, human approval, sandbox | unauthorized tool call |
> 요약: 우선순위 위험은 주입, 정보노출, 과도한 실행권한이며 권한·DLP·승인 통제로 줄인다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 통제 커버리지 | Top 10 항목별 통제 1개 이상, 핵심 3개는 2개 이상 | control matrix, audit checklist |
| 유출·위반 | PII leakage 0건, policy violation 1% 이하 | red-team set, DLP log |
| 운영 대응 | LLM 보안 사고 MTTR 4시간 이하 | SIEM, incident ticket, postmortem |
> 요약: 적용 효과는 위험 항목별 통제 커버리지, 유출률, 사고 대응 시간으로 측정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 위험 매핑: 서비스별 데이터 등급, 모델, RAG, 도구 권한을 표준화하고 OWASP LLM Top 10별 control matrix를 작성
2. 기술 통제: prompt injection 테스트, RBAC 기반 검색 필터, DLP/PII masking, tool sandbox, human approval을 배포 게이트에 포함
3. 운영 감사: LLM 요청·검색 문서·도구 호출·응답을 trace ID로 묶고 SIEM 경보, 월 1회 red-team, MTTR 4시간 기준으로 점검

**결론 (2줄):**
- 기술사 판단: LLM이 사내 데이터와 업무 API에 연결되면 OWASP LLM Top 10을 기준으로 설계·검증·운영 통제를 통합해야 함
- 향후 방향: AI TRiSM, NIST AI RMF, OWASP LLM 통제가 결합되어 생성형 AI 보안 감사의 표준 체크리스트가 됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OWASP LLM Top 10을 설명하시오" | 위험 매핑, 통제 설계, 레드팀 흐름 | 기존 웹 OWASP와 LLM 위험 차이 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "보안 설계를 하시오" | control matrix, RAG 권한, tool sandbox 절차 | 유출률, ASR, MTTR 기반 운영 기준 |
> 요약: 설명형은 위험 체계, 설계형은 통제 매트릭스와 운영 지표 중심으로 답안을 전환한다.
