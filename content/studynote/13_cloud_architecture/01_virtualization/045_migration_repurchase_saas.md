+++
title = "045. 클라우드 이전 전략 — Repurchase & SaaS Migration"
date = 2026-04-05

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

> **핵심 인사이트**
> 1. 클라우드 이전(Migration) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 6R(또는 7R) 프레임워크 — Retire(폐기), Retain(유지), Rehost([Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) & Shift), Replatform(이식), Repurchase([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 전환), [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)(재설계), Relocate(이전)으로 각 워크로드에 최적 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 선택한다.
> 2. Repurchase([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 재구매)는 사내 구축 소프트웨어를 SaaS로 교체 — 이메일(Exchange→Office 365), [CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/)(Siebel→Salesforce), [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)([온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)→SAP S/4HANA Cloud) 전환이 대표적이며, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용보다 장기 총소유비용([TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/)) 분석이 핵심이다.
> 3. [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 전환의 핵심 과제는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이전([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Migration)과 통합(Integration) — 수년간 축적된 레거시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모델로 변환하고, 기존 시스템과의 연동([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 통합)이 프로젝트 복잡성의 80%를 차지한다.

---

## Ⅰ. 클라우드 이전 6R



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">AWS 클라우드 이전 6R 프레임워크:</div>
<div class="kb-diagram-note">1. Retire (폐기):</div>
<div class="kb-diagram-note">더 이상 필요 없는 애플리케이션 폐기</div>
<div class="kb-diagram-note">예: 사용 안 하는 레거시 리포팅 도구</div>
<div class="kb-diagram-note">판단: 사용자 &lt; 5%, 비즈니스 가치 없음</div>
<div class="kb-diagram-note">결과: 비용 절감, 복잡성 감소</div>
<div class="kb-diagram-note">2. Retain (유지):</div>
<div class="kb-diagram-note">클라우드 이전 보류 (현재 위치 유지)</div>
<div class="kb-diagram-note">이유: 규제, 최근 업그레이드, 기술 부채 해결 우선</div>
<div class="kb-diagram-note">예: 6개월 내 EOL(End of Life) 예정 시스템</div>
<div class="kb-diagram-note">3. Rehost (Lift &amp; Shift):</div>
<div class="kb-diagram-note">코드·아키텍처 변경 없이 클라우드로 이전</div>
<div class="kb-diagram-note">속도: 빠름 (가장 간단)</div>
<div class="kb-diagram-note">비용: 초기 이전 이후 최적화 별도 필요</div>
<div class="kb-diagram-note">예: VM → EC2 1:1 이전</div>
<div class="kb-diagram-note">도구: AWS MGN (Application Migration Service)</div>
<div class="kb-diagram-note">4. Replatform (이식):</div>
<div class="kb-diagram-note">핵심 아키텍처 유지, 일부 최적화</div>
<div class="kb-diagram-note">예: DB → RDS (관리형 서비스), Tomcat → Elastic Beanstalk</div>
<div class="kb-diagram-note">비용 절감 + 운영 부담 감소</div>
<div class="kb-diagram-note">5. Repurchase (SaaS 재구매):</div>
<div class="kb-diagram-note">기존 On-Premise 소프트웨어 → SaaS 교체</div>
<div class="kb-diagram-note">예: Exchange → Microsoft 365</div>
<div class="kb-diagram-note">Siebel → Salesforce</div>
<div class="kb-diagram-note">개발/운영 부담 완전 제거</div>
<div class="kb-diagram-note">6. Refactor / Re-architect (재설계):</div>
<div class="kb-diagram-note">클라우드 네이티브 아키텍처로 완전 재설계</div>
<div class="kb-diagram-note">예: 모놀리식 → MSA + 컨테이너</div>
<div class="kb-diagram-note">비용: 가장 높음, 장기 이익 최대</div>
<div class="kb-diagram-note">적용: 핵심 비즈니스 차별화 서비스</div>
<div class="kb-diagram-note">선택 기준:</div>
<div class="kb-diagram-note">ROI 기준: Rehost(최저) ← → Refactor(최고)</div>
<div class="kb-diagram-note">기간 기준: Retire → Rehost → Repurchase → Refactor</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 6R은 이사 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) — 버리기(Retire), 두고가기(Retain), 그대로 옮기기(Rehost), 포장 개선(Replatform), 새 가구로 교체(Repurchase), 집 자체를 새로([Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/))!

---

## Ⅱ. Repurchase — [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 전환



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Repurchase SaaS 전환 유형:</div>
<div class="kb-diagram-note">이메일/협업:</div>
<div class="kb-diagram-note">On-Premise Exchange → Microsoft 365 (Exchange Online)</div>
<div class="kb-diagram-note">On-Premise 파일서버 → SharePoint Online / Teams</div>
<div class="kb-diagram-note">장점: 라이선스+서버+패치 비용 제거</div>
<div class="kb-diagram-note">비용: 사용자당 월 $12~35 (M365 E3)</div>
<div class="kb-diagram-note">CRM:</div>
<div class="kb-diagram-note">SAP CRM, Siebel → Salesforce</div>
<div class="kb-diagram-note">과정:</div>
<div class="kb-diagram-note">1. 데이터 이전 (Customer, Account, Opportunity)</div>
<div class="kb-diagram-note">2. 사용자 교육</div>
<div class="kb-diagram-note">3. 통합 (ERP, 마케팅 자동화)</div>
<div class="kb-diagram-note">4. 커스터마이제이션 (Flow, Apex)</div>
<div class="kb-diagram-note">ERP:</div>
<div class="kb-diagram-note">SAP ECC → SAP S/4HANA Cloud</div>
<div class="kb-diagram-note">Oracle EBS → Oracle Fusion Cloud</div>
<div class="kb-diagram-note">복잡도 최고: 핵심 비즈니스 프로세스</div>
<div class="kb-diagram-note">기간: 1~3년</div>
<div class="kb-diagram-note">비용: 수억~수백억</div>
<div class="kb-diagram-note">HR/급여:</div>
<div class="kb-diagram-note">자체 HR → Workday, SAP SuccessFactors</div>
<div class="kb-diagram-note">보안:</div>
<div class="kb-diagram-note">자체 방화벽/이메일 보안 → 클라우드 SEG (Proofpoint, Mimecast)</div>
<div class="kb-diagram-note">의사결정 기준:</div>
<div class="kb-diagram-note">SaaS 적합:</div>
<div class="kb-diagram-tree-item" style="--depth:1">공통 비즈니스 기능 (이메일, HR)</div>
<div class="kb-diagram-tree-item" style="--depth:1">차별화 필요 없음</div>
<div class="kb-diagram-tree-item" style="--depth:1">빠른 전환 필요</div>
<div class="kb-diagram-note">자체 개발 적합:</div>
<div class="kb-diagram-tree-item" style="--depth:1">핵심 경쟁 우위 기능</div>
<div class="kb-diagram-tree-item" style="--depth:1">특수 비즈니스 프로세스</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Repurchase는 식당 부엌 교체 — 직접 만든 낡은 냉장고([On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) 버리고, 최신 렌탈 냉장고([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)) 구독. 수리 걱정 없이 음식(비즈니스)만!

---

## Ⅲ. [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이전



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SaaS 데이터 이전 (Data Migration):</div>
<div class="kb-diagram-note">주요 단계:</div>
<div class="kb-diagram-note">1. 데이터 현황 분석:</div>
<div class="kb-diagram-note">소스 DB 스캔</div>
<div class="kb-diagram-note">데이터 품질 이슈 파악 (중복, 누락, 오류)</div>
<div class="kb-diagram-note">이전 범위 결정 (전체 vs 최근 X년)</div>
<div class="kb-diagram-note">2. 데이터 매핑:</div>
<div class="kb-diagram-note">소스 스키마 ↔ SaaS 데이터 모델 매핑</div>
<div class="kb-diagram-note">예: Siebel → Salesforce</div>
<div class="kb-diagram-note">Siebel: ACCOUNT.ACCOUNT_NAME → SF: Account.Name</div>
<div class="kb-diagram-note">Siebel: S_CONTACT.FST_NAME → SF: Contact.FirstName</div>
<div class="kb-diagram-note">3. ETL 구축:</div>
<div class="kb-diagram-note">Extract: 소스 DB에서 데이터 추출</div>
<div class="kb-diagram-note">Transform: 매핑에 따라 변환 + 정제</div>
<div class="kb-diagram-note">Load: Salesforce API로 업로드</div>
<div class="kb-diagram-note">도구: Informatica, Talend, MuleSoft, CSV + Data Loader</div>
<div class="kb-diagram-note">4. 검증:</div>
<div class="kb-diagram-note">건수 일치 확인</div>
<div class="kb-diagram-note">샘플링 검증 (수동)</div>
<div class="kb-diagram-note">업무팀 UAT</div>
<div class="kb-diagram-note">5. 컷오버:</div>
<div class="kb-diagram-note">이전 일정 (주말 또는 야간)</div>
<div class="kb-diagram-note">최종 델타 이전 (마지막 변경분)</div>
<div class="kb-diagram-note">전환 완료</div>
<div class="kb-diagram-note">이전 복잡성:</div>
<div class="kb-diagram-note">간단: 이메일 (메일박스 이전)</div>
<div class="kb-diagram-note">중간: CRM 고객 데이터</div>
<div class="kb-diagram-note">복잡: ERP (수십 년 트랜잭션 이력)</div>
<div class="kb-diagram-note">ERP 이전 전략:</div>
<div class="kb-diagram-note">신규 이력: SaaS</div>
<div class="kb-diagram-note">구 이력: 아카이브 또는 레거시 병행</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이전은 이사짐 정리 — 낡은 집(레거시)에서 짐([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 꺼내고, 새 집([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)) 크기에 맞게 정리(변환)해서 옮겨요. 이사짐이 많을수록 복잡!

---

## Ⅳ. [TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/) 분석



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SaaS 전환 TCO (Total Cost of Ownership) 분석:</div>
<div class="kb-diagram-note">On-Premise CRM 5년 TCO:</div>
<div class="kb-diagram-note">하드웨어: 1억 (서버 × 3)</div>
<div class="kb-diagram-note">SW 라이선스: 3억 (Siebel 영구)</div>
<div class="kb-diagram-note">DBA/운영 인력: 연 5천 × 5 = 2.5억</div>
<div class="kb-diagram-note">기반 SW (OS, DB): 0.5억</div>
<div class="kb-diagram-note">데이터센터 (전력, 공간): 0.3억</div>
<div class="kb-diagram-note">패치/업그레이드: 연 2천 × 5 = 1억</div>
<div class="kb-diagram-note">5년 총비용: 8.3억</div>
<div class="kb-diagram-note">Salesforce 5년 TCO:</div>
<div class="kb-diagram-note">구독료: 사용자 50명 × $150/월 × 12 × 5 = $450,000 ≈ 6억</div>
<div class="kb-diagram-note">구현/커스터마이징: 2억</div>
<div class="kb-diagram-note">통합 유지: 연 3천 × 5 = 1.5억</div>
<div class="kb-diagram-note">교육: 0.3억</div>
<div class="kb-diagram-note">5년 총비용: 9.8억</div>
<div class="kb-diagram-note">단순 숫자만 보면 On-Premise가 저렴!</div>
<div class="kb-diagram-note">추가 가치 고려:</div>
<div class="kb-diagram-note">Salesforce: 자동 업그레이드 (신기능 포함)</div>
<div class="kb-diagram-note">On-Premise: 업그레이드 프로젝트 별도 비용</div>
<div class="kb-diagram-note">Salesforce: 모바일·AI 기능 즉시 제공</div>
<div class="kb-diagram-note">On-Premise: 추가 개발 필요</div>
<div class="kb-diagram-note">Salesforce: 글로벌 접근 (원격 근무)</div>
<div class="kb-diagram-note">On-Premise: VPN 필수</div>
<div class="kb-diagram-note">TCO 결론:</div>
<div class="kb-diagram-note">단기(3년): On-Premise 유리할 수 있음</div>
<div class="kb-diagram-note">장기(5년+): SaaS 경쟁력 증가</div>
<div class="kb-diagram-note">기회비용 포함 시: SaaS 우위</div>
<div class="kb-diagram-note">핵심: 숫자만 보지 말고 전략적 유연성 포함 평가</div>
</div>
</div>



> 📢 **섹션 요약 비유**: TCO는 총 유지비용 — 새 차([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)) 월 리스료 vs 중고차([On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) 구입 후 수리비+보험. 겉 가격만 보지 말고 5년 총비용을 비교!

---

## Ⅴ. 실무 시나리오 — 글로벌 제조업 M365 전환



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">글로벌 제조업체 Microsoft 365 전환:</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">전 세계 30개국, 임직원 5만명</div>
<div class="kb-diagram-note">On-Premise Exchange 2013 (EOL 2023.10)</div>
<div class="kb-diagram-note">자체 파일 서버 수백 대</div>
<div class="kb-diagram-note">전환 결정:</div>
<div class="kb-diagram-note">Exchange 2013 EOL → 강제 이전 필요</div>
<div class="kb-diagram-note">신규 Exchange 서버 vs M365 선택</div>
<div class="kb-diagram-note">TCO 분석: 5년 기준 M365 2억 절감</div>
<div class="kb-diagram-note">→ M365 E3 선택</div>
<div class="kb-diagram-note">이전 전략:</div>
<div class="kb-diagram-note">물결 방식 (Wave Approach):</div>
<div class="kb-diagram-note">Wave 1: 본사 + 한국 (2,000명) — 파일럿</div>
<div class="kb-diagram-note">Wave 2~5: 지역별 순차 이전 (각 1만명)</div>
<div class="kb-diagram-note">총 기간: 8개월</div>
<div class="kb-diagram-note">기술 과제:</div>
<div class="kb-diagram-note">DNS 변경: MX 레코드 → EOP(Exchange Online Protection)</div>
<div class="kb-diagram-note">메일 데이터: Exchange Migration (ExchangeGUID 매핑)</div>
<div class="kb-diagram-note">공유 폴더: SharePoint Online 마이그레이션</div>
<div class="kb-diagram-note">(SharePoint Migration Tool)</div>
<div class="kb-diagram-note">통합:</div>
<div class="kb-diagram-note">SAP ↔ M365 (Azure AD SSO)</div>
<div class="kb-diagram-note">Teams ↔ 화상회의 레거시 → Teams Rooms</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">이전 완료: 8개월 (계획 대비 -1개월)</div>
<div class="kb-diagram-note">TCO 절감: 연 4억원</div>
<div class="kb-diagram-note">사용자 만족도: 4.2/5.0</div>
<div class="kb-diagram-note">보안: ATP (Advanced Threat Protection) 도입</div>
<div class="kb-diagram-note">원격근무 지원 크게 향상 (COVID-19 기간 중 완료)</div>
<div class="kb-diagram-note">교훈:</div>
<div class="kb-diagram-note">"사용자 변화관리 80%, 기술 20%"</div>
<div class="kb-diagram-note">현지화 교육이 채택률 결정적</div>
<div class="kb-diagram-note">IT-HR 협업 필수</div>
</div>
</div>



> 📢 **섹션 요약 비유**: M365 이전은 전국 지사 동시 이사 — 한 번에 5만 명 이사는 불가능, 물결([Wave](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/590_wave_ieee_802_11p_dsrc_v2x/))로 지역별 순차 이전. 기술보다 직원들 적응(변화관리)이 더 중요!

---

## 📌 관련 개념 맵

```
클라우드 이전 전략 (6R)
+-- Retire / Retain
+-- Rehost (Lift & Shift)
+-- Replatform
+-- Repurchase (SaaS)
|   +-- 이메일: M365
|   +-- CRM: Salesforce
|   +-- ERP: SAP Cloud
+-- Refactor (MSA/Cloud Native)
+-- 핵심 활동
    +-- TCO 분석
    +-- 데이터 이전 (ETL)
    +-- 통합 (API/iPaaS)
    +-- 변화 관리
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[클라우드 초기 이전 (2010s)]
Lift & Shift 주류
"빠른 이전"
      |
      v
[SaaS 폭발적 성장 (2012~)]
Salesforce, Workday, ServiceNow
Repurchase 트렌드 가속
      |
      v
[6R 프레임워크 (2017)]
AWS 마이그레이션 전략 공식화
워크로드별 최적 전략
      |
      v
[현재: 클라우드 네이티브 우선]
Refactor / 클라우드 네이티브
SaaS First 정책 (비커스텀 기능)
멀티클라우드 전략
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 6R은 이사 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 6가지 — 버리기(Retire), 그대로(Rehost), 일부 고치기(Replatform), 새 가구로 교체(Repurchase), 집 새로([Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/))! 상황에 맞는 방법 선택!
2. Repurchase는 구독 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 교체 — 직접 만든 낡은 냉장고(Exchange) 버리고, 매달 구독하는 새 냉장고(M365)로! 수리 걱정 끝!
3. TCO가 핵심 — "월 구독료([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/))가 비싸 보여도" 5년 총비용(서버+인건비+업그레이드) 합치면 SaaS가 저렴할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 44 / 371

← **이전**: [044. Re-factor & Re-architect — 클라우드 네이티브 MSA](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/044_refactor_re_architect_cloud_native_msa/)
**다음**: [046. 클라우드 마이그레이션 — Retire & Retain 전략](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/046_migration_retire_retain/) →

---
