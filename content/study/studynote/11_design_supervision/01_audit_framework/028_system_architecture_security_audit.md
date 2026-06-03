+++
weight = 28
title = "28. 시스템 아키텍처 보안 감리 (System Architecture Security Audit)"
date = "2026-04-29"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시스템 아키텍처 보안 감리는 정보시스템 감리의 보안 영역으로, 아키텍처 설계 단계에서 보안 원칙([[012_defense_in_depth|Defense in Depth]], [[010_least_privilege|Least Privilege]], [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 등)이 올바르게 구현됐는지를 독립적으로 [[395_verification_process_review|검증]]하는 활동이다.
> 2. **가치**: 보안 취약점은 운영 단계보다 설계 단계에서 발견할 때 수정 비용이 [[489_raid_10_hybrid|10]]~100배 저렴하다. 아키텍처 감리는 "설계 시 보안([[058_security_by_design|Security by Design]])"을 강제하여 레거시 시스템의 보안 취약점 누적을 예방한다.
> 3. **판단 포인트**: [[531_cloud_native_architecture|클라우드 네이티브]]·[[532_microservices_decomposition_patterns|마이크로서비스]] 아키텍처에서 보안 감리의 범위가 확대됐다. [[302_service_mesh_istio|서비스 메시]] [[164_policy|정책]]([[302_service_mesh_istio|Istio]]), [[014_api_posix|API]] 게이트웨이 접근 제어, [[561_container_based_deployment|컨테이너]] 이미지 보안, [[275_iam_role_for_service_accounts|서비스 계정]] 최소 권한이 현대 아키텍처 보안 감리의 핵심 점검 항목이다.

---

## Ⅰ. 개요 및 필요성

```text
┌──────────────────────────────────────────────────────┐
│       아키텍처 보안 감리 체계                         │
├──────────────────────────────────────────────────────┤
│                                                       │
│  감리 범위:                                           │
│  ┌────────────────────────────────────────────────┐  │
│  │ 네트워크 보안 아키텍처 (방화벽·DMZ·세그먼트)   │  │
│  │ 인증·권한 아키텍처 (IAM·SSO·MFA)              │  │
│  │ 데이터 보안 (암호화·키 관리·DLP)               │  │
│  │ 접근 제어 (RBAC·ABAC·Least Privilege)         │  │
│  │ 보안 모니터링 (SIEM·SOAR 통합)                │  │
│  └────────────────────────────────────────────────┘  │
│                                                       │
│  Zero Trust 원칙 검증:                                │
│    "Never Trust, Always Verify" 구현 여부             │
└──────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 시스템 아키텍처 보안 감리는 건물 준공 전 소방 안전 검사다. 건물이 완공되기 전 설계 단계에서 비상구·스프링클러·[[690_firewall_generation_evolution|방화벽]]을 제대로 설계했는지 독립적으로 검사한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[302_security_architecture_design|보안 아키텍처]] 핵심 원칙 [[395_verification_process_review|검증]]

| 원칙 | 감리 점검 항목 |
|:---|:---|
| **[[012_defense_in_depth|Defense in Depth]]** | 다계층 보안 통제 구현 여부 |
| **[[010_least_privilege|Least Privilege]]** | [[090_service_kubernetes_network_load_balancing|서비스]]·사용자별 최소 권한 부여 |
| **[[667_zero_trust_runtime_integrity_measurement|Zero Trust]]** | 내부 트래픽도 [[303_authentication_authorization_patterns|인증]]·암호화 |
| **Fail Secure** | 장애 시 보안 강화 방향으로 동작 |
| **[[011_separation_of_duties|Separation of Duties]]** | 권한 분리 (개발·운영·보안 분리) |

### [[531_cloud_native_architecture|클라우드 네이티브]] 보안 감리 항목

```text
컨테이너 보안:
  - 이미지 취약점 스캐닝 (Trivy, Snyk)
  - 특권 컨테이너(Privileged Container) 사용 여부
  - 읽기 전용 루트 파일 시스템

서비스 메시 (Istio):
  - mTLS (상호 TLS) 구현 여부
  - 서비스 간 최소 권한 정책

IAM:
  - 서비스 계정 키 만료 정책
  - MFA 강제 적용 여부
```

- **📢 섹션 요약 비유**: 클라우드 보안 감리는 아파트 단지 보안 점검이다. 출입 카드([[526_iam|IAM]]), 동별 잠금([[667_zero_trust_runtime_integrity_measurement|Zero Trust]]), [[933_cctv|CCTV]](모니터링), 화재 경보([[624_siem|SIEM]]) 등 각 보안 레이어가 제대로 구축됐는지 확인한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 아키텍처 감리 | 운영 [[527_security_audit_trail|보안 감사]] |
|:---|:---|:---|
| 시점 | 설계·구축 단계 | 운영 단계 |
| 목적 | 설계 보안 [[395_verification_process_review|검증]] | 운영 취약점 점검 |
| 효과 | 선제적 예방 | 사후 발견·개선 |
| 비용 효율 | 매우 높음 | 보통 |

- **📢 섹션 요약 비유**: 아키텍처 감리 vs 운영 [[606_auditing_linux_auditd|감사]]는 건물 설계 검토 vs 건물 안전 점검이다. 설계 단계 검토가 완공 후 보강 공사보다 훨씬 저렴하고 효과적이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 공공 정보화 사업 보안 감리 [[435_checklist_based_testing|체크리스트]]
- **[[781_personal_information|개인정보]] [[571_protection_vs_security|보호]]**: [[781_personal_information|개인정보]] 암호화(AES-256), 전송 구간 [[694_thread_local_storage_tls|TLS]] 1.2 이상.
- **접근 제어**: 역할 기반([[569_rbac|RBAC]]) 구현, 관리자 계정 분리.
- **네트워크**: [[219_demilitarized_zone_dmz_public_subnet|DMZ]] 구성, 내부망·외부망 분리, [[690_firewall_generation_evolution|방화벽]] [[164_policy|정책]] 문서화.
- **로깅·모니터링**: [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] 6개월 이상 보존, [[624_siem|SIEM]] 연동.
- **취약점 관리**: [[416_owasp_top_10|OWASP Top 10]] 점검, [[331_static_analysis|정적 분석]]([[491_sast_static_analysis|SAST]]) 수행 여부.

- **📢 섹션 요약 비유**: 공공 시스템 보안 감리 [[435_checklist_based_testing|체크리스트]]는 자동차 안전 검사 항목이다. 브레이크(접근 제어), 에어백(암호화), 블랙박스(로깅), 충돌 테스트(취약점 점검) — 각 항목을 빠짐없이 확인한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **설계 보안 강화** | [[058_security_by_design|Security by Design]] 실현 |
| **비용 절감** | 운영 단계 보안 패치 비용 감소 |
| **규제 준수** | [[783_pipa_korea|개인정보보호법]]·클라우드 보안 기준 충족 |

[[190_ai_llm_requirements_specification|AI]] 기반 자동화 보안 감리(Automated [[302_security_architecture_design|Security Architecture]] [[153_requirements_review_inspection_walkthrough|Review]])가 등장하고 있다. [[062_infrastructure_as_code|Infrastructure as Code]]([[793_iac_idempotency_template|IaC]]) 파일을 자동 분석하여 [[007_security_policy|보안 정책]] 위반을 실시간 탐지하는 정적 보안 분석 도구(Checkov, tfsec)가 현대 아키텍처 감리의 보조 도구로 활용된다.

- **📢 섹션 요약 비유**: [[793_iac_idempotency_template|IaC]] 보안 자동 감리는 코드 보안 맞춤법 검사기다. [[793_iac_idempotency_template|인프라 코드]]([[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]])를 작성할 때 "이 설정은 보안 취약점이 있어요"라고 실시간으로 알려주는 자동 감리 도구다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[667_zero_trust_runtime_integrity_measurement|Zero Trust]]** | 현대 [[302_security_architecture_design|보안 아키텍처]]의 핵심 원칙 |
| **[[012_defense_in_depth|Defense in Depth]]** | 다계층 보안 통제 |
| **[[526_iam|IAM]]** | [[303_authentication_authorization_patterns|인증]]·권한 아키텍처 |
| **[[793_iac_idempotency_template|IaC]] 보안 스캐닝** | 자동화 아키텍처 보안 [[395_verification_process_review|검증]] |
| **[[624_siem|SIEM]]** | 보안 모니터링 아키텍처 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 보안 감리 — 방화벽·DMZ·암호화 점검]
    │
    ▼
[클라우드 보안 감리 — IAM·VPC·암호화 키 관리]
    │
    ▼
[Zero Trust 아키텍처 감리 — mTLS·최소 권한 검증]
    │
    ▼
[컨테이너·마이크로서비스 감리 — 이미지 보안·서비스 메시]
    │
    ▼
[IaC 자동 보안 감리 — Checkov·tfsec 정적 분석]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 시스템 보안 감리는 건물 완공 전 소방 안전 검사예요! 나중에 고치는 것보다 설계 단계에서 잡는 게 훨씬 저렴해요.
2. [[667_zero_trust_runtime_integrity_measurement|Zero Trust]](절대 믿지 않기) 원칙이 제대로 구현됐는지, 모든 문에 잠금장치가 있는지 확인해요!
3. 요즘은 AI가 [[793_iac_idempotency_template|인프라 코드]]를 자동으로 분석해서 보안 취약점을 즉시 알려주는 자동 감리 도구도 있어요!
