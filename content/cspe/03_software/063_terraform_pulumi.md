---
title: "Terraform Pulumi (Terraform Pulumi)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 63
---

## Ⅰ. 개요
- **정의**: 인프라를 코드로 프로비저닝하는 대표적 IaC 도구로, Terraform은 HCL 기반 선언형, Pulumi는 범용 언어 기반 프로비저닝 도구임
- **배경/필요성**: IaC(062 참조) 개념을 실현하려면 상태 관리·멱등성·다중 프로바이더를 지원하는 전용 도구가 필요함
- **비유**: Terraform은 전용 설계도 양식, Pulumi는 자유 형식 스케치 — 둘 다 같은 건물을 짓지만 표현 방식이 다름

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 두 도구의 접근 방식 차이 비교 | DSL vs GPL, State 관리 방식 | 구성관리 도구(Ansible 등)와 혼동 금지 |

> 요약: IaC를 구현하는 두 축으로, 선언 언어 vs 범용 언어 접근의 차이를 이해해야 함

## Ⅱ. 구성요소
```text
Terraform: HCL File --> terraform CLI --> Provider --> Cloud Resource
                              |
                              v
                         State File (.tfstate)

Pulumi:    TS/Python --> pulumi CLI --> Provider --> Cloud Resource
                              |
                              v
                         Pulumi State (Backend)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 언어/DSL | Terraform은 HCL, Pulumi는 TypeScript·Python 등 범용 언어 사용 | 전용 양식 vs 자유 노트 |
| CLI 엔진 | `plan`/`up` 명령으로 Diff 계산 후 프로바이더 API를 호출함 | 시공 현장 감독 |
| Provider | AWS·Azure·GCP 등 클라우드 자원 CRUD를 추상화한 플러그인 | 자재 공급사 |
| State | 현재 인프라 상태를 기록하여 변경분만 계산하는 저장소 | 준공 대장 |

> 요약: 언어-CLI-프로바이더-상태저장소의 4요소로 인프라를 코드 기반 관리함

## Ⅲ. 절차
```text
Write Code --> Preview/Plan --> Apply/Up --> Destroy(optional)
```
- 1단계: HCL 또는 범용 언어로 인프라 자원을 정의함
- 2단계: `terraform plan` / `pulumi preview`로 변경 사항을 사전 확인함
- 3단계: `terraform apply` / `pulumi up`으로 실제 인프라에 반영함
- 4단계: 검증 후 불필요 자원은 `destroy`로 정리함

> 요약: 정의-미리보기-적용-정리의 4단계로 인프라 라이프사이클을 관리함

## Ⅳ. 문제점
- 학습 곡선 차이: Terraform은 HCL 별도 학습, Pulumi는 SDK 체계 이해가 각각 필요함
- 상태 파일 관리 부담: 원격 백엔드 미설정 시 상태 유실·충돌 위험이 있음
- 대규모 모듈 관리: 수백 개 모듈 간 의존성이 복잡해지면 Plan 시간이 증가함

> 요약: 학습 곡선, 상태 관리, 모듈 복잡성이 주요 과제임

## Ⅴ. 개선방안
1. 단기: 팀 표준 언어·도구를 선정하고 공통 모듈 템플릿을 제공함
2. 중기: 원격 백엔드(S3+DynamoDB, Pulumi Cloud)와 상태 잠금을 의무화함
3. 장기: 모듈 레지스트리·모노레포 전략으로 의존성을 체계적으로 관리함

> 요약: 표준화, 원격 상태 관리, 모듈 레지스트리로 개선함

## Ⅵ. 전망
- 발전 방향: CDKTF(CDK for Terraform) 등 범용 언어 지원이 확대되어 두 도구의 경계가 수렴함
- 기술사적 판단: 프로비저닝 도구 선택은 팀 역량·기존 코드베이스에 따라 결정할 사안임
- 기술사 제언: 도구 자체보다 모듈 설계·상태 관리 전략 수립이 우선임
