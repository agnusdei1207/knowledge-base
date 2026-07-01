---
title: "헌법형 AI (Constitutional AI)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 98
---

# 📖 【암기용】 개념 완전 이해

> 목적: Constitutional AI를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 사람이 일일이 선호를 라벨링하지 않고, 명시된 원칙 목록(constitution)에 따라 AI가 자기 비판·수정을 수행하게 하는 정렬 방식
- **왜 필요한가**: RLHF는 인간 라벨링 비용이 크고, 안전 기준이 라벨러마다 흔들릴 수 있음.
- **핵심 직관**: 회사 윤리강령을 모델에게 주고, 스스로 답안을 검토·수정하게 한 뒤 그 원칙을 따르도록 학습시키는 방식임.

## 깊이 이해
- **배경·문제의식**: 유해·편향·개인정보 응답은 명확한 원칙이 필요함. Constitutional AI는 “도움되되 해롭지 않게”, “개인정보를 노출하지 않게” 같은 규칙으로 critique와 revision 데이터를 생성함.
- **작동 원리**: 모델이 초기 답변을 만들고, constitution 원칙에 따라 스스로 비판한 뒤 수정 답변을 생성함. 수정 데이터는 SFT 또는 RLAIF 학습에 활용됨.
- **비유**: 학생이 답안 제출 전 채점기준표를 보고 자기 답안을 빨간펜으로 고친 뒤 다시 제출하는 것과 같음.
- **구체 예시**: 안전 정책, 인권 원칙, 법규 준수 규칙을 constitution으로 정의하고 AI evaluator가 답변을 비판·수정함.
- **흔한 오해·주의점**: 헌법이 있으면 자동으로 안전한 것은 아님. 원칙 간 충돌, 모호한 문장, 도메인별 법규 차이를 별도로 설계해야 함.

## 연결 개념
- RLAIF — AI feedback 기반 학습
- AI Alignment — Constitutional AI의 목적
- Guardrail — 배포 단계 보완 통제

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Constitutional AI는 명시 원칙을 기준으로 AI가 답변을 비판·수정하고 이를 정렬 학습에 사용하는 방식임.
> 2. **가치**: 인간 라벨링 의존도를 줄이고 일관된 안전 원칙을 모델 행동에 반영함.
> 3. **판단 포인트**: constitution 품질, 원칙 충돌, domain policy, AI critique 품질, 인간 감사가 핵심임.

## Ⅰ. 개요 및 필요성

- 개요: 원칙 기반 AI 정렬 기법
- 배경: 인간 선호 라벨링은 비용이 크고 라벨러별 판단 기준이 달라 정렬 데이터의 일관성이 흔들릴 수 있음.
- 필요성: constitution principles, AI critique, revision data, human audit로 정책 일관성과 고위험 출력 검수율을 관리해야 함.

## Ⅱ. 구조 및 구성요소

```text
Constitution Principles -> Initial Answer -> AI Critique
      -> Revised Answer -> SFT/RLAIF Training -> Evaluation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Constitution | 원칙·금지 기준 | 안전·법규·윤리 |
| Critique Model | 답변 문제 지적 | 원칙 기반 평가 |
| Revision | 수정 답변 생성 | 자기 개선 데이터 |
| Human Audit | 원칙·출력 검수 | 고위험 샘플 |

> 요약: Constitutional AI는 명시 원칙으로 답변을 비판·수정하고 그 데이터를 정렬 학습에 연결함.

## Ⅲ. 동작원리 및 흐름도

```text
원칙 수립 -> 초안 답변 생성 -> 원칙 기반 critique
    -> 수정 답변 생성 -> 학습 데이터화 -> 안전성 평가
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | constitution 원칙 작성 | 법규·정책 coverage |
| 2 | 모델 답변 critique 수행 | critique accuracy |
| 3 | revised answer 생성·필터링 | violation 감소율 |
| 4 | SFT/RLAIF 학습·평가 | toxicity, refusal |

> 요약: 헌법형 AI는 정책 원칙을 학습 데이터 생성 과정에 직접 넣어 안전 정렬을 자동화함.

## Ⅳ. 특징

| 구분 | RLHF | Constitutional AI | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 기준 | 인간 선호 | 명시 원칙 | constitution 품질 |
| 비용 | 라벨링 비용 큼 | AI critique 활용 | 인간 감사 필요 |
| 일관성 | 라벨러 편차 | 원칙 일관성 | 원칙 충돌 관리 |
| 한계 | 확장성 | 규칙 모호성 | domain별 보완 |

> 요약: Constitutional AI는 일관된 안전 원칙을 확장 가능하게 적용하지만, 원칙 설계와 충돌 해결이 성패를 좌우함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 금융·의료·교육 AI는 도메인 법규와 조직 정책을 constitution으로 작성하고 정책 owner 승인 절차를 둠
2. AI critique 결과 중 고위험·원칙 충돌 샘플 5~10%를 인간 감사로 검토
3. 배포 전후 violation rate, over-refusal, bias 지표를 추적하고 constitution 버전을 감사로그에 기록

**결론 (2줄):**
- 기술사 판단: 일관된 정책 정렬과 라벨 비용 절감이 목표면 Constitutional AI, 고위험 판단은 RLHF·인간 검토를 병행함.
- 향후 방향: Constitutional AI는 AI 거버넌스 정책을 모델 학습·평가·운영에 연결하는 핵심 패턴이 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | 원칙->critique->revision 흐름 | RLHF 대비 특징 |
| 요구사항 명시형 | 적용 방안을 제시하시오 | constitution 작성·감사 절차 | 법규·원칙충돌·과거부 기준 |

> 요약: 설명형은 원칙 기반 정렬 원리, 적용형은 정책 문서화와 인간 감사 기준으로 목차를 전환함.
