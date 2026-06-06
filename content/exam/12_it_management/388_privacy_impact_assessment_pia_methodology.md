---
title: "Privacy Impact Assessment PIA Methodology"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 개인정보 영향평가(PIA)는 ISO/IEC 29134:2017 및 GDPR 제35조, 개인정보보호법 제33조에 근거하여 정보시스템의 설계·구축·운영 전 단계에서 개인정보의 처리·저장·유통·파기 라이프사이클 전체에 대한 **위험식별(Risk Identification) -> 영향평가(Impact Assessment) -> 통제설계(Control Design) -> 잔여위험 승인(Residual Risk Acceptance)**의 4단계를 거치는 사전예방적 프라이버시 거버넌스 체계이다.
> 2. **가치**: PIA 조기 실시 시 설계 결함에 따른 재작업 비용을 약 60~80% 절감(IBM Systems Sciences Institute 1:10:100 Rule 적용)하며, GDPR 위반 시 글로벌 매출액 4% 또는 2,000만 유로 중 더 큰 금액의 과징금, PIPA 위반 시 5년 이하 징역 또는 5천만 원 이하 벌금 등 법적 리스크를 사전에 차단하고, 정보주체의 신뢰도(Trust Score)를 정량적으로 제고한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **(a) PIA 실시 시점**(사전/사후), **(b) 평가 범위**(정보시스템 단위 vs 사업단위), **(c) 정량평가 vs 정성평가**(CNIL 방식의 확률×영향 점수화 vs NIST 방식의 시나리오 기반), **(d) 자동화 도구 활용도**(수작업 템플릿 vs OneTrust/TrustArc 같은 GRC 플랫폼), **(e) Stakeholder 참여도**(내부 DPO 한정 vs 외부 정보주체 대리인 포함)이며, 기술사적 판단 기준은 **"처리하는 개인정보의 민감도, 데이터 주체 수, 처리 목적의 신규성, 자동화된 의사결정 여부"**라는 4대 트리거 조건의 충족 여부이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 정의 및 법적 근거

개인정보 영향평가(Privacy Impact Assessment, PIA)는 개인정보처리자가 개인정보를 처리하는 정보시스템의 구축·운영·변경 시, **정보주체의 개인정보가 침해될 위험을 사전에 분석·평가**하고 이를 보호하기 위한 조치를 마련하는 일련의 절차이다. 법적 근거는 다음과 같이 다층적 구조를 가진다.

| 법률/규범 | 조항 | 핵심 의무 | 발동 트리거 |
| :--- | :--- | :--- | :--- |
| **개인정보 보호법(PIPA)** | 제33조 (영향평가의 시행) | 공공기관은 개인정보 영향평가 의무, 민간은 권장 | 고유식별정보 처리, 민감정보 처리, 5만 명 이상 정보주체 |
| **GDPR** | Article 35 (DPIA) | 모든 컨트롤러에 대해 DPIA 의무화 | 대규모 모니터링, 고위험 처리, 신기술 사용, 자동화된 의사결정 |
| **ISO/IEC 29134:2017** | Section 6~8 | PIA 수행을 위한 7단계 프레임워크 | 권고사항(국제표준) |
| **NIST SP 800-53 Rev.5** | PT-7, RA-8 | Privacy Impact Assessment 통제 항목 | 연방기관 의무 |
| **개인정보보호위원회 고시** | 제2023-XX호 | PIA 수행 가이드라인 및 보고서 양식 | 국내 공공기관 |
| **CCPA/CPRA (캘리포니아)** | §1798.185(a)(16) | Risk Assessment 의무 | 민감정보 1,000명 이상 처리 시 |

### 1.2 필요성: 사후 대응에서 사전 예방으로

전통적 정보보호 패러다임은 **"침해 발생 -> 탐지 -> 대응 -> 복구"**의 사후적(Reactive) 모델이었다. 그러나 2017년 Equifax 사건(1.47억 명 정보 유출, 손해액 14억 달러), 2018년 Cambridge Analytica 사건(Facebook 8,700만 명 프로파일링), 2023년 23andMe 사건(690만 명 유전자 정보 유출) 등 **대규모 개인정보 침해사고가 빈발**하면서, 시스템 설계 단계부터 프라이버시를 내재화(Privacy by Design)하는 사전예방적(Proactive) 패러다임이 필수 불가결해졌다.

```text
   +--------------------------------------------------------------------+
   |     패러다임 전환: Reactive Security -> Proactive Privacy (PIA)     |
   +--------------------------------------------------------------------+
   |                                                                    |
   |   [기존: 침해사고 대응형]              [신규: PIA 사전예방형]        |
   |                                                                    |
   |   요구사항 정의 -+                    요구사항 정의 -+ PIA Phase 1  |
   |                 |                                  |                |
   |   시스템 설계 ---+                    프라이버시 위협 모델링 -+ P2  |
   |                 |                                  |                |
   |   구축/개발 ----+                    통제 설계(PbD 7원칙) --+ P3    |
   |                 |                                  |                |
   |   운영/배포 ----+                    영향평가/잔여위험 --+ P4        |
   |                 |                                  |                |
   |   사고 발생 ----+  <- 79%가 사후 발견    모니터링/재평가 --+ P5      |
   |                 |                                  |                |
   |   사후 분석/제재  +- 비용 100배        지속적 거버넌스      +- 비용 1|
   |                                                                       |
   |   1:10:100 Rule (IBM) : 설계단계 수정 1 -> 구축단계 10 -> 운영단계 100 |
   +--------------------------------------------------------------------+
```

**📢 섹션 요약 비유**: PIA는 자동차 설계 시 충돌 안전도 시뮬레이션을 하는 것과 같습니다. 실제 사고(개인정보 유출)가 난 후 안전벨트(보안솔루션)를 다는 것이 아니라, 설계 단계에서 시트백·ABS·에어백 구조(접근통제·암호화·마스킹)를 미리 설계도에 반영하는 것이죠.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 PIA 7단계 프레임워크 (ISO/IEC 29134:2017)

ISO/IEC 29134는 PIA를 **7단계 프로세스**로 정의한다. 이는 PIA 보고서의 국제적 표준 골격이 된다.

```text
   +----------------------------------------------------------------------+
   |                  ISO/IEC 29134:2017 PIA 7-Phase Process              |
   +----------------------------------------------------------------------+
                                    |
   +--------------------------------+---------------------------------+
   v                                v                                 v
 [Phase 1]                  [Phase 2]                          [Phase 3]
 사전준비                  PIA 범위 결정                       이해관계자 식별
 Prepare                   Define Scope                        Identify
                                                      Stakeholders
   |                          |                                  |
   +- PIA 필요성 판단         +- 평가 대상 시스템 경계           +- DPO(데이터보호책임자)
   +- 평가팀 구성 (최소 3인)   +- 정보자산 식별 (PII Inventory)   +- CISO
   +- 착수 보고서 작성         +- 처리 목적/법적 근거 매핑       +- 정보주체/대리인
   +- 일정 및 자원 계획        +- 평가 기준선(Baseline) 설정    +- 외부 전문가/이해관계자
                                                                       |
   +--------------------------------+---------------------------------+
   v                                v                                 v
 [Phase 4]                  [Phase 5]                          [Phase 6]
 PII 데이터 흐름 매핑        영향 및 위험 분석                  대응책 및 잔여위험
 Map & Analyze              Assess Impacts                     Recommend
 Data Flow                  & Risks                            Controls
   |                          |                                  |
   +- 수집/저장/사용/제공/    +- 5대 프라이버시 위협 매핑        +- 7원칙 기반 통제 설계
   |  파기/처리위탁 흐름도    |  (수집,저장,처리,공개,파기)      +- 암호화(TDE, ABE)
   +- 데이터 보호 조치 식별   +- 7대 프라이버시 원칙 평가        +- 접근통제(RBAC/ABAC)
   +- 처리위탁사 목록(Sub-    +- 4대 영향 도메인 분석            +- 기술적/관리적/물리적
   |  Processor Chain)         |  (신분,신용,평판,자유)            |  보호조치 도출
   +- 교차국적 이전 경로      +- 위험 등급 산정(H/M/L)            +- 잔여위험 매트릭스
   |                          |                                  |
   |                          |  <--- 피드백 루프(반복) ----------->|
   v                                                                 v
                          [Phase 7]
                          PIA 보고서 작성/검토/승인
                          Document & Review
                             |
                             +- 경영진 승인(Residual Risk Sign-off)
                             +- DPO 의견서 첨부
                             +- 정기적 재평가(연 1회 이상)
```

### 2.2 PIA의 핵심 5대 평가축 (5 Dimensions)

PIA는 단순히 "위험이 있다/없다"가 아니라, **5개 차원**에서 다각도로 분석한다.

```text
   +------------------------------------------------------------------+
   |                  PIA 5대 평가축 (5-Dimension)                    |
   |                                                                  |
   |                          +-------------+                         |
   |                          |  Data       |                         |
   |                          |  Lifecycle  |  수집->저장->사용->제공->파기|
   |                          +------+------+                         |
   |                  +--------------+--------------+                 |
   |                  v              v              v                 |
   |           +----------+   +----------+   +----------+            |
   |           | Threat   |   |Impact    |   | Control  |            |
   |           | Modeling |   | Domains  |   | Design   |            |
   |           +----------+   +----------+   +----------+            |
   |   STRIDE-PRIVACY       4대 영향           7원칙(PbD)             |
   |   ·Snooping            ·신분도용           ·Proactive             |
   |   ·Tampering           ·신용훼손           ·Default-Off           |
   |   ·Repudiation         ·평판훼손           ·Embedded              |
   |   ·Info Disclosure      ·자유침해           ·Full-lifecycle        |
   |   ·DoS                 (생계,거주이동)      ·Visibility/Transp.    |
   |   ·Elevation                                          ·Respect User|
   |                  +--------------+--------------+                 |
   |                  v              v              v                 |
   |           +----------+   +----------+   +----------+            |
   |           |Stakehold.|   |Risk      |   |Compliance|            |
   |           |Analysis  |   |Scoring   |   | Mapping  |            |
   |           +----------+   +----------+   +----------+            |
   |   RACI Matrix         위험 = L(가능성)   PIPA,GDPR,                |
   |   내부/외부           × I(영향)         ISO27701,HIPAA            |
   |   DPO,이해관계자       (1~5 점수)        Cross-Border             |
   +------------------------------------------------------------------+
```

### 2.3 핵심 구성 요소 및 기술

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **PII Inventory (개인정보 자산 식별)** | 처리 중인 모든 개인정보 항목의 카탈로그 작성 | 데이터 카탈로그 도구(Collibra, Alation, Immuta), 자동 PII 탐지(Sensitive Data Discovery, Microsoft Purview, AWS Macie, BigID) 활용. 스키마 메타데이터, regex 패턴(주민번호/카드번호/이메일), ML 기반 NER(Named Entity Recognition) 모델을 통해 1,000만 건 레코드에서 PII 자동 분류 |
| **Threat Modeling (위협 모델링)** | STRIDE-PRIVACY 프레임워크로 7대 프라이버시 위협 도출 | STRIDE의 6개 범주(Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege)에 **Consent Degradation**(동의 훼손), **Re-identification**(재식별) 2개 추가하여 총 8개 카테고리 운영. 데이터 흐름도(DFD) Level 0~3 단계로 작성, LINDDUN(Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of information, Unawareness, Non-compliance) 위협 모델링 프레임워크 병행 |
| **Risk Scoring (위험 점수화)** | 정량적 위험 등급 산정 | CNIL 방식: **위험 = 가능성(Likelihood, 1~4) × 영향(Impact, 1~4)** 의 4×4 매트릭스로 16개 셀. 예) (L3, I4)=12 -> 심각(Serious). 또는 NIST 방식: 5단계 정성평가(Very Low~Very High). 2차원에서 GDPR Article 35 기준 "High Risk" 트리거는 9점(가능성 High + 영향 High) 이상 |
| **Privacy Controls (통제 항목)** | 7원칙 기반 보호조치 도출 | ISO 27701 Annex A 통제항목 49개(관리적 30+기술적 19), NIST SP 800-53 Rev.5 PT 패밀리 9개(PT-1~9), CSA CCM(Cloud Controls Matrix) 프라이버시 도메인 7개 항목. 암호화는 AES-256-GCM(저장), TLS 1.3(전송), Homomorphic Encryption(연산 시), 토큰화(Tokenization) 적용 |
| **Stakeholder Engagement (이해관계자 참여)** | DPO, 정보주체, CISO 간 의견 수렴 | GDPR Recital 70에 따라 정보주체 의견 청취 의무. workshop, 설문, 공개 협의(Public Consultation) 절차. 한국 PIPA는 정보주체 대리인(Privacy Advocate) 참여 권장. RACI 매트릭스로 책임 할당 |
| **PIA Report Template** | 표준화된 결과 문서 | ISO 29134 Annex A 양식 12개 섹션, PIPC(개인정보보호위원회) 「개인정보 영향평가 수행 안내서」 8개 장. 보고서는 ① 요약 ② 처리현황 ③ 위험식별 ④ 영향평가 ⑤ 보호조치 ⑥ 잔여위험 ⑦ 의견수렴 ⑧ 승인 으로 구성 |
| **Residual Risk Sign-off** | 경영진의 잔여위험 수용 결정 | Risk Acceptance Form 작성, 연간 재평가 스케줄 등록. RAG(Red/Amber/Green) 등급으로 표시, Red는 90일 내 재평가, Amber 6개월, Green 1년 주기 |

### 2.4 핵심 알고리즘 및 정량 평가 모델

**가. CNIL 4×4 위험 매트릭스 (EU 권장)**

```
위험점수(R) = L(가능성) × I(영향)        가능성(L)
                                          1  2  3  4
+--------+---+---+---+---+                 (1) 거의 없음
| 영향 4 | 4 | 8 |12 |16 | <- Serious       (2) 낮음
| 영향 3 | 3 | 6 | 9 |12 | <- High          (3) 보통
|
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 388 / 800

<- **이전**: [387. 보안 감사 컴플라이언스 체크리스트](/studynote/12_it_management/05_security_compliance/387_security_audit_compliance_checklist/)
**다음**: [389. 정보보안 관리체계 ISMS 인증 심사](/studynote/12_it_management/05_security_compliance/389_isms_information_security_management/) ->

---
