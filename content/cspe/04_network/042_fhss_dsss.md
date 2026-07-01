---
title: "FHSS·DSSS 확산 스펙트럼 (FHSS DSSS)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 42
---

# 📖 【암기용】 개념 완전 이해

> 목적: FHSS·DSSS를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 원 신호보다 넓은 대역에 에너지를 퍼뜨려 간섭·도청·재밍 영향을 줄이는 확산 스펙트럼 방식
- **왜 필요한가**: 무선 채널은 협대역 간섭, 의도적 재밍, 다중 사용자 충돌이 발생한다. 확산 스펙트럼은 송수신자가 공유한 코드나 홉 패턴으로 신호를 분산해 복원한다.
- **핵심 직관**: FHSS는 주파수 채널을 계속 옮겨 다니고, DSSS는 신호를 짧은 칩 코드로 잘게 펼쳐 보낸다.

## 깊이 이해
- **배경·문제의식**: 좁은 주파수에 에너지를 집중하면 해당 대역 간섭에 취약하다. 확산 스펙트럼은 필요한 대역폭보다 넓게 전송해 특정 대역 손상에 대한 영향을 낮춘다.
- **작동 원리**: FHSS는 의사난수 홉 시퀀스에 따라 반송파 주파수를 바꾼다. DSSS는 데이터 비트에 PN 코드 칩을 곱해 대역을 넓히고, 수신기는 같은 코드로 역확산한다.
- **비유**: FHSS는 여러 방을 순서대로 옮겨 다니며 대화하는 방식이고, DSSS는 한 문장을 여러 조각 암호표로 펼친 뒤 같은 암호표를 가진 사람이 조립하는 방식이다.
- **구체 예시**: Bluetooth Classic은 2.4 GHz ISM 대역에서 79개 1 MHz 채널을 초당 1,600회 hopping한다. IEEE 802.11b는 11-chip Barker code 기반 DSSS를 사용했다.
- **흔한 오해·주의점**: 확산 스펙트럼은 암호화와 다르다. 코드나 홉 패턴이 노출되면 물리계층 은닉 효과가 줄어들므로 상위 계층 암호화가 별도로 필요하다.

## 연결 개념
- CDMA - DSSS와 코드 분리 다중 접속을 결합한 이동통신 방식
- Bluetooth - FHSS 기반 근거리 무선 통신
- Anti-jamming - 재밍 환경에서 확산 이득과 주파수 다양성 활용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: FHSS와 DSSS를 모두 확산 스펙트럼으로 묶되, 확산 방법·동기 방식·간섭 대응·적용 사례를 비교 축으로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FHSS는 주파수를 시간에 따라 hopping하고, DSSS는 PN code로 데이터를 chip 단위 확산하는 물리계층 간섭 완화 기술이다.
> 2. **가치**: Processing Gain과 주파수 다양성으로 협대역 간섭·재밍 영향을 낮추고 다중 사용자 분리 기반을 제공한다.
> 3. **판단 포인트**: 홉 동기, 코드 상관, 대역폭 사용량, 규제 대역, 상위 계층 암호화 필요성을 함께 판단해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 확산 스펙트럼 원리 확인 | FHSS hopping, DSSS PN code, processing gain | FHSS와 DSSS를 단순 변조 방식으로 설명 |
| 무선 간섭 대응 판단 확인 | 협대역 간섭, 재밍, 다중 사용자 분리 | 암호화와 확산 효과 혼동 |
| 적용 사례 구분 확인 | Bluetooth FHSS, 802.11b DSSS, CDMA | Wi-Fi 최신 규격까지 DSSS로 단정 |

> 요약: 이 문제는 확산 방식별 물리계층 원리와 간섭·보안 한계를 구분하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 대역을 넓혀 신호를 전송하는 방식
- 배경: 협대역 간섭과 재밍은 단일 주파수 전송의 오류율을 높임
- 필요성: hopping pattern 또는 PN code 동기로 확산 이득과 다중 사용자 분리를 확보

---

## Ⅱ. 구조 및 구성요소

```text
Data -> Spreading Control
  / FHSS: PN Sequence -> Frequency Synthesizer -> Hopping Carrier
  / DSSS: PN Code -> Chip Spreading -> Wideband Signal
Receiver -> Synchronization -> Despreading -> Data Recovery
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| PN Sequence/Code | 송수신 공유 확산 패턴 생성 | 코드 길이와 상관 특성이 확산 이득 결정 |
| FHSS Synthesizer | 홉 패턴에 따라 반송파 변경 | Bluetooth Classic 1,600 hops/s |
| DSSS Spreader | 데이터 비트를 chip stream으로 확산 | 802.11b Barker 11-chip 사례 |
| 동기 회로 | 홉 타이밍·코드 위상 정렬 | 동기 실패 시 역확산 불가 |

> 요약: FHSS는 주파수 합성기와 홉 패턴, DSSS는 PN 코드와 역확산 상관기가 핵심 구성이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
송신 데이터 -> PN 생성 -> 확산 방식 선택
  / FHSS: 홉 주파수 선택 -> 협대역 송신
  / DSSS: 칩 확산 -> 광대역 송신
수신 동기 -> 역확산/복조 -> 데이터 복원
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 송수신자가 동일 PN sequence 또는 code 확보 | 코드 충돌률, seed 관리 |
| 2 | FHSS는 hop dwell time마다 반송파 변경 | hop timing 오차, 채널 점유 규제 |
| 3 | DSSS는 데이터 비트와 chip code를 곱해 확산 | chip rate/data rate 비율 |
| 4 | 수신기는 동기 획득 후 역확산 수행 | correlation peak, BER |
| 5 | 간섭 구간은 확산 이득으로 영향 분산 | processing gain, PER |

> 요약: 확산 스펙트럼은 송신 확산과 수신 역확산이 같은 코드·타이밍에서 맞을 때 데이터가 복원된다.

---

## Ⅳ. 특징

| 구분 | FHSS | DSSS | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 확산 방식 | 시간별 주파수 hopping | PN code chip 확산 | hop rate, chip rate |
| 간섭 대응 | 특정 채널 간섭 시 다음 hop으로 회피 | 협대역 간섭을 역확산 후 분산 | processing gain dB |
| 동기 요구 | hop sequence·dwell time 동기 | code phase 동기 | acquisition time |
| 적용 사례 | Bluetooth Classic | 802.11b, CDMA | ISM 대역 규제와 공존성 |

> 요약: FHSS는 주파수 다양성, DSSS는 코드 상관 이득을 활용하므로 동기·대역폭·적용 시스템 기준이 다르다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | FHSS·DSSS | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 협대역 고정 채널 | 확산 대역 전송 | 간섭 밀도와 규제 대역폭 |
| 비용/성능 | RF 단순, 간섭 취약 | 동기·코드 처리 필요 | 단말 전력과 BER 목표 |
| 운영/위험 | 채널 충돌 직접 영향 | 코드/홉 관리 필요 | 키 관리, 공존성, 스캔 정책 |

> 요약: 간섭 회피가 목표이면 FHSS, 코드 분리와 역확산 이득이 목표이면 DSSS 계열을 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 동기 실패 | hop timing 또는 code phase 불일치 | preamble, acquisition loop, tracking loop | acquisition time, sync loss |
| 재밍 대응 한계 | 광대역 재밍 또는 패턴 노출 | hop set 변경, adaptive hopping, 상위 암호화 | PER, jammed channel ratio |
| 공존성 저하 | ISM 대역 Wi-Fi·Bluetooth 중첩 | AFH, 채널 마스크, 출력 제한 | channel occupancy, collision rate |

> 요약: 확산 스펙트럼의 운영 리스크는 동기와 공존성이며, PER·동기 손실·채널 점유율로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 링크 품질 | BER/PER 목표 만족 | 패킷 캡처, RF 시험기 |
| 확산 이득 | processing gain 산정 | chip rate/data rate, jammer test |
| 대역 공존 | 채널 충돌률·점유율 측정 | 스펙트럼 분석, AFH 로그 |

> 요약: FHSS·DSSS 검증은 링크 품질, 확산 이득, 대역 공존성을 함께 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 근거리 IoT: 2.4 GHz ISM 혼잡도가 높으면 FHSS/AFH로 간섭 채널을 제외하고 PER 기준으로 hop set을 조정함
2. DSSS 계열 설계: chip rate/data rate 비율로 processing gain을 산정하고 correlation peak 기반 동기 획득 시간을 시험함
3. 보안 설계: 확산 코드 은닉만 의존하지 않고 AES-CCM, TLS, 인증키 교체 주기를 상위 계층에 적용함

**결론 (2줄):**
- 기술사 판단: FHSS는 주파수 회피, DSSS는 코드 역확산 이득이 핵심이며 간섭 유형과 단말 전력 조건으로 선택함
- 향후 방향: 협대역 IoT·군집 센서·재밍 환경에서는 adaptive hopping과 상위 계층 암호화 결합이 요구됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "확산 스펙트럼을 설명하시오" | PN code, hopping, 역확산 원리 | FHSS/DSSS 비교와 적용 사례 |
| 요구사항 명시형 | "간섭 대응 방안을 제시하시오" | 재밍·협대역 간섭 흐름 | AFH, processing gain, 공존성 지표 |

> 요약: 설명형은 두 방식의 원리, 방안형은 간섭 유형별 선택 기준과 검증 지표 중심으로 전개한다.
