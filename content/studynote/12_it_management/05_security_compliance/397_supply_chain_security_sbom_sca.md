---
title: "Supply Chain Security SBOM SCA"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SBOM(SPDX/CycloneDX/SWID)은 SW 구성요소를 가시화하는 *정적 명세서*이며, SCA는 SBOM·매니페스트·바이너리·런타임 신호를 CVE/NVD/OSV/KEV/EPSS에 매핑하여 *의존성 트리 기반의 위험을 정량화*하는 도구군이다. Sigstore·in-toto·SLSA는 *출처(Provenance)·서명·증명*으로 SBOM의 신뢰성을 보강한다.
> 2. **가값**: 로그4j(2021)·솔라윈즈(2020)·3CX(2023)·XZ Utils(2024) 등 공급망 침해 이후, SCA 도입 조직은 *평균 MTTR 70~80% 단축*(Forrester/Gartner 사례), *M&A SW 실사 비용 60% 절감*, *EPSS 기반 우선순위화로 패치 노이즈 90% 감소* 효과를 보고한다.
> 3. **판단 포인트**: 핵심은 ① **SBOM 생성 시점**(Pre-build manifest vs Build-time SBOM vs Runtime SBOM), ② **포맷 선택**(SPDX = 법적 호환성·ISO/IEC 5962, CycloneDX = 가벼움·확장성·VEX 내장), ③ **Reachability 분석** 채택 여부, ④ **Sigstore 기반 보증** 적용 범위, ⑤ 거버넌스(미국 EO 14028·한국 클라우드보안인증·EU CRA) 정렬이다.

---

## Ⅰ. 개요 및 필요성

현대 SW는 평균 **70~90%가 오픈소스 및 서드파티 컴포넌트**(Synopsys 2024 BSA 보고서 기준 70% ~ 90% 범위)로 구성된다. 2021년 Log4j(Log4Shell, CVE-2021-44228, CVSS 10.0) 사건은 *단순 의존성 하나*가 글로벌 금융·통신·정부 시스템에 수조 원의 피해를 유발함을 입증했고, 2024년 XZ Utils 백도어(CVE-2024-3094)는 *OSS 메인테이너 신뢰 자체*가 공격 표면이 됨을 보여주었다. 전통적 경계 보안(네트워크/웹방화벽)은 CI/CD 파이프라인, 컨테이너 레지스트리, 패키지 매니저, 멀티테넌트 SaaS의 *동적·다층 의존성*을 보호하지 못한다. 이에 **SBOM**(Software Bill of Materials, *ISO/IEC 5962:2024·CISA Minimum Elements* 표준화) + **SCA**(Software Composition Analysis) + **SLSA·Sigstore**(출처 보증) 체인이 *“소프트웨어의 영수증 + 영양 성분표 + 부작용 설명서”*로 작동해야 한다.

```text
[공급망 공격 흐름과 SBOM/SCA 방어 시점]

  [개발자]--push--->[소스 리포]--CI--->[빌드 시스템]--push--->[레지스트리]--deploy--->[운영]
     |              |                    |                       |                  |
     |              |                    |                       |                  |
   ①계정탈취    ②악성PR/훅       ③빌드훼손/Typosq.       ④이미지오염/      ⑤설정변조/
   (SolarWinds)  (event-stream)  (Codecov bash)         (3CX X_TRADER)    (백도어)
     |              |                    |                       |                  |
     +--------------+--------------------+-----------------------+------------------+
                                  | SBOM + SCA + Sigstore + SLSA 탐지/차단 영역 |
                                  v
       +--------------------------------------------------------------+
       | • Pre-build SCA: 매니페스트(package.json/lock/Cargo.lock) 스캔|
       | • Build-time  : SBOM 생성(SPDX/CycloneDX) + Sigstore 서명    |
       | • Post-build  : 컨테이너/바이너리 SCA(Trivy, Grype, Syft)    |
       | • Runtime     : eBPF/CDN 기반 런타임 SBOM(Insignary, Aibolit)|
       +--------------------------------------------------------------+
```

과거는 *“한 명이 사인하고 ASA 방화벽 뒤에 두면 안전”*이라는 **Castle-and-Moat** 패러다임이었으나, 클라우드·컨테이너·OSS 생태계에서는 **Zero-Trust Supply Chain**(NIST SP 800-161r2 C-SCRM, *“모든 컴포넌트·모든 인격·모든 단계”* 검증)으로 전환되었다.

- **📢 섹션 요약 비유**: 옛날에는 *우리가 만든 반찬만* 음식을 만들었지만, 지금은 *전 세계 식료품 유통망*에서 재료를 사 온다. **SBOM**은 *영양 성분표*, **SCA**는 *알레르기·변질 검사관*, **Sigstore**는 *수입 증명서*다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SBOM/SCA 시스템은 **4계층**으로 분리된다. ① *표준화 계층*(SPDX/CycloneDX), ② *생성 계층*(Syft/CDXgen/SPDX Tools), ③ *분석 계층*(Snyk/Xray/Black Duck/Trivy), ④ *보증 계층*(Sigstore/in-toto/SLSA Attestation). 각 도구는 *manifest 분석*, *lockfile 파싱*, *바이너리 fingerprint(PE/ELF 해시)*, *런타임 syscall/eBPF 추적* 중 하나 이상의 신호를 통합한다.

```text
[SBOM + SCA 4계층 아키텍처와 데이터 흐름]

                  +-----------------------------------------------+
                  |          ④ 보증 계층 (Attestation)            |
                  |  Sigstore: Cosign(서명) · Rekor(투명성로그)    |
                  |            Fulcio(신원인증) · Gitsign         |
                  |  in-toto Attestation · SLSA Level 1~4        |
                  +-----------------+-----------------------------+
                                    v
  +------------------------------------------------------------------+
  |  개발자 -push--> Git -PR--> CI(Jenkins/GH Actions/Argo) --> Registry|
  |       |              |              |                 |         |
  |       |              |              | ③ SCA 분석      |         |
  |       |              |              |  +----------+   |         |
  |       |              |              |  | Snyk OSS |   | ② SBOM   |
  |       |              |              |  | Xray     |   | 생성     |
  |       |              |              |  | BlackDuck|   |  +-----+ |
  |       |              |              |  | Trivy    |   |  |Syft | |
  |       |              |              |  | Grype    |   |  |CDXgen| |
  |       |              |              |  +----+-----+   |  +--+--+ |
  |       |              |              |       |         |     |    |
  |       |              |              |       +----+----+     |    |
  |       |              |              |            v          v    |
  |       |              |              |      +--------------------+|
  |       |              |              |      | ① 표준화:          ||
  |       |              |              |      |  SPDX 2.3 / 3.0    ||
  |       |              |              |      |  CycloneDX 1.5/1.6  ||
  |       |              |              |      |  SWID (ISO 19770-2) ||

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 397 / 800

<- **이전**: [396. 제로 트러스트 보안 모델 NIST 800-207](/studynote/12_it_management/05_security_compliance/396_zero_trust_security_model_nist_800_207/)
**다음**: [398. 랜섬웨어 대응 전략 백업 복구](/studynote/12_it_management/05_security_compliance/398_ransomware_response_strategy_backup_recovery/) ->

---
