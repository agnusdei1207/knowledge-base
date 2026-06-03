+++
weight = 781
title = "781. FIB (Focused Ion Beam) 수정"
date = "2026-05-08"
[extra]
categories = "studynote-computer-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FIB (Focused Ion Beam) 수정은 패키지를 벗겨 노출한 다이 위에서 이온 빔으로 금속선과 절연막을 국소 가공해, 기존 회로를 끊거나 새로운 우회선을 만드는 침습적 회로 편집이다.
> 2. **가치**: 단순 관찰이 아니라 보안 센서 무력화, [[303_authentication_authorization_patterns|인증]] 분기 우회, [[554_fuse_filesystem_in_userspace|fuse]] 상태 수정처럼 칩의 **원래 [[369_logic_bomb|논리]] 자체**를 바꿀 수 있으므로, 비용이 높아도 하드웨어 신뢰 모델을 근본부터 흔든다.
> 3. **판단 포인트**: FIB를 막는 핵심은 완전 차단이 아니라, 상·하면 동시 [[571_protection_vs_security|보호]], 동적 [[389_mesh_topology|메시]], [[136_variance|분산]] [[395_verification_process_review|검증]], 짧은 수명 키 구조를 통해 "한 지점 수정만으로는 성공할 수 없는 칩"으로 만드는 것이다.

---

## Ⅰ. 개요 및 필요성

FIB (Focused Ion Beam) 수정은 원래 [[009_semiconductor|반도체]] 고장 분석과 마스크 수정 [[395_verification_process_review|검증]]에 쓰이던 장비를, 공격자가 보안 칩 편집 도구로 전용하는 기법이다. [[782_decapping_probing|디캡핑]] ([[782_decapping_probing|Decapping]])으로 다이를 노출한 뒤 특정 금속 배선이나 절연막을 이온 빔으로 깎아 내고, 필요하면 전도성 물질을 증착해 우회 배선을 만든다. 즉 "칩을 읽는 공격"이 아니라 "칩이 동작하는 방식 자체를 다시 쓰는 공격"이다.

이 개념이 중요한 이유는 많은 보안 설계가 여전히 "제조가 끝난 회로는 바꿀 수 없다"는 가정을 깔고 있기 때문이다. 하지만 스마트카드, 보안 [[130_microcontroller|마이크로컨트롤러]], [[475_hsm|하드웨어 보안 모듈]] ([[157_hsm_hardware_security_module|Hardware Security Module]], [[475_hsm|HSM]]) 같은 고가치 칩에서는, 공격자가 충분한 자금과 장비를 투입하면 특정 센서 선만 끊거나 승인 경로만 우회해 [[571_protection_vs_security|보호]] 로직을 무력화할 수 있다. 따라서 FIB를 이해한다는 것은 단순한 장비 지식을 넘어서, **어떤 보안 [[369_logic_bomb|논리]]가 물리적으로 편집되기 쉬운가**를 판단하는 일과 같다.

또한 FIB는 [[782_decapping_probing|디캡핑]]/프로빙, [[029_reverse_engineering|역공학]], 배면 분석과 자연스럽게 연결된다. 먼저 내부 구조를 보고, 그다음 취약한 지점을 찾고, 마지막에 회로를 실제로 바꾸는 흐름이 이어지기 때문이다. 그래서 FIB는 침습형 물리 공격의 "종착지"라기보다, 분석과 편집이 결합된 최종 실행 수단으로 보는 편이 정확하다.

- **📢 섹션 요약 비유**: FIB 수정은 금고를 훔쳐 가는 일이 아니라, 금고 문 안쪽 톱니를 현미경 아래에서 다시 깎아 "원래는 안 열리던 문"을 열리게 만드는 초정밀 자물쇠 개조와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

FIB 회로 편집은 보통 시료 준비, 표적 정렬, 가공, 증착, [[395_verification_process_review|검증]]의 순서로 진행된다. 최신 장비는 주사전자현미경 (Scanning Electron Microscope, SEM) 관찰 기능과 FIB 가공 기능을 함께 갖춘 경우가 많아, 공격자는 보면서 깎고 깎으면서 다시 정렬할 수 있다. 이때 사용되는 이온 소스는 갈륨 (Gallium, [[169_evolutionary_algorithms|Ga]]) 액체 금속 이온 소스나 크세논 (Xenon, Xe) 플라즈마 계열이 대표적이며, 목적은 크게 두 가지다: **끊기**와 **이어 붙이기**다.

| 단계 | 공격 동작 | 기술 포인트 |
| :-- | :-- | :-- |
| 시료 준비 | [[782_decapping_probing|디캡핑]], 연마, 배면 박막화 | 원하는 층에 접근할 수 있어야 한다. |
| 표적 정렬 | SEM/FIB 영상으로 배선 위치 [[396_validation|확인]] | 보안 센서선, [[554_fuse_filesystem_in_userspace|fuse]], 상태 머신 입력을 정확히 찾아야 한다. |
| Milling | 이온 빔으로 금속/절연막 국소 제거 | 단선, via 개방, [[571_protection_vs_security|보호]]막 제거에 쓰인다. |
| Deposition | 전구체 [[024_gas|가스]] 기반 금속/절연물 증착 | 우회선 [[087_process_state_transition|생성]], 절연 [[658_ir_recovery|복구]], 강제 [[369_logic_bomb|논리]]값 주입에 쓰인다. |
| [[395_verification_process_review|검증]] | 전기적 연속성·[[369_logic_bomb|논리]] 동작 [[396_validation|확인]] | 편집 성공 후 전원을 다시 넣어야 한다. |

아래 그림은 FIB가 보안 경로를 어떻게 바꾸는지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                 FIB circuit edit: cut, isolate, then reroute              │
├────────────────────────────────────────────────────────────────────────────┤
│ Original design                                                           │
│   Tamper Sensor ───────────────▶ Tamper Controller ─────────▶ Zeroization │
│                                 │                                          │
│                                 └──────────────▶ Secure state machine     │
│                                                                            │
│ FIB operation                                                             │
│   1) Milling        : cut sensor net                                      │
│   2) Insulator fill : isolate opened area                                 │
│   3) Metal deposit  : add bypass net forcing "sensor_ok"                  │
│                                                                            │
│ Edited design                                                             │
│   Tamper Sensor ──X                                                       │
│   Forced logic value ───────────────────────────▶ Secure state machine    │
└────────────────────────────────────────────────────────────────────────────┘
```

핵심은 FIB가 단순히 표면을 뚫는 장비가 아니라, 배선을 다시 쓰는 장비라는 점이다. 공격자는 센서 출력을 끊고 정적 0/1 값을 주입하거나, 검사용 모드 진입선을 강제로 활성화하거나, [[554_fuse_filesystem_in_userspace|fuse]] 판독 경로를 우회해 칩이 잘못된 상태를 믿게 만들 수 있다. 다만 이런 작업은 매우 느리고 비용이 높으며, 이온 오염·열 영향·정렬 오차 때문에 실패 위험도 크다. 그래서 FIB는 "누구나 하는 공격"은 아니지만, 고가치 비밀을 다루는 칩이라면 반드시 가정해야 하는 위협이다.

- **📢 섹션 요약 비유**: 이 과정은 벽을 부수는 공사가 아니라, 이미 완성된 건물의 전기 배선을 한 가닥씩 끊고 새 점퍼선을 심어 경보등 대신 정상등이 켜지게 만드는 실내 전기 재배선과 같다.

---

## Ⅲ. 비교 및 연결

FIB 수정은 [[782_decapping_probing|디캡핑]]/프로빙과 자주 함께 언급되지만, 목적이 다르다. [[782_decapping_probing|디캡핑]]과 프로빙이 **관찰** 중심이라면, FIB는 **수정** 중심이다. [[029_reverse_engineering|역공학]]이 회로 구조를 복원하는 데 초점이 있다면, FIB는 굳이 전체 구조를 다 알지 못해도 특정 한 점만 편집해 공격 목표를 달성할 수 있다.

| 기법 | 주 목적 | 공격 결과 | 대표 한계 |
| :-- | :-- | :-- | :-- |
| [[782_decapping_probing|디캡핑]] ([[782_decapping_probing|Decapping]]) | 패키지 제거 | 다이 노출 | 그 자체만으로는 동작 변경이 어렵다 |
| 프로빙 (Probing) | 내부 [[130_signal|신호]] 관찰 | [[344_bus|버스]]/노드 파형 획득 | 접촉 가능한 지점이 필요하다 |
| FIB 수정 | 내부 회로 편집 | 센서 우회, logic patch, [[554_fuse_filesystem_in_userspace|fuse]] 수정 | 매우 고가·저속이며 숙련도 요구가 크다 |
| [[029_reverse_engineering|역공학]] ([[780_reverse_engineering|Reverse Engineering]]) | 구조 복원 | 회로도·지적 재산 분석 | 시간과 분석량이 매우 크다 |

또 하나의 중요한 비교는 전면 (Frontside) 접근과 배면 (Backside) 접근이다. 전면 FIB는 상단 금속 배선을 직접 겨냥하기 좋지만, [[783_anti_tamper_mesh|안티 탬퍼]] ([[783_anti_tamper_mesh|Anti-Tamper]]) [[389_mesh_topology|메시]]가 촘촘하면 방해를 받는다. 반면 배면 FIB는 실리콘 기판을 얇게 연마한 뒤 뒤쪽에서 접근해 상단 [[389_mesh_topology|메시]]를 우회하려는 전략으로 이어질 수 있다. 그래서 상단 [[389_mesh_topology|메시]]만 믿는 설계는 FIB 위협을 절반만 본 셈이다.

이 연결 고리 때문에 FIB 대응은 결국 [[783_anti_tamper_mesh|안티 탬퍼]] [[389_mesh_topology|메시]], 센서 융합, [[784_zeroization_circuit|제로화]] ([[784_zeroization_circuit|Zeroization]]) 회로와 함께 설계되어야 한다. 단일 센서선 하나만 [[571_protection_vs_security|보호]]하는 구조는 편집 대상이 너무 명확하고, zeroize가 메인 제어기 하나에 종속돼 있으면 그 한 점만 우회해도 전체 방어가 붕괴한다.

- **📢 섹션 요약 비유**: [[782_decapping_probing|디캡핑]]이 지붕을 여는 일이고, 프로빙이 안을 들여다보는 일이라면, FIB는 집 안 전선함을 직접 뜯어 경보선과 현관 전자락을 다시 연결하는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 FIB를 어느 정도까지 가정해야 하는지는 자산 가치와 공격자 모델에 따라 달라진다. 일반 소비자 기기 전체에 국가급 침습 공격을 동일하게 적용할 필요는 없지만, [[475_hsm|HSM]], 결제용 보안 소자, 자동차 [[487_root_of_trust|루트 오브 트러스트]], 국방·[[303_authentication_authorization_patterns|인증]] 장비는 FIB 가능성을 전제로 설계해야 한다. 특히 "한 개의 [[043_comparator|비교기]] 결과", "한 줄의 tamper enable", "한 개의 test mode strap"에 시스템 운명이 걸린 구조는 매우 위험하다.

### 설계 판단 [[435_checklist_based_testing|체크리스트]]

1. 보안 상태를 결정하는 [[130_signal|신호]]가 한두 개의 단일 배선으로 집중되어 있지 않은가?
2. 상단 [[389_mesh_topology|메시]]뿐 아니라 배면 박막화·배면 정렬 공격까지 고려한 센서가 있는가?
3. 정적 연속성 검사 대신 의사난수 기반 동적 challenge-response [[389_mesh_topology|메시]]를 쓰는가?
4. 키 방출 승인, 디버그 허용, 부트 신뢰 판단이 여러 블록에서 교차 [[395_verification_process_review|검증]]되는가?
5. 장기 비밀을 고정 저장하기보다 물리적 [[016_replication_factor|복제]] 방지 기능 ([[788_sram_puf|Physical Unclonable Function]], [[485_puf|PUF]]) 기반 파생이나 짧은 수명 [[140_session_key|세션 키]] 구조를 사용할 수 있는가?

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- **단일 tamper 선 의존**: 한 가닥만 끊거나 고정값을 주입하면 방어가 사라진다.
- **정적 [[389_mesh_topology|메시]]만 사용**: 공격자가 continuity를 흉내 내기 쉬워진다.
- **[[784_zeroization_circuit|제로화]] 회로의 CPU 종속**: 메인 펌웨어를 우회하면 소거도 함께 멈춘다.
- **전면 [[571_protection_vs_security|보호]]만 강조**: 배면 FIB·배면 프로빙을 고려하지 않으면 [[571_protection_vs_security|보호]] 구멍이 남는다.

결국 기술사 관점에서 FIB 대응은 "절대 못 뚫게 하겠다"가 아니라, **단일 편집으로는 아무 보안 [[065_state_diagram|상태도]] 바꾸지 못하게 설계하고, 공격 시간이 길어질수록 탐지와 소거 가능성이 커지게 만드는 것**으로 정리하는 편이 좋다.

- **📢 섹션 요약 비유**: 좋은 FIB 대응 설계는 전등 [[238_switch_operation_principles|스위치]] 하나를 끊는다고 은행 전체 경비가 멈추지 않게 만드는 건물 배선과 같다. 한 줄을 잘라도 다른 감지기와 예비 회로가 즉시 이상을 알아차려야 한다.

---

## Ⅴ. 기대효과 및 결론

FIB 수정 위협을 반영한 보안 칩 설계는 "하드웨어는 제조 후 불변"이라는 안일한 가정을 버리게 만든다. 그 결과 센서 경로를 [[136_variance|분산]]하고, 상·하면 [[571_protection_vs_security|보호]]를 결합하고, 장기 키를 고정 저장하지 않는 방향으로 설계 수준이 높아진다. 즉 FIB 대응은 특정 장비 대응책이면서 동시에, 물리 침습 전반에 대한 설계 성숙도를 끌어올리는 기준이 된다.

물론 한계도 분명하다. 고급 장비를 가진 공격자를 완전히 막는 것은 현실적으로 어렵고, [[389_mesh_topology|메시]]·센서·[[136_variance|분산]] [[395_verification_process_review|검증]]은 면적, 전력, 테스트 복잡도를 증가시킨다. 앞으로는 배면 센서, 3차원 적층 [[571_protection_vs_security|보호]]층, [[485_puf|PUF]] 기반 비고정 키 구조, 더 촘촘한 sensor fusion이 중요해질 가능성이 크다. 따라서 FIB 수정은 "칩 위의 나노미터급 전기 배선 재시공"으로 기억하면 가장 정확하다.

- **📢 섹션 요약 비유**: 결국 FIB 대응은 문을 더 두껍게 만드는 일이 아니라, 집 안 배선을 미로처럼 나누고 곳곳에 비상 차단기를 넣어 외과수술급 침입에도 집 전체가 바로 경계 태세로 전환되게 만드는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[782_decapping_probing|디캡핑]] ([[782_decapping_probing|Decapping]]) 및 프로빙 (Probing) | FIB 수정이 시작되기 전에 다이를 노출하고 표적 노드를 찾는 선행 단계다. |
| [[783_anti_tamper_mesh|안티 탬퍼]] ([[783_anti_tamper_mesh|Anti-Tamper]]) [[389_mesh_topology|메시]]/쉴드 | FIB가 가장 먼저 우회하거나 절단하려는 상단 방어층이다. |
| [[784_zeroization_circuit|제로화]] ([[784_zeroization_circuit|Zeroization]]) 회로 | FIB가 무력화하려는 대표 목표이자, 침습 공격에 대한 최종 대응 장치다. |
| 배면 분석 (Backside Analysis) | 상단 [[389_mesh_topology|메시]]를 피하려고 실리콘 뒤쪽에서 접근하는 흐름과 연결된다. |
| 물리적 [[016_replication_factor|복제]] 방지 기능 ([[788_sram_puf|Physical Unclonable Function]], [[485_puf|PUF]]) | 고정 저장된 비밀을 줄여 FIB 편집 후 얻는 이득 자체를 낮추는 전략이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
패키지 제거 · 시료 준비
        │
        ▼
디캡핑 (Decapping) · 표적 노드 식별
        │
        ▼
FIB (Focused Ion Beam) milling
        │
        ▼
회로 절단 · via 개방 · 금속 증착 우회
        │
        ▼
센서 무력화 · fuse 수정 · logic patch
        │
        ▼
동적 메시 · 배면 보호 · 분산 zeroization 대응
```

이 흐름은 "노출 → [[655_ir_detection_analysis|식별]] → 편집 → 우회 → 복합 방어"로 이어지는 침습 공격과 대응의 진화를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. FIB 수정은 완성된 장난감 로봇 안의 전깃줄을 엄청 작은 바늘 공구로 잘라서 새 줄로 바꿔 끼우는 일이에요.
2. 그래서 원래는 "열리면 안 되는 문"도 로봇이 속아서 열어 버릴 수 있어요.
3. 똑똑한 로봇은 전깃줄을 한 군데에만 두지 않고, 여기저기 나눠 놓아서 한 줄만 잘라도 바로 이상하다고 알아차린답니다.
