+++
title = "045. NIST 사이버보안 프레임워크 2.0 — NIST CSF 2.0"
date = 2026-04-05

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

> **핵심 인사이트**
> 1. NIST [CSF](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/)(Cybersecurity Framework) 2.0(2024)은 기존 5대 기능([식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)·[보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)·탐지·대응·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/))에 "거버넌스(Govern)"를 추가해 6대 기능으로 확장 — 사이버보안을 기술 문제가 아닌 경영 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)로 보는 관점 전환이 핵심이다.
> 2. [CSF](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/) 2.0의 가장 큰 변화는 적용 범위 확대 — 기존 핵심 인프라 중심에서 모든 규모·유형의 조직으로 확대되었으며, [공급망 보안](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/)(SCRM)과 거버넌스 강화가 주요 추가 사항이다.
> 3. CSF는 규정(Regulation)이 아닌 프레임워크(Framework) — 법적 강제력이 없어 각 조직이 자신의 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 환경에 맞게 선택적으로 적용하며, [ISMS-P](/knowledge-base/studynote/12_it_management/05_security_compliance/171_isms_p/), ISO 27001 등 다른 표준과 매핑해 중복 작업을 줄일 수 있다.

---

## Ⅰ. NIST [CSF](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/) 개요



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">NIST CSF 발전:</div>
<div class="kb-diagram-note">CSF 1.0 (2014):</div>
<div class="kb-diagram-note">배경: 2013년 미국 오바마 행정명령 13636</div>
<div class="kb-diagram-note">(핵심 인프라 사이버보안 강화)</div>
<div class="kb-diagram-note">대상: 에너지, 금융, 의료 등 핵심 인프라</div>
<div class="kb-diagram-note">구조: 5대 기능 (식별-보호-탐지-대응-복구)</div>
<div class="kb-diagram-note">CSF 1.1 (2018):</div>
<div class="kb-diagram-note">공급망 리스크 관리 추가</div>
<div class="kb-diagram-note">자기 평가 지침 강화</div>
<div class="kb-diagram-note">CSF 2.0 (2024.02):</div>
<div class="kb-diagram-note">6대 기능: 거버넌스 추가</div>
<div class="kb-diagram-note">적용 범위: 모든 조직 (규모·유형 무관)</div>
<div class="kb-diagram-note">공급망 보안 강화</div>
<div class="kb-diagram-note">CSF 프로파일 업데이트</div>
<div class="kb-diagram-note">CSF 2.0 구조:</div>
<div class="kb-diagram-note">핵심 (Core):</div>
<div class="kb-diagram-note">6개 기능 → 카테고리 → 세부 카테고리</div>
<div class="kb-diagram-note">계층 (Tiers): 1~4단계 성숙도</div>
<div class="kb-diagram-note">프로파일 (Profile):</div>
<div class="kb-diagram-note">현재 상태 vs 목표 상태 갭 분석</div>
</div>
</div>



> 📢 **섹션 요약 비유**: CSF는 보안 체력 측정 키트 — 우리 회사 보안 상태(현재 프로파일)를 측정하고, 목표(목표 프로파일)와 비교해 부족한 부분을 개선해요. 법이 아닌 가이드!

---

## Ⅱ. 6대 기능 ([CSF](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/) Core Functions)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">NIST CSF 2.0 6대 기능:</div>
<div class="kb-diagram-note">1. 거버넌스 (GOVERN) — NEW in 2.0:</div>
<div class="kb-diagram-note">목적: 사이버보안 전략·정책·책임 수립</div>
<div class="kb-diagram-note">카테고리:</div>
<div class="kb-diagram-tree-item" style="--depth:1">GV.OC: 조직 컨텍스트</div>
<div class="kb-diagram-tree-item" style="--depth:1">GV.RM: 리스크 관리 전략</div>
<div class="kb-diagram-tree-item" style="--depth:1">GV.RR: 역할·책임·권한</div>
<div class="kb-diagram-tree-item" style="--depth:1">GV.PO: 정책</div>
<div class="kb-diagram-tree-item" style="--depth:1">GV.OV: 감독</div>
<div class="kb-diagram-tree-item" style="--depth:1">GV.SC: 공급망 리스크 관리</div>
<div class="kb-diagram-note">2. 식별 (IDENTIFY):</div>
<div class="kb-diagram-note">목적: IT/OT 자산, 리스크, 취약점 파악</div>
<div class="kb-diagram-note">자산 관리, 위험 평가, 개선 활동</div>
<div class="kb-diagram-note">3. 보호 (PROTECT):</div>
<div class="kb-diagram-note">목적: 사이버보안 결과 보장 서비스</div>
<div class="kb-diagram-note">접근 제어, 인식·훈련, 데이터 보안,</div>
<div class="kb-diagram-note">플랫폼 보안, 기술 인프라 강화</div>
<div class="kb-diagram-note">4. 탐지 (DETECT):</div>
<div class="kb-diagram-note">목적: 사이버보안 사건 발견</div>
<div class="kb-diagram-note">지속적 모니터링, 이상 탐지</div>
<div class="kb-diagram-note">5. 대응 (RESPOND):</div>
<div class="kb-diagram-note">목적: 탐지된 사건 처리</div>
<div class="kb-diagram-note">인시던트 관리, 분석, 완화, 보고</div>
<div class="kb-diagram-note">6. 복구 (RECOVER):</div>
<div class="kb-diagram-note">목적: 영향 받은 역량/서비스 복원</div>
<div class="kb-diagram-note">인시던트 복구, 커뮤니케이션</div>
<div class="kb-diagram-note">시각화:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">GV</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">IDENTIFY → PROTECT</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DETECT → RESPOND → RECOVER</div></div>
<div class="kb-diagram-note">거버넌스가 모든 기능을 포괄</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 6대 기능은 보안 요리 레시피 — 거버넌스(주방장 역할 지정), [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)(재료 파악), [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)(냉장 보관), 탐지(상한 음식 발견), 대응(처리), [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)(다시 요리)!

---

## Ⅲ. [CSF](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/) 계층 (Tiers)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">CSF 성숙도 계층:</div>
<div class="kb-diagram-note">Tier 1 — 부분적 (Partial):</div>
<div class="kb-diagram-note">사이버보안 관행이 비공식적·임기응변</div>
<div class="kb-diagram-note">리스크 인식 낮음</div>
<div class="kb-diagram-note">공급망 리스크 관리 없음</div>
<div class="kb-diagram-note">Tier 2 — 리스크 인식 (Risk Informed):</div>
<div class="kb-diagram-note">리스크 인식 있지만 조직 전체 정책 없음</div>
<div class="kb-diagram-note">부서별 독립 수행</div>
<div class="kb-diagram-note">일부 공급망 리스크 관리</div>
<div class="kb-diagram-note">Tier 3 — 반복 가능 (Repeatable):</div>
<div class="kb-diagram-note">공식 정책, 조직 전체 적용</div>
<div class="kb-diagram-note">리스크 기반 접근</div>
<div class="kb-diagram-note">공급망 파트너와 정보 공유</div>
<div class="kb-diagram-note">Tier 4 — 적응적 (Adaptive):</div>
<div class="kb-diagram-note">지속적 개선 프로세스</div>
<div class="kb-diagram-note">위협 정보 실시간 반영</div>
<div class="kb-diagram-note">공급망 전체와 협력</div>
<div class="kb-diagram-note">계층 선택:</div>
<div class="kb-diagram-note">모든 조직이 Tier 4 될 필요 없음</div>
<div class="kb-diagram-note">비용-편익 분석으로 적절한 계층 선택</div>
<div class="kb-diagram-note">예: 소규모 의료기관 → Tier 2 목표</div>
<div class="kb-diagram-note">대형 금융기관 → Tier 3~4 목표</div>
<div class="kb-diagram-note">계층 vs 성숙도:</div>
<div class="kb-diagram-note">계층은 단계적 목표 아닌 현 상태 설명</div>
<div class="kb-diagram-note">"우리는 Tier 2이고, Tier 3 목표"</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [CSF](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/) 계층은 운전 실력 — Tier 1: 처음 운전(임기응변), Tier 2: 기초 교통 법규 알기, Tier 3: 방어 운전, Tier 4: 레이서(실시간 대응). 목적지에 맞는 실력이면 OK!

---

## Ⅳ. 국내 보안 표준 매핑



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">CSF 2.0과 국내 표준 매핑:</div>
<div class="kb-diagram-note">ISMS-P (개인정보보호 관리체계):</div>
<div class="kb-diagram-note">2.2.1 현황 및 위험 분석 ↔ CSF IDENTIFY</div>
<div class="kb-diagram-note">2.5.1 사용자 인증 ↔ CSF PROTECT</div>
<div class="kb-diagram-note">2.11.1 사고 예방 및 대응 ↔ CSF RESPOND</div>
<div class="kb-diagram-note">ISO/IEC 27001:</div>
<div class="kb-diagram-note">A.5 정보보안 정책 ↔ CSF GOVERN</div>
<div class="kb-diagram-note">A.8 자산 관리 ↔ CSF IDENTIFY</div>
<div class="kb-diagram-note">A.16 보안 사고 ↔ CSF RESPOND/RECOVER</div>
<div class="kb-diagram-note">활용 이점:</div>
<div class="kb-diagram-note">중복 평가 최소화</div>
<div class="kb-diagram-note">기존 ISO 27001 인증 활용 → CSF 갭 최소화</div>
<div class="kb-diagram-note">K-ISMS → ISMS-P → CSF 2.0 연계:</div>
<div class="kb-diagram-note">금융 CISO: CSF 2.0 기반 보안 전략 수립</div>
<div class="kb-diagram-note">기존 ISMS-P 관리 항목 CSF 카테고리 매핑</div>
<div class="kb-diagram-note">중복 작업 제거, 글로벌 커뮤니케이션 향상</div>
<div class="kb-diagram-note">공급망 보안 (GV.SC):</div>
<div class="kb-diagram-note">CSF 2.0 강화 사항</div>
<div class="kb-diagram-note">주요 활동:</div>
<div class="kb-diagram-tree-item" style="--depth:1">공급업체 보안 평가</div>
<div class="kb-diagram-tree-item" style="--depth:1">소프트웨어 BOM (SBOM)</div>
<div class="kb-diagram-tree-item" style="--depth:1">공급망 리스크 모니터링</div>
<div class="kb-diagram-note">배경: SolarWinds 공급망 공격 (2020)</div>
<div class="kb-diagram-note">→ 미 정부 기관 18,000개 영향</div>
</div>
</div>



> 📢 **섹션 요약 비유**: CSF와 국내 표준 매핑은 공통 교과서 — ISO 27001도 배우고, ISMS-P도 배우지만, [CSF](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/) 지도로 보면 "이건 PROTECT, 저건 IDENTIFY" 한눈에 정리!

---

## Ⅴ. 실무 시나리오 — 제조업 [CSF](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/) 2.0 적용

```
자동차 부품 제조업체 CSF 2.0 적용:

배경:
  OT(Operational Technology) 환경 + IT 연결 증가
  고객사(완성차): 공급망 보안 요구 증가
  최근 랜섬웨어로 공장 3일 중단 경험

현재 상태 프로파일 (AS-IS):
  GOVERN:   Tier 1 (보안 정책 없음)
  IDENTIFY: Tier 2 (일부 자산 목록)
  PROTECT:  Tier 1 (방화벽만)
  DETECT:   Tier 1 (시스로그 없음)
  RESPOND:  Tier 1 (절차 없음)
  RECOVER:  Tier 2 (백업 있으나 미테스트)

목표 프로파일 (TO-BE, 18개월):
  GOVERN:   Tier 3 (정책, 역할 수립)
  IDENTIFY: Tier 3 (전체 자산, 취약점 관리)
  PROTECT:  Tier 3 (MFA, 네트워크 분리)
  DETECT:   Tier 2 (SIEM 도입)
  RESPOND:  Tier 2 (인시던트 대응 절차)
  RECOVER:  Tier 3 (BCP, 복구 테스트)

우선순위 액션 (갭 분석 기반):
  1순위: GOVERN — 보안 정책 수립, CISO 지정
  2순위: PROTECT — OT/IT 망 분리
  3순위: DETECT — SIEM 도입
  4순위: RESPOND — 플레이북 작성

결과:
  공급망 보안 평가 점수: 45 → 78점
  완성차 고객사 보안 요구사항 충족
  사이버보험 가입 가능 (이전: 거부)
```

> 📢 **섹션 요약 비유**: 제조업 [CSF](/knowledge-base/studynote/12_it_management/01_governance_strategy/017_csf/) 적용은 공장 안전 점검 — 지금 상태([AS-IS](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/))를 점검하고, 목표(TO-BE) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/). 가장 취약한 곳(Tier 1 GOVERN)부터 보강해서 고객사와 보험사 신뢰!

---

## 📌 관련 개념 맵

```
NIST CSF 2.0
+-- 6대 기능
|   +-- GOVERN (신규)
|   +-- IDENTIFY / PROTECT
|   +-- DETECT / RESPOND / RECOVER
+-- 계층 (Tiers 1~4)
+-- 프로파일 (현재↔목표)
+-- 비교/연계
|   +-- ISO 27001
|   +-- ISMS-P
|   +-- NIST SP 800-53
+-- 공급망 보안 (SCRM)
    +-- SBOM
    +-- 공급업체 평가
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[NIST CSF 1.0 (2014)]
핵심 인프라 대상
5대 기능 (IPDRR)
      |
      v
[CSF 1.1 (2018)]
공급망 리스크 관리 추가
자기 평가 강화
      |
      v
[SolarWinds 공급망 공격 (2020)]
공급망 보안 긴급성 부각
행정명령 14028
      |
      v
[NIST CSF 2.0 (2024)]
GOVERN 기능 추가
모든 조직 대상 확장
공급망·SBOM 강화
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. CSF는 보안 체력 진단표 — 우리 회사가 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/), [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/), 탐지, 대응, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 얼마나 잘 하는지 점수 매기고 개선해요!
2. GOVERN은 새로 추가된 "대장 역할" — 보안을 경영진이 직접 챙기고 책임지는 체계. 기술만이 아닌 경영 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)로!
3. Tier는 운전 레벨 — 초보(Tier 1)→기본(Tier 2)→안전(Tier 3)→전문가(Tier 4). 필요한 레벨까지만 올리면 돼요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 45 / 1108

← **이전**: [044. TOGAF — 엔터프라이즈 아키텍처 프레임워크](/knowledge-base/studynote/09_security/01_intro_principles/044_togaf/)
**다음**: [046. 제로 트러스트 — Zero Trust Security](/knowledge-base/studynote/09_security/01_intro_principles/046_zero_trust/) →

---
