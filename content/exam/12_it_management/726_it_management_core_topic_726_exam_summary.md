---
title: "IT Management Core Topic 726 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스·정보시스템 감리는 **COBIT 2019(Governance & Management Objectives 40개), ISO/IEC 38500:2015(평가·지시·모니터링 3원칙), ISACA IS Audit Framework(계획·수행·보고·후속조치)**를 기반으로, 정보시스템의 **전략적 정렬(Strategic Alignment), 가치 전달(Value Delivery), 위험 최적화(Risk Optimization), 자원 관리(Resource Management), 성과 측정(Performance Measurement)** 5대 핵심 영역을 통제·평가하는 경영 관리 체계이다.
> 2. **가치**: 정형화된 감리 수행 시 **프로젝트 실패율 30~50% 감소**(Standish Group CHAOS Report 기준), **감리 지적사항 평균 처리율 85% 이상**, **정보보안 사고 대응시간 60% 단축**(MTTD 14일->5일), **컴플라이언스 위반 비용 40% 절감**(GDPR/개인정보보호법 기준 평균 벌금 회피) 등 정량적 효과를 제공하며, 이사회-경영진-현업 간의 **3계층 의사결정 투명성**을 확보하여 조직의 디지털 트랜스포메이션 실패 리스크를 구조적으로 차단한다.
> 3. **판단 포인트**: (a) **감리 범위 설정** — 종합감리(연 1회, 전사)/상시감리(분기 1회, 핵심 SI)/수시감리(이슈 발생 시) 중 사업 연속성·이해관계자·비용 Trade-off, (b) **내부 통제 프레임워크 선택** — **COSO 2013 Internal Control(통제환경·위험평가·통제활동·정보통신·모니터링 5요소) vs COBIT 2019 vs ISO 27001(Annex A 93개 통제항목)** 중 조직 성숙도·산업 규제·국제 표준 부합성 기준, (c) **감리 도구 선정** — **CAAT(Computer-Assisted Audit Techniques) 도입 시 Tableau/Power BI 기반 데이터 분석 vs ACL/IDEA 기반 표본 추출 vs 자체 SQL 스크립트**의 정확성·재현성·비용 간 균형이 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

정보시스템 감리 및 IT 거버넌스는 1999년 「정보시스템 감리법」 제정(법률 제6040호, 2000년 1월 시행) 이래 대한민국 공공부문信息化建设 사업의 **성공률 제고·부패 방지·국민 신뢰 확보**를 목적으로 발전해 왔다. 초기에는 단순 **재무·계약 감사**(Financial Audit) 위주였으나, 2015년 「클라우드컴퓨팅법」, 2022년 개정 「개인정보 보호법」(GDPR과 유사성 강화), 2023년 「전자금융거래법」 개정, 그리고 2024년 AI 기본법(안) 등 **디지털 전환 거버넌스** 수요 증가로 인해 **IT 일반 통제(General Control) + IT 응용 통제(Application Control) + IT 거버넌스 통제(Governance Control)**의 3축 통합 감리가 요구되고 있다.

특히 **클라우드 전환**(AWS Organizations 기반 3-tier Landing Zone, Azure Landing Zone Architecture), **MSA/Microservices** 환경(EKS/AKS/GKE 기반 Service Mesh), **DevSecOps** 파이프라인(Jenkins X, GitLab CI, ArgoCD, Snyk, Trivy 통합) 등 기술적 복잡도 증가로 인해 전통적 **Waterfall 감리**(착수->요구사항->설계->구현->시험->종료 6단계)로는 한계가 명확해졌으며, **Agile 감리**(Sprint 단위 Risk-based Audit, Continuous Auditing) 패러다임으로 전환이 진행 중이다.

```text
+----------------------------------------------------------------------+
|            대한민국 정보시스템 감리 3계층 거버넌스 구조               |
+----------------------------------------------------------------------+
|                                                                      |
|  [1계층] 정책·감독 (Policy & Oversight)                              |
|  +--------------------------------------------------------+         |
|  |  • 국가정보화법 (제정 1999, 전부개정 2009)            |         |
|  |  • 정보시스템 감리법 (법률 제6040호)                  |         |
|  |  • 행정안전부 (국가정보화 업무 총괄)                  |         |
|  |  • 디지털위원회 (AI·데이터 거버넌스)                 |         |
|  |  • 개인정보보호위원회 (PIPC)                          |         |
|  +--------------+-----------------------------------------+         |
|                 | 정책 지침 하달                                       |
|                 v                                                     |
|  [2계층] 시행·수행 (Implementation)                                  |
|  +--------------------------------------------------------+         |
|  |  • 발주청 (중앙부처·지자체·공공기관)                 |         |
|  |  • 사업 주관부서 (정보화 담당관/PM)                  |         |
|  |  • SI 사업자 (1·2·3·4등급)                          |         |
|  |  • 감리법인 (한국감사원 등록 73개소)                  |         |
|  +--------------+-----------------------------------------+         |
|                 | 현장 적용                                            |
|                 v                                                     |
|  [3계층] 현장·기술 (Operational & Technical)                         |
|  +--------------------------------------------------------+         |
|  |  • 감리원 (정보시스템 감리사 자격 6,800여 명)         |         |
|  |  • CAAT Tool (ACL, IDEA, Tableau, Splunk)            |         |
|  |  • COBIT/COSO/ISO27001 통제 매핑                    |         |
|  |  • SIEM/SOC (ESG, AhnLab, S2W, Secuve)              |         |
|  +--------------------------------------------------------+         |
+----------------------------------------------------------------------+
```

**전통적 vs 현대적 감리 패러다임 비교**

| 구분 | 전통적 감리 (1999~2015) | 현대적 감리 (2016~현재) |
| :--- | :--- | :--- |
| **대상 시스템** | 온프레미스 모놀리식 (Mainframe, Unix) | 클라우드·MSA·AI·블록체인 |
| **감리 시점** | 사업 종료 후 사후 감리 | Agile Sprint 단위 실시간 감리 |
| **통제 중점** | 재무·계약·일정 | 보안·프라이버시·레지리언스·ESG |
| **도구** | 수기 표본 추출, 면담, 문서 검토 | **CAAT + AI/ML 기반 이상탐지 + Continuous Auditing** |
| **표준** | 한국정보통신기술협회(TTA) 감리지침 | **COBIT 2019 + ISO 38500 + DORA(2024 EU)** |
| **리스크** | 예산·일정 초과 | 사이버 공격·공급망 침투·AI 편향성 |

- **📢 섹션 요약 비유**: 정보시스템 감리는 **자동차의 종합검사**와 같다. 1999년대에는 출고 후 정기검사만 가능했다면, 지금은 **운행 중에도 OBD-Ⅱ 포트로 실시간 엔진·배기가스·타이어 공기압을 모니터링**하고, **OTA(Over-The-Air)**로 결함을 즉시 패치하는 **Connected Car 시대의 상시 진단 체계**로 진화한 셈이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

정보시스템 감리는 **3대 통제 영역**과 **5단계 감리 프로세스**, 그리고 **PDCA(Plan-Do-Check-Act) + 위험 기반 접근(Risk-Based Approach)**이 결합된 체계로 운영된다. 핵심 아키텍처는 **ISACA의 ITAF(Information Technology Assurance Framework) 4판**과 **행정안전부 「정보시스템 감리 가이드라인」(2023년 4차 개정)**을 기준으로 한다.

```text
+----------------------------------------------------------------------+
|         IT 거버넌스·감리 핵심 아키텍처 (3×5 Matrix)                  |
+----------------------------------------------------------------------+
|                                                                      |
|   통제영역(Control Domain)            감리단계(Audit Phase)          |
|   +----------------------+         +----------------------+         |
|   | G1. IT 거버넌스 통제 |         | P1. 계획(Planning)   |         |
|   |   (Governance Ctrl)  |<--------->|   - 리스크 평가      |         |
|   |   - 이사회/경영진    |         |   - 감리 전략 수립   |         |
|   |   - IT 전략 alignment|         |   - 자원 배분 (RAC) |         |
|   +----------------------+         +----------------------+         |
|   | G2. IT 일반 통제     |         | P2. 수행(Fieldwork)  |         |
|   |   (General Ctrl)     |<--------->|   - 통제 시험       |         |
|   |   - 접근통제(AC)     |         |   - 실증 절차       |         |
|   |   - 변경통제(CC)     |         |   - CAAT 적용       |         |
|   |   - 운영통제(OP)     |         |   - 표본 추출       |         |
|   +----------------------+         +----------------------+         |
|   | G3. IT 응용 통제     |         | P3. 평가(Evaluation) |         |
|   |   (Application Ctrl) |<--------->|   - 결함 식별       |         |
|   |   - 입력(IG)         |         |   - 영향 분석       |         |
|   |   - 처리(PG)         |         |   - 권고안 도출     |         |
|   |   - 출력(OG)         |         |   - 개선 과제화     |         |
|   +----------------------+         +----------------------+         |
|                                     | P4. 보고(Reporting)  |         |
|                                     |   - 감리보고서 작성  |         |
|                                     |   - 경영진 보고      |         |
|                                     |   - 이해관계자 통보 |         |
|                                     +----------------------+         |
|                                     | P5. 후속조치(F/U)    |         |
|                                     |   - 시정조치 검증    |         |
|                                     |   - 모니터링         |         |
|                                     |   - KPI 측정         |         |
|                                     +----------------------+         |
+----------------------------------------------------------------------+
```

### IT 일반 통제(General Control) 세부 통제 항목

| 통제영역 | 통제항목 | 핵심 통제 활동 | 도구/기술 | 위험 시나리오 |
| :--- | :--- | :--- | :--- | :--- |
| **AC-2: 계정 관리** | 사용자 등록·변경·삭제 절차 | JML(Joiner-Mover-Leaver) 프로세스, **IAM**(AWS IAM, Azure AD, Okta) RBAC 정책 | IAM 정책 위반, 퇴사자 계정 잔존 | 권한 상승, 데이터 유출 |
| **AC-6: 최소 권한** | Need-to-Know, Least Privilege | **JIT(Just-In-Time) 권한 상승**(Azure PIM), 권한 정기 재검토(Quarterly Access Review) | 권한 남용, 과도한 권한 누적 | 내부자 위협, 세션 하이재킹 |
| **AC-7: 다중 인증** | MFA·2FA 강제 | **FIDO2/WebAuthn**, TOTP, Push 인증, Hardware Token(YubiKey 5) | 피싱 자격증명 탈취, 패스워드 스프레이 | 계정 탈취, 랜섬웨어 진입 |
| **CC-2: 변경 통제** | SI 변경 영향 분석·승인·테스트·이관 | GitOps(ArgoCD, Flux), **CAB(Change Advisory Board)**, 4-eye principle | 비인가 변경, 프로덕션 오류 | 서비스 장애, 데이터 손상 |
| **CC-7: 모니터링** | SIEM 기반 이상 행위 탐지 | **Splunk Enterprise Security, Elastic SIEM, QRadar, Microsoft Sentinel**, UEBA(User Entity Behavior Analytics) | APT 침투, 횡적 이동(Lateral Movement) | 데이터 유출, 랜섬웨어 |
| **OP-4: 백업·복구** | RPO/RTO 정의·테스트 | **3-2-1-1-0 규칙**(원본 3개, 미디어 2종, 오프사이트 1개, 에어갭 1개, 오류 0개), Veeam·Zerto·Commvault | 재해 시 데이터 손실 | 비즈니스 중단, 매출 손실 |
| **OP-7: 취약점 관리** | 정기 취약점 스캔·패치 | **Tenable Nessus, Qualys VMDR, Rapid7 InsightVM**, SBOM(Software Bill of Materials) | 제로데이·Known CVE 미패치 | 데이터 유출, 규제 위반 |
| **CM-2: 기준선 설정** | 구성 항목(CI) 식별·기록 | **CMDB**(ServiceNow CMDB, Device42), IaC(Terraform, Ansible) 상태 추적 | 비인가 구성 변경, Shadow IT | 표준 미준수, 보안 사각지대 |
| **MP-4: 미디어 보호** | 저장 데이터 암호화, 전송 구간 TLS | **AES-256, KMS(Key Management Service)**, FIPS 140-2/3 인증 HSM | 평문 데이터 노출, 키 유출 | PII 유출, GDPR/개인정보보호법 위반 |
| **SC-7: 경계 보호** | 방화벽, IDS/IPS, WAF, NDR | **Palo Alto NGFW, Fortinet, AWS Network Firewall, Cloudflare WAF, Darktrace NDR**
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 726 / 800

<- **이전**: [725. IT 경영 관리 핵심 토픽 725번 시험 요약](/studynote/12_it_management/05_security_compliance/725_it_management_core_topic_725_exam_summary/)
**다음**: [727. IT 경영 관리 핵심 토픽 727번 시험 요약](/studynote/12_it_management/05_security_compliance/727_it_management_core_topic_727_exam_summary/) ->

---
