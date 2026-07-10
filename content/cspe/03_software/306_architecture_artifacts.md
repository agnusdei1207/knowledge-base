---
title: 소프트웨어 아키텍처 산출물 (Architecture Artifacts)
date: 2026-07-05
tags: [cspe-software]
weight: 306
---

## Ⅰ. 개요
- 정의: 아키텍처 설계 과정과 결과물을 이해관계자에게 전달하기 위해 문서화한 자산임
- 배경: 설계 결정의 근거와 구조·인터페이스·구현 간 추적 관계를 개발·운영팀이 공유할 필요
- 출제 의도: 주요 아키텍처 뷰(View) 및 기술 문서의 종류와 역할 이해도 확인

## Ⅱ. 구성요소
- ASCII 구조도
  [Reqs] -> [Architecture Design Document (ADD)] -> [Implementation]
               |-- Logical/Physical View
               |-- Interface Spec
               |-- Decision Records (ADR)
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| SAD | 전체 구조와 원칙을 담은 기술 문서 | 건축 설계 도서 |
| ADR | 의사결정 배경, 대안, 결과 및 사유 기록 | 회의록/판례 |
| 인터페이스 명세 | 시스템/컴포넌트 간 상호작용 규약 문서 | 규격 명세서 |
> 요약: 구조(SAD), 결정(ADR), 규약(Spec) 등을 체계적으로 기록한 문서 집합임

## Ⅲ. 절차
- ASCII 흐름도
  Template Set -> Content Fill -> Review -> Baseline
- 4단계 설명
1. Template Set: IEEE 1471 등 표준 규격을 기반으로 문서 구조 정의함
2. Content Fill: 각 뷰(View)별 다이어그램 및 설계 원칙, 제약 사항 기술함
3. Review: 이해관계자 간의 교차 검토를 통해 산출물의 정확성 검증함
4. Baseline: 승인된 산출물을 형상 관리 도구에 등록하여 버전 관리함
> 요약: 표준 템플릿에 따라 내용을 작성하고 검토를 거쳐 공식 문서로 확정함

## Ⅳ. 문제점
- 구현 변경이 SAD·ADR·인터페이스 명세에 반영되지 않으면 문서의 구조와 실제 동작이 달라짐

## Ⅴ. 개선방안
- Docs as Code와 CI 검사를 적용하고 코드·API·IaC에서 생성 가능한 구조 정보는 자동 갱신함

## Ⅵ. 전망
- 실시간 아키텍처 가시화 도구와 연동된 동적 산출물 관리 체계 도입
- CSF: 문서 양보다는 내용의 정확성과 최신성 유지(Up-to-date)가 프로젝트 성공의 열쇠임
