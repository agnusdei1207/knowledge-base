---
title: 데이터 무결성 제약 조건 (Data Integrity)
date: 2026-07-05
tags: ["cspe-software"]
weight: 178
---

## Ⅰ. 개요
- 정의: 저장된 데이터의 정확성, 일관성, 유효성을 유지하기 위한 제약 조건 및 관리 기술
- 배경: 데이터베이스의 신뢰성 확보 및 잘못된 데이터 입력 원천 차단
| 구분 | 내용 |
|------|------|
| 출제 의도 | 개체, 참조, 도메인, 사용자 정의 무결성의 의미와 구현 방법 이해 |

## Ⅱ. 구성요소
  [ Data Input ] -> [ Constraint Check ] -> [ Storage ]
  (Integrity Barrier)
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Entity Integrity | PK는 NULL 불가, 중복 불가 (식별 보장) | 주민번호 |
| Referential | FK는 참조하는 PK 값과 일치해야 함 (관계 보장) | 연결 고리 |
| Domain | 컬럼의 데이터 타입, 범위, 기본값 정의 (값 보장) | 규격 |
> 요약: 논리적 규칙 설정을 통한 데이터 품질의 자기 방어 체계

## Ⅲ. 절차
  Modify -> Verify Constraint -> Transaction -> Result
1. Triggering: 데이터 입력(INSERT) 또는 수정 요청 발생
2. Validation: 설정된 PK/FK/Check 제약 조건 위반 여부 확인
3. Enforcement: 위반 시 트랜잭션 중단(Rollback) 및 에러 반환
4. Commit: 모든 무결성 조건 만족 시 물리 디스크 저장
> 요약: 엄격한 규칙 검사를 통한 데이터 오염 방지 및 신뢰도 유지

## Ⅳ. 문제점
- 복잡한 제약 조건 설정 시 대량 데이터 처리 성능 저하
- 분산 DB 환경에서 노드 간 참조 무결성 유지의 어려움

## Ⅴ. 개선방안
- Batch 작업 시 제약 조건 일시 비활성화 후 벌크 로드
- 애플리케이션 레이어의 검증 로직과 DB 제약의 이중 방어

## Ⅵ. 전망
- 데이터 패브릭(Data Fabric) 기반 자동 품질 진단 및 AI를 이용한 이상 데이터 무결성 탐지
