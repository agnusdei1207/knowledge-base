+++
title = "049. OQPSK / π/4-QPSK — 오프셋 위상 변조"
date = 2026-04-05

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

> **핵심 인사이트**
> 1. OQPSK(Offset QPSK)는 Q 채널을 I 채널 대비 반 심볼(T/2)만큼 지연시켜 180° 위상 전이를 제거 — QPSK에서 [11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/)→00 천이 시 발생하는 180° 급격한 위상 점프가 전력 증폭기를 비선형 영역으로 밀어넣는 문제를 해결한다.
> 2. π/4-QPSK는 두 QPSK [성상도](/knowledge-base/studynote/03_network/01_data_communication/053_성상도_Constellation_Diagram/)를 45° 교대 사용하여 최대 위상 전이를 135°로 제한 — OQPSK보다 스펙트럼 효율이 높고 비차동(Differential) 복조가 가능해 이동통신(IS-95 이전, DECT, PDC)에서 널리 사용되었다.
> 3. 두 변조 방식 모두 "포락선 변동(Envelope Variation) 최소화"가 핵심 목표 — 위상 전이가 클수록 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 포락선이 0에 가까워져 전력 증폭기 효율이 급락하므로, 위상 전이 제한이 배터리 수명과 직결된다.

---

## Ⅰ. QPSK의 문제점



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">QPSK 위상 전이 문제:</div>
<div class="kb-diagram-note">QPSK 심볼 배치:</div>
<div class="kb-diagram-note">00: 45°, 01: 135°, 11: 225°, 10: 315°</div>
<div class="kb-diagram-note">천이 예:</div>
<div class="kb-diagram-note">00(45°) → 11(225°): 180° 점프</div>
<div class="kb-diagram-note">01(135°) → 10(315°): 180° 점프</div>
<div class="kb-diagram-note">180° 위상 전이의 문제:</div>
<div class="kb-diagram-note">포락선 소멸 (Envelope Null):</div>
<div class="kb-diagram-note">I/Q 신호가 동시에 0을 통과</div>
<div class="kb-diagram-note">포락선 A(t) = √(I²+Q²) = 0 순간 발생</div>
<div class="kb-diagram-note">그래프:</div>
<div class="kb-diagram-note">위상: 45° ──→ 180° 전이 ──→ 225°</div>
<div class="kb-diagram-note">포락선: ████████ ████████</div>
<div class="kb-diagram-note">↓↑ (0 근처 급락)</div>
<div class="kb-diagram-note">전력 증폭기 문제:</div>
<div class="kb-diagram-note">비선형 PA (Power Amplifier): 효율 ↑</div>
<div class="kb-diagram-note">선형 PA: 효율 ↓ (배터리 소모)</div>
<div class="kb-diagram-note">포락선 변동이 크면:</div>
<div class="kb-diagram-note">→ PA를 선형 영역에서 운용 (효율 30%↓)</div>
<div class="kb-diagram-note">→ 배터리 수명 감소</div>
<div class="kb-diagram-note">→ 또는 비선형 PA 사용 → 스펙트럼 재성장</div>
<div class="kb-diagram-note">이동통신 단말기에서 치명적 문제</div>
</div>
</div>



> 📢 **섹션 요약 비유**: QPSK 180° 전이 = 전등 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 급격히 반전 — [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/)이 순간 0이 됨. 증폭기가 0 근처에서 왜곡. OQPSK/π/4-QPSK는 "천천히 돌기"로 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 0 방지!

---

## Ⅱ. OQPSK



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">OQPSK (Offset QPSK):</div>
<div class="kb-diagram-note">Q 채널을 I 채널 대비 T/2 지연</div>
<div class="kb-diagram-note">원리:</div>
<div class="kb-diagram-note">QPSK: I와 Q 동시 전환</div>
<div class="kb-diagram-note">→ 최대 180° 전이 가능</div>
<div class="kb-diagram-note">OQPSK: I와 Q가 T/2 간격으로 번갈아 전환</div>
<div class="kb-diagram-note">→ 한 번에 최대 90° 전이만 발생</div>
<div class="kb-diagram-note">I/Q 타이밍:</div>
<div class="kb-diagram-note">QPSK:</div>
<div class="kb-diagram-note">I:</div>
<div class="kb-diagram-note">Q: (동시)</div>
<div class="kb-diagram-note">OQPSK:</div>
<div class="kb-diagram-note">I:</div>
<div class="kb-diagram-note">Q: (T/2 지연)</div>
<div class="kb-diagram-note">→ I 또는 Q 중 하나씩만 변환</div>
<div class="kb-diagram-note">→ 최대 위상 전이: ±90°</div>
<div class="kb-diagram-note">포락선 특성:</div>
<div class="kb-diagram-note">QPSK: 포락선 0 통과 가능 (180° 전이 시)</div>
<div class="kb-diagram-note">OQPSK: 포락선 항상 √2/2 이상 (90° 전이 최대)</div>
<div class="kb-diagram-note">포락선 변동 감소 → PA 효율 향상</div>
<div class="kb-diagram-note">단점:</div>
<div class="kb-diagram-note">비차동 검파만 가능 (기준 위상 필요)</div>
<div class="kb-diagram-note">시스템 복잡성 증가 (T/2 지연 구현)</div>
<div class="kb-diagram-note">응용:</div>
<div class="kb-diagram-note">IS-95 CDMA 역방향(단말→기지국)</div>
<div class="kb-diagram-note">군용 통신</div>
<div class="kb-diagram-note">위성 통신</div>
</div>
</div>



> 📢 **섹션 요약 비유**: OQPSK = 두 다리 교대 걷기 — 두 발 동시 들면 넘어짐(180° 전이=포락선 0). 교대로 반 박자씩 어긋나게 딛으면 안정(최대 90°). I/Q 채널이 교대로 전환!

---

## Ⅲ. π/4-QPSK



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">π/4-QPSK (Pi/4-QPSK):</div>
<div class="kb-diagram-note">두 개의 QPSK 성상도를 45° 교대 사용</div>
<div class="kb-diagram-note">두 성상도:</div>
<div class="kb-diagram-note">성상도 A: 0°, 90°, 180°, 270°</div>
<div class="kb-diagram-note">성상도 B: 45°, 135°, 225°, 315°</div>
<div class="kb-diagram-note">짝수 심볼: A 사용</div>
<div class="kb-diagram-note">홀수 심볼: B 사용</div>
<div class="kb-diagram-note">위상 전이:</div>
<div class="kb-diagram-note">A → B 또는 B → A 전환 시:</div>
<div class="kb-diagram-note">최소 전이: ±45°</div>
<div class="kb-diagram-note">최대 전이: ±135°</div>
<div class="kb-diagram-note">QPSK: 최대 180°</div>
<div class="kb-diagram-note">π/4-QPSK: 최대 135° (감소!)</div>
<div class="kb-diagram-note">→ 포락선 변동 감소</div>
<div class="kb-diagram-note">차동 변조 (Differential Encoding):</div>
<div class="kb-diagram-note">절대 위상이 아닌 위상 변화량으로 정보 전달</div>
<div class="kb-diagram-note">전이 테이블:</div>
<div class="kb-diagram-note">데이터 00: +45° 전이</div>
<div class="kb-diagram-note">데이터 01: +135° 전이</div>
<div class="kb-diagram-note">데이터 10: -135° 전이</div>
<div class="kb-diagram-note">데이터 11: -45° 전이</div>
<div class="kb-diagram-note">복조:</div>
<div class="kb-diagram-note">현재 위상 - 이전 위상 = 전이량 → 데이터 복원</div>
<div class="kb-diagram-note">장점: 기준 위상 불필요 (채널 위상 오차에 강인)</div>
<div class="kb-diagram-note">OQPSK vs π/4-QPSK:</div>
<div class="kb-diagram-note">항목: OQPSK π/4-QPSK</div>
<div class="kb-diagram-note">최대 위상 전이: 90° 135°</div>
<div class="kb-diagram-note">차동 복조: 불가 가능</div>
<div class="kb-diagram-note">스펙트럼 효율: 동일 동일</div>
<div class="kb-diagram-note">포락선 변동: 낮음 중간</div>
<div class="kb-diagram-note">실제 사용: 위성/군용 이동통신</div>
</div>
</div>



> 📢 **섹션 요약 비유**: π/4-QPSK = 45° 엇갈린 두 개의 바퀴 — 홀/짝 심볼마다 다른 [성상도](/knowledge-base/studynote/03_network/01_data_communication/053_성상도_Constellation_Diagram/)(45° 회전). 최대 이동 135°로 제한. 차동 변조로 기준점 없이도 복조!

---

## Ⅳ. 스펙트럼 효율과 포락선



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">변조 방식 포락선 비교:</div>
<div class="kb-diagram-note">BPSK:</div>
<div class="kb-diagram-note">180° 전이 가능, 포락선 변동 최대</div>
<div class="kb-diagram-note">QPSK:</div>
<div class="kb-diagram-note">180° 전이 가능, 포락선 변동 크음</div>
<div class="kb-diagram-note">OQPSK:</div>
<div class="kb-diagram-note">90° 전이 최대, 포락선 변동 작음</div>
<div class="kb-diagram-note">π/4-QPSK:</div>
<div class="kb-diagram-note">135° 전이 최대, 포락선 변동 중간</div>
<div class="kb-diagram-note">MSK (Minimum Shift Keying):</div>
<div class="kb-diagram-note">연속적 위상 변화, 포락선 거의 일정</div>
<div class="kb-diagram-note">사실상 CPFSK (연속 위상 FSK)</div>
<div class="kb-diagram-note">GMSK (Gaussian MSK):</div>
<div class="kb-diagram-note">가우시안 필터 + MSK</div>
<div class="kb-diagram-note">완전히 일정한 포락선 → 비선형 PA 사용 가능</div>
<div class="kb-diagram-note">GSM 채택</div>
<div class="kb-diagram-note">스펙트럼 효율:</div>
<div class="kb-diagram-note">모두 2bps/Hz (동일, 4진 변조)</div>
<div class="kb-diagram-note">포락선 안정 → 비선형 PA 사용 가능</div>
<div class="kb-diagram-note">→ 전력 효율 향상 → 배터리 수명 연장</div>
<div class="kb-diagram-note">실제 응용:</div>
<div class="kb-diagram-note">IS-95 역방향: OQPSK</div>
<div class="kb-diagram-note">PDC (일본 2G): π/4-DQPSK</div>
<div class="kb-diagram-note">DECT (무선 전화): GFSK</div>
<div class="kb-diagram-note">GSM: GMSK</div>
<div class="kb-diagram-note">TETRA (디지털 무전): π/4-DQPSK</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 포락선 안정 = 전력 효율 — 포락선이 0 안 되면 저효율 증폭기 OK. 핸드폰 배터리 수명 = 증폭기 효율. OQPSK/GMSK가 배터리 절약 핵심!

---

## Ⅴ. 실무 시나리오 — TETRA 긴급 통신 시스템



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">TETRA (Terrestrial Trunked Radio) 긴급 무선 통신:</div>
<div class="kb-diagram-note">사용: 경찰, 소방, 긴급 서비스</div>
<div class="kb-diagram-note">변조: π/4-DQPSK (차동 π/4-QPSK)</div>
<div class="kb-diagram-note">TETRA π/4-DQPSK 선택 이유:</div>
<div class="kb-diagram-note">1. 차동 변조 강점:</div>
<div class="kb-diagram-note">긴급 상황 = 전파 환경 극도로 불안정</div>
<div class="kb-diagram-note">건물, 차량, 이동 반사파 → 위상 오차</div>
<div class="kb-diagram-note">차동 복조: 절대 위상 불필요</div>
<div class="kb-diagram-note">→ 채널 위상 추정 없이 복조</div>
<div class="kb-diagram-note">→ 긴급 상황 신뢰성 향상</div>
<div class="kb-diagram-note">2. 포락선 특성:</div>
<div class="kb-diagram-note">최대 135° 전이 → 중간 수준 포락선 변동</div>
<div class="kb-diagram-note">PA 효율 확보 (배터리/전원 효율)</div>
<div class="kb-diagram-note">휴대형 단말기: 배터리 수명 중요</div>
<div class="kb-diagram-note">3. 스펙트럼 효율:</div>
<div class="kb-diagram-note">TETRA: 25kHz 채널 → 4슬롯 TDMA</div>
<div class="kb-diagram-note">π/4-DQPSK: 36kbps (2bps/Hz × 18kHz)</div>
<div class="kb-diagram-note">→ 4명 동시 통화</div>
<div class="kb-diagram-note">비교 (TETRA vs P25):</div>
<div class="kb-diagram-note">TETRA: π/4-DQPSK, 유럽 표준</div>
<div class="kb-diagram-note">P25: C4FM (CQPSK 변형), 북미 표준</div>
<div class="kb-diagram-note">둘 다 긴급 통신용 강인한 변조 선택</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">서울 소방본부 TETRA:</div>
<div class="kb-diagram-note">500MHz 대역, 도시 전역 커버</div>
<div class="kb-diagram-note">빌딩 내부 투과: 건물 3층까지</div>
<div class="kb-diagram-note">차동 변조: 도심 다중 반사파 환경 복조 성공률 99.7%</div>
</div>
</div>



> 📢 **섹션 요약 비유**: TETRA 긴급통신 = 나침반 없이 방향 찾기 — 차동 변조는 기준 없이 변화량만으로 복조. 긴급 상황 불안정 환경에서도 안정적 통화. 배터리도 효율적!

---

## 📌 관련 개념 맵

```
OQPSK / π/4-QPSK
+-- 배경: QPSK 180° 전이 문제
+-- OQPSK
|   +-- Q 채널 T/2 지연
|   +-- 최대 90° 전이
|   +-- 포락선 변동 최소
+-- π/4-QPSK
|   +-- 두 성상도 45° 교대
|   +-- 최대 135° 전이
|   +-- 차동 변조 가능
+-- 공통 목표
|   +-- 포락선 안정화
|   +-- PA 효율 향상
+-- 응용
    +-- OQPSK: IS-95, 위성
    +-- π/4-QPSK: PDC, TETRA
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[QPSK (1960s)]
4위상 변조, 2bps/Hz
180° 전이 문제
      |
      v
[OQPSK (1970s)]
Q 채널 오프셋
군용/위성 통신
      |
      v
[π/4-QPSK (1980s)]
두 성상도 교대
이동통신 표준
      |
      v
[GSM GMSK (1991)]
연속 위상 변조
완전 포락선 일정
      |
      v
[현재: OFDM, mMIMO]
QAM + OFDM
5G NR 표준
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. QPSK 180° 문제 = 전등 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 급격히 반전 — [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/)이 순간 0이 되어 증폭기 왜곡. 배터리 낭비!
2. OQPSK = 두 다리 교대 걷기 — I/Q 채널이 반 박자씩 어긋나 동시 전환 방지. 최대 90° 전이로 안정!
3. π/4-QPSK = 두 바퀴 45° 교대 사용 — 홀/짝 심볼마다 다른 [성상도](/knowledge-base/studynote/03_network/01_data_communication/053_성상도_Constellation_Diagram/). 최대 135°, 차동 복조로 기준점 없이도 OK!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 49 / 1120

← **이전**: [048. BPSK·QPSK — 위상 편이 변조](/knowledge-base/studynote/03_network/01_data_communication/048_BPSK_QPSK/)
**다음**: [M진 PSK — 8PSK·16PSK (M-ary Phase Shift Keying)](/knowledge-base/studynote/03_network/01_data_communication/050_M진_PSK_8PSK_16PSK/) →

---
