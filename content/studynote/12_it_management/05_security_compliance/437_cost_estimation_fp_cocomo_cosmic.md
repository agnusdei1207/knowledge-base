+++
title = "437. 비용 산정 FP COCOMO COSMIC (Cost Estimation FP COCOMO COSMIC)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FP(Function Points)는 사용자 관점의 기능 요구사항을 5대 컴포넌트(EI/EO/EQ/ILF/EIF)의 가중 합으로 정량화하고, COCOMO는 KLOC·규모계수·15가지 Effort Multiplier로 PM/Effort를 산출하며, COSMIC는 데이터 이동 4종류(Entry/Exit/Read/Write)의 CFP로 ISO/IEC 19761 기반 기능 크기를 측정한다.
> 2. **가치**: 프로젝트 투입 인력·기간·비용 예측 오차 ±10~25% 이내 통제, 계약 단가(S/W 사업대가) 산정 근거, EVM(Earned Value Management)과 연동한 진도·원가 통제, 다국적/아웃소싱 환경에서 언어·기술 중립적 의사소통 도구로 활용된다.
> 3. **판단 포인트**: FP는 "기능" 단위 주관성·요구변경 민감도가 높고, COCOMO는 LOC 의존으로 재사용·신기술 적용 시 보정 곱인자(EAF/COCOMO II의 EM/FS/DM) 누락이 치명적이며, COSMIC는 실시간/임베디드 같은 비데이터 처리형 시스템에서는 별도 도메인 확장이 필요하다. 각 기법의 가정·입력 산출 가능성·조직 역량에 따라 선택·혼용 전략이 결정된다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 비용 산정(Cost Estimation)은 "어느 규모에 누가 얼마나 걸려서 얼마가 드는가"에 대한 엔지니어링 의사결정의 출발점이다. 전통적 LOC(Lines of Code) 기반 추정은 언어·개발자 숙련도·도구 도입에 따라 ±400%까지 오차가 발생하여, 1970년대 후반 IBM의 Allan Albrecht가 FP를, 1981년 USC의 Barry Boehm이 COCOMO를 제안했고, 2002년경에는 FP의 한계를 보완하는 COSMIC FFPA가 등장했다.

현업에서는 SI(시스템 통합) 사업의 발주처-사업자 간 S/W 단가 산정(정보통신산업진흥원 표준단가, GS인증), 공공부문의 사업비 검토, CMMI L3 이상의 PP/PM/PI 영역 필수 활동, 그리고 RFP 응답 시 투입공수 산출 근거자료로 활용된다. 특히 RFP 단계에서 "개발 기간 12개월, 예산 8억 원"이라는 모호한 요구는 FP/COCOMO/COSMIC 결과로 "기능점수 1,250FP, 18.2 PM, 14.5인" 같은 정량 수치로 변환될 때 비로소 의사결정(공정 계획, 외주 단가 협상, 위험 분석)이 가능해진다.

기존 LOC 방식은 “측정 대상(=코드) 자체가 만들어져야 존재”하는 한계가 있어 요구사항 단계의 적시 산정이 불가했다. FP는 "요구사항이 확정된 시점"부터, COSMIC은 "설계/아키텍처 시점"까지 측정 가능하며, COCOMO는 FP->LOC 변환 또는 직접 LOC 입력으로 "노력(Effort, PM)·개발기간(TDEV)·비용"을 산출한다. 즉 세 기법은 상호 보완적 파이프라인을 형성한다.

```text
   [사업 초기/요구사항 단계]                  [설계 단계]                 [구현 단계]
   +------------------+                 +------------------+         +------------------+
   |  FP (Function    |  FP -> LOC 환산  |  COSMIC (CFP)    |  아키텍처|  COCOMO II       |
   |  Point) 측정     | ---------------> |  Data Movement   |  리팩토링|  (Size + EM/FS)  |
   |  5 Components    |  역산/스케일     |  4 Functional    |  영향 반영|  Post-Architecture|
   +------------------+                 |  User Types      |         +------------------+
            |                            +------------------+                  |
            | 14 GSC × 복잡도 × CAF           |  GSC/플랫폼별                    | Effort = A·Size^E
            v                                    v                                v
   +------------------------------------------------------------------------------------+
   |  PM(인월) · TDEV(월) · Cost(원)  --->  베이스라인 -> EVM -> To-Be 산정 -> 변경관리       |
   +------------------------------------------------------------------------------------+
```

**왜 세 기법이 모두 필요한가?**
- **FP**는 “기능” 단위 의사소통(영업 vs 개발)·다국적 비교(IFPUG)·계약 요율 적용에 강점
- **COCOMO**는 “노력·일정”으로 변환하여 PM Schedule, 인원투입 계획에 강점
- **COSMIC**는 비주류 언어·비즈니스 실시간 시스템·임베디드 SW·SaaS의 마이크로서비스 같은 환경에서 FP의 한계를 보완

- **📢 섹션 요약 비유**: FP는 “주문서(요구사항)의 요리 종류와 양”, COCOMO는 “요리 인원·시간 견적”, COSMIC은 “실제 손질(데이터 이동) 횟수”라 할 수 있다. 주방장(PM)이 세 눈을 모두 갖고 있어야 적정 견적이 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) FP(Function Points) — IFPUG 4.3.x

| 항목 | 내용 |
|---|---|
| 측정 대상 | 사용자 관점의 기능 사용자 요구사항(FUR) |
| 5대 컴포넌트 | EI(외부입력), EO(외부출력), EQ(외부조회), ILF(내부논리파일), EIF(외부연계파일) |
| 복잡도 | Low/Average/High, 가중치 행렬 사용 |
| 핵심 산식 | **FP = UFC × (0.65 + 0.01 × TDI) = UFC × CAF** |
| TDI | 14개 GSC(General System Characteristic) 영향도 합 (0~70) |
| CAF | 0.65 ~ 1.35 (대부분 0.85~1.15) |
| 규모 매핑 | 100FP 이하 소형, 100~1,000 중형, 1,000 이상 대형 |

**가중치 행렬 (IFPUG 기준, 5×3 매트릭스 예)**

|  | Low | Average | High |
|---|---:|---:|---:|
| EI | 3 | 4 | 6 |
| EO | 4 | 5 | 7 |
| EQ | 3 | 4 | 6 |
| ILF | 7 | 10 | 15 |
| EIF | 5 | 7 | 10 |

```text
            [요구사항 정의서/SRS]
                    |
            +-------+--------+
            v                v
    데이터 기능 분류      트랜잭션 기능 분류
    (ILF / EIF)          (EI / EO / EQ)
            |                |
            +-------+--------+
                    v
      [DET/RET/FTR 집계 -> 복잡도(L/A/H) 판정]
                    |
                    v
           UFP(미조정 FP) 산출
                    |
            + 14개 GSC 영향도(TDI) 평가
                    v
        CAF = 0.65 + 0.01 × TDI
                    |
                    v
        AFP = UFP × CAF  --->  1FP당 언어별 LOC 매핑
                            (Java≈53, C#≈59, COBOL≈107, JS≈47 등)
```

**GSC 14개 (IFPUG 기준)**: ①데이터통신 ②분산처리기능 ③성능 ④사용자기기환경 ⑤트랜잭션빈도 ⑥온라인데이터항목 ⑦최종사용자 효율 ⑧온라인 갱신 ⑨복잡한 처리 ⑩재사용성 ⑪설치 용이성 ⑫운영 용이성 ⑬다수 사이트 ⑭변경 촉진

### 2) COCOMO(Constructive Cost Model) — Boehm 1981/2000

| 모델 | 적용 시점 | 입력 | 산출 |
|---|---|---|---|
| **Basic** | 견적 초기 | KLOC | PM, TDEV |
| **Intermediate** | 계획/제안 | KLOC + 15 EAF | PM, TDEV (모드별) |
| **Detailed** | 실행/통제 | 계층별 KLOC + 15 EAF×단계 | 단계별 PM |
| **COCOMO II** | 요구->아키텍처->구현 | Size(FP/LOC)+ Scale Factors(SF)+ Effort Multipliers(EM)+ Phase/Product/Platform Factors | PM, 개발기간 분포 |

**Basic COCOMO (Organic/Semi-detached/Embedded)**

```
PM = a × (KLOC)^b      TDEV = c × (PM)^d

Organic(소형, 친숙 도메인)  : a=2.4, b=1.05, c=2.5, d=0.38
Semi-detached(중형)         : a=3.0, b=1.12, c=2.5, d=0.35
Embedded(실시간/안전)       : a=3.6, b=1.20, c=2.5, d=0.32
```

**COCOMO II 핵심 산식 (Post-Architecture)**
```
PM = A × (Size)^E  ×  ∏(EM_i)  ×  ∏(FS_j)  ×  ∏(DMM_k)
where  A = 2.94,  E = B + 0.01 × Σ(SF_i) ,  B = 0.91
SF 5개: PREC, FLEX, RESL, TEAM, PMAT  (합 0~50)
EM 17개: RCPX/RUSE/PVOL/PEXP/LEXP/PCAP/PEXP/... (5점 척도)
FS 5개: RUSE, DOC, TIME, STOR, PVOL (의존성 유사)
DMM: 도메인/플랫폼 성숙도
```

### 3) COSMIC FFPA(ISO/IEC 19761) v4.0+

COSMIC은 FUR을 4가지 **Functional User (FUR Type)**으로 분해하고, 각 사용자가 “데이터를 움직이는 동작(Data Movement)” 횟수를 측정한다. FPA/IFPUG의 “파일·요구 형식” 한계를 넘어 **마이크로서비스, API, IoT, 임베디드**에서도 적용 가능하다.

```text
   [소프트웨어 경계(Software Boundary) 정의]
                       |
        +--------------+--------------+
        v              v              v
   Entry (입력)   Exit (출력)   Read (읽기)   Write (쓰기)
   1 CFP each     1 CFP each   1 CFP each   1 CFP each
   사용자->SW       SW->사용자     SW->영속저장   영속저장->SW
   (단, Write는 SW에서 영속저장소 변경 시)
                       |
                       v
   CFP(소프트웨어 기능 크기) = Σ(Entry + Exit + Read + Write)
   ※ 1CFP ≈ 0.5~1.5LOC of equivalent code
```

**핵심 규칙**
- **Entry**: 데이터가 시스템 경계를 *안으로* 들어옴 (1개 트리거 기준 1CFP). 단, 동일 트랜잭션 내 N개 데이터 그룹 이동 = N개.
- **Exit**: 데이터가 *밖으로* 나감
- **Read**: SW가 영속 저장소에서 *데이터를 읽기만* 함 (쓰지 않음)
- **Write**: SW가 영속 저장소에 *데이터를 기록/갱신* 함
- **데이터 그룹(Group)**: ①하나의 의미적 단위로 묶인 필드들, ②서로 다른 그룹은 별도 카운트

| 구성 요소 | 역할 | 핵심 기술/동작 |
|:---|:---|:---|
| **FUR(Functional User Requirements)** | 측정 단위 정의 | 시스템이 “무엇을” 하는지에 대한 사용자 관점 진술(Why/What only) |
| **FUR Type(공정·데이터·연계·산술·제어·보안 등)** | 측정 분해 단위 | 데이터 이동의 발화 단위 (Use Case -> 1~N FUR) |
| **Data Movement(Entry/Exit/Read/Write)** | 카운팅 단위 | 4종 합산 -> CFP |
| **Scope/Boundary** | 측정 경계 | 시스템 내/외부, 외부 사용자/시스템 정의 |
| **Functional Process** | 측정 단위 그룹화 | “트리거 -> 데이터 이동들”의 실행 단위 |
| **GSC / Measurement Context** | FP 보정(선택적) | 규모 보정 없음, 순수 기능 크기 측정 |

**COCOMO II 후속/연계**: COSMIC 결과(CFP)는 COCOMO II의 Size 입력으로 직접 매핑 가능(`1CFP ≈ 0.5LOC`, 변환 후 PM 산출). 실제로 ISO/IEC 20926(COCOMO II), 19761(COSMIC), 24570(Use Case FP), 29881(automated FP)는 **ISO/IEC 14143 Common Software Measurement Framework** 아래 상호 환산·연계 표준화되어 있다.

- **📢 섹션 요약 비유**: COSMIC의 Entry/Exit은 우체국 “택배 배달/회수”이고, Read/Write는 “창고에서 물건 꺼내기/넣기”. 화물(데이터)을 얼마나 자주 옮겼나를 정확히 세면 우편사업의 “일의 양”이 자연스럽게 산출된다.

---

## Ⅲ. 비교 및 연결

| 구분 | **FP (IFPUG)** | **COCOMO** | **COSMIC FFPA** |
|---|---|---|---|
| 측정 단위 | 기능점수 (FP) | 노력/일정 (PM, TDEV) | 기능 사용자 요구 수 (CFP) |
| 분류 체계 | EI/EO/EQ/ILF/EIF 5종, 복잡도 3단계 | Organic/Semi-detached/Embedded + 15 EAF | Entry/Exit/Read/Write 4종 |
| 표준 | ISO/IEC 20926 | ISO/IEC 19761(COPSEMO), 20926(COCOMO II) | ISO/IEC 19761 |
| 적용 단계 | 요구사항(요구 확정) | 계획/설계/구현 | 요구~설계 (코드 비의존) |
| 언어/플랫폼 의존성 | 낮음(가중치 매트릭스) | 중(규모계수·EM으로 보정) | **없음**(순수 FUR) |
| 산출 시간 | 0.5~2일 (100~500FP 기준) | 데이터 입력 후 1~2시간 | 1~3일 (500~2,000CFP 기준) |
| 재사용/구성요소 | 가능 (v4+ 재사용 FP) | 가능 (RUSE EM) | 가능 (컴포넌트별 측정) |
| 주 사용처 | RFP/SLA, 글로벌 비교, EVM | PM 스케줄,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 437 / 800

<- **이전**: [436. 테스트 관리 품질 보증 자동화](/knowledge-base/studynote/12_it_management/05_security_compliance/436_test_management_quality_assurance_automation/)
**다음**: [438. 품질 관리 ISO 25010 품질 특성](/knowledge-base/studynote/12_it_management/05_security_compliance/438_quality_management_iso_25010_characteristics/) ->

---
