+++
title = "86. CP (Cyclic Prefix) / GI (Guard Interval) - ISI 방지"
description = "OFDM 시스템에서 다중경로 간섭(ISI)을 방지하고 직교성을 유지하기 위한 순환 전치의 원리와 실무 적용"
date = 2026-03-30

[taxonomies]
tags = ["network"]

[extra]
tags = ["network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OFDM (Orthogonal Frequency Division Multiplexing)에서 CP (Cyclic Prefix)와 GI (Guard Interval)는 ISI (Inter-Symbol Interference)를 막는 보호 구간이다.
> 2. **가치**: 심볼 꼬리를 앞에 복사해 다중경로 지연을 흡수하고, FFT (Fast Fourier Transform) 구간의 직교성을 지킨다.
> 3. **판단 포인트**: CP 길이, delay spread, 효율 손실의 균형을 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

무선 통신 환경에서 신호는 직선으로만 전달되지 않는다. 건물 벽, 지형지물, 이동하는 물체 등에 의해 반사·굴절·회절되어 동일한 신호가 서로 다른 경로로, 서로 다른 시간에 수신 안테나에 도착하게 된다. 이 현상을 다중경로 전파(Multipath Propagation)라고 한다.

문제는 앞 심볼의 지연 성분이 다음 심볼 수신 구간에 침투하는 경우이다. 이것이 바로 심볼 간 간섭(ISI: Inter-Symbol Interference)이다. ISI가 발생하면 OFDM 서브캐리어들의 직교성이 깨지고, FFT 복조 과정에서 서브캐리어 간 간섭(ICI: Inter-Carrier Interference)도 동반된다. 결과적으로 수신 신호의 오류가 급격히 증가한다.

CP (Cyclic Prefix)는 이 문제를 우아하게 해결한다. 송신 심볼의 뒷부분(꼬리)을 잘라내어 심볼 앞쪽에 복사해 붙이는 것이 전부다. 이 복사된 구간이 채널의 지연 성분을 흡수하는 '쿠션' 역할을 한다. GI (Guard Interval)는 CP와 동의어로 쓰이기도 하며, 두 심볼 사이의 보호 구간 개념을 표현한다. OFDM 수신기는 CP 구간을 버리고, 이후의 유효 심볼(Useful Symbol) 구간에만 FFT를 적용하므로 직교성이 완전히 보장된다.

이 메커니즘은 4G LTE, 5G NR, Wi-Fi 4/5/6/7, DVB-T/T2 등 현대의 모든 OFDM 기반 통신 표준에서 필수적으로 적용되고 있다.

- **📢 섹션 요약 비유**: 빗속에서 달려 집에 들어오기 전에 현관 앞 발판에서 비를 털어내는 것과 같다. 빗물(다중경로 지연 성분)이 집 안(유효 심볼 구간)으로 들어오기 전에 현관(CP/GI)에서 걸러진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### CP 삽입 과정 (송신 측)

OFDM 심볼은 IFFT (Inverse Fast Fourier Transform)를 통해 주파수 도메인 서브캐리어를 시간 도메인 신호로 변환하여 생성된다. CP는 이 시간 도메인 신호의 마지막 N_CP 샘플을 앞에 복사하여 추가한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">원래 OFDM 심볼</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">&lt;----------- N_FFT 샘플 (유효 심볼) -----------&gt;</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">CP 삽입 후</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">&lt;- N_CP 샘플 (CP) -&gt;</div><div class="kb-diagram-cell">&lt;--- N_FFT 샘플 (유효 심볼) ---&gt;</div></div>
<div class="kb-diagram-note">(끝부분 복사)</div>
<div class="kb-diagram-note">총 전송 길이: N_total = N_CP + N_FFT</div>
<div class="kb-diagram-note">CP 길이: N_CP &gt;= 최대 채널 지연 확산(Maximum Delay Spread) / 샘플 주기</div>
</div>
</div>



### CP 수신 및 제거 과정 (수신 측)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">수신 신호 (다중경로 영향)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">&lt;-- CP 수신 구간 --&gt;</div><div class="kb-diagram-cell">&lt;------- 유효 심볼 구간 -------&gt;</div></div>
<div class="kb-diagram-note">↓ CP 제거</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">&lt;------- 유효 심볼 구간 -------&gt;</div></div>
<div class="kb-diagram-note">↓ FFT 적용</div>
<div class="kb-diagram-note">서브캐리어 복조 → 직교성 유지</div>
</div>
</div>



### 핵심 구성 요소 표

| 구성 요소 | 의미 | 설계 포인트 |
|:---|:---|:---|
| CP (Cyclic Prefix) | 심볼 끝부분을 앞에 복사한 접두사 | 채널 최대 지연 확산보다 길어야 함 |
| GI (Guard Interval) | CP와 동의어, 보호 구간 개념 | ISI와 ICI 동시 방지 |
| Delay Spread | 다중경로 신호들의 도착 시간 폭 | CP 길이 결정 기준 |
| FFT Window | 실제 FFT를 적용하는 유효 심볼 구간 | CP 제거 후 시작 |
| 전송 효율 | N_FFT / (N_FFT + N_CP) | CP가 길수록 효율 저하 |

### CP 길이별 표준 규격

| 표준 | 서브캐리어 간격 | 유효 심볼 길이 | 일반 CP 길이 | 확장 CP 길이 |
|:---|:---|:---|:---|:---|
| LTE (4G) | 15 kHz | 66.7 us | 4.7 us (~7%) | 16.7 us (1심볼) |
| 5G NR (mu=0) | 15 kHz | 66.7 us | 4.7 us | - |
| 5G NR (mu=1) | 30 kHz | 33.3 us | 2.3 us | - |
| Wi-Fi 4 (802.11n) | 312.5 kHz | 3.2 us | 0.8 us (~25%) | - |
| Wi-Fi 6 (802.11ax) | 78.125 kHz | 12.8 us | 0.8 us (~6%) | 1.6/3.2 us |

### 순환 전치의 수학적 의미

CP는 단순한 보호 구간 이상의 의미를 가진다. CP를 삽입하면 채널에 의한 선형 컨볼루션(Linear Convolution)이 순환 컨볼루션(Circular Convolution)으로 변환된다. 주파수 도메인에서 순환 컨볼루션은 원소별 곱셈(Element-wise Multiplication)과 동치이므로, FFT 후 각 서브캐리어에 대해 단순한 1탭 등화(Equalization)만으로 채널 보상이 가능해진다.

```text
채널 h[n]과 심볼 x[n]의 관계:
  선형 컨볼루션: y = h * x  (복잡한 등화 필요)
  CP 적용 시:  y = h ⊛ x  (순환 컨볼루션 → FFT 후 단순 나눗셈으로 등화)
```

- **📢 섹션 요약 비유**: 순환 컨볼루션 변환은 마치 원형 트랙에서 달리기와 같다. 직선 트랙(선형 컨볼루션)에서는 출발점과 도착점이 달라 복잡하지만, 원형 트랙(순환 컨볼루션)에서는 돌고 돌아도 계산이 단순해진다.

---

## Ⅲ. 비교 및 연결

### CP 유형 비교

| 비교 항목 | Normal CP | Extended CP | CP 없음 |
|:---|:---|:---|:---|
| 길이 | 표준 설계값 | Normal CP의 약 2~4배 | 0 (이론상) |
| 적합 환경 | 일반 도심·교외 셀 | 대형 셀, 고속 이동, 연안 환경 | 존재하지 않음 |
| ISI 방지 능력 | 대부분 환경 커버 | 큰 지연 확산도 흡수 | 불가능 |
| 전송 효율 | 높음 (~93%) | 낮음 (~80%) | 100% (이론) |
| 실무 사용 | 대다수 기지국 | 특수 환경(MBSFN 등) | 사용 불가 |

### 관련 기술과의 연결 관계

| 관련 기술 | 연결 포인트 |
|:---|:---|
| OFDM (다중반송파 변조) | CP의 존재 이유. ISI 없이 서브캐리어 직교성 보장 |
| FFT/IFFT | CP 제거 후 적용. 주파수-시간 도메인 변환 핵심 |
| 채널 등화 (Equalization) | CP 덕분에 1탭 등화로 단순화 |
| 파일럿 신호 (Pilot) | CP와 함께 채널 추정에 사용 |
| 다중 안테나 (MIMO) | CP 메커니즘을 다중 경로·공간 영역으로 확장 |
| SC-FDMA | 4G LTE 업링크에서 CP를 유지하며 PAPR 개선 |

### OFDM vs 단일 반송파 비교

| 특성 | OFDM + CP | 단일 반송파 |
|:---|:---|:---|
| ISI 처리 | CP로 간단히 해결 | 복잡한 등화기 필요 |
| PAPR (Peak-to-Average Power Ratio) | 높음 (단점) | 낮음 |
| 주파수 효율 | CP 오버헤드만큼 감소 | CP 없음 |
| 구현 복잡도 | FFT 기반, 상대적 단순 | 적응형 등화기 복잡 |

- **📢 섹션 요약 비유**: CP가 있는 OFDM과 없는 단일 반송파는 고속도로(구조화된 차선 = 서브캐리어)와 비포장 도로의 차이다. 고속도로는 구조 덕분에 빠르지만, 진입로(CP)가 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **CP 길이 ≥ 채널 최대 지연 확산인가?**: 도심 환경 delay spread는 일반적으로 수 us 이내지만, 산악·해안·대형 실내 등 특수 환경에서는 수십 us에 달할 수 있다.
2. **동기 오차(Timing Error)가 CP 범위 안에 있는가?**: 수신기의 타이밍 동기 오차가 CP 길이를 초과하면 ISI가 발생한다.
3. **CP 오버헤드로 인한 효율 손실이 허용 범위인가?**: CP 길이/총 심볼 길이 비율만큼 전송 효율이 감소한다.
4. **고속 이동 환경인가?**: 도플러 효과에 의한 ICI도 고려해야 한다. CP만으로는 ICI를 완전히 해결할 수 없다.
5. **시스템이 Extended CP를 지원하는가?**: LTE MBSFN(Multicast Broadcast Single Frequency Network)처럼 특수 용도에서는 Extended CP가 필수다.

### 주요 적용 시나리오

| 시나리오 | CP 전략 | 이유 |
|:---|:---|:---|
| 도심 4G/5G 소형 셀 | 일반 CP | 지연 확산 작음, 효율 우선 |
| 농촌·해안 광역 셀 | Extended CP | 지연 확산 클 수 있음 |
| LTE MBSFN 방송 | Extended CP (확장) | 다수 기지국 신호 합성 |
| Wi-Fi 6 실내 | 0.8/1.6/3.2 us 선택 | 환경별 지연 확산 대응 |
| 위성 통신 OFDM | 매우 긴 CP | 전파 왕복 지연 대응 |

### 안티패턴

- **CP 무조건 최소화**: 전송 효율을 높이려고 CP를 줄이다가 지연 확산이 CP를 초과하면 ISI 폭증으로 서비스 불가 상태가 된다.
- **환경 무관 단일 CP 적용**: 실내와 실외, 도심과 농촌에 동일한 CP 길이를 적용하면 어느 환경에서도 최적이 아닌 타협점이 된다.
- **지연 확산 측정 생략**: 실측 채널 프로파일(Channel Delay Profile) 없이 이론값만 참고하면 실환경에서 예상 밖의 ISI가 발생할 수 있다.
- **도플러 효과 간과**: CP가 ISI를 막아도 고속 이동 환경에서는 ICI가 별도로 발생한다. 이는 CP로 해결되지 않으며 별도의 ICI 보상 알고리즘이 필요하다.

- **📢 섹션 요약 비유**: CP 설계는 우산의 크기와 같다. 너무 작으면 비를 맞고, 너무 크면 들고 다니기 불편하다. 환경에 맞는 크기를 골라야 한다.

---

## Ⅴ. 기대효과 및 결론

CP/GI는 수십 년간 OFDM 시스템의 핵심 메커니즘으로 자리잡아 왔으며, 5G NR에서도 다양한 서브캐리어 간격(Numerology)에 맞춰 다양한 CP 길이가 정의된다. CP는 약 6~25%의 전송 오버헤드를 감수하는 대신, 다중경로 채널에서의 안정적 복조를 가능하게 한다는 점에서 현실적인 최선의 타협점이다.

미래 통신에서도 CP 개념은 유지된다. 6G에서 논의 중인 OTFS (Orthogonal Time Frequency Space) 변조 방식은 시간-지연 도메인에서 전송함으로써 고속 이동 환경에서 더 효율적인 ISI/ICI 관리를 추구하지만, 그 기반에도 CP와 유사한 보호 구간 개념이 적용된다.

기술사 관점에서 CP를 설명할 때는 단순한 오버헤드가 아니라, 순환 컨볼루션 변환을 통한 채널 등화 단순화라는 수학적 근거를 함께 제시하는 것이 핵심이다.

- **📢 섹션 요약 비유**: 비 오는 날 현관문 앞에 발판을 두면 집 안이 깨끗이 유지된다. CP는 그 발판이다. 발판(CP)의 비용은 작지만, 집 안(유효 심볼)이 지저분해지는(ISI) 것을 막는 효과는 크다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| OFDM (Orthogonal Frequency Division Multiplexing) | 다중반송파 변조의 기본. CP가 존재하는 이유 |
| ISI (Inter-Symbol Interference) | CP가 방지하는 핵심 문제 |
| ICI (Inter-Carrier Interference) | 직교성 붕괴 시 발생. CP로 부분 방지 |
| FFT (Fast Fourier Transform) | CP 제거 후 적용하는 복조 핵심 알고리즘 |
| Delay Spread (지연 확산) | CP 길이 결정 기준값 |
| LTE/5G NR Numerology | 다양한 서브캐리어 간격별 CP 규격 |
| MIMO (다중 안테나) | CP와 함께 공간 다중화 활용 |
| SC-FDMA | LTE 업링크, CP 유지하며 PAPR 개선 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">무선 채널 다중경로 문제 인식</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">단일 반송파 → 복잡한 등화기 필요</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">OFDM 등장 → 서브캐리어 직교성 활용</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">CP (Cyclic Prefix) 도입 → ISI 방지 + 순환 컨볼루션 변환</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">4G LTE → Normal CP (4.7us) / Extended CP (16.7us) 표준화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">5G NR → Numerology별 다양한 CP 길이 (15~120kHz 서브캐리어 간격)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Wi-Fi 6 (802.11ax) → 환경별 CP 선택 (0.8/1.6/3.2us)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">미래 6G → OTFS 등 새로운 변조 방식도 CP 개념 유지</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 바다에서 파도가 치면 같은 파도가 여러 방향에서 조금씩 다른 시간에 도착해요. 이게 신호가 여러 경로로 오는 것과 같아요.
2. CP는 문 앞에 두는 발판 같아요. 늦게 도착한 파도(지연된 신호)가 중요한 방(유효 심볼)으로 들어오기 전에 발판에서 멈추게 해요.
3. 그래서 수신기는 발판 구간은 버리고 중요한 방 구간만 깨끗하게 읽을 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 86 / 1120

← **이전**: [85. 부반송파 (Subcarrier)](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/085_부반송파_Subcarrier/)
**다음**: [87. 다중 접속 (Multiple Access) 개념 (MAC 계층 연관)](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) →

---
