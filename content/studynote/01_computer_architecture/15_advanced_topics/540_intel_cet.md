---
title: 540. 버퍼 오버플로우 하드웨어 방어 (Intel CET 등)
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[591_buffer_overflow|버퍼 오버플로우]] 하드웨어 방어는 메모리 오염이 발생해도 리턴 주소와 간접 분기 목적지가 임의 값으로 바뀌지 못하도록 CPU (Central Processing Unit)가 실행 흐름을 직접 [[395_verification_process_review|검증]]하는 기술이다.
> 2. **가치**: Intel CET (Control-flow Enforcement Technology)의 shadow [[057_stack|stack]], IBT ([[177_indirect_addressing|Indirect]] Branch Tracking), ARM의 PAC ([[542_pointer_authentication|Pointer Authentication]] [[082_process_memory_structure|Code]])·BTI (Branch Target [[289_identification_flags_fragmentation_offset|Identification]])는 [[596_return_oriented_programming|ROP]] ([[596_return_oriented_programming|Return-Oriented Programming]])·[[346_jop|JOP]] ([[346_jop|Jump-Oriented Programming]]) 공격을 "실행"이 아니라 "즉시 fault"로 바꾼다.
> 3. **판단 포인트**: 이런 [[571_protection_vs_security|보호]]는 강력하지만 [[529_memory_safety_rust_go|메모리 안전성]] 전체를 대신하지는 않으며, [[001_operating_system_purpose|운영체제]]·컴파일러·런타임·[[568_jit_access|JIT]] ([[568_jit_access|Just-In-Time]]) [[344_compatibility_usability|호환성]]까지 끝단 지원이 있을 때만 실효성이 생긴다.

---

## Ⅰ. 개요 및 필요성

[[591_buffer_overflow|버퍼 오버플로우]] 하드웨어 방어는 함수 호출과 복귀, 간접 점프, 간접 호출이 반드시 정상적인 제어 흐름 안에서만 일어나도록 프로세서가 직접 감시하는 기술이다. 전통적인 [[591_buffer_overflow|버퍼 오버플로우]] ([[591_buffer_overflow|Buffer Overflow]])는 [[057_stack|스택]]이나 힙의 인접 메모리를 덮어쓰며, 그 결과 리턴 주소나 함수 포인터가 오염되면 공격자는 프로그램의 실행 경로를 빼앗을 수 있다. 문제는 이 공격이 "코드를 새로 심는" 방식이 아니라, 기존 코드 조각을 재배열하는 [[596_return_oriented_programming|ROP]]·[[346_jop|JOP]] 형태로 발전하면서 기존 소프트웨어 방어를 자주 우회해 왔다는 점이다.

[[339_stack_canary|스택 카나리]], [[336_dep|DEP]] ([[336_dep|Data Execution Prevention]]), [[374_aslr|ASLR]] (Address Space Layout Randomization)은 모두 중요한 방어선이지만, 각각 [[571_protection_vs_security|보호]] 범위가 다르다. [[339_stack_canary|스택 카나리]]는 인접 overwrite를 일부 잡지만 모든 경로를 막지는 못하고, DEP는 실행 금지 [[286_page_frame|페이지]]를 강제하지만 이미 존재하는 코드 조각 사용은 막지 못한다. ASLR은 주소 예측을 어렵게 하지만 정보 유출이 동반되면 약해질 수 있다. 그래서 현대 보안 아키텍처는 "메모리 오염이 있어도 제어권 탈취까지는 못 가게 하자"는 방향으로 하드웨어 [[395_verification_process_review|검증]]을 추가했다.

- **📢 섹션 요약 비유**: [[591_buffer_overflow|버퍼 오버플로우]] 하드웨어 방어는 누군가 대본 일부를 몰래 고쳐도, 배우가 무대에 오르기 전에 감독이 공식 대본과 실제 대본을 대조해 틀린 장면으로는 못 가게 막는 장치와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

하드웨어 방어의 핵심은 두 축이다. 첫째는 **복귀 주소 [[003_integrity|무결성]]**이다. Intel CET는 shadow stack에 리턴 주소를 별도로 저장하고, 함수 복귀 시 일반 [[057_stack|스택]] 값과 비교해 다르면 예외를 발생시킨다. ARM 계열은 PAC로 리턴 주소에 서명을 붙여, 변조된 주소가 유효한 포인터처럼 보이지 못하게 만든다. 둘째는 **간접 분기 목적지 [[395_verification_process_review|검증]]**이다. CET의 IBT와 ARM의 BTI는 간접 분기가 지정된 landing pad로만 들어가게 만들어, 코드 중간의 gadget으로 뛰어드는 공격을 어렵게 한다.

| 방어 축 | 대표 기술 | 막으려는 공격 | 시스템 요구 사항 |
| :--- | :--- | :--- | :--- |
| 복귀 주소 [[571_protection_vs_security|보호]] | Shadow [[057_stack|Stack]], PAC | [[596_return_oriented_programming|ROP]] | 컴파일러 prologue/epilogue, OS [[033_context|context]] save |
| 간접 분기 목적지 [[395_verification_process_review|검증]] | IBT, BTI | JOP와 코드 중간 진입 우회 | 합법적 landing pad 삽입, loader 지원 |
| 특권 상태 관리 | shadow [[057_stack|stack]] pointer, enable [[086_fenwick_tree|bit]], fault handler | [[571_protection_vs_security|보호]] 상태 우회 시도 | [[079_kube_scheduler_pod_placement|스케줄러]], [[130_signal|signal]]/unwind, 예외 처리 연동 |

이 그림은 [[591_buffer_overflow|버퍼 오버플로우]] 이후에도 제어권 탈취를 막는 하드웨어 [[395_verification_process_review|검증]] 과정을 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 하드웨어 버퍼 오버플로우 방어의 이중 검증                                 │
├────────────────────────────────────────────────────────────────────────────┤
│ CALL foo                                                                   │
│   │                                                                        │
│   ├─ 일반 스택          : return address 저장                              │
│   └─ 보호 영역          : shadow stack 저장 또는 PAC 서명 부착            │
│                                                                            │
│ RET / indirect JMP                                                         │
│   │                                                                        │
│   ├─ 주소 불일치 · 서명 불일치 ───────────────▶ fault                      │
│   └─ ENDBR / BTI landing pad 확인 ────────▶ 정상 target만 실행            │
│                                                                            │
│ 결과: overflow가 있어도 임의 gadget 체인으로 흐름 전환 어려움             │
└────────────────────────────────────────────────────────────────────────────┘
```

실제로는 프로세서만으로 끝나지 않는다. [[001_operating_system_purpose|운영체제]]는 [[092_thread_lwp|스레드]] 전환 때 shadow [[057_stack|stack]] pointer나 [[303_authentication_authorization_patterns|인증]] 상태를 저장·복원해야 하고, 컴파일러는 함수 진입점과 간접 분기 대상에 필요한 표식을 삽입해야 한다. 즉 이 기술은 "하드웨어 기능 하나 추가"가 아니라 **[[157_isa|ISA]] ([[157_isa|Instruction Set Architecture]]) + [[001_operating_system_purpose|운영체제]] + toolchain이 묶인 제어 흐름 [[003_integrity|무결성]] 체계**다.

- **📢 섹션 요약 비유**: 이 구조는 놀이공원 자유이용권과 출입 게이트를 함께 쓰는 것과 같다. 표가 진짜인지 확인하는 장치와, 아무 문으로나 못 들어가게 하는 게이트가 같이 있어야 안전하다.

---

## Ⅲ. 비교 및 연결

[[591_buffer_overflow|버퍼 오버플로우]] 하드웨어 방어는 기존 소프트웨어 방어를 대체하기보다 보완한다. DEP와 ASLR은 공격면을 줄이는 환경 방어이고, [[339_stack_canary|스택 카나리]]는 일부 overwrite를 감지하는 근접 방어다. 반면 CET와 PAC/BTI는 제어 흐름이 실제로 꺾이는 마지막 순간을 잡는다. 그래서 세 층은 경쟁 관계가 아니라, 서로 다른 단계에서 공격을 약화시키는 다층 방어로 봐야 한다.

| 기법 | 주된 [[571_protection_vs_security|보호]] 대상 | 강점 | 한계 |
| :--- | :--- | :--- | :--- |
| [[339_stack_canary|스택 카나리]] ([[339_stack_canary|Stack Canary]]) | [[057_stack|스택]] 인접 overwrite | 구현 단순, 기존 생태계 넓음 | non-contiguous overwrite, 정보 유출 우회 가능 |
| [[336_dep|DEP]] / NX (No-eXecute) | 실행 금지 [[286_page_frame|페이지]] | [[592_shellcode_injection|shellcode]] 실행 차단 | 기존 코드 재활용 공격은 못 막음 |
| [[374_aslr|ASLR]] | 주소 예측 | 공격 난이도 상승 | 주소 유출 시 약화 |
| CET / PAC / BTI | 복귀 주소·간접 분기 [[003_integrity|무결성]] | [[596_return_oriented_programming|ROP]]·[[346_jop|JOP]] 억제에 강력 | [[001_dikw_pyramid|data]]-only 공격, [[369_logic_bomb|논리]] 결함은 별도 |

이 주제는 소프트웨어 기반 CFI (Control-Flow [[003_integrity|Integrity]])와도 연결된다. 소프트웨어 CFI는 더 세밀한 [[164_policy|정책]]을 적용할 수 있지만, 검사 오버헤드와 적용 범위 제약이 있다. 하드웨어 CFI는 [[164_policy|정책]] 표현력은 상대적으로 단순할 수 있어도, 실행 경로의 마지막 문을 매우 빠르게 잠근다. 그래서 고보안 시스템은 소프트웨어 CFI, [[339_stack_canary|스택 카나리]], 하드웨어 shadow stack을 함께 쓰는 방향으로 간다.

또한 이 기술은 모든 메모리 취약점을 없애지 않는다. [[351_use_after_free|use-after-free]], [[001_dikw_pyramid|데이터]] 전용 공격, 권한 로직 버그는 제어 흐름을 정상처럼 유지한 채 악용될 수 있다. 따라서 "CET를 켰으니 [[591_buffer_overflow|버퍼 오버플로우]] 문제는 끝났다"는 식의 이해는 위험하다.

- **📢 섹션 요약 비유**: [[339_stack_canary|스택 카나리]]는 창문 깨짐 경보기이고, DEP는 건물에 불붙는 걸 막는 방염 처리이며, CET와 PAC는 건물 안 비밀문을 함부로 열 수 없게 하는 전자 잠금장치와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 CPU가 기능을 지원한다는 사실만으로 [[571_protection_vs_security|보호]]가 완성되지 않는다. [[001_operating_system_purpose|운영체제]]가 해당 비트를 활성화하고, 컴파일러가 적절한 명령과 표식을 삽입하고, 런타임과 예외 처리기가 shadow [[057_stack|stack]]·unwind 규칙을 이해해야 한다. 브라우저 [[568_jit_access|JIT]], hand-written assembly, 오래된 플러그인처럼 실행 코드를 직접 만들거나 비표준 프롤로그를 쓰는 소프트웨어는 여기서 가장 자주 문제를 일으킨다.

### 판단 [[435_checklist_based_testing|체크리스트]]

1. CPU, [[001_operating_system_purpose|운영체제]], 컴파일러, 링커, 로더가 end-to-end로 CET 또는 PAC/BTI를 지원하는가?
2. [[130_signal|signal]], exception, [[211_context_switch|context switch]], [[141_coroutine|coroutine]], JIT가 [[571_protection_vs_security|보호]] 상태를 깨지 않는가?
3. [[571_protection_vs_security|보호]]를 켜더라도 legacy module과 hand-written assembly가 정상적으로 landing pad를 제공하는가?
4. 하드웨어 [[571_protection_vs_security|보호]]를 켠 뒤에도 [[339_stack_canary|스택 카나리]], [[336_dep|DEP]], [[374_aslr|ASLR]] 같은 기존 방어를 유지하는가?
5. [[001_dikw_pyramid|데이터]] 전용 공격과 [[529_memory_safety_rust_go|메모리 안전성]] 문제를 별도 통제로 다루고 있는가?

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 일부 모듈만 [[571_protection_vs_security|보호]]하고 전체 프로그램이 안전해졌다고 가정하는 설계
- CET/PAC [[344_compatibility_usability|호환성]] 문제를 피하려고 [[571_protection_vs_security|보호]]를 전면 비활성화하는 운영
- 제어 흐름 [[571_protection_vs_security|보호]]를 [[529_memory_safety_rust_go|메모리 안전성]] 전체와 동일시해 use-after-free나 logic bug를 방치하는 판단

기술사 답안에서는 "Intel CET가 ROP를 막는다" 수준에서 끝내지 말고, **shadow [[057_stack|stack]] + 간접 분기 [[395_verification_process_review|검증]] + [[001_operating_system_purpose|운영체제]]/컴파일러 연동 + 남는 공격면**까지 함께 적는 것이 좋다. 그래야 왜 이 기술이 강력하면서도, 동시에 완전한 만능 방패는 아닌지가 균형 있게 드러난다.

- **📢 섹션 요약 비유**: 최신 전자도어락을 달아도 건물 관리 시스템이 문 열림 기록을 못 따라가면 혼란이 생기듯, 하드웨어 [[571_protection_vs_security|보호]]도 [[001_operating_system_purpose|운영체제]]와 도구 체인이 함께 맞물려야 제대로 작동한다.

---

## Ⅴ. 기대효과 및 결론

[[591_buffer_overflow|버퍼 오버플로우]] 하드웨어 방어가 잘 적용되면, 메모리 오염이 곧바로 임의 코드 실행이나 gadget 체인 실행으로 이어질 가능성이 크게 낮아진다. 특히 브라우저, [[022_kernel_role|커널]], 하이퍼바이저처럼 공격 표면이 넓고 제어 흐름 탈취의 파급이 큰 영역에서 효과가 크다. 더 중요한 점은 이 [[571_protection_vs_security|보호]]가 런타임에서 매우 낮은 오버헤드로 작동한다는 것이다.

그러나 한계도 분명하다. 제어 흐름만 [[571_protection_vs_security|보호]]해도 [[001_dikw_pyramid|데이터]] 위조, 권한 [[395_verification_process_review|검증]] 누락, 객체 수명 오류 같은 문제는 여전히 남는다. 앞으로는 shadow stack과 pointer authentication에 더해 MTE (Memory Tagging Extension), capability 기반 주소 [[395_verification_process_review|검증]] 같은 기술이 결합되며 "제어 흐름 [[571_protection_vs_security|보호]]"에서 "메모리 접근 자체 [[571_protection_vs_security|보호]]"로 범위가 넓어질 가능성이 크다.

결국 이 주제는 **[[591_buffer_overflow|버퍼 오버플로우]]를 없애는 기술**이 아니라, **[[591_buffer_overflow|버퍼 오버플로우]]가 나더라도 제어권을 빼앗기지 않게 만드는 하드웨어 안전벨트**로 기억하는 것이 정확하다. Intel CET는 그 대표 사례이고, PAC/BTI는 같은 방향의 다른 구현이다.

- **📢 섹션 요약 비유**: 이 기술은 사고를 완전히 없애는 마법이 아니라, 사고가 나더라도 운전대를 빼앗기지 않게 해 주는 안전벨트와 에어백의 조합에 가깝다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[591_buffer_overflow|Buffer Overflow]] | 하드웨어 제어 흐름 [[571_protection_vs_security|보호]]가 겨냥하는 대표 메모리 오염 출발점이다. |
| Shadow [[057_stack|Stack]] | 일반 [[057_stack|스택]]과 별도로 복귀 주소를 보관해 ROP를 억제한다. |
| IBT ([[177_indirect_addressing|Indirect]] Branch Tracking) | 간접 분기가 합법적 진입점으로만 들어가게 강제하는 CET 구성요소다. |
| PAC ([[542_pointer_authentication|Pointer Authentication]] [[082_process_memory_structure|Code]]) | 포인터에 서명을 붙여 변조된 복귀 주소와 함수 포인터를 걸러낸다. |
| [[339_stack_canary|스택 카나리]] ([[339_stack_canary|Stack Canary]]) | 하드웨어 [[571_protection_vs_security|보호]]와 함께 쓰이는 전통적 overwrite 탐지 기법이다. |
| CFI (Control-Flow [[003_integrity|Integrity]]) | CET와 PAC/BTI가 구현하는 상위 보안 목표다. |

### 📈 관련 키워드 및 발전 흐름도

```text
스택 overwrite 기반 코드 실행 공격
        │
        ▼
스택 카나리 · DEP · ASLR
        │
        ▼
ROP (Return-Oriented Programming) · JOP (Jump-Oriented Programming) 등장
        │
        ▼
소프트웨어 CFI (Control-Flow Integrity)
        │
        ▼
Intel CET · ARM PAC/BTI
        │
        ▼
Memory Tagging · capability 기반 메모리 보호 확장
```

이 흐름은 단순 overwrite 탐지에서 출발해, 점차 제어 흐름과 메모리 접근 자체를 하드웨어 수준에서 [[395_verification_process_review|검증]]하는 방향으로 방어가 진화하는 모습을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 누가 몰래 길안내 표지판을 바꿔도, 컴퓨터는 "원래 가야 할 길"을 따로 기억하고 있어요.
2. 그래서 나쁜 사람이 엉뚱한 길로 보내려고 하면, "여긴 가면 안 돼!" 하고 바로 멈춰요.
3. 하지만 길을 잘 지키는 것과 방이 어지럽지 않은 것은 다른 문제라서, 청소도 여전히 잘해야 해요.
