---
title: "5G SA 독립형·NSA 비독립형 (5G SA NSA)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 44
---

# 📖 【암기용】 개념 완전 이해

> 목적: 5G SA·NSA를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: NSA는 LTE EPC를 기반으로 5G NR을 보조 무선망으로 붙이고, SA는 5G Core와 5G NR만으로 동작하는 구축 방식
- **왜 필요한가**: 이동통신사는 기존 LTE 투자와 커버리지를 활용하면서 5G를 빨리 도입해야 했다. NSA는 초기 상용화 경로, SA는 5G 고유 기능을 위한 목표 구조이다.
- **핵심 직관**: NSA는 LTE 건물에 5G 증축동을 붙인 형태이고, SA는 5G 전용 설계로 새 건물을 세운 형태이다.

## 깊이 이해
- **배경·문제의식**: 5G 초기에는 5G Core 구축과 전국망 커버리지 확보가 동시에 어렵다. NSA는 LTE eNB와 EPC를 제어 앵커로 사용해 5G NR 속도를 먼저 제공했다.
- **작동 원리**: NSA Option 3 계열은 LTE eNB가 제어면 anchor가 되고 NR gNB가 데이터 용량을 보조한다. SA Option 2는 UE가 gNB를 통해 5GC에 직접 접속하고 AMF·SMF·UPF 기반 세션을 설정한다.
- **비유**: NSA는 기존 고속도로 요금소를 그대로 쓰면서 5G 차로를 추가하는 방식이고, SA는 요금소·도로·관제 시스템을 모두 5G 방식으로 바꾸는 방식이다.
- **구체 예시**: NSA는 eMBB 조기 제공에 적합하지만 5GC 기반 slicing, URLLC, SBA, UPF local breakout은 SA에서 본격 적용된다.
- **흔한 오해·주의점**: NSA도 5G NR을 사용하므로 5G가 아니다라는 표현은 부정확하다. 다만 5G Core 고유 기능은 SA에서 구현 범위가 넓다.

## 연결 개념
- 5G Core SBA - SA에서 AMF·SMF·UPF가 서비스 기반 구조로 동작
- Dual Connectivity - NSA에서 LTE와 NR을 동시에 사용하는 구조
- Network Slicing - SA 구축 이후 서비스별 논리망 분리의 핵심

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SA/NSA를 세대 우열로 쓰지 않고 EPC/5GC, 제어면 anchor, 기능 범위, 전환 전략 기준으로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NSA는 LTE EPC·eNB를 제어 anchor로 활용하는 5G NR 조기 구축 방식이고, SA는 5G NR과 5GC 기반 독립 운용 방식이다.
> 2. **가치**: NSA는 기존 LTE 투자 활용과 eMBB 조기 제공, SA는 slicing·URLLC·SBA·UPF 분산 등 5G 고유 기능 구현에 적합하다.
> 3. **판단 포인트**: 커버리지, 단말 호환성, EPC/5GC 투자, 서비스 SLA, 전환 기간의 이중 운용 비용을 함께 평가해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 5G 구축 옵션 이해 확인 | NSA Option 3, SA Option 2, EPC vs 5GC | NSA를 LTE와 동일하다고 단정 |
| 전환 전략 판단 확인 | eMBB 조기 제공과 SA 고유 기능 구분 | SA 장점만 쓰고 구축 비용 누락 |
| 코어망 구조 이해 확인 | AMF·SMF·UPF, SBA, UPF local breakout | 무선망 비교만 하고 코어망 누락 |

> 요약: 이 문제는 NSA와 SA의 제어면·코어망 차이와 서비스 전환 전략을 구분하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 5G 무선망과 코어망 결합 방식
- 배경: NSA는 LTE EPC를 재사용하지만 SA는 5GC 기반 기능을 전제로 함
- 필요성: 구축 기간, EPC 의존, slicing, URLLC, MEC 적용 범위를 기준으로 방식을 선택

---

## Ⅱ. 구조 및 구성요소

```text
NSA Option 3: UE -> LTE eNB Anchor -> EPC
                      / NR gNB Secondary for user data
SA Option 2: UE -> NR gNB -> 5GC
                      / AMF -> SMF -> UPF -> Data Network
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| LTE eNB/EPC | NSA 제어 anchor와 기존 코어 기능 제공 | EPC 기반 bearer, LTE 커버리지 활용 |
| NR gNB | 5G 무선 접속 제공 | NSA 보조 노드 또는 SA 단독 노드 |
| 5GC | SA에서 세션·이동성·정책 제어 | AMF·SMF·UPF·PCF 등 SBA |
| 단말 | NSA/SA 모드 지원 필요 | VoNR, EN-DC, NR band 지원 확인 |

> 요약: NSA는 LTE anchor와 NR 보조 노드의 결합이고, SA는 NR gNB가 5GC와 직접 연결되는 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 요구 확인 -> 구축 옵션 선택
  / NSA: LTE attach -> EN-DC 설정 -> NR bearer 추가 -> EPC 처리
  / SA: NR registration -> AMF 인증 -> SMF PDU Session -> UPF 경로 설정
운영 KPI 측정 -> SA 전환 계획 조정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 단말·커버리지·코어망 준비 상태 확인 | NSA/SA 단말 비율, NR coverage |
| 2 | NSA는 LTE anchor 후 NR secondary cell 추가 | EN-DC success rate |
| 3 | SA는 AMF 등록 후 SMF가 PDU Session 생성 | registration success, PDU success |
| 4 | UPF 위치와 QoS Flow로 서비스 경로 설정 | latency, packet loss |
| 5 | VoNR·handover·roaming 검증 후 전환 확대 | call setup time, handover fail |

> 요약: NSA는 LTE 절차 위에 NR 용량을 추가하고, SA는 5GC 등록·세션·UPF 경로로 5G 기능을 직접 제공한다.

---

## Ⅳ. 특징

| 구분 | NSA | SA | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 코어망 | EPC 사용 | 5GC 사용 | AMF/SMF/UPF 도입 여부 |
| 구축 목적 | eMBB 조기 제공 | slicing·URLLC·MEC 구현 | 서비스 SLA와 출시 일정 |
| 제어면 | LTE eNB anchor | NR gNB와 AMF 연결 | EN-DC vs N2/N3 |
| 운영 부담 | LTE/NR 이중 의존 | 5GC 신규 운영 | VoNR, roaming, 관측성 |

> 요약: NSA는 빠른 상용화 경로, SA는 5G 고유 서비스 확장 경로이며 코어망 전환이 핵심 차이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | SA/NSA 판단 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | LTE EPC 단독 | NSA 후 SA 전환 | 5GC 준비도와 NR 커버리지 |
| 비용/성능 | 기존망 유지 | 5GC·UPF·VoNR 투자 | eMBB 매출, 산업망 SLA |
| 운영/위험 | LTE 운영 체계 | 듀얼코어·SA 운영 자동화 | 장애 격리와 전환 리스크 |

> 요약: 초기 커버리지와 단말 호환성이 우선이면 NSA, slicing·MEC·URLLC 요구가 있으면 SA를 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| SA 전환 지연 | VoNR·roaming·단말 비율 부족 | NSA/SA 병행, 단계별 지역 전환 | SA traffic ratio |
| 품질 저하 | EN-DC 실패 또는 N2/N3 장애 | 커버리지 튜닝, gNB-CU/DU 점검 | EN-DC success, PDU success |
| 운영 복잡도 | EPC와 5GC 이중 운용 | OSS 통합, NWDAF/PM 연계 | incident MTTR, alarm correlation |

> 요약: 전환 리스크는 단말·코어·운영 체계가 동시에 맞아야 낮아지며 SA 트래픽 비율과 세션 성공률로 확인한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 접속 성공 | registration/PDU success 99% 이상 | AMF/SMF 로그, PM 카운터 |
| 서비스 지연 | MEC 경로 E2E latency 목표 | probe, UPF 로그 |
| 전환 품질 | handover fail, VoNR drop | drive test, CDR 분석 |

> 요약: SA/NSA 평가는 접속 성공률, 세션 지연, 핸드오버·음성 품질을 함께 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. NSA 단계: EN-DC success rate, NR coverage, eMBB throughput을 기준으로 LTE anchor 품질과 NR 보조 셀 용량을 검증함
2. SA 단계: AMF/SMF/UPF, N2/N3, VoNR, PDU Session 성공률 99% 이상을 목표로 상용 검증함
3. 전환 운영: 지역·단말·서비스별 SA traffic ratio를 추적하고 MEC·slicing 요구 서비스부터 SA 우선 적용함

**결론 (2줄):**
- 기술사 판단: NSA는 eMBB 조기 제공, SA는 5GC 기반 서비스 차별화가 목적이므로 사업 목표와 SLA 기준으로 선택함
- 향후 방향: 5G-Advanced와 private 5G 확산에 따라 SA 기반 slicing·NWDAF·UPF 분산 운영 비중이 증가함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SA와 NSA를 설명하시오" | NSA attach/EN-DC와 SA registration/PDU 흐름 | EPC vs 5GC, 기능 범위 비교 |
| 요구사항 명시형 | "SA 전환 방안을 제시하시오" | 전환 단계, VoNR, UPF, slicing 적용 | 전환 리스크와 KPI 점검표 |

> 요약: 설명형은 구조 차이, 방안형은 NSA에서 SA로 이동하는 운영·검증 절차 중심으로 작성한다.
