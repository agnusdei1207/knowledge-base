+++
title = "125. Error Budget (에러 예산) - 신뢰성과 혁신 속도의 균형 도구"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Error Budget은 <strong>SLO에서 파생되는 허용 가능 장애 시간/비율</strong>이며, "100% - [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/)"로 계산한다. [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/)=99.9%이면 [Error Budget](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/)=0.1%=**30일 기준 약 43분**.
> 2. **가치**: Error Budget은 <strong>"얼마나 더 위험을 감수(배포·실험)해도 되는가"의 정량적 기준</strong>이다. Budget이 남아있으면 공격적 배포, 소진되면 안정화에 집중하여 <strong>속도와 안정의 갈등을 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>로 해결</strong>한다.
> 3. **판단 포인트**: Burn Rate(소진 속도) 알림을 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하여 Budget이 빠르게 소진될 때 조기 경고하고, Budget 소진 시 **Release Freeze(배포 동결)** [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 실행한다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Error Budget 계산 및 의사결정</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SLO = 99.9% (30일 기준)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Error Budget = 0.1% = 43.2분</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">이번 달 장애 10분 발생</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">남은 Budget = 33.2분 → 배포 계속 OK ✅</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">이번 달 장애 50분 발생</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">남은 Budget = -6.8분 → Budget 소진!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ Release Freeze! 안정화 집중 🚨</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: Error Budget은 <strong>매월 주어지는 용돈(43분)</strong>이다. 장애가 나면 용돈이 줄고, 다 쓰면 <strong>새 장난감(<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a>) 구매 금지(Release Freeze)</strong>.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Burn Rate Alert

| 소진 속도 | 상황 | 알림 |
|:---|:---|:---|
| **1× (정상)** | 30일에 Budget 소진 | 안전 |
| **2×** | **15일에 소진 예상** | ⚠️ 주의 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a>×</strong> | **3일에 소진 예상** | 🚨 긴급 |
| **14.4×** | **1시간에 1% 소진** | 즉시 대응 |

- **📢 섹션 요약 비유**: Burn Rate는 용돈 소비 속도이다. 하루에 10만원씩 쓰면 월급 전에 바닥나므로 경고(Alert)가 필요하다.

---

## Ⅲ. 비교 및 연결

| 비교 | Budget 없음 | Budget 있음 |
|:---|:---|:---|
| **배포** | 공포 (변경 회피) | **Budget 내 자유** |
| **안정화** | 장애 후 사후 | **Budget 소진 시 즉시** |
| **판단** | 주관적 | <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 기반</strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Error Budget](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)

| Budget 잔량 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
|:---|:---|
| **> 50%** | 공격적 배포·실험 허용 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a>~50%</strong> | [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)로 신중하게 |
| **< [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%** | [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 동결, 안정화 집중 |
| **소진** | **Release Freeze** |

---

## Ⅴ. 기대효과 및 결론

Error Budget은 <strong>SRE의 가장 혁신적 도구</strong>이며, 개발팀(속도)과 운영팀(안정)의 갈등을 <strong>수치로 해결</strong>하는 공통 언어이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/">Error Budget</a></strong> | 100% - [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) (허용 장애 시간) |
| **Burn Rate** | Budget 소진 속도 |
| **Release Freeze** | Budget 소진 시 배포 동결 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/">SLO</a></strong> | Error Budget의 원천 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/">Toil</a></strong> | Budget 소진 시 자동화 투자 대상 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">100% 가용성 목표 (전통, 비현실적)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Error Budget 개념 (Google SRE, 2003~)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">SRE Book 공개 (2016) — Error Budget 대중화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Burn Rate Alert (2020~) — 소진 속도 알림</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: AI Error Budget — 자동 Budget 추천·정책 실행</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. Error Budget은 <strong>매달 받는 용돈(43분)</strong>이에요. 장애가 나면 용돈이 줄어요.
2. 용돈이 다 떨어지면 <strong>새 장난감(<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a>) 금지! 저축(안정화)</strong>에 집중해야 해요.
3. 용돈이 빨리 줄면 <strong>"조심해!"라는 알림(Burn Rate Alert)</strong>이 울려요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 125 / 373

← **이전**: [124. SLA (Service Level Agreement) - 서비스 수준 계약·위반 시 책임](/knowledge-base/studynote/15_devops_sre/03_sre_observability/124_sla_service_level_agreement/)
**다음**: [126. Toil (수동 운영 작업) - SRE의 자동화 대상 반복 작업](/knowledge-base/studynote/15_devops_sre/03_sre_observability/126_toil_sre/) →

---
