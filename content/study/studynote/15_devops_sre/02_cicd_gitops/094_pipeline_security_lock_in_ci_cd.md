---
title: 94. 파이프라인 보안 락인 (Pipeline Security)
date: '2026-03-04'
tags:
- cicd
- devsecops
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[123_pipe|파이프]]라인 보안 락인 ([[082_pipeline|Pipeline]] [[283_security_tactics|Security]] [[362_lock_in_portability|Lock-in]])은 코드 커밋부터 배포까지 이어지는 [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 자체를 노리는 [[764_supply_chain_attack|공급망 공격]]을 원천 차단하는 체계적인 보안 통제 장치다.
> 2. **가치**: 런타임 환경에 도달하기 전([[242_shift_left_sdlc|Shift-Left]]) 빌드 단계에서 악성 코드 주입이나 변조를 막아내어, 배포되는 소프트웨어 자산([[075_artifact_management_nexus_docker_registry|Artifact]])의 [[003_integrity|무결성]]을 [[652_cryptography_concept_encryption_decryption|암호학]]적으로 보장한다.
> 3. **판단 포인트**: 단순히 취약점 스캐너만 얹는 것이 아니라, 일회성 빌드 노드 사용, 이미지 서명, 그리고 최소 권한 부여를 결합한 '[[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]])' 아키텍처가 [[123_pipe|파이프]]라인 내부에 내재화되어야 한다.

---

## Ⅰ. 개요 및 필요성

[[123_pipe|파이프]]라인 보안은 소프트웨어를 빌드하고 배포하는 [[090_configuration_item|CI]]/CD ([[019_continuous_integration|Continuous Integration]] / [[165_continuous_deployment|Continuous Deployment]]) [[123_pipe|파이프]]라인 인프라 자체를 방어하는 활동이다. 개발자가 작성한 소스코드는 [[090_configuration_item|CI]]/CD를 거쳐 최종 서버에 도달하는데, [[123_pipe|파이프]]라인 보안 락인은 이 컨베이어 벨트에 악성 코드가 섞이지 않도록 각 단계마다 [[395_verification_process_review|검증]] 게이트를 잠그는([[362_lock_in_portability|Lock-in]]) 개념이다.

전통적인 보안은 이미 서버에 배포된 애플리케이션을 방어하는 데 집중했다. 그러나 해커들은 방어가 탄탄한 런타임 서버 대신, 소프트웨어 조립 공장인 [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인을 탈취하여 정상 업데이트 패치에 악성 코드를 심는 [[764_supply_chain_attack|공급망 공격]]([[764_supply_chain_attack|Supply Chain Attack]], 예: 솔라윈즈 사태)으로 타겟을 바꿨다. [[123_pipe|파이프]]라인 자체가 오염되면 수많은 고객사에 악성 코드가 정상 프로그램으로 둔갑하여 배포되므로, [[123_pipe|파이프]]라인의 [[003_integrity|무결성]]을 증명하는 락인 체계가 필수가 되었다.

- **📢 섹션 요약 비유**: 은행 금고(서버)를 뚫기 어렵자, 도둑들이 현금 수송 차량([[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인)을 털기 시작했습니다. [[123_pipe|파이프]]라인 보안 락인은 이 현금 수송 차량에 방탄 유리를 달고 무장 경비원을 배치하는 공정 [[571_protection_vs_security|보호]] 작업입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[123_pipe|파이프]]라인 [[302_security_architecture_design|보안 아키텍처]]는 코드 커밋, 빌드, [[075_artifact_management_nexus_docker_registry|아티팩트]] [[087_process_state_transition|생성]], 배포 승인의 4단계로 구성되며, 각 구간마다 신뢰를 [[395_verification_process_review|검증]]하는 락([[510_lock|Lock]])이 걸린다.

| 보안 통제 단계 | 적용 기술 / 원리 | 방어 목적 |
| :--- | :--- | :--- |
| 1. 소스코드 [[571_protection_vs_security|보호]] | 브랜치 [[571_protection_vs_security|보호]] (Branch [[571_protection_vs_security|Protection]]), 다중 리뷰어 강제 | 악의적 직접 푸시 방지 |
| 2. 빌드 환경 격리 | 일회성 러너 (Ephemeral Runner) 노드 사용 | 이전 빌드의 캐시 포이즈닝 악성 스크립트 잔류 차단 |
| 3. 내재화된 스캔 | [[491_sast_static_analysis|SAST]] / [[453_sca|SCA]] 자동 검사 및 Hard Gate 적용 | 취약점 [[431_ssthresh_slow_start_threshold|임계치]] 초과 시 [[123_pipe|파이프]]라인 즉각 중단(Break) |
| 4. 이미지 서명 및 [[395_verification_process_review|검증]] | Cosign 등으로 [[561_container_based_deployment|컨테이너]] 이미지에 [[652_cryptography_concept_encryption_decryption|암호학]]적 서명 추가 | 변조된 이미지가 운영 환경(K8s)에 배포되는 것 차단 |

```text
┌──────────────────────────────────────────────────────────────┐
│             Secure CI/CD Pipeline Lock-in Flow             │
├──────────────────────────────────────────────────────────────┤
│ [개발자] ─▶ (Git Commit) ─▶ [ 저장소 (Branch Protection) ] │
│                                          │                   │
│ ┌────────────────────────────────────────▼─────────────────┐ │
│ │                  CI Build Pipeline                       │ │
│ │  (1) 일회성 노드 (Ephemeral Node) 할당                   │ │
│ │  (2) 코드 취약점 자동 검사 (SAST/SCA Scan)               │ │
│ │  (3) 이미지 빌드 및 서명 생성 (Image Signing)            │ │
│ └────────────────────────────────────────┬─────────────────┘ │
│                                          │ 락인 통과 및 서명 │
│ ┌────────────────────────────────────────▼─────────────────┐ │
│ │               CD Deployment & Runtime                    │ │
│ │  [ Artifact Registry ] ──▶ [ K8s Admission Controller ]  │ │
│ │                               (서명 검증 후 배포 허가)   │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

가장 핵심적인 원리는 한 번 빌드된 이미지는 변경할 수 없다는 '불변성(Immutability)'과, 암호화 키를 통한 '증명(Attestation)'이다. K8s 클러스터 앞단에 있는 Admission Controller는 [[123_pipe|파이프]]라인이 정상적으로 찍어준 '서명 도장'이 없는 [[561_container_based_deployment|컨테이너]]의 실행을 가차 없이 거부한다.

- **📢 섹션 요약 비유**: 장난감 공장의 컨베이어 벨트를 매일 새것으로 교체(일회성 러너)하고, 엑스레이 검사(보안 스캔)를 통과한 장난감에만 품질 보증 마크(이미지 서명)를 찍어줍니다. 마크가 없는 장난감은 상점에 진열될 수 없습니다.

---

## Ⅲ. 비교 및 연결

[[123_pipe|파이프]]라인 보안을 이해하기 위해 기존 런타임 중심 방어(운영 보안)와 [[242_shift_left_sdlc|Shift-Left]] 기반의 [[123_pipe|파이프]]라인 방어(빌드 보안)의 접근법 차이를 비교해야 한다.

| 비교 항목 | 기존 런타임 중심 보안 | [[123_pipe|파이프]]라인 보안 락인 ([[242_shift_left_sdlc|Shift-Left]]) |
| :--- | :--- | :--- |
| 방어 시점 | 애플리케이션 배포 완료 후 운영 중 | 소스코드 작성 및 빌드 단계 |
| 주요 타겟 방어 | 침입 시도 차단, 비정상 행위 탐지 | 악성 코드 주입, 빌드 환경 변조 차단 |
| 핵심 도구 | [[696_waf_web_application_firewall|WAF]], [[601_ids_ips_syscall_tracing|IDS]]/[[695_ips_network_intrusion_prevention_system|IPS]], [[325_edr|EDR]] | [[491_sast_static_analysis|SAST]]/[[453_sca|SCA]], Cosign (서명), Branch Rule |
| [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 조치 비용 | 매우 높음 (장애 발생, 해킹 후 수습) | 매우 낮음 (빌드 실패 처리로 배포 전 예방) |
| [[177_secrets_management_vault_kubernetes|시크릿 관리]] 방식 | 코드 내 하드코딩 사후 적발 | [[123_pipe|파이프]]라인 변수로 [[095_secret_manager_hashicorp_vault_aws|Secret Manager]] 연동 주입 |

[[123_pipe|파이프]]라인 락인은 보안의 무게 중심을 '오른쪽(운영)'에서 '왼쪽(개발/빌드)'으로 앞당겨, 보안 부채가 누적되어 런타임에서 터지기 전에 미리 막아내는 [[653_devsecops_shift_left|DevSecOps]] 패러다임의 핵심 실천 방안이다.

- **📢 섹션 요약 비유**: 기존 보안이 병에 걸린 뒤 응급실(런타임)에서 수술하는 것이라면, [[123_pipe|파이프]]라인 보안은 공장에 들어갈 때마다 손을 씻고 무균실(빌드 환경)에서 작업하도록 강제하는 예방 접종입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 완벽한 [[123_pipe|파이프]]라인 보안을 구축하려면 툴(Tool) 도입을 넘어 [[164_policy|정책]]([[164_policy|Policy]])의 강제성이 수반되어야 한다.

### [[435_checklist_based_testing|체크리스트]]
1. **[[690_sbom_software_supply_chain_security|소프트웨어 자재 명세서]] ([[890_sbom_cyclonedx_spdx|SBOM]])**: [[123_pipe|파이프]]라인 내에서 [[385_third_party_cookie_deprecation_cdw|서드파티]] [[191_oss_license_compliance|오픈소스]] [[336_library_vs_framework|라이브러리]]의 [[288_version_ihl_tos_total_length|버전]]과 의존성 목록을 SBOM으로 추출하여 추적 가능한 가시성을 확보했는가?
2. **최소 권한의 원칙 (PoLP)**: [[090_configuration_item|CI]]/CD [[275_iam_role_for_service_accounts|서비스 계정]]([[526_iam|IAM]] Role)에 'AdministratorAccess' 같은 과도한 권한이 부여되지 않고, 딱 필요한 배포 권한만 부여되도록 격리했는가?
3. **Hard Gate 적용**: 보안 스캐너가 Critical 등급의 취약점을 발견했을 때 경고(Warn)에서 그치지 않고, [[123_pipe|파이프]]라인을 즉시 중단(Break)시켜 프로덕션 배포를 원천 차단하는 [[164_policy|정책]]이 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 [[009_config|설정]] [[501_file_definition_logical_record|파일]](`.gitlab-ci.yml`, `Jenkinsfile` 등)을 누구나 수정할 수 있게 방치하는 구성
- 고정된 하나의 빌드 서버([[598_vm_migration_nic|VM]])를 씻어내지 않고 수개월간 반복 사용하여 임시 [[501_file_definition_logical_record|파일]]과 악성 스크립트가 누적되도록 두는 방식

- **📢 섹션 요약 비유**: 아무리 좋은 보안 검사 기계가 있어도, 경고음이 울릴 때 기계를 끄고 그냥 제품을 통과시켜버리면(Soft Gate) 소용이 없습니다. 경고가 울리면 컨베이어 벨트 전원이 자동으로 꺼지는 강력한 장금장치(Hard Gate)가 필수입니다.

---

## Ⅴ. 기대효과 및 결론

견고하게 구축된 [[123_pipe|파이프]]라인 보안 락인은 글로벌 [[764_supply_chain_attack|공급망 공격]]으로부터 회사의 비즈니스 [[085_confidence_association_rule_conditional_probability|신뢰도]]를 지켜내는 최후의 보루다. 또한 모든 [[395_verification_process_review|검증]]이 자동화되어 [[123_pipe|파이프]]라인 내부에 내재화되므로, 개발 속도 저하 없이도 지속적인 컴플라이언스(보안 규정) 준수가 가능해진다.

앞으로는 SLSA ([[520_supply_chain_attack_and_ci_cd_security|Supply chain]] Levels for Software Artifacts)와 같은 글로벌 [[374_supply_chain_security|공급망 보안]] 프레임워크가 도입되면서, "우리가 만든 소프트웨어 [[075_artifact_management_nexus_docker_registry|아티팩트]]는 어느 수준의 [[123_pipe|파이프]]라인 보안 락인을 거쳤는가"를 정량적으로 입증하는 체계가 클라우드 보안의 가장 중요한 표준으로 자리 잡을 것이다.

- **📢 섹션 요약 비유**: 철통같이 [[571_protection_vs_security|보호]]된 [[123_pipe|파이프]]라인은 신뢰할 수 있는 수원지(소스코드)에서 출발한 맑은 물이, 오염된 배관(해킹)을 거치지 않고 고객의 수도꼭지(배포)까지 깨끗하게 도달하도록 보증하는 정수기 필터 시스템입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[890_sbom_cyclonedx_spdx|SBOM]] ([[890_sbom_cyclonedx_spdx|Software Bill of Materials]]) | 빌드 과정에 포함된 모든 부품의 명세서로, 취약점 추적의 기본 [[001_dikw_pyramid|데이터]] |
| Ephemeral Runner (일회성 러너) | 빌드 노드 오염을 막기 위해 1회 빌드 후 파괴되는 격리된 실행 환경 |
| Image Signing (이미지 서명) | Cosign 등을 이용해 [[075_artifact_management_nexus_docker_registry|아티팩트]]의 [[003_integrity|무결성]]을 [[652_cryptography_concept_encryption_decryption|암호학]]적으로 도장 찍는 기술 |
| [[105_devsecops_shift_left_security|Shift-Left Security]] | 보안 [[395_verification_process_review|검증]] 단계를 소프트웨어 생명 주기 [[459_quic_fec_forward_error_correction|초기]](왼쪽)로 앞당기는 사상 |

### 📈 관련 키워드 및 발전 흐름도

```text
전통적 런타임 보안 방어 (WAF, IDS)
    │
    ▼
Shift-Left 사상 · DevSecOps 태동
    │
    ▼
SAST / SCA 스캔 내재화 · Pipeline Hard Gate 적용
    │
    ▼
일회성 러너 (Ephemeral Node) · SBOM 의무화
    │
    ▼
아티팩트 서명 (Image Signing) · SLSA 레벨 보증 체계
```

이 흐름도는 "사후 탐지 → 사전 예방 → 스캔 자동화 → 환경 격리 → [[652_cryptography_concept_encryption_decryption|암호학]]적 [[003_integrity|무결성]] 증명"으로 [[520_supply_chain_attack_and_ci_cd_security|공급망]] 방어 체계가 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감을 만들 때 나쁜 악당이 몰래 독을 타지 못하게 철통같은 안전 [[123_pipe|파이프]]라인(컨베이어 벨트)을 만들어요.
2. 재료가 들어올 때부터 포장될 때까지 엑스레이 기계가 자동으로 검사하고, 통과 못 하면 기계가 바로 멈춰요.
3. 마지막에 '안전 합격 도장(서명)'이 꽝 찍힌 장난감만 트럭에 실어서 가게로 나갈 수 있는 아주 튼튼한 규칙이랍니다!
