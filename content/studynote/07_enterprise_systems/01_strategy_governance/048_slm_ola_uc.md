+++
title = "048. SLM·OLA·UC — 서비스 수준 관리 체계"
date = 2026-04-05

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

> **핵심 인사이트**
> 1. [SLM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/313_slm/)([Service Level Management](/knowledge-base/studynote/12_it_management/02_itsm_itil/084_service_level_management/))은 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)·[OLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/)·[UC](/knowledge-base/studynote/12_it_management/02_itsm_itil/087_underpinning_contract/) 계층으로 이루어진 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 보증 체계 — SLA는 고객 대면 계약, OLA는 내부 팀 간 합의, UC는 외부 공급자와의 계약으로, 세 계층이 정합성을 가져야 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 이행이 가능하다.
> 2. [OLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/)([Operational Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/))가 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 이행의 실질적 기반 — [서비스 데스크](/knowledge-base/studynote/12_it_management/02_itsm_itil/072_service_desk/), 네트워크팀, 서버팀 간 내부 SLA가 없으면 고객 SLA가 깨지는 병목을 어디서도 파악하지 못한다.
> 3. [SLM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/313_slm/) 구현의 함정 — 계약서에만 SLA를 명시하고 [OLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/) 합의와 측정 도구를 갖추지 않으면 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 위반 시 책임 소재를 찾을 수 없는 "서류상의 [SLM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/313_slm/)"으로 전락한다.

---

## Ⅰ. [SLM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/313_slm/) 계층 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SLM (Service Level Management):</div>
<div class="kb-diagram-note">IT 서비스가 합의된 수준으로 제공됨을 보장하는 프로세스</div>
<div class="kb-diagram-note">ITIL v4 핵심 관리 관행</div>
<div class="kb-diagram-note">3계층 구조:</div>
<div class="kb-diagram-note">고객</div>
<div class="kb-diagram-note">SLA (Service Level Agreement): 고객 ↔ IT 서비스 제공자</div>
<div class="kb-diagram-note">"IT 부서가 고객에게 제공하는 서비스 수준"</div>
<div class="kb-diagram-note">IT 서비스 제공자 (내부)</div>
<div class="kb-diagram-note">OLA (Operational Level Agreement): 내부 팀 간 합의</div>
<div class="kb-diagram-note">"서비스 데스크 ↔ 네트워크팀 ↔ DB팀"</div>
<div class="kb-diagram-note">UC (Underpinning Contract): IT 제공자 ↔ 외부 공급자</div>
<div class="kb-diagram-note">"외부 클라우드, 통신사, 소프트웨어 벤더와의 계약"</div>
<div class="kb-diagram-note">SLA 체인 원칙:</div>
<div class="kb-diagram-note">SLA 약속 ≤ OLA 합의 ≤ UC 계약</div>
<div class="kb-diagram-note">예:</div>
<div class="kb-diagram-note">SLA: 인시던트 P1 복구 4시간 이내</div>
<div class="kb-diagram-note">OLA: 서버팀이 네트워크팀에 알림 후 30분 내 처리</div>
<div class="kb-diagram-note">UC: 클라우드 제공자 가용성 99.95% 보장</div>
<div class="kb-diagram-note">OLA 위반 → SLA 위반 가능성 높음</div>
<div class="kb-diagram-note">UC 위반 → SLA 위반 가능성 높음</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [SLM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/313_slm/) 3계층 = 레스토랑 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체계 — 손님(고객)에게 "30분 내 음식 제공([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/))" 약속. 주방팀 내 "15분 내 조리([OLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/))" 합의. 식재료 공급사와 "당일 납품([UC](/knowledge-base/studynote/12_it_management/02_itsm_itil/087_underpinning_contract/))" 계약. 모든 계층 지켜야 손님 약속 이행!

---

## Ⅱ. [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 설계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SLA (Service Level Agreement) 구성요소:</div>
<div class="kb-diagram-note">1. 서비스 범위:</div>
<div class="kb-diagram-note">어떤 서비스, 어떤 업무 시간</div>
<div class="kb-diagram-note">"이메일 서비스, 24×7 x 365"</div>
<div class="kb-diagram-note">2. 서비스 수준 목표:</div>
<div class="kb-diagram-note">가용성 (Availability): 99.9%</div>
<div class="kb-diagram-note">응답 시간 (Response Time): &lt; 200ms (P95)</div>
<div class="kb-diagram-note">인시던트 해결 시간 (Resolution Time): P1 4시간</div>
<div class="kb-diagram-note">3. 측정 방법:</div>
<div class="kb-diagram-note">측정 도구: Datadog, Prometheus</div>
<div class="kb-diagram-note">측정 주기: 5분 간격 헬스체크</div>
<div class="kb-diagram-note">보고 주기: 월별 SLM 보고서</div>
<div class="kb-diagram-note">4. 책임 한계:</div>
<div class="kb-diagram-note">고객 귀책 제외: 고객 측 네트워크 장애</div>
<div class="kb-diagram-note">계획된 다운타임 제외: 사전 공지 유지보수</div>
<div class="kb-diagram-note">5. 위반 시 조치:</div>
<div class="kb-diagram-note">SLA Credit:</div>
<div class="kb-diagram-note">가용성 99.9% 미달 시 → 요금 10% 크레딧</div>
<div class="kb-diagram-note">99% 미달 시 → 25% 크레딧</div>
<div class="kb-diagram-note">95% 미달 시 → 50% 크레딧</div>
<div class="kb-diagram-note">6. 검토 주기:</div>
<div class="kb-diagram-note">분기별 SLM 검토 미팅</div>
<div class="kb-diagram-note">서비스 변경 시 SLA 재협의</div>
<div class="kb-diagram-note">SLA 작성 원칙:</div>
<div class="kb-diagram-note">측정 가능: "빠른 응답" X → "P99 &lt; 500ms" O</div>
<div class="kb-diagram-note">현실적: 현재 성능 기반 + 개선 여유</div>
<div class="kb-diagram-note">균형: 고객 기대 + 제공 가능한 수준</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) = 식당 메뉴판 약속 — "30분 내 배달 보장([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)+응답시간)". 늦으면 다음 주문 할인([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) Credit). 측정 가능하고 현실적인 약속이 진짜 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)!

---

## Ⅲ. [OLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/) 설계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">OLA (Operational Level Agreement):</div>
<div class="kb-diagram-note">IT 내부 팀 간 서비스 수준 합의</div>
<div class="kb-diagram-note">SLA 이행을 위한 내부 메커니즘</div>
<div class="kb-diagram-note">예시: P1 인시던트 대응 OLA:</div>
<div class="kb-diagram-note">서비스 데스크:</div>
<div class="kb-diagram-note">P1 탐지 → 5분 내 분류(Triage)</div>
<div class="kb-diagram-note">15분 내 에스컬레이션 결정</div>
<div class="kb-diagram-note">고객 최초 알림: 30분 내</div>
<div class="kb-diagram-note">인프라팀:</div>
<div class="kb-diagram-note">서비스 데스크 에스컬레이션 → 15분 내 대응</div>
<div class="kb-diagram-note">초기 진단: 30분 내</div>
<div class="kb-diagram-note">임시 조치(Workaround): 2시간 내</div>
<div class="kb-diagram-note">애플리케이션팀:</div>
<div class="kb-diagram-note">코드 관련 장애 에스컬레이션 → 30분 내 대응</div>
<div class="kb-diagram-note">핫픽스 릴리스: 4시간 내</div>
<div class="kb-diagram-note">SLA 연결:</div>
<div class="kb-diagram-note">P1 SLA: 4시간 내 복구</div>
<div class="kb-diagram-note">OLA 합: 5+15+30 = 50분 (서비스 데스크) + 2시간(인프라) &lt; 4시간 ✓</div>
<div class="kb-diagram-note">OLA 측정:</div>
<div class="kb-diagram-note">ITSM 도구 (ServiceNow, Jira Service Desk)</div>
<div class="kb-diagram-note">인시던트 각 단계 타임스탬프 자동 기록</div>
<div class="kb-diagram-note">주간 OLA 위반 리포트:</div>
<div class="kb-diagram-note">어떤 팀이 어떤 단계에서 OLA 초과?</div>
<div class="kb-diagram-note">OLA 거버넌스:</div>
<div class="kb-diagram-note">분기별 팀 리뷰</div>
<div class="kb-diagram-note">반복 위반 팀 → 근본 원인 분석 + 개선 계획</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [OLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/) = 식당 내부 배달 타임라인 — 주방(인프라): 15분, 포장(앱팀): 10분, 배달([서비스 데스크](/knowledge-base/studynote/12_it_management/02_itsm_itil/072_service_desk/)): 5분 합계 30분. 외부 약속([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)) 지키려면 내부 타임라인([OLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/)) 먼저 정확히!

---

## Ⅳ. [SLM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/313_slm/) 성숙도와 자동화



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SLM 성숙도 모델:</div>
<div class="kb-diagram-note">레벨 1 - 임시 (Ad-hoc):</div>
<div class="kb-diagram-note">SLA 문서 있지만 측정 없음</div>
<div class="kb-diagram-note">위반 시 인지 불가</div>
<div class="kb-diagram-note">레벨 2 - 반응적 (Reactive):</div>
<div class="kb-diagram-note">SLA 측정 도구 있음</div>
<div class="kb-diagram-note">위반 발생 후 인지</div>
<div class="kb-diagram-note">월별 보고서</div>
<div class="kb-diagram-note">레벨 3 - 사전 예방적 (Proactive):</div>
<div class="kb-diagram-note">실시간 SLA 대시보드</div>
<div class="kb-diagram-note">위반 임박 시 경보</div>
<div class="kb-diagram-note">Burn Rate 모니터링</div>
<div class="kb-diagram-note">레벨 4 - 최적화 (Optimized):</div>
<div class="kb-diagram-note">AI 기반 SLA 예측</div>
<div class="kb-diagram-note">자동 스케일링으로 SLA 유지</div>
<div class="kb-diagram-note">SLA 자동 보고</div>
<div class="kb-diagram-note">현대 SLM 자동화:</div>
<div class="kb-diagram-note">ServiceNow SLM:</div>
<div class="kb-diagram-note">인시던트 자동 SLA 타이머 시작</div>
<div class="kb-diagram-note">OLA 단계별 자동 에스컬레이션</div>
<div class="kb-diagram-note">SLA 위반 자동 크레딧 계산</div>
<div class="kb-diagram-note">Prometheus + SLO:</div>
<div class="kb-diagram-note">SLI(Error Rate, Latency) 자동 수집</div>
<div class="kb-diagram-note">SLO 위반 → PagerDuty 자동 알림</div>
<div class="kb-diagram-note">Error Budget 실시간 계산</div>
<div class="kb-diagram-note">Datadog SLO Tracking:</div>
<div class="kb-diagram-note">서비스 수준 목표 정의 → 자동 모니터링</div>
<div class="kb-diagram-note">SLA 리포트 자동 생성 → 고객 공유</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [SLM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/313_slm/) 성숙도 = 배달 추적 시스템 발전 — 레벨 1(배달 완료만 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)), 레벨 2(배달 완료 후 늦음 인지), 레벨 3(실시간 GPS 추적 + 30분 초과 경보), 레벨 4([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 예측으로 최적 경로 자동 선택)!

---

## Ⅴ. 실무 시나리오 — [SLM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/313_slm/) 체계 구축



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">제조업 IT 부서 SLM 체계 구축:</div>
<div class="kb-diagram-note">현황:</div>
<div class="kb-diagram-note">IT 서비스 200개 운영</div>
<div class="kb-diagram-note">SLA: 계약서에만 존재 (측정 없음)</div>
<div class="kb-diagram-note">월 평균 SLA 위반 클레임: 10건</div>
<div class="kb-diagram-note">근거 없는 클레임 분쟁 잦음</div>
<div class="kb-diagram-note">목표:</div>
<div class="kb-diagram-note">측정 기반 SLM 체계 구축</div>
<div class="kb-diagram-note">SLA 위반 인시던트 50% 감소</div>
<div class="kb-diagram-note">1단계: 서비스 카탈로그 정의</div>
<div class="kb-diagram-note">200개 서비스를 5개 등급으로 분류:</div>
<div class="kb-diagram-note">P1 (Critical): ERP, 생산 시스템 (24×7)</div>
<div class="kb-diagram-note">P2 (High): 그룹웨어, 이메일 (업무 시간)</div>
<div class="kb-diagram-note">P3 (Medium): HR 시스템</div>
<div class="kb-diagram-note">P4 (Low): 사내 포털, 교육 시스템</div>
<div class="kb-diagram-note">P5 (Minimal): 개발 서버</div>
<div class="kb-diagram-note">2단계: SLA/OLA 문서화</div>
<div class="kb-diagram-note">P1 SLA: 가용성 99.9%, 복구 4시간</div>
<div class="kb-diagram-note">관련 OLA: 네트워크팀/서버팀/DB팀 각 1시간</div>
<div class="kb-diagram-note">3단계: 측정 도구 구축</div>
<div class="kb-diagram-note">ServiceNow: 인시던트 SLA 자동 타이머</div>
<div class="kb-diagram-note">Zabbix + Grafana: 인프라 가용성 자동 측정</div>
<div class="kb-diagram-note">SLA 대시보드: 실시간 가용성 + OLA 위반</div>
<div class="kb-diagram-note">4단계: 월별 SLM 검토</div>
<div class="kb-diagram-note">SLA 달성률: 서비스별</div>
<div class="kb-diagram-note">OLA 위반: 팀별</div>
<div class="kb-diagram-note">반복 위반 → 근본 원인 분석</div>
<div class="kb-diagram-note">결과 (6개월):</div>
<div class="kb-diagram-note">SLA 측정 자동화: 100% 서비스 커버리지</div>
<div class="kb-diagram-note">SLA 위반: 10건/월 → 3건/월</div>
<div class="kb-diagram-note">OLA 위반 식별: "DB팀이 병목" 발견 → DB 전담 인력 증원</div>
<div class="kb-diagram-note">클레임 분쟁: 데이터 기반 해결 (클레임 80% 감소)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [SLM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/313_slm/) 체계 구축 = GPS 배달 추적 도입 — "언제 도착하냐"는 분쟁에서 GPS 기록([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 측정 도구)으로 해결. 병목(DB팀) 발견해 인력 증원. [클레임](/knowledge-base/studynote/09_security/11_iam_access_control/539_claims/) 분쟁 80% 감소!

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SLM (Service Level Management)</div>
<div class="kb-diagram-note">+-- 계층</div>
<div class="kb-diagram-note">+-- SLA (고객 대면)</div>
<div class="kb-diagram-note">+-- OLA (내부 팀 간)</div>
<div class="kb-diagram-note">+-- UC (외부 공급자)</div>
<div class="kb-diagram-note">+-- ITIL v4 관련</div>
<div class="kb-diagram-note">+-- 인시던트 관리</div>
<div class="kb-diagram-note">+-- 문제 관리</div>
<div class="kb-diagram-note">+-- 변경 관리</div>
<div class="kb-diagram-note">+-- 측정 도구</div>
<div class="kb-diagram-note">+-- ServiceNow, Jira SM</div>
<div class="kb-diagram-note">+-- Prometheus + Grafana</div>
<div class="kb-diagram-note">+-- 성숙도</div>
<div class="kb-diagram-note">+-- 임시 → 반응적 → 예방적 → 최적화</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도

```
[ITIL v1 (1989)]
영국 정부 IT 관리 표준
SLA 개념 도입
      |
      v
[ITIL v2/v3 (2000~2007)]
SLM 프로세스 체계화
OLA, UC 개념 정립
      |
      v
[클라우드 SLA (2010s~)]
AWS/Azure SLA 표준화
SLO(Site Reliability) 등장
      |
      v
[ITIL v4 (2019)]
가치 스트림 중심
DevOps + SRE 통합
      |
      v
[현재: AI 기반 SLM]
예측 기반 SLA 관리
자동 스케일링으로 SLA 유지
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) = 식당 약속 — 손님에게 "30분 내 음식 제공". 위반 시 할인권([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) Credit). 측정 가능해야 진짜 약속!
2. [OLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/) = 주방 팀 내부 타임라인 — 주방장에서 홀 서빙까지 각 단계 시간 합산이 손님 약속 시간보다 짧아야 해요!
3. [SLM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/313_slm/) 성숙도 = 배달 추적 진화 — 완료만 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)(레벨1)에서 실시간 GPS+[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 경로 최적화(레벨4)까지. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 없이는 관리 불가!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 48 / 482

← **이전**: [047. SLA 심화 — 계약 구조와 거버넌스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/047_sla_service_level_agreement/)
**다음**: [049. 서비스 카탈로그 — Service Catalog](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/049_service_catalog/) →

---
