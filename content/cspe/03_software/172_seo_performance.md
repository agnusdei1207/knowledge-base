---
title: 검색 엔진 최적화 SEO 및 웹 성능 (SEO and Performance)
date: 2026-07-05
tags: ["cspe-software"]
weight: 172
---

## Ⅰ. 개요
- 정의: 웹사이트가 검색 결과 상위에 노출되도록 최적화하고 사용자 체감 성능을 향상시키는 활동
- 배경: 검색 노출 확대와 페이지 이용 중 이탈 감소를 위한 지표 관리
| 구분 | 내용 |
|------|------|
| 출제 의도 | Core Web Vitals(LCP, FID, CLS) 지표와 기술적 SEO(Metadata, Sitemap) 이해 |

## Ⅱ. 구성요소
  [ SEO: Content/Meta ] + [ Perf: Speed/Stability ]
  -> Better Search Ranking
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Web Vitals | 로딩 속도, 인터랙션, 시각적 안정성 지표 | 건강 검진 |
| Sitemap | 검색 로봇에게 사이트 구조 제공 파일 | 지도 |
| Robots.txt | 크롤링 허용/차단 범위 지정 | 출입 통제 |
> 요약: 색인 가능한 콘텐츠 구조와 로딩·상호작용·화면 안정성 지표를 함께 관리함

## Ⅲ. 절차
  Audit -> Measure -> Optimize -> Monitor
1. Auditing: Lighthouse 등을 사용한 현재 성능 및 SEO 진단
2. Technical SEO: 시맨틱 태그 적용 및 메타데이터 최적화
3. Performance Fix: 이미지 압축, 리소스 우선순위 지정
4. Validation: 검색 엔진 색인 여부 및 지표 변화 확인
> 요약: 검색 색인과 웹 성능을 측정하고 변경 전후 지표로 개선 효과를 검증함

## Ⅳ. 문제점
- 클라이언트 사이드 렌더링(CSR) 시 검색 엔진 크롤링 한계
- 대용량 리소스 및 복잡한 JS 실행으로 인한 페이지 로드 지연

## Ⅴ. 개선방안
- SSR(Server Side Rendering) 적용 및 미리 렌더링(Prerendering)
- 이미지 WebP 변환, 가상화(Virtualization), CDN 엣지 활용

## Ⅵ. 전망
- AI 검색(SGE) 대응을 위한 정교한 스키마 마크업 및 사용자 경험 지표 중심 평가 강화
