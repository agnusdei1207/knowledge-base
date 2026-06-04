---
title: "412. 행위 주도 개발 (Behavior-Driven Development)"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)
1. **본질**: 행위 주도 개발 ([Behavior-Driven Development](/studynote/04_software_engineering/02_requirements_analysis/126_bdd_behavior_driven_development_given_when_then/), [BDD](/studynote/12_it_management/04_sdlc_testing/165_bdd_behavior_driven_development/))은 사용자 관점의 행위와 기대 결과를 공통 언어로 정의해 개발·테스트·업무를 정렬하는 접근법이다.
2. **가치**: 요구사항 오해를 줄이고 [인수 기준](/studynote/04_software_engineering/03_design_architecture/165_acceptance_criteria_definition/)을 자동화 가능한 시나리오로 바꾸어 품질과 소통 효율을 함께 높인다.
3. **판단 포인트**: [유비쿼터스 언어](/studynote/04_software_engineering/04_testing_quality/220_ubiquitous_language_ddd_communication/) ([Ubiquitous Language](/studynote/04_software_engineering/04_testing_quality/220_ubiquitous_language_ddd_communication/))의 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 시나리오의 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능성, 문서와 자동화의 연계 수준을 점검해야 한다.

## Ⅰ. 개요 및 필요성
BDD는 “무엇을 만들 것인가”보다 “사용자가 어떤 행위를 했을 때 어떤 가치를 얻는가”를 먼저 서술한다. 그래서 개발자 중심의 기능 목록보다 비즈니스 맥락이 선명해지고, 요구사항의 숨은 가정이 빠르게 드러난다. 시험에서는 BDD를 단순 테스트 기법이 아니라 [이해관계자](/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/) 간 의미를 맞추는 요구사항 정렬 프레임으로 설명해야 한다.

특히 업무 시스템에서 실패하는 원인 중 상당수는 구현 기술 부족이 아니라 용어 불일치다. 같은 “승인”, “완료”, “정산”이라는 말도 부서마다 의미가 다르면 테스트와 운영이 모두 어긋난다. BDD는 이런 문제를 방지하기 위해 시나리오와 [유비쿼터스 언어](/studynote/04_software_engineering/04_testing_quality/220_ubiquitous_language_ddd_communication/)를 중심으로 요구를 구조화한다.

```text
+------------+   +------------+   +------------+
| 사용자 행위 |--->| 공통 언어   |--->| 검증 시나리오 |
+------------+   +------------+   +------------+
```

따라서 감리 시에는 화면 목록이나 기능 목록만 확인할 것이 아니라, 시나리오가 실제 업무 흐름과 같은 말을 쓰고 있는지 반드시 확인해야 한다.
- **📢 섹션 요약 비유**: 같은 지도를 보고 같은 지명으로 말해야 길을 잃지 않는다.

## Ⅱ. 아키텍처 및 핵심 원리
BDD의 대표 형식은 Given-When-Then이다. Given은 전제 조건, When은 행위, Then은 기대 결과를 나타낸다. 이를 [도메인 주도 설계](/studynote/12_it_management/05_security_compliance/310_architecture/) ([Domain-Driven Design](/studynote/04_software_engineering/02_requirements_analysis/127_ddd_domain_driven_design/), [DDD](/studynote/12_it_management/05_security_compliance/310_architecture/))의 [유비쿼터스 언어](/studynote/04_software_engineering/04_testing_quality/220_ubiquitous_language_ddd_communication/)와 결합하면 요구사항, 테스트, 문서가 같은 문장 구조를 공유하게 된다.

| 구성 요소 | 핵심 역할 | 설계·감리 포인트 |
|:---|:---|:---|
| 시나리오 | 사용자 가치와 업무 흐름을 서술 | 업무 용어가 애매하지 않고 측정 가능한 결과를 포함해야 함 |
| 스텝 정의 | 시나리오 문장을 실제 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 코드와 연결 | 자동화 범위와 책임 경계를 명확히 해야 함 |
| 실행 보고 | 통과·실패 결과를 [이해관계자](/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/)에게 공유 | [인수 기준](/studynote/04_software_engineering/03_design_architecture/165_acceptance_criteria_definition/) 변경 시 시나리오와 코드가 동시에 갱신되어야 함 |

```text
+----------+   +----------+   +----------+
| Given    |--->| When     |--->| Then     |
+----+-----+   +----+-----+   +----+-----+
     |              |              |
     +------도메인 용어/자동화 코드로 연결------+
```

핵심 원리는 첫째, 시나리오가 비즈니스 가치를 반영해야 한다는 점이다. 둘째, 문장이 테스트 가능해야 한다. 셋째, 자동화가 어려운 문서는 시간이 지나면 죽은 문서가 되므로 실행 가능한 시나리오로 유지해야 한다. 이 세 가지를 답안에 넣으면 BDD의 본질이 드러난다.
- **📢 섹션 요약 비유**: 연극 대본처럼 등장인물, 행동, 결과가 한 줄로 이어져야 모두가 같은 장면을 떠올릴 수 있다.

## Ⅲ. 비교 및 연결
BDD는 TDD와 자주 비교된다. TDD가 개발자 관점에서 내부 설계를 다듬는다면, BDD는 업무 담당자·기획자·테스터까지 포함한 외부 행위 관점에서 시스템을 설명한다. 따라서 둘은 경쟁 기법이 아니라 계층이 다른 품질 접근법이다.

| 비교 항목 | [BDD](/studynote/12_it_management/04_sdlc_testing/165_bdd_behavior_driven_development/) | [TDD](/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) | 전통 요구사항 문서 |
|:---|:---|:---|:---|
| 중심 관점 | 사용자 행위와 가치 | 코드 단위와 설계 | 기능 목록과 서술 문서 |
| 표현 방식 | Given-When-Then 시나리오 | 실패 테스트와 단정문 | 자연어 설명, 표준 양식 |
| 강점 | 소통, [인수 기준](/studynote/04_software_engineering/03_design_architecture/165_acceptance_criteria_definition/) 명확화 | 빠른 피드백, 구조 개선 | 작성이 익숙하고 범용적 |
| 약점 | 시나리오만 많고 자동화가 약할 수 있음 | 비즈니스 맥락 설명은 약함 | 해석 차이와 최신성 저하 |

또한 BDD는 [인수 테스트](/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/) ([Acceptance Test](/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/)), 예제 기반 명세 ([Specification](/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/) by Example), [사용자 스토리](/studynote/04_software_engineering/02_requirements_analysis/081_user_story_invest/)와 연결된다. 시험에서는 “BDD는 시나리오를 통해 요구사항을 실행 가능한 명세로 만든다”는 문장을 써 주면 좋다.
- **📢 섹션 요약 비유**: 요리법을 말로만 적는 것보다 재료·행동·완성 사진을 함께 보여 주면 모두가 같은 음식을 만든다.

## Ⅳ. 실무 적용 및 기술사 판단
BDD는 고객 여정이 분명한 전자상거래, 금융 승인, 예약, 정산 같은 업무에서 큰 힘을 발휘한다. 반면 계산 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 중심의 내부 라이브러리처럼 사용자 행위 서술이 큰 의미를 갖지 않는 영역에서는 TDD가 더 직접적일 수 있다. 따라서 시스템 전체에 동일 비율로 적용하기보다 업무 흐름이 중요한 경계면에 우선 적용하는 전략이 합리적이다.

실무에서는 시나리오를 잘 썼더라도 자동화 유지 체계가 없으면 금방 형식 문서가 된다. 그래서 [제품 책임자](/studynote/04_software_engineering/02_requirements_analysis/063_product_owner_po/), 품질 담당자, 개발자가 함께 시나리오를 검토하는 3자 협업이 중요하다. 기술사 답안에서는 “용어 표준화 + 시나리오 자동화 + 결과 공유”의 삼박자를 강조하면 좋다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- 핵심 업무 용어가 부서별로 동일한 의미로 사용되는가?
- Given-When-Then 문장이 측정 가능한 기대 결과를 포함하는가?
- 시나리오 변경 시 자동화 코드와 문서가 함께 갱신되는가?
- 예외 흐름과 실패 시나리오가 정상 흐름만큼 충분히 정의되는가?
- [인수 기준](/studynote/04_software_engineering/03_design_architecture/165_acceptance_criteria_definition/)이 화면 단위가 아니라 사용자 가치 단위로 기술되는가?

결국 BDD의 성패는 도구보다 언어 정렬 수준에 달려 있다. 따라서 답안 마무리는 “문장 품질이 곧 시스템 품질의 선행지표”라는 메시지로 정리하면 좋다.
- **📢 섹션 요약 비유**: 운동회 규칙을 모두가 같은 말로 이해해야 경기 결과에 불만이 적다.

## Ⅴ. 기대효과 및 결론
BDD를 도입하면 요구사항 오해로 인한 재작업이 줄고, [인수 기준](/studynote/04_software_engineering/03_design_architecture/165_acceptance_criteria_definition/)이 선명해져 테스트 설계와 사용자 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 쉬워진다. 또한 조직 차원에서는 개발자와 현업의 대화 비용이 낮아지고, 신규 인력이 시스템 맥락을 더 빨리 이해하는 효과도 있다.

결론적으로 BDD는 문서를 예쁘게 쓰는 기법이 아니라, 비즈니스 의미를 실행 가능한 시나리오로 고정하는 방법이다. 기술사 답안에서는 TDD와의 차이, [유비쿼터스 언어](/studynote/04_software_engineering/04_testing_quality/220_ubiquitous_language_ddd_communication/)의 역할, 자동화 유지의 중요성을 균형 있게 제시하는 것이 고득점 포인트다.
- **📢 섹션 요약 비유**: 모두가 같은 대본으로 연습하면 공연 당일에 실수가 줄어드는 것과 같다.

### 📌 관련 개념 맵
- [BDD](/studynote/12_it_management/04_sdlc_testing/165_bdd_behavior_driven_development/) -> [유비쿼터스 언어](/studynote/04_software_engineering/04_testing_quality/220_ubiquitous_language_ddd_communication/) -> 요구사항 정렬
- Given-When-Then -> 실행 가능한 시나리오 -> [인수 기준](/studynote/04_software_engineering/03_design_architecture/165_acceptance_criteria_definition/) 명확화
- 시나리오 자동화 -> 회귀 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) -> 품질 가시성 향상
- [DDD](/studynote/12_it_management/05_security_compliance/310_architecture/) 연계 -> [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 모델 정교화 -> 업무-개발 간 간극 축소

### 📈 관련 키워드 및 발전 흐름도
기능 명세 문서 -> [사용자 스토리](/studynote/04_software_engineering/02_requirements_analysis/081_user_story_invest/) -> [BDD](/studynote/12_it_management/04_sdlc_testing/165_bdd_behavior_driven_development/) 시나리오 -> 예제 기반 명세 -> [인수 테스트](/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/) 자동화 -> 제품 중심 협업 문화

- 핵심 키워드: Given-When-Then, [유비쿼터스 언어](/studynote/04_software_engineering/04_testing_quality/220_ubiquitous_language_ddd_communication/), [인수 기준](/studynote/04_software_engineering/03_design_architecture/165_acceptance_criteria_definition/), 시나리오 자동화, 3자 협업

### 👶 어린이를 위한 3줄 비유 설명
1. 친구들과 게임 규칙을 정할 때 “언제 이기고 언제 지는지”를 먼저 같이 말해 보는 게 BDD예요.
2. 모두가 같은 말로 규칙을 적어 두면 중간에 싸울 일이 줄어요.
3. 나중에 게임을 다시 해도 그 종이를 보면 똑같이 놀 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 490 / 530

<- **이전**: [411. 테스트 주도 개발 (Test-Driven Development)](/studynote/11_design_supervision/06_exam_summary/411_process/)
**다음**: [413. 서드파티 종속과 벤더 락인 통제 (Vendor Lock-in Control)](/studynote/11_design_supervision/06_exam_summary/413_management/) ->

---
