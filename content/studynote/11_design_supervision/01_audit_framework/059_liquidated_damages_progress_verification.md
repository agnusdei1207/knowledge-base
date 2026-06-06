---
title: "059. Liquidated Damages Progress Verification"
date: "2026-04-05"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 지체 상금(Liquidated Damages)은 계약상 정해진 종료일을 넘겼을 때 사전 합의된 금액을 부과하는 조항이다.
> 2. **가치**: 감리인은 실제 진척도와 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 사유를 객관적 증빙으로 구분해 분쟁을 줄여야 한다.
> 3. **판단 포인트**: 사업자 귀책, 발주자 귀책, 외부 요인을 나눠 보고, 과업변경과 일정 영향도 함께 검증해야 한다.

---

## Ⅰ. 개요 및 필요성

공공 정보화 사업에서는 종료일 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 곧 비용과 책임 문제로 이어진다. 지체 상금은 이런 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)에 대해 미리 합의한 배상 규칙이다.

문제는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 항상 사업자 탓만은 아니라는 점이다. 요구사항 변경, 외부 시스템 연동 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 발주자 검토 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 섞이면 책임 판단이 복잡해진다.

- **📢 섹션 요약 비유**: 책을 늦게 반납하면 벌금이 있지만, 도서관이 문을 닫아 놓은 날은 이야기가 달라진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

감리의 핵심은 계획 대비 실제를 비교할 수 있는 기준과 기록을 갖추는 것이다. [WBS](/studynote/12_it_management/04_sdlc_testing/149_wbs_work_breakdown_structure/)([Work Breakdown Structure](/studynote/12_it_management/04_sdlc_testing/149_wbs_work_breakdown_structure/)), PMIS([Project](/studynote/05_database/01_db_architecture_relational/042_relational_algebra_project/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/) Information System), 변경 요청서가 이 기준을 만든다.

```text
계약 종료일
   v
기준 계획(Baseline)
   v
실제 진척 / 변경 요청
   v
지연 사유 분류
   v
지체 상금 여부 판단
```

| 항목 | [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 포인트 |
| :-- | :-- |
| 진척도 | [WBS](/studynote/12_it_management/04_sdlc_testing/149_wbs_work_breakdown_structure/) [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/), 마일스톤, 산출물 완료 여부 |
| 변경 기록 | 과업변경 요청서, 회의록, 승인 시점 |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 사유 | 사업자 귀책 / 발주자 귀책 / 외부 요인 |
| 증빙 | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 이메일, 검수 문서, 시스템 기록 |

지체 상금 판단은 "얼마나 늦었는가"만이 아니라 "왜 늦었는가"를 함께 봐야 한다. 일정 변화가 공식 승인되었다면 책임 비율도 달라질 수 있다.

- **📢 섹션 요약 비유**: 숙제 제출이 늦었는지, 선생님이 제출일을 바꿨는지를 함께 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것과 같다.

---

## Ⅲ. 비교 및 연결

[지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 사유는 보통 네 범주로 나눈다.

| 범주 | 예시 | 판단 |
| :-- | :-- | :-- |
| 사업자 귀책 | 설계 오류, 인력 부족, 내부 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 지체 상금 부과 대상 |
| 발주자 귀책 | 요구사항 변경, 검토 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 일정 조정 가능 |
| 외부 요인 | 법령 변경, 천재지변, 연동 대상 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 별도 인정 검토 |
| 혼합 책임 | 변경 이후 대응 미흡 | 비율 분리 필요 |

진척도 측정도 하나만 쓰면 위험하다. 기간 기반, 금액 기반보다 산출물 기반과 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 기반이 더 객관적이다. 그래서 감리인은 문서와 시스템 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 함께 봐야 한다.

- **📢 섹션 요약 비유**: 시험 점수를 볼 때 출석만 보지 말고, 과제와 시험지를 같이 보는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

지체 상금 분쟁을 막으려면 "누가 늦었나"보다 "무엇이 기록되어 있나"를 먼저 봐야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 계약상 종료일과 실제 종료일이 명확한가?
2. 변경 요청과 승인 시점이 기록되어 있는가?
3. 진척률 데이터와 보고서가 일치하는가?
4. [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 사유별 책임 비율이 문서화되어 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 구두 합의만 믿고 일정 변경을 기록하지 않는 설계
- 진척률을 감으로만 적는 설계
- 사업자/발주자/외부 요인을 구분하지 않는 설계

### 실무 시나리오

- 과업변경으로 일정이 늘어난 경우
- 외부 시스템 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)으로 통합이 밀린 경우
- 산출물은 완성됐지만 검수가 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)된 경우

- **📢 섹션 요약 비유**: 누가 먼저 밀었는지, 넘어지기 전 합의가 있었는지를 꼭 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 하는 줄다리기다.

---

## Ⅴ. 기대효과 및 결론

정확한 증빙과 진척 관리가 있으면 지체 상금은 감정 싸움이 아니라 계약 해석의 문제로 정리된다. 그 결과 사업자와 발주자 모두 예측 가능성이 높아진다.

감리의 역할은 돈을 매기는 것이 아니라, 책임의 경계를 사실로 설명하는 것이다. 결국 지체 상금 관리의 핵심은 기록, 비교, 검증이다.

- **📢 섹션 요약 비유**: 블랙박스가 있어야 사고 후에 누가 무엇을 했는지 차분히 볼 수 있다.

---

## 관련 개념 맵

```text
계약 종료일
   v
진척도 측정
   v
지연 사유 분류
   v
지체 상금 판단
```

---

## 관련 키워드 및 발전 흐름도

```text
계약 기준
   v
WBS / PMIS
   v
변경 요청 관리
   v
증빙 기반 진척도 검증
   v
분쟁 예방과 책임 비율 산정
```

---

## 어린이를 위한 3줄 비유 설명

책을 늦게 내면 벌금을 낼 수 있어요.
하지만 선생님이 마감일을 바꿨다면 이야기가 달라져요.
그래서 언제, 왜, 누가 바꿨는지 기록을 꼭 봐야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 89 / 530

<- **이전**: [58. 고가용성 및 이중화 클러스터 페일오버 시나리오 실지 테스트 참관 (HA Failover Test Audit)](/studynote/11_design_supervision/01_audit_framework/630_ha_failover_test_audit/)
**다음**: [59. 보안 장비 정책 룰셋 최적화 상태 점검 (Security Device Ruleset Audit)](/studynote/11_design_supervision/01_audit_framework/631_security_device_ruleset_audit/) ->

---
