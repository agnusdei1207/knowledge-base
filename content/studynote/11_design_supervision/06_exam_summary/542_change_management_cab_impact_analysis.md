---
title: "542. 변경 관리 CAB 영향 분석 승인 (Change Management CAB Impact Analysis)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ITIL Change Management의 CAB(Change Advisory Board, 변경 자문 위원회)는 표준/긴급/주요 변경에 대해 다학제적 이해관계자(Change Manager, 기술 책임자, 보안/컴플라이언스, 서비스 오너, 인프라/DB/네트워크 SME)가 RFC(Request for Change, 변경 요청서)의 7R's(Requestor, Reason, Return, Risks, Resources, Responsibility, Relationship) 및 CIA(Confidentiality, Integrity, Availability) + RTO/RPO 기준 영향 분석을 수행하고 Go/No-go를 결정하는 공식 거버넌스 메커니즘이다.
> 2. **가치**: 성숙한 CAB 운영을 통해 변경 실패율 60%v(Forrester, 2023), 계획되지 않은 장애 41%v(ITSM.tools 산업 벤치마크), MTTR(Mean Time To Restore) 28% 개선, 컴플라이언스 감사 결함 73% 감소의 정량 효과를 달성하며, CMDB(Configuration Management Database) 기반 의존성 매핑과 결합 시 "한 줄 변경이 전체 결제 시스템 다운" 같은 폭발 반경(Blast Radius) 예측 정확도를 90% 이상으로 끌어올린다.
> 3. **판단 포인트**: 기술사는 (a) CAB 회의 주기(일일/주간/Ad-hoc)와 Emergency CAB(ECAB) 발동 기준의 분리, (b) "Risk-based Approval Matrix"를 통한 저위험 변경의 Pre-authorization, (c) DevOps 파이프라인의 CI/CD 자동 변경과 CAB 수동 승인 간의 경계 설계, (d) Shadow IT·SaaS 변경에 대한 CAB 적용 범위 확장 여부를 설계적 트레이드오프로 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

IT 환경은 모놀리식에서 MSA(Microservices Architecture), 온프레미스에서 컨테이너 오케스트레이션(Kubernetes), 수동 배포에서 GitOps/IaC(Infrastructure as Code)로 급격히 진화했다. 그러나 "변경(Change)"은 여전히 시스템 장애의 1위 원인이라는 통계는 변하지 않는다—PagerDuty "State of Digital Operations 2024"에 따르면, 전체 프로덕션 장애의 **74%**가 변경에 기인한다. 특히 2024년 7월 CrowdStrike Falcon 업데이트의 글로벌 8.5M대 Windows 장애, 2023년 6월 한국 편의점 결제 망 일시 중단 등은 모두 "검증 부재의 변경"이 만들어낸 대형 사고다.

이러한 환경에서 **변경 관리(Change Management)**는 ITIL Service Transition의 핵심 프로세스로서, 변경의 생애주기(요청->평가->승인->구현->검토)를 통제하여 비즈니스 연속성을 보장한다. 그리고 이 통제의 중심에 **CAB(Change Advisory Board)**가 위치한다. CAB는 단순한 "결재 라인"이 아니라, RFC의 **영향 분석(Impact Analysis)**을 다각도로 수행하고 **승인(Approval)** 권한을 가진 의사결정 기구다.

기존 패러다임(Pre-2000s)에서는 "한 명의 시니어 엔지니어가 야간에 서버에 패치 적용" 식의 암묵적 변경 관행이 만연했다. 이는 지식 공유 부재, 롤백 불가, 감사 추적 결핍, 사일로별 변경 충돌이라는 4대 문제를 야기했다. ITIL v2(2001)->v3(2007)->2011->2019(v4) 로의 진화, 그리고 COBIT 2019, ISO/IEC 20000:2018, NIST SP 800-128 같은 표준들이 CAB 기반의 체계적 변경 관리를 요구하면서, **CAB 영향 분석·승인**은 엔터프라이즈 IT 거버넌스의 필수 컴플라이언스 항목이 되었다.

```text
+-----------------------------------------------------------------------------+
|              변경 관리의 진화: 암묵적 관행 -> CAB 중심 거버넌스                 |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [Pre-2000s: 암묵적 변경]      [ITIL v2~v3: CAB 도입]    [ITIL 4 / DevOps 시대]|
|                                                                             |
|  +--------------+           +--------------+          +------------------+  |
|  | 시니어 엔지니 |           | CAB 주간회의  |          | Risk-based Matrix|  |
|  | 어 야간 패치  |  ------->  | + 표준변경   | ------->  | + 자동승인 게이트 |  |
|  | (no audit)   |           | + ECAB       |          | + CI/CD 통합     |  |
|  +--------------+           +--------------+          +------------------+  |
|         |                          |                          |             |
|         v                          v                          v             |
|   • 장애의 74%가 변경  • 회의 비효율/병목           • 자동화/사람 결정 분리  |
|   • 감사 추적 불가     • Shadow IT 증가            • CAB를 "리스크 자문"으|
|   • 롤백 계획 부재     • DevOps와 충돌              |  로 재정의          |
+-----------------------------------------------------------------------------+
```

한국 환경에서는 금융감독원의 `전자금융감독규정` 및 `금융회사 IT 통제기준`, 개인정보보호법의 안전조치, 클라우드 보안인증(CSAP) 등에서 변경 관리 통제를 명시적으로 요구하고 있어, CAB 영향 분석·승인은 **컴플라이언스 필수 통제(Required Control)**이다.

- **📢 섹션 요약 비유**: CAB는 "병원 수술팀의 수술 전 컨퍼런스(Tumor Board)"와 같다. 외과 의사가 단독으로 칼을 들지 못하게, 마취과·내과·영상의학과·병리과가 함께 CT/MRI 결과를 보며 "수술의 위험도, 절제 범위, 대체 치료법, 응급 시 계획(B计划)"을 함께 검토하는 다학제 회의다. 이 회의의 결과가 바로 "수술 진행/중단/연기"의 CAB 승인 결정이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CAB 영향 분석·승인 프로세스는 크게 **① RFC 등록 ② 자동 사전 분석 ③ CAB 회의 ④ 승인/반려 ⑤ 구현 ⑥ PIR(Post-Implementation Review)**의 6단계로 구성된다. 각 단계는 CMDB, ITSM 툴(ServiceNow/Jira/BMC Remedy), CI/CD 파이프라인, 보안 스캔 도구와 통합된다.

```text
+------------------------------------------------------------------------------+
|                CAB 영향 분석·승인 전체 아키텍처 (End-to-End Flow)              |
+------------------------------------------------------------------------------+

  [1. RFC 작성]        [2. 자동 사전 분석]        [3. CAB 회의]
  +------------+       +----------------+         +----------------+
  | Change     |       | • 7R's 검증     |         | 정기 CAB       |
  | Requester  |------->| • CMDB 매핑     |--------->| (주 1~2회)     |
  | (개발/운영) |       | • 의존성 그래프  |         |                |
  +------------+       | • 자동 위험 점수 |         | 참석자:        |
                       | • 정책 컴플라이언스|         |  • Change Mgr  |
                       +--------+-------+         |  • Change Owner|
                                |                 |  • 보안/컴플   |
                                v                 |  • 서비스 오너 |
                       +----------------+         |  • 인프라 SME  |
                       | Risk Score     |         |  • DBA/네트워크|
                       | L: 1~4 (저)    |         |  • 외부 벤더   |
                       | M: 5~9 (중)    |         +-------+--------+
                       | H: 10~16 (고)  |                 |
                       | E: 17+ (긴급)  |                 v
                       +--------+-------+         +----------------+
                                |                 | 영향 분석 보고서|
                                |                 | • CIA 영향      |
                                |                 | • 의존 서비스   |
                                |                 | • RTO/RPO      |
                                |                 | • Backout Plan |
                                |                 | • 테스트 결과   |
                                |                 | • 자원(자원/창) |
                                |                 +-------+--------+
                                |                         |
                                v                         v
                       [4. 승인 결정]            [5. 변경 구현]
                       +----------------+         +----------------+
                       | • Approved     |--------->| • 변경 창(Window)|
                       | • Conditionally|         | • 4-Eyes 원칙  |
                       | • Rejected     |         | • 자동 롤백 트리|
                       | • Deferred     |         | • 실시간 모니터 |
                       +--------+-------+         +-------+--------+
                                |                         |
                                |                         v
                                |                 [6. PIR]
                                |                 +----------------+
                                +----------------->|• KPI 비교      |
                                                  |• Inc 발생 여부 |
                                                  |• 교훈 도출      |
                                                  |• CMDB 갱신     |
                                                  +----------------+
```

### 영향 분석의 7대 핵심 축 (Impact Analysis Dimensions)

CAB는 단일 차원이 아니라 다음 7개 축을 다차원 분석한다. ITIL 4 "Change Management Practice Guide"와 `ISO/IEC 20000-1:2018 §8.5.1`의 통제 요구사항을 결합한 종합 프레임워크다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **RFC & 7R's 검증** | 변경의 완전성·정합성 검증 | `Requestor`(변경 요청자), `Reason`(근본 원인), `Return`(기대 효과), `Risks`(식별된 위험), `Resources`(필요 자원: 인력/예산/도구), `Responsibility`(R&R 매트릭스/RACI), `Relationship`(다른 변경·인시던트·문제와의 연관). 미충족 시 RFC 거부. **ServiceNow** `sn_chg_rfc` 테이블, **Jira Service Management** "Change" 이슈 타입에서 강제 필드로 적용. |
| **CMDB 의존성 매핑 (Blast Radius)** | 영향받는 CI(Configuration Item)와 서비스 도출 | `ServiceNow CMDB`, **BMC Discovery**, **Device42** 등으로 CI 간 의존성(`Depends on::Used by::Connected to`) 그래프 구축. 핵심 서비스(예: 결제 게이트웨이)에 매핑되는 CI 개수 = 영향 반경. **ServiceNow "Change Risk Calculator"**는 CMDB 의존성 깊이(2-hop, 3-hop) 기반 위험 점수 자동 산정. |
| **CIA + RTO/RPO 영향** | 보안·가용성 영향 정량화 | **CIA**: Confidentiality(데이터 노출 위험), Integrity(데이터 변조 위험), Availability(가용성 손실). **RTO**(Recovery Time Objective, 복구 목표 시간), **RPO**(Recovery Point Objective, 복구 시점 목표). 변경으로 인해 RTO/RPO가 미충족 시 자동 차단. 예: OLTP DB 인덱스 재구성 -> RTO 30분 초과 시 Reject. |
| **위험 매트릭스 (Risk Matrix)** | 발생 가능성 × 영향도 정량화 | 5×5 매트릭스 사용. 가능성(Likelihood, 1~5) × 영향도(Impact, 1~5) = 위험 점수(1~25). 점수별 자동 라우팅: 1~4=Pre-authorized(사전 승인), 5~9=단순 검토, 10~16=정기 CAB, 17+=ECAB 또는 거부. **FMEA(Failure Mode and Effects Analysis)** RPN(Risk Priority Number) 기반 확장 모델. |
| **Backout Plan (롤백 계획)** | 실패 시 복구 가능성 보장 | 변경 실패 감지 기준(예: HTTP 5xx > 1% 상승, CPU > 90% 5분 지속, 에러율 0.5%->2%) + 자동 트리거 스크립트 + 수동 검증 절차. **ServiceNow** `Backout Plan` 필드(200자 이상), **GitOps** 환경에서는 `git revert` + Argo Rollouts 기반 카나리 분석과 통합. 테스트 필수. |
| **변경 창(Change Window) & 동시성 검사** | 동일 시간대 변경 충돌 방지 | 변경 캘린더(Change Calendar) 시각화. 같은 CI/서비스에 대한 동시 변경은 자동 경고. **금융권 메인뱅킹**은 일요일 02:00~06:00 등 정해진 Blackout(금지 시간대) 적용. **ServiceNow "Change Conflict Detection"**가 동일 CI/시간/팀 변경을 자동 탐지. |
| **승인 매트릭스 (Approval Matrix)** | 역할 기반 다단계 승인 | RACI(Responsible, Accountable, Consulted, Informed) 기반. 주요 변경(Major Change) 시 CIO 또는 변화 관리 책임자(Change Manager) 승인 필수. **4-Eyes Principle**(2인 승인), 6-Eyes(3인) 규칙 적용. SAP/Oracle ERP 등 업무 영향도 높은 시스템은 별도 Application Owner 승인 추가. |

### 위험 점수 산정 알고리즘 (Risk Score Algorithm)

CAB 영향 분석의 정량적 핵심은 **위험 점수(Risk Score)** 자동 산정이다. 다음은 ServiceNow가 내부적으로 사용하는 것과 유사한 가중치 모델이다.

```
RiskScore = (C × Wc) + (I × Wi) + (A × Wa) + (D × Wd) + (T × Wt) + (N × Wn) + (H × Wh)

여기서:
  C = Change Complexity (변경 복잡도) 1~5
  I = Impact (영향받는 사용자/트랜잭션 수) 1~5
  A = Availability Impact (가용성 영향) 1~5
  D = Dependency Depth (CMDB 의존 깊이) 1~5
  T = Test Coverage (테스트 커버리지) 1~5 (낮을수록 위험)
  N = Novelty (신규 기술/미경험 변경) 1~5
  H = History (이전 동일 변경 실패 이력) 1~5

  가중치 (금융권 표준): Wc=2.0, Wi=3.0, Wa=4.0, Wd=2.5, Wt=2.0, Wn=1.5, Wh=2.0
  (총 가중치 합 = 17.0, 최대 점수 = 85.0)

  임계값:
    0~20  : Low Risk  -> Pre-authorized (자동 승인)
    21~40 : Medium    -> 단일 승인자(Change Manager)
    42~60 : High      -> 정기 CAB 회의
    61+   : Critical  -> ECAB + 임원진 승인

  예시: ① OS 패치 (C=2, I=2, A=3, D=1, T=2, N=1, H=1)
        RiskScore = (2×2.0)+(2×3.0)+(3×4.0)+(1×2.5)+(2×2.0)+(1×1.5)+(1×2.0)
                  = 4.0 + 6.0 + 12.0 + 2.5 + 4.0 + 1.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 542 / 600

<- **이전**: [541. 문제 관리 근본 원인 분석 RCA](/studynote/12_it_management/05_security_compliance/428_problem_management_root_cause_analysis)
**다음**: [543. 서비스 수준 관리 SLA SLO SLI](/studynote/11_design_supervision/06_exam_summary/543_service_level_management_sla_slo_sli/) ->

---
