+++
title = "514. COCOMO 비용 산정 모델 (COCOMO Cost Estimation Model)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COCOMO(Constructive Cost Model)는 Barry W. Boehm이 1981년 저서 *Software Engineering Economics*에서 제시한 **알고리즘 기반 SW 비용 산정 모델**로, 코드 라인 수(KLOC/DSI)와 15~17개 비용 요인(Effort Multiplier)을 곱셈·지수 함수로 결합하여 `Effort = A × (Size)^B × ∏EMi`의 형태로 공수(PM), 개발 기간(TDEV), 평균 인원(ASG)을 도출한다.
> 2. **가치**: 계획 단계에서 ±25~35% 범위의 사전 견적 정확도를 제공하며, ISO/IEC 20926(SLIM/Check), ISO/IEC 20968(FPA), IEEE 12207의 SW 규모·비용 산정 절차와 직접 매핑되어 **발주사-수주사 간 객관적 계약 기준선(PCF, Price-to-Capability Floor)**을 수립하는 근거로 활용된다.
> 3. **판단 포인트**: COCOMO 81(Organic/Semi-detached/Embedded)과 COCOMO II(Composition/Early Design/Post-Architecture) 중 프로젝트 단계와 가용 데이터 수준에 맞는 모형을 선택해야 하며, **규모 척도(KLOC vs FP vs Object Point vs Use Case)**와 **스케일 팩터(B = 1.01 + 0.01 × ΣSF)** 적용 여부가 추정치의 30~200% 편차를 결정한다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 프로젝트의 약 60~70%가 예산 초과, 일정 지연, 또는 사용자 불만족으로 종료된다는 Standish Group CHAOS Report(2023)의 통계는, SW 개발의 본질적 비가시성·비가역성·변동성을 정확히 수치화해야 할 필요성을 부각시킨다. 1970년대 후반 미 국방성(DoD) 다수 프로젝트의 비용 폭증을 계기로, USC의 Barry Boehm은 SLIM( Putnam 모델)과 비교 가능한 **방사형 알고리즘 모델**을 고안했고, 그 결과물이 COCOMO이다.

기존 자의적 판단이나 전문가 경험에만 의존하던 **"경험적 추정(Expert Judgment)"** 방식은 다음과 같은 한계를 가진다.

| 기존 방식의 한계 | 상세 |
| :--- | :--- |
| 주관성 편향 | 추정자-낙관주의 편향(Optimism Bias)에 25~50% 과소 산정 |
| 학습 효과 부재 | 유사 프로젝트 데이터가 조직 지식으로 축적되지 않음 |
| 정당화 부재 | 발주처·경영진에 대한 "왜 이 견적인가?" 설명 불가 |
| 민감도 분석 불가 | 리스크 요인이 최종 비용에 미치는 영향 정량화 불가 |
| 표준 부재 | 다수 벤더 비교·계약 협상 시 객관 기준 부재 |

COCOMO는 **Size -> Effort -> Duration -> Cost -> Staffing**의 인과 사슬을 명시적 수식으로 표현하고, 15~17개 비용 조정 인자(EM, Effort Multiplier)와 5개 스케일 인자(SF, Scale Factor)를 통해 조직·프로젝트·제품·플랫폼 특성을 반영한다. 결과적으로 IEEE Std 12207.1-1995, ISO/IEC 20926, CMMI-DEV v1.3의 **Project Planning Process Area**에서 가장 보편적인 1차 산정 도구로 채택되었다.

```text
[프로젝트 착수 단계의 정보 흐름]

   +----------+    +--------------+    +--------------+
   | 사용자    |---->| 요구사항 정의 |---->|  기능/규모    |
   | Needs     |    |  (SRS)       |    |  (FP/KLOC)   |
   +----------+    +--------------+    +------+-------+
                                              | 입력
                                              v
        +-------------------------------------------------+
        |              COCOMO 알고리즘 코어                |
        |   +---------------------------------------+     |
        |   |  Size 입력(DSI or FP->KLOC 변환)      |     |
        |   |       |                                |     |
        |   |       v                                |     |
        |   |  Mode 결정 (Organic/Semi/Embedded     |     |
        |   |  OR COCOMO II Sub-model 선택)         |     |
        |   |       |                                |     |
        |   |       v                                |     |
        |   |  EMi × SFi 곱 산정 (1.0 baseline)      |     |
        |   |       |                                |     |
        |   |       v                                |     |
        |   |  Effort = A × Size^B × ΠEMi           |     |
        |   |  TDEV  = C × Effort^D                 |     |
        |   +---------------------------------------+     |
        +--------------------+----------------------------+
                             |
              +--------------+--------------+
              v              v              v
        +----------+   +----------+   +----------+
        | PM (공수) |   | TDEV(기간)|   | ASG(인원)|
        | 318.0 PM |   | 18.3 M   |   | 17.4 FTE |
        +----------+   +----------+   +----------+
```

- **📢 섹션 요약 비유**: COCOMO는 마치 **건축물의 건축비 산정 엔진**과 같다. 연면적(KLOC)·층수·지반 조건(EM)·내진 등급(SF) 같은 "숫자"만 정확히 입력하면, 콘크리트·철근·인건비·기간이 자동으로 산출되는 자동 견적 시스템이라 할 수 있다. 단, "연면적을 잘못 잰다면" 이후의 모든 견적은 그대로 무너진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COCOMO 81(원형 모델) 핵심 공식

```
① Effort (공수, 단위: Person-Months)  =  a × (KLOC)^b  ×  EAF
② Duration (개발 기간, 단위: Months)   =  c × (Effort)^d
③ Staffing (평균 인원)                =  Effort / Duration
④ Productivity (생산성)              =  KLOC / Effort  (단위: KLOC/PM)
```

여기서 **a, b, c, d**는 프로젝트 모드에 따른 고정 상수이며, **EAF(Effort Adjustment Factor)**는 15개 비용 요인의 곱이다.

| 모드 | a | b | c | d | 적용 사례 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Organic** (단순) | 2.4 | 1.05 | 2.5 | 0.38 | 5만 라인 이하, 숙련 팀, 친숙 환경 (예: 사내 CRM) |
| **Semi-detached** (중간) | 3.0 | 1.12 | 2.5 | 0.35 | 30만 라인, 일부 신규 기술 (예: IoT 게이트웨이) |
| **Embedded** (복합) | 3.6 | 1.20 | 2.5 | 0.32 | 실시간·안전-critical, 30만 라인 이상 (예: 항공기 FCS) |

### 2. COCOMO II (1997, 2000) — 현대화 모델

COCOMO II는 객체지향, 4GL, COTS, CBD(Component-Based Development), Agile·반복 개발, 그리고 분산 팀 환경을 반영하기 위해 ① **비선형 스케일링**, ② **5단계 척도 요인**, ③ **17개 비용 조정 인자(EM)**를 도입했다.

#### 2-1) 핵심 수식

```
PM_NS  =  A × (Size)^B  ×  ∏(EM_i)
PM     =  PM_NS × (1 + (%Schedule Overhead/100))
B      =  1.01 + 0.01 × Σ(SF_j)        # j = 1..5, 5개 스케일 팩터의 합
```

* A = 2.94 (Post-Architecture 모델 기본값)
* Size: KLOC 또는 Function Point -> Backfiring Table로 KLOC 변환
* 5개 Scale Factor: PREC(선행 유사 경험), FLEX(유연성), RESL(위험 해결·아키텍처 성숙도), TEAM(팀 응집도), PMAT(프로세스 성숙도, CMM 단계 0~5)
* 17개 EM은 Product(4) / Platform(3) / Personnel(5) / Project(5) 카테고리로 분류

#### 2-2) 스케일 팩터(SF) — 5개 인자

| 인자 | Very Low | Low | Nominal | High | Very High | Extra High |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| PREC | 6.20 | 4.96 | 3.72 | 2.48 | 1.24 | 0.00 |
| FLEX | 5.07 | 4.05 | 3.04 | 2.03 | 1.01 | 0.00 |
| RESL | 7.07 | 5.65 | 4.24 | 2.83 | 1.41 | 0.00 |
| TEAM | 5.48 | 4.38 | 3.29 | 2.19 | 1.10 | 0.00 |
| PMAT | 7.80 | 6.24 | 4.68 | 3.12 | 1.56 | 0.00 |

Σ(SF) 합계가 클수록 B 지수가 커져 -> **규모에 대한 비선형(Super-linear) 비용 증가 효과**를 표현한다. 예를 들어 Σ(SF)=15이면 B=1.16, Σ(SF)=5이면 B=1.06.

#### 2-3) Effort Multiplier(EM) — 17개 인자(예시 7개)

| EM 인자 | Very Low | Low | Nominal | High | Very High | Extra High | 적용 시 영향 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| RELY (신뢰성 요구) | 0.82 | 0.92 | 1.00 | 1.10 | 1.26 | n/a | 안전 critical SW 1.26배 |
| CPLX (복잡도) | 0.73 | 0.87 | 1.00 | 1.17 | 1.34 | 1.74 | 운영체제 커널 1.74배 |
| RUSE (재사용) | n/a | 0.95 | 1.00 | 1.07 | 1.15 | 1.24 | 전사 공통 컴포넌트화 |
| ACAP (분석가 역량) | 1.42 | 1.22 | 1.00 | 0.83 | 0.67 | n/a | 역량 ^ -> 비용 v |
| PCAP (프로그래머 역량) | 1.34 | 1.15 | 1.00 | 0.88 | 0.76 | n/a | 시니어 투입 시 단가 v |
| SCED (일정 압축) | 1.43 | 1.14 | 1.00 | 1.00 | n/a | n/a | 일정 단축 시 비용 ^ |
| TOOL (도구 사용) | 1.24 | 1.10 | 1.00 | 0.91 | 0.82 | n/a | IDE·CI 도구 활용 |

* `Multipliers < 1.0`: 비용을 **감소**시키는 요인 (예: 숙련된 인력, 도구 활용)
* `Multipliers > 1.0`: 비용을 **증가**시키는 요인 (예: 높은 신뢰성, 복잡도)
* EAF(Effort Adjustment Factor) = ∏EMi (모든 EM의 곱, 통상 0.9~1.4 범위)

### 3. COCOMO II의 3단계 Sub-Model 아키텍처

```text
[프로젝트 진행 단계별 COCOMO II Sub-Model 선택 흐름]

   프로젝트 초기 (Initiating)
            |
            v
   +--------------------------+
   |  Application Composition  | <--- 초기 단계, 4GL/CASE 도구로
   |  Model                    |     프로토타이핑·스크립팅
   |  (Object Points 기반)     |     Size: Object Point
   |  A = 2.94                 |
   +------------+-------------+
                | 요구사항·아키텍처 결정
                v
   +--------------------------+
   |  Early Design Model       | <--- 아키텍처 결정 후, 상세 설계 전
   |  (Function Point / UC)   |     Size: FP -> Backfiring
   |  SF: 5개 모두 활용       |     A = 2.94
   +------------+-------------+
                | 상세 설계·구현 진입
                v
   +--------------------------+
   |  Post-Architecture Model  | <--- 표준 산정 단계
   |  (전체 17개 EM + 5개 SF) |     가장 정밀, 5단계 척도 활용
   |  가장 정밀한 산정        |     Size: KLOC or FP 변환
   +--------------------------+
```

### 4. From Effort to Schedule & Cost

```
TDEV  =  [3.67 × (PM)^(0.28 + 0.2 × (B-1.01))] × (SCED%/100)        # 3 Sub-models 공통
ASG   =  PM / TDEV
Cost  =  PM × (평균 단가) × 지역 보정 계수 (CPI, Cost Performance Index)
       +  CapEx (HW, SW, 라이선스) + OpEx (유지보수 5~7% × 개발비)
```

* 예) PM=100, ΣSF=10(->B=1.11) -> TDEV = 3.67 × 100^0.306 ≈ 11.5개월
* 예) PM=100, ΣSF=25(->B=1.26) -> TDEV = 3.67 × 100^0.362 ≈ 16.3개월 (규모 효과로 기간 ^)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Size 측정 모듈**
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 514 / 600

<- **이전**: [513. FPA 기능점 분석 규모 산정](/knowledge-base/studynote/11_design_supervision/06_exam_summary/514_fpa_function_point_analysis_size_estimat/)
**다음**: [515. COSMIC 기능 크기 측정](/knowledge-base/studynote/11_design_supervision/06_exam_summary/515_cosmic_functional_size_measurement/) ->

---
