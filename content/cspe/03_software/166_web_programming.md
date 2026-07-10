---
title: 웹 프로그래밍 — HTML5·CSS3·JS (Web Programming)
date: 2026-07-05
tags: ["cspe-software"]
weight: 166
---

## Ⅰ. 개요
- 정의: HTML5, CSS3, JavaScript를 중심으로 한 표준 웹 애플리케이션 개발 기술
- 배경: 멀티 플랫폼 대응 및 플러그인(ActiveX 등) 없는 웹 환경 요구
| 구분 | 내용 |
|------|------|
| 출제 의도 | 시맨틱 웹, 반응형 레이아웃, 동적 인터랙션 기술의 유기적 결합 이해 |

## Ⅱ. 구성요소
  [ Structure: HTML5 ] + [ Design: CSS3 ] + [ Logic: JS ]
  -> Modern Web Experience
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Semantic Tag | 의미 있는 태그(article, section) 사용 | 색인 태그 |
| Flex/Grid | 반응형 레이아웃을 위한 배치 기술 | 격자 가이드 |
| ES6+ | module·class·promise·async function 등 JavaScript language 기능 | script 실행·모듈 경계 |
> 요약: HTML은 document structure, CSS는 presentation, JavaScript는 event·state·network 동작을 담당하며 Web API로 연결됨

## Ⅲ. 절차
  Request -> DOM/CSSOM -> Render Tree -> Layout/Paint
1. Parsing: HTML 문자열을 객체 모델(DOM)로 변환
2. Styling: CSS를 해석하여 스타일 규칙(CSSOM) 생성
3. Attachment: DOM과 CSSOM을 결합하여 렌더 트리 구성
4. Painting: 화면의 각 픽셀에 요소의 색상과 형태 출력
> 요약: browser는 HTML·CSS를 DOM·CSSOM으로 구성하고 style·layout·paint·composite 단계로 화면을 갱신함

## Ⅳ. 문제점
- 브라우저별 지원 사양 차이로 인한 크로스 브라우징 이슈
- 콘텐츠 복잡도 증가에 따른 초기 로딩 속도 및 렌더링 성능 저하

## Ⅴ. 개선방안
- Polyfill 및 Transpiler(Babel) 활용으로 호환성 확보
- 이미지 최적화, Lazy Loading, CDN 활용을 통한 성능 개선

## Ⅵ. 전망
- WebGPU 기반 고성능 그래픽 구현 및 웹 표준 기반 메타버스/몰입형 웹 환경 확산
