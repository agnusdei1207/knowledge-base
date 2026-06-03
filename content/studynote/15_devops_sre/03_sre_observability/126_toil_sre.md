+++
title = "126. Toil (수동 운영 작업) - SRE의 자동화 대상 반복 작업"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Toil은 <strong>수동적·반복적·자동화 가능·전술적·장기적 가치 없는 운영 작업</strong>이며, [SRE](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 엔지니어의 <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/">Toil</a> 비율을 50% 미만으로 유지</strong>하여 나머지를 엔지니어링(자동화·시스템 개선)에 투자하는 것이 SRE의 핵심 원칙이다.
> 2. **가치**: Toil이 50%를 넘으면 엔지니어가 <strong>소방수(장애 대응)</strong>만 하게 되어 근본 개선이 불가능하고, Toil이 줄면 <strong>시스템 안정성·개발자 생산성·직원 만족도</strong>가 동시에 향상된다.
> 3. **판단 포인트**: Toil은 "힘든 작업"이 아니라 <strong>"자동화 가능한 수동 작업"</strong>이다. [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 분석·아키텍처 설계는 어렵지만 Toil이 아니다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Toil vs 엔지니어링</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Toil — 제거 대상</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">수동 서버 재시작</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">반복 인증서 갱신</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">수동 트래픽 이동</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">반복 에러 확인·리포트</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">엔지니어링 — 투자 대상</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">자동화 스크립트 개발</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">관측성 대시보드 구축</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">셀프힐링 시스템 구축</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">용량 계획 도구 개발</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SRE 원칙: Toil &lt; 50%</div><div class="kb-diagram-cell">엔지니어링 &gt; 50%</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: Toil은 매일 손빨래하는 것이고, 엔지니어링은 세탁기를 만드는 것이다. 세탁기를 만들면 빨래([Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)) 시간이 영구히 사라진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Toil의 5가지 특징

| 특징 | 설명 |
|:---|:---|
| **수동적** | 사람이 직접 수행 |
| **반복적** | 같은 작업을 반복 |
| **자동화 가능** | 기술적으로 자동화 가능 |
| **전술적** | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 가치 없음 |
| **O(n) 성장** | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 성장에 비례해 증가 |

- **📢 섹션 요약 비유**: "[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 2배 커지면 Toil도 2배" → 자동화하지 않으면 팀이 Toil에 묻힌다.

---

## Ⅲ. 비교 및 연결

| 비교 | [Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 방치 | [Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 자동화 |
|:---|:---|:---|
| **엔지니어** | 소방수 | **건축가** |
| **안정성** | 정체 | **지속 개선** |
| **만족도** | 낮음 | **높음** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 측정 방법
1. 팀원의 주간 작업 시간을 [Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)/엔지니어링으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/).
2. [Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 비율 = [Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 시간 / 전체 작업 시간.
3. 50% 초과 시 자동화 프로젝트 우선순위↑.

---

## Ⅴ. 기대효과 및 결론

[Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 관리는 <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/">SRE</a> 팀의 <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/386_sustainability_green_coding/">지속 가능성</a></strong>을 결정하며, "Toil을 줄이는 것이 곧 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 안정성을 높이는 것"이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/">Toil</a></strong> | 자동화 가능한 수동 운영 작업 |
| **50% 규칙** | SRE의 [Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 상한선 |
| **자동화** | [Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 제거의 핵심 수단 |
| **셀프힐링** | [Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 자동화의 고급 형태 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/">SRE</a></strong> | [Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 관리의 조직 프레임워크 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">수동 운영 (전통 Ops, 100% Toil)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스크립트 자동화 (Bash/Python, 2000s)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">SRE Toil 정의 (Google, 2003~2016)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">IaC + CI/CD (자동화 인프라, 2015~)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: AIOps — AI가 Toil을 자동 감지·자동화</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. Toil은 매일 <strong>손빨래</strong>하는 거예요. 힘들고 반복돼요.
2. SRE는 <strong>세탁기(자동화)</strong>를 만들어서 빨래 시간을 없애요.
3. 빨래 시간이 줄면 <strong>새 옷(기능) 만드는 시간</strong>이 생기니까 모두 행복해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 126 / 373

← **이전**: [125. Error Budget (에러 예산) - 신뢰성과 혁신 속도의 균형 도구](/knowledge-base/studynote/15_devops_sre/03_sre_observability/125_error_budget/)
**다음**: [127. 온콜 관리 (On-Call Management) - SRE 장애 대응 당번 체계](/knowledge-base/studynote/15_devops_sre/03_sre_observability/127_on_call_management/) →

---
