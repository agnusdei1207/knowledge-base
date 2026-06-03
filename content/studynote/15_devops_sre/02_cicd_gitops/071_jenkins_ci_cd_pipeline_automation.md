+++
title = "71. 젠킨스 (Jenkins) - 오픈소스 CI/CD 자동화 빌드 서버"
date = 2026-04-10

[taxonomies]
tags = ["studynote-devops"]

[extra]
tags = ["studynote-devops"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Jenkins는 플러그인 기반의 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 자동화 서버다.
> 2. **가치**: 빌드, 테스트, 배포를 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인으로 자동화한다.
> 3. **판단**: [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Code와 에이전트 구성, 플러그인 관리가 중요하다.

---

## Ⅰ. 개요 및 필요성

반복 빌드와 배포를 수동으로 하면 느리고 실수도 많다.

Jenkins는 그 반복을 자동화한다.

- **📢 섹션 요약 비유**: 일을 대신 해 주는 자동화 공장이다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Source</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Jenkins Pipeline</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Build / Test / Deploy</div>
</div>
</div>



| 요소 | 의미 |
| :-- | :-- |
| Job | 작업 |
| [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) | 단계 흐름 |
| Agent | 실행 노드 |

Jenkins는 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 정의해 자동화하고, 에이전트로 작업을 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)한다.

- **📢 섹션 요약 비유**: 공정이 순서대로 움직이는 자동 조립 라인이다.

---

## Ⅲ. 비교 및 연결

| 구분 | Jenkins | 단순 스크립트 |
| :-- | :-- | :-- |
| 자동화 | 높음 | 낮음 |
| 확장성 | 높음 | 낮음 |
| 관리 | 플러그인 | 수동 |

| 개념 | 의미 |
| :-- | :-- |
| [Pipeline as Code](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/072_declarative_pipeline_jenkinsfile_as_code/) | 코드로 정의 |
| Plugin | 기능 확장 |

Jenkins는 유연하지만 플러그인 관리가 중요하다. 그래서 운영 표준이 필요하다.

- **📢 섹션 요약 비유**: 자동화 공장에 부품을 잘 꽂아야 멈추지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) Code를 쓰는가?
2. 에이전트를 적절히 분리하는가?
3. 플러그인을 관리하는가?
4. 빌드/테스트/배포를 자동화하는가?
5. 보안과 자격 증명을 관리하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 수동 Job만 잔뜩 쌓는 설계
- 플러그인 업데이트를 방치하는 설계
- 자격 증명을 노출하는 설계
- [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 코드화 없이 운영하는 설계

기술사 관점에서는 Jenkins를 "[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 자동화 서버"로 설명해야 한다.

- **📢 섹션 요약 비유**: 반복 작업을 대신하는 똑똑한 기계다.

---

## Ⅴ. 기대효과 및 결론

Jenkins는 배포 자동화와 품질 확보를 돕는다.

결론적으로 Jenkins는 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 자동화 서버다.

- **📢 섹션 요약 비유**: 코드가 바뀌면 알아서 공정이 돌아간다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Source</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Jenkins</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Pipeline</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Deploy</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">CI/CD</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Jenkins</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Pipeline as Code</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Automation</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

반복 일을 대신해 줘요.  
단계별로 알아서 움직여요.  
젠킨스는 그런 자동화 도구예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 71 / 373

← **이전**: [70. 빌드 도구 (Build Tools) - Maven, Gradle (Java), npm (Node.js)](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/070_build_tools_maven_gradle_npm/)
**다음**: [72. 선언적 파이프라인 - Jenkinsfile (Pipeline as Code)](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/072_declarative_pipeline_jenkinsfile_as_code/) →

---
