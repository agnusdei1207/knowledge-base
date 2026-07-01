---
title: "정렬 (AI Alignment)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 97
---

# 📖 【암기용】 개념 완전 이해

> 목적: AI Alignment를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **정의**: AI 모델의 목표·행동·출력이 인간의 의도, 가치, 법규, 조직 정책과 일치하도록 만드는 기술·거버넌스 체계
- **왜 필요한가**: 성능이 높은 모델도 유해 조언, 허위 답변, 개인정보 노출, 정책 위반을 만들 수 있음.
- **핵심 직관**: 똑똑한 직원을 뽑는 것뿐 아니라, 회사 규정과 윤리 기준에 맞게 일하도록 교육·감사하는 것임.

## 깊이 이해
- **배경·문제의식**: LLM은 next-token prediction으로 학습되어 인간 의도와 안전 기준을 직접 최적화하지 않음. Alignment는 SFT, RLHF/DPO, Constitutional AI, guardrail, red-team 평가를 결합함.
- **작동 원리**: 정책·가치 기준을 정의하고, 모델을 지시 수행과 선호 기준에 맞게 학습함. 배포 후에는 입력·출력 필터, 감사로그, 위험 평가로 지속 통제함.
- **비유**: 운전 능력이 뛰어난 운전자에게 교통법규, 회사 운행 규정, 사고 대응 절차를 함께 훈련시키는 것과 같음.
- **구체 예시**: 금융 상담 AI는 투자권유 규정, 개인정보보호, 설명 가능성 기준을 만족해야 하며 refusal rate와 policy violation을 측정함.
- **흔한 오해·주의점**: Alignment는 한 번의 학습으로 끝나지 않음. 모델 업데이트, 새로운 공격, 정책 변화에 따라 지속 평가가 필요함.

## 연결 개념
- RLHF/DPO — 선호 기반 정렬 기법
- Constitutional AI — 규칙 기반 정렬
- AI Governance — 조직 차원의 통제 체계

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AI Alignment는 모델 행동을 인간 의도·안전·법규·조직 정책에 맞추는 기술·운영 체계임.
> 2. **가치**: 유해 출력, 환각, 개인정보 노출, 규제 위반을 줄여 AI 서비스 신뢰성을 확보함.
> 3. **판단 포인트**: 정책 정의, 정렬 학습, guardrail, red-team, 지속 모니터링을 통합해야 함.

## Ⅰ. 개요 및 필요성

AI Alignment는 AI 행동 정렬 체계임. 고성능 생성형 AI도 인간 의도와 조직 정책을 벗어난 출력을 생성할 수 있으므로, 학습·평가·운영 통제를 결합한 정렬이 필요함.

## Ⅱ. 구조 및 구성요소

```text
Policy/Values → SFT/RLHF/DPO/Constitutional AI
      → Guardrail → Red-team/Evaluation → Monitoring
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Policy | 금지·허용 기준 정의 | 법규·조직 규정 |
| Alignment Training | 모델 행동 조정 | SFT, RLHF, DPO |
| Guardrail | 입출력 실시간 통제 | PII, toxicity |
| Evaluation | 정렬 수준 검증 | red-team, benchmark |

> 요약: Alignment는 정책 정의부터 학습, 실시간 통제, 평가, 모니터링까지 이어지는 폐루프 체계임.

## Ⅲ. 동작원리 및 흐름도

```text
위험 기준 정의 → 정렬 데이터 생성 → 모델 학습
    → 안전성 평가 → 배포 guardrail → 로그 기반 개선
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 도메인별 위험·정책 정의 | risk taxonomy |
| 2 | 선호·거부·안전 데이터 학습 | policy coverage |
| 3 | red-team·회귀 평가 | violation rate |
| 4 | 운영 로그로 재정렬 | incident, drift |

> 요약: Alignment는 사전 학습보다 운영 중 정책 위반을 측정하고 다시 개선하는 지속 프로세스임.

## Ⅳ. 특징

| 구분 | 성능 최적화 | Alignment | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 목표 | 정확도·처리량 | 유용성·무해성·정직성 | HHH 기준 |
| 방법 | pretraining/SFT | RLHF/DPO/guardrail | 다층 통제 |
| 지표 | accuracy, loss | violation, refusal, toxicity | domain별 기준 |
| 리스크 | 과소성능 | 과거부·편향 | 균형 평가 |

> 요약: Alignment는 정확도와 별개로 안전·정책 준수 지표를 관리하며 과거부와 편향도 함께 통제해야 함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 금융·의료·공공 AI는 금지 질의, 허용 답변, escalation 기준을 policy taxonomy로 정의
2. RLHF/DPO와 출력 guardrail을 결합하고 violation rate 0.1% 이하 등 도메인별 SLO를 설정
3. red-team, 감사로그, incident review로 월 단위 재평가와 데이터 보강 루프를 운영

**결론 (2줄):**
- 기술사 판단: 고위험 도메인은 학습 정렬+guardrail+감사 체계, 저위험 업무는 prompt policy와 로그 모니터링부터 적용함.
- 향후 방향: Alignment는 AI 규제, ISO/IEC 42001, AI risk management와 결합해 거버넌스 체계로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | 정책→학습→평가→운영 흐름 | 성능 최적화 대비 특징 |
| 요구사항 명시형 | 관리 방안을 제시하시오 | 위험분류·guardrail·감사 절차 | 규제·위반율·과거부 기준 |

> 요약: 설명형은 정렬 체계 전반, 관리형은 위험 기반 통제와 지속 평가 중심으로 목차를 전환함.
