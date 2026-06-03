---
title: 58. 시프트 레지스터 (Shift Register)
date: '2026-04-19'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시프트 [[057_register|레지스터]](Shift [[175_register_addressing|Register]])는 [[051_flip_flop|플립플롭]]([[051_flip_flop|Flip-Flop]])을 [[149_serial_communication_rs232_rs485|직렬]]로 연결해 클록마다 [[073_bit|비트]]를 한 칸씩 이동시키는 순차 논리회로다.
> 2. **가치**: [[149_serial_communication_rs232_rs485|직렬]]-[[430_index_fast_full_scan|병렬]] 변환과 2의 거듭제곱 연산, 지연선, 통신 인터페이스에서 매우 유용하다.
> 3. **판단 포인트**: SISO, SIPO, PISO, PIPO 같은 형태와 LFSR (Linear Feedback Shift [[175_register_addressing|Register]]), Barrel Shifter 응용을 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

시프트 [[057_register|레지스터]]는 [[001_dikw_pyramid|데이터]] [[073_bit|비트]]를 옆 칸으로 밀어 보내는 회로다. 작은 저장소들이 줄지어 있고, 클록이 들어올 때마다 모두 한 칸씩 이동한다.

[[459_quic_fec_forward_error_correction|초기]] 하드웨어는 [[149_serial_communication_rs232_rs485|직렬]] 통신이나 [[073_bit|비트]] 이동 연산을 효율적으로 처리하기 위해 이런 구조를 필요로 했다.

- **📢 섹션 요약 비유**: 시프트 [[057_register|레지스터]]는 컨베이어 벨트 위의 상자들처럼 한 칸씩 밀려가는 구조다.

---

## Ⅱ. 동작 구조

각 [[051_flip_flop|플립플롭]]의 출력이 다음 [[051_flip_flop|플립플롭]]의 입력으로 연결된다.

```text
SI -> [FF0] -> [FF1] -> [FF2] -> [FF3] -> SO
          ↑       ↑       ↑       ↑
        같은 CLK가 모두에 동시에 들어감
```

클록이 한 번 오면 모든 [[073_bit|비트]]가 동시에 한 칸씩 이동한다. 이 단순한 구조가 [[149_serial_communication_rs232_rs485|직렬]] 처리를 가능하게 한다.

- **📢 섹션 요약 비유**: 줄 서 있던 사람들이 신호가 울릴 때마다 한 칸씩 앞으로 움직이는 모습이다.

---

## Ⅲ. 종류와 방향

시프트 [[057_register|레지스터]]는 [[001_dikw_pyramid|데이터]] 입출력 방식에 따라 나뉜다.

- **SISO (Serial-In Serial-Out)**: 한 [[073_bit|비트]]씩 넣고 한 [[073_bit|비트]]씩 뺀다.
- **SIPO (Serial-In Parallel-Out)**: 한 [[073_bit|비트]]씩 넣고 여러 [[073_bit|비트]]를 한 번에 뺀다.
- **PISO (Parallel-In Serial-Out)**: 여러 [[073_bit|비트]]를 한 번에 넣고 한 [[073_bit|비트]]씩 뺀다.
- **PIPO (Parallel-In Parallel-Out)**: 한 번에 넣고 한 번에 뺀다.

방향이 양쪽인 구조나, [[430_index_fast_full_scan|병렬]] 로드가 가능한 구조도 자주 쓴다.

- **📢 섹션 요약 비유**: 들어오는 문과 나가는 문이 하나인지 여러 개인지에 따라 다른 우편함 구조가 된다.

---

## Ⅳ. 활용과 응용

시프트 [[057_register|레지스터]]는 다양한 곳에 쓰인다.

- [[149_serial_communication_rs232_rs485|직렬]] 통신 버퍼
- 지연선(delay line)
- [[121_arithmetic_shift|산술 시프트]](곱셈/나눗셈)
- LFSR (Linear Feedback Shift [[175_register_addressing|Register]])
- Barrel Shifter

특히 LFSR은 난수 [[087_process_state_transition|생성]]과 패턴 [[087_process_state_transition|생성]]에, Barrel Shifter는 빠른 시프트 연산에 쓰인다.

- **📢 섹션 요약 비유**: 레일 위에서 짐을 조금씩 옮기다가, 필요하면 한 번에 훅 밀어 보내는 장치다.

---

## Ⅴ. 실무 비교와 설계 관점

[[057_register|레지스터]]와 달리 시프트 [[057_register|레지스터]]는 "저장"보다 "이동"이 핵심이다. 그래서 [[001_dikw_pyramid|데이터]] 흐름을 다루는 설계에서 중요하다.

설계할 때는 다음을 본다.

- 입력/출력 방향
- [[073_bit|비트]] 폭
- [[430_index_fast_full_scan|병렬]] 로드 필요 여부
- 시프트 속도
- 통신 프로토콜과의 연계

- **📢 섹션 요약 비유**: 서랍장보다 컨베이어 벨트에 더 가까운 장치다.

---

## 관련 개념 맵

```text
플립플롭
   ↓
직렬 연결
   ↓
비트 이동
   ↓
통신 / LFSR / Barrel Shifter
```

---

## 관련 키워드 및 발전 흐름도

1. [[051_flip_flop|플립플롭]] [[055_array|배열]] → 기본 저장과 이동
2. [[149_serial_communication_rs232_rs485|직렬]] 통신 요구 → SISO/SIPO/PISO/PIPO 등장
3. [[121_arithmetic_shift|산술 시프트]] → 빠른 [[073_bit|비트]] 이동 활용
4. LFSR → 난수와 패턴 [[087_process_state_transition|생성]] 응용
5. Barrel Shifter → 고속 [[430_index_fast_full_scan|병렬]] 시프트로 발전

---

## 어린이를 위한 3줄 비유 설명

시프트 [[057_register|레지스터]]는 줄지어 선 친구들이 한 칸씩 옆으로 움직이는 거예요.  
뒤에서 새 친구가 들어오면 앞사람들이 같이 밀려나요.  
그래서 [[073_bit|비트]]를 옮기거나 나누고 붙이는 데 아주 편해요.
