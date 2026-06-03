---
title: 53. 예방 통제 (Preventive Controls)
date: '2026-05-01'
tags:
- studynote-security
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 예방 통제 (Preventive Controls)는 사고가 나기 전에 위협의 발생이나 확산을 막는 보안 통제다.
> 2. **가치**: [[387_access_control_pattern|접근 통제]], [[690_firewall_generation_evolution|방화벽]], [[601_input_validation|입력 검증]], 패치, 암호화, 분리 설계가 대표적인 예방 수단이다.
> 3. **판단 포인트**: 예방만으로는 충분하지 않다. [[054_detective_controls|탐지 통제]]와 [[055_corrective_controls|교정 통제]]를 함께 배치해야 방어가 완성된다.

---

## Ⅰ. 개요 및 필요성

보안은 사고 뒤에 대응하는 것보다 사고 자체를 줄이는 것이 더 효율적이다. 예방 통제는 바로 그 목적을 가진다. 시스템에 들어오는 위험을 미리 차단해 피해 가능성을 낮춘다.

특히 계정 탈취, 악성 입력, 네트워크 침입, [[001_dikw_pyramid|데이터]] 유출은 사후 [[658_ir_recovery|복구]]보다 사전 차단이 훨씬 싸다.

- **📢 섹션 요약 비유**: 예방 통제는 문을 잠그고 경비를 세워 도둑이 들어오지 못하게 하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

예방 통제는 사람, 네트워크, 애플리케이션, [[001_dikw_pyramid|데이터]], 물리 환경에 걸쳐 적용된다. 위협이 시스템에 닿기 전에 경로를 차단하는 것이 핵심이다.

```text
Threat → Preventive Control → Block / Limit
```

| 영역 | 예시 | 목적 |
| :--- | :--- | :--- |
| Identity | [[552_mfa|MFA]], [[010_least_privilege|least privilege]] | 계정 [[571_protection_vs_security|보호]] |
| Network | [[690_firewall_generation_evolution|Firewall]], [[364_segmentation|segmentation]] | 경로 차단 |
| App | [[601_input_validation|Input validation]] | 코드 공격 차단 |
| [[001_dikw_pyramid|Data]] | Encryption, masking | 유출 방지 |
| Physical | Badge, [[510_lock|lock]] | 출입 통제 |

핵심 원리는 "기본 허용"이 아니라 "필요한 것만 허용"이다. 그래서 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]])와도 연결된다.

- **📢 섹션 요약 비유**: 예방 통제는 울타리, 자물쇠, 출입증, 검문소를 함께 두는 마을의 방어선이다.

---

## Ⅲ. 비교 및 연결

예방 통제는 [[054_detective_controls|탐지 통제]] (Detective Control), [[055_corrective_controls|교정 통제]] ([[380_maintenance_types|Corrective]] Control), [[056_deterrent_controls|억제 통제]] (Deterrent Control)와 함께 본다. 예방이 전부가 아니라 전체 방어 체계의 일부다.

| 통제 유형 | 목적 | 예 |
| :--- | :--- | :--- |
| Preventive | 사고 예방 | [[552_mfa|MFA]], [[549_acl_access_control_list|ACL]] |
| Detective | [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] | [[568_logs_distributed_logging_elk_fluentd|로그]], [[601_ids_ips_syscall_tracing|IDS]] |
| [[380_maintenance_types|Corrective]] | [[658_ir_recovery|복구]] | 패치, [[555_backup_and_restore_strategy|백업]] |
| Deterrent | [[656_ir_containment|억제]] | 경고문, 배너 |

예방 통제는 특히 [[303_authentication_authorization_patterns|인증]], 권한, [[601_input_validation|입력 검증]], 네트워크 경계, [[001_dikw_pyramid|데이터]] [[571_protection_vs_security|보호]]에서 중요하다. 하지만 오탐/미탐을 고려해 탐지와 [[658_ir_recovery|복구]]를 반드시 결합해야 한다.

- **📢 섹션 요약 비유**: 예방은 우산, 탐지는 비 오는지 [[396_validation|확인]], 교정은 젖은 옷을 말리는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 최소 권한, 네트워크 분리, 보안 패치, 안전한 기본값, 비밀정보 관리가 기본이다. 예방 통제는 여러 층으로 쌓을수록 강해진다.

### [[435_checklist_based_testing|체크리스트]]

1. 모든 계정에 MFA가 적용되는가?
2. [[601_input_validation|입력 검증]]과 권한 검사가 둘 다 있는가?
3. 중요 [[001_dikw_pyramid|데이터]]가 암호화되는가?
4. 네트워크와 시스템이 분리되어 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 단일 [[690_firewall_generation_evolution|방화벽]]만 믿는 경우
- 권한을 넓게 주고 나중에 막으려는 경우
- 탐지/[[658_ir_recovery|복구]] 체계를 없이 예방만 강조하는 경우

기술사 관점에서는 예방 통제가 비용을 줄이는 가장 앞단의 방어라는 점과, 단독으로는 충분하지 않다는 점을 함께 설명해야 한다.

- **📢 섹션 요약 비유**: 예방 통제는 집 앞의 자물쇠지만, 안에서 불이 날 수 있으니 경보기와 소화기도 필요하다.

---

## Ⅴ. 기대효과 및 결론

예방 통제는 침해와 오류를 미리 줄여 운영 안정성과 보안을 동시에 높인다. 적절히 설계된 예방 통제는 사고 [[130_probability|확률]] 자체를 낮춘다.

정리하면, 좋은 보안은 사고 후 [[658_ir_recovery|복구]]보다 사고 전 차단에서 시작된다.

- **📢 섹션 요약 비유**: 예방 통제는 넘어지기 전에 손을 잡아 주는 [[571_protection_vs_security|보호]]대다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Preventive | 사전 차단 |
| Detective | [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] |
| [[380_maintenance_types|Corrective]] | [[658_ir_recovery|복구]] |
| [[010_least_privilege|Least Privilege]] | 최소 권한 |
| [[012_defense_in_depth|Defense in Depth]] | 다층 방어 |

### 📈 관련 키워드 및 발전 흐름도

```text
위협 인지
    │
    ▼
예방 통제
    │
    ▼
탐지 통제
    │
    ▼
교정 통제
    │
    ▼
지속 개선
```

이 흐름은 사고를 막고, 못 막은 사고는 빨리 발견하고, 다시 고치는 보안 운영의 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 예방 통제는 문을 잠그고 낯선 사람을 막는 거예요.
2. 문제가 생기기 전에 미리 막으면 훨씬 안전해요.
3. 하지만 경보기와 소화기도 같이 있어야 더 든든해요.
