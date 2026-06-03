+++
title = "047. 요구사항 추적 매트릭스 — RTM 심화"
date = 2026-04-05

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

> **핵심 인사이트**
> 1. [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/)([Requirements Traceability Matrix](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/))은 요구사항과 설계·개발·테스트 산출물 간의 연결 고리를 추적하는 표 — "요구사항 RQ-001이 어느 설계 문서, 어느 코드, 어느 테스트 케이스에 반영되었는가"를 한눈에 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하며, 누락·중복·불일치를 방지한다.
> 2. 양방향 추적성(Bi-directional [Traceability](/knowledge-base/studynote/12_it_management/05_security_compliance/228_blockchain_smart_contract_traceability/))이 RTM의 핵심 가치 — 전방 추적([Forward](/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/): 요구사항→테스트)은 "모든 요구사항이 테스트되었는가" [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 후방 추적(Backward: 테스트→요구사항)은 "모든 테스트가 요구사항에 기반하는가(불필요 테스트 탐지)" [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)이다.
> 3. RTM은 변경 영향 분석의 핵심 도구 — 요구사항 변경 시 RTM으로 영향받는 설계·코드·테스트 케이스를 즉시 파악하여 변경 범위와 비용을 정확히 산정할 수 있다.

---

## Ⅰ. [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) 기본 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RTM (Requirements Traceability Matrix) 구조:</div>
<div class="kb-diagram-note">목적:</div>
<div class="kb-diagram-note">요구사항 → 설계 → 구현 → 테스트 연결 추적</div>
<div class="kb-diagram-note">누락 탐지: 테스트 없는 요구사항</div>
<div class="kb-diagram-note">과잉 탐지: 요구사항 없는 기능</div>
<div class="kb-diagram-note">변경 영향 분석</div>
<div class="kb-diagram-note">기본 구성 (열):</div>
<div class="kb-diagram-note">요구사항 ID</div>
<div class="kb-diagram-note">요구사항 설명</div>
<div class="kb-diagram-note">우선순위</div>
<div class="kb-diagram-note">설계 문서 참조 (섹션)</div>
<div class="kb-diagram-note">소스코드 참조 (모듈/클래스)</div>
<div class="kb-diagram-note">테스트 케이스 ID</div>
<div class="kb-diagram-note">테스트 상태 (통과/실패/미실행)</div>
<div class="kb-diagram-note">샘플 RTM:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RQ-ID</div><div class="kb-diagram-cell">설명</div><div class="kb-diagram-cell">설계</div><div class="kb-diagram-cell">코드</div><div class="kb-diagram-cell">TC-ID</div><div class="kb-diagram-cell">상태</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RQ-001</div><div class="kb-diagram-cell">로그인 기능</div><div class="kb-diagram-cell">D-3.1</div><div class="kb-diagram-cell">AuthService</div><div class="kb-diagram-cell">TC-001</div><div class="kb-diagram-cell">통과</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RQ-002</div><div class="kb-diagram-cell">MFA 지원</div><div class="kb-diagram-cell">D-3.2</div><div class="kb-diagram-cell">MFAHandler</div><div class="kb-diagram-cell">TC-002</div><div class="kb-diagram-cell">실패</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RQ-003</div><div class="kb-diagram-cell">세션 만료 30분</div><div class="kb-diagram-cell">D-3.3</div><div class="kb-diagram-cell">SessionManager</div><div class="kb-diagram-cell">TC-003</div><div class="kb-diagram-cell">통과</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RQ-004</div><div class="kb-diagram-cell">비밀번호 재설정</div><div class="kb-diagram-cell">D-3.4</div><div class="kb-diagram-cell">-</div><div class="kb-diagram-cell">-</div><div class="kb-diagram-cell">미구현</div></div>
<div class="kb-diagram-note">RTM 분석:</div>
<div class="kb-diagram-note">RQ-002: 테스트 실패 → 버그 수정 필요</div>
<div class="kb-diagram-note">RQ-004: 코드/테스트 없음 → 구현 누락!</div>
<div class="kb-diagram-note">역방향 확인:</div>
<div class="kb-diagram-note">TC-005 가 있는데 어느 RQ에도 없음</div>
<div class="kb-diagram-note">→ TC-005는 불필요 테스트? 숨겨진 요구사항?</div>
<div class="kb-diagram-note">도구:</div>
<div class="kb-diagram-note">Jira + Xray (엔터프라이즈)</div>
<div class="kb-diagram-note">IBM DOORS (대형 시스템, 항공/국방)</div>
<div class="kb-diagram-note">Requiment 추적: Azure DevOps, Rally</div>
</div>
</div>



> 📢 **섹션 요약 비유**: RTM은 건축 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) — "설계도 3번 항목(요구사항)이 실제 벽(코드)에 있나? 감리 검사(테스트)에서 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)됐나?" 연결 추적표!

---

## Ⅱ. 양방향 추적성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">양방향 추적성 (Bi-directional Traceability):</div>
<div class="kb-diagram-note">전방 추적 (Forward Traceability):</div>
<div class="kb-diagram-note">요구사항 → 설계 → 구현 → 테스트</div>
<div class="kb-diagram-note">목적:</div>
<div class="kb-diagram-note">"모든 요구사항이 구현되고 테스트되었나?"</div>
<div class="kb-diagram-note">위험:</div>
<div class="kb-diagram-note">RQ-004 (비밀번호 재설정): 테스트 없음</div>
<div class="kb-diagram-note">→ 기능 미구현 또는 테스트 누락</div>
<div class="kb-diagram-note">후방 추적 (Backward Traceability):</div>
<div class="kb-diagram-note">테스트 → 구현 → 설계 → 요구사항</div>
<div class="kb-diagram-note">목적:</div>
<div class="kb-diagram-note">"모든 테스트 케이스가 요구사항에 기반하는가?"</div>
<div class="kb-diagram-note">탐지:</div>
<div class="kb-diagram-note">TC-999 (없는 요구사항 테스트):</div>
<div class="kb-diagram-note">→ 개발자 추가 기능? Gold Plating?</div>
<div class="kb-diagram-note">→ 필요 없는 테스트 = 비용 낭비</div>
<div class="kb-diagram-note">→ 또는 요구사항 명세 누락 발견</div>
<div class="kb-diagram-note">완전한 추적성 확인:</div>
<div class="kb-diagram-note">요구사항 커버리지:</div>
<div class="kb-diagram-note">= 테스트된 요구사항 / 전체 요구사항</div>
<div class="kb-diagram-note">목표: 100%</div>
<div class="kb-diagram-note">테스트 정당성:</div>
<div class="kb-diagram-note">= 요구사항 있는 테스트 / 전체 테스트</div>
<div class="kb-diagram-note">목표: 100%</div>
<div class="kb-diagram-note">ISO/IEC 29119 (소프트웨어 테스트 표준):</div>
<div class="kb-diagram-note">추적 매트릭스 필수 산출물</div>
<div class="kb-diagram-note">요구사항 커버리지 측정 의무화</div>
<div class="kb-diagram-note">변경 관리 연동:</div>
<div class="kb-diagram-note">RQ-003 변경: 세션 만료 30분 → 15분</div>
<div class="kb-diagram-note">RTM으로 영향 분석:</div>
<div class="kb-diagram-note">→ D-3.3 설계 수정</div>
<div class="kb-diagram-note">→ SessionManager 코드 수정</div>
<div class="kb-diagram-note">→ TC-003 테스트 케이스 수정 (15분 기준으로)</div>
<div class="kb-diagram-note">→ TC-007 (세션 연장 테스트)도 수정 필요</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 양방향 추적은 건물+감리 체크 — 앞방향(설계→건물→감리: 누락 탐지), 뒷방향(감리→건물→설계: 불필요 감리 탐지). 양방향 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)으로 완전성 보장!

---

## Ⅲ. 공공 SI에서의 [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">공공 SI 프로젝트 RTM:</div>
<div class="kb-diagram-note">공공 발주 표준:</div>
<div class="kb-diagram-note">PMO (프로젝트 관리 조직) 검토 필수</div>
<div class="kb-diagram-note">감리 시 RTM 제출 의무</div>
<div class="kb-diagram-note">요구사항 정의서 (RD)</div>
<div class="kb-diagram-note">→ 기능 설계서 (FD)</div>
<div class="kb-diagram-note">→ 소스코드</div>
<div class="kb-diagram-note">→ 단위 테스트 결과</div>
<div class="kb-diagram-note">→ 통합 테스트 결과</div>
<div class="kb-diagram-note">공공 SI RTM 구성:</div>
<div class="kb-diagram-note">요구사항 분류:</div>
<div class="kb-diagram-note">기능 요구사항 (FR)</div>
<div class="kb-diagram-note">비기능 요구사항 (NFR)</div>
<div class="kb-diagram-tree-item" style="--depth:1">성능: 응답 3초 이내</div>
<div class="kb-diagram-tree-item" style="--depth:1">보안: 개인정보 암호화</div>
<div class="kb-diagram-tree-item" style="--depth:1">가용성: 99.5%</div>
<div class="kb-diagram-note">법적 요구사항 (LR):</div>
<div class="kb-diagram-tree-item" style="--depth:1">개인정보보호법 준수</div>
<div class="kb-diagram-tree-item" style="--depth:1">전자정부법 표준</div>
<div class="kb-diagram-note">감리 RTM 검토 포인트:</div>
<div class="kb-diagram-note">1. 커버리지 확인:</div>
<div class="kb-diagram-note">기능 요구사항 → 테스트 케이스 100%</div>
<div class="kb-diagram-note">2. 테스트 결과 링크:</div>
<div class="kb-diagram-note">테스트 케이스 → 실제 테스트 실행 결과</div>
<div class="kb-diagram-note">3. 비기능 요구사항 검증:</div>
<div class="kb-diagram-note">성능 테스트 결과 (JMeter 보고서)</div>
<div class="kb-diagram-note">보안 취약점 점검 결과 (KISA 점검)</div>
<div class="kb-diagram-note">4. 변경 이력 관리:</div>
<div class="kb-diagram-note">요구사항 변경 이력 + RTM 변경 이력 일치</div>
<div class="kb-diagram-note">대표 도구:</div>
<div class="kb-diagram-note">엑셀 (소규모): 간단, 관리 어려움</div>
<div class="kb-diagram-note">JIRA + Xray: 자동 연결, 커버리지 리포트</div>
<div class="kb-diagram-note">IBM DOORS: 대형 공공, 방산</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 공공 SI RTM은 감리 보고서의 뼈대 — 감리원이 "이 기능 어디 구현?" 물으면 RTM이 즉시 답변. 없으면 감리 지적(하자)!

---

## Ⅳ. [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) 자동화



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RTM 자동화 도구 활용:</div>
<div class="kb-diagram-note">JIRA + Xray 자동화:</div>
<div class="kb-diagram-note">요구사항 생성:</div>
<div class="kb-diagram-note">JIRA Story: RQ-001 "로그인 기능"</div>
<div class="kb-diagram-note">테스트 케이스 생성:</div>
<div class="kb-diagram-note">Xray Test: TC-001</div>
<div class="kb-diagram-note">연결: TC-001 → RQ-001 (Covers 관계)</div>
<div class="kb-diagram-note">자동 커버리지:</div>
<div class="kb-diagram-note">요구사항 커버리지 대시보드 자동 갱신</div>
<div class="kb-diagram-note">CI/CD 통합:</div>
<div class="kb-diagram-note">테스트 자동 실행 (pytest, JUnit)</div>
<div class="kb-diagram-note">결과 → Xray 자동 업데이트</div>
<div class="kb-diagram-note">→ RTM 실시간 반영</div>
<div class="kb-diagram-note">AI 기반 추적 (최신 트렌드):</div>
<div class="kb-diagram-note">요구사항 텍스트 → NLP 분석</div>
<div class="kb-diagram-note">유사 테스트 케이스 자동 제안</div>
<div class="kb-diagram-note">Code → 요구사항 역추적:</div>
<div class="kb-diagram-note">소스코드 변경 → 영향 요구사항 자동 탐지</div>
<div class="kb-diagram-note">(GitHub Copilot + 추적 도구)</div>
<div class="kb-diagram-note">RTM 자동화 장점:</div>
<div class="kb-diagram-note">수동 엑셀 RTM:</div>
<div class="kb-diagram-note">→ 매번 수작업 업데이트</div>
<div class="kb-diagram-note">→ 불일치 오류 발생</div>
<div class="kb-diagram-note">자동화 RTM:</div>
<div class="kb-diagram-note">→ CI/CD와 연동 실시간 업데이트</div>
<div class="kb-diagram-note">→ 커버리지 대시보드 항상 최신</div>
<div class="kb-diagram-note">→ 변경 시 영향 분석 즉시</div>
<div class="kb-diagram-note">한계:</div>
<div class="kb-diagram-note">도구 초기 설정 비용</div>
<div class="kb-diagram-note">팀의 도구 적응 시간</div>
<div class="kb-diagram-note">요구사항이 명확해야 자동화 가능</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) 자동화는 스마트 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) — 엑셀(수동 체크) → JIRA+Xray([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 연동 자동 체크). 코드 커밋할 때마다 [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) 자동 갱신!

---

## Ⅴ. 실무 시나리오 — 의료 기기 [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">의료 기기 소프트웨어 RTM (IEC 62304):</div>
<div class="kb-diagram-note">규제 배경:</div>
<div class="kb-diagram-note">IEC 62304: 의료 기기 소프트웨어 수명주기</div>
<div class="kb-diagram-note">Class C (높은 위험): 완전한 추적성 필수</div>
<div class="kb-diagram-note">FDA 21 CFR Part 11: 전자 기록 추적성</div>
<div class="kb-diagram-note">"모든 요구사항이 테스트됨" 입증 필수</div>
<div class="kb-diagram-note">RTM 구성 (의료 기기):</div>
<div class="kb-diagram-note">소프트웨어 요구사항 명세 (SRS)</div>
<div class="kb-diagram-note">→ 소프트웨어 상세 설계 (SDD)</div>
<div class="kb-diagram-note">→ 소스 코드</div>
<div class="kb-diagram-note">→ 단위 테스트 (UT)</div>
<div class="kb-diagram-note">→ 통합 테스트 (IT)</div>
<div class="kb-diagram-note">→ 소프트웨어 검증 (SVT)</div>
<div class="kb-diagram-note">예시 (인슐린 펌프 소프트웨어):</div>
<div class="kb-diagram-note">RQ-INS-001: 혈당 임계값 180mg/dL 초과 시 경고</div>
<div class="kb-diagram-note">추적:</div>
<div class="kb-diagram-note">SDD 4.2.1 → 경고 알고리즘 설계</div>
<div class="kb-diagram-note">알림모듈.cpp → 구현</div>
<div class="kb-diagram-note">UT-INS-001 → 단위 테스트 (180 경계값 검증)</div>
<div class="kb-diagram-note">IT-INS-001 → 통합 테스트 (센서→알고리즘→알림)</div>
<div class="kb-diagram-note">SVT-INS-001 → 검증 (실제 혈당 시뮬레이터)</div>
<div class="kb-diagram-note">상태: ✅ 통과 (FDA 제출 증거)</div>
<div class="kb-diagram-note">감사 추적 (Audit Trail):</div>
<div class="kb-diagram-note">모든 요구사항 변경: 날짜, 담당자, 이유 기록</div>
<div class="kb-diagram-note">IBM DOORS: 변경 이력 자동 관리</div>
<div class="kb-diagram-note">FDA 검사관 요청:</div>
<div class="kb-diagram-note">"RQ-INS-001이 언제 생성됐나?"</div>
<div class="kb-diagram-note">→ DOORS 클릭 → 생성/변경 이력 즉시 제공</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">FDA 510(k) 심사 통과</div>
<div class="kb-diagram-note">RTM 완전성이 핵심 증거</div>
<div class="kb-diagram-note">RTM 불완전 → 심사 반려</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 의료 기기 RTM은 안전 인증서 — "이 혈당 경고(요구사항)가 실제 코드(구현)에 있고, 테스트([검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/))로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)됐다"는 FDA 증거. [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) 빠지면 의료 기기 판매 불가!

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RTM (요구사항 추적 매트릭스)</div>
<div class="kb-diagram-note">+-- 추적 방향</div>
<div class="kb-diagram-note">+-- 전방 (요구사항 → 테스트)</div>
<div class="kb-diagram-note">+-- 후방 (테스트 → 요구사항)</div>
<div class="kb-diagram-note">+-- 활용</div>
<div class="kb-diagram-note">+-- 커버리지 분석</div>
<div class="kb-diagram-note">+-- 변경 영향 분석</div>
<div class="kb-diagram-note">+-- 감리/감사 증거</div>
<div class="kb-diagram-note">+-- 도구</div>
<div class="kb-diagram-note">+-- JIRA + Xray</div>
<div class="kb-diagram-note">+-- IBM DOORS (안전-필수)</div>
<div class="kb-diagram-note">+-- 적용 표준</div>
<div class="kb-diagram-note">+-- IEEE 829 (테스트)</div>
<div class="kb-diagram-note">+-- IEC 62304 (의료)</div>
<div class="kb-diagram-note">+-- ISO 26262 (자동차)</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 문서 추적 (1980s)]
수작업 참조 문서
방산/항공 요구
      |
      v
[IEEE 830 요구사항 표준 (1993)]
요구사항 명세 표준화
RTM 개념 공식화
      |
      v
[CASE 도구 (1990s~)]
DOORS, Requisite Pro
자동 추적 관리
      |
      v
[애자일 + RTM (2000s~)]
JIRA 스토리 ↔ 테스트 연결
CI/CD 자동화 RTM
      |
      v
[현재: AI 기반 추적]
NLP 요구사항 분석
코드↔요구사항 자동 매핑
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. RTM은 연결 지도 — "요구사항 001번이 어느 코드(지점 A), 어느 테스트(검사소 B)에 있나?" 지도. 없으면 길을 잃어요!
2. 양방향 추적 — 앞으로(요구사항→테스트: 테스트 빠진 것 찾기), 뒤로(테스트→요구사항: 불필요 테스트 찾기). 양방향 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)!
3. 의료 기기 RTM은 안전 인증서 — 혈당 경고 기능이 코드+테스트로 증명돼야 FDA 통과. RTM이 없으면 의료 기기 판매 금지!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 71 / 530

← **이전**: [47. 요구사항 추적 매트릭스 양방향 추적성 검증 (RTM Bidirectional Traceability Validation)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/047_rtm_bidirectional_traceability_validation/)
**다음**: [048. 소프트웨어 산출물 검증 — Deliverables Verification](/knowledge-base/studynote/11_design_supervision/01_audit_framework/048_software_deliverables_verification/) →

---
