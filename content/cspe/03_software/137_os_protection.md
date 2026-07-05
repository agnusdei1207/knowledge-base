---
title: 보호 및 보안 — 접근 제어 리스트 ACL (OS Protection)
date: 2026-07-05
tags: [cspe-software]
weight: 137
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | OS 내 자원에 대해 주체별 허용 권한을 명시한 접근 제어 메커니즘 |
| 배경 | 다중 사용자 환경에서 부적절한 자원 접근 및 위변조 방지 필요 |
| 출제 의도 | ACL vs Capability 비교, 보안 모델(Bell-LaPadula 등) 이해 측정 |

## Ⅱ. 구성요소
```text
[ Access Control Matrix ]      [ Access Control List ]
       File1 File2 File3       File1: {UserA: R, UserB: RW}
UserA    R     -     W    -->  File2: {UserC: X}
UserB    RW    -     -         File3: {UserA: W}
```
| 구성요소 | 설명 | 비유 |
|---|---|---|
| 주체 (Subject) | 자원에 접근하려는 사용자 또는 프로세스 | 방문객 |
| 객체 (Object) | 보호받는 자원 (파일, 디바이스, 메모리) | 방/금고 |
| 권한 (Permission) | 주체가 객체에 수행 가능한 동작 (R/W/X) | 열람/수정권 |
> 요약: ACL은 객체 중심으로 주체별 권한을 관리하는 목록임.

## Ⅲ. 절차
```text
Request (User, Op) -> Kernel Check -> Lookup ACL for Object -> Match?
      ^                                                         |
      +----- (Denied) <----- Reject Access <----- (No) ---------+
      |                                                         |
      +----- (Granted) <---- Allow Access <----- (Yes) ---------+
```
1. 접근 요청: 주체가 특정 객체에 대해 시스템 콜을 통해 작업 요청.
2. 메타데이터 조회: OS 커널이 해당 객체의 보안 속성(ACL)을 디스크/메모리에서 로드.
3. 규칙 매칭: 요청 주체의 ID와 ACL의 항목을 대조하여 허용 여부 판단.
4. 실행 제어: 매칭 결과에 따라 작업을 허가하거나 권한 오류(EACCES) 반환.
> 요약: 매 접근 시 권한을 검증하여 시스템의 기밀성과 무결성을 보장함.

## Ⅳ. 문제점
- 객체 수가 많아질 경우 ACL 관리가 복잡해지고 탐색 오버헤드 발생.
- 권한 철회(Revocation) 시 모든 ACL을 수정해야 하는 비효율성.

## Ⅴ. 개선방안
- RBAC(Role-Based Access Control)을 도입하여 역할 기반 그룹 권한 관리.
- ABAC(Attribute-Based) 적용으로 환경 속성(IP, 시간 등) 고려 동적 제어.

## Ⅵ. 전망
- Zero Trust OS: 모든 프로세스 요청을 명시적으로 검증하는 커널 보안 강화.
- 하드웨어 격리: Intel SGX 등을 활용한 ACL 기반 메모리 격리 보호 기술 확대.
