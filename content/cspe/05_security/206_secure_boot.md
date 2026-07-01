---
title: "Secure Boot 보안 부팅 (Secure Boot)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 206
---

# 📖 【암기용】 개념 완전 이해

> 목적: Secure Boot를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 전원이 켜진 순간부터 서명된 코드만 다음 단계로 실행시키는 부팅 신뢰 체인
- **왜 필요한가**: 운영체제나 애플리케이션 보안이 아무리 촘촘해도 첫 부트로더가 변조되면 이후 검증 로직 자체를 공격자가 바꿀 수 있다. Secure Boot는 첫 실행 코드부터 신뢰 근거를 세운다.
- **핵심 직관**: 건물 출입증 검사원을 믿으려면, 그 검사원을 임명한 사람부터 확인해야 한다.

## 깊이 이해
- **배경·문제의식**: 루트킷, 부트킷, 변조 펌웨어는 OS 로딩 전 실행되어 백신·EDR보다 먼저 권한을 가진다. 따라서 변경 가능한 저장소가 아니라 ROM, eFuse, OTP 같은 변조 곤란 위치에 root of trust가 필요하다.
- **작동 원리**: ROM code가 부트로더 공개키 hash를 확인하고, 부트로더는 커널을, 커널은 initramfs·드라이버를 검증한다. 측정 부팅은 각 단계 hash를 TPM PCR에 누적해 원격 검증에 사용한다.
- **비유**: 릴레이 경주에서 첫 주자가 신분 확인을 통과하고, 각 주자가 다음 주자의 신분증을 확인한 뒤 배턴을 넘기는 구조이다.
- **구체 예시**: ROM에 저장된 SHA-256 public key hash와 부트로더 서명이 불일치하면 부팅 중단, A/B slot 중 이전 정상 이미지로 복구, boot fail 이벤트 기록 수행.
- **흔한 오해·주의점**: Secure Boot는 취약한 애플리케이션 실행을 자동 차단하지 않는다. 부팅 체인 무결성 통제이며, 런타임 취약점은 TEE, SELinux, EDR, 패치로 별도 대응해야 한다.

## 연결 개념
- ROM Root of Trust - 변경 불가능한 첫 신뢰 근거
- Measured Boot - TPM PCR에 부팅 측정값 누적
- Firmware Security - 서명 이미지와 rollback 방지 연계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Secure Boot는 verified boot와 measured boot를 구분하고, 서명 체인·rollback protection·TPM/TEE 연계를 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Secure Boot는 ROM root of trust에서 시작해 부트로더, 커널, OS 구성요소의 서명을 순차 검증하는 부팅 무결성 체계이다.
> 2. **가치**: 부트킷·변조 펌웨어 실행을 OS 시작 전 차단하고, measured boot는 TPM PCR 기반 원격 attestation 근거를 제공한다.
> 3. **판단 포인트**: verified boot, measured boot, 서명키 보호, rollback protection, 복구 경로를 구분해 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 부팅 신뢰 체인 이해 확인 | ROM RoT, public key hash, bootloader, kernel, OS chain | 단순 BIOS 옵션으로만 설명 |
| verified/measured boot 구분 확인 | 실행 차단 vs PCR 측정·원격 검증 | 측정 부팅을 서명 검증과 동일시 |
| 운영 설계 판단 확인 | anti-rollback, A/B recovery, TPM/TEE, key rotation | 서명 실패 시 복구 절차 누락 |
> 요약: 이 문제는 첫 신뢰 근거에서 실행 이미지까지 이어지는 체인과 운영 복구 조건을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 부팅 코드 무결성 검증 체계
- 배경: 부트킷은 OS 보안 모듈보다 먼저 실행되어 탐지 회피와 영속화를 수행하므로 부팅 전 검증이 필요하다.
- 필요성: ROM root of trust, 서명 체인, rollback protection으로 장치 출고 후 펌웨어 변조 실행을 차단한다.

---

## Ⅱ. 구조 및 구성요소

```text
ROM Root of Trust -> First Stage Bootloader -> Second Stage Bootloader
Second Stage Bootloader -> Kernel / Device Tree / initramfs
Measured Path -> TPM PCR -> Attestation Server
Recovery Path -> A/B Slot -> Rollback Counter
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| ROM RoT | 변경 불가 첫 검증 코드 | public key hash, eFuse, OTP |
| Bootloader | 다음 단계 이미지 검증 | U-Boot verified boot, UEFI Secure Boot |
| TPM/TEE | 측정값·키·정책 보호 | PCR, sealed storage, OP-TEE 연계 |
| Rollback Protection | 취약 이전 버전 실행 차단 | monotonic counter, RPMB, eFuse |
> 요약: Secure Boot 구조는 ROM RoT에서 시작한 검증 체인과 TPM/TEE 기반 측정·저장 체인으로 나뉜다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Power On -> ROM Code 실행 -> Bootloader 서명 검증
검증 성공 -> Kernel 서명 검증 -> OS 부팅
검증 실패 -> Recovery Slot 선택 -> 감사로그 기록
Measured Boot -> Hash Extend -> PCR 누적 -> 원격 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | ROM code가 부트로더 hash와 서명 확인 | SHA-256 hash, ECDSA/RSA 서명 |
| 2 | 부트로더가 커널·DTB·initramfs 검증 | allow key list, revocation list |
| 3 | version counter로 rollback 차단 | downgrade boot 0회 |
| 4 | 각 단계 hash를 TPM PCR에 extend | PCR expected value match |
| 5 | 실패 시 A/B slot 복구 또는 halt | boot failure audit 100% 기록 |
> 요약: verified boot는 실패 이미지를 실행하지 않고, measured boot는 실행 이력을 PCR에 남겨 원격 검증에 사용한다.

---

## Ⅳ. 특징

| 구분 | Verified Boot | Measured Boot | 판단 포인트 |
|:---|:---|:---|:---|
| 목적 | 변조 이미지 실행 차단 | 부팅 상태 증거 생성 | 차단 필요 시 verified 우선 |
| 동작 | 서명 검증 실패 시 halt/recovery | hash를 TPM PCR에 누적 | 원격 검증 필요 시 measured 병행 |
| 산출물 | boot pass/fail | PCR, event log, quote | attestation server와 연계 |
| 한계 | 런타임 exploit 차단 범위 아님 | 측정만으로 실행 차단 없음 | SELinux, TEE, 패치 병행 |
> 요약: Secure Boot 답안은 차단 기능과 증거 생성 기능을 분리해야 채점 포인트가 명확하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 신뢰 시작점 | Flash bootloader | ROM RoT, eFuse key hash | 물리 접근 가능 장비는 ROM RoT 필요 |
| 검증 범위 | 부트로더 일부 | kernel, DTB, initramfs, module | 커널 모듈 위협 있으면 범위 확대 |
| 원격 검증 | 로컬 부팅 성공 | TPM quote, PCR policy | 제로트러스트 단말 검증 시 적용 |
> 요약: Secure Boot 적용 범위는 물리 공격 가능성, 원격 검증 요구, 복구 요구수준으로 결정한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 키 유출 | 서명 개인키 파일 보관 | HSM/KMS, key ceremony, revocation | unauthorized image 0건 |
| rollback 공격 | 취약 구버전 재설치 | monotonic counter, revocation list | downgrade boot 0회 |
| 복구 실패 | 단일 이미지 손상 | A/B slot, rescue image, watchdog | boot recovery success 99.9% |
> 요약: 운영 리스크는 서명키, rollback, 복구 실패이며 키 관리와 이중 파티션으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 서명 검증 | unsigned image boot 0회 | negative boot test |
| PCR 측정 | expected PCR match 100% | TPM quote, event log |
| 버전 통제 | rollback attempt 차단 100% | version counter test |
| 복구 | OTA 실패 후 정상 slot 복구 99.9% | power-cut update test |
> 요약: Secure Boot 품질은 unsigned 차단, PCR 일치, rollback 차단, 복구 성공률로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 제조 단계: ROM RoT에 public key hash를 eFuse/OTP로 고정하고 signing key는 HSM에서 관리함
2. 부팅 단계: bootloader, kernel, initramfs, device tree를 ECDSA P-256 또는 RSA-3072 서명으로 검증함
3. 운영 단계: TPM PCR attestation, rollback counter, A/B recovery, key revocation list를 업데이트 정책에 포함함

**결론 (2줄):**
- 기술사 판단: 물리 접근 가능 장치와 규제 단말은 verified boot와 measured boot를 함께 적용함
- 향후 방향: Secure Boot는 TPM attestation과 TEE 키 보호를 결합해 제로트러스트 단말 신뢰 근거로 확장됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Secure Boot를 설명하시오" | ROM RoT에서 OS까지 서명 검증 흐름 | verified boot와 measured boot 차이 |
| 요구사항 명시형 | "보안 부팅을 설계하시오", "TPM과 연계하시오" | PCR 측정, rollback, recovery 흐름 | 키 관리·복구·원격 검증 선택 기준 |
> 요약: 설명형은 신뢰 체인 원리를, 설계형은 서명키·PCR·복구 정책을 중심으로 목차를 전환한다.
