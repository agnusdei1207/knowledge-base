import os

files_data = [
    ("121_dspm.md", "DSPM 데이터 보안 형상 관리 (DSPM)"),
    ("122_cloud_native_security_4c.md", "클라우드 네이티브 보안 4C (Cloud Native Security 4C)"),
    ("123_container_image_scan.md", "컨테이너 이미지 취약점 스캔 — Trivy (Container Image Scan)"),
    ("124_opa_gatekeeper.md", "OPA Gatekeeper 정책 엔진 (OPA Gatekeeper)"),
    ("125_falco_runtime.md", "Falco 런타임 보안 (Falco Runtime Security)"),
    ("126_seccomp_apparmor.md", "Seccomp·AppArmor·SELinux (Seccomp AppArmor SELinux)"),
    ("127_namespace_cgroup.md", "네임스페이스·cgroup 격리 (Namespace Cgroup Isolation)"),
    ("128_rootless_container.md", "Rootless 컨테이너 보안 (Rootless Container Security)"),
    ("129_csap.md", "클라우드 CSAP 보안 인증 등급제 (CSAP)"),
    ("130_supply_chain_security.md", "소프트웨어 공급망 보안 — SBOM·VEX (Supply Chain Security)"),
    ("131_slsa.md", "SLSA 공급망 보안 프레임워크 (SLSA)"),
    ("132_artifact_signing.md", "아티팩트 서명 — Cosign·Sigstore (Artifact Signing)"),
    ("133_secrets_management.md", "비밀 관리 — Vault·AWS Secrets (Secrets Management)"),
    ("134_ai_security_threat.md", "AI 보안 위협 전체 구조 (AI Security Threat Landscape)"),
    ("135_prompt_injection.md", "프롬프트 인젝션 (Prompt Injection)"),
    ("136_indirect_prompt_injection.md", "간접 프롬프트 인젝션 (Indirect Prompt Injection)"),
    ("137_jailbreak_attack.md", "탈옥 Jailbreak 공격 (Jailbreak Attack)"),
    ("138_prompt_leakage.md", "프롬프트 유출 (Prompt Leakage)"),
    ("139_model_inversion.md", "모델 역전 공격 (Model Inversion Attack)"),
    ("140_model_extraction.md", "모델 추출 공격 (Model Extraction Attack)"),
    ("141_data_poisoning.md", "데이터 오염 공격 (Data Poisoning)"),
    ("142_backdoor_attack.md", "백도어 공격 (Backdoor Attack)"),
    ("143_adversarial_example.md", "적대적 예제 공격 (Adversarial Example)"),
    ("144_model_dos.md", "모델 DoS (Model Denial of Service)"),
    ("145_owasp_llm_top_10.md", "OWASP LLM Top 10 (OWASP LLM Top 10)"),
    ("146_llm01_prompt_injection.md", "LLM01 프롬프트 인젝션 (LLM01 Prompt Injection)"),
    ("147_llm02_sensitive_info.md", "LLM02 민감 정보 노출 (LLM02 Sensitive Information Disclosure)"),
    ("148_llm06_excessive_agency.md", "LLM06 과도한 에이전시 (LLM06 Excessive Agency)"),
    ("149_llm10_unbounded_consumption.md", "LLM10 무제한 소비 (LLM10 Unbounded Consumption)"),
    ("150_ai_red_teaming.md", "AI 레드팀 (AI Red Teaming)"),
    ("151_agent_security.md", "에이전트 보안 — 권한 통제·가드레일 (Agent Security)"),
    ("152_agent_sandbox.md", "에이전트 샌드박스 격리 (Agent Sandbox)"),
    ("153_ai_watermarking.md", "AI 워터마킹 (AI Watermarking)"),
    ("154_deepfake_detection.md", "딥페이크 탐지 (Deepfake Detection)"),
    ("155_c2pa.md", "C2PA 콘텐츠 진위 표준 (C2PA Content Provenance)"),
    ("156_ai_supply_chain.md", "AI 공급망 보안 (AI Supply Chain Security)"),
    ("157_pipa.md", "개인정보보호법 — 수집·이용·제공·파기 (Personal Data Protection Act)"),
    ("158_pipa_2023.md", "개인정보보호법 2023 개정 — 마이데이터·과징금 (PIPA 2023 Amendment)"),
    ("159_mydata.md", "전송 요구권·마이데이터 (Data Portability MyData)"),
    ("160_gdpr.md", "GDPR — 동의·잊혀질 권리·DPO (GDPR)")
]

template = """---
title: "{title}"
date: 2026-07-05
tags:
  - cspe-security
weight: {weight}
---

## Ⅰ. 개요
- **정의**: {def_text}
- **배경/필요성**: {bg_text}
- **출제 의도**: {intent_text}

## Ⅱ. 구성요소
```text
+-------------------+       +-------------------+
|   컴포넌트 1      | ----> |   컴포넌트 2      |
+-------------------+       +-------------------+
| - 기능 1          |       | - 기능 1          |
| - 기능 2          |       | - 기능 2          |
+-------------------+       +-------------------+
```
| 구성요소 | 설명 | 비유 |
|---|---|---|
| {comp1} | {comp1_desc} | {comp1_meta} |
| {comp2} | {comp2_desc} | {comp2_meta} |
| {comp3} | {comp3_desc} | {comp3_meta} |

> 요약: {comp_summary}

## Ⅲ. 절차
```text
+-----------+    +-----------+    +-----------+    +-----------+
| 1. 준비   | -> | 2. 실행   | -> | 3. 검증   | -> | 4. 완료   |
+-----------+    +-----------+    +-----------+    +-----------+
```
1. **준비**: 사전 단계 분석 및 설계 수행함
2. **실행**: 계획된 절차에 따라 핵심 로직 실행함
3. **검증**: 처리 결과의 무결성 및 정합성 검증함
4. **완료**: 최종 결과물 산출 및 사후 관리 수행함

> 요약: {proc_summary}

## Ⅳ. 문제점
- **문제 1**: 기존 시스템과의 호환성 부족으로 인한 적용 지연 문제 발생함
- **문제 2**: 보안 관리 체계 미흡으로 인한 데이터 유출 위험 존재함
- **문제 3**: 전문 인력 부족 및 초기 구축 비용 부담으로 인한 도입 한계임

## Ⅴ. 개선방안
- **단기 방안**: 호환성 확보를 위한 인터페이스 표준화 및 API 개발 적용함
- **중기 방안**: 통합 보안 관제 시스템 구축 및 암호화 강화로 보안 위협 대응함
- **장기 방안**: 사내 전문 인력 양성 프로그램 운영 및 단계적 투자 계획 수립함

## Ⅵ. 전망
- 클라우드 및 AI 기술 발전과 융합되어 보안성 및 효율성이 극대화될 전망임
- 관련 규제 완화 및 글로벌 표준화가 진행됨에 따라 도입이 가속화될 것으로 예상됨
"""

def_texts = {
    "121_dspm.md": "클라우드 환경에서 중요 데이터의 위치, 흐름, 권한을 파악하여 데이터 보안 상태를 관리하는 체계임",
    "122_cloud_native_security_4c.md": "클라우드 네이티브 환경의 보안을 Code, Container, Cluster, Cloud 4개 계층으로 나누어 방어하는 전략임",
    "123_container_image_scan.md": "컨테이너 이미지 내의 OS 패키지, 라이브러리 등에 존재하는 알려진 보안 취약점을 식별하는 도구 및 과정임",
    "124_opa_gatekeeper.md": "쿠버네티스 환경에서 OPA를 통해 인가 및 admission 제어 정책을 적용하는 엔진임",
    "125_falco_runtime.md": "클라우드 네이티브 환경에서 비정상적인 동작이나 위협을 실시간으로 탐지하는 런타임 보안 도구임",
    "126_seccomp_apparmor.md": "리눅스 커널 수준에서 프로세스의 시스템 콜 및 파일 접근 권한을 제한하여 시스템을 보호하는 보안 모듈임",
    "127_namespace_cgroup.md": "리눅스 환경에서 프로세스 자원을 격리하고 사용량을 제한하는 컨테이너 핵심 기술임",
    "128_rootless_container.md": "컨테이너 데몬과 런타임을 root 권한 없이 실행하여 호스트 시스템의 권한 탈취 위험을 최소화하는 기술임",
    "129_csap.md": "공공기관에 클라우드 서비스 제공 시 보안성을 검증하기 위해 등급을 나누어 평가하는 인증 제도임",
    "130_supply_chain_security.md": "소프트웨어 개발, 배포, 운영 전 과정에서 SBOM 및 VEX를 활용하여 공급망 위협을 통제하는 체계임",
    "131_slsa.md": "소프트웨어 공급망의 무결성을 보장하기 위해 구글이 제안한 단계별 보안 프레임워크임",
    "132_artifact_signing.md": "컨테이너 이미지 및 소프트웨어 아티팩트의 무결성과 출처를 보장하기 위해 디지털 서명을 적용하는 기술임",
    "133_secrets_management.md": "API 키, 비밀번호 등 민감한 자격 증명 정보를 안전하게 저장, 관리, 접근 통제하는 솔루션임",
    "134_ai_security_threat.md": "AI 시스템의 학습, 추론, 운영 등 전 주기에 걸쳐 발생하는 계층별 보안 위협 체계임",
    "135_prompt_injection.md": "악의적인 프롬프트를 입력하여 LLM이 설계된 지침을 무시하고 공격자의 의도대로 동작하게 만드는 공격임",
    "136_indirect_prompt_injection.md": "LLM이 참조하는 외부 문서에 악성 프롬프트를 숨겨두어 간접적으로 시스템을 조작하는 공격임",
    "137_jailbreak_attack.md": "AI 모델에 설정된 안전 가드레일을 우회하여 금지된 콘텐츠나 악의적인 답변을 유도하는 공격임",
    "138_prompt_leakage.md": "LLM에 입력된 시스템 프롬프트나 민감한 지침을 외부로 유출시키는 공격임",
    "139_model_inversion.md": "AI 모델의 출력 결과와 API 접근을 통해 모델이 학습한 원본 데이터의 특성을 재구성하는 공격임",
    "140_model_extraction.md": "AI 모델의 입력-출력 쌍을 대량으로 수집하여 원본과 유사한 기능을 하는 복제 모델을 생성하는 공격임",
    "141_data_poisoning.md": "AI 모델의 학습 데이터에 악의적인 노이즈를 주입하여 판단 결과를 조작하는 공격임",
    "142_backdoor_attack.md": "특정 트리거 조건에서만 오작동하도록 모델 학습 단계에서 숨겨진 악의적 패턴을 삽입하는 공격임",
    "143_adversarial_example.md": "인간은 인식할 수 없는 미세한 노이즈를 입력 데이터에 추가하여 AI 모델의 오분류를 유발하는 공격임",
    "144_model_dos.md": "AI 모델에 연산 비용이 매우 높은 복잡한 입력을 지속 전송하여 자원을 고갈시키는 공격임",
    "145_owasp_llm_top_10.md": "OWASP에서 선정한 LLM 애플리케이션 개발 및 운영 시 발생할 수 있는 상위 10대 보안 위협임",
    "146_llm01_prompt_injection.md": "사용자 입력이 시스템 프롬프트를 무력화하여 의도치 않은 동작을 유발하는 OWASP 1위 취약점임",
    "147_llm02_sensitive_info.md": "LLM이 생성한 응답에 학습 데이터나 PII 등 보호되어야 할 민감 정보가 노출되는 취약점임",
    "148_llm06_excessive_agency.md": "LLM 에이전트가 외부 시스템 연동 시 과도한 권한을 부여받아 예기치 않은 피해를 유발하는 취약점임",
    "149_llm10_unbounded_consumption.md": "API 호출 시 토큰 소비량에 제한을 두지 않아 과도한 과금이나 리소스 고갈이 발생하는 취약점임",
    "150_ai_red_teaming.md": "AI 시스템의 잠재적 취약점, 편향성 문제를 식별하기 위해 공격자 관점에서 결함을 찾는 평가 방법임",
    "151_agent_security.md": "자율 AI 에이전트의 오작동 및 악용을 방지하기 위해 권한 통제 및 안전 가드레일을 적용하는 보안 기술임",
    "152_agent_sandbox.md": "AI 에이전트가 외부 환경에 영향을 주지 못하도록 안전하게 격리된 환경에서 실행되게 하는 기술임",
    "153_ai_watermarking.md": "AI가 생성한 콘텐츠에 보이지 않는 식별 정보를 삽입하여 AI 생성물임을 증명하는 기술임",
    "154_deepfake_detection.md": "AI 기술로 합성된 영상, 음성 등 딥페이크 콘텐츠의 진위 여부를 판별하고 탐지하는 기술임",
    "155_c2pa.md": "디지털 콘텐츠의 생성부터 배포까지의 출처와 이력을 암호화하여 투명하게 추적하는 개방형 표준임",
    "156_ai_supply_chain.md": "데이터 수집부터 배포에 이르는 AI 개발/운영 전 과정에 걸쳐 인프라의 안전성을 보장하는 체계임",
    "157_pipa.md": "개인정보의 수집, 이용, 제공, 파기 등 전 생애주기에 걸친 처리 기준을 규정한 기본법임",
    "158_pipa_2023.md": "전송요구권 도입, 과징금 산정 기준 변경 등을 반영하여 2023년에 전면 개정된 개인정보보호법임",
    "159_mydata.md": "정보주체가 본인의 개인정보를 본인 또는 제3자에게 전송해 줄 것을 요구하는 마이데이터 권리임",
    "160_gdpr.md": "EU 시민의 개인정보 보호 강화를 위해 동의 강화, 잊힐 권리 등을 포함하여 제정된 규정임"
}

out_dir = "/home/user/study/content/cspe/05_security"
os.makedirs(out_dir, exist_ok=True)

for i, (filename, raw_title) in enumerate(files_data):
    weight = i + 121
    title_str = raw_title.strip()

    def_text = def_texts.get(filename, "보안 체계를 강화하고 데이터 유출 및 외부 공격에 대비하기 위한 핵심 기술 및 관리 방안임")

    comp1 = "식별/탐지"
    comp1_desc = "보안 위협 요소 및 자산 식별함"
    comp1_meta = "CCTV"

    comp2 = "통제/보호"
    comp2_desc = "위협으로부터 자산 보호 및 접근 통제함"
    comp2_meta = "보안요원"

    comp3 = "대응/복구"
    comp3_desc = "사고 발생 시 신속한 대응 및 복구 수행함"
    comp3_meta = "구조대"

    comp_summary = "자산의 안전한 보호를 위해 탐지, 보호, 대응의 유기적인 연계가 필요함"
    proc_summary = "체계적인 보안 절차 수행을 통해 시스템 안정성 확보 및 사고 피해 최소화 가능함"

    content = template.format(
        title=title_str,
        weight=weight,
        def_text=def_text,
        bg_text="디지털 전환 가속화 및 AI/클라우드 기술 확산으로 인해 신종 보안 위협이 증가하여 체계적인 대응 전략이 필요함",
        intent_text="해당 보안 기술/정책의 개념과 동작 원리를 이해하고, 최신 위협에 대응하기 위한 실무 적용 방안을 묻기 위함",
        comp1=comp1, comp1_desc=comp1_desc, comp1_meta=comp1_meta,
        comp2=comp2, comp2_desc=comp2_desc, comp2_meta=comp2_meta,
        comp3=comp3, comp3_desc=comp3_desc, comp3_meta=comp3_meta,
        comp_summary=comp_summary,
        proc_summary=proc_summary
    )

    filepath = os.path.join(out_dir, filename)
    with open(filepath, "w") as f:
        f.write(content)

print(f"Created 40 files in {out_dir}")
