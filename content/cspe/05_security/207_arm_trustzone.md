---
title: "ARM TrustZone (ARM TrustZone)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 207
---

# 📖 【암기용】 개념 완전 이해

> 목적: ARM TrustZone을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: ARM 프로세서를 Secure World와 Normal World로 나누어 민감 코드와 데이터를 격리하는 하드웨어 보안 기능
- **왜 필요한가**: 스마트폰, 결제 단말, 셋톱박스, IoT 장치에서는 일반 OS가 침해되어도 결제 키, DRM 키, 생체 인증 데이터가 함께 노출되면 안 된다. TrustZone은 같은 SoC 안에 별도 보안 실행 영역을 만든다.
- **핵심 직관**: 한 건물 안에 일반 사무실과 금고실을 만들고, 경비원이 문을 열 때마다 출입 목적을 검사하는 구조이다.

## 깊이 이해
- **배경·문제의식**: 모바일 OS와 앱은 공격면이 넓고 패치 지연이 발생한다. 모든 비밀 처리를 OS에 맡기면 루팅·커널 exploit 시 키가 노출되므로 하드웨어 수준의 격리 영역이 필요하다.
- **작동 원리**: ARM 코어는 NS bit로 Secure/Normal 상태를 구분한다. Secure Monitor가 world switch를 수행하고, OP-TEE 같은 TEE OS가 Trusted Application을 실행한다. 메모리, 인터럽트, 주변장치 접근도 TZASC/TZPC로 분리한다.
- **비유**: 은행 창구 앱은 Normal World에서 동작하고, 금고 열쇠 확인과 서명은 Secure World 창구에서만 처리하는 방식이다.
- **구체 예시**: 모바일 결제에서 카드 토큰 서명키는 Secure World의 TA가 보관하고, Android 앱은 SMC 호출로 서명 요청만 전달한다. 키 원문은 Normal World 메모리에 올라오지 않는다.
- **흔한 오해·주의점**: TrustZone은 Secure World 자체의 취약점과 side-channel을 없애지 않는다. TA 코드 품질, shared memory 검증, cache timing 대응이 별도로 필요하다.

## 연결 개념
- TEE - Trusted Execution Environment 구현 환경
- OP-TEE - 오픈소스 TEE OS와 Trusted Application 프레임워크
- Secure Boot - TEE OS와 TA 로딩 무결성 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: ARM TrustZone은 Secure/Normal World 격리, secure monitor 전환, TEE 응용, side-channel 리스크를 함께 설명해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ARM TrustZone은 SoC 자원을 Secure World와 Normal World로 분리해 민감 연산과 키를 일반 OS로부터 격리하는 하드웨어 기반 TEE이다.
> 2. **가치**: 결제, DRM, 생체 인증, 키 관리에서 일반 OS 침해 후에도 키 원문과 신뢰 연산의 노출 범위를 제한한다.
> 3. **판단 포인트**: world switch, secure monitor, OP-TEE, shared memory 검증, side-channel 대응, secure boot 연계를 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TEE 구조 이해 확인 | Secure World, Normal World, NS bit, Secure Monitor | 단순 가상화 또는 컨테이너로 설명 |
| 적용 사례 판단 확인 | 키 보호, 결제, DRM, 생체 인증, secure storage | 기능명만 쓰고 키 이동 경로 누락 |
| 리스크 인식 확인 | TA 취약점, shared memory 검증, cache side-channel | TrustZone을 완전 격리로 단정 |
> 요약: 이 문제는 TrustZone의 하드웨어 격리 구조와 TEE 운영 리스크를 함께 쓰는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

ARM TrustZone은 ARM SoC를 Secure World와 Normal World로 분리하는 하드웨어 보안 확장이다.
모바일·임베디드 장치는 일반 OS 공격면이 넓어 결제키, DRM키, 생체정보를 별도 실행 영역에 격리해야 한다.
TrustZone은 Secure Boot, TEE OS, Trusted Application과 결합되어 키 보호와 원격 신뢰 검증의 기반이 된다.

---

## Ⅱ. 구조 및 구성요소

```text
Normal World -> Rich OS / App / Driver
Normal World App -> TEE Client API -> SMC Call -> Secure Monitor
Secure World -> TEE OS / Trusted Application / Secure Storage
Hardware Control -> TZASC / TZPC / Interrupt Controller
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Secure World | TEE OS와 민감 연산 실행 | OP-TEE, trusted app, secure storage |
| Normal World | Android/Linux와 일반 앱 실행 | client app, driver, shared memory |
| Secure Monitor | world switch와 SMC 처리 | ARM monitor mode, exception level |
| TrustZone Controller | 메모리·주변장치 접근 분리 | TZASC, TZPC, GIC security state |
> 요약: TrustZone은 CPU 상태뿐 아니라 메모리·인터럽트·주변장치 접근 권한까지 Secure/Normal로 분리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Normal App -> TEE Client API -> Shared Memory 준비
TEE Driver -> SMC 호출 -> Secure Monitor 전환
TEE OS -> Trusted Application 실행 -> 키 연산
결과 반환 -> Secure Monitor 복귀 -> Normal App 응답
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Normal 앱이 TEE 요청과 shared memory 구성 | buffer length, 권한 검사 |
| 2 | 커널 드라이버가 SMC로 world switch 요청 | SMC ID allowlist |
| 3 | Secure Monitor가 Secure World로 전환 | NS bit, exception level 확인 |
| 4 | TA가 키 서명·복호화·검증 수행 | 키 원문 Normal memory 0건 |
| 5 | 결과와 감사 이벤트 반환 | TA return code, audit log |
> 요약: TrustZone 연산은 Normal 요청을 Secure World에서 처리한 뒤 결과만 반환하며, shared memory 검증이 공격면 통제의 핵심이다.

---

## Ⅳ. 특징

| 구분 | 일반 OS 처리 | ARM TrustZone 처리 | 판단 포인트 |
|:---|:---|:---|:---|
| 격리 경계 | 프로세스·커널 권한 | Secure/Normal World 하드웨어 경계 | 커널 침해 후 키 보호 필요 시 선택 |
| 키 보관 | 파일·Keystore | secure storage, RPMB, eFuse 연계 | 키 원문 export 금지 |
| 성능 비용 | world switch 없음 | SMC 전환과 shared memory 복사 | 호출 빈도·payload 크기 제한 |
| 리스크 | OS exploit | TA 버그, side-channel | TA 코드 최소화, cache 대응 |
> 요약: TrustZone은 키 원문 노출 범위를 줄이지만, Secure World 코드와 전환 인터페이스를 작게 유지해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 격리 방식 | OS 권한 분리, SELinux | 하드웨어 Secure World | 커널 exploit을 위협 모델에 포함할 때 |
| 외장 장비 | HSM, Secure Element | SoC 내 TEE | 모바일·IoT 원가와 지연 조건 고려 |
| 개발 모델 | 일반 앱 라이브러리 | CA/TA 분리, GP TEE API | 민감 코드 5천 LOC 이하 목표 |
> 요약: TrustZone은 외장 보안칩보다 통합성이 높지만 TA 코드 검증과 SoC 설정 검사가 선택 기준이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| TA 취약점 | 입력 검증 누락·버퍼 오류 | fuzzing, static analysis, code review | TA crash 0건, coverage 80% 이상 |
| shared memory 공격 | Normal World가 buffer 변조 | length 재검증, copy-in/copy-out | TOCTOU test pass 100% |
| side-channel | cache timing, power trace | constant-time crypto, cache partition | key recovery test 실패 100% |
> 요약: TrustZone 운영 리스크는 TA 품질, shared memory, side-channel이며 검증 자동화가 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 격리 설정 | secure memory 접근 위반 0건 | TZASC/TZPC test, negative access |
| 키 보호 | Normal World key dump 0건 | memory dump, kernel root test |
| 호출 지연 | SMC p95 5ms 이하 | trace, benchmark |
| 감사 | TA 호출 로그 보존 180일 | secure log, remote upload |
> 요약: 도입 효과는 메모리 격리, 키 덤프 차단, SMC 지연, TA 감사로그로 측정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 부팅 단계: Secure Boot로 TEE OS와 TA 이미지 서명을 검증하고 rollback counter를 적용함
2. 개발 단계: OP-TEE 기반 CA/TA를 분리하고 TA 입력 fuzzing, static analysis, constant-time crypto를 적용함
3. 운영 단계: 키는 secure storage/RPMB에 보관하고 Normal World에는 handle만 반환하며 TA 호출 감사로그를 수집함

**결론 (2줄):**
- 기술사 판단: 결제·DRM·생체 인증처럼 키 원문 노출을 막아야 하는 모바일/임베디드 장치는 TrustZone 기반 TEE를 선택함
- 향후 방향: TrustZone은 Secure Boot, attestation, confidential computing 경량 구현과 결합해 단말 신뢰 근거로 확장됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ARM TrustZone을 설명하시오" | CA-SMC-TA 호출 흐름 | Secure/Normal World 구조와 적용 사례 |
| 요구사항 명시형 | "TEE 적용 방안을 제시하시오", "키 보호를 설계하시오" | 키 요청·서명·반환 흐름 | TA 검증, side-channel, secure boot 연계 |
> 요약: 설명형은 격리 구조를, 설계형은 키 이동 경로와 TA 검증 지표를 중심으로 목차를 전환한다.
