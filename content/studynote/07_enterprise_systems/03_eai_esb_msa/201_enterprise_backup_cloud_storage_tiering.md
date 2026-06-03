---
title: 201. 엔터프라이즈 백업 아키텍처 클라우드 티어링 (Cloud Tiering)
date: '2026-05-08'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 티어링 (Cloud Tiering)은 [[555_backup_and_restore_strategy|백업]] [[001_dikw_pyramid|데이터]]를 접근 빈도와 보존 기간에 따라 서로 다른 저장 계층으로 자동 이동시키는 수명주기 기반 스토리지 최적화 [[268_strategy_pattern|전략]]이다.
> 2. **가치**: 최근 [[658_ir_recovery|복구]]용 [[001_dikw_pyramid|데이터]]는 빠른 계층에, 장기 보관용 [[001_dikw_pyramid|데이터]]는 저렴한 객체 스토리지나 아카이브 계층에 두어 총소유비용 ([[016_tco|TCO]], Total Cost of Ownership)과 [[061_on_premise_legacy_infrastructure|온프레미스]] 증설 부담을 크게 낮춘다.
> 3. **판단 포인트**: 성공의 핵심은 단순 저장비 절감이 아니라, [[658_ir_recovery|복구]] 시간 목표 ([[176_rto_recovery_time_objective|RTO]], [[176_rto_recovery_time_objective|Recovery Time Objective]]), [[658_ir_recovery|복구]] 시점 목표 ([[177_rpo_recovery_point_objective|RPO]], [[177_rpo_recovery_point_objective|Recovery Point Objective]]), 불변성, 반출 [[015_지연_데이터_관점|지연]]을 함께 고려한 [[164_policy|정책]] 설계에 있다.

---

## Ⅰ. 개요 및 필요성

클라우드 티어링은 [[555_backup_and_restore_strategy|백업]] [[001_dikw_pyramid|데이터]]를 한 종류의 스토리지에만 두지 않고, [[282_performance_tactics|성능]] 계층과 장기 보관 계층으로 나누어 관리하는 [[555_backup_and_restore_strategy|백업]] 아키텍처다. 최근 [[087_process_state_transition|생성]]된 [[555_backup_and_restore_strategy|백업]]은 [[658_ir_recovery|복구]] 가능성이 높으므로 빠른 디스크나 [[061_on_premise_legacy_infrastructure|온프레미스]] 스토리지에 두고, 오래된 [[555_backup_and_restore_strategy|백업]]은 저렴한 객체 스토리지나 아카이브로 이동시킨다. 이렇게 해야 급증하는 보존 [[001_dikw_pyramid|데이터]] 때문에 고가 장비를 무한정 증설하는 비효율을 줄일 수 있다.

[[001_dikw_pyramid|데이터]] 증가 속도는 [[090_service_kubernetes_network_load_balancing|서비스]] [[001_dikw_pyramid|데이터]] 증가보다 [[555_backup_and_restore_strategy|백업]] [[001_dikw_pyramid|데이터]]에서 더 가파르게 나타나는 경우가 많다. 운영 [[001_dikw_pyramid|데이터]] 자체는 수십 테라바이트 (TB, Terabyte)여도, 일일 [[555_backup_and_restore_strategy|백업]], 주간 전체 [[555_backup_and_restore_strategy|백업]], 장기 보관본이 누적되면 수 배 이상으로 커진다. 이 모든 [[001_dikw_pyramid|데이터]]를 동일한 고성능 스토리지에 보관하면, 실제로는 거의 읽지 않는 장기 [[555_backup_and_restore_strategy|백업]] 때문에 비용과 전력, 공간이 과도하게 낭비된다.

따라서 [[555_backup_and_restore_strategy|백업]] 설계에서 중요한 것은 "어디에 저장할까"만이 아니라 "언제 어느 계층으로 내릴까"다. [[555_backup_and_restore_strategy|백업]]은 [[282_performance_tactics|성능]]보다 [[658_ir_recovery|복구]] 가능성과 보존 [[164_policy|정책]]이 핵심이므로, [[001_dikw_pyramid|데이터]] 온도와 규제 요구를 반영한 계층화가 필수다.

- **📢 섹션 요약 비유**: 클라우드 티어링은 자주 꺼내는 옷은 옷장 앞칸에 두고, 계절 지난 옷은 창고 박스로 옮기는 정리법과 같다. 모든 옷을 비싼 드레스룸 맨 앞에 둘 필요는 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

전형적인 구조는 [[282_performance_tactics|성능]] 티어, 용량 티어, 아카이브 티어, 그리고 이를 움직이는 정보 수명주기 관리 (ILM, Information [[927_medical_device_lifecycle|Lifecycle Management]]) [[164_policy|정책]] 엔진으로 구성된다. [[555_backup_and_restore_strategy|백업]] 소프트웨어는 [[087_process_state_transition|생성]] 시점, 마지막 접근 시점, 보존 등급, 불변 [[164_policy|정책]]을 기준으로 [[001_dikw_pyramid|데이터]]를 어느 계층에 둘지 결정한다. [[658_ir_recovery|복구]] 요청이 오면 필요 시 아카이브에서 다시 불러오는 리콜 ([[254_recall_sensitivity|Recall]]) 과정이 수행된다.

| 계층 | 대표 [[121_transmission_media_guided_unguided|매체]] | 용도 | 설계 포인트 |
| :-- | :-- | :-- | :-- |
| [[282_performance_tactics|성능]] 티어 | 고체 상태 드라이브 ([[327_ssd|SSD]], [[327_ssd|Solid State Drive]]), 네트워크 결합 스토리지 ([[492_nas_network_attached_storage|NAS]], [[492_nas_network_attached_storage|Network Attached Storage]]) | 최근 [[555_backup_and_restore_strategy|백업]], 즉시 [[658_ir_recovery|복구]] | 짧은 [[176_rto_recovery_time_objective|RTO]], 빠른 랜덤 접근 |
| 용량 티어 | [[465_hdd_structure|하드 디스크 드라이브]] ([[465_hdd_structure|HDD]], Hard Disk Drive), 객체 스토리지 | 중기 보관, 일반 [[658_ir_recovery|복구]] | 비용 효율, 확장성 |
| 아카이브 티어 | Glacier, Tape | 장기 보관, 규제 대응 | 저비용, 높은 [[658_ir_recovery|복구]] [[015_지연_데이터_관점|지연]] |
| [[164_policy|정책]] 엔진 | ILM, [[555_backup_and_restore_strategy|백업]] 소프트웨어 | 이동·보존·삭제 자동화 | [[164_policy|정책]] [[002_bigdata_5v|정확성]], [[606_auditing_linux_auditd|감사]]성 |
| 불변 계층 | 객체 잠금 (Object [[510_lock|Lock]]), [[590_worm|WORM]] ([[693_worm_storage|Write Once Read Many]]) | [[730_ransomware|랜섬웨어]] 방어 | 삭제 금지, 보존 기간 준수 |

아래 그림은 [[555_backup_and_restore_strategy|백업]] [[001_dikw_pyramid|데이터]]가 시간이 지나며 더 저렴한 계층으로 이동하고, [[658_ir_recovery|복구]] 시에는 다시 리콜되는 구조를 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                         Backup data lifecycle tiering                     │
├────────────────────────────────────────────────────────────────────────────┤
│ Backup Job -> Performance Tier -> Capacity Tier -> Archive Tier          │
│                (SSD / NAS)        (Object / HDD)     (Glacier / Tape)    │
│                     └────────── ILM / retention policy ──────────┘        │
│                                      │                                     │
│                                      ▼                                     │
│                         Recall for restore / immutable copy                │
└────────────────────────────────────────────────────────────────────────────┘
```

핵심 원리는 자동 이동 자체보다 [[164_policy|정책]] [[233_precision_recall_f1_roc_auc_threshold|정밀도]]에 있다. 예를 들어 30일 이내 [[555_backup_and_restore_strategy|백업]]은 [[061_on_premise_legacy_infrastructure|온프레미스]]에 유지하고, 30일 이후는 객체 스토리지로 이동하며, 1년 이후는 딥 아카이브 (Deep Archive)로 내리는 식의 [[164_policy|정책]]이 대표적이다. 여기에 객체 잠금 (Object [[510_lock|Lock]])과 [[590_worm|WORM]] ([[693_worm_storage|Write Once Read Many]])을 결합하면, [[555_backup_and_restore_strategy|백업]] 복사본이 삭제·변조되지 않는 불변 저장소 역할도 수행할 수 있다.

- **📢 섹션 요약 비유**: 클라우드 티어링은 냉장고, 창고, 장기 보관 창고를 나눠 쓰는 살림과 같다. 오늘 먹을 음식과 3년 뒤 꺼낼 비상식량을 같은 자리에 둘 필요는 없다.

---

## Ⅲ. 비교 및 연결

클라우드 티어링은 [[555_backup_and_restore_strategy|백업]], [[022_snapshot_backup_architecture|스냅샷]], 아카이브와 비슷해 보이지만 목적이 다르다. [[022_snapshot_backup_architecture|스냅샷]]은 빠른 시점 [[658_ir_recovery|복구]]에 초점이 있고, [[555_backup_and_restore_strategy|백업]]은 장애·삭제·재해에 대비한 독립 복사본에 가깝다. 아카이브는 장기 보관과 규제 대응에 초점이 있으며, 티어링은 이들 [[001_dikw_pyramid|데이터]]를 비용과 [[658_ir_recovery|복구]] 요구에 맞춰 적절한 계층에 배치하는 운영 [[268_strategy_pattern|전략]]이다.

| 구분 | [[022_snapshot_backup_architecture|스냅샷]] | [[555_backup_and_restore_strategy|백업]] + 티어링 | 아카이브 |
| :-- | :-- | :-- | :-- |
| 주 목적 | 빠른 [[098_rollback_strategy_pipeline_error_threshold|롤백]] | [[658_ir_recovery|복구]] 가능성 + 비용 최적화 | 장기 보존 |
| 저장 위치 | 원본과 가까운 스토리지 | 다계층 스토리지 | 저비용 장기 저장소 |
| [[658_ir_recovery|복구]] 속도 | 매우 빠름 | 계층에 따라 다름 | 느림 |
| 대표 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] | 원본 장애 전파 가능 | [[164_policy|정책]] 오류 시 [[658_ir_recovery|복구]] [[015_지연_데이터_관점|지연]] | 즉시 [[658_ir_recovery|복구]] 어려움 |

또한 [[061_on_premise_legacy_infrastructure|온프레미스]] 티어링과 클라우드 티어링도 구분해야 한다. 전자는 내부 스토리지 계층만 바꾸는 반면, 후자는 클라우드 객체 스토리지를 활용해 사실상 무한 확장과 지역 외부 [[016_replication_factor|복제]]를 얻는다. 대신 네트워크 [[140_bandwidth|대역폭]], 반출 비용, [[658_ir_recovery|복구]] [[015_지연_데이터_관점|지연]]이라는 새로운 판단 요소가 추가된다.

- **📢 섹션 요약 비유**: [[022_snapshot_backup_architecture|스냅샷]]이 책상 위 복사본이라면, [[555_backup_and_restore_strategy|백업]]은 금고 속 사본이고, 아카이브는 지하 문서 보관소다. 티어링은 이 문서들을 언제 어디로 옮길지 정하는 보관 [[164_policy|정책]]이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[555_backup_and_restore_strategy|백업]] [[001_dikw_pyramid|데이터]]의 중요도와 [[658_ir_recovery|복구]] 빈도를 등급화해 티어 [[164_policy|정책]]을 나누는 것이 출발점이다. 운영 [[658_ir_recovery|복구]]가 잦은 가상 머신 [[555_backup_and_restore_strategy|백업]]은 빠른 티어에 더 오래 남겨 두고, 법정 보관용 [[555_backup_and_restore_strategy|백업]]은 조기에 저비용 티어로 이동시키는 식이다. 또한 [[730_ransomware|랜섬웨어]] 대응을 위해 최소 한 계층은 삭제 불가 [[164_policy|정책]]과 별도 계정, 별도 리전에 두는 것이 안전하다.

### [[435_checklist_based_testing|체크리스트]]

1. [[001_dikw_pyramid|데이터]] 등급별 [[176_rto_recovery_time_objective|RTO]]·RPO가 정의되어 있는가?
2. 티어 이동 이후 [[658_ir_recovery|복구]] [[015_지연_데이터_관점|지연]]과 반출 비용을 사업이 감당할 수 있는가?
3. 불변성 [[164_policy|정책]]과 보존 기간이 규제 요구와 일치하는가?
4. 리콜 테스트와 [[658_ir_recovery|복구]] 훈련을 정기적으로 수행하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 저장비만 보고 장기 보관 티어로 빠르게 내린 뒤, 실제 [[658_ir_recovery|복구]] 시간이 업무 기준을 초과하는 설계
- [[061_on_premise_legacy_infrastructure|온프레미스]] 장애 대비 없이 같은 계정, 같은 리전에만 [[555_backup_and_restore_strategy|백업]]을 두는 설계
- 티어링 [[164_policy|정책]]은 자동화했지만, 실제 리스토어 [[395_verification_process_review|검증]]을 하지 않아 종이상 [[555_backup_and_restore_strategy|백업]]만 존재하는 상태

기술사 답안에서는 비용 절감뿐 아니라 [[658_ir_recovery|복구]] [[282_performance_tactics|성능]]과 [[283_security_tactics|보안성]]을 함께 언급해야 한다. 특히 "티어링 = 아카이브"로 단순화하지 말고, 운영 [[658_ir_recovery|복구]] 구간과 장기 보존 구간을 분리해 설명하면 경계가 명확해진다.

- **📢 섹션 요약 비유**: 값싼 창고를 빌리는 것만으로 좋은 이사가 되는 것은 아니다. 급히 꺼내야 할 짐이 있다면, 가장 싼 창고보다 꺼내기 쉬운 위치를 함께 따져야 한다.

---

## Ⅴ. 기대효과 및 결론

클라우드 티어링을 적절히 설계하면 고가 스토리지 증설을 줄이고, 장기 보관 [[555_backup_and_restore_strategy|백업]]의 운영 비용을 크게 낮출 수 있다. 동시에 객체 잠금과 외부 리전 보관을 활용하면 [[379_dr_architecture|재해 복구]]와 [[730_ransomware|랜섬웨어]] 대응력도 강화된다. 즉 티어링은 단순 저장 기술이 아니라 비용, [[658_ir_recovery|복구]], 보안을 함께 최적화하는 [[555_backup_and_restore_strategy|백업]] 운영 [[268_strategy_pattern|전략]]이다.

물론 지나친 저비용 최적화는 [[658_ir_recovery|복구]] 실패로 되돌아올 수 있다. 실제 [[658_ir_recovery|복구]]가 필요한 [[001_dikw_pyramid|데이터]]를 과도하게 깊은 아카이브로 보내거나, 테스트 없는 자동 [[164_policy|정책]]에 의존하면 위기 시 [[555_backup_and_restore_strategy|백업]]이 쓸모없어질 수 있다. 따라서 이 개념은 **[[001_dikw_pyramid|데이터]] 온도와 [[658_ir_recovery|복구]] 요구에 맞춰 [[555_backup_and_restore_strategy|백업]]의 거주지를 설계하는 것**으로 기억하는 편이 가장 정확하다.

- **📢 섹션 요약 비유**: 클라우드 티어링은 모든 짐을 가장 싼 창고에 넣는 기술이 아니라, 자주 쓰는 짐과 거의 안 쓰는 짐의 자리를 다르게 배치해 집과 창고를 함께 효율적으로 쓰는 방법이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| ILM (Information [[927_medical_device_lifecycle|Lifecycle Management]]) | [[555_backup_and_restore_strategy|백업]] [[001_dikw_pyramid|데이터]]의 이동·보존·삭제 [[164_policy|정책]]을 자동화 |
| [[176_rto_recovery_time_objective|RTO]]/[[177_rpo_recovery_point_objective|RPO]] | 계층 선택 시 [[658_ir_recovery|복구]] 속도와 허용 [[001_dikw_pyramid|데이터]] 손실을 결정 |
| 객체 잠금 (Object [[510_lock|Lock]]) | 클라우드 [[555_backup_and_restore_strategy|백업]]의 불변성을 보장하는 기능 |
| [[590_worm|WORM]] ([[693_worm_storage|Write Once Read Many]]) | 삭제·변조를 막아 [[730_ransomware|랜섬웨어]] 방어력을 높이는 저장 방식 |
| 딥 아카이브 (Deep Archive) | 최저 비용 대신 높은 [[658_ir_recovery|복구]] [[015_지연_데이터_관점|지연]]을 감수하는 장기 보관 계층 |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 고가 스토리지 백업
    │
    ▼
성능 티어 + 용량 티어 분리
    │
    ▼
객체 스토리지 활용
    │
    ▼
아카이브 · 불변 백업 결합
    │
    ▼
정책 기반 클라우드 티어링 백업 아키텍처
```

이 흐름은 단순 보관에서, 비용·[[658_ir_recovery|복구]]·보안을 함께 최적화하는 계층형 [[555_backup_and_restore_strategy|백업]] [[268_strategy_pattern|전략]]으로 진화한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 자주 쓰는 장난감은 방 안 가까운 상자에 두고, 잘 안 쓰는 장난감은 창고에 넣어 두는 것과 같아요.
2. 클라우드 티어링은 컴퓨터가 알아서 어떤 상자에 넣을지 정해 주는 정리 방법이에요.
3. 그래서 방은 덜 복잡해지고, 필요할 때는 다시 꺼내 쓸 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 201 / 482

← **이전**: [[200_low_code_no_code_enterprise_workflow_automation|200. 로우코드 / 노코드 (LC/NC) 기반 엔터프라이즈 워크플로우 자동화]]
**다음**: [[202_bpm_lifecycle_design_execution_monitoring_optimization|202. BPM 라이프사이클 (Business Process Management Lifecycle)]] →

---
