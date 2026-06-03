+++
title = "048. BPSK·QPSK — 위상 편이 변조"
date = 2026-04-05

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

> **핵심 인사이트**
> 1. [PSK](/knowledge-base/studynote/09_security/03_network_security/142_psk_pre_shared_key/)(Phase Shift Keying)는 반송파의 위상(Phase)을 변화시켜 디지털 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전송 — BPSK는 2가지 위상(0°/180°)으로 1비트, QPSK는 4가지 위상(0°/90°/180°/270°)으로 2비트를 동시에 전송한다.
> 2. QPSK는 BPSK와 동일한 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)([Bandwidth](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))으로 2배 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 — 위상 수를 4개로 늘려 심볼당 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수를 2배로 높이면서도 BER([Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Error Rate) 성능은 BPSK와 동일하게 유지되는 효율적인 변조 방식이다.
> 3. 현대 통신에서 QAM(직교진폭변조)으로의 진화 — [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) NR에서 256-QAM을 사용하면 심볼당 8비트 전송이 가능하지만, [SNR](/knowledge-base/studynote/03_network/01_data_communication/024_신호_대_잡음비/) 요구사항도 급격히 높아지는 트레이드오프가 존재하며, 채널 상태에 따라 QPSK~256-QAM을 적응적으로 선택(AMC)한다.

---

## Ⅰ. BPSK (Binary Phase Shift Keying)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">BPSK 개요:</div>
<div class="kb-diagram-note">가장 단순한 PSK</div>
<div class="kb-diagram-note">2가지 위상 상태로 1비트 전송</div>
<div class="kb-diagram-note">위상 매핑:</div>
<div class="kb-diagram-note">비트 1 → 위상 0° (cos(2πft))</div>
<div class="kb-diagram-note">비트 0 → 위상 180° (-cos(2πft))</div>
<div class="kb-diagram-note">신호 표현:</div>
<div class="kb-diagram-note">s(t) = A cos(2πft + φ)</div>
<div class="kb-diagram-note">φ = 0° → 비트 1</div>
<div class="kb-diagram-note">φ = 180° → 비트 0</div>
<div class="kb-diagram-note">성상도 (Constellation Diagram):</div>
<div class="kb-diagram-note">Q축 (허수)</div>
<div class="kb-diagram-tree-item" style="--depth:1">● ●── I축 (실수)</div>
<div class="kb-diagram-note">(-1,0) (+1,0)</div>
<div class="kb-diagram-note">비트 0 비트 1</div>
<div class="kb-diagram-note">I축 위 2개 점 (동위상 / 역위상)</div>
<div class="kb-diagram-note">수신기 판별:</div>
<div class="kb-diagram-note">수신 신호의 위상이 0° 근방 → 비트 1</div>
<div class="kb-diagram-note">수신 신호의 위상이 180° 근방 → 비트 0</div>
<div class="kb-diagram-note">결정 경계: 허수(Q)축</div>
<div class="kb-diagram-note">BER (Bit Error Rate):</div>
<div class="kb-diagram-note">BPSK BER = Q(√(2Eb/N0))</div>
<div class="kb-diagram-note">Eb/N0 = 10dB (충분한 SNR)</div>
<div class="kb-diagram-note">BER ≈ 10^-5 (100,000비트 중 1개 오류)</div>
<div class="kb-diagram-note">BPSK: 가장 강한 잡음 내성</div>
<div class="kb-diagram-note">(두 점 간 거리가 최대)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: BPSK = 동전 앞뒤 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) — 앞면(0°) = 1, 뒷면(180°) = 0. 딱 두 가지만 구분하니 잡음에 강해요. 단, 한 번에 1비트만 전송!

---

## Ⅱ. QPSK (Quadrature Phase Shift Keying)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">QPSK 개요:</div>
<div class="kb-diagram-note">4가지 위상으로 심볼당 2비트 전송</div>
<div class="kb-diagram-note">= 동일 대역폭에서 BPSK의 2배 처리량</div>
<div class="kb-diagram-note">위상 매핑 (Gray Coding):</div>
<div class="kb-diagram-note">비트 00 → 위상 45° (+I, +Q)</div>
<div class="kb-diagram-note">비트 01 → 위상 135° (-I, +Q)</div>
<div class="kb-diagram-note">비트 11 → 위상 225° (-I, -Q)</div>
<div class="kb-diagram-note">비트 10 → 위상 315° (+I, -Q)</div>
<div class="kb-diagram-note">성상도 (Constellation Diagram):</div>
<div class="kb-diagram-note">Q축</div>
<div class="kb-diagram-connector">↑</div>
<div class="kb-diagram-note">● ● 01 | 00</div>
<div class="kb-diagram-note">(135°)(45°)</div>
<div class="kb-diagram-tree-item" style="--depth:1">I축</div>
<div class="kb-diagram-note">● ● 11 | 10</div>
<div class="kb-diagram-note">(225°)(315°)</div>
<div class="kb-diagram-note">4개 점이 원 위에 45° 간격으로 배치</div>
<div class="kb-diagram-note">Gray Coding 이유:</div>
<div class="kb-diagram-note">인접 심볼: 1비트만 다름</div>
<div class="kb-diagram-note">00 ↔ 01: 1비트 다름 (45°→135°)</div>
<div class="kb-diagram-note">00 ↔ 10: 1비트 다름 (45°→315°)</div>
<div class="kb-diagram-note">오류 발생 시: 대부분 1비트 오류 (2비트 방지)</div>
<div class="kb-diagram-note">QPSK vs BPSK 비교:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">특성</div><div class="kb-diagram-cell">BPSK</div><div class="kb-diagram-cell">QPSK</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">위상 수</div><div class="kb-diagram-cell">2</div><div class="kb-diagram-cell">4</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">비트/심볼</div><div class="kb-diagram-cell">1</div><div class="kb-diagram-cell">2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">대역폭 효율</div><div class="kb-diagram-cell">1bps/Hz</div><div class="kb-diagram-cell">2bps/Hz</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">BER 성능</div><div class="kb-diagram-cell">기준</div><div class="kb-diagram-cell">동등 (같은 Eb/N0)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">구현 복잡도</div><div class="kb-diagram-cell">낮음</div><div class="kb-diagram-cell">중간</div></div>
<div class="kb-diagram-note">왜 BER이 같은가?</div>
<div class="kb-diagram-note">QPSK = I채널 BPSK + Q채널 BPSK 독립 동작</div>
<div class="kb-diagram-note">각 채널: 서로 직교(Orthogonal) → 간섭 없음</div>
<div class="kb-diagram-note">→ 심볼 간 거리 유지 → 동등한 오류 성능</div>
</div>
</div>



> 📢 **섹션 요약 비유**: QPSK = 나침반 4방향 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) — 북(0°)=00, 동(90°)=01, 남(180°)=[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/), 서(270°)=[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). 4방향으로 한 번에 2비트! BPSK와 같은 도로폭으로 2배 짐을 실어요!

---

## Ⅲ. 고차 QAM으로의 진화



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">진화 과정:</div>
<div class="kb-diagram-note">BPSK (2PSK): 1비트/심볼</div>
<div class="kb-diagram-note">QPSK (4PSK): 2비트/심볼</div>
<div class="kb-diagram-note">8PSK: 3비트/심볼</div>
<div class="kb-diagram-note">16-QAM: 4비트/심볼</div>
<div class="kb-diagram-note">64-QAM: 6비트/심볼</div>
<div class="kb-diagram-note">256-QAM: 8비트/심볼</div>
<div class="kb-diagram-note">1024-QAM: 10비트/심볼</div>
<div class="kb-diagram-note">QAM (Quadrature Amplitude Modulation):</div>
<div class="kb-diagram-note">위상 + 진폭 동시 변조</div>
<div class="kb-diagram-note">PSK보다 더 많은 심볼 상태 가능</div>
<div class="kb-diagram-note">16-QAM 성상도:</div>
<div class="kb-diagram-note">4×4 격자 → 16개 점</div>
<div class="kb-diagram-note">각 점 = 4비트</div>
<div class="kb-diagram-note">SNR 요구사항 증가:</div>
<div class="kb-diagram-note">변조 방식 | 최소 SNR (BER 10^-5)</div>
<div class="kb-diagram-note">BPSK | 9.6 dB</div>
<div class="kb-diagram-note">QPSK | 9.6 dB</div>
<div class="kb-diagram-note">16-QAM | 16.5 dB</div>
<div class="kb-diagram-note">64-QAM | 22.5 dB</div>
<div class="kb-diagram-note">256-QAM | 28.5 dB</div>
<div class="kb-diagram-note">고차 QAM: 점 간 거리 좁아짐 → 잡음에 취약</div>
<div class="kb-diagram-note">AMC (Adaptive Modulation and Coding):</div>
<div class="kb-diagram-note">채널 상태에 따라 변조 방식 자동 선택</div>
<div class="kb-diagram-note">SNR 높음 (가까운 기지국): 256-QAM</div>
<div class="kb-diagram-note">SNR 낮음 (먼 기지국): QPSK or BPSK</div>
<div class="kb-diagram-note">5G NR AMC: 실시간 CQI(채널 품질 지시자) 측정</div>
<div class="kb-diagram-note">→ 매 서브프레임(1ms)마다 변조 방식 전환</div>
</div>
</div>



> 📢 **섹션 요약 비유**: QAM 진화 = 암호 복잡도 증가 — BPSK(2가지 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)), 256-QAM(256가지 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)). 가까우면 복잡한 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)로 빠르게, 멀면 단순 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)로 안전하게. AMC가 자동 선택!

---

## Ⅳ. 실제 통신 시스템 적용



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">LTE/5G에서의 변조:</div>
<div class="kb-diagram-note">LTE (4G):</div>
<div class="kb-diagram-note">다운링크: QPSK / 16-QAM / 64-QAM</div>
<div class="kb-diagram-note">업링크: QPSK / 16-QAM / 64-QAM</div>
<div class="kb-diagram-note">최대 변조: 64-QAM (6비트/심볼)</div>
<div class="kb-diagram-note">5G NR:</div>
<div class="kb-diagram-note">다운링크: QPSK ~ 256-QAM (최대 8비트/심볼)</div>
<div class="kb-diagram-note">업링크: π/2-BPSK ~ 256-QAM</div>
<div class="kb-diagram-note">π/2-BPSK: 5G 특수 BPSK</div>
<div class="kb-diagram-note">연속 심볼 간 π/2 위상 회전</div>
<div class="kb-diagram-note">→ PAPR(최대 전력 대 평균 전력비) 감소 → 배터리 효율</div>
<div class="kb-diagram-note">Wi-Fi 802.11ax (Wi-Fi 6):</div>
<div class="kb-diagram-note">1024-QAM: 10비트/심볼</div>
<div class="kb-diagram-note">이론 속도: Wi-Fi 5 대비 40% 향상</div>
<div class="kb-diagram-note">위성 통신:</div>
<div class="kb-diagram-note">BPSK: DVB-S (위성 TV 방송)</div>
<div class="kb-diagram-note">낮은 SNR 환경에서 강한 신뢰성</div>
<div class="kb-diagram-note">8PSK / 16-APSK: DVB-S2 (고급 위성)</div>
<div class="kb-diagram-note">DOCSIS (케이블 인터넷):</div>
<div class="kb-diagram-note">다운링크: 1024-QAM ~ 4096-QAM</div>
<div class="kb-diagram-note">케이블 = 유선 → 높은 SNR → 고차 QAM 가능</div>
<div class="kb-diagram-note">심볼 속도 (Baud Rate) vs 비트 레이트:</div>
<div class="kb-diagram-note">심볼 레이트 = 1000 Baud</div>
<div class="kb-diagram-note">BPSK: 1000 bps</div>
<div class="kb-diagram-note">QPSK: 2000 bps</div>
<div class="kb-diagram-note">64-QAM: 6000 bps</div>
<div class="kb-diagram-note">256-QAM: 8000 bps</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 통신 시스템 변조 선택 = 도로별 차 크기 — 위성(울퉁불퉁 도로): 작은 차(BPSK). [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)(도시 고속도로): 트럭(256-QAM). 케이블(고속도로): 대형 트럭(1024-QAM)!

---

## Ⅴ. 실무 시나리오 — [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 기지국 AMC



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">5G NR AMC 동작 예시:</div>
<div class="kb-diagram-note">단말 A: 기지국 100m 근방</div>
<div class="kb-diagram-note">측정 CQI: 15 (최고)</div>
<div class="kb-diagram-note">선택 변조: 256-QAM</div>
<div class="kb-diagram-note">코딩률: 948/1024 (약 0.93)</div>
<div class="kb-diagram-note">비트/심볼: 8 × 0.93 ≈ 7.4비트</div>
<div class="kb-diagram-note">채널 10MHz → 최대 74Mbps</div>
<div class="kb-diagram-note">단말 B: 기지국 1km 거리</div>
<div class="kb-diagram-note">측정 CQI: 7 (중간)</div>
<div class="kb-diagram-note">선택 변조: 16-QAM</div>
<div class="kb-diagram-note">코딩률: 476/1024 (약 0.46)</div>
<div class="kb-diagram-note">비트/심볼: 4 × 0.46 ≈ 1.8비트</div>
<div class="kb-diagram-note">채널 10MHz → 최대 18Mbps</div>
<div class="kb-diagram-note">단말 C: 기지국 3km 외곽</div>
<div class="kb-diagram-note">측정 CQI: 2 (낮음)</div>
<div class="kb-diagram-note">선택 변조: QPSK</div>
<div class="kb-diagram-note">코딩률: 120/1024 (약 0.12)</div>
<div class="kb-diagram-note">비트/심볼: 2 × 0.12 ≈ 0.24비트</div>
<div class="kb-diagram-note">채널 10MHz → 최대 2.4Mbps</div>
<div class="kb-diagram-note">기지국 스케줄러:</div>
<div class="kb-diagram-note">매 1ms(서브프레임)마다 단말별 CQI 수신</div>
<div class="kb-diagram-note">각 단말에 최적 변조+코딩 방식(MCS) 할당</div>
<div class="kb-diagram-note">목표: 셀 전체 처리량(Throughput) 최대화</div>
<div class="kb-diagram-note">알고리즘: Proportional Fair (PF) 스케줄링</div>
<div class="kb-diagram-note">→ 처리량 + 공정성 균형</div>
<div class="kb-diagram-note">AMC 효과:</div>
<div class="kb-diagram-note">고정 QPSK만 사용 시: 평균 5Mbps</div>
<div class="kb-diagram-note">AMC 적용 시: 평균 35Mbps</div>
<div class="kb-diagram-note">→ 7배 효율 향상</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) AMC = 도로 상황별 속도 조절 — 고속도로(가까운 기지국)엔 256-QAM으로 질주, 막히는 골목(먼 거리)엔 QPSK로 안전 운행. 매 1ms마다 자동 조정!

---

## 📌 관련 개념 맵

```
PSK/QAM 변조
+-- PSK 유형
|   +-- BPSK (1비트/심볼)
|   +-- QPSK (2비트/심볼)
|   +-- 8PSK (3비트/심볼)
+-- QAM 진화
|   +-- 16-QAM, 64-QAM
|   +-- 256-QAM, 1024-QAM
+-- 성능 지표
|   +-- BER, SNR, Eb/N0
|   +-- 성상도 (Constellation)
+-- 응용
    +-- 5G NR, LTE, Wi-Fi 6
    +-- AMC (적응 변조)
    +-- DVB (위성 방송)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[PSK 개념 (1950s)]
군사 위성 통신
BPSK 초기 적용
      |
      v
[QPSK 표준화 (1960s~)]
위성/케이블 TV 방송
효율적 대역폭 활용
      |
      v
[QAM 도입 (1980s~)]
케이블 모뎀
64-QAM, 256-QAM
      |
      v
[AMC + OFDM (LTE, 2009)]
적응 변조 도입
다중 반송파 결합
      |
      v
[5G NR 256-QAM (2019~)]
초고속 변조
Massive MIMO 결합
      |
      v
[현재: 1024-QAM 상용화]
Wi-Fi 6E, 6G 연구
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. BPSK = 동전 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) — 앞면(0°)=1, 뒷면(180°)=0. 딱 두 가지라 잡음에 강해요. 단, 한 번에 1비트만!
2. QPSK = 나침반 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) — 북/동/남/서 4방향으로 한 번에 2비트! BPSK와 같은 도로폭에서 2배 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)!
3. AMC = 도로 상황별 속도 — 고속도로(256-QAM: 빠름), 골목길(QPSK: 안전). 5G가 매 1ms마다 자동 선택!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 48 / 1120

← **이전**: [047. PSK — 위상 편이 변조](/knowledge-base/studynote/03_network/01_data_communication/047_위상_편이_변조_PSK/)
**다음**: [049. OQPSK / π/4-QPSK — 오프셋 위상 변조](/knowledge-base/studynote/03_network/01_data_communication/049_OQPSK_Pi_4_QPSK/) →

---
