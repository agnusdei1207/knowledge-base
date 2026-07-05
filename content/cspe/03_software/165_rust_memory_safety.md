---
title: 러스트 Rust 언어 및 메모리 안전성 (Rust Memory Safety)
date: 2026-07-05
tags: ["cspe-software"]
weight: 165
---

## Ⅰ. 개요
- 정의: 소유권(Ownership) 개념을 통해 GC 없이 컴파일 타임에 메모리 안전성을 보장하는 언어
- 배경: C++의 성능과 높은 안전성을 동시에 요구하는 시스템 프로그래밍 트렌드
| 구분 | 내용 |
|------|------|
| 출제 의도 | Ownership, Borrowing, Lifetime 규칙을 통한 데이터 레이스 및 메모리 오류 제거 원리 |

## Ⅱ. 구성요소
  Variable A --(Owns)--> Memory
  Variable B --(Borrows)--> A (Reference)
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Ownership | 변수가 메모리 해제의 유일한 책임을 가짐 | 소유권 증서 |
| Borrowing | 소유권을 넘기지 않고 참조만 허용(mutable/immutable) | 대여 |
| Borrow Checker | 컴파일 시 메모리 규칙 위반 여부 검사 | 검문소 |
> 요약: 엄격한 컴파일 규칙을 통한 런타임 오버헤드 없는 안전성 확보

## Ⅲ. 절차
  Define -> Move/Borrow -> Compile Check -> Zero-cost Free
1. Define: 변수 선언 시 해당 데이터의 소유자 확정
2. Move/Borrow: 소유권 이전 또는 읽기/쓰기 권한 대여
3. Borrow Check: 대여 기간과 소유권 생명주기 일치 확인
4. Drop: 스코프 종료 시 소유자가 자동으로 메모리 해제
> 요약: 컴파일 단계에서의 철저한 검증을 통한 런타임 오류 원천 차단

## Ⅳ. 문제점
- 학습 곡선(Learning Curve)이 높고 엄격한 규칙으로 개발 속도 저하
- 기존 C/C++ 라이브러리와의 상호 운용(FFI) 시 unsafe 블록 관리 부담

## Ⅴ. 개선방안
- 풍부한 패키지 매니저(Cargo) 및 커뮤니티 문서 기반 학습 지원 강화
- 점진적인 모듈 단위 교체 및 Safe Wrapper 레이어 구축

## Ⅵ. 전망
- 리눅스 커널 공식 채택을 기점으로 임베디드, 클라우드 인프라 보안의 핵심 언어로 부상
