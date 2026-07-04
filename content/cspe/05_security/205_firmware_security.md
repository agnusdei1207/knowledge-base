---
title: "펌웨어 보안 (Firmware Security)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 205
---

# 📖 【암기용】 개념 완전 이해

> 목적: 펌웨어 보안을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 장치 내부 소프트웨어의 비밀값·무결성·업데이트·저장소를 보호하는 보안 체계
- **왜 필요한가**: 펌웨어는 하드웨어와 운영체제 사이에서 부팅, 센서, 네트워크, 암호키를 제어한다. 펌웨어가 변조되면 앱 보안과 네트워크 보안이 남아 있어도 장치 제어권이 공격자에게 넘어간다.
- **핵심 직관**: 펌웨어는 장치의 운영 매뉴얼이자 열쇠 묶음이므로, 변조와 열쇠 노출을 동시에 막아야 한다.

## 깊이 이해
- **배경·문제의식**: 펌웨어에는 유지보수 계정, API token, Wi-Fi PSK, 인증서, 디버그 문자열이 남기 쉽다. 단일 이미지가 수십만 대에 배포되면 한 번의 유출이 전체 장치군 침해로 확산된다.
- **작동 원리**: 안전한 펌웨어는 빌드 시 secret scan과 SBOM 생성, 배포 시 서명, 장치 측 검증, 설치 후 rollback protection, 실행 중 secure storage를 결합한다.
- **비유**: 펌웨어 이미지는 택배 상자와 같다. 보내는 사람 서명, 훼손 여부, 이전 버전 재배송 차단, 상자 안 열쇠 보관 위치까지 확인해야 한다.
- **구체 예시**: CWE-798 하드코딩 자격증명이 펌웨어 1개에 포함되면 `strings`와 `binwalk`로 계정 추출 후 동일 모델 10만 대에 대입 공격 가능.
- **흔한 오해·주의점**: 펌웨어 파일을 압축하거나 난독화해도 무결성 검증이 되지 않는다. 공격자는 SPI flash dump, OTA 패킷, 제조사 다운로드 서버에서 이미지를 확보할 수 있다.

## 연결 개념
- Secure Boot - 부팅 시 서명된 펌웨어만 실행
- SBOM - 펌웨어 구성 라이브러리와 CVE 추적
- Secure Storage - 키와 토큰을 TrustZone, TPM, HSM, eFuse에 보관

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 펌웨어 보안은 secret 제거, 서명 검증, SBOM, OTA rollback, secure storage를 빌드-배포-운영 흐름으로 묶어 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 펌웨어 보안은 장치 제어 소프트웨어의 비밀값 노출, 변조 실행, 취약 구성요소, rollback 공격을 통제하는 체계이다.
> 2. **가치**: 서명 검증과 SBOM 기반 CVE 추적으로 대량 장치군의 동일 취약점 확산을 제한한다.
> 3. **판단 포인트**: CWE-798 제거, 이미지 서명, A/B OTA, rollback counter, secure storage, 감사로그를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 펌웨어 취약점 원인 분석 확인 | 하드코딩 자격증명, unsigned image, outdated library, rollback | 펌웨어를 단순 파일 암호화로만 설명 |
| 업데이트 무결성 판단 확인 | secure boot, signed OTA, version counter, A/B partition | OTA 성공만 쓰고 실패 복구·rollback 방지 누락 |
| 공급망 관리 역량 확인 | SBOM, SCA, CVE, reproducible build, signing key 보호 | 라이브러리 취약점 추적 기준 누락 |
> 요약: 이 문제는 펌웨어 라이프사이클에서 비밀값·무결성·취약점·복구를 통합해 쓰는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 장치 펌웨어 통제 활동
- 배경: 펌웨어는 부팅, 센서, 네트워크, 키 저장을 제어하므로 변조 시 장치 전체 권한이 침해된다.
- 필요성: CWE-798 하드코딩 비밀값 제거, 서명 OTA, SBOM, 롤백 방지로 동일 이미지 재사용 리스크를 통제한다.

---

## Ⅱ. 구조 및 구성요소

```text
Source Code -> Secret Scan -> SBOM/SCA -> Build Artifact
Build Artifact -> Code Signing -> OTA Server -> Device Verifier
Device Verifier -> A/B Partition -> Rollback Counter -> Secure Storage
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Secret Scan | 키·토큰·계정 문자열 탐지 | CWE-798, entropy scan, allowlist |
| SBOM/SCA | 구성요소와 CVE 추적 | SPDX, CycloneDX, CVSS 기준 |
| Code Signing | 펌웨어 무결성·출처 검증 | ECDSA P-256, Ed25519, SHA-256 |
| Secure Storage | 키·토큰·카운터 보호 | TEE, TPM, HSM, eFuse, monotonic counter |
> 요약: 펌웨어 보안 구조는 빌드 산출물 생성 전 secret 제거와 배포 후 장치 검증을 하나의 체인으로 묶는다.

---

## Ⅲ. 동작원리 및 흐름도

```text
코드 변경 -> secret scan -> SBOM 생성 -> CVE gate
빌드 산출물 -> hash 생성 -> 개인키 서명 -> OTA 등록
장치 수신 -> 서명 검증 -> version counter 비교 -> A/B 설치
부팅 검증 -> 실패 시 이전 slot 복구 -> 감사로그 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 저장소와 바이너리에서 자격증명 탐지 | CWE-798 0건, entropy 임계값 |
| 2 | 라이브러리 목록과 CVE 매핑 | Critical CVE 0건, High 예외 승인 |
| 3 | 이미지 hash와 서명 생성 | SHA-256, ECDSA/Ed25519 서명 |
| 4 | 장치 측 서명·버전·호환성 검증 | unsigned·downgrade 설치 0회 |
| 5 | A/B boot, 실패 복구, 감사로그 저장 | boot success rate 99.9%, 로그 180일 |
> 요약: 펌웨어 보안은 빌드 게이트와 장치 검증 게이트를 모두 통과해야 설치되며, 실패 시 복구 경로가 필요하다.

---

## Ⅳ. 특징

| 구분 | 취약 펌웨어 배포 | 보안 펌웨어 배포 | 판단 포인트 |
|:---|:---|:---|:---|
| 자격증명 | 동일 계정·토큰 포함 | per-device secret, runtime injection | 동일 secret 0건 |
| 무결성 | hash만 제공 또는 미검증 | 제조사 개인키 서명과 장치 검증 | unsigned image reject 100% |
| 취약점 추적 | 구성요소 수동 관리 | SBOM, SCA, CVE feed 연계 | Critical CVE SLA 7일 |
| 복구 | 단일 파티션 덮어쓰기 | A/B partition, rollback counter | OTA 실패 복구 99.9% |
> 요약: 펌웨어 보안은 서명만으로 끝나지 않으며, 비밀값 제거와 취약점 추적, 실패 복구를 같은 수준으로 설계해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 배포 검증 | checksum, HTTPS 다운로드 | device-side signature verification | 오프라인 공격 가능 장비는 서명 필수 |
| 취약점 관리 | 수동 라이브러리 목록 | SBOM+SCA 자동 게이트 | CVE SLA 요구 조직에 적용 |
| 키 관리 | 빌드 서버 파일 키 | HSM/KMS signing key, 2인 승인 | 릴리스 권한 분리 필요 시 선택 |
> 요약: 펌웨어 보호 수준은 장치 측 검증과 서명키 관리 수준으로 결정된다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 하드코딩 자격증명 | 개발·테스트 secret 잔존 | secret scan, per-device provisioning | CWE-798 0건 |
| rollback 공격 | 취약 이전 버전 재설치 | monotonic counter, anti-rollback fuse | downgrade install 0회 |
| 서명키 유출 | CI 서버 키 파일 보관 | HSM, PKCS#11, key ceremony | unauthorized signing 0건 |
> 요약: 펌웨어 보안 리스크는 secret, rollback, signing key로 압축되며 각 항목은 자동 게이트와 키 관리로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Secret | 코드·바이너리 secret 0건 | trufflehog, strings, binwalk |
| SBOM | SPDX/CycloneDX 100% 생성 | CI artifact, SCA report |
| OTA | staged rollout 실패율 0.1% 이하 | device telemetry, update server log |
| 저장소 | 키 평문 저장 0건 | TEE/TPM API audit, flash dump test |
> 요약: 도입 효과는 secret 잔존, SBOM 생성률, OTA 실패율, 평문 키 저장 여부로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. CI 단계: secret scan, SCA, SBOM 생성, Critical CVE 0건 gate를 릴리스 조건으로 설정함
2. 서명 단계: HSM 또는 cloud KMS에 signing key를 보관하고 PKCS#11 API와 2인 승인으로 릴리스 서명을 수행함
3. 장치 단계: A/B partition, anti-rollback counter, secure storage, OTA telemetry를 결합해 실패 복구와 변조 차단을 수행함

**결론 (2줄):**
- 기술사 판단: 1만 대 이상 동일 펌웨어 배포 제품은 signed OTA, SBOM, per-device secret을 기본 통제로 선택함
- 향후 방향: 펌웨어 보안은 SBOM 의무화와 장치 원격 attestation으로 공급망 검증 범위가 확대됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "펌웨어 보안을 설명하시오" | 빌드-서명-OTA-부팅 검증 흐름 | secret, SBOM, OTA, secure storage 비교 |
| 요구사항 명시형 | "하드코딩 자격증명 대응 방안을 제시하시오", "OTA를 설계하시오" | secret 제거 또는 OTA 검증 단계 | rollout, rollback, signing key 선택 기준 |
> 요약: 설명형은 전체 생명주기를, 설계형은 서명·버전·복구·키 관리 항목을 중심으로 목차를 전환한다.
