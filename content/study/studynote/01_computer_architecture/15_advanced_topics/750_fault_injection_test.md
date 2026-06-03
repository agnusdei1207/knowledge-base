---
title: 750. 결함 주입 테스트 (Fault Injection Test)
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[352_defect_definition|결함]] 주입 테스트 ([[670_fault_injection_chaos_testing_kernel|Fault Injection]] Test)는 시스템이 정상일 때 일부러 [[073_bit|비트]] 반전, 링크 단절, 전원 강하, [[573_timeout_retry_backoff_strategy|타임아웃]] 같은 오류를 넣어 **감지·격리·[[658_ir_recovery|복구]] 경로가 실제로 작동하는지 [[396_validation|확인]]하는 [[395_verification_process_review|검증]] 기법**이다.
> 2. **가치**: 평상시에는 거의 실행되지 않는 예외 처리 코드를 강제로 통과시켜, 문서상 이중화와 실제 복원력 사이의 간극을 드러낸다.
> 3. **판단 포인트**: 무엇을 어디에 어떻게 주입할지는 실제 현장 고장 모델과 연결되어야 하며, **관측 지표·안전 경계·합격 기준** 없이 무작위로 깨뜨리는 것은 좋은 테스트가 아니다.

---

## Ⅰ. 개요 및 필요성

[[352_defect_definition|결함]] 주입 테스트 ([[670_fault_injection_chaos_testing_kernel|Fault Injection]] Test)는 시스템에 인위적 오류를 넣어 **오류가 발생했을 때의 반응을 [[395_verification_process_review|검증]]**하는 방법이다. 기능 테스트가 정상 입력에서 올바른 출력이 나오는지를 본다면, [[352_defect_definition|결함]] 주입은 비정상 상황에서 **탐지, 격리, [[658_ir_recovery|복구]], [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] 보존**이 되는지를 본다. 즉 "정상 동작 증명"이 아니라 "고장 대응 증명"에 가깝다.

이 기법이 필요한 이유는 실제 장애의 상당수가 평소 경로가 아니라 예외 경로에서 터지기 때문이다. 우주 방사선에 의한 **단일 사건 업셋 (Single Event Upset, SEU)**, 느슨해진 케이블, 간헐적 [[001_voltage|전압]] 강하, [[032_firmware|펌웨어]] [[281_deadlock_definition|교착 상태]], [[344_bus|버스]] [[573_timeout_retry_backoff_strategy|타임아웃]]은 평상시 부하 테스트만으로는 드러나지 않는다. 평소엔 한 번도 호출되지 않던 예외 핸들러가 실전에서 처음 실행되면, 설계자는 그제야 숨은 가정을 발견하게 된다.

또한 [[352_defect_definition|결함]] 주입은 단순 파괴가 아니라 **모델 기반 [[395_verification_process_review|검증]]**이어야 한다. 예를 들어 "메모리 1비트 뒤집힘"을 시험하려면 오류 정정 코드 (Error Correcting [[082_process_memory_structure|Code]], [[554_ecc_circuit|ECC]])가 교정했는지, "[[356_pcie|PCI Express]] ([[355_pci|Peripheral Component Interconnect]] Express, [[356_pcie|PCIe]]) 링크 단절"을 시험하려면 재훈련이 몇 밀리초 걸렸는지, "컨트롤러 다운"을 시험하려면 세션이 중복 처리되지 않았는지를 함께 봐야 한다. 그래서 Fault Injection은 테스트 도구라기보다 **[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 가설을 [[395_verification_process_review|검증]]하는 실험 체계**라고 보는 편이 정확하다.

- **📢 섹션 요약 비유**: [[352_defect_definition|결함]] 주입 테스트는 소방 훈련 때 진짜 연기 발생기를 켜 보고, 경보기·대피 유도·스프링클러가 제대로 반응하는지 [[396_validation|확인]]하는 연습과 같다. 비상벨만 벽에 달아 놓는다고 훈련이 되지는 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

좋은 [[352_defect_definition|결함]] 주입 테스트는 보통 **정상 상태 정의 → [[352_defect_definition|결함]] 주입 → 감지 [[396_validation|확인]] → [[658_ir_recovery|복구]] [[395_verification_process_review|검증]] → 결과 판정** 순서로 설계된다. 먼저 기준 부하와 정상 지표를 정하고, 그다음 실제 고장과 닮은 fault model을 주입한다. 이후 하드웨어 센서, 오류 [[568_logs_distributed_logging_elk_fluentd|로그]], [[573_timeout_retry_backoff_strategy|타임아웃]], [[112_checksum|체크섬]], [[090_service_kubernetes_network_load_balancing|서비스]] 지표를 통해 감지가 이루어졌는지 보고, 마지막으로 [[658_ir_recovery|복구]] 시간과 [[001_dikw_pyramid|데이터]] 정확성을 판정한다.

아래 흐름은 Fault Injection이 단순히 "깨뜨린다"가 아니라 **주입기, 감지기, [[658_ir_recovery|복구]]기, 판정기**가 연결된 [[395_verification_process_review|검증]] 루프임을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                 Fault Injection verification loop                   │
├──────────────────────────────────────────────────────────────────────┤
│ Baseline workload                                                    │
│      │                                                               │
│      ▼                                                               │
│ [Injector] ─▶ bit flip / link down / power cut / delay               │
│      │                                                               │
│      ▼                                                               │
│ [Detector] ─▶ ECC / watchdog / timeout / bus error log              │
│      │                                                               │
│      ▼                                                               │
│ [Recovery] ─▶ retry / isolate / failover / reset                     │
│      │                                                               │
│      ▼                                                               │
│ [Oracle] ─▶ latency, error count, data integrity, state continuity   │
└──────────────────────────────────────────────────────────────────────┘
```

주입 지점은 하드웨어, [[032_firmware|펌웨어]], [[001_operating_system_purpose|운영체제]], 네트워크, 저장장치 등 다양하다. 하드웨어 레벨에서는 전원 공급기 강하, 클럭 글리치, 핀 레벨 강제 값, 메모리 [[073_bit|비트]] 플립, 디스크 분리 등을 다룰 수 있다. 시스템 레벨에서는 드라이버 [[573_timeout_retry_backoff_strategy|타임아웃]], 패킷 손실, 스토리지 [[015_지연_데이터_관점|지연]], 프로세스 중단처럼 물리 장애를 논리적으로 모의한다.

| [[352_defect_definition|결함]] 유형 | 대표 예시 | 기대 반응 | 주요 측정값 |
| :--- | :--- | :--- | :--- |
| 일시적 [[352_defect_definition|결함]] (Transient Fault) | 정적 램 (Static Random Access Memory, [[250_sram|SRAM]]) 1비트 뒤집힘 | [[554_ecc_circuit|ECC]] 교정, [[568_logs_distributed_logging_elk_fluentd|로그]] 기록 | 교정 횟수, [[282_performance_tactics|성능]] 영향 |
| 간헐 [[352_defect_definition|결함]] (Intermittent Fault) | [[587_nic_offloading|네트워크 인터페이스 카드]] (Network Interface Card, [[587_nic_offloading|NIC]]) 링크 플랩, 패킷 손실 | 재전송, 경로 우회 | 재시도 횟수, [[015_지연_데이터_관점|지연]] 증가 |
| 영구 [[352_defect_definition|결함]] (Permanent Fault) | 컨트롤러 다운, 디스크 제거 | 격리 후 예비 경로 전환 | [[658_ir_recovery|복구]] 시간, [[001_dikw_pyramid|데이터]] 지속성 |
| 환경성 [[352_defect_definition|결함]] | [[001_voltage|전압]] 강하, 과열, 진동 | 스로틀링, 셧다운, 알람 | [[571_protection_vs_security|보호]] 발동 시점, 안전 정지 |

여기서 합격 기준은 "살아남았다"만으로 부족하다. [[001_dikw_pyramid|데이터]] 훼손 없이 살아남았는지, [[658_ir_recovery|복구]] 중 중복 처리나 순서 뒤바뀜이 없는지, 감지 알람이 실제 운영자가 이해할 수 있는 형태로 남았는지까지 [[396_validation|확인]]해야 한다. 즉 Fault Injection의 평가는 **[[452_availability|가용성]] + [[003_integrity|무결성]] + [[111_observability_metrics_logs_traces|관측 가능성]]**을 함께 본다.

- **📢 섹션 요약 비유**: 이 테스트는 복싱 선수가 샌드백만 치는 것이 아니라, 코치가 일부러 균형을 흔들고 잽을 날려 봤을 때 자세를 잃지 않는지 [[396_validation|확인]]하는 스파링과 같다.

---

## Ⅲ. 비교 및 연결

[[352_defect_definition|결함]] 주입 테스트는 다른 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] [[395_verification_process_review|검증]] 기법과 겹쳐 보이지만 목적이 다르다. **[[447_stress_test|스트레스 테스트]]**는 한계 부하를 찾고, **[[758_burn_in_test|번인]] 테스트 ([[758_burn_in_test|Burn-In]] Test)** 는 [[459_quic_fec_forward_error_correction|초기]] 불량을 조기에 드러내며, **[[751_chaos_engineering|카오스 엔지니어링]] ([[751_chaos_engineering|Chaos Engineering]])** 은 운영 환경 수준에서 시스템 전체의 회복탄력성을 본다. 반면 Fault Injection은 특정 fault model에 대해 **예상한 [[571_protection_vs_security|보호]] 메커니즘이 정확히 동작하는가**를 더 촘촘히 [[395_verification_process_review|검증]]한다.

| 기법 | 질문 | 주된 장소 | 초점 |
| :--- | :--- | :--- | :--- |
| [[447_stress_test|스트레스 테스트]] | 어디서 [[282_performance_tactics|성능]] 한계가 무너지는가 | 실험실·[[282_performance_tactics|성능]] 환경 | [[139_throughput|처리량]], [[015_지연_데이터_관점|지연]], 병목 |
| [[758_burn_in_test|번인]] 테스트 | [[459_quic_fec_forward_error_correction|초기]] 불량이 조기에 드러나는가 | 제조·검수 | 조기 고장 선별 |
| [[352_defect_definition|결함]] 주입 테스트 | 특정 고장에 [[571_protection_vs_security|보호]] 경로가 동작하는가 | 실험실·스테이징·제한적 운영 | 감지, 격리, [[658_ir_recovery|복구]] |
| [[751_chaos_engineering|카오스 엔지니어링]] | 실제 [[090_service_kubernetes_network_load_balancing|서비스]]가 넓은 장애를 견디는가 | 운영·운영 유사 환경 | 회복탄력성, 운영 문화 |

또한 Fault Injection은 **[[752_fmea|FMEA]] (Failure Mode and Effects Analysis)** 와 자연스럽게 이어진다. FMEA가 "어떤 고장이 위험한가"를 문서로 뽑아내면, Fault Injection은 그중 중요한 고장을 실제로 넣어 봐서 가설을 [[395_verification_process_review|검증]]한다. 다시 말해 FMEA가 설계 우선순위를 정한다면, Fault Injection은 **설계가 약속한 [[571_protection_vs_security|보호]] 수준을 실험으로 증명**한다.

한편 하드웨어 무정전 아키텍처에서도 Fault Injection은 필수다. 전원 모듈을 뽑아 보고, 링크를 끊어 보고, 메모리 오류를 강제로 넣어 봐야 진짜로 무중단인지 알 수 있다. 설계 문서만으로는 예외 경로의 타이밍 문제와 운영 자동화 버그를 발견하기 어렵기 때문이다.

- **📢 섹션 요약 비유**: FMEA가 병원 문진표라면, [[352_defect_definition|결함]] 주입 테스트는 의사가 실제로 무릎을 톡 쳐서 반사 신경이 살아 있는지 [[396_validation|확인]]하는 진찰이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[352_defect_definition|결함]] 주입을 "무섭지만 언젠가 해야 하는 행사"가 아니라, 설계와 운영의 일부로 반복해야 한다. 특히 [[658_ir_recovery|복구]] 목표 시간 (Mean Time To Repair, [[451_mttr|MTTR]]), 경보 [[015_지연_데이터_관점|지연]], [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] 보장을 수치화해 두지 않으면 실험 결과가 남지 않는다. 예를 들어 메모리 단일 [[073_bit|비트]] 오류는 즉시 교정 후 [[090_service_kubernetes_network_load_balancing|서비스]] 영향 0, [[356_pcie|PCIe]] 링크 재훈련은 100ms 이하, 이중 컨트롤러 전환은 1초 이하처럼 **명시적 기대치**를 두는 것이 좋다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 정상 상태를 설명하는 기준 지표가 있는가? (예: 주문 성공률, [[015_지연_데이터_관점|지연]]시간, [[001_dikw_pyramid|데이터]] [[112_checksum|체크섬]])
2. 주입 [[352_defect_definition|결함]]이 실제 필드 고장과 연결되는가?
3. 주입 후 자동 중지 조건과 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 경로가 있는가?
4. [[568_logs_distributed_logging_elk_fluentd|로그]], 센서, 추적 정보가 원인 분석에 충분한가?
5. [[658_ir_recovery|복구]] 성공뿐 아니라 [[001_dikw_pyramid|데이터]] 정확성과 경보 품질까지 평가하는가?

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- **오라클 없는 파괴 실험**: 무엇이 성공인지 정의하지 않고 장비만 꺼 보는 경우다.
- **현장과 무관한 fault model**: 실제로는 [[001_voltage|전압]] 강하가 문제인데 의미 없는 랜덤 [[073_bit|비트]] 뒤집기만 반복하면 도움이 작다.
- **[[658_ir_recovery|복구]] 시간만 보고 [[003_integrity|무결성]]을 놓침**: [[090_service_kubernetes_network_load_balancing|서비스]]는 다시 떴지만 [[001_dikw_pyramid|데이터]]가 중복 기록되거나 손상되면 실패다.

기술사 답안에서는 "[[352_defect_definition|결함]]을 넣는다"보다 **어떤 계층에 어떤 [[352_defect_definition|결함]]을 넣고, 어떤 지표로 합격을 판단하며, 그 결과를 설계 개선으로 어떻게 환류하는가**까지 보여 주는 것이 중요하다. 결국 Fault Injection은 테스트가 아니라 **[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] [[005_feedback_loop|피드백 루프]]**다.

- **📢 섹션 요약 비유**: 자동차 안전 [[395_verification_process_review|검증]]은 시동이 걸리는지만 보는 것이 아니라, 충돌 후 에어백이 몇 ms 안에 터지고 탑승자가 실제로 [[571_protection_vs_security|보호]]되는지까지 보는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

[[352_defect_definition|결함]] 주입 테스트의 가장 큰 효과는 "언젠가 고장 날 것"을 전제로 설계를 다듬게 만든다는 점이다. 실제 필드에서 처음 겪을 장애를 실험실에서 먼저 겪게 해 주므로, 잠복 오류를 조기에 발견하고 [[658_ir_recovery|복구]] 경로를 자동화하며 운영자 대응 문서를 현실화할 수 있다. 특히 안전성 [[303_authentication_authorization_patterns|인증]], 금융 인프라, 서버 플랫폼 [[395_verification_process_review|검증]]처럼 **예외 경로 증빙**이 필요한 분야에서 가치가 크다.

물론 모든 위험을 이 기법 하나로 다 [[395_verification_process_review|검증]]할 수는 없다. 주입하지 않은 고장 모드는 여전히 남고, 실험 환경이 실제 현장의 전기적·열적·인적 요인을 완벽히 재현하지 못할 수도 있다. 따라서 Fault Injection은 [[752_fmea|FMEA]], [[758_burn_in_test|번인]] 테스트, [[751_chaos_engineering|카오스 엔지니어링]], 현장 텔레메트리와 함께 사용해야 한다.

앞으로는 [[126_digital_twin_concept|디지털 트윈]] ([[126_digital_twin_concept|Digital Twin]]) 기반 시뮬레이션과 자동화된 [[352_defect_definition|결함]] 캠페인이 늘어나겠지만, 핵심은 변하지 않는다. **중요한 장애를 미리 넣어 보고, 감지·격리·[[658_ir_recovery|복구]]의 약속을 실험으로 증명하는 것**이 [[352_defect_definition|결함]] 주입 테스트의 본질이다.

- **📢 섹션 요약 비유**: 시험 전 예상 문제를 일부러 틀려 보며 어디서 자주 실수하는지 찾는 학생처럼, 컴퓨터도 일부러 문제를 만들어 봐야 진짜 약한 부분을 빨리 고칠 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 단일 사건 업셋 (Single Event Upset, SEU) | 메모리·[[057_register|레지스터]] [[073_bit|비트]] 반전처럼 대표적인 주입 대상 fault model이다. |
| [[554_ecc_circuit|ECC]] 메모리 | [[073_bit|비트]] 오류 주입 시 교정·검출 경로가 제대로 작동하는지 [[396_validation|확인]]하는 핵심 대상이다. |
| [[716_pcie_aer|PCIe AER]] ([[716_pcie_aer|Advanced Error Reporting]]) | 링크·전송 오류를 보고하고 [[658_ir_recovery|복구]] 경로를 유도하는 대표적 관측 채널이다. |
| 감시 타이머 ([[461_watchdog_timer|Watchdog Timer]]) | 응답 정지 상태를 감지해 리셋·격리를 수행하는 [[571_protection_vs_security|보호]] 장치다. |
| [[752_fmea|FMEA]] | 어떤 고장 모드를 우선 주입할지 결정하는 설계 입력 자료다. |
| [[751_chaos_engineering|카오스 엔지니어링]] | Fault Injection을 더 넓은 운영 환경 실험으로 확장한 회복탄력성 접근이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
현장 장애 이력 · FMEA
    │
    ▼
고장 모델 정의
: bit flip · link loss · power drop · timeout
    │
    ▼
결함 주입 테스트 (Fault Injection Test)
: inject → detect → recover → verify
    │
    ├──▶ 설계 보강
    │     : ECC · watchdog · redundancy · retry policy
    │
    └──▶ 운영 확장
          : chaos engineering · game day · resilience drill
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[352_defect_definition|결함]] 주입 테스트는 장난감 자동차가 고장 났을 때도 잘 굴러가는지 일부러 바퀴를 살짝 흔들어 보는 거예요.
2. 그냥 "튼튼하겠지" 하고 믿는 대신, 진짜로 시험해 봐야 어디가 약한지 알 수 있어요.
3. 그래서 컴퓨터도 일부러 작은 문제를 넣어 보고, 스스로 잘 고치는지 [[396_validation|확인]]한답니다.
