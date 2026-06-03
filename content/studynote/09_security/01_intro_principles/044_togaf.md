+++
title = "044. TOGAF — 엔터프라이즈 아키텍처 프레임워크"
date = 2026-04-05

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

> **핵심 인사이트**
> 1. [TOGAF](/knowledge-base/studynote/12_it_management/03_ea_isp/113_togaf/)([The Open Group](/knowledge-base/studynote/12_it_management/03_ea_isp/113_togaf/) [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) Framework)는 엔터프라이즈 아키텍처([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/))를 개발·관리하는 세계 표준 프레임워크로 — 비즈니스·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·애플리케이션·기술의 4개 아키텍처 도메인과 [ADM](/knowledge-base/studynote/03_network/01_data_communication/066_적응형_델타_변조_ADM/)([Architecture Development Method](/knowledge-base/studynote/12_it_management/03_ea_isp/114_togaf_adm_architecture_development_method/)) 9단계 사이클로 구성된다.
> 2. [ADM](/knowledge-base/studynote/03_network/01_data_communication/066_적응형_델타_변조_ADM/)([Architecture Development Method](/knowledge-base/studynote/12_it_management/03_ea_isp/114_togaf_adm_architecture_development_method/))은 예비 단계 → A(비전) → B(비즈니스) → C(정보시스템) → D(기술) → E(기회/해결) → F(마이그레이션) → G(거버넌스) → H([변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/))의 순환 사이클로 — 아키텍처가 비즈니스 전략과 IT 구현 사이의 단절을 메우는 체계적 접근법이다.
> 3. TOGAF의 아키텍처 저장소([Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) Repository)와 아키텍처 역량 프레임워크(ACF)는 조직이 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 역량을 성숙시키는 로드맵을 제공하며 — IT 거버넌스, 비용 최적화, 비즈니스-IT 정렬의 실질적 도구로 금융·공공·제조 등 대규모 조직에서 광범위하게 활용된다.

---

## Ⅰ. [TOGAF](/knowledge-base/studynote/12_it_management/03_ea_isp/113_togaf/) 개요

```
TOGAF (The Open Group Architecture Framework):

발행: The Open Group (1995년 초판, 현재 TOGAF 10)
목적: EA 개발·운영을 위한 표준 방법론

엔터프라이즈 아키텍처 (EA):
  조직의 비전·전략을 IT 시스템으로 구현하는
  구조적·통합적 청사진
  
  "조직이 어떻게 작동하고, IT가 어떻게 지원하는가"

4개 아키텍처 도메인 (BDAT):
  B — Business Architecture (비즈니스):
    비즈니스 전략, 거버넌스, 조직, 프로세스
    
  D — Data Architecture (데이터):
    데이터 자산 구조, 데이터 흐름, 데이터 관리
    
  A — Application Architecture (애플리케이션):
    애플리케이션 구성, 인터페이스, 시스템 간 관계
    
  T — Technology Architecture (기술):
    HW/SW 인프라, 네트워크, 플랫폼

아키텍처 격차:
  현행 아키텍처 (Baseline/As-Is)
  목표 아키텍처 (Target/To-Be)
  격차 분석 (Gap Analysis)
  
  TOGAF ADM: 격차를 체계적으로 메우는 사이클
```

> 📢 **섹션 요약 비유**: TOGAF는 도시 마스터플랜 — 건물(비즈니스)·도로([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))·시설(애플리케이션)·인프라(기술)의 4개 레이어를 통합적으로 설계하는 도시 계획 표준.

---

## Ⅱ. [ADM](/knowledge-base/studynote/03_network/01_data_communication/066_적응형_델타_변조_ADM/) 사이클



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ADM (Architecture Development Method):</div>
<div class="kb-diagram-note">예비 단계 (Preliminary):</div>
<div class="kb-diagram-note">EA 역량 준비</div>
<div class="kb-diagram-note">아키텍처 원칙(Principle) 정의</div>
<div class="kb-diagram-note">A. 아키텍처 비전 (Architecture Vision):</div>
<div class="kb-diagram-note">이해관계자 관심사 파악</div>
<div class="kb-diagram-note">비즈니스 목표 → 아키텍처 비전 수립</div>
<div class="kb-diagram-note">Statement of Architecture Work 승인</div>
<div class="kb-diagram-note">B. 비즈니스 아키텍처:</div>
<div class="kb-diagram-note">비즈니스 전략·목표·드라이버 분석</div>
<div class="kb-diagram-note">현행/목표 비즈니스 프로세스 모델</div>
<div class="kb-diagram-note">Gap Analysis</div>
<div class="kb-diagram-note">C. 정보 시스템 아키텍처:</div>
<div class="kb-diagram-note">C1: 데이터 아키텍처 (논리/물리 데이터 모델)</div>
<div class="kb-diagram-note">C2: 애플리케이션 아키텍처 (시스템 목록, 인터페이스)</div>
<div class="kb-diagram-note">D. 기술 아키텍처:</div>
<div class="kb-diagram-note">플랫폼, 미들웨어, 네트워크, 보안 인프라</div>
<div class="kb-diagram-note">현행/목표 기술 스택 Gap Analysis</div>
<div class="kb-diagram-note">E. 기회와 해결책 (Opportunities &amp; Solutions):</div>
<div class="kb-diagram-note">아키텍처 로드맵 초안</div>
<div class="kb-diagram-note">작업 패키지(Work Package) 정의</div>
<div class="kb-diagram-note">F. 마이그레이션 계획:</div>
<div class="kb-diagram-note">이행 순서, 비용/이익 분석</div>
<div class="kb-diagram-note">최종 아키텍처 로드맵</div>
<div class="kb-diagram-note">G. 거버넌스 구현:</div>
<div class="kb-diagram-note">아키텍처 변경 감독</div>
<div class="kb-diagram-note">컴플라이언스 점검</div>
<div class="kb-diagram-note">H. 아키텍처 변경 관리:</div>
<div class="kb-diagram-note">기술/비즈니스 변경 모니터링</div>
<div class="kb-diagram-note">다음 ADM 사이클 트리거</div>
<div class="kb-diagram-note">중앙: 아키텍처 요구사항 관리</div>
<div class="kb-diagram-note">→ 모든 단계에서 지속적으로 관리</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [ADM](/knowledge-base/studynote/03_network/01_data_communication/066_적응형_델타_변조_ADM/) 9단계는 건물 설계 프로세스 — 비전(설계 콘셉트) → 비즈니스(용도) → [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)/앱(내부 구조) → 기술(자재) → 공사 계획 → 시공 감리 → 준공 후 유지.

---

## Ⅲ. [TOGAF](/knowledge-base/studynote/12_it_management/03_ea_isp/113_togaf/) 핵심 개념



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">아키텍처 빌딩 블록 (ABB vs SBB):</div>
<div class="kb-diagram-note">ABB (Architecture Building Block):</div>
<div class="kb-diagram-note">아키텍처 명세서의 구성 요소 (논리적)</div>
<div class="kb-diagram-note">"무엇이 필요한가?"</div>
<div class="kb-diagram-note">예: "인증 서비스 필요"</div>
<div class="kb-diagram-note">SBB (Solution Building Block):</div>
<div class="kb-diagram-note">ABB를 구현하는 실제 제품/컴포넌트 (물리적)</div>
<div class="kb-diagram-note">"어떻게 구현하는가?"</div>
<div class="kb-diagram-note">예: "Keycloak IAM 솔루션"</div>
<div class="kb-diagram-note">아키텍처 저장소 (Architecture Repository):</div>
<div class="kb-diagram-note">Architecture Metamodel: 아키텍처 언어 정의</div>
<div class="kb-diagram-note">Architecture Landscape: 현행 아키텍처 현황</div>
<div class="kb-diagram-note">Standards Information Base: 기준·표준 목록</div>
<div class="kb-diagram-note">Reference Library: 참조 모델, 뷰포인트</div>
<div class="kb-diagram-note">Governance Log: 변경 이력, 의사결정</div>
<div class="kb-diagram-note">아키텍처 원칙 (Architecture Principles):</div>
<div class="kb-diagram-note">비즈니스·데이터·애플리케이션·기술 각각의 원칙</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-tree-item" style="--depth:1">"데이터는 한 번만 수집된다 (Single Source of Truth)"</div>
<div class="kb-diagram-tree-item" style="--depth:1">"모든 시스템은 표준 인터페이스를 통해 연동"</div>
<div class="kb-diagram-tree-item" style="--depth:1">"보안은 설계 시점에 내재화 (Security by Design)"</div>
<div class="kb-diagram-note">이해관계자 관리 (Stakeholder Management):</div>
<div class="kb-diagram-note">아키텍처 비전: 관심사 → 뷰포인트 → 뷰</div>
<div class="kb-diagram-note">CEO: 비즈니스 영향 뷰</div>
<div class="kb-diagram-note">CTO: 기술 스택 뷰</div>
<div class="kb-diagram-note">개발팀: 컴포넌트 다이어그램</div>
<div class="kb-diagram-note">감사: 보안·컴플라이언스 뷰</div>
<div class="kb-diagram-note">각 이해관계자에게 필요한 뷰만 제공</div>
</div>
</div>



> 📢 **섹션 요약 비유**: ABB vs SBB는 설계도 vs 실제 자재 — ABB는 "여기 방이 필요해"(설계), SBB는 "이케아 가구 사용"(실제 구현). TOGAF는 설계와 구현을 연결해요.

---

## Ⅳ. TOGAF와 보안



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">TOGAF와 보안 아키텍처 통합:</div>
<div class="kb-diagram-note">보안은 TOGAF의 모든 도메인에 적용:</div>
<div class="kb-diagram-note">B. 비즈니스: 보안 정책, 컴플라이언스 요건</div>
<div class="kb-diagram-note">D. 데이터: 데이터 분류, 암호화, 접근 제어</div>
<div class="kb-diagram-note">A. 애플리케이션: 인증/인가, IAM, API 보안</div>
<div class="kb-diagram-note">T. 기술: 방화벽, SIEM, PKI, 제로 트러스트</div>
<div class="kb-diagram-note">SABSA와 TOGAF 매핑:</div>
<div class="kb-diagram-note">SABSA (Sherwood Applied Business Security Architecture):</div>
<div class="kb-diagram-note">비즈니스 주도 보안 아키텍처 프레임워크</div>
<div class="kb-diagram-note">TOGAF 계층 → SABSA 계층:</div>
<div class="kb-diagram-note">비즈니스 → Contextual (Why)</div>
<div class="kb-diagram-note">데이터 → Conceptual (What)</div>
<div class="kb-diagram-note">애플리케이션 → Logical (How)</div>
<div class="kb-diagram-note">기술 → Physical (With what)</div>
<div class="kb-diagram-note">보안 아키텍처 산출물:</div>
<div class="kb-diagram-note">보안 원칙: "최소 권한, 심층 방어, 실패 안전"</div>
<div class="kb-diagram-note">위협 모델: STRIDE 기반 위협 카탈로그</div>
<div class="kb-diagram-note">보안 기준선: 표준 보안 통제 목록</div>
<div class="kb-diagram-note">보안 로드맵: ADM F단계에 통합</div>
<div class="kb-diagram-note">Zero Trust 통합:</div>
<div class="kb-diagram-note">TOGAF 기술 아키텍처:</div>
<div class="kb-diagram-tree-item" style="--depth:1">네트워크 세그먼트 대신 ID 기반 접근</div>
<div class="kb-diagram-tree-item" style="--depth:1">마이크로세그멘테이션</div>
<div class="kb-diagram-tree-item" style="--depth:1">지속적 검증 (Never Trust, Always Verify)</div>
<div class="kb-diagram-note">TOGAF 로드맵에 ZT 마이그레이션 계획 포함</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [TOGAF](/knowledge-base/studynote/12_it_management/03_ea_isp/113_togaf/) 보안 통합은 건물 보안 설계 — 설계 초기부터 잠금장치(보안)를 설계에 포함. 완공 후 자물쇠 붙이기보다 훨씬 효과적이고 저렴해요.

---

## Ⅴ. 실무 시나리오 — 공공기관 차세대 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">공공기관 차세대 시스템 TOGAF 적용:</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">기관: 국세청 (가상)</div>
<div class="kb-diagram-note">현황: 노후 메인프레임 시스템 (30년 이상)</div>
<div class="kb-diagram-note">목표: 클라우드 기반 차세대 세금 신고 시스템</div>
<div class="kb-diagram-note">TOGAF ADM 적용:</div>
<div class="kb-diagram-note">예비 단계:</div>
<div class="kb-diagram-note">EA 팀 구성 (3인: 비즈니스/데이터/기술 아키텍트)</div>
<div class="kb-diagram-note">아키텍처 원칙 15개 승인</div>
<div class="kb-diagram-note">A단계 — 비전:</div>
<div class="kb-diagram-note">이해관계자: 국세청장, CIO, 납세자, 세무사</div>
<div class="kb-diagram-note">비전: "납세자 편의 3배, 시스템 비용 40% 절감"</div>
<div class="kb-diagram-note">B단계 — 비즈니스:</div>
<div class="kb-diagram-note">현행: 종이 신고 → 담당자 입력 → 심사 → 결정</div>
<div class="kb-diagram-note">목표: 자동 신고 → AI 검증 → 즉시 처리</div>
<div class="kb-diagram-note">C단계 — 정보 시스템:</div>
<div class="kb-diagram-note">데이터: 납세자 마스터, 거래 내역, 과세 DB</div>
<div class="kb-diagram-note">→ 통합 데이터 레이크로 전환</div>
<div class="kb-diagram-note">애플리케이션: 신고 포털, AI 심사 엔진, 민원 시스템</div>
<div class="kb-diagram-note">D단계 — 기술:</div>
<div class="kb-diagram-note">현행: 메인프레임 (IBM Z series)</div>
<div class="kb-diagram-note">목표: AWS/NCP 클라우드 (GovCloud)</div>
<div class="kb-diagram-note">이행: 비중요 시스템부터 클라우드 이전</div>
<div class="kb-diagram-note">F단계 — 마이그레이션 계획:</div>
<div class="kb-diagram-note">연도별 이행:</div>
<div class="kb-diagram-note">2026: 민원 시스템 클라우드 이전</div>
<div class="kb-diagram-note">2027: 데이터 레이크 구축</div>
<div class="kb-diagram-note">2028: AI 심사 엔진 가동</div>
<div class="kb-diagram-note">2029: 메인프레임 폐기</div>
<div class="kb-diagram-note">결과 (3년 후):</div>
<div class="kb-diagram-note">납세자 신고 처리 시간: 14일 → 즉시</div>
<div class="kb-diagram-note">IT 운영 비용: 40% 절감</div>
<div class="kb-diagram-note">TOGAF: 3년간의 복잡한 의사결정을 정렬한 나침반</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 공공기관 TOGAF는 도시 재개발 마스터플랜 — 낡은 건물(메인프레임)을 새 빌딩(클라우드)으로 교체할 때 어느 건물을 먼저 허물고, 어떤 순서로 새로 지을지 체계적으로 계획.

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">TOGAF</div>
<div class="kb-diagram-note">+-- 4 도메인 (BDAT)</div>
<div class="kb-diagram-note">+-- Business, Data, Application, Technology</div>
<div class="kb-diagram-note">+-- ADM 9단계</div>
<div class="kb-diagram-note">+-- 예비→A→B→C→D→E→F→G→H</div>
<div class="kb-diagram-note">+-- 핵심 개념</div>
<div class="kb-diagram-note">+-- ABB (논리), SBB (물리)</div>
<div class="kb-diagram-note">+-- 아키텍처 원칙</div>
<div class="kb-diagram-note">+-- 아키텍처 저장소</div>
<div class="kb-diagram-note">+-- 관련 프레임워크</div>
<div class="kb-diagram-note">+-- SABSA (보안 아키텍처)</div>
<div class="kb-diagram-note">+-- Zachman Framework</div>
<div class="kb-diagram-note">+-- FEAF (미국 연방 EA)</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도

```
[Zachman Framework (1987)]
EA 최초 프레임워크
6×6 행렬 구조
      |
      v
[TOGAF 초판 (1995)]
The Open Group 발행
TAFIM (미 국방부) 기반
      |
      v
[TOGAF 9 (2009)]
ADM 체계화
아키텍처 역량 프레임워크 추가
      |
      v
[TOGAF 10 (2022)]
애자일 EA 통합
클라우드/디지털 트랜스포메이션 반영
      |
      v
[현재: EA + DevOps]
지속적 아키텍처 진화
IaC와 EA 자동화 통합
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. TOGAF는 도시 마스터플랜 — 건물(비즈니스), 도로([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)), 시설(앱), 인프라(기술) 4개 레이어를 통합 설계하는 표준 계획서예요!
2. [ADM](/knowledge-base/studynote/03_network/01_data_communication/066_적응형_델타_변조_ADM/) 9단계는 건물 설계~시공 과정 — 비전→비즈니스→기술 순서로 설계하고, 마이그레이션 계획으로 단계적으로 옮겨가요.
3. [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 없이 IT 투자하면 낭비 — 한 팀이 만든 시스템이 다른 팀 시스템과 안 맞으면 다시 만들어야 해요. TOGAF는 이 낭비를 막는 설계도예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 44 / 1108

← **이전**: [043. OSA — 오픈 보안 아키텍처 (Open Security Architecture)](/knowledge-base/studynote/09_security/01_intro_principles/043_osa/)
**다음**: [045. NIST 사이버보안 프레임워크 2.0 — NIST CSF 2.0](/knowledge-base/studynote/09_security/01_intro_principles/045_nist_csf_2_0/) →

---
