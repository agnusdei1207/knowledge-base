+++
title = "064. DREAD 모델 — Damage/Reproducibility/Exploitability/Affected Users discoverability"
date = 2026-04-05

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DREAD는 위협의 위험도를 Damage, Reproducibility, Exploitability, Affected Users, Discoverability 다섯 축으로 점수화하는 위험 평가 모델이다.
> 2. **가치**: 정성적인 위협 목록을 정량 점수로 바꾸면 우선순위가 명확해지고, 보안 개선 순서도 정리된다.
> 3. **판단**: DREAD는 [STRIDE](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) 같은 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 도구와 함께 써야 하고, 점수는 절대값이 아니라 비교용 지표로 봐야 한다.

---

## Ⅰ. 개요 및 필요성

위협을 찾는 것과, 그중 무엇부터 고칠지 결정하는 것은 다르다. DREAD는 후자를 돕는 도구다.

보안 예산은 한정되어 있으므로, 모든 위협을 같은 무게로 다루면 안 된다. DREAD는 위험의 크기를 숫자로 바꿔 대화하게 해 준다.

- **📢 섹션 요약 비유**: 사고 가능성뿐 아니라 다칠 사람 수와 고칠 난이도까지 함께 보는 점수표다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Threat
  v
DREAD Factors
  v
Score
  v
Priority
  v
Mitigation
```

| 항목 | 의미 |
| :-- | :-- |
| Damage | 피해 규모 |
| Reproducibility | 재현 가능성 |
| Exploitability | 공격 난이도 |
| Affected Users | 영향 받는 사용자 수 |
| Discoverability | 발견 가능성 |

각 항목을 1~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 정도의 점수로 평가하고 평균 또는 가중치로 우선순위를 정한다. 핵심은 "느낌"이 아니라 "같은 기준"이다.

- **📢 섹션 요약 비유**: 위험한 문제를 색깔 대신 숫자로 표시해 놓는 메모장이다.

---

## Ⅲ. 비교 및 연결

| 프레임 | 역할 | 강점 | 주의점 |
| :-- | :-- | :-- | :-- |
| [STRIDE](/knowledge-base/studynote/10_ai/01_ai_basics/097_stride_convolutional_neural_network_downsampling/) | 위협 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 공격 유형 구분 | 정량화 약함 |
| DREAD | 위험 점수화 | 우선순위화 | 점수 주관성 |
| [MITRE ATT&CK](/knowledge-base/studynote/09_security/13_secops_ir_forensics/642_mitre_attack/) | 공격 전술/기법 | 실제 공격자 관점 | 설계 초기에 과할 수 있음 |

DREAD는 위협을 "많다/적다"가 아니라 "먼저/나중"으로 바꾸는 데 유용하다. 그래서 설계 검토와 보안 백로그 정리에 잘 맞는다.

- **📢 섹션 요약 비유**: 장바구니에 물건을 담을 때, 무거운 것부터 들지 가벼운 것부터 들지 정하는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 점수 기준을 팀에서 합의했는가?
2. 점수 결과를 실제 우선순위와 연결했는가?
3. STRIDE나 아키텍처 리뷰와 함께 사용했는가?
4. 정량 점수를 절대값처럼 오해하지 않았는가?
5. 반복 평가로 점수 기준을 보정하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 점수만 매기고 아무 조치도 하지 않는 설계
- 모든 항목을 똑같이 중요하다고 두는 설계
- 팀마다 다른 기준으로 점수를 내는 설계
- DREAD만으로 보안 의사결정을 끝내는 설계

기술사 관점에서는 DREAD를 보안 "계산기"가 아니라 "우선순위 정렬 도구"로 봐야 한다. 숫자는 결론이 아니라 토론의 시작이다.

- **📢 섹션 요약 비유**: 줄 세우기를 쉽게 해 주지만, 최종 판단은 사람이 해야 한다.

---

## Ⅴ. 기대효과 및 결론

DREAD를 쓰면 보안 논의가 구체적이고 반복 가능해진다. 무엇보다 같은 기준으로 여러 위협을 비교할 수 있다.

결론적으로 DREAD는 위험을 비교 가능한 언어로 바꾸는 보조 도구다.

- **📢 섹션 요약 비유**: 모두가 같은 눈금의 자를 들고 있으면 길이를 비교하기 쉬워진다.

---

## 관련 개념 맵

```text
Threat
  v
DREAD
  v
Priority
  v
Mitigation Plan
```

---

## 관련 키워드 및 발전 흐름도

```text
Threat Identification
  v
Risk Scoring
  v
DREAD
  v
Security Backlog
```

---

## 어린이를 위한 3줄 비유 설명

무서운 일을 숫자로 적어 보면 어떤 게 더 급한지 알 수 있어요.
사람이 많이 다칠수록 점수가 높아요.
DREAD는 그런 위험 점수표예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 64 / 1108

<- **이전**: [063. 위협 모델링 (Threat Modeling)](/knowledge-base/studynote/09_security/01_intro_principles/063_threat_modeling/)
**다음**: [065. STRIDE 모델 — Spoofing/Tampering/Repudiation/Information Disclosure/DoS/Elevation](/knowledge-base/studynote/09_security/01_intro_principles/065_stride_model/) ->

---
