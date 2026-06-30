---
title: "TEE·Secure Boot (Trusted Execution Environment / Secure Boot)"
date: "2026-06-30"
weight: 87
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> TEE(Trusted Execution Environment)는 일반 OS와 격리된 하드웨어 신뢰 실행영역이며(ARM TrustZone, Intel SGX), Secure Boot는 부팅 단계마다 코드 서명을 검증해 신뢰사슬을 보장하는 보안 부팅 기법이다.

## Ⅱ. 구성요소 / 원리
- TrustZone: Secure World / Normal World 하드웨어 분리
- SGX(Software Guard Extensions): 엔클레이브(Enclave) 메모리 격리·암호화
- Secure Boot: 부트로더→커널 단계별 서명검증(Chain of Trust)
- 신뢰근원(Root of Trust): TPM/HSM, 변조 시 부팅 차단

## Ⅲ. 흐름도 / 구조
```text
Secure Boot: [ROM RoT]→서명검증→[Bootloader]→[Kernel]
                 실패 시 부팅 중단
TEE: [Normal World OS] | [Secure World: 키·인증·결제]
                       └ 하드웨어 격리
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 민감코드·데이터 보호, 부팅 무결성 보장 |
| 장점 | 하드웨어 격리, 변조 방지, 신뢰사슬 |
| 한계 | 사이드채널 취약, 엔클레이브 크기 제약, 복잡성 |

## Ⅴ. 기술사적 적용
- 모바일 결제(삼성페이)·DRM·생체인증에 TrustZone 적용
- 기밀컴퓨팅(Confidential Computing)으로 클라우드 데이터 보호
- 사이드채널 공격(Spectre/Meltdown) 대비 완화 필수
