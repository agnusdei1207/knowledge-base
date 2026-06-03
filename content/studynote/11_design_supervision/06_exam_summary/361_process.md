+++
title = "361. 중복 배제 원칙 (Don't Repeat Yourself, DRY)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 중복 배제 원칙 (Don't Repeat Yourself, DRY)은 지식과 규칙을 한 곳에 모아 중복 구현을 줄이는 설계 원칙이다.
> 2. **가치**: [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 일관성과 수정 추적성을 높여 준다.
> 3. **판단 포인트**: DRY는 코드 줄 수 절감보다 “같은 의미의 중복”을 제거하는 원칙이라는 점을 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

중복 배제 원칙 (Don't Repeat Yourself, DRY)은 지식과 규칙을 한 곳에 모아 중복 구현을 줄이는 설계 원칙이다. 복사-붙여넣기 코드가 늘어나면 동일 규칙을 여러 곳에서 따로 수정해야 하는 유지보수 비용이 커진다. 이 개념이 필요한 이유는 같은 지식을 한 번만 표현하는 일을 시스템 수준의 규칙으로 끌어올리기 위해서다. 반대로 이를 무시하면 같아 보여야 할 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 위치마다 다르게 수정되어 버그와 불일치를 만든다.

아래 그림은 왜 이 주제가 “문제 인식 → 설계 규칙 → 안정화 결과”의 흐름으로 이해되어야 하는지를 압축한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Change</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">DRY</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">Stable</div></div>
</div>
</div>



이 흐름의 핵심은 기능 하나를 설명하는 것이 아니라, 어떤 압력이 들어와도 구조가 흔들리지 않게 만드는 기준을 세우는 데 있다.

- **📢 섹션 요약 비유**: 서랍을 용도별로 나누지 않으면 필요한 물건을 찾을 때마다 전체를 뒤집어야 하는 상황과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

중복 배제 원칙 (Don't Repeat Yourself, DRY)의 핵심 원리는 "같은 지식을 한 번만 표현하는 일"을 구현 규칙으로 고정하는 데 있다. 실제 설계에서는 공통 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함수, [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 템플릿, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)으로 추출해 변경 지점을 단일화한다. 동시에 표면적 중복만 보고 성급히 통합하면 서로 다른 변화 축까지 결합시켜 오히려 수정이 어려워질 수 있다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 문제 | 같은 지식을 한 번만 표현하는 일 | 이 축이 흔들리면 설계 목적이 사라진다 |
| 구현 방식 | 공통 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함수, [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 템플릿, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)으로 추출해 변경 지점을 단일화한다 | 코드·계층·배포 단위에 일관되게 반영해야 한다 |
| 트레이드오프 | 표면적 중복만 보고 성급히 통합하면 서로 다른 변화 축까지 결합시켜 오히려 수정이 어려워질 수 있다 | 복잡도와 운영 비용을 함께 관리해야 한다 |

다음 그림은 입력, 경계, 핵심 규칙, 결과가 어디서 갈리는지 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Reason</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">Boundary</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">DRY</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">Test</div></div>
</div>
</div>



이때 중요한 것은 도구 이름보다 경계와 책임의 방향이다. 동일한 기술을 써도 이 방향이 다르면 [유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/), 테스트성, 운영 난도가 크게 달라진다.

- **📢 섹션 요약 비유**: 톱니가 맞게 설계된 기어처럼, 책임과 의존이 맞물려야 힘이 새지 않는다.

---

## Ⅲ. 비교 및 연결

기술사 답안에서는 중복 배제 원칙 (Don't Repeat Yourself, DRY)을 단독 정의보다 대안 구조와 함께 써야 경계가 살아난다. 여기서는 **원칙 준수 구조** 와 **원칙 무시 구조** 를 대비해 핵심 차이를 정리한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 변경 대응 | 원칙 준수 구조는 같은 지식을 한 번만 표현하는 일에 맞춰 영향 범위를 줄인다 | 원칙 무시 구조는 변경이 주변 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)로 번지기 쉽다 |
| 구조 안정성 | 원칙 준수 구조는 공통 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함수, [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 템플릿, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)으로 추출해 변경 지점을 단일화한다 | 원칙 무시 구조는 책임과 의존이 섞여 규칙이 흐려진다 |
| 운영 결과 | 원칙 준수 구조는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 일관성과 수정 추적성을 높여 준다 | 원칙 무시 구조는 같아 보여야 할 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 위치마다 다르게 수정되어 버그와 불일치를 만든다 |

연결 개념으로는 리팩터링, [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/) 같은 주변 주제를 함께 써 주면, 단순 암기보다 적용 맥락이 살아난다.

- **📢 섹션 요약 비유**: 전용 공구와 만능 공구를 비교해 보는 순간 어떤 문제가 줄어드는지가 선명해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 중복 배제 원칙 (Don't Repeat Yourself, DRY)을 무조건 채택하기보다 DRY는 코드 줄 수 절감보다 “같은 의미의 중복”을 제거하는 원칙이라는 점을 구분해야 한다. 아래 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)는 설계 감리 시 최소한으로 확인해야 할 질문이다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 변경 이유를 한 문장으로 설명할 수 있는가?
2. 공개 인터페이스가 실제 책임보다 넓지 않은가?
3. 숨은 결합 없이 단위 테스트가 가능한가?
4. [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 추가 비용이 얻는 안정성보다 크지 않은가?

답안을 마무리할 때는 “어디에 쓰는가”만이 아니라 “언제 과한가”를 함께 적어야 한다. 그래야 설계 원칙, 패턴, 아키텍처가 구호가 아니라 의사결정 기준으로 읽힌다.

- **📢 섹션 요약 비유**: 출항 전 점검표처럼, 적용 조건을 확인해야 원칙이 장식이 아니라 안전장치가 된다.

---

## Ⅴ. 기대효과 및 결론

중복 배제 원칙 (Don't Repeat Yourself, DRY)의 기대효과는 분명하다. [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 일관성과 수정 추적성을 높여 준다. 다만 표면적 중복만 보고 성급히 통합하면 서로 다른 변화 축까지 결합시켜 오히려 수정이 어려워질 수 있다. 결국 기억할 관점은 같은 지식을 한 번만 표현하는 일을 구조 규칙으로 만드는 데 있다는 점이다.

- **📢 섹션 요약 비유**: 반복해서 꺼내 보는 사용 설명서처럼, 오래 갈 설계일수록 핵심 규칙이 짧고 분명해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 리팩터링 | 중복 배제 원칙 (Don't Repeat Yourself, DRY)을 설계하고 감리할 때 함께 보는 연관 개념 |
| [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/) | 중복 배제 원칙 (Don't Repeat Yourself, DRY)을 설계하고 감리할 때 함께 보는 연관 개념 |
| [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 중앙화 | 중복 배제 원칙 (Don't Repeat Yourself, DRY)을 설계하고 감리할 때 함께 보는 연관 개념 |
| [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/) | 중복 배제 원칙 (Don't Repeat Yourself, DRY)을 설계하고 감리할 때 함께 보는 연관 개념 |

### 📈 관련 키워드 및 발전 흐름도
[복사-붙여넣기 구현] → [DRY 적용] → [정책 중앙화]

### 👶 어린이를 위한 3줄 비유 설명
1. 중복 배제 원칙 (Don't Repeat Yourself, DRY)은 같은 숙제 답을 여러 공책에 쓰지 않고 한 장에 정리하는 것처럼 약속을 먼저 정하는 거예요.
2. 그러면 서로 다른 사람이 해도 같은 규칙으로 움직일 수 있어요.
3. 그래서 규모가 커질수록 같은 지식을 한 번만 표현하는 일이 더 중요해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 439 / 530

← **이전**: [360. 데메테르 법칙 (Law of Demeter, LoD)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/360_process/)
**다음**: [362. 지금 필요하지 않은 기능 배제 (You Aren't Gonna Need It, YAGNI)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/362_yagni/) →

---
