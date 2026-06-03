+++
title = "047. SLA 심화 — 계약 구조와 거버넌스"
date = 2026-04-05

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

> **핵심 인사이트**
> 1. [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)([Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/))는 기술 지표가 아닌 비즈니스 계약 — [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공자와 고객 간 상호 의무와 기대를 법적으로 구속하는 문서이며, "무엇을 보장하고 위반 시 어떻게 보상하는가"가 핵심이다.
> 2. [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 협상에서 흔히 놓치는 세 가지 — ① 측정 방법(누가 어떻게 측정?), ② 예외 사항(scheduled maintenance, force majeure), ③ 에스컬레이션 절차. 이 세 가지가 분쟁의 씨앗이 된다.
> 3. [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 위반보다 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 초과(Over-delivery)도 위험 — [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 99.9%를 지속적으로 99.99%로 제공하면 고객이 실제 SLA를 99.99%로 기대하게 되어, 단 한 번의 99.95% 시 불만이 발생한다. 의도적 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 관리가 필요하다.

---

## Ⅰ. [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 계약 구조

```
SLA 문서 구조:

1. 서비스 범위 정의:
  포함된 서비스: 명확히 열거
  제외된 서비스: 명확히 열거 (중요!)
  
  예: 클라우드 SaaS SLA
  포함: 웹 서비스 가용성, API 응답
  제외: 인터넷 연결 문제, 사용자 오류

2. 가용성 정의:
  측정 단위: 월간 또는 연간
  계산 방법:
  (합의 서비스 시간 - 다운타임) / 합의 서비스 시간
  
  합의 서비스 시간:
  24×7 (항상) 또는 영업 시간(08~18시)
  
  다운타임 카운팅 기준:
  "서비스 응답 불가 또는 5초 이상 지연"

3. 측정 방법:
  합성 모니터링 (Synthetic Monitoring):
  30초 간격 외부 프로브
  누가 측정?: 제3자 또는 제공자
  
  제공자 측정 vs 독립 측정:
  제공자가 자체 측정 → 이해 충돌 가능
  권고: 제3자 모니터링 또는 합의된 방법

4. 페널티 구조:
  위반 심각도별 크레딧:
  99.0~99.9%: 10%
  95.0~99.0%: 25%
  95.0% 미만: 50%
  
  최대 크레딧 한도: 월 청구 금액의 100%
  
5. 지원 SLA:
  P1 (심각): 30분 내 초기 응답, 4시간 내 해결
  P2 (높음): 2시간 내 초기 응답
  P3 (보통): 다음 영업일 내
```

> 📢 **섹션 요약 비유**: [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 문서는 집 임대 계약서 — 집 상태([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 범위), 하자 보수 기간([응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)), 집주인 책임 범위(제외 사항), 위반 시 임대료 공제(페널티). 모든 조건을 미리 명시!

---

## Ⅱ. [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 협상 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SLA 협상 핵심 포인트:</div>
<div class="kb-diagram-note">공급업체 관점:</div>
<div class="kb-diagram-note">1. 합리적 목표 설정:</div>
<div class="kb-diagram-note">역사 데이터 기반: 과거 6개월 가용성</div>
<div class="kb-diagram-note">예: 실제 99.97% → SLA 99.9% 제안</div>
<div class="kb-diagram-note">(여유 0.07% = 완충 지대)</div>
<div class="kb-diagram-note">2. 예외 사항 명확화:</div>
<div class="kb-diagram-note">Scheduled Maintenance:</div>
<div class="kb-diagram-note">"매주 일요일 02:00-04:00 정기 점검" 제외</div>
<div class="kb-diagram-note">사전 72시간 공지 조건</div>
<div class="kb-diagram-note">Force Majeure:</div>
<div class="kb-diagram-note">자연재해, 법적 규제, 사이버 공격</div>
<div class="kb-diagram-note">제공자 통제 불가 상황</div>
<div class="kb-diagram-note">고객 귀책 사유:</div>
<div class="kb-diagram-note">API 오용, 제한 초과, 설정 오류</div>
<div class="kb-diagram-note">3. 측정 방법 합의:</div>
<div class="kb-diagram-note">제공자 모니터링 시스템 사용</div>
<div class="kb-diagram-note">고객이 독립 검증 원하면: 제3자 도구 합의</div>
<div class="kb-diagram-note">4. 크레딧 한도:</div>
<div class="kb-diagram-note">과도한 페널티 = 사업 불가</div>
<div class="kb-diagram-note">최대 크레딧: 월 청구액의 30~100%</div>
<div class="kb-diagram-note">현금 환불 대신 서비스 크레딧 선호</div>
<div class="kb-diagram-note">고객 관점:</div>
<div class="kb-diagram-note">1. 측정 방법 검토:</div>
<div class="kb-diagram-note">누가 측정? → 독립성 요구</div>
<div class="kb-diagram-note">"제공자가 자체 측정"이면 제3자 추가</div>
<div class="kb-diagram-note">2. SLA 적용 범위:</div>
<div class="kb-diagram-note">전체 서비스 vs 핵심 기능 SLA 구분</div>
<div class="kb-diagram-note">핵심 기능 더 엄격한 SLA 요구</div>
<div class="kb-diagram-note">3. 에스컬레이션 절차:</div>
<div class="kb-diagram-note">누구에게 보고? 언제?</div>
<div class="kb-diagram-note">이슈 미해결 시 다음 단계?</div>
<div class="kb-diagram-note">4. 종료 권리 (Termination Right):</div>
<div class="kb-diagram-note">연속 N회 SLA 위반 시 계약 해지 권리</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 협상은 임대 계약 협상 — 집주인(공급업체)은 여유 있게 약속(실제 99.97% → [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 99.9%), 세입자(고객)는 독립 검사(제3자 측정)와 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 조항(종료권) 요구!

---

## Ⅲ. [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 거버넌스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SLA 거버넌스 체계:</div>
<div class="kb-diagram-note">정기 리뷰 사이클:</div>
<div class="kb-diagram-note">월간 운영 리뷰 (MOR):</div>
<div class="kb-diagram-note">SLA 실적 보고</div>
<div class="kb-diagram-note">인시던트 요약</div>
<div class="kb-diagram-note">개선 계획</div>
<div class="kb-diagram-note">분기 서비스 리뷰 (QBR):</div>
<div class="kb-diagram-note">트렌드 분석</div>
<div class="kb-diagram-note">비즈니스 요구사항 변화</div>
<div class="kb-diagram-note">SLA 수정 논의</div>
<div class="kb-diagram-note">연간 계약 리뷰:</div>
<div class="kb-diagram-note">SLA 재협상</div>
<div class="kb-diagram-note">서비스 로드맵 공유</div>
<div class="kb-diagram-note">다음 해 목표 설정</div>
<div class="kb-diagram-note">SLA 리포트 구성:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">월간 서비스 리포트</div></div>
<div class="kb-diagram-note">기간: 2024년 3월</div>
<div class="kb-diagram-note">가용성:</div>
<div class="kb-diagram-note">합의 SLA: 99.9%</div>
<div class="kb-diagram-note">실제 가용성: 99.97%</div>
<div class="kb-diagram-note">다운타임: 8.6분 (목표 43.2분 대비 양호)</div>
<div class="kb-diagram-note">응답 시간:</div>
<div class="kb-diagram-note">P50: 180ms (목표 300ms ↓)</div>
<div class="kb-diagram-note">P95: 450ms (목표 500ms ↓)</div>
<div class="kb-diagram-note">P99: 1,200ms (목표 1,000ms ↑ ← 주의!)</div>
<div class="kb-diagram-note">인시던트:</div>
<div class="kb-diagram-note">P1: 0건</div>
<div class="kb-diagram-note">P2: 2건 (MTTR: 1.8시간, SLA: 4시간)</div>
<div class="kb-diagram-note">SLA 크레딧: 0원 (모든 지표 SLA 준수)</div>
<div class="kb-diagram-note">개선 과제:</div>
<div class="kb-diagram-note">P99 응답시간 초과 → DB 쿼리 최적화 계획</div>
<div class="kb-diagram-note">에스컬레이션 매트릭스:</div>
<div class="kb-diagram-note">L1: 담당자 자체 해결 (4시간)</div>
<div class="kb-diagram-note">L2: 팀 리더 참여 (다음 날)</div>
<div class="kb-diagram-note">L3: 관리자 / 임원 (SLA 위반 시)</div>
<div class="kb-diagram-note">L4: 경영진 회의 (반복 위반 시)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 거버넌스는 성적표+학부모 회의 — 매달 성적표(월간 리포트), 분기마다 학부모 상담(QBR), 연도말 진학 계획(연간 리뷰). 성적 나쁘면 보충수업(개선 계획)!

---

## Ⅳ. [멀티 클라우드](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 관리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">멀티 클라우드 SLA 복잡성:</div>
<div class="kb-diagram-note">단일 클라우드:</div>
<div class="kb-diagram-note">SLA: 한 공급업체 = 단순</div>
<div class="kb-diagram-note">멀티 클라우드:</div>
<div class="kb-diagram-note">AWS + Azure + GCP 동시 사용</div>
<div class="kb-diagram-note">서비스 A: AWS (SLA 99.99%)</div>
<div class="kb-diagram-note">서비스 B: Azure (SLA 99.95%)</div>
<div class="kb-diagram-note">DB: GCP Cloud SQL (SLA 99.95%)</div>
<div class="kb-diagram-note">End-to-End 가용성:</div>
<div class="kb-diagram-note">0.9999 × 0.9995 × 0.9995 ≈ 99.89%</div>
<div class="kb-diagram-note">→ 각 구성 요소 SLA 곱 = 낮아짐!</div>
<div class="kb-diagram-note">SLA 연쇄 (Cascaded SLA):</div>
<div class="kb-diagram-note">사용자 → 앱 → DB</div>
<div class="kb-diagram-note">전체 SLA = 앱 SLA × DB SLA</div>
<div class="kb-diagram-note">앱 SLA 99.9%, DB SLA 99.9%:</div>
<div class="kb-diagram-note">전체: 0.999 × 0.999 = 99.8%</div>
<div class="kb-diagram-note">(각각 SLA보다 낮음!)</div>
<div class="kb-diagram-note">멀티 클라우드 SLA 전략:</div>
<div class="kb-diagram-note">1. 의존성 최소화:</div>
<div class="kb-diagram-note">핵심 경로의 의존성 컴포넌트 수 최소화</div>
<div class="kb-diagram-note">2. 비동기 처리:</div>
<div class="kb-diagram-note">동기 호출 대신 큐 기반 비동기</div>
<div class="kb-diagram-note">→ 한 서비스 다운 시 영향 격리</div>
<div class="kb-diagram-note">3. 서킷 브레이커:</div>
<div class="kb-diagram-note">의존 서비스 장애 시 빠른 실패 + 폴백</div>
<div class="kb-diagram-note">4. 다중화 (Redundancy):</div>
<div class="kb-diagram-note">AWS + Azure 이중화 → 전체 가용성 향상</div>
<div class="kb-diagram-note">0.9999 × (1 - (1-0.9995)²) ≈ 99.9975%</div>
<div class="kb-diagram-note">SLA 관리 도구:</div>
<div class="kb-diagram-note">CloudHealth: 멀티 클라우드 비용+SLA</div>
<div class="kb-diagram-note">Datadog: 통합 모니터링</div>
<div class="kb-diagram-note">Statuspage.io: 상태 페이지 (고객 공개)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [멀티 클라우드](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) SLA는 체인 약점 — 99.9%짜리 링크 3개 연결 = 99.7%. 체인은 가장 약한 고리! 의존성 최소화와 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)로 체인 강화!

---

## Ⅴ. 실무 시나리오 — 핀테크 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 재협상



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">핀테크 스타트업 클라우드 SLA 재협상:</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">AWS 기반 결제 서비스</div>
<div class="kb-diagram-note">현재 SLA: 99.9% (월 43분 다운타임 허용)</div>
<div class="kb-diagram-note">문제:</div>
<div class="kb-diagram-note">실제 발생한 장애 (지난 분기):</div>
<div class="kb-diagram-tree-item" style="--depth:1">DB 장애: 2시간 (SLA 위반!)</div>
<div class="kb-diagram-tree-item" style="--depth:1">네트워크 이슈: 15분</div>
<div class="kb-diagram-note">SLA 크레딧 청구: 없음 (고객이 모름)</div>
<div class="kb-diagram-note">고객 불만: 3건 (결제 실패 경험)</div>
<div class="kb-diagram-note">재협상 목표:</div>
<div class="kb-diagram-note">1. SLA 강화:</div>
<div class="kb-diagram-note">가용성: 99.9% → 99.95%</div>
<div class="kb-diagram-note">MTTR: 미명시 → P1 4시간 보장</div>
<div class="kb-diagram-note">2. 측정 독립성:</div>
<div class="kb-diagram-note">AWS CloudWatch 외 Pingdom 추가</div>
<div class="kb-diagram-note">→ 독립적 외부 측정</div>
<div class="kb-diagram-note">3. 페널티 강화:</div>
<div class="kb-diagram-note">99.9~99.95%: 10% 크레딧 (기존 없음)</div>
<div class="kb-diagram-note">99.0~99.9%: 25% 크레딧</div>
<div class="kb-diagram-note">99.0% 미만: 100% 크레딧</div>
<div class="kb-diagram-note">4. 자동 크레딧:</div>
<div class="kb-diagram-note">조건 충족 시 자동 크레딧 (청구 불필요)</div>
<div class="kb-diagram-note">→ 고객 신뢰 향상</div>
<div class="kb-diagram-note">AWS와 협상 결과:</div>
<div class="kb-diagram-note">99.95% SLA → 기존 Premium Support 계약 조건</div>
<div class="kb-diagram-note">자동 크레딧: 일부 서비스만 적용</div>
<div class="kb-diagram-note">보완:</div>
<div class="kb-diagram-note">내부 SLO: 99.99% (SLA 여유분 확보)</div>
<div class="kb-diagram-note">중복화: Multi-AZ RDS + ALB</div>
<div class="kb-diagram-note">DR: 타 리전 수동 페일오버 절차</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">이후 4개월: SLA 위반 0건</div>
<div class="kb-diagram-note">고객 불만: 0건</div>
<div class="kb-diagram-note">결제 성공률: 99.82% → 99.97%</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 핀테크 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 재협상은 보험 업그레이드 — 기본 보험(99.9%)에서 업그레이드(99.95%). 독립 측정(제3자) + 자동 보상 추가. 장애 없어지자 고객 불만도 0!

---

## 📌 관련 개념 맵

```
SLA 거버넌스
+-- 문서 구조
|   +-- 서비스 범위, 가용성, 측정 방법
|   +-- 페널티, 예외 사항
+-- 협상 전략
|   +-- 공급업체: 완충 지대, 예외 명확화
|   +-- 고객: 독립 측정, 종료 권리
+-- 거버넌스
|   +-- 월간/분기/연간 리뷰
|   +-- 에스컬레이션 매트릭스
+-- 멀티 클라우드
    +-- SLA 연쇄 (가용성 곱)
    +-- 이중화 전략
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 IT 아웃소싱 (1990s)]
주관적 서비스 약속
SLA 미정착
      |
      v
[ITIL + SLA 표준화 (2000s)]
서비스 수명주기 관리
SLA 계약 형식화
      |
      v
[클라우드 SLA 공개 (2006~)]
AWS, Azure, GCP SLA 공표
크레딧 구조 표준화
      |
      v
[SLA 자동화 (2015~)]
Statuspage.io
자동 크레딧, 모니터링 통합
      |
      v
[현재: 비즈니스 임팩트 SLA]
가용성 → 수익 연결
AI 기반 SLA 예측 관리
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. SLA는 약속 증서 — "이만큼 잘 해드릴게요!" 서면 계약. 못 지키면 돈(크레딧) 드려요. 집 계약서처럼 모든 조건을 명시!
2. [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 협상은 균형 찾기 — 공급업체는 달성 가능한 약속, 고객은 강한 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 요구. 양쪽이 Win-Win하는 균형점 찾기!
3. [멀티 클라우드](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 함정 — 99.9%짜리 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 3개 연결하면 전체 99.7%로 떨어져요. 체인은 가장 약한 고리가 결정!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 47 / 482

← **이전**: [046. IT 서비스 관리 — ITSM 심화](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/046_itsm_it_service_management/)
**다음**: [048. SLM·OLA·UC — 서비스 수준 관리 체계](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/048_slm_ola_uc/) →

---
