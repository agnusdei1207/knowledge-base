+++
title = "53. 예방 통제 (Preventive Controls)"
date = 2026-05-01

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 예방 통제 (Preventive Controls)는 사고가 나기 전에 위협의 발생이나 확산을 막는 보안 통제다.
> 2. **가치**: [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/), [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/), [입력 검증](/knowledge-base/studynote/09_security/uncategorized/1034_input_validation/), 패치, 암호화, 분리 설계가 대표적인 예방 수단이다.
> 3. **판단 포인트**: 예방만으로는 충분하지 않다. [탐지 통제](/knowledge-base/studynote/09_security/01_intro_principles/054_detective_controls/)와 [교정 통제](/knowledge-base/studynote/09_security/01_intro_principles/055_corrective_controls/)를 함께 배치해야 방어가 완성된다.

---

## Ⅰ. 개요 및 필요성

보안은 사고 뒤에 대응하는 것보다 사고 자체를 줄이는 것이 더 효율적이다. 예방 통제는 바로 그 목적을 가진다. 시스템에 들어오는 위험을 미리 차단해 피해 가능성을 낮춘다.

특히 계정 탈취, 악성 입력, 네트워크 침입, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출은 사후 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)보다 사전 차단이 훨씬 싸다.

- **📢 섹션 요약 비유**: 예방 통제는 문을 잠그고 경비를 세워 도둑이 들어오지 못하게 하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

예방 통제는 사람, 네트워크, 애플리케이션, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 물리 환경에 걸쳐 적용된다. 위협이 시스템에 닿기 전에 경로를 차단하는 것이 핵심이다.

```text
Threat -> Preventive Control -> Block / Limit
```

| 영역 | 예시 | 목적 |
| :--- | :--- | :--- |
| Identity | [MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/), [least privilege](/knowledge-base/studynote/09_security/01_intro_principles/010_least_privilege/) | 계정 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| Network | [Firewall](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/), [segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) | 경로 차단 |
| App | [Input validation](/knowledge-base/studynote/09_security/uncategorized/1034_input_validation/) | 코드 공격 차단 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | Encryption, masking | 유출 방지 |
| Physical | Badge, [lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/) | 출입 통제 |

핵심 원리는 "기본 허용"이 아니라 "필요한 것만 허용"이다. 그래서 [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) ([Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/))와도 연결된다.

- **📢 섹션 요약 비유**: 예방 통제는 울타리, 자물쇠, 출입증, 검문소를 함께 두는 마을의 방어선이다.

---

## Ⅲ. 비교 및 연결

예방 통제는 [탐지 통제](/knowledge-base/studynote/09_security/01_intro_principles/054_detective_controls/) (Detective Control), [교정 통제](/knowledge-base/studynote/09_security/01_intro_principles/055_corrective_controls/) ([Corrective](/knowledge-base/studynote/04_software_engineering/06_software_architecture/380_maintenance_types/) Control), [억제 통제](/knowledge-base/studynote/09_security/01_intro_principles/056_deterrent_controls/) (Deterrent Control)와 함께 본다. 예방이 전부가 아니라 전체 방어 체계의 일부다.

| 통제 유형 | 목적 | 예 |
| :--- | :--- | :--- |
| Preventive | 사고 예방 | [MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/), [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) |
| Detective | [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [IDS](/knowledge-base/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/) |
| [Corrective](/knowledge-base/studynote/04_software_engineering/06_software_architecture/380_maintenance_types/) | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 패치, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) |
| Deterrent | [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) | 경고문, 배너 |

예방 통제는 특히 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 권한, [입력 검증](/knowledge-base/studynote/09_security/uncategorized/1034_input_validation/), 네트워크 경계, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)에서 중요하다. 하지만 오탐/미탐을 고려해 탐지와 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 반드시 결합해야 한다.

- **📢 섹션 요약 비유**: 예방은 우산, 탐지는 비 오는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 교정은 젖은 옷을 말리는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 최소 권한, 네트워크 분리, 보안 패치, 안전한 기본값, 비밀정보 관리가 기본이다. 예방 통제는 여러 층으로 쌓을수록 강해진다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 모든 계정에 MFA가 적용되는가?
2. [입력 검증](/knowledge-base/studynote/09_security/uncategorized/1034_input_validation/)과 권한 검사가 둘 다 있는가?
3. 중요 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 암호화되는가?
4. 네트워크와 시스템이 분리되어 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 단일 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)만 믿는 경우
- 권한을 넓게 주고 나중에 막으려는 경우
- 탐지/[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 체계를 없이 예방만 강조하는 경우

기술사 관점에서는 예방 통제가 비용을 줄이는 가장 앞단의 방어라는 점과, 단독으로는 충분하지 않다는 점을 함께 설명해야 한다.

- **📢 섹션 요약 비유**: 예방 통제는 집 앞의 자물쇠지만, 안에서 불이 날 수 있으니 경보기와 소화기도 필요하다.

---

## Ⅴ. 기대효과 및 결론

예방 통제는 침해와 오류를 미리 줄여 운영 안정성과 보안을 동시에 높인다. 적절히 설계된 예방 통제는 사고 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 자체를 낮춘다.

정리하면, 좋은 보안은 사고 후 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)보다 사고 전 차단에서 시작된다.

- **📢 섹션 요약 비유**: 예방 통제는 넘어지기 전에 손을 잡아 주는 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)대다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Preventive | 사전 차단 |
| Detective | [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) |
| [Corrective](/knowledge-base/studynote/04_software_engineering/06_software_architecture/380_maintenance_types/) | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| [Least Privilege](/knowledge-base/studynote/09_security/01_intro_principles/010_least_privilege/) | 최소 권한 |
| [Defense in Depth](/knowledge-base/studynote/09_security/01_intro_principles/012_defense_in_depth/) | 다층 방어 |

### 📈 관련 키워드 및 발전 흐름도

```text
위협 인지
    |
    v
예방 통제
    |
    v
탐지 통제
    |
    v
교정 통제
    |
    v
지속 개선
```

이 흐름은 사고를 막고, 못 막은 사고는 빨리 발견하고, 다시 고치는 보안 운영의 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 예방 통제는 문을 잠그고 낯선 사람을 막는 거예요.
2. 문제가 생기기 전에 미리 막으면 훨씬 안전해요.
3. 하지만 경보기와 소화기도 같이 있어야 더 든든해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 53 / 1108

<- **이전**: [52. 위험 완화 (Risk Mitigation)](/knowledge-base/studynote/09_security/01_intro_principles/052_risk_mitigation/)
**다음**: [54. 탐지 통제 (Detective Controls)](/knowledge-base/studynote/09_security/01_intro_principles/054_detective_controls/) ->

---
