---
title: "509. ISO 25010 소프트웨어 품질 모델 (ISO 25010 Software Quality Model)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ISO/IEC 25010은 SQuaRE(System and Software Quality Requirements and Evaluation) 시리즈의 핵심 모델로, 8개(2011) -> 9개(2022) **품질 특성(Quality Characteristic)** 과 각 특성별 **하위 특성(Sub-characteristic)** 계층으로 소프트웨어 품질을 정의·측정·평가하기 위한 국제 표준 프레임워크임.
> 2. **가치**: 주관적·정성적 평가에 머물던 SW 품질을 **정량적 메트릭(ISO 25023)** 과 연결하여, 공공 SI 감리·발주자 RFP·GS인증·인력양성과정 등에서 **일관성 있는 품질 기준·계약적 분쟁 방지·TCO 절감(평균 23~35%)** 효과를 제공함.
> 3. **판단 포인트**: 8~9개 특성을 **동등 가중치로 다루지 말고**, 도메인·아키텍처(MSA/모놀리식/실시간·안전-critical)에 따라 **우선순위 매트릭스**를 구성해야 함. 예) 금융/원전 S/W는 신뢰성·보안·안전을, 게임·HCI는 사용성·성능효율성을, 레거시 유지보수는 변경성·테스트성·모듈성에 가중치를 부여함.

---

## Ⅰ. 개요 및 필요성

ISO/IEC 25010:2011은 **소프트웨어 품질**에 대한 일반적인 관점을 정의한 표준으로, 단순히 "버그가 없다"는 차원을 넘어 **사용 시점, 변경 시점, 전이 시점**의 품질을 통합적으로 다룸. 2022년 개정판에서는 **Safety(안전성)** 가 9번째 품질 특성으로 추가되어, 자율주행·의료기기·산업제어·원자력 등 safety-critical 영역의 품질 평가 기반을 제공함.

기존의 SW 품질 평가는 **ISO/IEC 9126(1991/2001)** 기반으로 수행되었으나, ①품질 특성이 6개로 한정되어 클라우드·IoT·AI 시대의 다차원 품질 요구를 반영하지 못함, ②측정 메트릭과 평가 절차가 분절되어 있어 **요구사항->측정->평가** 전 과정을 일관되게 추적할 수 없음, ③발주자·개발자·감리인 간 **공통 어휘 부재**로 분쟁이 빈번함, 이라는 세 가지 한계가 존재했음.

이에 ISO/IEC 25000 시리즈(**SQuaRE**, Systems and Software Quality Requirements and Evaluation)로 발전시키면서 25010을 **품질 모델(Quality Model)**, 25040을 **품질 평가 프로세스**, 25023/25024를 **측정 참조 모델**로 명확히 분리하고, SQuaRE는 다음 5개 Division으로 구성됨.

```text
  +-------------------------------------------------------------+
  |        SQuaRE (ISO/IEC 25000n) Quality Framework            |
  +-------------------------------------------------------------+
              |             |              |             |
              v             v              v             v
   +---------------+ +--------------+ +--------------+ +----------------+
   | 2500n Quality | | 2501n Quality| | 2502n Quality| | 2503n Quality  |
   |  Management   | |   Model      | |  Measurement | |  Requirements  |
   |  (25001)      | |  ★ 25010 ★  | |  (25020,23,  | |  (25030)       |
   +---------------+ +--------------+ |   25024)     | +----------------+
                                       +--------------+
                                          |
                                          v
                                   +----------------+
                                   | 2504n Quality  |
                                   |   Evaluation   |
                                   |  (25040~25045) |
                                   +----------------+

   +----------------------------------------------------------+
   |  ★ 25010 = 시스템/소프트웨어 품질 모델의 중심축 ★        |
   |   - 8개(2011) -> 9개(2022) 품질특성                        |
   |   - 31개 하위특성으로 분해                                |
   |   - 외부/내부 품질 view 와 사용 시점/변경 시점 view 제공  |
   +----------------------------------------------------------+
```

도입 필요성은 다음 4가지로 요약됨: ① **공통 어휘 표준화**(발주·개발·감리 공용), ② **정량적 측정 가능**(메트릭·측정 함수 연결), ③ **전 생애주기 품질 추적**(요구->설계->구현->테스트->운영), ④ **안전·보안·AI 윤리** 등 신규 품질 요구 반영. 한국에서도 행정안전부 공공소프트웨어 품질관리 지침, NIA 클라우드 품질인증, KISA 보안성 평가 등에서 사실상 참조 표준으로 활용됨.

- **📢 섹션 요약 비유**: ISO 25010은 마치 **자동차 종합 검사 기준서**와 같다. 차의 성능(가속력), 안전(에어백), 연비(자원효율), 편의(사용성), 내구성(신뢰성), A/S 편의(유지보수성), 타 차종 호환(호환성), 사고 시 탑승자 보호(안전성) 등 — 차량을 8~9가지 차원으로 동시에 평가하듯, SW를 다차원 동시 평가하는 기준표이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ISO/IEC 25010의 구조는 **3계층 모델**이다: 최상위 **품질 특성(Quality Characteristic) 8~9개 -> 하위 특성(Sub-characteristic) 31개 -> 측정 가능한 메트릭(Metric, ISO 25023/25024)**. 그리고 **뷰(view)** 관점: **내부 품질(Internal Quality)**, **외부 품질(External Quality)**, **사용 시점 품질(Quality in Use)** 의 3-view 구조로 품질을 시점별로 분리함.

```text
                  +----------------------+
                  |  8/9 Quality         |   ★ 품질 특성(2011:8, 2022:9)
                  |  Characteristics     |     ① 기능적합성(F)        ⑥ 보안성(S)
                  |                      |     ② 성능효율성(PE)      ⑦ 유지보수성(M)
                  |                      |     ③ 호환성(C)           ⑧ 이식성(Po)
                  |                      |     ④ 사용성(Us)          ⑨ 안전성(Sf, 2022)
                  |                      |     ⑤ 신뢰성(R)
                  +----------+-----------+
                             | 1:N 분해(decomposition)
                             v
                  +----------------------+
                  |  31 Sub-characteristic|   ★ 하위 특성
                  |  (예: Functional     |     - 정량 측정 가능 단위
                  |   Suitability ->      |     - 메트릭의 속성 정의
                  |   Completeness/      |
                  |   Correctness/       |
                  |   Appropriateness)   |
                  +----------+-----------+
                             | 매핑(mapping)
                             v
                  +----------------------+
                  |  ISO 25023 / 25024   |   ★ 측정 참조 모델
                  |  Metrics             |     - Time Behavior: 평균/최대 응답시간(ms)
                  |  - Functional        |     - MTBF, MTTR, 가용성(%)
                  |  - Performance        |     - Cyclomatic Complexity, CBO
                  |  - Reliability        |     - Test Coverage %
                  |  - Maintainability    |     - CVSS, 인증 실패율
                  +----------+-----------+
                             |
                             v
            +----------------+----------------+
            |  Quality Model VIEW (3-view)     |
            |  ---------------------------     |
            |  ▸ Internal Quality : 코드/설계  |
            |  ▸ External Quality : 동작 SW    |
            |  ▀ Quality in Use  : 사용자 관점  |
            |    (효과성, 효율성, 만족도,       |
            |     위험 회피, 컨텍스트 완전성)   |
            +----------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **품질 특성 (8->9개)** | 최상위 평가 차원, 이해관계자 간 합의 단위 | 기능적합성·성능효율성·호환성·사용성·신뢰성·보안성·유지보수성·이식성(·안전성 2022 추가). 각 특성은 **수명주기 단계별 별도 가중치** 적용 가능 |
| **하위 특성 (31개)** | 측정이 가능한 속성으로 분해 | 예) 기능적합성 -> **완전성(Completeness)·정확성(Correctness·Fault Tolerance)·적절성(Appropriateness)**, 유지보수성 -> **모듈성·재사용성·분석성·변경성·테스트성** |
| **3-view 품질 모델** | 평가 시점 분리 | Internal: 정적 분석(SonarQube, ESLint), External: 부하 테스트(JMeter, Gatling), Quality in Use: SUS(System Usability Scale), NPS |
| **SQuaRE 연계** | 모델->측정->평가로 일관 추적 | 25010(모델) -> 25023/25024(메트릭) -> 25040(평가 프로세스) -> 25042(평가 모듈). 발주 RFP에 "25040 절차 준수" 명시 가능 |
| **측정 함수(Metric)** | 정량값 산출 | 예) Cyclomatic Complexity(McCabe, V(g)≤10 권장), Efferent Coupling(Ce), 응답시간 P95, MTBF = MTTR + MTTF, 가용성 = MTBF/(MTBF+MTTR) × 100 |

### 2022 개정판 핵심 변화(Safety 추가)
- **Safety(안전성)** 이 9번째 특성으로 신규 편입. 하위 특성: 운영 제약(Operational Constraint), 위험 식별(Risk Identification), 페일 세이프(Fail Safe), 위험 경고(Hazard Warning), 안전 통합(Safe Integration).
- 영향 도메인: **자율주행(ISO 26262, SOTIF ISO 21448)**, 의료기기(ISO 14971, IEC 62304), 산업제어(IEC 61508, IEC 62443), 원자력·철도·항공.
- 기존 ISO 26262·IEC 61508 등 도메인별 안전표준과 **상위-하위 매핑**이 가능해져, 도메인 표준의 **공통 어휘 레이어** 역할 수행.

### Quality in Use (사용 시점 품질)
2011부터 보강된 개념으로, 실제 사용자·업무 컨텍스트에서의 품질을 별도 평가. 5개 하위 특성: 효과성(Effectiveness), 효율성(Efficiency), 만족도(Satisfaction), 사용 시 위험 회피(Freedom from risk), 컨텍스트 완전성(Context completeness). 측정 도구: **SUS(System Usability Scale, 10문항 5점 척도, ≥68 양호)**, **NPS(Net Promoter Score)**, **SUPR-Q**, 작업완료시간(Task Completion Time
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 509 / 600

<- **이전**: [508. ISO 27001 정보보안 관리체계](/studynote/11_design_supervision/06_exam_summary/508_iso_27001_isms_standard)
**다음**: [510. CMMI 프로세스 성숙도 모델](/studynote/11_design_supervision/06_exam_summary/510_cmmi_process_maturity_model/) ->

---
