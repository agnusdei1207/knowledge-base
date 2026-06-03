+++
title = "기술 부채 (Technical Debt)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

> **핵심 인사이트 3줄**
> 1. [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)([Technical Debt](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/))는 Ward Cunningham(1992)이 제안한 개념으로, 더 나은 설계 대신 빠른 구현을 선택할 때 발생하는 미래 추가 비용의 은유다.
> 2. [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)는 의도적·비의도적으로 발생하며, 방치하면 이자(유지보수 비용 증가)가 쌓여 최초 부채보다 큰 비용이 된다.
> 3. 측정(코드 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·SQALE 모델)→[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)(4분면)→[리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 로드맵→지속적 [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) 모니터링이 현대적 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 관리의 표준 사이클이다.

---

## Ⅰ. [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)의 정의와 은유

[기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)([Technical Debt](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/))는 <strong>소프트웨어 개발에서 단기 이익을 위해 선택한 차선책이 장기적으로 추가 비용을 유발하는 현상</strong>이다.

```
기술 부채 = (최적 설계 비용) - (실제 구현 비용)
이자      = 부채를 갚지 않아 증가하는 유지보수 비용
```

### Cunningham의 원래 은유

> "작동하는 코드지만 이상적 설계가 아닌 것은 금융 부채와 같다. [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)을 통해 갚지 않으면 이자가 쌓인다."

### [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 4분면 (Fowler)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">의도적 비의도적</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">무모한</div><div class="kb-diagram-cell">무모-의도: 출시</div><div class="kb-diagram-cell">무모-비의도: 레이어</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">압박으로 설계</div><div class="kb-diagram-cell">가 뭔지 몰랐어</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">포기 ("나중에")</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">신중한</div><div class="kb-diagram-cell">신중-의도: 배포</div><div class="kb-diagram-cell">신중-비의도: "이제는</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">먼저, 결과 처리</div><div class="kb-diagram-cell">어떻게 해야 했는지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">는 나중에</div><div class="kb-diagram-cell">알겠다"</div></div>
</div>
</div>



📢 **섹션 요약 비유**: [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)는 신용카드다 — 지금 당장 사고 나중에 갚지만, 방치하면 이자가 쌓여 원금보다 이자가 더 커진다.

---

## Ⅱ. [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 유형 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)

| 유형            | 발생 원인                    | 예시                         |
|---------------|-----------------------------|-----------------------------|
| 코드 부채       | 중복 코드, 긴 메서드          | Copy-paste 프로그래밍         |
| [설계 부채](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/140_design_debt/)       | 잘못된 아키텍처·패턴          | 모놀리식 → [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 전환 미완료    |
| 테스트 부채     | 테스트 커버리지 부족           | [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 미만          |
| 문서 부채       | 코드·[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 문서 미작성          | 레거시 코드 설명 없음          |
| 의존성 부채    | 구버전 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 방치         | Spring Boot 1.x 미업그레이드  |
| 인프라 부채    | 자동화 미흡·수동 배포          | 수동 [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 배포                 |

📢 **섹션 요약 비유**: [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 유형은 집 수리 목록이다 — 누수(코드), 잘못된 설계도(설계), 화재경보기 없음(테스트), 사용설명서 없음(문서)이 모두 부채다.

---

## Ⅲ. [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 측정 — SQALE / [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/)

### SQALE ([Software Quality](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/) Assessment based on Lifecycle Expectations)

SQALE은 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)를 <strong>수정 시간(분·시간)</strong>으로 정량화한다.

```
기술 부채 = Σ (각 위반 수정 비용)

SQALE 지수 = 기술 부채 / 이상적 개발 시간
  < 5%: A등급 (우수)
  5-10%: B등급
  10-20%: C등급
  > 50%: E등급 (위험)
```

### [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SonarQube 대시보드:</div>
<div class="kb-diagram-tree-item" style="--depth:0">Bugs: 0 (결함)</div>
<div class="kb-diagram-tree-item" style="--depth:0">Vulnerabilities: 2 (보안 취약점)</div>
<div class="kb-diagram-tree-item" style="--depth:0">Code Smells: 128 (코드 악취)</div>
<div class="kb-diagram-tree-item" style="--depth:0">Technical Debt: 3d 2h (수정 소요 시간)</div>
<div class="kb-diagram-tree-item" style="--depth:0">Coverage: 72.3% (테스트 커버리지)</div>
<div class="kb-diagram-tree-item" style="--depth:0">Duplications: 8.1% (코드 중복)</div>
</div>
</div>



📢 **섹션 요약 비유**: [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) 대시보드는 자동차 계기판이다 — 연료(커버리지), 엔진 경고등(버그), 배기가스(중복 코드)를 한눈에 보여준다.

---

## Ⅳ. [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 관리 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

### 부채 관리 사이클



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">측정 → 분류 → 우선순위화 → 리팩토링 → 재측정</div>
<div class="kb-diagram-note">지속적 모니터링</div>
</div>
</div>



### 보이 스카우트 규칙 (Boy Scout Rule)

> "캠프장을 떠날 때는 도착했을 때보다 깨끗이 남겨라"
> → 코드를 수정할 때마다 주변 코드를 조금씩 개선

### [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) vs 재구축

| 상황                    | 권장 접근         |
|----------------------|-----------------|
| 부채 < 20%, 기능 변경 시 | 점진적 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)   |
| 부채 20-50%           | 아키텍처 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) |
| 부채 > 50%, 사업 가치 높음 | 재구축(Rearchitect) |
| 부채 > 50%, 사업 가치 낮음 | 은퇴(Retire)    |

📢 **섹션 요약 비유**: 보이 스카우트 규칙은 식사 후 설거지다 — 매번 완벽히 청소하기 어렵지만, 조금씩 쌓이지 않도록 지속적으로 관리한다.

---

## Ⅴ. 현대적 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 예방

### [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)/[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)·CD 파이프라인 통합



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">코드 커밋 → SonarQube SAST → 기술 부채 증가 감지 → PR 차단</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">SQALE 지수 임계값 초과 시 빌드 실패</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">자동 리팩토링 제안 (AI 코드 리뷰)</div>
</div>
</div>



### 아키텍처 결정 기록 ([ADR](/knowledge-base/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/))

- <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/">ADR</a>(<a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/231_adr_architecture_decision_record_documentation/">Architecture Decision Record</a>)</strong>: 의도적 부채 발생 시 이유·예상 비용·상환 계획 문서화
- [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)를 투명하게 관리해 나중에 "왜 이렇게 짰지?" 방지

📢 **섹션 요약 비유**: ADR은 차용증이다 — 돈을 빌릴 때(부채 발생) 이유와 상환 계획을 적어두면 나중에 갚기도 쉽고, 빌린 사실 자체를 잊지 않는다.

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">기술 부채 (Technical Debt)</div>
<div class="kb-diagram-tree-item" style="--depth:0">분류 (Fowler 4분면)</div>
<div class="kb-diagram-note">── 의도적·무모</div>
<div class="kb-diagram-note">── 의도적·신중</div>
<div class="kb-diagram-note">── 비의도적·무모</div>
<div class="kb-diagram-note">── 비의도적·신중</div>
<div class="kb-diagram-tree-item" style="--depth:0">측정 도구</div>
<div class="kb-diagram-note">── SonarQube (코드 메트릭)</div>
<div class="kb-diagram-note">── SQALE 모델 (수리 시간 기반)</div>
<div class="kb-diagram-note">── CodeClimate</div>
<div class="kb-diagram-tree-item" style="--depth:0">관리 전략</div>
<div class="kb-diagram-note">── 보이 스카우트 규칙</div>
<div class="kb-diagram-note">── 리팩토링 로드맵</div>
<div class="kb-diagram-note">── ADR (Architecture Decision Record)</div>
<div class="kb-diagram-tree-item" style="--depth:0">관련 개념</div>
<div class="kb-diagram-tree-item" style="--depth:2">코드 악취 (Code Smell)</div>
<div class="kb-diagram-tree-item" style="--depth:2">소프트웨어 엔트로피</div>
<div class="kb-diagram-tree-item" style="--depth:2">지속적 리팩토링</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">기술 부채 개념 발전 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1992년</div><div class="kb-diagram-cell">Cunningham 제안</div><div class="kb-diagram-cell">금융 부채 은유 최초 도입</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1999년</div><div class="kb-diagram-cell">Fowler 코드 악취</div><div class="kb-diagram-cell">리팩토링 기법 체계화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2009년</div><div class="kb-diagram-cell">SQALE 모델 제안</div><div class="kb-diagram-cell">기술 부채 정량화 방법론</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2013년</div><div class="kb-diagram-cell">SonarQube 보급</div><div class="kb-diagram-cell">CI/CD 통합 자동 측정</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2018년</div><div class="kb-diagram-cell">ADR 실천 확산</div><div class="kb-diagram-cell">의도적 부채 투명 관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2020년대</div><div class="kb-diagram-cell">AI 코드 리뷰</div><div class="kb-diagram-cell">GitHub Copilot 등 자동 탐지</div></div>
<div class="kb-diagram-note">핵심 키워드 연결:</div>
<div class="kb-diagram-note">기술 부채 → 측정(SQALE) → 분류(4분면) → 리팩토링 → SonarQube</div>
<div class="kb-diagram-note">빠른 구현 수리 시간 의도적/비의도 코드 개선</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">소프트웨어 노후화 → 레거시 마이그레이션 (5R 전략)</div>
</div>
</div>



---

## 👶 어린이를 위한 3줄 비유 설명

1. [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)는 숙제 미루기다 — 오늘 안 하면 내일 두 배, 계속 미루면 끝내기 불가능한 산이 된다.
2. 보이 스카우트 규칙은 지나갈 때마다 쓰레기 하나씩 줍기다 — 큰 청소 한 번보다 매번 조금씩이 더 깨끗한 길을 만든다.
3. SonarQube는 숙제 검사 로봇이다 — 제출 전에 틀린 문제(버그), 지저분한 글씨(코드 악취), 베낀 답안(중복 코드)을 자동으로 잡아낸다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 33 / 973

← **이전**: [소프트웨어 노후화 (Software Obsolescence)](/knowledge-base/studynote/04_software_engineering/01_overview_principles/032_software_obsolescence/)
**다음**: [레거시 시스템 현대화 (Legacy System Modernization)](/knowledge-base/studynote/04_software_engineering/01_overview_principles/034_legacy_system_modernization/) →

---
