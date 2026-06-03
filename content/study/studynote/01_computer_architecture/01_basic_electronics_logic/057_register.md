+++
weight = 57
title = "57. 레지스터 (Register)"
date = "2026-04-19"
[extra]
categories = "studynote-computer-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 레지스터([[175_register_addressing|Register]])는 D [[051_flip_flop|플립플롭]]([[051_flip_flop|Flip-Flop]])을 [[430_index_fast_full_scan|병렬]]로 묶어 CPU가 아주 빠르게 읽고 쓰는 [[148_5g_embb_urllc_mmtc|초고속]] 저장 공간이다.
> 2. **가치**: 메모리 계층 구조에서 가장 가까운 위치에 있어, 연산 직전에 필요한 값을 즉시 공급해 CPU 성능을 좌우한다.
> 3. **판단 포인트**: [[162_gpr|범용 레지스터]]([[162_gpr|GPR]])와 [[163_spr|특수 목적 레지스터]](Program [[059_counter|Counter]], [[158_instruction|Instruction]] [[175_register_addressing|Register]], [[057_stack|Stack]] Pointer 등)를 구분해 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

레지스터는 CPU 안에서 데이터를 잠깐 올려두는 작업대다. DRAM보다 훨씬 빠르기 때문에, 연산 직전의 값을 거기에 놓고 바로 꺼내 쓴다.

만약 레지스터가 없다면 CPU는 매 연산마다 메인 메모리까지 왕복해야 하므로 속도가 급격히 떨어진다. 그래서 레지스터는 CPU 동작의 중심에 있다.

- **📢 섹션 요약 비유**: 레지스터는 요리사가 손에 쥐고 쓰는 도마처럼, 바로 앞에 있어야 하는 재료를 두는 자리다.

---

## Ⅱ. [[430_index_fast_full_scan|병렬]] 저장 구조와 동작 원리

레지스터는 여러 개의 D [[051_flip_flop|플립플롭]]을 한 번에 묶어 같은 클록([[045_clock|Clock]])에 맞춰 동작한다.

```text
입력 비트 ─► D FF ─► D FF ─► D FF ─► D FF
                │        │        │        │
             클록 신호가 동시에 들어와 저장
```

클록이 들어오면 입력 [[073_bit|비트]]들이 동시에 저장되고, 읽을 때는 [[344_bus|버스]]([[344_bus|Bus]])를 통해 한 번에 출력된다. 이 [[430_index_fast_full_scan|병렬]] 구조 덕분에 여러 [[073_bit|비트]]를 한 번에 다룰 수 있다.

- **📢 섹션 요약 비유**: 레지스터는 여러 칸짜리 우편함이 한 박자에 동시에 닫히고 열리는 구조다.

---

## Ⅲ. 레지스터의 종류

레지스터는 쓰임새에 따라 나뉜다.

- **[[162_gpr|범용 레지스터]] (General Purpose [[175_register_addressing|Register]], [[162_gpr|GPR]])**: 연산 중간값을 저장한다.
- **Program [[059_counter|Counter]] ([[164_pc|PC]])**: 다음에 실행할 [[158_instruction|명령어]] 주소를 가리킨다.
- **[[158_instruction|Instruction]] [[175_register_addressing|Register]] ([[165_ir|IR]])**: 현재 실행 중인 [[158_instruction|명령어]]를 담는다.
- **[[057_stack|Stack]] Pointer ([[166_sp|SP]])**: 스택의 꼭대기를 가리킨다.
- **[[167_status_register|Status Register]] / Program [[167_status_register|Status Register]] (PSR)**: 연산 결과의 상태 [[073_bit|비트]]를 담는다.

이 구분을 알면 CPU가 [[158_instruction|명령어]]를 어떻게 해석하고 실행하는지 훨씬 명확해진다.

- **📢 섹션 요약 비유**: 같은 서랍장이라도 어떤 칸은 메모용, 어떤 칸은 주소용, 어떤 칸은 현재 작업용으로 나뉜다.

---

## Ⅳ. CPU [[205_datapath|데이터패스]]에서의 역할

레지스터는 [[117_alu|Arithmetic Logic Unit]] ([[117_alu|ALU]])와 거의 붙어 있다. 따라서 연산에 필요한 피연산자를 지체 없이 공급한다.

레지스터 [[501_file_definition_logical_record|파일]]([[175_register_addressing|Register]] [[501_file_definition_logical_record|File]]) 구조가 커질수록 한 번에 더 많은 값을 저장하고 꺼낼 수 있지만, 설계가 복잡해지고 전력과 면적 부담도 함께 커진다.

- **📢 섹션 요약 비유**: 레지스터는 부엌 조리대 바로 옆에 있는 양념통처럼, 손이 닿는 거리에서 연산을 빠르게 돕는다.

---

## Ⅴ. 실무적 비교와 판단 기준

레지스터는 캐시(Cache)나 메모리와 역할이 다르다.

- **레지스터**: 가장 빠르지만 가장 작다.
- **캐시**: 레지스터보다 느리지만 더 크다.
- **메인 메모리**: 더 크지만 훨씬 느리다.

CPU를 이해할 때는 단순히 "빠르다"가 아니라, 어떤 값을 어디에 얼마나 오래 둘지까지 함께 봐야 한다.

- **📢 섹션 요약 비유**: 레지스터는 책상 위 펜, 캐시는 책상 서랍, 메모리는 창고라고 보면 된다.

---

## 관련 개념 맵

```text
D 플립플롭
   ↓
레지스터
   ↓
레지스터 파일
   ↓
CPU 데이터패스 / ALU
```

---

## 관련 키워드 및 발전 흐름도

1. 단일 [[073_bit|비트]] [[051_flip_flop|플립플롭]] → 기본 저장 소자
2. [[430_index_fast_full_scan|병렬]] 결합 → 다비트 레지스터
3. [[162_gpr|GPR]] / [[164_pc|PC]] / [[165_ir|IR]] / [[166_sp|SP]] 분화 → CPU 제어 정교화
4. 레지스터 [[501_file_definition_logical_record|파일]] → 대규모 [[205_datapath|데이터패스]] 지원
5. 고성능 CPU 설계 → 더 많은 레지스터와 더 빠른 접근 최적화

---

## 어린이를 위한 3줄 비유 설명

레지스터는 요리사가 바로 앞에 두는 작은 접시예요.  
바로 써야 할 재료를 거기 올려두면 빨리 요리할 수 있어요.  
멀리 있는 창고까지 가지 않아도 되니까 아주 빠른 거예요.
