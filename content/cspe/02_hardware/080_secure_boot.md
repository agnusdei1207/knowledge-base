---
title: "Secure Boot 보안 부팅 (Secure Boot)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 80
extra:
  question_no: "080"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- Secure Boot는 부팅 단계마다 다음 단계 코드의 무결성과 출처를 검증하는 절차임
- root of trust와 chain of trust와 rollback protection이 핵심 개념임
- 암호화보다 서명 기반 무결성 검증이 중심 역할을 함

## Ⅰ. 개요

- **정의/개념**: Secure Boot는 ROM에서 시작한 신뢰 루트가 부트로더와 펌웨어와 커널 이미지를 단계적으로 서명 검증한 뒤에만 실행하게 하는 부팅 신뢰 체계임
- **배경/필요성**: 부팅 초기 코드는 운영체제 보안보다 먼저 실행되므로 이 경로가 변조되면 모든 상위 보안 기능이 우회될 수 있어, 가장 이른 시점의 검증이 필요함

## Ⅱ. 특징

- 승인된 코드만 실행하게 해 부트킷과 변조 펌웨어를 차단함
- root key 보호와 버전 검증과 복구 정책이 함께 있어야 완결된 구조가 됨
- 업데이트 체계와 긴밀히 연결되므로 운영 절차가 중요함
- 키 관리 실패 시 오히려 시스템 전체 신뢰가 무너질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | 일반 부팅 | Secure Boot |
|:---|:---|:---|
| 코드 실행 기준 | 저장된 순서대로 로드 | 서명과 정책 검증 후 로드 |
| 보호 대상 | 부팅 성공 자체 | 부트 체인 무결성 |
| 공격 저항성 | 낮음 | 높음 |
| 운영 요구 | 단순 배포 | 키 관리와 복구 절차 필요 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Boot ROM, Root of Trust | 변경 어려운 초기 코드와 키가 신뢰의 시작점이 됨 |
| Bootloader Chain | 각 단계가 다음 단계 이미지를 검증하며 chain of trust를 형성함 |
| Signed Image, Version Metadata | 무결성과 출처와 롤백 방지 정책을 함께 제공함 |
| Recovery, Policy Engine | 검증 실패 시 복구 이미지와 실패 처리 정책을 수행해 부팅 안정성을 보장함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 전원 인가/ROM 시작 | --> | 이미지 서명 검증 | --> | 다음 단계 로드  | --> | 정책 적용/복구  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **전원 인가 및 ROM 시작**: 변경 불가 초기 코드가 동작함
2. **이미지 서명 검증**: 해시와 공개키로 다음 단계 이미지를 확인함
3. **다음 단계 로드**: 검증된 이미지에 한해 실행을 이어감
4. **정책 적용 및 복구**: 실패 시 부팅 중단이나 복구 이미지를 선택함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 서명 키가 유출되거나 루트 키 교체 절차가 없으면 악성 이미지도 정상 코드처럼 실행될 수 있음
   - 해결방안: HSM 기반 서명과 key rotation 절차를 운영하고 signing audit trail과 revoked key coverage로 검증함
2. 문제: 유효한 서명이 붙은 오래된 취약 버전으로 되돌리는 rollback 공격이 가능할 수 있음
   - 해결방안: monotonic version counter를 적용하고 rollback block rate와 version policy compliance로 검증함
3. 문제: 검증 실패 시 복구 경로가 부실하면 장치가 현장에서 영구 부팅 불가 상태가 될 수 있음
   - 해결방안: signed recovery image와 fallback path를 설계하고 recovery success rate와 brick incident count로 검증함

## Ⅶ. 적용 사례

- 자동차 ECU 부팅 경로에서는 펌웨어 서명을 검증하고, boot integrity pass rate와 rollback block rate로 결과를 확인함
- 모바일 단말기에서는 secure boot와 TEE를 연계하고, tamper resistance와 recovery success rate로 결과를 확인함
- 산업 IoT 게이트웨이에서는 OTA 업데이트와 연동해 운영하고, signed update success rate와 unauthorized boot count로 결과를 확인함

## Ⅷ. 결론

Secure Boot의 핵심은 부팅을 암호화하는 것이 아니라 신뢰되지 않은 코드가 첫 단계부터 실행되지 못하게 막는 데 있으므로, 키 관리와 복구 정책이 설계의 중심임.
