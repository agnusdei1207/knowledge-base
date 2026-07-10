---
title: 클라우드 기반 아키텍처 설계 (Cloud Architecture)
date: 2026-07-05
tags: [cspe-software]
weight: 310
---

## Ⅰ. 개요
- 정의: 클라우드의 가상 자원·관리형 서비스·자동화 API를 이용해 배포·확장·복구·비용을 관리하는 시스템 구조임
- 배경: 인프라의 가상화 및 종량제 모델 도입으로 인한 자원 관리 패러다임 변화 대응
- 출제 의도: 클라우드 네이티브 원칙(CNA) 및 관리형 서비스(SaaS/PaaS) 활용 능력 평가

## Ⅱ. 구성요소
- ASCII 구조도
  [User] -> [CDN/LB] -> [Auto-Scaling Group] -> [Managed DB]
               |               |                   |
          (Global)         (Elastic)           (Serverless)
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| 탄력성(Elasticity)| 부하에 따라 자원이 자동으로 증감하는 특성 | 고무줄 |
| 비상태성(Stateless)| 로컬 자원에 의존하지 않아 확장이 용이한 구조 | 렌터카 |
| 마이크로서비스 | 기능을 독립적 서비스 단위로 쪼개어 배포함 | 레고 블록 |
> 요약: 인프라를 코드화(IaC)하고 서비스 단위로 분산하여 가용성과 유연성을 높임

## Ⅲ. 절차
- ASCII 흐름도
  Requirement -> Service Select -> Security Design -> Cost Opt
- 4단계 설명
1. Requirement: 클라우드 이전 목표(Lift & Shift vs Re-platform) 설정함
2. Service Select: 컴퓨팅(EC2, Lambda), 스토리지, 네트워크 서비스 선정함
3. Security Design: IAM 권한 관리 및 VPC 분리 등 클라우드 보안 계층 설계함
4. Cost Opt: 예약 인스턴스(RI) 및 미사용 자원 정리로 비용 효율화함
> 요약: 이전 목표와 품질 요구에 따라 서비스를 선택하고 IAM·네트워크·용량·비용 정책을 구성함

## Ⅳ. 문제점
- 벤더 전용 API와 데이터 형식은 이전 비용을 높이고, 사용량·전송량을 추적하지 않으면 예산을 초과할 수 있음

## Ⅴ. 개선방안
- 전환 가능성이 필요한 계층은 표준 인터페이스로 분리하고 FinOps로 서비스·태그별 비용과 예산 편차를 관리함

## Ⅵ. 전망
- 하이브리드/멀티 클라우드 환경의 일관된 관리를 위한 서비스 메쉬 통합
- CSF: 클라우드 공유 책임 모델(Shared Responsibility Model)에 대한 명확한 이해가 필수임
