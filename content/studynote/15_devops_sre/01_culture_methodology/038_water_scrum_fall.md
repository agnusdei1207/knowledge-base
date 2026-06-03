+++
title = "038. 워터스크럼폴 (WaterScrumFall) — 애자일 실패 패턴"
date = 2026-03-03

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

> **핵심 인사이트**
> 1. 워터스크럼폴(WaterScrumFall)은 기획과 배포는 전통적인 워터폴 방식으로, 개발만 [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/) 형태로 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)되는 반()[애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)으로, [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)의 핵심 가치인 "고객 피드백을 통한 지속적 적응"이 불가능한 형태다.
> 2. 조직이 워터스크럼폴에 빠지는 가장 흔한 원인은 구조적 장벽 — 기획팀(PRD 고정), 개발팀([스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/)), 운영팀(분기 별 릴리즈)이 각자의 [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)에서 [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/) 프레임워크만 이식하고 전체 가치 흐름은 바꾸지 않기 때문이다.
> 3. 진정한 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 전환은 팀 구조 변경(교차 기능팀)과 배포 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD) 모두가 바뀌어야 완성되며, [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/) 세리머니만 도입하는 것은 형식적 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)(Cargo Cult [Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/))에 불과하다.

---

## I. 워터스크럼폴 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">워터스크럼폴 패턴:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">기획/요구사항 수집</div><div class="kb-diagram-note">(Waterfall Phase 1)</div></div>
<div class="kb-diagram-note">6개월 PRD(Product Requirements Doc) 작성</div>
<div class="kb-diagram-note">요구사항 고정, 변경 어려움</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스프린트 개발</div><div class="kb-diagram-note">(Scrum Phase)</div></div>
<div class="kb-diagram-note">2주 스프린트 반복</div>
<div class="kb-diagram-note">요구사항이 이미 고정되어 있어</div>
<div class="kb-diagram-note">"스프린트 계획 미팅"은 형식적</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">통합 테스트/스테이징</div><div class="kb-diagram-note">(Waterfall Phase 2)</div></div>
<div class="kb-diagram-note">수 개월간 QA, UAT</div>
<div class="kb-diagram-note">대규모 통합 -&gt; 결함 폭발</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">분기별 배포</div><div class="kb-diagram-note">(Waterfall Phase 3)</div></div>
<div class="kb-diagram-note">분기 1회 프로덕션 릴리즈</div>
<div class="kb-diagram-tree-item" style="--depth:0">피드백 주기: 6개월 이상</div>
<div class="kb-diagram-note">진짜 애자일:</div>
<div class="kb-diagram-note">2주마다 프로덕션 배포 + 고객 피드백</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 마라톤 코치가 경기 3개월 전에 훈련 계획을 완전히 고정한 뒤, 매일 "[스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/)"라고 부르는 것 — 이름만 빠를 뿐 실제론 같은 속도.

---

## II. [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 실패 패턴

```
흔한 애자일 실패 패턴:

1. 워터스크럼폴:
기획/배포 워터폴 + 개발만 스크럼

2. 스크럼버스터 (ScrumBuster):
스크럼 마스터가 없거나 형식적
스프린트 목표 없이 작업 목록만 관리

3. 화물 컬트 애자일 (Cargo Cult Agile):
세리머니(스탠드업, 회고)만 실시
애자일 가치/원칙 이해 없음

4. 스네일 (Snail):
스프린트 길이만 짧아진 워터폴
스프린트 종료 후 통합 테스트 없음

5. 계획 드리븐 스크럼:
6개월치 스프린트 백로그 미리 고정
우선순위 변경 불가 (스폰서 압박)

공통점:
피드백 루프(Feedback Loop)가 막힘
팀이 학습하고 적응할 기회 없음
```

> 📢 **섹션 요약 비유**: [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/) 서적을 읽고 일일 스탠드업만 시작한 팀 — "어제 뭐 했어요" 물어보지만, 목표 달성 여부는 6개월 후에야 알 수 있음.

---

## III. 조직 장벽



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">워터스크럼폴을 만드는 조직 구조:</div>
<div class="kb-diagram-note">사일로 구조:</div>
<div class="kb-diagram-note">기획팀 -&gt; 개발팀 -&gt; QA팀 -&gt; 운영팀</div>
<div class="kb-diagram-note">팀 간 핸드오프(Handoff) 발생</div>
<div class="kb-diagram-note">각 팀 KPI가 다름:</div>
<div class="kb-diagram-note">기획: PRD 완성도</div>
<div class="kb-diagram-note">개발: 스프린트 벨로시티</div>
<div class="kb-diagram-note">QA: 버그 발견율</div>
<div class="kb-diagram-note">운영: SLA 준수율</div>
<div class="kb-diagram-tree-item" style="--depth:0">팀 간 최적화 (전체 최적화 실패)</div>
<div class="kb-diagram-note">계약 관계:</div>
<div class="kb-diagram-note">SI 프로젝트: 요구사항이 계약서에 명시</div>
<div class="kb-diagram-note">변경은 추가 비용 -&gt; 변경 저항</div>
<div class="kb-diagram-note">보안/컴플라이언스 병목:</div>
<div class="kb-diagram-note">모든 변경을 6개월마다 일괄 보안 검토</div>
<div class="kb-diagram-tree-item" style="--depth:0">지속적 배포 불가</div>
<div class="kb-diagram-note">해결: 진정한 교차 기능팀(Cross-Functional Team)</div>
<div class="kb-diagram-note">한 팀 안에: 기획 + 개발 + QA + 운영</div>
<div class="kb-diagram-note">팀 KPI: 비즈니스 결과 (고객 전환율 등)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 릴레이 경주([사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/))를 팀 구기 종목(교차 기능팀)으로 바꾸기 — 공 하나를 여러 포지션이 협력해서 같이 골 넣기.

---

## [IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). 진정한 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 전환 요건



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">기술적 요건:</div>
<div class="kb-diagram-note">CI/CD 파이프라인:</div>
<div class="kb-diagram-note">코드 커밋 -&gt; 자동 빌드/테스트 -&gt; 배포</div>
<div class="kb-diagram-note">배포 주기: 일 단위 또는 즉시</div>
<div class="kb-diagram-note">Feature Flag (피처 플래그):</div>
<div class="kb-diagram-note">기능을 배포하지만 특정 사용자에게만 활성화</div>
<div class="kb-diagram-note">점진적 롤아웃 가능</div>
<div class="kb-diagram-note">자동화 테스트:</div>
<div class="kb-diagram-note">Unit 80%+ 커버리지</div>
<div class="kb-diagram-note">통합 테스트, E2E 자동화</div>
<div class="kb-diagram-note">조직적 요건:</div>
<div class="kb-diagram-note">팀 자율성: 팀이 배포 결정 가능</div>
<div class="kb-diagram-note">심리적 안전: 실험/실패 허용</div>
<div class="kb-diagram-note">DevOps 문화: 개발자가 운영 책임</div>
<div class="kb-diagram-note">측정:</div>
<div class="kb-diagram-note">DORA 4 Key Metrics:</div>
<div class="kb-diagram-tree-item" style="--depth:0">Deployment Frequency (배포 빈도)</div>
<div class="kb-diagram-tree-item" style="--depth:0">Lead Time for Changes</div>
<div class="kb-diagram-tree-item" style="--depth:0">Change Failure Rate</div>
<div class="kb-diagram-tree-item" style="--depth:0">MTTR (Mean Time to Recovery)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 진짜 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)은 세리머니가 아니라 "고객에게 가치를 얼마나 빠르게 전달하는가"를 측정할 수 있어야 함.

---

## V. 실무 시나리오 — 전환 진단과 처방



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">증상 진단:</div>
<div class="kb-diagram-tree-item" style="--depth:0">스프린트를 하고 있지만 분기별 1회 배포</div>
<div class="kb-diagram-tree-item" style="--depth:0">일일 스탠드업은 있지만 목표 달성률 불투명</div>
<div class="kb-diagram-tree-item" style="--depth:0">"기획 변경은 다음 분기에"라는 말이 자주 나옴</div>
<div class="kb-diagram-tree-item" style="--depth:0">워터스크럼폴 진단</div>
<div class="kb-diagram-note">처방 단계:</div>
<div class="kb-diagram-note">단계 1: CI/CD 구축 (1~2개월)</div>
<div class="kb-diagram-note">GitHub Actions로 자동 배포 파이프라인</div>
<div class="kb-diagram-note">Staging 환경 자동 배포 먼저</div>
<div class="kb-diagram-note">단계 2: 배포 주기 단축 (3~6개월)</div>
<div class="kb-diagram-note">분기 -&gt; 월 -&gt; 격주 -&gt; 주간</div>
<div class="kb-diagram-note">Feature Flag 도입</div>
<div class="kb-diagram-note">단계 3: 팀 구조 변경 (6~12개월)</div>
<div class="kb-diagram-note">QA 팀원을 개발 팀에 임베딩</div>
<div class="kb-diagram-note">운영자를 개발 팀에 SRE로</div>
<div class="kb-diagram-note">기획자를 팀 내 Product Owner로</div>
<div class="kb-diagram-note">6개월 후 DORA 지표:</div>
<div class="kb-diagram-note">배포 빈도: 분기 1회 -&gt; 주 3회</div>
<div class="kb-diagram-note">변경 리드타임: 3개월 -&gt; 2주</div>
<div class="kb-diagram-note">변경 실패율: 15% -&gt; 5%</div>
<div class="kb-diagram-note">MTTR: 4시간 -&gt; 30분</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 워터스크럼폴 탈출은 운동 시작하기처럼 작은 것부터 — 스탠드업 다음은 자동 배포, 그 다음은 팀 구조 재편.

---

## 📌 관련 개념 맵

```
워터스크럼폴 (안티패턴)
+-- 구조
| +-- 기획 워터폴 + 개발 스크럼 + 배포 워터폴
+-- 원인
| +-- 사일로 조직 구조
| +-- 계약 기반 요구사항 고정
+-- 해결
| +-- CI/CD (기술적 요건)
| +-- 교차 기능팀 (조직적 요건)
+-- 측정
+-- DORA 4 Key Metrics
+-- 배포 빈도, 리드타임, 변경 실패율
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[애자일 선언 (2001)]
12개 원칙 정의
|
v
[스크럼 대중화 (2003~2010)]
워터스크럼폴 안티패턴 등장
|
v
[SAFe/LeSS (2011~)]
대규모 애자일 프레임워크
|
v
[DevOps 운동 (2009~)]
CI/CD로 배포 장벽 제거
DORA 연구 (2013~)
|
v
[현재: Platform Engineering]
내부 개발자 플랫폼(IDP)으로
조직 장벽 기술적으로 극복
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 워터스크럼폴은 요리 재료 구매는 6개월 계획으로, 실제 요리만 매일 한다는 이름 붙인 것처럼 — 겉만 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)이고 속은 워터폴인 패턴이에요.
2. 진짜 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)은 계획부터 배포까지 전체 흐름이 빨라야 하며, 2주마다 실제 고객이 사용할 수 있는 기능을 배포할 수 있어야 해요.
3. [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 4가지 지표(배포 빈도, 리드타임, 실패율, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)시간)가 낮으면 워터스크럼폴 진단을 의심하고 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD와 팀 구조를 바꿔야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 38 / 373

← **이전**: [037. 애자일 PMO (Agile PMO)](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/037_agile_pmo/)
**다음**: [039. 피처 플래그 (Feature Flag / Feature Toggle)](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/039_feature_flag/) →

---
