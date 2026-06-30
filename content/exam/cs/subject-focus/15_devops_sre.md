---
title: "DevOps SRE 핵심 트랙"
date: "2026-06-29"
tags:
  - "exam-cspe-devops-sre"
  - "exam-cspe-track"
weight: 91
---

## 컴퓨터시스템응용기술사 핵심 트랙

- 기준: 컴퓨터시스템응용기술사 관점만 반영
- 과목 총 노트 수: 400개
- 과목 필요성:
  - 데브옵스(DevOps)와 사이트 신뢰성 엔지니어링(Site Reliability Engineering, SRE)은 현대 시스템 운영의 표준 방법론으로, 배포 속도와 안정성의 균형을 설명하는 핵심 과목이다.
  - 기술사는 도구명 나열보다 지속적 통합·지속적 배포(Continuous Integration/Continuous Delivery, CI/CD), 코드형 인프라(Infrastructure as Code, IaC), 관측성(Observability), 보안 자동화의 연결 구조를 본다.
  - 특히 서비스 장애, 변경 실패율, 복구 시간, 에러 버짓(Error Budget), 운영 조직모델을 함께 설명할 수 있어야 실제 시스템 아키텍트 관점의 답안이 된다.
  - 플랫폼 엔지니어링과 AIOps까지 연결되면서 최근 출제 포인트가 "운영 자동화의 수준"과 "개발자 경험"으로 확장되고 있다.
- 우선 학습 챕터:
  - `01_culture_methodology`
  - `02_cicd_gitops`
  - `03_sre_observability`
  - `04_iac_cloud_native`
  - `05_devsecops`
- 추천 핵심 키워드 목표 수: 100개
- 단답형 포인트:
  - CI/CD, GitOps, IaC, SLI(Service Level Indicator), SLO(Service Level Objective), SLA(Service Level Agreement), MTTR(Mean Time To Recovery) 정의 정리
  - Canary, Blue-Green, Rolling Update, SBOM(Software Bill of Materials), SAST(Static Application Security Testing), DAST(Dynamic Application Security Testing) 구분
  - Trace, Metric, Log, Error Budget, Toil, Blameless Postmortem 개념을 짧게 말할 수 있어야 함
- 서술형 포인트:
  - 배포 자동화 체계, GitOps 운영모델, SRE 지표 체계, DevSecOps 통합 전략을 구조도형 답안으로 전개
  - 장애 예방-탐지-복구-회고의 전 주기를 설명하고, 조직 문화와 운영지표를 함께 묶어야 함
  - 안정성, 속도, 보안, 비용, 인지부하(Cognitive Load) 간 트레이드오프를 판단하는 문제가 핵심
- 최신 기술 동향 연결:
  - 플랫폼 엔지니어링: 내부 개발자 플랫폼(IDP), 골든 패스(Golden Path), 셀프서비스 배포 체계와 연결
  - 클라우드 네이티브: 쿠버네티스 기반 GitOps, 정책형 코드(Policy as Code), 서비스 메시 보안으로 확장
  - AIOps: 이상 탐지, 근본원인 분석, 자동 롤백, 자동 스케일링과 연계
  - 데이터 파이프라인: 배포 파이프라인과 데이터 품질 검증 파이프라인의 결합 관점 정리
  - 레이크하우스: DataOps, MLOps와 DevSecOps 교차 지점에서 플랫폼 운영 범위 확대
