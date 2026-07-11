---
title: "컨테이너 보안 — Seccomp·AppArmor·OPA (Container Security)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 180
extra:
  question_no: "180"
  exam_status: "기출"
  exam_history: "121회, 130회, 136회"
---

## 미리 알고가기

- Seccomp는 프로세스가 사용자 공간에서 호출할 수 있는 Linux 시스템 호출을 프로필로 제한함
- AppArmor는 Linux 보안 모듈이 경로 기반 파일·권한·네트워크 접근을 프로필로 제한함
- OPA는 Rego 정책과 입력 데이터를 평가해 허용·거부 결정을 반환하는 정책 엔진임
- OPA Gatekeeper는 Kubernetes AdmissionReview와 정책 CRD·감사 기능을 OPA에 연결함
- Admission Control은 API 객체가 저장되기 전에 생성·수정 요청을 검증하거나 변경함
- Privileged 컨테이너는 Seccomp·AppArmor 제한을 우회하므로 별도 Admission 정책으로 제한해야 함
- 스케줄러는 Localhost 프로필 유무를 알지 못하므로 노드 레이블·selector로 배치 대상을 제한함
- SecurityContext는 Pod·컨테이너의 사용자·권한·Seccomp·AppArmor 설정을 선언함
- RuntimeDefault는 런타임 기본 프로필, Localhost는 노드에 미리 배포한 프로필을 사용함

## 작성 근거(검토용)

- 세 기술은 모두 보안 통제지만 OPA는 배포 전 객체, Seccomp·AppArmor는 실행 중 커널 접근을 통제함
- 통제 시점·입력·대상·판정·실패 결과·의존성을 비교하고 Admission부터 커널 실행까지 연결함
- 제목부터 결론까지 5회 전수 검수하여 정책 검증과 런타임 격리의 역할을 구분함

## Ⅰ. 개요

- **정의/개념**: 컨테이너 보안은 OPA로 배포 객체를 검증하고 Seccomp·AppArmor로 실행 중 커널 접근을 제한하는 계층 통제임
- **배경/필요성**: 공유 커널과 잘못된 Pod 설정이 노드 권한으로 확산되는 범위를 줄이기 위해 배포 전·실행 중 통제가 필요함

## Ⅱ. 특징

- OPA는 이미지 출처·권한·리소스 설정 같은 객체 속성을 API 저장 전에 판정함
- Seccomp는 시스템 호출 번호·인수에 허용·거부 동작을 적용해 커널 진입 범위를 제한함
- AppArmor는 실행 파일별 프로필로 파일 경로·capability·네트워크 작업을 통제함
- 로컬 프로필은 모든 실행 노드에 배포돼야 하며 누락 시 컨테이너 생성이 실패할 수 있음

## Ⅲ. 통제 기술 비교

| 판단 기준 | Seccomp | AppArmor | OPA·Gatekeeper |
|:---|:---|:---|:---|
| 통제 시점 | 컨테이너 프로세스의 시스템 호출 시점 | 컨테이너 프로세스의 자원 접근 시점 | API 객체 생성·수정 Admission 시점 |
| 입력 | 시스템 호출 번호·인수와 프로필 | 실행 파일·경로·권한·네트워크와 프로필 | AdmissionReview 객체·정책·외부 데이터 |
| 통제 대상 | 사용자 공간에서 커널로 진입하는 호출 | 파일·capability·네트워크 등 커널 자원 접근 | 이미지·권한·레이블·리소스 같은 객체 구성 |
| 판정 결과 | 호출 허용·오류 반환·프로세스 종료 | 작업 허용·거부·감사 로그 | 객체 허용·거부와 위반 메시지 |
| 배포 의존성 | 런타임 기본 또는 노드 로컬 프로필 | 노드 커널 모듈과 로드된 프로필 | Admission Webhook·Constraint 정책 |
| 적합 조건 | 불필요한 시스템 호출 제한 | 애플리케이션별 자원 접근 제한 | 클러스터 공통 배포 정책 적용 |

> 요약: OPA는 배포 구성을 검증하고 Seccomp·AppArmor는 실행 중 커널 접근을 제한함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 역할 |
|:---|:---|
| API 서버·Admission Webhook | Pod 요청을 OPA Gatekeeper에 전달하고 판정 결과를 적용함 |
| ConstraintTemplate·Constraint | 정책 논리와 적용 대상·매개변수를 선언함 |
| Pod SecurityContext | Seccomp·AppArmor 프로필 유형과 권한 설정을 지정함 |
| 프로필 배포 계층 | Localhost 프로필을 해당 Pod가 실행될 모든 노드에 배포함 |
| 컨테이너 런타임 | 승인된 프로필을 OCI 실행 설정에 반영함 |
| Linux 커널·감사 로그 | 시스템 호출과 자원 접근을 판정하고 위반 내역을 기록함 |

```text
Pod 요청 -> API 서버 -> OPA Admission -> 승인 -> kubelet·런타임
                                                  |
                                      Seccomp·AppArmor 프로필
                                                  |
                                              Linux 커널
```

> 요약: OPA 승인 후 런타임이 보안 프로필을 적용하고 Linux 커널이 실행 중 접근을 판정함.

## Ⅴ. 정책 적용 흐름

```text
Pod 요청 -> OPA 객체 검증 -> 노드 배치 -> 프로필 확인 -> 컨테이너 시작 -> 커널 접근 판정
```

1. **Pod 요청**: 사용자나 배포 도구가 SecurityContext를 포함한 객체를 API 서버에 제출함
2. **OPA 객체 검증**: AdmissionReview를 정책과 비교해 허용하거나 위반 사유로 거부함
3. **노드 배치**: Localhost 프로필을 쓸 때 노드 레이블·selector로 실행 노드를 제한함
4. **프로필 확인**: kubelet과 런타임이 RuntimeDefault 또는 Localhost 프로필을 확인함
5. **컨테이너 시작**: 런타임이 Seccomp·AppArmor 설정을 프로세스 실행 경계에 적용함
6. **커널 접근 판정**: Linux 커널이 호출·자원 접근을 프로필과 대조하고 위반 로그를 남김

> 요약: 배포 객체는 OPA를 통과하고 실행 프로세스는 노드의 Seccomp·AppArmor 프로필을 통과함.

## Ⅵ. 실무 사례

1. CI 클러스터는 OPA로 Privileged·비승인 이미지를 거부하고 거부 건수·감사 위반을 확인함
2. API Pod는 RuntimeDefault Seccomp와 AppArmor를 적용해 거부 호출 수·프로필 로드 실패를 확인함

## Ⅶ. 결론

- 컨테이너 보안은 OPA의 배포 전 정책과 Seccomp·AppArmor의 실행 중 통제를 계층으로 적용해야 함
