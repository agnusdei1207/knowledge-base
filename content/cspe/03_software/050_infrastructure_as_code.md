---
title: 코드형 인프라 IaC — Terraform (Infrastructure as Code)
date: 2026-07-05
tags: ["cspe-software"]
weight: 50
---

## Ⅰ. 개요
- 정의: 인프라를 수동 구성 대신 프로그래밍 언어나 선언적 코드로 정의하고 관리하는 기술.
- 출제 의도: 인프라 구성의 재현성, 버전 관리, 자동화 역량 및 Terraform의 핵심 메커니즘 이해도 평가.

## Ⅱ. 구성요소
- ASCII 구조도
  [ Terraform Code (.tf) ] ----> [ Terraform Engine ] ----> [ State File ]
  (Resource Definition)    |    (Plan / Apply)       |    (Current Status)
                           v                         v
                   [ Provider (AWS, Azure) ] <-> [ Real Infra ]
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| HCL (언어) | Terraform에서 사용하는 인간 친화적 선언형 구성 언어 | 인프라 설계 도면 |
| State File | 현재 인프라 상태를 기록한 JSON 파일로 동기화의 기준 | 건물 현황 대장 |
| Provider | 클라우드 서비스 API와 연결해주는 플러그인 | 통역 및 대행사 |
> 요약: 코드로 선언하면 엔진이 실제 인프라와 상태를 비교하여 변경사항만 반영함.

## Ⅲ. 절차
- ASCII 흐름도
  [Init] -> [Plan] -> [Apply] -> [State Update]
- 4단계 설명
1. `terraform init`으로 필요한 공급자(Provider) 플러그인 다운로드함.
2. `terraform plan` 실행하여 코드가 실제 환경에 미칠 영향을 사전 시뮬레이션함.
3. `terraform apply`로 실제 인프라 자원을 생성, 수정, 삭제함.
4. 작업 완료 후 최신 상태를 `terraform.tfstate` 파일에 영구 저장함.
> 요약: 코드와 실제 인프라 간의 '멱등성(Idempotency)'을 유지하는 과정임.

## Ⅳ. 문제점
- 상태 파일 충돌: 협업 시 여러 작업자가 동시에 상태 파일을 수정하여 데이터 손상 가능함.
- 구성 드리프트: 수동으로 인프라 조작 시 코드와 실제 환경 간의 불일치 발생함.

## Ⅴ. 개선방안
- Remote State Locking: S3/DynamoDB 등을 활용해 원격 저장 및 동시 수정 방지(Locking)함.
- Drift Detection: 주기적으로 `plan`을 실행하여 코드와 실제 상태 차이를 자동 감지 및 경고함.

## Ⅵ. 전망
- Crossplane 등을 통해 쿠버네티스 API로 인프라를 제어하는 'Control Plane' 방식과 융합됨.
- 보안 코딩(Policy as Code)이 강화되어 배포 전 보안 정책 위반을 코드로 자동 검사함.
- AI가 최적의 인프라 구성을 추천하고 코드를 생성해주는 자동 생성 IaC 기술 고도화될 것임.
