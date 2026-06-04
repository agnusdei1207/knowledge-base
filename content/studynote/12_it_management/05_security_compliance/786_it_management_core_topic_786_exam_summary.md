---
title: "786. IT 경영 관리 핵심 토픽 786번 시험 요약 (IT Management Core Topic 786 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 786. IT 경영 관리 핵심 토픽 786번 시험 요약 (IT Management Core Topic 786 Exam Summary)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 거버넌스(COBIT 2019), 전략(ISP/EA), 서비스(ITIL 4), 보안(ISMS-P), 프로젝트(PMBOK 7th), 변화관리(Kotter 8단계)를 통합해 IT 가치사슬(Value Chain)을 최적화하는 체계이며, 최신 기술사 시험은 디지털전환·AI 거버넌스·ESG-정보화 융합으로 출제 비중이 이동하고 있다.
> 2. **가치**: 정량적으로는 TCO 20~35% 절감, ROI 25% 이상 확보, 정보시스템 감리 부적정 건수 50% 감소, 정성적으로는 의사결정 속도 향상·리스크 가시화·규제 컴플라이언스 자동화 효과를 통해, 사업 연속성(BCP)과 디지털 신뢰(Digital Trust)를 동시에 확보한다.
> 3. **판단 포인트**: 중앙집중(CoE) vs 분산(Federation) 거버넌스, Build vs Buy, Agile-Water-Hybrid, On-Premise vs Hybrid vs Multi-Cloud, Zero Trust vs 전통 경계보안 사이의 트레이드오프를 조직 성숙도(CMMI 2.0·IT 거버넌스 성숙도 5단계)와 규제 환경(개인정보보호법, 클라우드 보안인증, AI 기본법)에 맞춰 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(Information Technology Management)는 1980년대 MIS(경영정보시스템) 시대부터 2020년대 AI·클라우드·제로트러스트 시대까지 진화해 온, 기업의 IT 자산을 전략·운영·감리 차원에서 통합 관리하는 discipline이다. 한국 IT 기술사(정보관리/컴퓨터시스템응용) 시험은 2020년 이후 "IT와 경영의 융합"을 핵심 축으로 재편되었으며, 단순 암기형 이론이 아닌 **"상황 제시 -> 프레임워크 선택 -> 정량/정성 효과 산출 -> 리스크 및 예외사항"** 형태의 실무 사례형 문제가 60% 이상을 차지한다.

특히 2023~2025년 기출 동향을 분석하면, (1) 클라우드 전환 시 정보시스템 감리 기준의 적용, (2) AI 서비스 도입 시 개인정보 영향평가·알고리즘 영향평가, (3) 공급망 보안(Cybersecurity Supply Chain Risk Management, C-SCRM), (4) ESG 공시 지표 중 정보화 항목(예: TCFD 사이버 리스크, EU CSRD의 데이터 거버넌스)이 신규 출제 영역으로 부상했다. 따라서 기술사 응시자는 ITIL·COBIT·PMBOK·ISO 27001·ISO 22301·전자정부법·클라우드컴퓨팅법·AI기본법·개인정보보호법 등 10여 개 표준·법령을 cross-walk 할 수 있는 능력이 필수다.

```text
+----------------------------------------------------------------------+
|          IT 경영 관리 통합 프레임워크 (Integrated IT Management)       |
+----------------------------------------------------------------------+
|                                                                      |
|  [전략 계층]              [거버넌스 계층]            [운영 계층]       |
|  +------------+          +-------------+          +------------+     |
|  | 사업전략    |◄--------►| 이사회/IT전략|◄--------►|  IT조직     |     |
|  | (CSF/KPI)  | Alignment| 위원회(ISAC) | Oversight| (CoE/Fed)  |     |
|  +-----+------+          +------+------+          +------+-----+     |
|        |                        |                        |           |
|        v                        v                        v           |
|  +------------+          +-------------+          +------------+     |
|  | ISP/EA     |   Align  |  COBIT 2019 |  Monitor |  ITIL 4    |     |
|  | (TOGAF 10) +---------►|  + ISO 38500+---------►|  + DevOps  |     |
|  +-----+------+          +------+------+          +------+-----+     |
|        |                        |                        |           |
|        v                        v                        v           |
|  +--------------------------------------------------------------+   |
|  |   디지털 전환(DX) · AI 거버넌스 · 클라우드 · Zero Trust        |   |
|  |   데이터 거버넌스(DAMA-DMBOK 2.0) · ESG-정보화 융합            |   |
|  +--------------------------------------------------------------+   |
|        |                        |                        |           |
|        v                        v                        v           |
|  +------------+          +-------------+          +------------+     |
|  | BSC/ROI    |  Measure |  ISMS-P     | Assure   | 감리/감사  |     |
|  | (NPV/IRR)  |◄--------►|  ISO 27001  |◄--------►|  ISO 19011|     |
|  +------------+          +-------------+          +------------+     |
|                                                                      |
+----------------------------------------------------------------------+
```

기존 패러다임은 ①IT는 비용(Cost Center) ②프로젝트 단위 관리 ③요구사항 중심 개발 ④수동 보안 통제 위주였으나, 현재는 ①IT는 가치 창출 엔진(Value Driver) ②포트폴리오·제품 중심 관리(PPM) ③Outcome·데이터·AI 모델 중심 ④자동화·지속적 검증(Continuous Audit) 중심으로 전환되었다. 이 변화는 **"VUCA + BANI + AI"** 환경에서 IT가 사업의 회복탄력성(Resilience)과 신뢰(Trust)를 좌우하는 핵심 인프라로 격상되었기 때문이다.

- **📢 섹션 요약 비유**: IT 경영 관리를 **"도시의 종합계획(Urban Master Plan)"** 에 비유할 수 있다. 도로·상하수도·교통·건축·환경·재난대응을 별개로 관리하면 한 번의 정전(사이버 사고)·홍수(데이터 폭증)·지진(규제 변경)에 도시 전체가 마비되듯, IT도 거버넌스·아키텍처·운영·보안·감리를 통합하지 않으면 같은 재앙이 반복된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 5대 핵심 영역은 ①IT 거버넌스(Governance) ②전략·아키텍처(Strategy & EA) ③서비스 운영(Delivery & Support) ④보안·컴플라이언스(Security & Compliance) ⑤변화 관리·리더십(Change & Leadership)이다. 각 영역은 PDCA(Plan-Do-Check-Act)와 통합 리스크 관리(ERM, COSO-ERM 2017)로 연결된다.

```text
[IT 경영 관리 5대 영역의 상호작용 상세 흐름]

  +----------+    CSF/KPI     +----------+   SLA/OLA   +----------+
  | 사업부서  |--------------►| IT거버넌스|------------►|  IT운영   |
  | (Demand) |   Demand Mgmt |   위원회   |  Performance| (Service)|
  +----+-----+               +-----+----+   Mgmt      +----+-----+
       |                           |                       |
       | Demand                   | Policy                 | Incident
       v                           v                       v
  +----------+               +----------+             +----------+
  | 포트폴리오|               | 정책/표준 |             | 변경/배포 |
  | 관리(PPM)|◄--Prioritize--| (COBIT)  |---Guidance-►| (CAB)    |
  +----+-----+               +----+-----+             +----+-----+
       |                           |                       |
       | Resource                  | Compliance            | Monitoring
       v                           v                       v
  +-----------------------------------------------------------------+
  |   감리/감사 피드백 루프: ISMS-P(연1) + 내부감사(분기) + 외부감사(연1)  |
  +-----------------------------------------------------------------+
                                  |
                                  v
                       지속적 개선(Kaizen) -> 성숙도 상승
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 위원회 (IT Steering Committee)** | 의사결정·감독·자원 배분·리스크 승인 | COBIT 2019의 **EDM(Evaluate, Direct, Monitor)** 5개 프로세스(EDM01~05) 기반. 의장 CIO, 위원 사업부서장+CFO+CDO+CISO+내부감사. 분기별 개최, 안건: 투자 포트폴리오·중대 리스크·예산·아키텍처 결정. |
| **EA(Enterprise Architecture) & ISP** | 전략->아키텍처->구현->폐기 전 과정의 청사진 | **TOGAF 10 ADM**(Preliminary->A~H->Requirements Mgmt) 또는 **DoDAF/Zachman** 활용. 산출물: As-Is(현황), To-Be(목표), Gap Analysis, 마이그레이션 로드맵(4R: Rehost/Replatform/Refactor/Replace). 한국 공공부문은 **EA-Reference Model v3.0**(행정안전부) 의무 준수. |
| **IT 서비스 운영 (IT Service Management)** | 서비스의 설계·전환·운영·개선 | **ITIL 4**의 34개 Practice 중 핵심: Incident, Problem, Change Enablement, Service Request, Service Level, Continual Improvement. **DevOps/Agile(SRE)** 와 융합되어 DORA Metrics(배포 빈도·변경 Lead Time·변경 실패율·복구 시간)로 성과 측정. |
| **정보보안 및 컴플라이언스 (ISMS)** | 기밀성·무결성·가용성·인증·책임성 보장 | **ISMS-P 인증**(국내, PIMS 포함 102개 통제항목) + **ISO 27001:2022**(Annex A 93 통제, 4개 테마: 조직·인적·물리·기술) + **ISO 27701**(PIMS) + **ISO 27017**(클라우드) + **ISO 27018**(클라우드 개인정보) + **ISO 42001**(AI 관리체계, 2023년 최초 발표). 국내 클라우드는 **CSAP(클라우드 보안인증) I·II·Ⅲ** 등급제. |
| **변화 관리 및 리더십** | 사람·문화·역량의 전환 | **Kotter 8단계**(긴급성->연대->비전->전파->장애물제거->단기성과->확산->새문화) + **ADKAR**(인지->욕구->지식->능력->강화) + **Prosci 3-Phase Process**. 저항 분석: Lewin의 3단계(해빙->변화->재결빙). |
| **프로젝트·프로그램·포트폴리오 관리 (PPM)** | 전략 실행의 실행 통제 | **PMBOK 7th**(12 Principles + 8 Performance Domains), **PRINCE2 7th**(7 Practices/Themes), **SAFe 6.0**(Agile 스케일링). KPI: SPI(Schedule), CPI(Cost), EAC(Estimate At Completion), RSME(Risk Severity). |
| **IT 성과 및 가치 측정** | 투자의 정당화·학습·의사결정 | **BSC 4관점**(재무·고객·내부·학습성장) + **KPI Tree** + **NPV/IRR/Payback/ROI/TCO**. 정성효과: 사용자 만족도, 브랜드 신뢰, 리스크 회피액. 공공: **정보화사업 사업비 산정 가이드라인**(행정안전부) + **디지털서비스 영향평가**(2024~). |

### 핵심 알고리즘/모델/산식

- **EA 정합도 분석**: ADM Cycle Time = Σ(단계별 산출물 승인 시간). 이상치 > 30% 시 갭 분석.
- **COBIT 2019 Focus Area 매핑**: 11개 Focus Area(예: DevOps, Cyber Security, Privacy, Cloud, AI, ESG) 중 조직 목표(Enterprise Goals 13개, Alignment Goals 13개)와 매핑하여 목표 연쇄(Goals Cascade) 도출.
- **ISMS-P 위험 평가**: 위험도 = 자산가치(5단계) × 위협빈도(5단계) × 취약점(5단계) × 영향도. 허용 기준(예: ≥12점) 이상 통제 필수. ISO 27005와 동일 방법론.
- **TCO 산출**: TCO = CapEx(서버·네트워크·라이선스) + OpEx(인건비·전력·냉각·교육·지원) + Risk Cost(다운타임·브랜드) + End-of-Life Cost. 클라우드 비교 시 FinOps(Cost Optimization·Allocation·Anomaly Detection) 적용.
- **VCPU/ROI 산식**: ROI(%) = (총편익 − 총비용) / 총비용 × 100. 공공: B/C(Benefit/Cost) ≥ 1.0 권고.
- **DORA Metrics**: Elite ≤ 1시간 Lead Time, 15% 이하 Change Failure Rate, 1시간 이하 MTTR.

- **📢 섹션 요약 비유**: 5대 영역을 **"비행기의 5계통(엔진·날개·착륙장치·조종석·통신)"** 에 비유할 수 있다. 엔진(거버넌스)·날개(아키텍처)·착륙장치(운영)·조종석(보안)·통신(변화관리) 어느 하나가 고장나면 추락한다. 또한 5계통은 **비행 기록기(감리/감사)** 로 실시간 모니터링되어야 한다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 핵심 프레임워크 간 비교는 기술사 시험의 단골 출제 영역이다. 각 프레임워크는 탄생 배경·목적·적용 범위가 다르므로 **상호보완적(Complementary)** 으로 이해해야 한다.

| 구분 | **COBIT 2019** (거버넌스) | **ITIL 4** (서비스 운영) | **PMBOK 7th** (프로젝트) | **ISO 27001:2022** (보안) | **TOGAF 10** (아키텍처) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **출처/연도** | ISACA, 2019(2018 이전: COBIT 5) | AXELOS->PeopleCert, 2019 | PMI, 2021 | ISO/IEC, 2022(개정) | The Open Group, 2022 |
| **핵심 목적** | IT 거버넌스·관리 목표와 지표 | 서비스의 End-to-End 라이프사이클 | 프로젝트 성공·가치 전달 | 정보보호 관리체계(ISMS) | 아키텍처 개발 방법론 |
| **구조** | EDM(5) + APO/BAI/D
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 786 / 800

<- **이전**: [785. IT 경영 관리 핵심 토픽 785번 시험 요약](/studynote/12_it_management/05_security_compliance/785_it_management_core_topic_785_exam_summary/)
**다음**: [787. IT 경영 관리 핵심 토픽 787번 시험 요약](/studynote/12_it_management/05_security_compliance/787_it_management_core_topic_787_exam_summary/) ->

---
