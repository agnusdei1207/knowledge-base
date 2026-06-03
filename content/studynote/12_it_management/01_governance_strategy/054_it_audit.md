---
title: 54. IT 감사 (IT Audit)
date: '2026-05-01'
tags:
- studynote-it-management
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT [[606_auditing_linux_auditd|감사]]는 정보시스템의 통제, 보안, 운영, 준법 상태를 독립적으로 확인하는 활동이다.
> 2. **가치**: 접근권한, [[555_backup_and_restore_strategy|백업]], [[568_logs_distributed_logging_elk_fluentd|로그]], 변경, 개발통제가 제대로 작동하는지 검증한다.
> 3. **판단 포인트**: 위험 기반으로 범위를 정하고, 증거 중심으로 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

IT는 조직의 핵심 운영 자산이므로, 제대로 통제되지 않으면 보안 사고와 업무 중단으로 이어진다. IT [[606_auditing_linux_auditd|감사]]는 이런 위험을 객관적으로 점검한다.

[[606_auditing_linux_auditd|감사]]는 "잘 되고 있다"는 말이 아니라 실제 증거를 보는 일이다.

- **📢 섹션 요약 비유**: IT [[606_auditing_linux_auditd|감사]]는 집 문이 잠겼는지, 열쇠가 누구에게 있는지 확인하는 검사다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT [[606_auditing_linux_auditd|감사]]는 사람, 프로세스, 시스템, [[001_dikw_pyramid|데이터]], 보안 통제를 함께 본다. 범위는 자산, 계정, [[568_logs_distributed_logging_elk_fluentd|로그]], [[555_backup_and_restore_strategy|백업]], 변경관리, 재해복구까지 넓다.

```text
IT Governance → Controls → Evidence → Findings → Recommendation
```

| 영역 | 예시 통제 | 증거 |
| :--- | :--- | :--- |
| Access | 권한 검토 | 계정 목록 |
| Change | 승인/배포 | 변경 기록 |
| [[555_backup_and_restore_strategy|Backup]] | [[658_ir_recovery|복구]] 가능성 | [[658_ir_recovery|복구]] 테스트 |
| [[526_security_logging_and_monitoring_failures|Logging]] | 추적성 | [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] |

핵심은 통제가 문서상 존재하는지보다 실제로 동작하는지를 확인하는 것이다.

- **📢 섹션 요약 비유**: IT [[606_auditing_linux_auditd|감사]]는 안전벨트가 차 안에 있는지보다 실제로 맬 수 있는지 보는 일이다.

---

## Ⅲ. 비교 및 연결

IT [[606_auditing_linux_auditd|감사]]는 [[062_itil|ITIL]]/[[096_iso_iec_20000_itsm_certification|ITSM]] [[606_auditing_linux_auditd|감사]]보다 넓은 범위를 볼 수 있다. ITSM이 [[090_service_kubernetes_network_load_balancing|서비스]] 프로세스 중심이라면 IT [[606_auditing_linux_auditd|감사]]는 기술 통제와 리스크를 더 폭넓게 본다.

| 항목 | IT [[606_auditing_linux_auditd|감사]] | [[096_iso_iec_20000_itsm_certification|ITSM]] [[606_auditing_linux_auditd|감사]] |
| :--- | :--- | :--- |
| 초점 | 통제/준법/보안 | [[090_service_kubernetes_network_load_balancing|서비스]] 프로세스 |
| 증거 | 권한, [[568_logs_distributed_logging_elk_fluentd|로그]], [[555_backup_and_restore_strategy|백업]] | 티켓, [[018_kpi|KPI]], 승인 |
| 목적 | 통제 적합성 | 운영 성숙도 |

IT [[606_auditing_linux_auditd|감사]]는 내부감사, 외부감사, 규제 대응과도 연결된다. 따라서 통제 설계와 운영 증거가 동시에 필요하다.

- **📢 섹션 요약 비유**: IT [[606_auditing_linux_auditd|감사]]는 건물 전체의 전기, 소방, 출입통제를 보는 종합 점검이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 범위를 좁게 잡고, 위험이 큰 영역부터 증거를 확인한다. 계정, 변경, [[555_backup_and_restore_strategy|백업]], [[568_logs_distributed_logging_elk_fluentd|로그]], [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 테스트는 우선순위가 높다.

### [[435_checklist_based_testing|체크리스트]]

1. 접근권한과 분리가 적절한가?
2. 변경 승인과 기록이 남는가?
3. [[555_backup_and_restore_strategy|백업]]/[[658_ir_recovery|복구]]가 실제로 검증되는가?
4. [[568_logs_distributed_logging_elk_fluentd|로그]]와 모니터링이 추적 가능한가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 문서만 있고 실제 증거가 없는 경우
- [[606_auditing_linux_auditd|감사]] 범위가 너무 넓어 핵심 리스크를 놓치는 경우
- 문제를 찾아내는 데 그치고 개선이 없는 경우

기술사 관점에서는 IT [[606_auditing_linux_auditd|감사]]가 시스템 기술뿐 아니라 통제 설계와 운영 증거를 함께 보는 활동이라는 점을 강조해야 한다.

- **📢 섹션 요약 비유**: IT [[606_auditing_linux_auditd|감사]]는 집의 창문, 자물쇠, CCTV가 같이 잘 돌아가는지 보는 일이다.

---

## Ⅴ. 기대효과 및 결론

IT [[606_auditing_linux_auditd|감사]]는 조직의 통제 신뢰도를 높이고 사고를 예방한다. 또한 개선 과제를 우선순위화하는 기준이 된다.

정리하면, IT [[606_auditing_linux_auditd|감사]]는 "통제가 설계대로 실제로 작동하는가"를 확인하는 과정이다.

- **📢 섹션 요약 비유**: IT [[606_auditing_linux_auditd|감사]]는 지도와 실제 길이 같은지 확인하는 탐험가다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[547_access_control_rwx|Access Control]] | 계정 통제 |
| Change Control | 변경 통제 |
| [[555_backup_and_restore_strategy|Backup]]/[[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] | [[658_ir_recovery|복구]] 통제 |
| [[526_security_logging_and_monitoring_failures|Logging]] | 추적 통제 |
| Evidence | [[606_auditing_linux_auditd|감사]] 증거 |

### 📈 관련 키워드 및 발전 흐름도

```text
리스크 식별
    │
    ▼
통제 설계
    │
    ▼
증거 수집
    │
    ▼
감사 판단
    │
    ▼
개선 조치
```

이 흐름은 IT 통제가 설계에서 운영, [[606_auditing_linux_auditd|감사]], 개선으로 이어지는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. IT [[606_auditing_linux_auditd|감사]]는 컴퓨터 방이 안전한지 살펴보는 검사예요.
2. 열쇠, 기록, [[555_backup_and_restore_strategy|백업]]이 제대로 있는지 봐요.
3. 그래서 문제가 생기기 전에 고칠 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 97 / 587

← **이전**: [[053_data_stewardship_role|53. 데이터 스튜어드 역할 (Data Stewardship Role)]]
**다음**: [[055_digital_transformation|55. 디지털 전환 (Digital Transformation)]] →

---
