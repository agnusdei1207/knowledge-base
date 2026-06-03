+++
title = "116. 컨테이너 이미지 보안 스캐닝 (Container Image Security Scanning) - CVE·SBOM·정책"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지 보안 스캐닝은 [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)/[OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) 이미지의 <strong>OS 패키지·언어 라이브러리에 포함된 알려진 취약점(<a href="/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/">CVE</a>)</strong>을 자동으로 탐지하고, [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/)(Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여 [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/)을 확보하는 프로세스다.
> 2. **가치**: 프로덕션 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 <strong>76%가 High/Critical <a href="/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/">CVE</a></strong>를 포함하고 있으며(Sysdig 2024 보고서), 빌드 시점(Shift Left)에서 스캔하여 취약 이미지의 배포를 차단해야 한다.
> 3. **판단 포인트**: Trivy([OSS](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), 빠름)·Snyk(개발자 친화)·Grype([SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 통합)가 대표 도구이며, K8s Admission Controller와 연동하여 <strong>스캔 미통과 이미지의 배포를 자동 거부</strong>하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">이미지 보안 스캐닝 파이프라인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 개발자: Dockerfile → docker build</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. CI: Trivy 스캔 → CVE 탐지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">HIGH: 3개, CRITICAL: 1개 → ❌ 빌드 실패</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 수정: base image 업데이트, 라이브러리 패치</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 재스캔 → CVE 0개 → ✅ 레지스트리 Push</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5. K8s: Admission Controller → 스캔 미통과 이미지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">배포 자동 거부</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 이미지 스캐닝은 공항 수하물 X-ray다. 위험물([CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/))이 발견되면 비행기(프로덕션)에 못 태운다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 도구 비교

| 도구 | 유형 | 특징 | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) |
|:---|:---|:---|:---|
| **Trivy** | [OSS](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 빠름, All-in-one | ✅ |
| **Grype** | [OSS](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | Syft [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 연동 | ✅ |
| **Snyk** | [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) | 개발자 IDE 통합 | ✅ |
| <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a> Scout</strong> | [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) | [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 내장 | ✅ |

### [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))
이미지 내 모든 패키지·버전을 <strong>재료 목록</strong>으로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) → [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 매칭·라이선스 감사에 활용.

- **📢 섹션 요약 비유**: SBOM은 식품 성분표이다. "이 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에 openssl 1.1.1이 들어있다"를 알아야 취약점 알림 시 영향 범위를 즉시 파악한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 스캔 없음 | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 스캔 | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) + Admission |
|:---|:---|:---|:---|
| **배포 차단** | ✗ | 빌드만 | **빌드+배포** |
| **취약 이미지** | 프로덕션 진입 | 빌드 실패 | **완전 차단** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Shift Left [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)
- **IDE**: Snyk 플러그인으로 코딩 시점 [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 감지.
- <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a></strong>: Trivy를 GitHub Actions에 통합, Critical [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 시 빌드 실패.
- <strong><a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/">Registry</a></strong>: Harbor 내장 스캐너로 Push 시 자동 스캔.
- **Runtime**: Falco로 실행 중 이상 행위 탐지.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 스캔 미도입 | 스캔 도입 | 개선 |
|:---|:---|:---|:---|
| 취약 이미지 배포 | 76% | <strong>0% (<a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a> 적용)</strong> | 완전 차단 |
| [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 패치 시간 | 발견 후 수일 | **빌드 시점 즉시** | Shift Left |
| [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 가시성 | 없음 | **전체 재료 목록** | [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/) |

[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지 보안은 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 의무화(미국 행정명령 14028)와 함께 소프트웨어 [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/)의 핵심 요소로 부상하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/">CVE</a></strong> | 알려진 취약점 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) |
| <strong><a href="/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/">SBOM</a></strong> | 이미지 내 패키지 재료 목록 |
| **Trivy** | 대표 [OSS](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 이미지 스캐너 |
| **Admission Controller** | K8s 배포 시점 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용 |
| <strong>소프트웨어 <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/">공급망 보안</a></strong> | 이미지 스캐닝이 속하는 상위 체계 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">수동 취약점 관리 (2010s)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Clair / Anchore (2016~) — 초기 이미지 스캐너</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Trivy / Snyk (2019~) — All-in-one, 개발자 친화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">SBOM 의무화 (2021, 미국 행정명령 14028)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: CI + Registry + Admission 전 구간 스캐닝</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지는 <strong>도시락 상자</strong>예요. 안에 뭐가 들었는지 확인해야 해요.
2. 보안 스캐닝은 도시락을 <strong>X-ray로 검사</strong>해서 상한 음식(취약점)이 있으면 학교에 못 가져가게 해요.
3. SBOM은 <strong>성분표</strong>처럼 "이 도시락에 뭐가 들었는지" 목록을 만들어서 문제가 생기면 빠르게 찾아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 115 / 371

← **이전**: [115. Terraform 인프라 프로비저닝 - IaC 선언적 다중 클라우드 관리](/knowledge-base/studynote/13_cloud_architecture/07_container_k8s/115_terraform_infrastructure_provisioning/)
**다음**: [117. K8s Network Policy 마이크로 세그멘테이션 - Pod 간 트래픽 격리·제로 트러스트](/knowledge-base/studynote/13_cloud_architecture/07_container_k8s/117_kubernetes_network_policy_micro_segmentation/) →

---
