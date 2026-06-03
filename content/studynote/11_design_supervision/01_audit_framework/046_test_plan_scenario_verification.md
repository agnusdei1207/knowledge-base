+++
title = "046. 테스트 계획서·시나리오·확인 — Test Plan, Scenario, Verification"
date = 2026-04-05

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

> **핵심 인사이트**
> 1. 테스트 계획서(Test Plan)는 무엇을, 어떻게, 언제, 누가 테스트할지를 정의한 테스트의 "헌법" — IEEE 829 표준이 테스트 계획서 구조를 정의하며, 잘 작성된 계획서는 QA팀과 개발팀 간 기대 불일치를 예방한다.
> 2. [테스트 시나리오](/knowledge-base/studynote/04_software_engineering/11_testing_validation/442_test_scenario/)([Test Scenario](/knowledge-base/studynote/04_software_engineering/11_testing_validation/442_test_scenario/))는 사용자 관점의 실제 동작 흐름을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) — 단순 기능 테스트(버튼 클릭)를 넘어 [end-to-end](/knowledge-base/studynote/03_network/08_transport_layer/401_transport_layer_role_end_to_end_multiplexing/) 비즈니스 흐름(회원가입→로그인→결제→환불)을 시뮬레이션하며, 높은 커버리지와 실질적 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 탐지를 동시에 달성한다.
> 3. [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)([Verification](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)) vs [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)([Validation](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))의 구분 — Verification은 "올바르게 만들었는가(스펙 준수)", Validation은 "올바른 것을 만들었는가(사용자 요구 충족)". 두 활동 모두 필수이며, V&V([Verification](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) & [Validation](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))는 소프트웨어 품질의 양대 축이다.

---

## Ⅰ. 테스트 계획서

```
테스트 계획서 (Test Plan):

목적: 테스트 전 활동 전체를 정의하는 문서

IEEE 829 구조:

1. 테스트 계획 식별자
2. 소개 (테스트 범위)
3. 테스트 항목 (무엇을 테스트)
4. 테스트할 기능
5. 테스트하지 않을 기능 + 이유
6. 테스트 접근 방법 (단위/통합/시스템/인수)
7. 합격 판정 기준 (Pass/Fail 기준)
8. 일시 중단 기준 (테스트 중단 조건)
9. 테스트 결과물 (산출물 목록)
10. 테스트 활동 일정
11. 테스트 환경 (하드웨어/소프트웨어/데이터)
12. 책임 사항 (역할·담당자)
13. 위험 및 우발 계획
14. 승인

테스트 레벨 계획:

단위 테스트 (Unit Test):
  범위: 함수/메서드 단위
  담당: 개발자
  도구: JUnit, pytest
  목표: 코드 커버리지 80%+

통합 테스트 (Integration Test):
  범위: 모듈 간 인터페이스
  담당: QA + 개발자
  방법: 빅뱅, 점증적

시스템 테스트 (System Test):
  범위: 전체 시스템
  담당: QA팀
  환경: 스테이징 환경

인수 테스트 (Acceptance Test):
  범위: 비즈니스 요구사항
  담당: 고객/사용자
  방법: UAT (User Acceptance Test)
```

> 📢 **섹션 요약 비유**: 테스트 계획서는 공사 설계도 — 어떤 방(기능)을 어떤 순서로, 어떤 방법으로 검사할지 미리 정의. 없으면 테스트가 중구난방!

---

## Ⅱ. [테스트 시나리오](/knowledge-base/studynote/04_software_engineering/11_testing_validation/442_test_scenario/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">테스트 시나리오 (Test Scenario):</div>
<div class="kb-diagram-note">정의: 테스트할 단일 기능 또는 비즈니스 흐름</div>
<div class="kb-diagram-note">vs 테스트 케이스:</div>
<div class="kb-diagram-note">시나리오: 무엇을 테스트 (상위 수준)</div>
<div class="kb-diagram-note">케이스: 어떻게 테스트 (구체적 단계, 데이터)</div>
<div class="kb-diagram-note">예: 온라인 쇼핑몰</div>
<div class="kb-diagram-note">시나리오 1: 정상 구매 흐름</div>
<div class="kb-diagram-note">케이스 1.1: 상품 검색 후 장바구니 추가</div>
<div class="kb-diagram-note">케이스 1.2: 장바구니에서 결제 진행</div>
<div class="kb-diagram-note">케이스 1.3: 신용카드 결제 성공</div>
<div class="kb-diagram-note">케이스 1.4: 주문 확인 이메일 수신</div>
<div class="kb-diagram-note">시나리오 2: 재고 부족 상황</div>
<div class="kb-diagram-note">케이스 2.1: 재고 0 상품 구매 시도</div>
<div class="kb-diagram-note">케이스 2.2: 품절 안내 메시지 확인</div>
<div class="kb-diagram-note">시나리오 작성 기법:</div>
<div class="kb-diagram-note">유스케이스 기반:</div>
<div class="kb-diagram-note">기능 명세의 유스케이스 → 시나리오 도출</div>
<div class="kb-diagram-note">경계값 분석:</div>
<div class="kb-diagram-note">입력 경계 (최솟값, 최댓값, 경계+1)</div>
<div class="kb-diagram-note">동등 분할:</div>
<div class="kb-diagram-note">유사 입력 그룹 → 대표값 선택</div>
<div class="kb-diagram-note">탐색적 테스팅:</div>
<div class="kb-diagram-note">테스터가 직관+경험으로 자유롭게 탐색</div>
<div class="kb-diagram-note">공식 케이스로 못 잡는 엣지케이스 탐지</div>
<div class="kb-diagram-note">시나리오 우선순위:</div>
<div class="kb-diagram-note">위험 기반 (Risk-Based):</div>
<div class="kb-diagram-note">빈도×영향도 → 높은 위험 시나리오 우선</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [테스트 시나리오](/knowledge-base/studynote/04_software_engineering/11_testing_validation/442_test_scenario/)는 영화 시나리오 — 영화(시스템)에서 주인공(사용자)이 경험하는 장면(비즈니스 흐름)을 순서대로 기술. 시나리오마다 여러 테이크(케이스)!

---

## Ⅲ. [Verification](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) & [Validation](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">V&amp;V (Verification &amp; Validation):</div>
<div class="kb-diagram-note">Verification (검증, 확인):</div>
<div class="kb-diagram-note">"올바르게 만들었는가?"</div>
<div class="kb-diagram-note">스펙·설계 문서와의 일치 확인</div>
<div class="kb-diagram-note">질문: "시스템이 요구사항 명세를 따르는가?"</div>
<div class="kb-diagram-note">활동:</div>
<div class="kb-diagram-tree-item" style="--depth:1">코드 리뷰 (설계 스펙 준수 확인)</div>
<div class="kb-diagram-tree-item" style="--depth:1">단위/통합 테스트</div>
<div class="kb-diagram-tree-item" style="--depth:1">정적 분석 (SAST)</div>
<div class="kb-diagram-tree-item" style="--depth:1">인스펙션, 워크스루</div>
<div class="kb-diagram-note">예: 결제 모듈이 API 명세서대로 구현됐나?</div>
<div class="kb-diagram-note">Validation (타당성 확인):</div>
<div class="kb-diagram-note">"올바른 것을 만들었는가?"</div>
<div class="kb-diagram-note">실제 사용자 요구사항 충족 확인</div>
<div class="kb-diagram-note">질문: "시스템이 사용자의 실제 필요를 만족하는가?"</div>
<div class="kb-diagram-note">활동:</div>
<div class="kb-diagram-tree-item" style="--depth:1">인수 테스트 (UAT)</div>
<div class="kb-diagram-tree-item" style="--depth:1">사용자 피드백</div>
<div class="kb-diagram-tree-item" style="--depth:1">베타 테스트</div>
<div class="kb-diagram-tree-item" style="--depth:1">파일럿 운영</div>
<div class="kb-diagram-note">예: 고객이 결제 흐름을 자연스럽게 쓸 수 있나?</div>
<div class="kb-diagram-note">V 모델 (V-Model):</div>
<div class="kb-diagram-note">개발 테스트</div>
<div class="kb-diagram-note">요구분석 → 인수 테스트 (UAT)</div>
<div class="kb-diagram-note">시스템 설계 → 시스템 테스트</div>
<div class="kb-diagram-note">아키텍처 → 통합 테스트</div>
<div class="kb-diagram-note">상세 설계 → 단위 테스트</div>
<div class="kb-diagram-note">구현 →→→→→→→→→→</div>
<div class="kb-diagram-note">좌측 V: 개발(Verification)</div>
<div class="kb-diagram-note">우측 V: 테스트(Validation)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: V&V는 설계도 검사+입주자 검사 — [Verification](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/): 집이 설계도대로 지어졌나(벽 두께, 전기 배선). [Validation](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/): 입주자가 실제로 살기 편한가!

---

## Ⅳ. 테스트 커버리지

```
테스트 커버리지 유형:

코드 커버리지:

1. 구문 커버리지 (Statement Coverage):
   실행된 구문 / 전체 구문
   가장 기본, 가장 약함
   
2. 분기 커버리지 (Branch Coverage):
   실행된 분기 / 전체 분기
   if/else 양쪽 모두 실행
   
3. 조건 커버리지 (Condition Coverage):
   각 조건식의 T/F 모두 실행
   
4. MC/DC (Modified Condition/Decision Coverage):
   항공/의료 소프트웨어 필수
   각 조건이 독립적으로 결과에 영향
   가장 강력, 가장 어려움

요구사항 커버리지:
  요구사항 항목이 모두 테스트되었는가?
  추적 매트릭스 (Traceability Matrix):
  요구사항 ↔ 테스트 케이스 매핑

커버리지 목표:
  일반 웹 앱: 라인 커버리지 70~80%
  금융/보안: 분기 커버리지 90%+
  항공/의료: MC/DC 100%

한계:
  100% 커버리지 = 버그 없음 아님
  테스트된 경로 = 테스트된 시나리오

실무 측정:
  Python: pytest-cov
  Java: JaCoCo
  JS: Istanbul/nyc
  
  CI/CD 파이프라인 통합:
  커버리지 < 목표 → 빌드 실패
```

> 📢 **섹션 요약 비유**: 테스트 커버리지는 건물 검사 점검표 — 점검 항목(구문)을 모두 체크했나, 양쪽 문(분기) 모두 열어봤나, 각 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 독립 동작(MC/DC). 더 꼼꼼할수록 비용↑!

---

## Ⅴ. 실무 시나리오 — 금융 앱 테스트 계획



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">모바일 뱅킹 앱 테스트 계획:</div>
<div class="kb-diagram-note">환경:</div>
<div class="kb-diagram-note">Android 8~14, iOS 15~17</div>
<div class="kb-diagram-note">스테이징 서버 (실제와 동일 구성)</div>
<div class="kb-diagram-note">테스트 데이터 (가상 계좌)</div>
<div class="kb-diagram-note">테스트 레벨별 계획:</div>
<div class="kb-diagram-note">1. 단위 테스트:</div>
<div class="kb-diagram-note">범위: 이자 계산 로직, 암호화 함수</div>
<div class="kb-diagram-note">담당: 개발자</div>
<div class="kb-diagram-note">목표: 라인 커버리지 85%</div>
<div class="kb-diagram-note">도구: JUnit 5 + Mockito</div>
<div class="kb-diagram-note">2. 통합 테스트:</div>
<div class="kb-diagram-note">범위: API 연동 (계좌 조회, 이체)</div>
<div class="kb-diagram-note">담당: QA</div>
<div class="kb-diagram-note">방법: API 레벨 테스트 (Postman)</div>
<div class="kb-diagram-note">시나리오:</div>
<div class="kb-diagram-tree-item" style="--depth:1">정상 이체 (잔액 충분)</div>
<div class="kb-diagram-tree-item" style="--depth:1">이체 실패 (잔액 부족)</div>
<div class="kb-diagram-tree-item" style="--depth:1">네트워크 단절 중 이체</div>
<div class="kb-diagram-note">3. 시스템 테스트:</div>
<div class="kb-diagram-note">범위: 전체 앱 기능</div>
<div class="kb-diagram-note">주요 시나리오:</div>
<div class="kb-diagram-tree-item" style="--depth:1">로그인 → 잔액 조회 → 이체 → 거래 내역</div>
<div class="kb-diagram-tree-item" style="--depth:1">생체인증(Face ID/지문) 로그인</div>
<div class="kb-diagram-tree-item" style="--depth:1">5회 비밀번호 실패 → 계정 잠금</div>
<div class="kb-diagram-tree-item" style="--depth:1">대용량 거래 내역 (10,000건) 페이징</div>
<div class="kb-diagram-note">4. 성능 테스트:</div>
<div class="kb-diagram-note">도구: JMeter</div>
<div class="kb-diagram-note">목표: 1,000 동시 사용자, 응답 &lt; 3초</div>
<div class="kb-diagram-note">5. 보안 테스트:</div>
<div class="kb-diagram-note">OWASP Mobile Top 10</div>
<div class="kb-diagram-note">침투 테스트 (외부 전문기업)</div>
<div class="kb-diagram-note">6. 인수 테스트 (UAT):</div>
<div class="kb-diagram-note">실제 은행 직원 + 고객 20명</div>
<div class="kb-diagram-note">2주 베타 테스트</div>
<div class="kb-diagram-note">합격 판정:</div>
<div class="kb-diagram-note">P1 버그: 0개 (차단 결함 없음)</div>
<div class="kb-diagram-note">P2 버그: 5개 이하 (작업 계획 포함)</div>
<div class="kb-diagram-note">성능: P95 &lt; 3초</div>
<div class="kb-diagram-note">커버리지: 85% 이상</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 모바일 뱅킹 테스트 계획은 신차 출시 전 검사 — 엔진([단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/)), 부품 연결([통합 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/)), 실도로 주행([시스템 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/405_system_test/)), 고객 시승(UAT). 단계마다 합격 기준!

---

## 📌 관련 개념 맵

```
테스트 계획·시나리오·V&V
+-- 테스트 계획서
|   +-- IEEE 829 표준
|   +-- 테스트 레벨 (단위~인수)
+-- 테스트 시나리오
|   +-- 유스케이스 기반
|   +-- 경계값 분석
|   +-- 동등 분할
+-- V&V
|   +-- Verification (스펙 준수)
|   +-- Validation (사용자 요구)
+-- 커버리지
    +-- 구문/분기/조건
    +-- MC/DC (항공/의료)
    +-- 요구사항 추적 매트릭스
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[폭포수 테스트 (1970~1980s)]
개발 완료 후 전체 테스트
버그 늦게 발견 = 비용 폭발
      |
      v
[V 모델 (1980s~)]
개발 단계 ↔ 테스트 단계 매핑
      |
      v
[애자일 TDD (2000s)]
테스트 먼저, 코드 나중
켄트 벡: Test-Driven Development
      |
      v
[BDD (2006~)]
비즈니스 시나리오 기반 (Gherkin)
Given/When/Then
      |
      v
[현재: Shift-Left + AI 테스팅]
CI/CD 파이프라인 통합
AI 기반 테스트 케이스 자동 생성
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 테스트 계획서는 검사 일정표 — "언제, 무엇을, 어떻게 검사할까?" 미리 쓴 표. 없으면 검사가 엉망이 돼요!
2. V&V는 레시피+손님 만족 — 레시피(설계서)대로 만들었나([Verification](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)) + 손님이 맛있다고 하나([Validation](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)). 둘 다 OK여야 성공!
3. 테스트 커버리지는 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 달성률 — 100개 항목 중 80개 검사(80% 커버리지). 더 많이 검사할수록 더 안전하지만 시간도 더 걸려요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 69 / 530

← **이전**: [46. 테스트 계획·시나리오·결과서 완결성 대조 확인 (Test Plan, Scenario and Result Verification)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/046_test_plan_scenario_result_verification/)
**다음**: [47. 요구사항 추적 매트릭스 양방향 추적성 검증 (RTM Bidirectional Traceability Validation)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/047_rtm_bidirectional_traceability_validation/) →

---
