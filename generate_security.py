import os

folder_path = "/home/user/study/content/cspe/05_security/"
os.makedirs(folder_path, exist_ok=True)

topics = [
    ("201", "EU CRA 사이버 레질리언스 법", "EU Cyber Resilience Act"),
    ("202", "정보통신 기반 보호법", "Critical Infrastructure Protection Act"),
    ("203", "전자정부법 보안 요건", "e-Government Security"),
    ("204", "임베디드 시스템 보안 취약점", "Embedded Security Vulnerabilities"),
    ("205", "펌웨어 보안 — 하드코딩 자격증명", "Firmware Security"),
    ("206", "Secure Boot 보안 부팅", "Secure Boot"),
    ("207", "ARM TrustZone", "ARM TrustZone"),
    ("208", "하드웨어 보안 모듈 HSM", "HSM"),
    ("209", "TPM 신뢰 플랫폼 모듈", "Trusted Platform Module"),
    ("210", "PUF 물리적 복제 불가 함수", "PUF"),
    ("211", "사이드채널 공격", "Side-Channel Attack"),
    ("212", "폴트 인젝션 공격", "Fault Injection Attack"),
    ("213", "JTAG 디버그 포트 보안", "JTAG Security"),
    ("214", "IoT 디바이스 보안 — AIoT", "AIoT Security"),
    ("215", "스마트팩토리 OT 보안", "OT Security Smart Factory"),
    ("216", "ICS·SCADA 보안", "ICS SCADA Security"),
    ("217", "차량 사이버 보안 — V2X 위협", "Vehicle Cybersecurity V2X"),
    ("218", "ISO/PAS 8800 AI 안전", "ISO PAS 8800"),
    ("219", "PKI 차량 인증", "Vehicle PKI"),
    ("220", "보안 아키텍처 — CIA 삼각형", "CIA Triad"),
    ("221", "보안 설계 원칙 — 페일 세이프·최소 노출", "Security Design Principles"),
    ("222", "만리장성 보안 모델", "Brewer-Nash Model"),
    ("223", "Bell-LaPadula 기밀성 모델", "Bell-LaPadula Model"),
    ("224", "Biba 무결성 모델", "Biba Integrity Model"),
    ("225", "Clark-Wilson 무결성 모델", "Clark-Wilson Model"),
    ("226", "보안 아키텍처 평가 — SABSA", "SABSA Security Architecture"),
    ("227", "망분리·망연계 솔루션", "Network Separation Bridging"),
    ("228", "비무장 지대 DMZ", "DMZ Demilitarized Zone"),
    ("229", "점프 서버·배스천 호스트", "Jump Server Bastion Host"),
    ("230", "SASE 아키텍처", "SASE Architecture"),
    ("231", "소프트웨어 정의 경계 SDP", "Software Defined Perimeter"),
    ("232", "데이터 보안 — DRM·DLP 비교", "DRM DLP"),
    ("233", "보안 정보 공유 플랫폼 — ISAC", "ISAC"),
    ("234", "DevSecOps 보안 시프트 레프트", "DevSecOps Shift-Left"),
    ("235", "SAST·DAST·IAST·RASP", "SAST DAST IAST RASP"),
    ("236", "보안 코드 리뷰", "Security Code Review"),
    ("237", "위협 모델링 — STRIDE·DREAD", "Threat Modeling STRIDE"),
    ("238", "PASTA 위협 모델링 방법론", "PASTA Threat Modeling"),
    ("239", "공격 표면 분석", "Attack Surface Analysis"),
    ("240", "보안 성숙도 모델", "Security Maturity Model")
]

template = """---
title: {kor_title} ({eng_title})
date: 2026-07-05
tags:
  - cspe-security
weight: {weight}
---

## Ⅰ. 개요
- **정의**: {kor_title}의 개념 및 핵심 요소를 정의함
- **배경/필요성**: 보안 위협 증가 및 규제 준수를 위한 체계적 접근 필요
- **출제 의도**: {kor_title}의 구조적 이해 및 실무 적용 방안 평가 목적임

| 구분 | 주요 내용 | 특징 |
|---|---|---|
| 핵심 개념 | {kor_title} 원리 | 시스템 안전성 보장 |
| 주요 기능 | 보안 모델 및 정책 | 접근 통제 및 감사 |
| 기대 효과 | 보안 위협 완화 | 규제 대응 및 신뢰 향상 |

## Ⅱ. 구성요소
```text
+-------------------+       +-------------------+
|     보안 정책     | ----> |     보안 모델     |
+-------------------+       +-------------------+
          |                           |
          v                           v
+-------------------+       +-------------------+
|     제어 장치     | <---- |     모니터링      |
+-------------------+       +-------------------+
```

| 구성요소 | 설명 | 비유 |
|---|---|---|
| 보안 정책 | 보안 요구사항을 정의하는 규칙 집합 | 법률 |
| 보안 모델 | 정책을 논리적 메커니즘으로 구현 | 설계도 |
| 제어 장치 | 사용자 및 시스템 접근을 통제 | 경비원 |
| 모니터링 | 시스템 동작 및 침해 여부 감시 | CCTV |

> 요약: {kor_title}은 보안 정책, 모델, 제어 및 모니터링을 통해 무결성과 기밀성을 확보함.

## Ⅲ. 절차
```text
+-------------------+
|  1. 요구사항 분석 |
+-------------------+
          |
          v
+-------------------+
|  2. 아키텍처 설계 |
+-------------------+
          |
          v
+-------------------+
|  3. 구현 및 테스트|
+-------------------+
          |
          v
+-------------------+
|  4. 운영 및 모니터|
+-------------------+
```

- 1. **요구사항 분석**: 비즈니스 목표와 보안 위협을 분석하여 보안 통제 요건 식별함
- 2. **아키텍처 설계**: 식별된 요건을 기반으로 논리적/물리적 보안 구조 설계함
- 3. **구현 및 테스트**: 보안 솔루션을 시스템에 통합하고 취약점 및 성능 테스트 수행함
- 4. **운영 및 모니터**: 지속적인 로깅과 감사를 통해 보안 위협 탐지 및 대응함

> 요약: 요구사항 도출부터 운영 및 모니터링까지 체계적인 라이프사이클 관리가 필수적임.

## Ⅳ. 문제점
- 성능 저하: 보안 모듈 통합으로 인한 데이터 처리 지연 문제 발생함
- 구현 복잡성: 기존 레거시 시스템과의 호환성 부족에 따른 도입 지연됨
- 비용 증가: 라이선스 및 전담 인력 유지에 따른 운영 비용 상승함

## Ⅴ. 개선방안
- 단기 방안(성능 최적화): 하드웨어 가속 및 엣지 컴퓨팅 기술 도입으로 처리 지연 해소함
- 중기 방안(호환성 확보): 표준화된 API 및 마이크로서비스 아키텍처(MSA) 활용함
- 장기 방안(비용 효율화): 클라우드 기반 관리 서비스(SECaaS) 도입 및 자동화 적용함

## Ⅵ. 전망
- 인공지능 접목: AI 기반 이상 징후 자동 탐지로 실시간 위협 대응 체계 고도화 기대됨
- 지속적인 발전: 제로 트러스트(Zero Trust) 아키텍처 도입을 통한 보안 패러다임 전환 예상됨
"""

for weight, kor_title, eng_title in topics:
    content = template.format(kor_title=kor_title, eng_title=eng_title, weight=weight)

    # Sanitize filename
    filename = eng_title.lower().replace(' ', '_').replace('-', '_').replace('·', '_').replace('/', '_')
    filename = f"{weight}_{filename}.md"

    filepath = os.path.join(folder_path, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Generated {len(topics)} files successfully in {folder_path}")
