+++
title = "045. ITIL과 ITSM 프레임워크 — ITIL & ITSM"
date = 2026-04-05

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

> **핵심 인사이트**
> 1. [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/)([IT Infrastructure Library](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/))은 IT [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 관리([ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000_itsm_certification/))의 사실상 표준 프레임워크 — 영국 정부 CCTA가 1980년대 개발하고 현재 Axelos가 관리하며, IT [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 비즈니스 관점에서 제공·지원·개선하는 모범 사례([Best Practice](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/087_erp_package_advantages_best_practice/)) 집합이다.
> 2. [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) 4(2019)의 핵심은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 가치 시스템(SVS)과 [4차원 모델](/knowledge-base/studynote/12_it_management/02_itsm_itil/071_four_dimensions/) — 기존 프로세스 중심에서 [Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)·Lean을 통합한 가치 공동 창출 관점으로 진화하며, 34개 관리 관행(Practice)으로 구성된다.
> 3. [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000_itsm_certification/) 구현의 핵심 도전은 도구(Tool) 도입보다 문화(Culture) 변화 — ServiceNow 같은 [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000_itsm_certification/) 플랫폼만 도입한다고 ITIL이 작동하지 않으며, 인시던트 → 변경 → [문제 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/077_problem_management/)의 프로세스 규율이 필요하다.

---

## Ⅰ. [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) 역사와 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ITIL 발전 역사:</div>
<div class="kb-diagram-note">ITIL v1 (1989): 영국 정부 CCTA</div>
<div class="kb-diagram-note">31권의 책자 → IT 운영 모범 사례</div>
<div class="kb-diagram-note">ITIL v2 (2000): 표준화·통합</div>
<div class="kb-diagram-note">서비스 지원 + 서비스 전달 핵심</div>
<div class="kb-diagram-note">전 세계 확산 (ISO 20000 기반)</div>
<div class="kb-diagram-note">ITIL v3 (2007): 서비스 수명주기</div>
<div class="kb-diagram-note">서비스 전략, 설계, 전환, 운영, 지속적 개선</div>
<div class="kb-diagram-note">5권 구조</div>
<div class="kb-diagram-note">ITIL 4 (2019): 가치 중심 + 애자일</div>
<div class="kb-diagram-note">SVS (Service Value System)</div>
<div class="kb-diagram-note">4차원 모델</div>
<div class="kb-diagram-note">34개 관리 관행</div>
<div class="kb-diagram-note">ITIL 4 구조:</div>
<div class="kb-diagram-note">서비스 가치 시스템 (SVS):</div>
<div class="kb-diagram-note">외부 기회/수요 → 가치 창출</div>
<div class="kb-diagram-note">구성 요소:</div>
<div class="kb-diagram-tree-item" style="--depth:1">거버넌스 (Governance)</div>
<div class="kb-diagram-tree-item" style="--depth:1">서비스 가치 체인 (SVC)</div>
<div class="kb-diagram-tree-item" style="--depth:1">지속적 개선</div>
<div class="kb-diagram-tree-item" style="--depth:1">관리 관행 (34개)</div>
<div class="kb-diagram-tree-item" style="--depth:1">안내 원칙 (7개)</div>
<div class="kb-diagram-note">4차원 모델:</div>
<div class="kb-diagram-note">1. 조직 및 인력</div>
<div class="kb-diagram-note">2. 정보 및 기술</div>
<div class="kb-diagram-note">3. 파트너 및 공급자</div>
<div class="kb-diagram-note">4. 가치 흐름 및 프로세스</div>
</div>
</div>



> 📢 **섹션 요약 비유**: ITIL은 IT [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 레시피북 — 수십 년간 쌓인 IT 운영 모범 사례를 책으로 정리. [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) 4는 "요즘 트렌드([애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)) 반영 개정판"!

---

## Ⅱ. 핵심 관리 관행 ([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) Practices)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ITIL 4 주요 관리 관행:</div>
<div class="kb-diagram-note">인시던트 관리 (Incident Management):</div>
<div class="kb-diagram-note">목적: 비정상적 서비스 복구</div>
<div class="kb-diagram-note">흐름:</div>
<div class="kb-diagram-note">인시던트 발생 → 분류/우선순위</div>
<div class="kb-diagram-note">→ 조사/진단 → 해결 → 종료</div>
<div class="kb-diagram-note">SLA 준수:</div>
<div class="kb-diagram-note">P1 (Critical): 1시간 내 해결</div>
<div class="kb-diagram-note">P2 (High): 4시간</div>
<div class="kb-diagram-note">P3 (Medium): 8시간</div>
<div class="kb-diagram-note">문제 관리 (Problem Management):</div>
<div class="kb-diagram-note">목적: 인시던트 근본 원인 제거</div>
<div class="kb-diagram-note">반응적: 반복 인시던트 → 근본 원인 분석</div>
<div class="kb-diagram-note">예방적: 잠재 문제 사전 식별</div>
<div class="kb-diagram-note">RCA (Root Cause Analysis):</div>
<div class="kb-diagram-note">5 Whys, 피시본(Ishikawa) 다이어그램</div>
<div class="kb-diagram-note">변경 가능화 (Change Enablement):</div>
<div class="kb-diagram-note">목적: 위험 최소화하며 변경 구현</div>
<div class="kb-diagram-note">변경 유형:</div>
<div class="kb-diagram-tree-item" style="--depth:1">표준 변경: 사전 승인 (낮은 위험)</div>
<div class="kb-diagram-tree-item" style="--depth:1">일반 변경: CAB 승인 필요</div>
<div class="kb-diagram-tree-item" style="--depth:1">긴급 변경: ECAB 긴급 승인</div>
<div class="kb-diagram-note">CAB: Change Advisory Board</div>
<div class="kb-diagram-note">서비스 데스크 (Service Desk):</div>
<div class="kb-diagram-note">단일 접촉 창구 (SPOC)</div>
<div class="kb-diagram-note">인시던트/서비스 요청 접수·조율</div>
<div class="kb-diagram-note">변경 설정 관리 (CMDB):</div>
<div class="kb-diagram-note">CI (Configuration Item): IT 구성 요소</div>
<div class="kb-diagram-note">CMDB: CI 정보·관계 데이터베이스</div>
<div class="kb-diagram-note">→ 변경 영향 분석 기반</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) 관행들은 병원 운영 — [서비스 데스크](/knowledge-base/studynote/12_it_management/02_itsm_itil/072_service_desk/)(응급실 접수), 인시던트(응급 처치), [문제 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/077_problem_management/)(병원균 박멸), [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)(수술 계획 승인)!

---

## Ⅲ. 7가지 안내 원칙

```
ITIL 4 안내 원칙 (Guiding Principles):

1. 가치에 집중 (Focus on Value):
   모든 활동이 이해관계자 가치로 연결
   "이게 고객에게 어떤 가치인가?"

2. 현재 상태에서 시작 (Start Where You Are):
   기존 리소스·역량 최대 활용
   Zero-base 보다 점진적 개선

3. 반복적 피드백과 함께 진보 (Progress Iteratively):
   작은 단계로 빠른 개선
   애자일 스프린트 적용

4. 협업하고 가시성 높이기 (Collaborate & Promote Visibility):
   사일로 제거, 정보 공유

5. 전체적으로 사고하고 작업하기 (Think & Work Holistically):
   부분 최적화 아닌 전체 최적화
   가치 흐름 전체 시각

6. 단순하고 실용적으로 유지 (Keep It Simple & Practical):
   불필요한 절차 제거
   결과에 기여하지 않는 것은 제거

7. 최적화하고 자동화 (Optimize & Automate):
   반복 작업 자동화
   인간은 가치 있는 작업에 집중

실무 적용:
  원칙 1+7: 가치 있는 것만 자동화
  원칙 3+4: 스크럼 + 데일리 스탠드업
  원칙 5: 엔드투엔드 서비스 맵핑
```

> 📢 **섹션 요약 비유**: 7원칙은 IT팀 팀워크 규칙 — "가치 집중, 지금부터 시작, 조금씩 개선, 함께 공유, 전체 시각, 복잡하지 않게, 자동화!" 팀이 이 원칙으로 움직이면 [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000_itsm_certification/) 성공!

---

## Ⅳ. [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000_itsm_certification/) 도구 — ServiceNow



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ITSM 플랫폼 대표: ServiceNow</div>
<div class="kb-diagram-note">모듈:</div>
<div class="kb-diagram-note">ITSM:</div>
<div class="kb-diagram-tree-item" style="--depth:1">Incident Management</div>
<div class="kb-diagram-tree-item" style="--depth:1">Problem Management</div>
<div class="kb-diagram-tree-item" style="--depth:1">Change Management</div>
<div class="kb-diagram-tree-item" style="--depth:1">Service Catalog</div>
<div class="kb-diagram-tree-item" style="--depth:1">CMDB</div>
<div class="kb-diagram-note">ITOM (IT Operations Management):</div>
<div class="kb-diagram-tree-item" style="--depth:1">인프라 모니터링</div>
<div class="kb-diagram-tree-item" style="--depth:1">자동화</div>
<div class="kb-diagram-note">HRSD, CSM 등 ITSM 개념 확장</div>
<div class="kb-diagram-note">CMDB 활용:</div>
<div class="kb-diagram-note">CI 관계 맵:</div>
<div class="kb-diagram-note">서버A ──(호스팅)──&gt; 애플리케이션X</div>
<div class="kb-diagram-note">애플리케이션X ──(의존)──&gt; 데이터베이스Y</div>
<div class="kb-diagram-note">변경 영향 분석:</div>
<div class="kb-diagram-note">"서버A 패치 → 어떤 서비스 영향?"</div>
<div class="kb-diagram-note">→ CMDB 관계 조회 → 영향 범위 자동 계산</div>
<div class="kb-diagram-note">인시던트 자동화:</div>
<div class="kb-diagram-note">모니터링 경보 → ServiceNow API → 인시던트 자동 생성</div>
<div class="kb-diagram-note">AI 분류기 → 우선순위·담당자 자동 배정</div>
<div class="kb-diagram-note">MTTR 단축:</div>
<div class="kb-diagram-note">수동 생성: 15분 → 자동 생성: 2분</div>
<div class="kb-diagram-note">지식 관리:</div>
<div class="kb-diagram-note">반복 인시던트 → 지식 베이스 문서화</div>
<div class="kb-diagram-note">→ 검색 → 1차 해결율 향상</div>
<div class="kb-diagram-note">KPI:</div>
<div class="kb-diagram-note">FCR (First Contact Resolution): 70%+ 목표</div>
<div class="kb-diagram-note">CSAT (Customer Satisfaction): 4.0/5.0 이상</div>
<div class="kb-diagram-note">기타 ITSM 도구:</div>
<div class="kb-diagram-note">Jira Service Management (Atlassian)</div>
<div class="kb-diagram-note">Freshservice</div>
<div class="kb-diagram-note">BMC Remedy</div>
<div class="kb-diagram-note">Zendesk (IT 응용)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: ServiceNow는 IT팀 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) — 인시던트(고장 신고), 변경(수리 계획), [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/)(부품 목록) 모두 한 시스템에서 관리. [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) 프로세스를 디지털화!

---

## Ⅴ. 실무 시나리오 — 대기업 [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000_itsm_certification/) 도입



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">금융그룹 ITSM 혁신 프로젝트:</div>
<div class="kb-diagram-note">현황 문제:</div>
<div class="kb-diagram-tree-item" style="--depth:1">IT 장애 시 담당자 파악에 1시간+</div>
<div class="kb-diagram-tree-item" style="--depth:1">변경 관리 없이 배포 → 장애 빈발</div>
<div class="kb-diagram-tree-item" style="--depth:1">MTTR: 평균 4시간</div>
<div class="kb-diagram-tree-item" style="--depth:1">장애 원인 분석 없이 임시 처방 반복</div>
<div class="kb-diagram-note">ITSM 도입 계획 (6개월):</div>
<div class="kb-diagram-note">Phase 1 (1-2개월): 기반 구축</div>
<div class="kb-diagram-note">CMDB 구축: 서버 500대, 애플리케이션 100개</div>
<div class="kb-diagram-note">CI 관계 맵핑</div>
<div class="kb-diagram-note">ServiceNow 기본 설정</div>
<div class="kb-diagram-note">Phase 2 (3-4개월): 프로세스 확립</div>
<div class="kb-diagram-note">인시던트 관리: 우선순위 체계, SLA 설정</div>
<div class="kb-diagram-note">변경 관리: CAB 구성, 변경 절차</div>
<div class="kb-diagram-note">서비스 데스크: 헬프데스크 → SPOC 전환</div>
<div class="kb-diagram-note">Phase 3 (5-6개월): 자동화</div>
<div class="kb-diagram-note">모니터링 → 인시던트 자동 생성</div>
<div class="kb-diagram-note">표준 변경 자동 승인</div>
<div class="kb-diagram-note">AI 기반 분류·배정</div>
<div class="kb-diagram-note">결과 (1년 후):</div>
<div class="kb-diagram-note">MTTR: 4시간 → 45분 (배정 자동화 효과)</div>
<div class="kb-diagram-note">변경 관련 장애: 40% 감소</div>
<div class="kb-diagram-note">FCR: 45% → 68%</div>
<div class="kb-diagram-note">장애 재발률: 60% 감소 (문제 관리 효과)</div>
<div class="kb-diagram-note">핵심 교훈:</div>
<div class="kb-diagram-note">"도구는 20%, 프로세스와 문화가 80%"</div>
<div class="kb-diagram-note">CAB 참석자 저항 → 변경 관리 문화 정착 6개월 소요</div>
<div class="kb-diagram-note">CMDB 정확도 유지가 지속 과제</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 금융그룹 ITSM은 소방서 체계화 — 불 나면(인시던트) 빨리 끄고(해결), 왜 났는지([문제 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/077_problem_management/)) 분석, 건물 공사(변경) 전 심사([CAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_cab/)). 체계가 없으면 매번 같은 불!

---

## 📌 관련 개념 맵

```
ITIL / ITSM
+-- ITIL 4 구조
|   +-- SVS (서비스 가치 시스템)
|   +-- 34개 관리 관행
|   +-- 7가지 안내 원칙
+-- 핵심 관행
|   +-- 인시던트 관리
|   +-- 문제 관리 (RCA)
|   +-- 변경 가능화 (CAB)
|   +-- CMDB
+-- 도구
|   +-- ServiceNow
|   +-- Jira Service Management
+-- 관련 표준
    +-- ISO 20000 (ITSM 표준)
    +-- COBIT (IT 거버넌스)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[ITIL v1 (1989)]
영국 정부 CCTA 발행
31권 모범 사례 문서
      |
      v
[ITIL v2/v3 (2000~2007)]
글로벌 표준화
ISO 20000 연계
      |
      v
[ITSM 도구 성숙 (2010s)]
ServiceNow 성장
클라우드 ITSM SaaS
      |
      v
[ITIL 4 (2019)]
애자일·DevOps 통합
가치 공동 창출 패러다임
SRE와 ITSM 융합
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. ITIL은 IT팀 운영 교과서 — 수십 년간 전 세계 IT팀이 쌓은 경험을 책으로 정리한 것. 이 교과서대로 하면 IT [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 잘 돌아가요!
2. 인시던트는 응급실, [문제 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/077_problem_management/)는 예방 접종 — 불 났을 때(인시던트) 빠르게 끄고, 왜 불이 났는지(문제) 찾아서 다시 안 나게 해요!
3. CMDB는 IT 지도 — 서버, 앱, DB가 어떻게 연결됐는지 지도([CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/)). 뭔가 바꿀 때(변경) 지도 보고 영향 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 45 / 482

← **이전**: [044. 기업 애자일 경영](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/044_agile_management_enterprise/)
**다음**: [046. IT 서비스 관리 — ITSM 심화](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/046_itsm_it_service_management/) →

---
