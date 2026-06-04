---
title: "147. 황의 법칙 (Hwang's Law)"
date: "2026-04-19"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 황의 법칙(Hwang's Law)은 전원이 꺼져도 데이터가 보존되는 <strong>NAND <a href="/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/">플래시 메모리</a>(NAND <a href="/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/">Flash Memory</a>)의 집적도가 1년마다 2배씩 증가</strong>한다는 관찰 모델로, 무어의 법칙(Moore's Law, 2년 주기)보다 두 배 빠른 메모리 스토리지 진화를 예측했다.
> 2. **가치**: 고용량 낸드 플래시를 경제적으로 공급함으로써 MP3, 디지털카메라, 스마트폰, [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)([Solid State Drive](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)) 혁명을 촉발한 <strong>모바일·스토리지 경제학의 핵심 성장 공식</strong>이다.
> 3. **판단 포인트**: 평면(2D) 미세 공정이 10nm 이하에서 물리적 한계에 도달하자, 칩을 수직으로 쌓는 **3D V-NAND(Vertical NAND)** 구조로 진화하면서 법칙의 연장선이 형성됐다.

---

## Ⅰ. 개요 및 필요성

황의 법칙은 2002년 삼성전자 황창규 사장이 국제고체회로학회(ISSCC, International [Solid](/studynote/04_software_engineering/04_testing_quality/242_solid_object_oriented_design_principles/)-[State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Circuits Conference)에서 발표한 경험적 예측으로, "낸드 [플래시 메모리](/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/)의 집적도는 매년 2배씩 증가한다"는 명제다.

1990년대 후반, [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)·모바일 시장이 텍스트를 넘어 멀티미디어(사진·음악·영상)로 전환되면서 저장 공간 수요가 폭발적으로 증가했다. [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/)(Hard Disk Drive)는 충격에 약하고 부피가 커서 소형 기기에 적합하지 않았다. 낸드 플래시가 유일한 대안이었으나 GB당 단가가 너무 높았다. "집적도를 매년 2배로 높이지 않으면 수요를 따라잡을 수 없다"는 산업 압박이 황의 법칙을 낳았다.

무어의 법칙과의 핵심 차이는 다음과 같다.

| 구분 | 무어의 법칙 | 황의 법칙 |
|:---|:---|:---|
| 대상 | CPU [트랜지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/014_transistor/) 수 | [NAND Flash](/studynote/01_computer_architecture/06_memory_hierarchy_cache/257_nand_flash/) 집적도([비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)/칩) |
| 주기 | 약 2년 2배 | 약 1년 2배 |
| 메커니즘 | 공정 미세화(Scaling) | 셀 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)(MLC·TLC·QLC) + 공정 |
| 현황 | 2010년대 이후 둔화 | 2D 한계 -> 3D V-NAND 전환 |

- **📢 섹션 요약 비유**: 황의 법칙은 **'매년 서랍 깊이가 2배로 늘어나는 마법 책상'** 입니다. 서랍이 작아 사진 몇 장만 들어갔던 초창기에서, 매년 두 배씩 깊어지면서 수만 장의 고해상도 사진과 동영상을 통째로 쓸어 담을 수 있게 된 스토리지 성장의 기적입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

메모리 집적도를 높이는 두 가지 경로, 즉 <strong>공정 미세화</strong>와 <strong>셀 <a href="/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/">다중화</a>(Multi-Level Cell)</strong> 가 황의 법칙을 구동한 핵심 메커니즘이다.

### 1. 셀 레벨 코딩 구조

```text
전압 레벨 수에 따른 1셀당 비트 수 및 트레이드오프

  SLC (Single Level Cell)   MLC (Multi Level Cell)   TLC/QLC
  +--------------------+    +----------------------+  +----------------+
  |  전압 2단계 -> 1bit  |    |  전압 4단계 -> 2bit   |  | 8/16단계 -> 3/4bit|
  |  수명: 100K P/E     |    |  수명:   10K P/E     |  | 수명: 1K~3K P/E |
  |  속도: 빠름          |    |  속도:   중간        |  | 속도: 느림      |
  |  용량: 적음          |    |  용량:   중간        |  | 용량: 최대      |
  +--------------------+    +----------------------+  +----------------+
```

같은 면적의 칩에 더 많은 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 구겨 넣기 위해 [전압](/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 레벨을 세분화한다. [SLC](/studynote/01_computer_architecture/15_advanced_topics/597_slc_caching/)(Single Level Cell)는 셀당 1비트, MLC(Multi Level Cell)는 2비트, TLC(Triple Level Cell)는 3비트, QLC(Quad Level Cell)는 4비트를 저장한다. [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수가 늘수록 용량은 늘지만, [전압](/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 판별 오류 가능성 증가로 속도·수명이 감소한다.

### 2. 2D -> 3D 전환: V-NAND의 등장

평면 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)은 20nm 이하에서 인접 셀 간 전기 누설([Crosstalk](/studynote/03_network/01_data_communication/030_누화_크로스토크/))과 제조 수율 문제로 한계를 맞았다. 해결책은 **수직 적층(3D V-NAND)** 이었다.

```text
2D NAND (평면)                      3D V-NAND (수직 적층)
+----------------------+            +------------------------+
| ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓  |            | Layer 256              |
| (셀이 미세할수록 간섭^) |            | Layer 255              |
|                      |            | ···                    |
|  한계: ~20nm 이하 붕괴 |            | Layer 2                |
+----------------------+            | Layer 1 (기판)          |
                                    +------------------------+
  동일 면적, 셀 간격 v                 수직 구멍(Channel Hole)으로
  -> 크로스톡(Crosstalk) ^            셀을 관통 연결 -> 간섭v, 수명^
```

삼성전자가 2013년 처음 상용화한 V-NAND는 셀을 24층부터 시작해 현재 200층 이상으로 쌓으며 집적도를 유지하고 있다. 황의 법칙의 수직 연장이다.

### 3. [FTL](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)([Flash Translation Layer](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/))과 수명 관리

낸드 플래시는 블록 단위 소거 후 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 단위 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)만 가능하다. 같은 블록이 반복 소거되면 산화막이 열화되어 수명이 소진된다. 이를 방지하기 위해 [FTL](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)([Flash Translation Layer](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/))이 <strong>웨어 레벨링(<a href="/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/">Wear Leveling</a>)</strong> 과 <strong><a href="/studynote/02_operating_system/06_memory_management/380_garbage_collection/">가비지 컬렉션</a>(<a href="/studynote/02_operating_system/06_memory_management/380_garbage_collection/">Garbage Collection</a>)</strong> 을 수행한다.

- **📢 섹션 요약 비유**: 2D 낸드는 **'단층 주택가에서 방을 성냥갑만 하게 쪼개는 것'** 입니다. 벽이 얇아져 옆방 소음(전기 간섭)이 심해집니다. 3D V-NAND는 방 크기는 넉넉하게 유지하고, 건물을 200층 마천루로 올려 수용량을 늘린 재건축의 기적입니다.

---

## Ⅲ. 비교 및 연결

### 황의 법칙 vs. 무어의 법칙 vs. 구스타프슨의 법칙

| 법칙 | 예측 대상 | 한계 요인 | [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) |
|:---|:---|:---|:---|
| 무어의 법칙(Moore's Law) | CPU [트랜지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/014_transistor/) 수 | 열벽([Power](/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Wall), 누설 [전류](/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/) | 2년 -> 3~4년으로 느려짐 |
| 황의 법칙(Hwang's Law) | NAND 집적도 | 2D 공정 한계 -> 3D로 전환 | 3D 적층으로 연명 중 |
| 구스타프슨의 법칙(Gustafson's Law) | [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 확장성 | 순차 병목([Serial](/studynote/03_network/01_data_communication/009_직렬_전송_vs_병렬_전송/) [Bottleneck](/studynote/02_operating_system/10_security/617_io_bottleneck/)) | 클라우드·[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시대에 유효 |
| 덴나드 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)([Dennard Scaling](/studynote/01_computer_architecture/03_architecture_basics_performance/148_dennard_scaling/)) | [트랜지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/014_transistor/) 전력 밀도 | 누설 [전류](/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/) 급증 | 2004년경 붕괴 |

### 연결 개념 흐름

낸드 플래시 수요 폭발 -> 황의 법칙 성립 -> 2D 미세화 한계 -> V-NAND 3D 적층 -> TLC·QLC 셀 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) -> 엔터프라이즈 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 티어링(Tiering) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 필요

- **📢 섹션 요약 비유**: 무어의 법칙이 **'두뇌(CPU)를 2년마다 똑똑하게 만드는 계획'** 이라면, 황의 법칙은 **'기억 서랍(NAND)을 1년마다 두 배 크게 만드는 계획'** 입니다. 둘 다 물리 한계에 부딪혔지만, 해결 방향은 달랐습니다 — CPU는 코어를 여럿으로 쪼갰고, NAND는 하늘을 향해 층을 쌓았습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 의사결정 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

| 상황 | 선택 | 이유 |
|:---|:---|:---|
| DB [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 스토리지 ([OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)) | [SLC](/studynote/01_computer_architecture/15_advanced_topics/597_slc_caching/)/MLC 고내구성 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) | 높은 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 반복 횟수(P/E Cycle) 필요 |
| 영상 스트리밍 콜드 스토리지 | QLC 대용량 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 빈도 낮고 용량·단가가 중요 |
| 엔터프라이즈 캐시 레이어 | [SLC](/studynote/01_computer_architecture/15_advanced_topics/597_slc_caching/) Optane/[SLC](/studynote/01_computer_architecture/15_advanced_topics/597_slc_caching/) 버퍼 | 극저지연(μs) + 고내구성 |
| [NAS](/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/) [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 스토리지 | TLC 대용량 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) or [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) | 균형적 비용·용량 |

### 핵심 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

**QLC SSD를 고쓰기 DB에 무지성 투입**: QLC는 [전압](/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 16단계 판별로 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 속도(레이턴시)가 느리고 P/E 사이클이 1,000~3,000회로 낮다. RDBMS [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 몰리면 수주 내 수명이 소진된다. 반드시 [SLC](/studynote/01_computer_architecture/15_advanced_topics/597_slc_caching/)/MLC 고내구성 드라이브로 교체하거나, TLC SSD에 [SLC](/studynote/01_computer_architecture/15_advanced_topics/597_slc_caching/) [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) 버퍼를 구성해야 한다.

<strong>TRIM <a href="/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a> 비활성화 상태 방치</strong>: SSD는 덮어쓰기가 불가능하므로, 삭제된 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 미리 소거(Erase)해 두지 않으면 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 시 [가비지 컬렉션](/studynote/02_operating_system/06_memory_management/380_garbage_collection/)이 동시에 발생해 [쓰기 증폭](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/)([Write Amplification](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/))이 폭증한다. OS에서 TRIM 활성화 여부를 반드시 확인해야 한다.

- **📢 섹션 요약 비유**: TRIM 비활성화는 **'손님이 나간 뒤 그릇을 치우지 않다가, 새 손님이 와서야 부랴부랴 상을 닦는 식당'** 과 같습니다. 미리미리 치워두면(TRIM) 손님이 바로 앉을 수 있지만, 방치하면 입장 대기가 폭발합니다.

---

## Ⅴ. 기대효과 및 결론

황의 법칙이 실효성을 가졌던 2000년대 초반부터 2010년대 초반까지, 낸드 플래시 GB당 단가가 기하급수적으로 하락했다. 128MB [USB](/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) 메모리에서 1TB 스마트폰으로의 진화는 바로 이 법칙이 관통한 10년의 산물이다.

**한계와 전제조건**: 물리 법칙은 공학 의지만으로 극복할 수 없다. 20nm 이하 2D 미세화에서 [터널링](/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/)([Tunneling](/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/)) [전류](/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/)와 셀 간 간섭이 수율을 무너뜨렸다. 3D V-NAND는 수평 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)이 아닌 수직 스택으로 황의 법칙을 연명시키고 있지만, 200층 이상의 적층은 제조 공정의 복잡도와 비용을 급격히 높인다.

**미래 방향**: ① 300층 이상 V-NAND 적층 경쟁(삼성, SK하이닉스, 마이크론), ② [PLC](/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/)(Penta Level Cell, 5비트/셀) 상용화 연구, ③ 스토리지급 메모리(Storage Class Memory)와의 경계 융합.

황의 법칙은 "끝났다"가 아니라, "차원을 바꾸어 계속된다"고 기억해야 한다. 평면 한계에 부딪혔을 때 하늘로 방향을 튼 발상 전환이 V-NAND라는 새 법칙의 씨앗이 됐다.

- **📢 섹션 요약 비유**: 황의 법칙은 **'디지털 데이터를 담는 방주(Ark)를 매년 두 배씩 만들던 기적의 조선업'** 이었습니다. 바다(실리콘)가 좁아져 더 큰 배를 평평하게 만들 수 없자, 배 위로 200층을 쌓아 올리며(V-NAND) 계속 항해하고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **무어의 법칙 (Moore's Law)** | CPU [트랜지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/014_transistor/) 집적도의 2년 2배 예측; 황의 법칙과 대칭적 성장 모델 |
| **V-NAND (Vertical NAND)** | 2D 미세화 한계 극복을 위한 수직 적층 기술; 황의 법칙의 물리적 연장 |
| **MLC / TLC / QLC** | 1셀당 저장 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 늘려 집적도를 높이는 다중 레벨 셀 기술 |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/">FTL</a> (<a href="/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/">Flash Translation Layer</a>)</strong> | 낸드 플래시 수명 관리(웨어 레벨링, [가비지 컬렉션](/studynote/02_operating_system/06_memory_management/380_garbage_collection/))를 담당하는 [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/) |
| <strong>덴나드 <a href="/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a> (<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/148_dennard_scaling/">Dennard Scaling</a>)</strong> | [트랜지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/014_transistor/) 축소 시 전력 밀도 일정 -> 2004년 붕괴; 황의 법칙과 무어의 법칙 쇠퇴의 공통 원인 |

### 📈 관련 키워드 및 발전 흐름도

```text
디지털 멀티미디어 폭발 -> 낸드 플래시 수요 급증
    |
    v
황의 법칙 (Hwang's Law) — 1년 2배 집적도 성장
    |
    +-► SLC -> MLC -> TLC -> QLC (셀 다중화)
    |
    +-► 2D 공정 미세화 -> 20nm 물리 한계
              |
              v
        3D V-NAND (Vertical NAND) 수직 적층
              |
              v
        200층+ 적층 / PLC 연구 / SCM 융합
```

### 👶 어린이를 위한 3줄 비유 설명

1. 황의 법칙은 우리 스마트폰 속 마법 서랍장(NAND 메모리)이 <strong>매년 두 배씩 쑥쑥 커진다는 놀라운 성장 규칙</strong>이에요!
2. 서랍을 더 잘게 쪼개다 보니 너무 좁아져서 전기가 새는 문제가 생겼어요. 그래서 천재 공학자들이 아예 서랍장을 <strong>아파트처럼 200층으로 높이 쌓는 기술(V-NAND)</strong>을 발명했답니다!
3. 게다가 방 하나에 한 명만 자던 것을 2층·3층 침대로 바꿔 여러 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 구겨 넣는 꼼수(TLC, QLC)도 써서, 요즘 스마트폰 한 대에 영화 수백 편을 담을 수 있게 된 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 147 / 803

<- **이전**: [146. 무어의 법칙 (Moore's Law)](/studynote/01_computer_architecture/03_architecture_basics_performance/146_moores_law/)
**다음**: [148. 데나드 스케일링 (Dennard Scaling)](/studynote/01_computer_architecture/03_architecture_basics_performance/148_dennard_scaling/) ->

---
