---
title: "AI 위험관리 (AI Risk Management)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 165
---

# 📖 【암기용】 개념 완전 이해

> 목적: AI Risk Management를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: AI 시스템에서 발생 가능한 기술·법규·윤리·보안·운영 위험을 식별·평가·완화·모니터링하는 활동
- **왜 필요한가**: AI는 편향, 환각, 개인정보 유출, 보안 공격, 저작권 침해, 자동화 오류 등 복합 위험을 가진다.
- **핵심 직관**: AI를 배포하기 전과 후에 "무엇이 잘못될 수 있고 어떻게 막을 것인가"를 계속 관리하는 절차임.

## 깊이 이해
- **배경·문제의식**: AI 모델은 데이터와 환경 변화에 따라 성능이 변하고, 생성형 AI는 예측 불가능한 출력을 만들 수 있다.
- **작동 원리**: use case별 위험 시나리오를 식별하고 가능성·영향도를 평가한 뒤, 통제조치와 잔여위험 승인을 거쳐 운영 모니터링을 수행함.
- **비유**: 공장 설비의 위험성 평가처럼 AI 기능마다 사고 시나리오, 예방장치, 점검 주기, 책임자를 지정하는 작업임.
- **구체 예시**: 고객 상담 LLM에서 prompt injection, PII leakage, hallucination, toxic output을 위험 register에 등록하고 각각 차단율·탐지율 KPI를 설정.
- **흔한 오해·주의점**: 모델 정확도만 높으면 위험이 낮아지는 것이 아님. 법무·보안·운영·사용자 영향 위험을 별도 평가해야 함.

## 연결 개념
- NIST AI RMF — AI 위험관리 기능 체계
- AI Governance — 위험관리를 조직 의사결정과 연결
- AI Red Teaming — 보안·안전 위험을 공격적으로 검증

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AI Risk Management는 AI 위험을 식별·평가·완화·모니터링하는 지속 활동임.
> 2. **가치**: 편향·환각·보안·개인정보·규제 위험을 배포 전후 통제해 사고 비용을 줄임.
> 3. **판단 포인트**: 위험 register, 정량 지표, residual risk 승인, 사고 대응 체계가 핵심임.

## Ⅰ. 개요 및 필요성

- 개요: AI 위험 식별·통제 활동
- 배경: AI 시스템은 데이터, 모델, 사용자, 환경 변화에 따라 편향, 환각, 보안, 법규 위반 위험을 만든다.
- 필요성: risk register, control mapping, monitoring metric으로 사전 식별, 완화 조치, 운영 중 재평가를 수행한다.

## Ⅱ. 구조 및 구성요소

```text
AI Use Case -> Risk Identification -> Risk Assessment
  -> Mitigation Controls -> Residual Approval -> Monitoring
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Risk Register | 위험 시나리오 목록화 | owner, likelihood, impact |
| Assessment | 가능성·영향도·등급 평가 | 5×5 matrix |
| Mitigation | 예방·탐지·대응 통제 | guardrail, testing, review |
| Monitoring | 운영 지표·사고 감시 | drift, abuse, incident |

> 요약: AI 위험관리는 위험을 등록·평가하고 통제조치를 적용한 뒤 잔여위험과 운영 지표를 지속 관리함.

## Ⅲ. 동작원리 및 흐름도

```text
위험 시나리오 도출 -> 가능성/영향도 평가
  -> 통제조치 설계 -> 잔여위험 승인 -> 운영 모니터링/개선
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 데이터·모델·출력·사용자 위험 식별 | 고위험 use case 100% 평가 |
| 2 | 가능성×영향도 기반 등급 산정 | high risk 누락 0건 |
| 3 | 통제조치와 owner 지정 | mitigation owner 100% |
| 4 | 운영 지표·사고 대응 관리 | critical incident SLA 24시간 |

> 요약: AI 위험은 시나리오 기반으로 식별하고 등급화한 뒤 통제 책임자와 모니터링 지표로 운영함.

## Ⅳ. 특징

| 구분 | 전통 IT 위험 | AI 위험 | 판단 포인트 |
|:---|:---|:---|:---|
| 위험 원인 | 취약점·장애 | 데이터 편향·모델 출력·오남용 | AI 특화 지표 필요 |
| 측정 | CVSS·가용성 | bias, drift, hallucination, toxicity | 다차원 평가 |
| 통제 | 패치·접근제어 | guardrail·red team·human review | 수명주기 통제 |
| 변화 | 비교적 예측 가능 | 데이터·프롬프트 변화 민감 | 지속 모니터링 |

> 요약: AI 위험관리는 전통 IT 위험에 모델·데이터·출력 위험을 추가해 수명주기 기반으로 관리함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 위험 register: hallucination, bias, PII leakage, prompt injection, copyright, model drift를 use case별 등록
2. 정량 지표: Faithfulness 0.9, PII 탐지율 95%, jailbreak 차단율 99%, drift PSI 0.2 이하 기준 설정
3. 대응 체계: high risk는 human approval, critical incident는 24시간 내 차단·보고·재발방지 조치

**결론 (2줄):**
- 기술사 판단: AI 위험은 모델 정확도와 별개로 식별·완화·모니터링해야 하는 운영 리스크임
- 향후 방향: AI RMF, ISO 42001, EU AI Act 요구를 통합한 AI GRC 자동화로 발전

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "AI Risk Management를 설명하시오" | 식별->평가->완화->모니터링 흐름 | 전통 IT 위험 대비 차이 |
| 요구사항 명시형 | "AI 위험관리 방안을 제시하시오" | 위험 register·지표·SLA 기준 | 거버넌스·GRC 연계 방안 |

> 요약: 설명형은 위험관리 절차, 방안형은 정량 지표와 사고 대응 체계를 중심으로 작성함.
