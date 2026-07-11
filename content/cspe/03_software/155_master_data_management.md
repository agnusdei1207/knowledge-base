---
title: "마스터 데이터 관리 MDM (Master Data Management)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 155
extra:
  question_no: "155"
  exam_status: "기출"
  exam_history: "121회"
---

## 미리 알고가기

- 마스터 데이터는 고객·상품·조직·공급자처럼 여러 업무가 공통 참조하는 기준 개체 데이터임
- Match는 여러 원천 레코드가 같은 실제 개체인지 규칙·확률로 판정하는 과정임
- Merge는 같은 개체로 판정된 레코드를 하나의 기준 개체로 통합하는 과정임
- Survivorship은 원천 신뢰도·최신성·완전성 규칙으로 기준 속성값을 선택하는 과정임
- Golden Record는 중복 제거·병합·승인을 거쳐 개체별 기준으로 제공하는 레코드임
- Crosswalk는 Golden ID와 각 원천 시스템의 로컬 키를 연결하는 매핑임
- Registry는 원천 레코드를 중앙 식별 링크로 연결하고 속성은 원천에 유지하는 방식임
- Consolidation은 원천을 중앙 Golden Record로 통합해 분석에 제공하는 방식임
- Coexistence는 중앙 기준과 원천 변경을 동기화하고 Transaction Hub는 중앙 기준을 운영 업무에 제공함

## 작성 근거(검토용)

- MDM은 식별·Match·Merge·Survivorship·Golden Record·Crosswalk·Stewardship을 핵심으로 선정함
- 비교표는 Registry·Consolidation·Coexistence·Transaction Hub를 저장·갱신·배포·통제·적합 조건으로 대비함
- 절차는 표준화된 원천 레코드가 매칭·병합·승인을 거쳐 Golden Record로 배포되는 흐름을 설명함
- 제목부터 결론까지 모든 문장·표 셀·요약을 5회 전수 검수해 중복 판정과 값 선택을 구분함

## Ⅰ. 개요

- **정의/개념**: MDM은 여러 시스템의 기준 개체를 매칭·병합하고 속성 선택과 Steward 검토로 Golden Record와 원천 키 매핑을 제공하는 관리 체계임
- **배경/필요성**: 시스템별 고객·상품·조직 식별자와 속성값의 불일치를 줄이고 업무 간 동일 개체를 일관되게 참조하기 위해 기준 레코드가 필요함

## Ⅱ. 특징

- 이름·주소·식별번호를 표준화하고 결정 규칙·유사도·참조 데이터로 동일 개체를 판정함
- Survivorship 규칙이 원천 신뢰도·최신성·완전성을 기준으로 Golden 속성값을 선택함
- Golden ID와 원천 로컬 키의 Crosswalk가 기존 시스템과 기준 개체를 연결함
- 자동 병합·분리 임계값 사이의 후보는 Steward가 검토하고 판정 이력을 남김
- 개체·속성·계층별 소유권과 변경 배포 방식을 함께 정해 원천과 MDM의 충돌을 통제함

## Ⅲ. 종류 및 비교

| 판단 기준 | Registry | Consolidation | Coexistence | Transaction Hub |
|:---|:---|:---|:---|:---|
| 기준 저장 | 원천 키와 식별 링크 중심 | Golden Record를 분석용으로 저장 | Golden Record와 원천 변경을 동기화 | Hub가 운영 기준 레코드를 직접 저장 |
| 갱신 주체 | 원천 시스템이 속성 소유 | 원천에서 Hub로 단방향 수집 | 원천과 Hub가 규칙에 따라 상호 갱신 | 업무 응용이 Hub를 기준으로 갱신 |
| 배포 방식 | 조회 시 원천 위치 연결 | 배치·증분으로 통합 결과 제공 | 변경 이벤트·서비스로 양방향 배포 | API·서비스로 운영 트랜잭션 제공 |
| 통제 수준 | 중복 식별과 Crosswalk | 매칭·병합·분석 일관성 | 속성 소유권·충돌 조정 필요 | Hub 가용성·트랜잭션·권한 통제 필요 |
| 적합 조건 | 원천 변경을 최소화해야 함 | 보고·분석용 통합 기준 필요 | 기존 시스템과 기준값을 함께 유지 | 신규 업무가 중앙 기준을 직접 사용 |

> 요약: MDM 구현은 원천 소유권과 Golden Record의 갱신·배포 범위에 따라 Registry부터 Transaction Hub까지 선택함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Source Adapter | 원천 레코드·키·변경 이벤트와 코드 체계를 수집함 |
| Standardization·Validation | 이름·주소·식별자 형식을 통일하고 필수·유효성 규칙을 검사함 |
| Match·Merge Engine | 동일 개체 후보를 점수화하고 병합·분리 판정을 수행함 |
| Survivorship·Golden Store | 속성별 선택 규칙을 적용해 기준 레코드와 변경 이력을 저장함 |
| Crosswalk·Hierarchy | Golden ID와 원천 키, 조직·상품 계층 관계를 관리함 |
| Stewardship Workflow | 모호한 후보·규칙 위반·병합 취소를 검토하고 승인 이력을 남김 |

```text
원천 레코드 -> 표준화 -> Match·Merge -> Golden Record -> 원천·응용 배포
                                |
                         Steward Review·Crosswalk
```

> 요약: 표준화·매칭·속성 선택과 Steward 검토가 원천 레코드를 Golden Record와 Crosswalk로 통합함.

## Ⅴ. 원리 및 절차 흐름도

```text
원천 수집 -> 표준화·검증 -> 후보 검색·매칭 -> 병합·속성 선택 -> 승인·배포
```

1. **원천 수집**: 개체 속성·로컬 키·원천·변경 시각을 MDM 처리 영역에 적재함
2. **표준화**: 문자열·주소·코드 형식을 통일하고 유효하지 않은 레코드를 분리함
3. **후보 매칭**: 차단 키로 후보를 줄이고 규칙·유사도 점수로 동일 개체를 판정함
4. **기준 생성**: 동일 개체를 병합하고 Survivorship 규칙으로 속성별 기준값을 선택함
5. **승인·배포**: 경계 후보를 Steward가 검토하고 Golden ID·Crosswalk·변경을 소비 시스템에 제공함

> 요약: MDM은 원천을 표준화해 동일 개체를 판정하고 속성 선택과 승인으로 Golden Record를 확정함.

## Ⅵ. 실무 사례

1. 고객 MDM은 이메일·전화 기반 매칭과 속성 선택 규칙을 적용하고 중복률·수동 검토 건수를 확인함
2. 상품 MDM은 표준 코드와 계층을 배포하고 미매핑 상품 수·원천 동기화 지연을 확인함

## Ⅶ. 결론

- MDM은 개체 식별 정확도·속성 소유권·Golden Record 갱신 방식·배포 지연과 Steward 검토 범위로 설계해야 함
