---
title: "CAPTCHA·reCAPTCHA (CAPTCHA)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 113
---

# 📖 【암기용】 개념 완전 이해

> 목적: CAPTCHA와 reCAPTCHA를 로그인 화면의 퍼즐이 아니라 자동화 봇과 사람 사용자를 구분하는 위험 기반 방어 장치로 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 사람은 통과하고 자동화 프로그램은 통과하기 어렵게 만든 사용자 검증 기법
- **왜 필요한가**: 회원가입, 로그인, 결제, 댓글, 크롤링 지점은 봇이 대량 요청을 보내 계정 탈취·스팸·재고 선점·비용 유발을 일으킨다. CAPTCHA는 위험 요청에 추가 검증을 걸어 자동화 비용을 올린다.
- **핵심 직관**: 문 앞 경비원이 모든 방문객을 막지 않고, 수상한 방문객에게만 추가 질문이나 신분 확인을 요구하는 방식임

## 깊이 이해
- **배경·문제의식**: 단순 rate limit은 IP 회전, 프록시, 자동화 브라우저에 우회된다. 비밀번호 유출 목록을 이용한 credential stuffing은 정상 로그인 API를 반복 호출하므로 사용자 행위 기반 검증이 필요하다.
- **작동 원리**: 서버가 클라이언트에 challenge 또는 risk token을 발급한다. 사용자가 이미지 선택, 체크박스, 행위 분석을 통과하면 토큰이 생성되고, 서버는 secret key로 토큰 유효성·만료·점수를 검증한다.
- **비유**: 시험장 입구에서 무작위 신분 확인을 하는 것과 유사함. 모든 사람에게 긴 검사를 하면 줄이 길어지므로 위험도가 높은 사람에게만 검사를 강화한다.
- **구체 예시**: 로그인 실패 5회, 신규 ASN, 헤드리스 브라우저 탐지 시 reCAPTCHA 점수 0.3 미만이면 MFA를 요구하고, 점수 0.7 이상이면 비밀번호 검증만 수행한다.
- **흔한 오해·주의점**: CAPTCHA는 인증이 아니다. 계정 소유자를 증명하지 못하며, 접근성·개인정보·우회 서비스·AI OCR 위험 때문에 MFA, rate limit, bot management와 함께 써야 한다.

## 연결 개념
- Credential Stuffing — 유출 계정 목록 기반 자동 로그인 공격
- Bot Management — 지문, 행위, 평판, JavaScript challenge 결합
- MFA — CAPTCHA 통과 후 계정 소유성 추가 검증
- WAF/API Gateway — CAPTCHA 토큰 검증과 rate limit 적용 위치

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CAPTCHA는 사람 여부를 완전 판정하는 기술이 아니라 위험 기반으로 자동화 비용을 높이고, 계정 공격·스팸·스크래핑을 다층 통제로 낮추는 보안 통제임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CAPTCHA는 사용자의 인지·행위·브라우저 신호를 이용해 자동화 봇 요청과 사람 요청을 구분하는 challenge-response 통제이다.
> 2. **가치**: 로그인, 가입, 결제, 댓글 API에 추가 검증 토큰을 요구해 credential stuffing, 스팸, 대량 스크래핑의 요청 성공률을 낮춘다.
> 3. **판단 포인트**: 우회 가능성, 접근성, 개인정보 전송, 사용자 이탈률, false positive, MFA·rate limit 연계를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 봇 방어 통제 이해 확인 | challenge, token, risk score, server-side verify | 화면 퍼즐 UI만 설명 |
| 보안·사용성 균형 판단 확인 | 위험 기반 적용, 접근성 대체 수단, false positive | 모든 요청에 CAPTCHA 적용 |
| 우회 대응 설계 확인 | rate limit, MFA, device fingerprint, WAF 연계 | CAPTCHA를 인증 수단으로 오해 |
> 요약: 이 문제는 CAPTCHA를 단독 방어가 아니라 위험 기반 봇 통제 체계의 한 구성요소로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

CAPTCHA는 봇 요청 억제 통제이다.
웹 서비스는 로그인, 가입, 결제, 댓글 API에서 자동화 요청을 받는다. CAPTCHA와 reCAPTCHA는 위험 요청에 challenge 또는 점수 기반 검증을 적용해 스팸, 계정 탈취, 재고 선점, 스크래핑 비용을 증가시킨다.

---

## Ⅱ. 구조 및 구성요소

```text
Client Action -> CAPTCHA Widget / Risk Script -> Token
-> Application Server -> Provider Verify API -> Allow / MFA / Block
           +-> WAF / Rate Limit / Bot Signal
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Challenge UI | 이미지·문자·체크박스 검증 | 접근성 대체 수단 필요 |
| Risk Engine | 행위, 브라우저, IP 평판 점수화 | reCAPTCHA v3/Enterprise 방식 |
| Token | 클라이언트 검증 결과 전달 | 만료 2분 수준, 1회 사용 |
| Server Verify | secret key로 토큰 검증 | 서버 측 검증 누락 시 우회 |
| Policy Engine | 점수별 허용·MFA·차단 결정 | 임계값 0.3/0.7 등 업무별 조정 |
> 요약: CAPTCHA 구조는 클라이언트 challenge, 위험 점수, 서버 검증, 정책 엔진이 결합되어 요청 처리를 결정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> 위험 신호 수집 -> challenge/token 발급
-> 사용자 응답/행위 분석 -> 서버 토큰 검증 -> 허용 / MFA / 차단
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 로그인·가입·댓글 등 보호 지점 식별 | 실패 횟수, IP 평판, ASN, User-Agent |
| 2 | CAPTCHA challenge 또는 risk token 발급 | site key, action, nonce |
| 3 | 사용자가 challenge 수행 또는 행위 분석 | token 생성, score 산출 |
| 4 | 서버가 verify API 호출 | secret key, hostname, action, score |
| 5 | 정책 적용 후 결과 기록 | score 0.3 미만 차단, 0.3~0.7 MFA |
> 요약: CAPTCHA는 토큰을 클라이언트에서 받되, 최종 판정은 서버 검증과 위험 정책으로 수행해야 우회를 줄인다.

---

## Ⅳ. 특징

| 구분 | 단순 CAPTCHA | reCAPTCHA 점수형 | 정량·기술 포인트 |
|:---|:---|:---|:---|
| 검증 방식 | 문자·이미지 challenge | 행위·평판 기반 risk score | score 0.0~1.0 정책 |
| 사용자 영향 | 모든 challenge에 지연 발생 | 위험 요청 중심 추가 검증 | 이탈률 2%p 이하 목표 |
| 방어 범위 | 스팸·기초 봇 | credential stuffing, 자동화 브라우저 | 실패 로그인 5회 후 적용 |
| 한계 | OCR·대행 서비스 우회 | 개인정보·추적 우려 | DPIA, 쿠키 고지 필요 |
> 요약: 점수형 CAPTCHA는 사용자 마찰을 줄일 수 있지만, 개인정보 전송과 오탐 정책을 명시해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | CAPTCHA·reCAPTCHA | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | rate limit, IP 차단 | challenge, token, risk score | IP 회전·프록시 봇 대응 필요 |
| 비용/성능 | 자체 룰 운영 | 외부 검증 API, JS 로딩 | verify p95 300ms 이하 |
| 운영/위험 | 낮은 사용자 마찰 | 접근성, 오탐, 외부 의존 | WCAG 대체 수단, fallback 정책 |
> 요약: CAPTCHA는 rate limit 우회를 보완하지만 접근성 요구와 외부 서비스 의존을 수용할 업무에 적용해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 서버 검증 우회 | 클라이언트 토큰만 신뢰 | verify API 필수, hostname/action 검증 | 미검증 요청 차단율 100% |
| 사용자 오탐 | VPN, 장애인 보조기기, 저신호 환경 | 음성·OTP·MFA 대체 경로 | false positive 1% 이하 |
| 우회 서비스 | CAPTCHA 대행, ML OCR | device fingerprint, MFA, velocity rule | 봇 성공률 0.5% 이하 |
> 요약: CAPTCHA 리스크는 서버 검증, 대체 경로, 다층 봇 신호로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 봇 억제 | credential stuffing 성공률 0.5% 이하 | 로그인 로그, SIEM |
| 사용자 영향 | challenge 이탈률 2%p 이하, 오탐 1% 이하 | UX 로그, 고객센터 티켓 |
| 검증 처리 | verify API p95 300ms, 오류율 1% 이하 | APM, provider status |
> 요약: CAPTCHA 도입 효과는 봇 성공률, 사용자 이탈, 검증 API 지연과 오류율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 위험 기반 적용: 로그인 실패 5회, 신규 단말, 신규 ASN, 비정상 velocity에서 CAPTCHA를 적용하고 정상 세션은 challenge 생략
2. 서버 검증 고정: verify API에서 hostname, action, timestamp, score를 확인하고 token replay 방지를 위해 nonce와 2분 만료 적용
3. 다층 방어 연계: WAF rate limit, device fingerprint, MFA, IP 평판, SIEM 알림을 결합해 봇 성공률 0.5% 이하 관리

**결론 (2줄):**
- 기술사 판단: CAPTCHA는 공개 API의 봇 비용 상승에는 적용하고, 계정 소유성 확인은 FIDO2·MFA로 별도 설계한다.
- 향후 방향: 행위 기반 점수, 패스키, bot management가 결합되어 사용자 마찰을 줄인 위험 기반 인증 흐름으로 전환된다.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CAPTCHA를 설명하시오" | challenge, token, 서버 검증, 정책 적용 흐름 | 단순 CAPTCHA와 점수형 reCAPTCHA 차이 |
| 요구사항 명시형 | "봇 방어 방안을 제시하시오", "설계하시오" | 위험 신호, score threshold, MFA 연계 | 접근성, 오탐, 우회 대응, 지표 |
> 요약: 설명형은 동작 원리, 방안형은 위험 기반 적용과 우회 대응 지표를 중심으로 목차를 전환한다.
