---
title: "PDH·SDH·SONET 디지털 계위 (PDH SDH SONET)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 83
---

# 📖 【암기용】 개념 완전 이해

> 목적: PDH, SDH, SONET을 처음 봐도 디지털 전송망 계위와 동기화의 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 음성·데이터를 TDM으로 묶어 전송하는 디지털 전송망 계위
- **왜 필요한가**: 통신망은 낮은 속도 회선을 모아 장거리 백본으로 보내야 한다. 계위가 있어야 회선 증설, 절체, 운용관리 기준이 맞는다.
- **핵심 직관**: PDH는 각 장비 시계가 조금씩 다른 묶음 방식이고, SDH/SONET은 공통 시계와 포인터로 원하는 신호를 바로 꺼내는 방식이다.

## 깊이 이해
- **배경·문제의식**: PDH는 북미 T1, 유럽 E1 계위가 다르고 장비별 클록 편차를 stuffing bit로 보정한다. 중간 회선을 꺼내려면 상위 계위를 단계적으로 역다중화해야 한다.
- **작동 원리**: SDH/SONET은 동기식 프레임과 pointer를 사용한다. SONET STS-1은 51.84Mbps, SDH STM-1은 155.52Mbps로 국제 전송망 기준을 제공한다.
- **비유**: PDH는 크기가 조금씩 다른 상자를 겹겹이 포장한 택배이고, SDH/SONET은 위치표가 붙은 표준 컨테이너라 중간 화물을 바로 찾는다.
- **구체 예시**: STM-1 155.52Mbps는 OC-3와 대응하고, STM-4 622.08Mbps, STM-16 2.488Gbps로 확장된다.
- **흔한 오해·주의점**: SDH/SONET은 단순 속도 이름이 아니다. OAM, 보호절체, 포인터 처리, 동기망 설계까지 포함한다.

## 연결 개념
- TDM — 시간 슬롯 기반 다중화 원리
- WDM/DWDM — 광 파장 기반 전송 용량 확장
- MPLS-TP/OTN — 전송망 운용관리의 후속 구조

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 디지털 계위 문제는 속도 암기가 아니라 비동기 PDH 한계와 동기식 SDH/SONET의 운용관리 구조를 비교해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PDH·SDH·SONET은 저속 회선을 계층적으로 다중화해 장거리 전송망으로 운반하는 디지털 전송 계위이다.
> 2. **가치**: SDH/SONET은 동기 프레임, pointer, overhead로 회선 add/drop, OAM, 50ms 보호절체를 제공한다.
> 3. **판단 포인트**: PDH의 단계적 역다중화 한계와 SDH/SONET의 표준 속도(OC-n, STM-n), 운용관리 기능을 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 전송망 계위 이해 확인 | PDH 비동기, SDH/SONET 동기, TDM | 속도명만 나열 |
| 표준 속도 적용 확인 | STS-1 51.84Mbps, STM-1 155.52Mbps, OC-n | SDH와 SONET 대응 관계 누락 |
| 운용관리 판단 확인 | overhead, pointer, add/drop, protection | 단순 다중화 장비로만 설명 |

> 요약: 이 문제는 디지털 전송망의 계위, 동기화, 운용관리 기능을 한 구조로 묶어 쓰는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

PDH·SDH·SONET은 회선 기반 디지털 전송망 계위이다.
음성·전용회선·초기 데이터망은 저속 회선을 다중화해 백본으로 전달해야 했고, 장거리 전송망은 표준화된 속도와 장애 절체가 필요했다.
PDH는 비동기 계위의 한계가 있었고, SDH/SONET은 동기식 프레임과 OAM으로 대규모 전송망 운용 기준을 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
Tributary Signal -> Multiplexer -> Digital Hierarchy
                 / PDH: E1/T1 -> E3/T3
                 / SONET: STS-1 -> OC-n
                 / SDH: STM-1 -> STM-n
-> Add/Drop Multiplexer -> Optical Transport
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| PDH | 비동기식 계위 다중화 | T1 1.544Mbps, E1 2.048Mbps |
| SONET | 북미 동기식 광 전송 표준 | STS-1/OC-1 51.84Mbps |
| SDH | ITU-T 동기식 전송 표준 | STM-1 155.52Mbps |
| ADM | 중간 회선 add/drop | 포인터 기반 접근 |

> 요약: PDH는 저속 계위 묶음, SDH/SONET은 동기 프레임 기반 광 전송망과 ADM 운용을 제공함.

---

## Ⅲ. 동작원리 및 흐름도

```text
저속 회선 수용 -> TDM 매핑 -> 계위 프레임 생성
-> Overhead 삽입 -> 광 전송
-> Pointer 기반 추출 -> 보호절체/OAM
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | T1/E1 등 tributary 신호 수용 | 회선 속도, clock slip |
| 2 | PDH stuffing 또는 SDH/SONET mapping | pointer adjustment count |
| 3 | section/line/path overhead 삽입 | B1/B2/B3 error |
| 4 | ADM에서 회선 추출·삽입 | 50ms protection switching |

> 요약: SDH/SONET은 동기 프레임과 overhead를 이용해 전송, 감시, 회선 추출, 보호절체를 함께 수행함.

---

## Ⅳ. 특징

| 구분 | PDH | SDH/SONET | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 동기 방식 | plesiochronous, clock 편차 허용 | network synchronous | PRC, SSU 클록 |
| 회선 추출 | 단계적 역다중화 필요 | ADM에서 직접 add/drop | pointer 기반 |
| 표준 속도 | T1/E1, T3/E3 | OC-1 51.84Mbps, STM-1 155.52Mbps | OC-3 = STM-1 |
| 운용관리 | 제한적 overhead | section/line/path OAM | 50ms APS |

> 요약: SDH/SONET은 PDH의 비동기·역다중화 한계를 동기식 프레임과 OAM으로 보완한 전송 계위임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | SDH/SONET | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | PDH 계단식 mux | 동기식 ADM, ring | 회선 add/drop 빈도 |
| 비용/용량 | 저속 회선 중심 | STM-n/OC-n 확장 | 회선 수, 보호절체 요구 |
| 운영/위험 | 장비별 클록 편차 | 동기망 클록 관리 | clock slip, pointer event |

> 요약: 회선 기반 전송과 50ms 보호절체가 필요하면 SDH/SONET, 패킷 통합망은 OTN/MPLS-TP와 비교함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 클록 슬립 | 동기 기준 불량 | PRC/SSU 구성, holdover 설계 | slip count, wander |
| 포인터 이벤트 증가 | tributary clock 편차 | pointer threshold 관리 | pointer adjustment/sec |
| 보호절체 실패 | ring 구성 오류 | MSP/SNCP 시험 | APS 50ms 이내 |

> 요약: 동기식 전송망 리스크는 클록, 포인터, 보호절체이며 장비 OAM 카운터로 확인함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전송 오류 | B1/B2/B3 error 0 또는 임계치 이하 | NMS, PM counter |
| 절체 시간 | APS 50ms 이내 | protection switching test |
| 계위 매핑 | OC-n/STM-n 대응 일치 | 회선 설계서, OTDR |

> 요약: 도입 평가는 비트 오류, 절체 시간, 계위 매핑 정확도로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 기존 T1/E1 회선 수용 구간은 PDH tributary 매핑을 유지하되 SDH ADM에서 STM-1 이상으로 통합함.
2. 백본 ring은 MSP 또는 SNCP 보호를 설계하고 절체 시험으로 50ms 이내 복구를 검증함.
3. 신규 패킷 백본은 SDH/SONET 잔존 회선과 OTN/MPLS-TP 연동 경계를 분리해 운용함.

**결론 (2줄):**
- 기술사 판단: 회선 품질과 보호절체가 우선이면 SDH/SONET, 이더넷 패킷 집선이 중심이면 OTN 또는 MPLS-TP를 선택함.
- 향후 방향: 전송망은 SDH/SONET 회선 수용을 유지하면서 DWDM, OTN, packet transport로 통합되는 방향임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "디지털 계위를 설명하시오" | TDM 매핑, overhead, add/drop 흐름 | PDH vs SDH/SONET 차이 |
| 요구사항 명시형 | "PDH와 SDH를 비교하시오", "전송망 설계를 제시하시오" | 동기화·보호절체 설계 절차 | OC-n/STM-n, OAM, 50ms 기준 |

> 요약: 설명형은 계위와 프레임 구조, 요구사항형은 회선 추출·보호절체·클록 관리 기준으로 목차를 전환함.
