+++
title = "84. 직교 주파수 분할 다중화 (OFDM, Orthogonal FDM)"
description = "초고속 데이터를 수천 개의 저속 부반송파로 쪼개어 직교성 기반으로 빈틈없이 다중화한 5G와 Wi-Fi의 핵심 물리 아키텍처"
date = 2026-03-30

[taxonomies]
tags = ["network"]

[extra]
tags = ["network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OFDM (Orthogonal Frequency [Division](/knowledge-base/studynote/05_database/07_exam_summary/411_division_operation/) [Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/))은 넓은 대역을 서로 직교하는 많은 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)로 나눠 전송하는 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) 방식이다.
> 2. **가치**: 다중경로가 심한 채널을 좁은 대역의 단순한 문제들로 바꾸므로, 등화가 쉬워지고 스펙트럼 효율이 높아진다.
> 3. **판단 포인트**: 대신 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/), PAPR (Peak-to-Average [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Ratio), [FFT](/knowledge-base/studynote/08_algorithm_stats/07_numerical/126_fft/)/IFFT 처리와 같은 비용을 감당할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

OFDM (Orthogonal Frequency [Division](/knowledge-base/studynote/05_database/07_exam_summary/411_division_operation/) [Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/))은 하나의 고속 데이터를 여러 저속 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)로 나누어 보내는 방식이다. 각 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)는 직교하도록 배치되므로 서로 간섭하지 않으면서도 좁은 간격으로 촘촘히 채울 수 있다. 무선 채널이 다중경로와 주파수 선택적 페이딩으로 복잡해질수록 OFDM의 장점이 커진다.

이 방식이 널리 쓰이는 이유는, 넓은 대역을 한 번에 통과시키는 것보다 좁은 대역 여러 개를 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 다루는 편이 등화가 쉽기 때문이다. Wi-Fi와 4G/[5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 계열이 OFDM 계열을 적극적으로 사용하는 것도 같은 이유다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">고속 직렬 데이터</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">부반송파 여러 개로 분할</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">각 부반송파는 직교 상태로 전송</div>
</div>
</div>



- **📢 섹션 요약 비유**: 한 줄로 달리던 사람들이 서로 부딪히지 않도록, 여러 줄의 좁은 통로로 나눠 달리게 하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

OFDM은 송신 측에서 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 데이터를 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 나눈 뒤 IFFT (Inverse Fast Fourier Transform)로 시간 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 만들고, 수신 측에서 [FFT](/knowledge-base/studynote/08_algorithm_stats/07_numerical/126_fft/) (Fast Fourier Transform)로 다시 주파수 영역으로 돌린다. 이때 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/) 간격은 유효 심볼 시간의 역수와 맞춰 [직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)을 유지한다. 또한 [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) ([Cyclic Prefix](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/))를 앞에 붙여 다중경로 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 심볼 사이 간섭으로 번지는 것을 줄인다.

| 구성 | 역할 | 핵심 포인트 |
| :--- | :--- | :--- |
| [Subcarrier](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/) | 좁은 주파수 단위 | [직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/) 유지 |
| IFFT | 주파수 → 시간 변환 | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 합성 |
| [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) ([Cyclic Prefix](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)) | 심볼 앞의 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 구간 | 다중경로와 ISI 완화 |
| [FFT](/knowledge-base/studynote/08_algorithm_stats/07_numerical/126_fft/) | 시간 → 주파수 변환 | 수신 복원 |
| Pilot | 채널 추정 기준점 | 등화와 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 지원 |

```text
비트 → QAM 매핑 → IFFT → CP 추가 → 채널 → CP 제거 → FFT → 등화 → 비트 복원

직교성 덕분에 부반송파는 겹쳐도 수학적으로 분리된다.
```

수식으로 보면 [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/) 간격 Δf = 1 / T_u 이고, [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 길이는 채널 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 확산보다 길어야 한다. 즉 OFDM은 채널을 '더 좋은 채널'로 만드는 것이 아니라, 어려운 채널을 다루기 쉬운 여러 개의 작은 문제로 쪼개는 기술이다.

- **📢 섹션 요약 비유**: 빨대 여러 개를 나눠 쓰면 한 번에 마시는 양은 줄어도, 막히는 문제는 훨씬 줄어든다.

---

## Ⅲ. 비교 및 연결

OFDM을 이해하려면 단일 [반송파](/knowledge-base/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/), 전통 FDM (Frequency [Division](/knowledge-base/studynote/05_database/07_exam_summary/411_division_operation/) [Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)), 그리고 [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) (Orthogonal Frequency [Division](/knowledge-base/studynote/05_database/07_exam_summary/411_division_operation/) [Multiple Access](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/))를 함께 봐야 한다. 단일 [반송파](/knowledge-base/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/)는 구현이 단순하지만 다중경로에 약하고, FDM은 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)대역 때문에 스펙트럼 효율이 떨어지며, OFDMA는 OFDM을 사용자 단위 [자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/)으로 확장한 형태다.

| 방식 | 다중경로 대응 | 스펙트럼 효율 | 다중 사용자 |
| :--- | :--- | :--- | :--- |
| 단일 [반송파](/knowledge-base/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) | 등화가 어려움 | 보통 | 직접 분할 필요 |
| FDM | [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)대역이 큼 | 낮음 | 주파수로 나눔 |
| OFDM | 등화가 쉬움 | 높음 | 사용자 분할은 별도 |
| [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) | OFDM 기반 | 높음 | 서브캐리어를 사용자별 배정 |

즉 OFDM은 물리 계층의 전송 효율을, OFDMA는 그 위에서의 다중 사용자 자원 분배를 다룬다. 두 용어를 섞어 쓰면 설계 범위를 놓치기 쉬우므로, 하나는 변조/[다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) 방식이고 다른 하나는 [자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/) 방식이라는 점을 구분해야 한다.

- **📢 섹션 요약 비유**: 한 명이 긴 줄로 주문받는 것과, 여러 창구로 나눠 받는 것의 차이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 OFDM의 장점보다 약점이 더 먼저 문제로 드러나기도 한다. [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 맞지 않으면 [직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)이 깨지고, PAPR (Peak-to-Average [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Ratio)이 높으면 전력 증폭기가 비효율적이 된다. 그래서 수신기 설계에서는 채널 추정, 주파수 오프셋 보정, 파일럿 배치가 중요하다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 길이가 채널 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 확산을 충분히 덮는가?
2. 파일럿 구조가 채널 추정을 안정적으로 지원하는가?
3. 고 PAPR에 대비한 전력 증폭기 여유가 있는가?
4. 주파수 / 시간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 오차를 보정할 수 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)만 강조하고 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 예산을 계산하지 않는 경우
- CP를 너무 짧게 잡아 ISI를 다시 만드는 경우
- PAPR 문제를 고려하지 않고 출력만 키우는 경우

- **📢 섹션 요약 비유**: 마라톤을 여러 레인으로 나눠 달리면 좋지만, 출발선이 어긋나면 서로 밀치게 된다.

---

## Ⅴ. 기대효과 및 결론

OFDM의 기대효과는 다중경로 환경에서 높은 데이터율과 비교적 단순한 수신 구조를 동시에 확보하는 데 있다. 그러나 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 비용과 전력 증폭기 제약까지 포함해 봐야 진짜 성능을 판단할 수 있다. 결국 OFDM은 빠른 전송을 위한 꼼수가 아니라, 복잡한 무선 채널을 다루기 위한 체계적인 분해 전략이다.

따라서 OFDM을 기억할 때는 '주파수를 잘게 쪼갠다'보다 '쪼갠 뒤 [직교성](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)을 이용해 다시 합친다'는 관점이 더 중요하다. 이 관점이 있어야 [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/), [MIMO](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/097_MIMO_다중_안테나_기술/), [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 물리계층으로도 자연스럽게 연결된다.

- **📢 섹션 요약 비유**: 큰 돌멩이를 한 번에 옮기기보다, 작은 돌로 쪼개서 바구니에 담는 것이 더 안정적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Orthogonality](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/) | [부반송파](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)가 겹쳐도 분리되는 수학적 성질 |
| IFFT / [FFT](/knowledge-base/studynote/08_algorithm_stats/07_numerical/126_fft/) | 송수신 변환의 핵심 도구 |
| [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) ([Cyclic Prefix](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)) | 심볼 간 간섭을 줄이는 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 구간 |
| PAPR (Peak-to-Average [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Ratio) | 전력 증폭기 설계의 부담 |
| [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) | OFDM을 다중 사용자 자원 배분으로 확장 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">직렬 비트 스트림</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">병렬 서브캐리어 분할</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">IFFT → CP → 전송</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">채널 → FFT → 등화 → 복원</div>
</div>
</div>



흐름의 핵심은 '하나의 어려운 채널'을 '많은 쉬운 채널'로 바꾸는 데 있다.

### 👶 어린이를 위한 3줄 비유 설명

1. 길 하나로 달리면 부딪히기 쉬워요.
2. 길을 여러 개로 나누면 서로 덜 막혀요.
3. 그래도 출발 시간이 맞아야 모두 같이 잘 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 84 / 1120

← **이전**: [83. 직교성 (Orthogonality) 원리](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/083_직교성_Orthogonality/)
**다음**: [85. 부반송파 (Subcarrier)](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/) →

---
