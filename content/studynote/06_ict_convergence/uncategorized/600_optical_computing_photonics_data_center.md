+++
title = "600. 광 컴퓨팅 포토닉스 데이터 센터 (Optical Computing Photonics Data Center)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 실리콘 포토닉스(Silicon Photonics) 기반 CPO(Co-Packaged Optics)와 MZI(Mach-Zehnder Interferometer) 연산을 활용해, 전기 신호 변환 없이 광 도메인에서 직접 행렬곱·스위칭·메모리 접근을 수행하여 Tbps/mm급 대역폭 밀도와 pJ/bit급 에너지 효율을 달성하는 차세대 데이터센터 아키텍처
> 2. **가치**: 800G/1.6T→3.2T 광 트랜시버, 1µm 이하의 광-전기 변환 latency 제거, GPU/ASIC 패키지당 100Tbps급 optical I/O (Ayar Labs TeraPHY, Intel Silicon Photonics), 데이터센터 PUE 1.1 이하 + 광 스위칭 기반 재구성 네트워크로 CapEx/OpEx 동시 절감
> 3. **판단 포인트**: 실리콘 포토닉스 공정 yield vs CMOS 호환성, 레이저 광원(Quantum Dot/DML/EML) 통합 방식, 광 패키징(Thermal, Polarization, Coupling loss) 신뢰성, 광 회로 스위치(OCS) vs 전기 패킷 스위치 트래픽 모델링, 광 컴퓨팅의 정밀도(FP16/INT8) 한계와 전자-광자 분업 아키텍처 경계 설정

---

## Ⅰ. 개요 및 필요성

기존 데이터센터는 Nvidia NVLink(900GB/s), PCIe Gen6(64GT/s), 800G 이더넷까지 "구리-광 변환-구리"의 직렬화(serialization-deserialization) 구조로 진화해 왔으나, AI/HPC 워크로드(LLM, 추천 시스템, HPC 시뮬레이션)에서 GPU/ASIC 간 collective communication(all-reduce, all-to-all)이 전체 학습 시간의 30~60%를 차지하면서 **메모리 월(Memory Wall), 인터커넥트 월(Interconnect Wall), 전력 월(Power Wall)** 의 3중 장벽이 도래했습니다. 

예를 들어, GPT-4급 모델 학습에서 H100 8,000장 클러스터는 400Gbps InfiniBand NDR당 30W의 광 트랜시버를 1,000개 이상 운용하여 트랜시버 전력만 약 30kW가 소모되며, 신호 왜곡을 막기위해 DSP(SerDes)가 1포트당 5~8W를 추가 소모합니다. 결국 **프로세서에서 copper가 끝나는 지점(EOB: Electrical-Optical Boundary)이 시스템 병목**이 됩니다.

광 컴퓨팅 포토닉스 데이터센터는 이를 두 축으로 해결합니다:
- **광 인터커넥트(Optical Interconnect)**: 패키지 내부/보드/랙/팟(Pod) 단위 광 I/O 통합
- **광 연산(Photonic Computing)**: MZI mesh, 마이크로링 변조기, 광-광 비선형소자(MRR nonlinearity, PPLN, SOA-XGM)를 활용한 in-domain 연산

```text
[기존 전기 도메인 데이터센터]
CPU/GPU ──┬── PCB 트레이스 (Cu) ── Retimer/DSP ── 광모듈 (QSFP-DD/OSFP) ── MPO/MTP 광케이블 ── ToR 스위치 ── Leaf/Spine ── 광모듈 ── 다른 GPU
          │   [25mm ~ 500mm]      [1~5W/port]    [수 mm ~ 수십 m]                  [1~10m]      [수십 m]
          └────────────────────────────────────────────────────────────────────────────────────────
                              ◀── 직렬화/디직렬화(SerDes) 4~6회 반복, 누적 지연 500~1500ns ──▶
                              ◀── 광전변환(O/E) - 전기처리 - 광전변환(E/O) 반복 ──▶

[광 컴퓨팅 포토닉스 데이터센터 (목표 아키텍처)]
┌──────────────────────────────────────── 데이터센터 팟(Pod) ────────────────────────────────────────┐
│                                                                                                    │
│  ┌──────────────┐   광 I/O Chiplet   ┌──────────────┐   Photonic        ┌──────────────┐         │
│  │  GPU/ASIC    │◀── TeraPHY/Aura ──▶│ Silicon      │◀── Waveguide ───▶│ Photonic     │         │
│  │  (H200/B200) │   (1pJ/bit)        │ Photonic     │   on Interposer   │ Compute Mesh │         │
│  │              │   64~128ch × 32G   │ Interposer   │   (SiN/SOI)       │ (MZI array)  │         │
│  └──────────────┘                    │ + WDM Mux    │                   └──────────────┘         │
│         ▲                            └──────┬───────┘                            ▲               │
│         │                                   │                                    │               │
│         │       ╔═══════════════════ Photonic Fabric (OCS-based) ══════════════════╗              │
│         │       ║   MEMS/MZI Optical Circuit Switch (ns~µs 단위 회로 재구성)        ║              │
│         └───────╫───────◀────── Optical Waveguide / Fiber ◀─────────────────────╫──────────────┘
│                 ║   DWDM 32~96λ × 32G NRZ/PAM4 → 1~3 Tbps/포트로 확장                ║
│                 ╚══════════════════════════════════════════════════════════════════╝
└────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

광 컴퓨팅 포토닉스 데이터센터는 "전기 신호는 반드시 짧게, 광 신호는 광 도메인 안에서 길고 넓게 처리" 한다는 전제하에, **데이터가 변환되는 경계(EOB)를 패키지 내부로 끌어내려 1,000배 더 많은 대역폭을 같은 전력으로** 제공하는 패러다임 전환입니다.

- **📢 섹션 요약 비유**: 기존 데이터센터가 "택배 기사가 매번 우체국에서 짐을 풀었다 다시 포장하는" 구조라면, 광 컴퓨팅 데이터센터는 **"도청 개방형 파이프라인"** 처럼, 광자가 패키지에서 나와 라우터/메모리/연산 코어에 도달할 때까지 단 한 번도 상자에서 꺼내지 않고 통째로 흘려보내는 구조입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

광 컴퓨팅 포토닉스 데이터센터는 5계층 스택으로 구성됩니다.

```text
[광 컴퓨팅 포토닉스 데이터센터 - 5계층 아키텍처]
═══════════════════════════════════════════════════════════════════════════════════════════════════
Tier 1: Photonic Compute (광 연산 유닛)
  - Photonic Tensor Core (PTC) : MZI mesh + MRR(마이크로링) 가중치 인코딩
  - Photonic Activation Unit     : SOA-XGM, EAM 흡수변조, Microring Saturable Absorber
  - Photonic Memory Readout     : SiN 마이크로링 뱅크 + Drop Port
═══════════════════════════════════════════════════════════════════════════════════════════════════
Tier 2: Optical I/O Chiplet (CPO/Co-Packaged Optics)
  - TeraPHY (Ayar Labs) : 64 optical port × 32Gbps NRZ = 2.048 Tbps in 9mm²
  - Intel SiPh            : 8λ DWDM × 50G PAM4 = 400G/포듈
  - Lightmatter Passage : PCIe Gen5 optical bridge
═══════════════════════════════════════════════════════════════════════════════════════════════════
Tier 3: Photonic Interconnect Fabric (광 스위칭 패브릭)
  - Optical Circuit Switch (OCS) : MEMS 3D-mirror / MZI 2×2 array
  - Wavelength Selective Switch (WSS) : 1×N 분기 + λ별 라우팅
  - Optical Top-of-Rack (Optical ToR) : Leafless / Optical Direct-Connect
═══════════════════════════════════════════════════════════════════════════════════════════════════
Tier 4: Hybrid Control Plane (하이브리드 제어 평면)
  - SDN Controller (ONOS/OpenDaylight) : 전기 제어 + 광 회로 설정 오케스트레이션
  - Photonic Resource Manager (PRM)   : λ 할당, 빔 포인팅, 모니터링 PD feedback
  - Thermal/Power Co-Manager         : MZI bias drift 보상, 레이저 APC
═══════════════════════════════════════════════════════════════════════════════════════════════════
Tier 5: Workload Orchestration (워크로드 오케스트레이션)
  - Job-aware Topology Reconfiguration (Google Jupiter-style)
  - Collective-aware Optical Bypass
  - Photonic-aware Scheduler (K8s + Photonic Resource Plugin)
═══════════════════════════════════════════════════════════════════════════════════════════════════
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **실리콘 포토닉스 트랜시버 (SiPh Transceiver)** | 전기↔광 변환, 변조/복조 | SOI(Silicon-On-Insulator) 도파로 + MZM/MRR 변조기, 1310/1550nm CW 레이저(DFB/EML/Quantum Dot), Ge/Si 광검출기(PD/APD), 50G PAM4 / 100G PAM4 / 200G coherent |
| **CPO (Co-Packaged Optics)** | 패키지 단 광 I/O | OSFP/QSFP-DD 모듈을 ASIC 패키지 기판 위 또는 인접 interposer에 직접 실장. Broadcom Bailly(51.2T CPO 스위치), Intel Falcon Mesa(1.6T CPO), Marvell COLORZ 800 등. 거리 50mm 이하, **소비전력 5~7W/lane → 1.5~2.5W/lane** (약 50~70% 절감) |
| **광 회로 스위치 (OCS)** | 광-광(OOO) 회로 단위 스위칭 | Calient/MEMS 3D-mirror(스위칭 시간 10~25ms), MZI-based fast OCS(µs 단위), Polatis/WaveShaper(WSS). 패킷 단위 X (스토리지가 없음), 토폴로지 단위 ○ |
| **Photonic Compute Core** | 광 도메인 행렬곱 | Reck decomposition 기반 MZI mesh로 N×N unitary 행렬 구현. 입력은 Mach-Zehnder Modulator(MZM) 전압 → 인코딩, 가중치는 thermo-optic phase shifter(Heater)로 bias, 출력은 balanced PD에서 광전류 측정 → 곱셈 누산. 예: Lightmatter ENVISE(96×96 photonic MAC, 2.5pJ/MAC) |
| **WDM/DWDM 멀티플렉서** | 단일 광섬유 다중화 | Arrayed Waveguide Grating(AWG), Echelle Grating, MRR Drop filter. 32λ × 32Gbps = 1Tbps/섬유 → 96λ × 100G PAM4 = 9.6Tbps/섬유 (CoreScale급) |
| **Quantum Dot / DFB 레이저** | 광원(On-chip/Off-chip) | III-V QD on Si(Intel 300mm 실리콘 포토닉스 라인), 1310nm O-band, 파장 안정성 ±0.5nm, TOSA/External Cavity Laser(ECL) 형태로 실리콘 기판 위 hybrid integration |
| **Photonic Memory Subsystem** | 광 메모리/광-메모리 I/O | silicon nitride(SIN/SiN) waveguides + MRR bank로 optical cache, MRAM/ReRAM/PCM과 광 readout 결합. Lightmatter Passage M1000 4Tbps photonic interconnect |

**핵심 원리 1 - MZI(Mach-Zehnder Interferometer) 연산 원리**

```
        ───►[분배 50:50]──── [상위 arm θ₁] ────┐
I_in ──┤                                ├─[50:50]────► I_out
        ───►[분배 50:50]──── [하위 arm θ₂] ────┘

        sin²((θ₁-θ₂)/2) = 투과율 T
        θ₁ = α·V₁ (MZM/P phase shifter), θ₂ = α·V₂ (가중치)
        ▶ 2×2 unitary(회전) 연산의 building block
        ▶ N개 직렬 연결 시 N+1개 MZI로 N×N unitary(U(2ⁿ) Bloch sphere) 구현 (Reck 1994)
        ▶ Deep Learning의 Fully-Connected 가중치 행렬 W = W_diag · U_(unitary) 로 분해해 인코딩
```

**핵심 원리 2 - CPO(Co-Packaged Optics)와 Pluggable 대비 비교**

- Pluggable QSFP-DD800: ASIC ↔ 모듈 50~80mm 트레이스, 16W/포듈, 0.5~1.0pJ/bit(광전변환 포함)
- CPO 1.6T: ASIC과 5~10mm 거리에 photonic interposer, 4~5W/포듈, **0.2~0.4pJ/bit** (실리콘 포토닉스 N=8 lane × 200G PAM4 기준)

**핵심 원리 3 - 광 스위치의 3가지 계층**
- OCS(Optical Circuit Switch): µs~ms, 회로 단위, 패킷 손실 X
- WSS(Wavelength Selective Switch): µs, λ별 라우팅, OCS보다 빠름
- OPS(Optical Packet Switch): ns, 하지만 광 메모리 부재로 상용화 미성숙 (실험실 단계)

**핵심 원리 4 - 광-전 하이브리드 워크플로우**
- **Compute-bound 작업**: GPU 내부 텐서코어(Blackwell 5세대) + 외부 광 매트릭스(Photonic Tensor Core)
- **Communication-bound 작업**: All-Reduce/All-to-All → GPU ↔ Optical Fabric ↔ Photonic Switch ↔ 다른 GPU
- **Memory-bound 작업**: HBM → On-chip photonic interconnect(MRR bank) → 다른 패키지 HBM (CXL/UALink over Photonics)

- **📢 섹션 요약 비유**: MZI mesh는 **"빛이 거울과 프리즘을 거치며 위상이 누적되는 라우팅 미로"** 이고, CPO는 **"CPU 옆에 다리(bus) 대신 텔레포트(wormhole)를 붙이는 것"** 입니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **광 컴퓨팅 포토닉스 데이터센터** | **기존 전기 도메인 데이터센터** | **Quantum Optical Data Center (연구단계)** |
| :--- | :--- | :--- | :--- |
| **대역폭 밀도** | 1~10 Tbps/mm (waveguide + WDM) | 0.1~0.5 Tbps/mm (SerDes + PCB) | 1~100 Tbps/mm (single-photon level) |
| **에너지 효율** | 0.2~1.0 pJ/bit (포토닉 I/O), 2~5 pJ/MAC (광 텐서코어) | 5~15 pJ/bit (DSP+SerDes), 100~500 pJ/MAC (H100 tensor core) | 0.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 600 / 800

<- **이전**: [599. 뉴로모픽 칩 신경망 하드웨어](/knowledge-base/studynote/06_ict_convergence/uncategorized/599_neuromorphic_chip_neural_network_hardware/)
**다음**: [601. 에너지 하베스팅 저전력 IoT 전원](/knowledge-base/studynote/06_ict_convergence/uncategorized/601_energy_harvesting_low_power_iot_supply/) ->

---
