---
title: 85. 부반송파 (Subcarrier)
date: '2026-03-30'
description: OFDM 시스템에서 대역폭을 잘게 쪼개어 다중경로 간섭을 방어하는 부반송파의 원리와 실무 적용
tags:
- network
---

## 핵심 인사이트 (3줄 요약)

> **본질**: 부반송파(Subcarrier)는 넓은 대역을 잘게 나눈 좁은 주파수 채널로, 하나의 심볼(Symbol)을 실어 나르는 운반선이다.
> **가치**: OFDM (Orthogonal Frequency [[411_division_operation|Division]] [[071_다중화_Multiplexing|Multiplexing]])과 [[945_ofdma_orthogonal_frequency_division_multiple_access_resource_block|OFDMA]] (Orthogonal Frequency [[411_division_operation|Division]] [[087_다중접속_Multiple_Access|Multiple Access]])는 많은 부반송파를 직교시키는 덕분에 다중경로에 강하다.
> **판단 포인트**: 부반송파 간격, [[086_CP_순환_전치_GI|CP]] ([[086_CP_순환_전치_GI|Cyclic Prefix]]), [[212_synchronization_mechanisms|동기화]]가 맞지 않으면 [[083_직교성_Orthogonality|직교성]]이 깨져 ISI (Inter-Symbol Interference)와 ICI (Inter-Carrier Interference)가 커진다.

---

## Ⅰ. 개요 및 필요성

부반송파는 전체 대역을 여러 개의 좁은 주파수 칸으로 쪼개 만든 개별 운반 채널이다. 한 번에 큰 신호를 보내는 대신, 여러 부반송파에 나눠 보내면 각 채널의 왜곡이 작아져 등화(Equalization)가 쉬워진다.

이 방식이 필요한 이유는 무선 채널이 항상 평평하지 않기 때문이다. 다중경로와 주파수 선택적 페이딩이 있는 환경에서는 단일 반송파보다 다중 부반송파 구조가 훨씬 다루기 쉽고, 여러 사용자의 자원 배분도 정교하게 할 수 있다.

- 📢 섹션 요약 비유: 좁은 차선 여러 개

---

## Ⅱ. 아키텍처 및 핵심 원리

OFDM은 [[001_dikw_pyramid|데이터]]를 여러 부반송파에 나눠 실은 뒤 IFFT (Inverse Fast Fourier Transform)로 시간 영역 신호를 만들고, 수신 측에서 [[126_fft|FFT]] (Fast Fourier Transform)로 다시 복원한다. 부반송파는 서로 직교하도록 배치되어, 주파수는 겹쳐 보이지만 간섭은 최소화된다.

```text
주파수 축
|  |  |  |  |  |
|__|__|__|__|__|__  -> orthogonal subcarriers
```

| 요소 | 역할 |
| --- | --- |
| Subcarrier | 개별 심볼을 실어 나르는 좁은 주파수 칸 |
| IFFT/[[126_fft|FFT]] | 주파수-시간 변환 |
| [[086_CP_순환_전치_GI|CP]] ([[086_CP_순환_전치_GI|Cyclic Prefix]]) | 다중경로 [[015_지연_데이터_관점|지연]]에 대한 [[571_protection_vs_security|보호]] 구간 |
| QAM (Quadrature Amplitude Modulation) | 각 부반송파에 실리는 변조 방식 |

핵심은 "대역을 넓게 쓰되, 각 칸은 좁게 유지한다"는 분할 전략이다.

- 📢 섹션 요약 비유: 분할된 고속도로

---

## Ⅲ. 비교 및 연결

단일 반송파는 구현이 단순하지만 채널 왜곡에 취약하다. 반면 부반송파 기반 OFDM은 채널을 잘게 나눠 다루므로 등화가 쉬워지고, OFDMA는 그 부반송파들을 사용자별로 나눠 쓰게 해 [[087_다중접속_Multiple_Access|다중 접속]]까지 가능하게 한다. [[088_주파수_분할_다중접속_FDMA|FDMA]] (Frequency [[411_division_operation|Division]] [[087_다중접속_Multiple_Access|Multiple Access]])나 [[089_시분할_다중접속_TDMA|TDMA]] (Time [[411_division_operation|Division]] [[087_다중접속_Multiple_Access|Multiple Access]])와 비교하면, OFDMA는 주파수와 사용자 배정을 더 세밀하게 조정할 수 있다.

| 비교 대상 | 차이점 |
| --- | --- |
| Single-Carrier | 하나의 넓은 채널 사용 |
| [[088_주파수_분할_다중접속_FDMA|FDMA]] | 주파수 대역을 사용자별로 분리 |
| [[089_시분할_다중접속_TDMA|TDMA]] | 시간 슬롯을 사용자별로 분리 |
| OFDM | 한 사용자 신호를 여러 부반송파로 [[136_variance|분산]] |
| [[945_ofdma_orthogonal_frequency_division_multiple_access_resource_block|OFDMA]] | 부반송파를 사용자별로 동적 할당 |

즉 부반송파는 "같은 도로를 작은 차선들로 나눠 교통 체증을 줄이는 방식"이다.

- 📢 섹션 요약 비유: 차선 분리와 분배

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 부반송파 간격이 너무 좁으면 Doppler shift에 약해지고, 너무 넓으면 [[083_직교성_Orthogonality|직교성]]과 대역 효율이 나빠진다. CP는 다중경로 [[015_지연_데이터_관점|지연]]보다 길어야 하지만, 길어질수록 유효 전송률이 떨어진다. 또 OFDM은 PAPR (Peak-to-Average [[069_type_1_2_error_statistical_power|Power]] Ratio)가 커서 전력 증폭기 선형성 관리가 중요하다.

### [[435_checklist_based_testing|체크리스트]]
1. 채널 [[015_지연_데이터_관점|지연]] 확산과 부반송파 간격의 균형이 맞는가?
2. [[086_CP_순환_전치_GI|CP]] 길이가 최대 [[015_지연_데이터_관점|지연]]보다 충분한가?
3. [[212_synchronization_mechanisms|동기화]] 오차와 주파수 오프셋 보정이 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- CP를 너무 짧게 잡아 ISI를 키우는 것
- PAPR를 무시하고 증폭기를 포화시키는 것
- 서브캐리어 [[083_직교성_Orthogonality|직교성]]을 유지할 [[212_synchronization_mechanisms|동기화]]를 생략하는 것

- 📢 섹션 요약 비유: 속도와 안정의 타협점

---

## Ⅴ. 기대효과 및 결론

부반송파 구조의 장점은 강인한 수신, 유연한 [[041_resource_allocation|자원 할당]], 고속 [[001_dikw_pyramid|데이터]] 전송이다. 그러나 [[212_synchronization_mechanisms|동기화]]·PAPR·[[086_CP_순환_전치_GI|CP]] 손실 같은 비용이 있어, 아무 채널에나 무조건 유리한 것은 아니다. 그래서 좋은 설계는 "주파수 분할"의 이득과 "[[212_synchronization_mechanisms|동기화]] 복잡도"의 비용을 함께 본다.

결론적으로 부반송파는 다중경로 시대의 실용적 분할 전략이다. 기술사 답변에서는 OFDM/[[945_ofdma_orthogonal_frequency_division_multiple_access_resource_block|OFDMA]], [[083_직교성_Orthogonality|직교성]], [[086_CP_순환_전치_GI|CP]], PAPR를 연결해 설명하면 완성도가 높다.

- 📢 섹션 요약 비유: 좁은 길 여러 개

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| Subcarrier | 좁은 주파수 운반 단위 |
| OFDM | 부반송파 기반 전송 방식 |
| [[945_ofdma_orthogonal_frequency_division_multiple_access_resource_block|OFDMA]] | 부반송파 기반 [[087_다중접속_Multiple_Access|다중 접속]] |
| [[126_fft|FFT]]/IFFT | 주파수-시간 변환 도구 |
| [[086_CP_순환_전치_GI|CP]] ([[086_CP_순환_전치_GI|Cyclic Prefix]]) | 다중경로 [[571_protection_vs_security|보호]] 구간 |
| PAPR (Peak-to-Average [[069_type_1_2_error_statistical_power|Power]] Ratio) | 전력 증폭기 설계 이슈 |

### 📈 관련 키워드 및 발전 흐름도

```text
데이터 분할
   ↓
부반송파에 매핑
   ↓
IFFT로 시간영역 변환
   ↓
CP 추가
   ↓
무선 전송
   ↓
FFT 복원 / 등화
```

### 👶 어린이를 위한 3줄 비유 설명

1. 부반송파는 큰 도로를 여러 작은 차선으로 나눈 것과 같아요.
2. 차선이 많으면 차가 서로 덜 부딪히고 빨리 갈 수 있어요.
3. 대신 차선 표시를 정확히 맞춰야 길이 꼬이지 않아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 85 / 1120

← **이전**: [[084_직교_주파수_분할_다중화_OFDM|84. 직교 주파수 분할 다중화 (OFDM, Orthogonal FDM)]]
**다음**: [[086_CP_순환_전치_GI|86. CP (Cyclic Prefix) / GI (Guard Interval) - ISI 방지]] →

---
