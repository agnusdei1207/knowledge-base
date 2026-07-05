---
title: 웹 어셈블리 WebAssembly (WebAssembly)
date: 2026-07-05
tags: ["cspe-software"]
weight: 169
---

## Ⅰ. 개요
- 정의: 웹 브라우저에서 네이티브에 가까운 속도로 실행되는 저수준 이진 형식 코드
- 배경: 복잡한 연산(게임, 영상 편집 등)을 웹에서 처리하기 위한 성능 한계 극복
| 구분 | 내용 |
|------|------|
| 출제 의도 | C/C++/Rust 코드를 웹에서 실행하는 방식과 JS와의 상호 운용성 이해 |

## Ⅱ. 구성요소
  [ C/Rust Code ] -> [ Emscripten/Wasm ] -> [ Browser VM ]
  (Fast Execution Area)
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Module | Wasm 바이너리 코드 단위 | 기계 뭉치 |
| Memory | JS와 공유 가능한 가변 길이 바이트 배열 | 공유 창고 |
| Table | 함수 참조를 안전하게 저장하는 배열 | 인덱스 카드 |
> 요약: 플랫폼 독립적인 고성능 실행 환경 및 샌드박스 보안 모델

## Ⅲ. 절차
  Compile -> Fetch -> Instantiate -> Call Function
1. Compile: 소스 코드를 .wasm 바이너리로 컴파일
2. Fetching: 브라우저에서 바이너리 데이터를 스트리밍 로드
3. Instantiation: 메모리 및 임포트 객체와 결합하여 인스턴스 생성
4. Execution: JS에서 Wasm 함수를 호출하거나 연산 수행
> 요약: 컴파일된 바이너리를 브라우저 VM에서 직접 실행하여 성능 극대화

## Ⅳ. 문제점
- 직접적인 DOM 접근 불가로 JS와의 빈번한 데이터 교환 오버헤드
- 디버깅의 어려움 및 바이너리 형식에 따른 가독성 저하

## Ⅴ. 개선방안
- Interface Types 표준화를 통한 복합 데이터 구조 통신 개선
- Source Map 지원 확대 및 Wasm 전용 디버깅 툴 도입

## Ⅵ. 전망
- 서버리스(Serverless) 런타임으로서의 Wasm 활용 및 브라우저 기반 고사양 SaaS 시장 폭발적 성장
