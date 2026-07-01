---
title: "TPM 신뢰 플랫폼 모듈 (Trusted Platform Module)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 209
---

# 📖 【암기용】 개념 완전 이해

> 목적: TPM을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: PC·서버·장치에 부착된 보안 칩으로 키 보호, 부팅 측정, 원격 검증, 봉인 저장을 제공하는 신뢰 모듈
- **왜 필요한가**: 디스크 암호화 키나 장치 신뢰 상태를 소프트웨어만으로 관리하면 루트 권한 탈취 시 조작될 수 있다. TPM은 플랫폼 상태를 하드웨어에 기록하고 키 사용 조건을 묶는다.
- **핵심 직관**: 장치 안의 공증인처럼 부팅 때 본 내용을 장부에 기록하고, 장부 값이 맞을 때만 금고 열쇠를 내준다.

## 깊이 이해
- **배경·문제의식**: 원격 근무와 제로트러스트 환경에서는 단말이 패치된 상태인지, Secure Boot가 유지되는지, 디스크 키가 안전한지 확인해야 한다. TPM은 장치 상태를 PCR에 측정하고 외부에 quote로 증명한다.
- **작동 원리**: TPM 2.0은 PCR, NV storage, EK/AK, sealed storage, random generator, crypto engine을 제공한다. 부팅 단계 hash가 PCR에 extend되고, attestation server는 TPM quote와 event log를 비교한다.
- **비유**: 호텔 금고가 객실 카드와 체크인 기록이 모두 맞을 때만 열리는 구조와 같다. 카드만 훔쳐도 체크인 기록이 다르면 열리지 않는다.
- **구체 예시**: BitLocker는 디스크 키를 TPM PCR 정책에 seal한다. 부트로더가 변조되어 PCR 값이 바뀌면 자동 잠금 해제 실패, recovery key 입력 요구가 발생한다.
- **흔한 오해·주의점**: TPM은 대용량 암복호화 장비가 아니다. 키 보호와 상태 증명에 특화되며, 디스크 전체 암호화 연산은 CPU AES-NI가 수행한다.

## 연결 개념
- Measured Boot - PCR에 부팅 hash 누적
- Remote Attestation - TPM quote로 단말 상태 검증
- Sealed Storage - PCR 조건이 맞을 때만 키 사용 허용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: TPM은 키 저장 장치가 아니라 PCR 기반 measured boot, attestation, sealed storage를 결합한 플랫폼 신뢰 근거로 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TPM 2.0은 플랫폼 부팅 상태를 PCR에 누적하고, 키를 PCR 정책에 묶어 사용 조건을 강제하는 하드웨어 신뢰 모듈이다.
> 2. **가치**: BitLocker, 원격 단말 검증, Secure Boot 측정, 인증키 보호에서 소프트웨어 조작 가능성을 줄인다.
> 3. **판단 포인트**: PCR, measured boot, quote, AK/EK, sealed storage, event log 검증을 분리해 답안을 구성해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TPM 구조 이해 확인 | TPM 2.0, PCR, EK, AK, NV, sealed storage | 단순 USB 보안키로 설명 |
| 부팅 검증 흐름 확인 | measured boot, PCR extend, quote, event log | Secure Boot와 measured boot 혼동 |
| 적용 사례 판단 확인 | BitLocker, 원격 검증, device identity | 디스크 암호화 전체를 TPM이 수행한다고 서술 |
> 요약: 이 문제는 TPM의 측정·증명·봉인 기능을 플랫폼 신뢰 흐름으로 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

TPM은 플랫폼 상태 측정과 키 보호를 제공하는 하드웨어 기반 신뢰 모듈이다.
제로트러스트 단말과 디스크 암호화는 장치 부팅 상태가 정책과 일치할 때만 키 사용을 허용해야 한다.
TPM 2.0의 PCR, attestation, sealed storage는 Secure Boot 이후의 신뢰 검증 근거가 된다.

---

## Ⅱ. 구조 및 구성요소

```text
Boot Components -> Hash 측정 -> TPM PCR Extend
TPM Core -> PCR / EK / AK / NV Storage / Crypto Engine
Verifier -> Quote Request -> TPM Quote + Event Log
Protected Data -> Sealed Storage -> PCR Policy Match
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| PCR | 부팅 단계 측정값 누적 | extend 연산, reset 제한 |
| EK/AK | 장치 신원과 attestation 서명 | endorsement key, attestation key |
| Sealed Storage | PCR 조건부 키 사용 | BitLocker, VPN key, certificate |
| Event Log | PCR 값을 만든 측정 이벤트 목록 | verifier가 expected value 비교 |
> 요약: TPM은 PCR 측정값과 키 정책을 결합해 장치 상태가 맞을 때만 비밀 사용을 허용한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Power On -> Firmware 측정 -> PCR Extend
Bootloader 측정 -> Kernel 측정 -> Event Log 생성
Verifier 요청 -> TPM Quote 생성 -> AK로 서명
정책 일치 -> sealed key unseal -> BitLocker/VPN 사용
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | BIOS/UEFI, bootloader, kernel hash 측정 | PCR expected profile |
| 2 | 측정값을 PCR에 extend하고 event log 저장 | log-PCR replay 일치 |
| 3 | verifier가 nonce 포함 quote 요청 | nonce freshness, AK cert |
| 4 | TPM이 PCR quote를 AK로 서명 | signature verify 100% |
| 5 | 정책 일치 시 sealed key 사용 허용 | unseal failure on tamper |
> 요약: TPM은 부팅 측정값을 PCR에 누적하고 quote와 sealed storage로 검증·키 사용을 연결한다.

---

## Ⅳ. 특징

| 구분 | 소프트웨어 키 관리 | TPM 기반 키 관리 | 판단 포인트 |
|:---|:---|:---|:---|
| 키 보호 | OS 파일·메모리 의존 | TPM sealed storage와 policy | 루트 권한 침해 위협 시 적용 |
| 상태 검증 | 에이전트 보고 | PCR quote와 event log | 원격 검증 신뢰도 확보 |
| 연산 범위 | 범용 암호 처리 | 키 보호·서명·난수 중심 | 대용량 암호화는 CPU 수행 |
| 적용 사례 | 앱 설정 암호화 | BitLocker, device attestation | 부팅 상태와 키 정책 연결 |
> 요약: TPM은 암호 연산 가속기보다 플랫폼 상태 증명과 조건부 키 사용에 초점을 둔 모듈이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 신뢰 근거 | OS agent 보고 | TPM quote, PCR, event log | 제로트러스트 단말 검증 시 TPM |
| 키 저장 | 파일·KMS 호출 | sealed storage, NV index | 오프라인 부팅 키 보호 필요 시 |
| 장비 형태 | Secure Element, HSM | TPM 2.0 discrete/firmware | PC·서버 플랫폼 표준성 우선 시 |
> 요약: TPM은 범용 키 금고보다 플랫폼 상태에 묶인 키 사용과 원격 검증에서 선택 가치가 크다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| PCR drift | 펌웨어 업데이트 후 예상값 변경 | baseline 재등록, staged rollout | false reject 1% 이하 |
| quote 재사용 | nonce 검증 누락 | verifier nonce, timestamp, TLS binding | replay accept 0건 |
| recovery key 노출 | 운영자 절차 미흡 | escrow 접근통제, 감사로그 | recovery access 승인 100% |
> 요약: TPM 운영 리스크는 기준값 변화, quote 재사용, 복구키 노출이며 verifier 정책과 감사로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| PCR 검증 | expected PCR match 95% 이상 | attestation server report |
| Event Log | PCR replay 일치 100% | event log parser |
| Sealing | 변조 부팅 시 unseal 0회 | tamper boot test |
| BitLocker | TPM 보호 적용률 100% | MDM compliance, recovery audit |
> 요약: TPM 적용 효과는 PCR 일치율, event log 검증, unseal 차단, 디스크 암호화 정책 준수율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 단말 등록: TPM EK 인증서와 AK를 등록하고 MDM에 장치 신원, OS baseline, PCR profile을 저장함
2. 부팅 검증: UEFI measured boot와 Secure Boot를 병행하고 event log를 attestation server에서 재계산함
3. 키 보호: BitLocker, VPN 인증서, 앱 secret을 PCR policy로 seal하고 recovery key 접근을 RBAC와 감사로그로 통제함

**결론 (2줄):**
- 기술사 판단: 원격 단말 신뢰와 디스크 키 보호가 필요한 조직은 TPM 2.0 measured boot와 sealed storage를 기본 통제로 선택함
- 향후 방향: TPM attestation은 제로트러스트, DICE, confidential computing의 장치 신뢰 증명으로 확장됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TPM을 설명하시오" | PCR extend, quote, unseal 흐름 | 키 저장과 measured boot 차이 |
| 요구사항 명시형 | "원격 검증 방안을 제시하시오", "BitLocker와 연계하시오" | verifier nonce, event log, sealed key 흐름 | PCR drift, recovery key, 정책 기준 |
> 요약: 설명형은 TPM 기능을 넓게, 방안형은 attestation과 sealed storage 운영 지표 중심으로 목차를 전환한다.
