+++
weight = 9999
title = "03. 데이터통신/네트워크 키워드 목록"
date = "2026-03-04"
[extra]
categories = "studynote-network"
+++
[[267_weight_bias_activation|weight]] = 9999

# [[001_dikw_pyramid|데이터]]통신 / 네트워크 키워드 목록 (1,200+ 심화 확장판)

정보통신기술사·컴퓨터응용시스템기술사 및 전문 엔지니어를 위한 [[001_dikw_pyramid|데이터]]통신/네트워크 전 영역 핵심 및 심화 키워드 1,200선입니다.

---

## 1. [[001_dikw_pyramid|데이터]]통신 기초 및 [[130_signal|신호]]처리 (70개)
1. [[001_데이터통신_시스템_구성요소|데이터통신 시스템 구성요소]] (단말장치 DTE, [[001_dikw_pyramid|데이터]]회선종단장치 DCE, 통신제어장치 CCU)
2. [[002_정보처리장치|정보처리장치]] (Host Computer, Front-End Processor FEP)
3. [[003_아날로그_신호_vs_디지털_신호|아날로그 신호]] (연속적, 증폭기) vs 디지털 [[130_signal|신호]] (이산적, 리피터)
4. [[004_배드보_비트레이트|배드보]] (Baud Rate, 변조 속도) vs [[073_bit|비트]]레이트 ([[086_fenwick_tree|Bit]] Rate, 전송 속도)
5. [[005_비트_시간_심볼_시간|비트 시간]] ([[005_비트_시간_심볼_시간|Bit Duration]]) / 심볼 시간 (Symbol Duration)
6. 아날로그 통신 vs 디지털 통신
7. [[007_기저대역_대역통과_전송|기저대역 전송]] ([[007_기저대역_대역통과_전송|Baseband Transmission]]) / 대역통과 전송 (Broadband Transmission)
8. [[008_단방향_반이중_전이중|단방향]] ([[406_linear_programming_simplex|Simplex]]) / 반이중 (Half-Duplex) / 전이중 (Full-Duplex)
9. [[009_직렬_전송_vs_병렬_전송|직렬 전송]] ([[009_직렬_전송_vs_병렬_전송|Serial]]) vs [[430_index_fast_full_scan|병렬]] 전송 (Parallel)
[[489_raid_10_hybrid|10]]. [[010_동기식_비동기식_전송|동기식 전송]] ([[010_동기식_비동기식_전송|Synchronous]]) vs 비동기식 전송 (Asynchronous)
[[308_static_dynamic_nat_pat_port_address_translation|11]]. 비동기식 전송 - 시작/정지 [[073_bit|비트]] (Start/Stop [[086_fenwick_tree|Bit]]), [[184_framing_mechanism|프레이밍]] 에러
12. [[010_동기식_비동기식_전송|동기식 전송]] - 문자 동기방식 (SYN, [[019_bsc|BSC]]), [[073_bit|비트]] 동기방식 ([[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]], [[216_hdlc_high_level_data_link_control|HDLC]])
13. [[140_bandwidth|대역폭]] ([[140_bandwidth|Bandwidth]]), [[140_bandwidth|대역폭]]-효율성 [[083_relationship_in_er_model|관계]]
14. [[139_throughput|처리량]] ([[139_throughput|Throughput]]) / 굿풋 (Goodput)
15. [[015_지연_데이터_관점|지연]] ([[141_latency|Latency]]/Delay) - [[001_dikw_pyramid|데이터]] 관점
16. [[016_전파_지연|전파 지연]] ([[016_전파_지연|Propagation Delay]]) - 거리/속도
17. [[017_전송_지연|전송 지연]] ([[017_전송_지연|Transmission Delay]]) - 패킷길이/[[140_bandwidth|대역폭]]
18. [[018_큐잉_지연|큐잉 지연]] ([[018_큐잉_지연|Queueing Delay]]) - 라우터 버퍼
19. [[019_처리_지연|처리 지연]] ([[019_처리_지연|Processing Delay]]) - 헤더 검사, [[339_routing_overview_best_path_selection|라우팅]]
20. [[020_나이퀴스트_채널_용량|나이퀴스트 채널 용량]] ([[020_나이퀴스트_채널_용량|Nyquist Capacity]]) - 무잡음 채널, C = 2B log2(M)
21. [[021_샤논의_채널_용량|샤논의 채널 용량]] ([[021_샤논의_채널_용량|Shannon Capacity]]) - 잡음 채널, C = B log2(1 + S/N)
22. [[022_심볼_상호_간섭_ISI|심볼 상호 간섭]] (ISI: Inter-Symbol Interference)
23. 나이퀴스트 펄스 포맷 / 아이패턴 (Eye Pattern)
24. [[024_신호_대_잡음비|신호 대 잡음비]] ([[024_신호_대_잡음비|SNR]], [[024_신호_대_잡음비|Signal-to-Noise Ratio]])
25. 감쇠 (Attenuation), 데시벨(dB) 측정
26. [[026_지연_왜곡|지연 왜곡]] ([[026_지연_왜곡|Delay Distortion]])
27. 백색 잡음 (White Noise) / 가우스 잡음
28. 충격 잡음 (Impulse Noise) / 열 잡음 (Thermal Noise)
29. [[029_상호변조_잡음|상호변조 잡음]] ([[029_상호변조_잡음|Intermodulation Noise]])
30. [[030_누화_크로스토크|누화]] ([[030_누화_크로스토크|Crosstalk]], 혼선)
31. [[031_에코_반향|에코]] (Echo, [[031_에코_반향|반향]])
32. [[032_회선_제어_규약|회선 제어 규약]] (Line Discipline)
33. 엔트 (ENQ) / 애크 (ACK) / 나크 ([[211_nak_negative_acknowledgement|NAK]]) / EOT
34. [[034_에러_검출율|에러 검출율]] ([[040_error_detection|Error Detection]] Rate)
35. 부호화 (Encoding) - Line Coding, [[042_4B5B_8B10B_블록_코딩|Block Coding]]
36. Line Coding - 단극성 (Unipolar), 극성 (Polar), 양극성 (Bipolar)
37. NRZ (Non-[[038_RZ_Return_to_Zero|Return to Zero]]) - NRZ-L, NRZ-I
38. RZ ([[038_RZ_Return_to_Zero|Return to Zero]]) - [[212_synchronization_mechanisms|동기화]] 장점, [[140_bandwidth|대역폭]] 증가
39. 맨체스터 (Manchester) 부호화 / 차분 맨체스터 (Differential Manchester)
40. [[162_ami_advanced_metering_infrastructure|AMI]] (Alternate Mark Inversion) / Pseudoternary
41. [[041_차분_부호화|차분 부호화]] ([[041_차분_부호화|Differential Encoding]])
42. 4B/5B, 8B/10B 부호화 ([[042_4B5B_8B10B_블록_코딩|Block Coding]])
43. B8ZS (Bipolar with 8-[[585_zero_skipping|Zero]] Substitution) / HDB3 (High-Density Bipolar 3 zeros)
44. 변조 (Modulation) 필요성 - [[171_antenna_basic_dipole_resonance|안테나]] 크기, 주파수 [[071_다중화_Multiplexing|다중화]]
45. 진폭 편이 변조 (ASK, [[045_진폭_편이_변조_ASK|Amplitude Shift Keying]])
46. 주파수 편이 변조 (FSK, [[046_주파수_편이_변조_FSK|Frequency Shift Keying]])
47. 위상 편이 변조 ([[142_psk_pre_shared_key|PSK]], Phase Shift Keying)
48. BPSK (Binary [[142_psk_pre_shared_key|PSK]], 1bit/symbol) / QPSK (Quadrature [[142_psk_pre_shared_key|PSK]], 2bit/symbol)
49. OQPSK (Offset QPSK) / [[009_process_innovation|Pi]]/4 QPSK
50. M진 [[142_psk_pre_shared_key|PSK]] (8PSK, 16PSK)
51. [[051_직교_진폭_변조_QAM|직교 진폭 변조]] (QAM, Quadrature Amplitude Modulation) - ASK+[[142_psk_pre_shared_key|PSK]] 혼합
52. 16-QAM, 64-QAM, 256-QAM, 1024-QAM
53. [[053_성상도_Constellation_Diagram|성상도]] ([[053_성상도_Constellation_Diagram|Constellation Diagram]]) - 진폭과 위상 표시
54. [[054_반송파_Carrier_Wave|반송파]] ([[054_반송파_Carrier_Wave|Carrier Wave]])
55. [[055_아날로그_연속파_변조_AM_FM_PM|아날로그 연속파 변조]] - AM, FM, PM
56. [[056_표본화_Sampling|표본화]] ([[056_표본화_Sampling|Sampling]]), [[056_표본화_Sampling|표본화]] 정리 ([[056_표본화_Sampling|Sampling]] Theorem)
57. [[057_에일리어싱_Aliasing|에일리어싱]] ([[057_에일리어싱_Aliasing|Aliasing]]) - [[056_표본화_Sampling|표본화]] 주파수 부족시 발생
58. [[058_폴딩_주파수_Folding_Frequency|폴딩 주파수]] ([[058_폴딩_주파수_Folding_Frequency|Folding Frequency]])
59. [[434_quantization|양자화]] ([[434_quantization|Quantization]]) - 선형/비선형
60. [[060_양자화_잡음_양자화_스텝|양자화 잡음]] ([[434_quantization|Quantization]] Noise/Error), [[434_quantization|양자화]] 스텝
61. [[061_컴팬딩_압신_mu_law_A_law|컴팬딩]] ([[061_컴팬딩_압신_mu_law_A_law|Companding]]) / 압신 - μ-law, A-law
62. [[062_펄스_부호_변조_PCM_과정|펄스 부호 변조]] ([[943_pcm_pulse_code_modulation_sampling_quantization|PCM]], Pulse [[082_process_memory_structure|Code]] Modulation) 처리 과정
63. [[063_DPCM_차분_펄스_부호_변조|DPCM]] ([[063_DPCM_차분_펄스_부호_변조|Differential PCM]]) - 차분 [[062_펄스_부호_변조_PCM_과정|펄스 부호 변조]]
64. [[064_ADPCM_적응형_차분_펄스_부호_변조|ADPCM]] ([[064_ADPCM_적응형_차분_펄스_부호_변조|Adaptive DPCM]]) - 적응형 차분 [[062_펄스_부호_변조_PCM_과정|펄스 부호 변조]]
65. [[065_델타_변조_DM|델타 변조]] (DM, Delta Modulation) - 1비트 전송
66. [[066_적응형_델타_변조_ADM|적응형 델타 변조]] ([[066_적응형_델타_변조_ADM|ADM]])
67. [[067_경사과부하_그래뉼러_잡음|경사 과부하 잡음]] ([[067_경사과부하_그래뉼러_잡음|Slope Overload Noise]]) / 그래뉼러 잡음 (Granular Noise)
68. [[068_스펙트럼_확산_Spread_Spectrum|스펙트럼 확산]] ([[068_스펙트럼_확산_Spread_Spectrum|Spread Spectrum]])
69. 직접 수열 [[954_spread_spectrum_communication_anti_jamming_cdma|확산 스펙트럼]] ([[956_dsss_direct_sequence_spread_spectrum_chipping_code|DSSS]], [[176_direct_addressing|Direct]] Sequence [[068_스펙트럼_확산_Spread_Spectrum|Spread Spectrum]]) - PN 시퀀스
70. [[955_fhss_frequency_hopping_spread_spectrum_bluetooth|주파수 도약]] [[954_spread_spectrum_communication_anti_jamming_cdma|확산 스펙트럼]] ([[955_fhss_frequency_hopping_spread_spectrum_bluetooth|FHSS]], Frequency Hopping [[068_스펙트럼_확산_Spread_Spectrum|Spread Spectrum]])

## 2. [[071_다중화_Multiplexing|다중화]] 및 다중접속 기술 (50개)
71. [[071_다중화_Multiplexing|다중화]] ([[071_다중화_Multiplexing|Multiplexing]]) 개념 및 특징
72. [[072_공간_분할_다중화_SDM|공간 분할 다중화]] (SDM, Space [[411_division_operation|Division]] [[071_다중화_Multiplexing|Multiplexing]])
73. [[073_주파수_분할_다중화_FDM|주파수 분할 다중화]] (FDM, Frequency [[411_division_operation|Division]] [[071_다중화_Multiplexing|Multiplexing]])
74. [[074_보호_대역_Guard_Band|보호 대역]] ([[946_guard_band_fdm_adjacent_channel_interference|Guard Band]])
75. [[075_시분할_다중화_TDM|시분할 다중화]] (TDM, Time [[411_division_operation|Division]] [[071_다중화_Multiplexing|Multiplexing]]) (타임디비전 멀티플렉싱)
76. [[076_동기식_시분할_다중화|동기식 시분할 다중화]] ([[076_동기식_시분할_다중화|Synchronous TDM]]) - 정적 타임슬롯 할당
77. 비동기식/통계적 [[075_시분할_다중화_TDM|시분할 다중화]] (Asynchronous/Statistical TDM) - 동적 할당
78. [[078_비트_교차_워드_교차|비트 교차]] ([[078_비트_교차_워드_교차|Bit Interleaving]]) / [[075_word|워드]] 교차 ([[075_word|Word]] Interleaving)
79. [[079_광파장_분할_다중화_WDM|광파장 분할 다중화]] (WDM, Wavelength [[411_division_operation|Division]] [[071_다중화_Multiplexing|Multiplexing]])
80. 저밀도 파장 분할 [[071_다중화_Multiplexing|다중화]] (CWDM, Coarse WDM)
81. 고밀도 파장 분할 [[071_다중화_Multiplexing|다중화]] (DWDM, Dense WDM) - EDFA 증폭기 사용
82. [[082_코드_분할_다중화_CDM|코드 분할 다중화]] (CDM, [[082_process_memory_structure|Code]] [[411_division_operation|Division]] [[071_다중화_Multiplexing|Multiplexing]])
83. [[083_직교성_Orthogonality|직교성]] ([[083_직교성_Orthogonality|Orthogonality]]) 원리
84. 직교 [[073_주파수_분할_다중화_FDM|주파수 분할 다중화]] (OFDM, Orthogonal FDM)
85. [[085_부반송파_Subcarrier|부반송파]] ([[085_부반송파_Subcarrier|Subcarrier]])
86. [[086_CP_순환_전치_GI|CP]] ([[086_CP_순환_전치_GI|Cyclic Prefix]]) / GI (Guard Interval) - ISI 방지
87. [[087_다중접속_Multiple_Access|다중 접속]] ([[087_다중접속_Multiple_Access|Multiple Access]]) 개념 ([[673_mac_message_authentication_code|MAC]] 계층 연관)
88. [[088_주파수_분할_다중접속_FDMA|FDMA]] (Frequency [[411_division_operation|Division]] [[087_다중접속_Multiple_Access|Multiple Access]])
89. [[089_시분할_다중접속_TDMA|TDMA]] (Time [[411_division_operation|Division]] [[087_다중접속_Multiple_Access|Multiple Access]]) - 슬롯 할당
90. [[957_cdma_code_division_multiple_access_dsss_orthogonality|CDMA]] ([[082_process_memory_structure|Code]] [[411_division_operation|Division]] [[087_다중접속_Multiple_Access|Multiple Access]]) - 왈시 코드 (Walsh [[082_process_memory_structure|Code]])
91. 동기식 [[957_cdma_code_division_multiple_access_dsss_orthogonality|CDMA]] vs 비동기식 [[957_cdma_code_division_multiple_access_dsss_orthogonality|CDMA]] ([[091_동기식_비동기식_CDMA_WCDMA|WCDMA]])
92. [[092_근거리_원거리_문제_CDMA_전력제어|근거리-원거리 문제]] ([[092_근거리_원거리_문제_CDMA_전력제어|Near-Far Problem]]) - [[957_cdma_code_division_multiple_access_dsss_orthogonality|CDMA]] 전력 제어
93. [[093_셀_호흡_현상|셀 호흡]] ([[093_셀_호흡_현상|Cell Breathing]]) 현상
94. [[945_ofdma_orthogonal_frequency_division_multiple_access_resource_block|OFDMA]] (Orthogonal Frequency [[411_division_operation|Division]] [[087_다중접속_Multiple_Access|Multiple Access]]) - [[752_lte_long_term_evolution_4g|LTE]], [[418_5g_embb_urllc_mmtc_slicing|5G]]
95. [[095_NOMA_비직교_다중_접속|NOMA]] ([[095_NOMA_비직교_다중_접속|Non-Orthogonal Multiple Access]]) - 비직교 [[087_다중접속_Multiple_Access|다중 접속]] ([[418_5g_embb_urllc_mmtc_slicing|5G]]/[[419_6g_ntn_thz_ris_next_gen|6G]] 기술)
96. 공간 분할 [[087_다중접속_Multiple_Access|다중 접속]] (SDMA, Space [[411_division_operation|Division]] [[087_다중접속_Multiple_Access|Multiple Access]])
97. [[097_MIMO_다중_안테나_기술|MIMO]] ([[097_MIMO_다중_안테나_기술|Multiple-Input Multiple-Output]]) 다중 [[171_antenna_basic_dipole_resonance|안테나]] 기술
98. [[098_SU_MIMO_vs_MU_MIMO|SU-MIMO]] ([[098_SU_MIMO_vs_MU_MIMO|Single User MIMO]]) vs MU-[[097_MIMO_다중_안테나_기술|MIMO]] (Multi-User [[097_MIMO_다중_안테나_기술|MIMO]])
99. [[099_Massive_MIMO_대규모_다중_안테나|Massive MIMO]] ([[099_Massive_MIMO_대규모_다중_안테나|대규모 다중 안테나]])
100. [[100_공간_다중화_Spatial_Multiplexing|공간 다중화]] ([[100_공간_다중화_Spatial_Multiplexing|Spatial Multiplexing]])
101. [[101_beamforming|빔포밍]] ([[101_beamforming|Beamforming]]) - 아날로그/디지털 [[101_beamforming|빔포밍]]
102. [[164_tdd_test_driven_development|TDD]] ([[102_tdd|Time Division Duplexing]]) - 시분할 [[456_dual_redundancy|이중화]] (업/다운링크 분리)
103. [[103_fdd|FDD]] ([[103_fdd|Frequency Division Duplexing]]) - 주파수 분할 [[456_dual_redundancy|이중화]]
104. [[104_csma|CSMA]] (Carrier Sense [[087_다중접속_Multiple_Access|Multiple Access]]) [[054_반송파_Carrier_Wave|반송파]] 감지
105. 1-Persistent, Non-Persistent, p-Persistent [[104_csma|CSMA]]
106. [[104_csma|CSMA]]/CD ([[106_CSMA_CD_유선이더넷_충돌감지|Collision Detection]]) - 유선 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]], 충돌 감지
107. [[107_잼_신호_백오프_알고리즘|잼 신호]] ([[107_잼_신호_백오프_알고리즘|Jam Signal]]) / 백오프 [[001_algorithm_definition|알고리즘]] (Backoff [[001_algorithm_definition|Algorithm]])
108. [[104_csma|CSMA]]/[[089_contract_account_smart_contract|CA]] ([[563_hash_collision_chaining_linear_probing|Collision]] Avoidance) - 무선 LAN, 충돌 회피
109. RTS/CTS (Request To Send / Clear To Send) - 은닉 노드 문제 해결
110. [[110_노출_노드_문제|노출 노드 문제]] ([[110_노출_노드_문제|Exposed Node Problem]])
111. [[111_aloha_protocol|ALOHA]] ([[111_aloha_protocol|순수 알로하]]) - 하와이 대학, 무작위 채널 접근
112. [[112_slotted_aloha|Slotted ALOHA]] - 슬롯 단위 전송, 충돌 감소
113. [[113_reservation_access|예약 방식 접속]] ([[113_reservation_access|Reservation Access]])
114. [[114_polling_access|폴링 접속]] ([[114_polling_access|Polling Access]])
115. [[115_token_passing|토큰 패싱]] ([[115_token_passing|Token Passing]]) - [[281_token_ring_ieee_802_5_token_bus_ieee_802_4|토큰 링]], 토큰 [[344_bus|버스]]
116. [[116_prma|PRMA]] (Packet Reservation [[087_다중접속_Multiple_Access|Multiple Access]])
117. [[117_dama|DAMA]] (Demand Assignment [[087_다중접속_Multiple_Access|Multiple Access]]) - [[592_satellite_communication_characteristics|위성 통신]]
118. [[118_pama|PAMA]] ([[118_pama|Pre-Assigned Multiple Access]])
119. CDMA2000 [[584_802_1x_pnac_eap_radius|1x]] / EV-DO ([[119_cdma2000_evdo|Evolution-Data Optimized]])
120. [[120_wcdma_hspa|W-CDMA]] ([[120_wcdma_hspa|Wideband CDMA]]) / HSPA (High Speed Packet Access)

## 3. 전송 [[121_transmission_media_guided_unguided|매체]] 및 물리 계층 구성 (70개)
121. [[121_transmission_media_guided_unguided|매체]]([[121_transmission_media_guided_unguided|Media]]) 구분: 유도 [[121_transmission_media_guided_unguided|매체]] (Guided) vs 비유도 [[121_transmission_media_guided_unguided|매체]] (Unguided)
122. [[122_twin_lead_cable|평행 2선식 케이블]] ([[122_twin_lead_cable|Twin-lead cable]])
123. [[123_twisted_pair_cable|꼬임 쌍선 케이블]] ([[123_twisted_pair_cable|Twisted Pair Cable]])
124. [[124_unshielded_twisted_pair|UTP]] ([[124_unshielded_twisted_pair|Unshielded Twisted Pair]])
125. [[570_stp_vs_mtp|STP]] ([[125_shielded_foil_twisted_pair|Shielded Twisted Pair]]) / [[482_ftp_file_transfer_protocol|FTP]] (Foil Twisted Pair)
126. [[124_unshielded_twisted_pair|UTP]] 카테고리 (Cat 3, Cat 5, Cat 5e, Cat 6, Cat 6a, Cat 7, Cat 8)
127. [[127_coaxial_cable|동축 케이블]] ([[127_coaxial_cable|Coaxial Cable]]) - BNC 커넥터
128. [[128_optical_fiber_cable|광섬유 케이블]] ([[128_optical_fiber_cable|Optical Fiber Cable]]) - 코어(Core), 클래딩(Cladding)
129. [[129_refractive_index_tir|굴절률]] ([[129_refractive_index_tir|Refractive Index]]), 전반사 (Total Internal Reflection)
130. [[130_multimode_step_index_fiber|멀티모드 계단형 광섬유]] ([[130_multimode_step_index_fiber|Multi-mode Step-index]])
131. [[131_multi_mode_graded_index|멀티모드 언덕형 광섬유]] ([[131_multi_mode_graded_index|Multi-mode Graded-index]])
132. [[132_single_mode_multi_mode_fiber|단일모드 광섬유]] (Single-mode Fiber, [[771_smf_upf_session_management_user_plane|SMF]]) / 다중모드 광섬유 (MMF)
133. [[136_variance|분산]] ([[133_dispersion_mode_chromatic|Dispersion]]) - 모드 [[136_variance|분산]], 파장 [[136_variance|분산]]
134. [[134_optical_amplifier_edfa_soa_raman|광증폭기]] (EDFA, [[618_soa_hardware|SOA]], 라만 증폭기)
135. [[135_optical_transmission_components|광전송 용어]] - 광원 ([[013_led|LED]], LD), 수광소자 (PIN 디오드, APD)
136. [[136_fso_free_space_optics_laser|자유 공간 광통신]] ([[900_fso_free_space_optics_hybrid_rf_backup|FSO]], Free Space Optics) / 레이저 통신
137. [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 물리 계층 표준 (IEEE 802.3 PHY)
138. 10BASE-T, 100BASE-TX ([[138_10base_t_100base_tx_fast_ethernet|Fast Ethernet]])
139. [[139_1000base_t_gigabit_ethernet|1000BASE-T]] ([[139_1000base_t_gigabit_ethernet|Gigabit Ethernet]]) - 4페어 사용, 5단계 [[564_pam|PAM]] 변조
140. 10GBASE-T / 10GBASE-SR / 10GBASE-LR
141. 40GbE / 100GbE / 400GbE / 800GbE [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]
142. MDI/MDI-X ([[142_mdi_mdix_interface|Medium Dependent Interface]])
143. [[143_auto_mdix|Auto-MDIX]] (크로스 케이블 자동 인식)
144. 케이블 배선: 다이렉트 케이블 ([[144_cable_wiring_direct_cross|T568B]]) vs 크로스오버 케이블
145. [[145_dsu_csu_digital_service_unit|DSU]] ([[145_dsu_csu_digital_service_unit|Digital Service Unit]]) / CSU (Channel [[090_service_kubernetes_network_load_balancing|Service]] Unit)
146. [[146_modem_modulator_demodulator|모뎀]] (Modem, Modulator/Demodulator)
147. [[147_cable_modem_docsis|케이블 모뎀]] ([[147_cable_modem_docsis|Cable Modem]]) / DOCSIS 표준
148. [[148_adsl_vdsl_gfast|VDSL]] ([[148_adsl_vdsl_gfast|Very high-bit-rate DSL]]) / ADSL (Asymmetric DSL) / G.fast
149. RS-232C, RS-422, RS-485 시리얼 통신 인터페이스
150. [[359_usb|USB]], IEEE 1394 ([[150_usb_ieee1394_firewire|FireWire]])
151. 베이스밴드 중계기 / 리피터 ([[151_repeater_baseband|Repeater]])
152. [[152_hub_dummy_switching_intelligent|허브]] ([[152_hub_dummy_switching_intelligent|Hub]]) - [[459_dummy_test_double|더미]] [[152_hub_dummy_switching_intelligent|허브]] ([[459_dummy_test_double|Dummy]]), 스위칭 [[152_hub_dummy_switching_intelligent|허브]], 인텔리전트 [[152_hub_dummy_switching_intelligent|허브]]
153. [[153_transceiver_mau_sfp|트랜시버]] ([[153_transceiver_mau_sfp|Transceiver]]) / MAU (Medium Attachment Unit)
154. 전파(Radio [[590_wave_ieee_802_11p_dsrc_v2x|Wave]])의 [[104_classification_analysis|분류]]: 장파/중파/단파/초단파(VHF)/극초단파(UHF)
155. [[154_radio_wave_classification|마이크로파]] ([[154_radio_wave_classification|Microwave]]) - 1GHz~300GHz
156. [[156_mmwave_millimeter_wave|밀리미터파]] ([[156_mmwave_millimeter_wave|mmWave]]) - 30GHz~300GHz
157. [[157_terahertz_thz_6g|테라헤르츠]] ([[157_terahertz_thz_6g|THz]]) - [[419_6g_ntn_thz_ris_next_gen|6G]] 통신 대상 대역
158. [[158_vlc_lifi_visible_light|가시광 통신]] ([[1021_vlc_lifi|VLC]], Visible Light Communication) / Li-Fi
159. [[159_underwater_acoustic_communication|음향 통신]] ([[159_underwater_acoustic_communication|수중 음파 통신]])
160. [[160_radio_propagation_ground_sky_space|지상파]] ([[160_radio_propagation_ground_sky_space|Ground Wave]]) / 천파 (Sky [[590_wave_ieee_802_11p_dsrc_v2x|Wave]]) / 공간파 (Space [[590_wave_ieee_802_11p_dsrc_v2x|Wave]])
161. 전리층 반사 / 대류권 [[164_scattering_reflection_radio_waves|산란]]
162. [[162_los_line_of_sight_communication|직선 가시거리 통신]] (LOS, Line-of-Sight)
163. [[163_penetration_diffraction_radio_waves|투과율]] ([[163_penetration_diffraction_radio_waves|Penetration]]) / 회절 (Diffraction)
164. [[164_scattering_reflection_radio_waves|산란]] ([[164_scattering_reflection_radio_waves|Scattering]]) / 반사 (Reflection)
165. [[165_fresnel_zone_clearance|프레넬 영역]] ([[165_fresnel_zone_clearance|Fresnel Zone]])
166. 자유 공간 경로 손실 (FSPL, Free Space Path Loss)
167. [[167_fading_large_scale_small_scale|페이딩]] ([[167_fading_large_scale_small_scale|Fading]]) - 대규모(Large-scale) [[167_fading_large_scale_small_scale|페이딩]] vs 소규모(Small-scale) [[167_fading_large_scale_small_scale|페이딩]]
168. [[168_multipath_fading_isi|다중 경로 페이딩]] ([[168_multipath_fading_isi|Multipath Fading]]) - 주파수 선택적/평탄 [[167_fading_large_scale_small_scale|페이딩]]
169. [[169_doppler_effect_fast_fading|도플러 효과]] ([[169_doppler_effect_fast_fading|Doppler Effect]]) / 고속 이동체 통신
170. [[170_diversity_system_equalizer|다이버시티 시스템]] ([[170_diversity_system_equalizer|Diversity System]]) / 경로 이퀄라이저 ([[566_equalizer_isi_inter_symbol_interference|Equalizer]])
171. [[171_antenna_basic_dipole_resonance|안테나]] ([[171_antenna_basic_dipole_resonance|Antenna]]) 기본 원리 (공진/다이폴)
172. [[172_omni_directional_vs_directional_antenna|무지향성 안테나]] (Omni-Directional) vs 지향성 [[171_antenna_basic_dipole_resonance|안테나]] (Directional)
173. [[173_isotropic_antenna_theory|등방성 안테나]] ([[173_isotropic_antenna_theory|Isotropic Antenna]])
174. [[174_antenna_gain_dbi_dbd|안테나 이득]] ([[171_antenna_basic_dipole_resonance|Antenna]] Gain, dBi, dBd)
175. 유효 등방성 복사 전력 (EIRP, Effective Isotropic Radiated [[069_type_1_2_error_statistical_power|Power]])
176. 야기우다 [[171_antenna_basic_dipole_resonance|안테나]], 파라볼라 [[171_antenna_basic_dipole_resonance|안테나]] ([[176_antenna_yagi_parabolic_patch|Parabolic]]), 패치 [[171_antenna_basic_dipole_resonance|안테나]]
177. [[177_smart_antenna_phased_array|스마트 안테나]] ([[177_smart_antenna_phased_array|Smart Antenna]]) / 위상 [[055_array|배열]] [[171_antenna_basic_dipole_resonance|안테나]] (Phased [[055_array|Array]])
178. [[178_small_cell_macro_femto|스몰셀]] ([[178_small_cell_macro_femto|Small Cell]]) / 매크로셀 ([[553_macro_micro_pico_femto_cell_topology|Macro Cell]]) / 펨토셀 (Femto Cell)
179. [[179_plc_power_line_communication|전력선 통신]] ([[896_plc_programmable_logic_controller|PLC]], [[069_type_1_2_error_statistical_power|Power]] Line Communication)
180. [[180_xpon_epon_gpon_10gpon|xPON]] ([[284_pon_passive_optical_network_vs_aon_active|Passive Optical Network]]) - EPON, GPON, 10G-[[284_pon_passive_optical_network_vs_aon_active|PON]]

## 4. [[001_dikw_pyramid|데이터]] 링크 계층 - 오류성능 및 [[295_protocol_field_tcp_udp_icmp|프로토콜]] (90개)
181. [[001_dikw_pyramid|데이터]] 링크 계층의 역할: [[184_framing_mechanism|프레이밍]], [[213_flow_control_buffer_overflow|흐름 제어]], [[188_error_control_overview|오류 제어]], 회선 제어
182. [[182_llc_logical_link_control|논리적 링크 제어]] ([[744_load_line_calibration|LLC]], Logical Link Control) - IEEE 802.2
183. [[183_mac_media_access_control|매체 접근 제어]] ([[673_mac_message_authentication_code|MAC]], [[121_transmission_media_guided_unguided|Media]] [[547_access_control_rwx|Access Control]]) - IEEE 802.3~802.[[308_static_dynamic_nat_pat_port_address_translation|11]]
184. [[184_framing_mechanism|프레이밍]] ([[184_framing_mechanism|Framing]]) 메커니즘
185. [[185_byte_counting_framing|바이트 카운트]] ([[185_byte_counting_framing|Byte Counting]]) 방식
186. [[186_character_stuffing_dle_stx_etx|플래그]]([[186_character_stuffing_dle_stx_etx|Flag]]) 방식 - 문자 삽입 (Character/[[074_byte|Byte]] Stuffing) - DLE, STX, ETX
187. [[187_bit_stuffing_flag_mechanism|비트 스터핑]] ([[187_bit_stuffing_flag_mechanism|Bit Stuffing]]) - 01111110 [[186_character_stuffing_dle_stx_etx|플래그]] 중복 방지 (5개 1 뒤에 0 삽입)
188. [[188_error_control_overview|오류 제어]] ([[188_error_control_overview|Error Control]]) 개요
189. [[189_ber_bit_error_rate|비트 에러율]] (BER, [[086_fenwick_tree|Bit]] Error Rate)
190. [[190_fec_forward_error_correction_hamming|순방향 에러 수정]] (FEC, [[235_forward_backward_chaining|Forward]] Error Correction)
191. 역방향 에러 수정 / 자동 재전송 요청 ([[949_arq_automatic_repeat_request_go_back_n_selective|ARQ]], Automatic Repeat reQuest)
192. [[192_parity_check_even_odd_block|패리티 검사]] ([[192_parity_check_even_odd_block|Parity Check]]) - 홀수/짝수, [[008_단방향_반이중_전이중|단방향]]/이차원(블록) 패리티
193. [[193_checksum_ones_complement|검사합]] ([[112_checksum|Checksum]]) - 1의 보수 합 검사 (IP/[[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/[[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 헤더에 주로 사용)
194. [[113_crc|CRC]] ([[113_crc|Cyclic Redundancy Check]], 순환 중복 검사)
195. [[195_polynomial_generator_crc|다항식]]([[195_polynomial_generator_crc|Polynomial]]) 연산 / [[087_process_state_transition|생성]] [[195_polynomial_generator_crc|다항식]] (Generator [[195_polynomial_generator_crc|Polynomial]])
196. [[113_crc|CRC]]-16, [[113_crc|CRC]]-32 ([[196_crc_standards_16_32_ccitt|Ethernet FCS]]), [[113_crc|CRC]]-CCITT
197. [[197_burst_error_detection_crc|버스트 에러]] ([[197_burst_error_detection_crc|Burst Error]]) 검출 능력 유지
198. [[111_hamming_code|해밍 코드]] ([[111_hamming_code|Hamming Code]]) - 1비트 수정 2비트 오류 검출
199. [[199_reed_solomon_code_burst_error|리드-솔로몬 코드]] ([[199_reed_solomon_code_burst_error|Reed-Solomon Code]]) - 블록 오류 정정
200. BCH 코드 / 골레이([[200_bch_golay_code_fec|Golay]]) 코드
201. [[201_convolutional_code_viterbi|길쌈 코드]] ([[201_convolutional_code_viterbi|Convolutional Code]]) - 연속 스트림, 비터비 [[001_algorithm_definition|알고리즘]]
202. [[202_turbo_code_shannon_limit|터보 코드]] ([[202_turbo_code_shannon_limit|Turbo Code]]) - 샤논 한계에 근접, [[752_lte_long_term_evolution_4g|LTE]]
203. [[203_ldpc_low_density_parity_check|LDPC]] (Low Density [[192_parity_check_even_odd_block|Parity Check]]) - [[418_5g_embb_urllc_mmtc_slicing|5G]], [[148_5g_embb_urllc_mmtc|초고속]] 정정
204. [[204_polar_code_5g_control_channel|폴라 코드]] ([[204_polar_code_5g_control_channel|Polar Code]]) - [[418_5g_embb_urllc_mmtc_slicing|5G]] 제어채널 무오류/고신뢰
205. [[205_harq_hybrid_arq_chase_combining|HARQ]] ([[205_harq_hybrid_arq_chase_combining|Hybrid ARQ]]) - FEC + [[949_arq_automatic_repeat_request_go_back_n_selective|ARQ]] 결합기술
206. Chase Combining / [[165_ir|IR]] ([[206_chase_combining_vs_incremental_redundancy|Incremental Redundancy]])
207. [[949_arq_automatic_repeat_request_go_back_n_selective|ARQ]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 종류
208. 정지-대기 [[949_arq_automatic_repeat_request_go_back_n_selective|ARQ]] ([[208_stop_and_wait_arq|Stop-and-Wait ARQ]]) - 응답 받을때까지 대기, 효율 낮음
209. [[209_go_back_n_arq_gbn|GBN ARQ]] ([[209_go_back_n_arq_gbn|Go-Back-N ARQ]]) - 오류 발생 프레임부터 재전송 (슬라이딩 윈도우)
210. [[210_sr_arq_selective_repeat|SR ARQ]] ([[210_sr_arq_selective_repeat|Selective Repeat ARQ]]) - 오류 프레임만 재전송, 수신측 [[454_buffering|버퍼링]] 복잡
211. [[211_nak_negative_acknowledgement|NAK]] ([[211_nak_negative_acknowledgement|Negative Acknowledgement]])
212. [[212_piggybacking_ack_merging|피기배킹]] ([[212_piggybacking_ack_merging|Piggybacking]]) - [[001_dikw_pyramid|데이터]] 프레임에 ACK 병합
213. [[213_flow_control_buffer_overflow|흐름 제어]] ([[421_tcp_flow_control_sliding_window_algorithm|Flow Control]]) - 수신 [[591_buffer_overflow|버퍼 오버플로우]] 방지
214. [[214_sliding_window_protocol|슬라이딩 윈도우 프로토콜]] ([[214_sliding_window_protocol|Sliding Window Protocol]]) 개념
215. [[413_tcp_window_size_flow_control_16bit|윈도우 크기]] ([[215_window_size_sender_receiver|Window Size]]), 송신/수신 윈도우
216. [[216_hdlc_high_level_data_link_control|HDLC]] (High-Level [[001_dikw_pyramid|Data]] Link Control) - [[073_bit|비트]] 동기식 [[295_protocol_field_tcp_udp_icmp|프로토콜]], ISO
217. [[216_hdlc_high_level_data_link_control|HDLC]] 프레임 구조 - [[186_character_stuffing_dle_stx_etx|플래그]], 주소, 제어, 정보, FCS
218. [[216_hdlc_high_level_data_link_control|HDLC]] 국([[218_hdlc_station_primary_secondary|Station]]) 종류 - 주국(Primary), 종국(Secondary), 혼성국(Combined)
219. [[219_nrm_arm_abm_hdlc_modes|NRM]] ([[219_nrm_arm_abm_hdlc_modes|정규 응답 모드]]) / ARM (비동기 응답 모드) / ABM (비동기 균형 모드)
220. [[220_hdlc_frames_i_s_u|정보 프레임]]([[220_hdlc_frames_i_s_u|I-Frame]]), 감독/제어(S-Frame / [[834_load_balancing_algorithm_round_robin_least_connection|RR]], RNR, REJ, SREJ), 비번호(U-Frame)
221. [[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]] ([[010_동기식_비동기식_전송|Synchronous]] [[001_dikw_pyramid|Data]] Link Control) - IBM
222. [[222_lapb_link_access_procedure_balanced|LAPB]] (Link Access Procedure Balanced) - X.25 망
223. [[223_lapd_isdn_d_channel|LAPD]] (Link Access Procedure on the D channel) - ISDN 망
224. [[224_ppp_point_to_point_protocol|PPP]] ([[224_ppp_point_to_point_protocol|Point-to-Point Protocol]]) - [[149_serial_communication_rs232_rs485|직렬]] 회선 표준, [[074_byte|바이트]] 지향
225. [[225_lcp_link_control_protocol|LCP]] ([[225_lcp_link_control_protocol|Link Control Protocol]]) - 링크 [[009_config|설정]]/폐기 규약
226. [[226_ncp_network_control_protocol|NCP]] ([[226_ncp_network_control_protocol|Network Control Protocol]]) - 네트워크 계층 동적 [[009_config|설정]] (IPCP, IPXCP)
227. [[227_pap_password_authentication_protocol|PAP]] ([[227_pap_password_authentication_protocol|Password Authentication Protocol]]) - 클리어텍스트 [[303_authentication_authorization_patterns|인증]]
228. [[228_chap_challenge_handshake_authentication_protocol|CHAP]] (Challenge Handshake [[604_authentication_factors|Authentication]] [[295_protocol_field_tcp_udp_icmp|Protocol]]) - 해시 기반 [[303_authentication_authorization_patterns|인증]] (3-way)
229. [[229_eap_extensible_authentication_protocol|EAP]] ([[229_eap_extensible_authentication_protocol|Extensible Authentication Protocol]]) - [[224_ppp_point_to_point_protocol|PPP]] 확장 [[303_authentication_authorization_patterns|인증]]

## 5. 근거리, 광역통신망(LAN/WAN) 및 2계층 장비 (80개)
230. [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] ([[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]]) 구조 및 원리 (IEEE 802.3)
231. [[673_mac_message_authentication_code|MAC]] 주소 ([[121_transmission_media_guided_unguided|Media]] [[547_access_control_rwx|Access Control]] Address) - 48비트 (OUI 24bit + [[587_nic_offloading|NIC]] 24bit)
232. [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] [[673_mac_message_authentication_code|MAC]] 주소 / 브로드캐스트 [[673_mac_message_authentication_code|MAC]] 주소 (FF:FF:FF:FF:FF:FF)
233. [[233_ethernet_frame_format_ethernet_ii_vs_ieee_802_3|이더넷 프레임 포맷]] ([[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]] II vs IEEE 802.3)
234. [[234_preamble_and_sfd_start_of_frame_delimiter|Preamble & SFD]] (Start of Frame Delimiter)
235. Type 필드 ([[235_type_field_ethertype_length_ipv4_arp|Ethertype]]) / Length 필드 ([[286_ipv4_internet_protocol_version_4_rfc_791|IPv4]] = 0x0800, [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] = 0x0806)
236. [[236_payload_size_and_padding_46_1500_bytes|페이로드 크기]] (46 ~ 1500 bytes), [[098_padding_convolutional_neural_network_same_valid|패딩]]([[098_padding_convolutional_neural_network_same_valid|Padding]])
237. [[237_collision_domain_vs_broadcast_domain|충돌 도메인]] ([[237_collision_domain_vs_broadcast_domain|Collision Domain]]) / 브로드캐스트 [[064_relation_domain|도메인]] (Broadcast [[064_relation_domain|Domain]])
238. [[238_switch_operation_principles|스위치]] ([[238_switch_operation_principles|Switch]]) 의 동작 원리
239. [[673_mac_message_authentication_code|MAC]] 주소 테이블 ([[673_mac_message_authentication_code|MAC]] Address Table, CAM Table)
240. 수신/학습 ([[240_switch_learning_forwarding_flooding|Learning]]) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding
241. [[411_aging_algorithm|에이징]] ([[182_aging|Aging]]) / [[446_port_and_bus|포트]] [[333_raid_1|미러링]] ([[446_port_and_bus|Port]] Mirroring)
242. [[243_switching_method_store_and_forward|스위칭 방식]] - 컷스루 (Cut-through)
243. [[243_switching_method_store_and_forward|스위칭 방식]] - 스토어 앤 포워드 (Store-and-[[235_forward_backward_chaining|forward]]) - [[034_에러_검출율|에러 검출율]] 높음
244. [[243_switching_method_store_and_forward|스위칭 방식]] - 프래그먼트 프리 (Fragment-free) - 앞부분 64바이트만 [[396_validation|확인]]
245. [[245_vlan_virtual_lan_broadcast_control|가상 랜]] ([[224_vlan_virtual_lan_broadcast_domain|VLAN]], [[224_vlan_virtual_lan_broadcast_domain|Virtual LAN]]) - [[369_logic_bomb|논리]]적 분할, 브로드캐스트 제어
246. IEEE 802.1Q - [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 태깅(Tagging), TPID, TCI, VID 필드 (4바이트 추가)
247. [[247_access_port_vs_trunk_port|접근 포트]] ([[247_access_port_vs_trunk_port|Access Port]]) / 트렁크 [[446_port_and_bus|포트]] (Trunk [[446_port_and_bus|Port]])
248. [[248_dtp_and_vtp_cisco_dynamic_trunking|DTP]] ([[248_dtp_and_vtp_cisco_dynamic_trunking|Dynamic Trunking Protocol]]) / VTP ([[224_vlan_virtual_lan_broadcast_domain|VLAN]] Trunking [[295_protocol_field_tcp_udp_icmp|Protocol]]) - [[539_netflow_sflow_traffic_monitoring|Cisco]] 전용
249. [[249_isl_inter_switch_link_cisco|ISL]] ([[249_isl_inter_switch_link_cisco|Inter-Switch Link]]) - 시스코 구형 [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 태깅
250. [[250_native_vlan_untagged_traffic|Native VLAN]] ([[250_native_vlan_untagged_traffic|언태그드 트래픽 처리용]])
251. [[251_looping_broadcast_storm|루프 문제]] ([[251_looping_broadcast_storm|Looping]]) - [[1097_broadcast_storm_switching_loop_stp|브로드캐스트 스톰]] (Broadcast Storm)
252. [[673_mac_message_authentication_code|MAC]] 주소 호핑 ([[252_mac_address_hopping_flapping|MAC Flapping]])
253. [[253_spanning_tree_protocol_stp_ieee_802_1d|스패닝 트리 프로토콜]] ([[570_stp_vs_mtp|STP]], Spanning Tree [[295_protocol_field_tcp_udp_icmp|Protocol]]) - IEEE 802.1D
254. [[254_bpdu_bridge_protocol_data_unit|BPDU]] ([[260_bridge_pattern_abstraction_implementation|Bridge]] [[295_protocol_field_tcp_udp_icmp|Protocol]] [[001_dikw_pyramid|Data]] Unit)
255. [[255_root_bridge_rp_dp_bp|루트 브리지]] ([[255_root_bridge_rp_dp_bp|Root Bridge]]), 루트 [[446_port_and_bus|포트]] ([[370_pim_rp_rendezvous_point_rpf_loop_prevention|RP]]), 지정 [[446_port_and_bus|포트]] (DP), 차단 [[446_port_and_bus|포트]] (BP, Non-Designated)
256. [[260_bridge_pattern_abstraction_implementation|브리지]] ID (Priority + [[673_mac_message_authentication_code|MAC]]), 비용 (Path Cost)
257. [[570_stp_vs_mtp|STP]] 4단계 [[632_state_transition_diagram_testing|상태 전이]] (단절, 청취, 학습, 전송)
258. [[258_stp_convergence_time_30_50_seconds|컨버전스 시간]] ([[570_stp_vs_mtp|STP]] 약 30~50초 소요)
259. [[259_portfast_and_bpdu_guard_cisco|포트 패스트]] ([[259_portfast_and_bpdu_guard_cisco|PortFast]]) / [[254_bpdu_bridge_protocol_data_unit|BPDU]] Guard ([[539_netflow_sflow_traffic_monitoring|Cisco]] 확장)
260. [[260_rstp_rapid_spanning_tree_protocol_ieee_802_1w|RSTP]] ([[260_rstp_rapid_spanning_tree_protocol_ieee_802_1w|Rapid STP]]) - IEEE 802.1w, 컨버전스 1~2초 단축
261. [[261_rstp_backup_port_and_alternate_port|백업 포트]] ([[261_rstp_backup_port_and_alternate_port|Backup Port]]), 대체 [[446_port_and_bus|포트]] (Alternate [[446_port_and_bus|Port]]) 추가
262. [[262_mstp_multiple_stp_ieee_802_1s|MSTP]] ([[262_mstp_multiple_stp_ieee_802_1s|Multiple STP]]) - IEEE 802.1s, [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 인스턴스 묶음
263. [[263_etherchannel_link_aggregation_lacp|이더채널]] ([[263_etherchannel_link_aggregation_lacp|EtherChannel]]) / 링크 어그리게이션 (LACP, IEEE 802.3ad/802.1AX) - [[446_port_and_bus|포트]] 결합 [[140_bandwidth|대역폭]] 확장
264. [[264_pagp_port_aggregation_protocol_cisco|PAgP]] ([[264_pagp_port_aggregation_protocol_cisco|Port Aggregation Protocol]]) - 시스코 전용
265. [[265_poe_power_over_ethernet|PoE]] ([[265_poe_power_over_ethernet|Power over Ethernet]]) - IEEE 802.3af/at/bt, 랜선으로 전력 공급
266. [[266_leased_line_basics_e1_t1_t3|전용선]] ([[266_leased_line_basics_e1_t1_t3|Leased Line]]) 기초 (E1, T1/T3 망)
267. 다이얼업 [[071_다중화_Multiplexing|다중화]], X.25 ([[276_packet_switching_vs_circuit_switching_message_switching|패킷 교환]] 망 원조)
268. [[268_frame_relay_x25_simplification|프레임 릴레이]] ([[268_frame_relay_x25_simplification|Frame Relay]]) - X.25 간소화, 흐름/오류제어 생략
269. [[269_pvc_vs_svc_virtual_circuits|PVC]] ([[269_pvc_vs_svc_virtual_circuits|Permanent Virtual Circuit]]) / SVC (Switched Virtual Circuit)
270. [[270_dlci_data_link_connection_identifier|DLCI]] ([[001_dikw_pyramid|Data]] Link Connection [[088_identifier_in_er_model|Identifier]])
271. [[271_cir_fecn_becn_congestion_notification|CIR]] ([[271_cir_fecn_becn_congestion_notification|Committed Information Rate]]) / FECN, BECN 혼잡 알림
272. [[272_atm_asynchronous_transfer_mode_53byte_cell|ATM]] ([[272_atm_asynchronous_transfer_mode_53byte_cell|Asynchronous Transfer Mode]]) - 비동기 전송 모드, 53바이트 셀
273. [[272_atm_asynchronous_transfer_mode_53byte_cell|ATM]] [[212_synchronization_mechanisms|동기화]] (셀 헤더의 HEC 사용)
274. VPI / VCI (Virtual Path/Channel [[088_identifier_in_er_model|Identifier]])
275. [[275_aal_atm_adaptation_layer|AAL]] ([[275_aal_atm_adaptation_layer|ATM Adaptation Layer]]) - AAL1, AAL2, AAL5 등 트래픽별 지원
276. [[276_packet_switching_vs_circuit_switching_message_switching|패킷 교환]] ([[276_packet_switching_vs_circuit_switching_message_switching|Packet Switching]]) vs 회선 교환 (Circuit Switching) vs [[389_mesh_topology|메시]]지 교환
277. [[277_datagram_transmission_connectionless_packet_switching|데이터그램 전송 방식]] ([[277_datagram_transmission_connectionless_packet_switching|비연결형 패킷 교환]])
278. 가상 회선 전송 방식 (연결형 [[276_packet_switching_vs_circuit_switching_message_switching|패킷 교환]] - [[405_tcp_transmission_control_protocol_connection_oriented|TCP]], [[272_atm_asynchronous_transfer_mode_53byte_cell|ATM]] 등)
279. [[279_b_isdn_broadband_integrated_services_digital_network|브로드밴드통신망]] ([[279_b_isdn_broadband_integrated_services_digital_network|B-ISDN]])
280. [[280_local_loop_subscriber_line|로컬 루프]] (Local Loop, 가입자 선로)
281. [[281_token_ring_ieee_802_5_token_bus_ieee_802_4|토큰 링]] ([[281_token_ring_ieee_802_5_token_bus_ieee_802_4|Token Ring]]) - IEEE 802.5 / 토큰 [[344_bus|버스]] (Token [[344_bus|Bus]]) - IEEE 802.4
282. [[282_fddi_fiber_distributed_data_interface_dual_ring|FDDI]] (Fiber Distributed [[001_dikw_pyramid|Data]] Interface) - 이중 링 기반 100Mbps
283. [[283_dqdb_distributed_queue_dual_bus_ieee_802_6|DQDB]] (Distributed [[058_queue|Queue]] Dual [[344_bus|Bus]]) - IEEE 802.6 MAN 방식
284. [[284_pon_passive_optical_network_vs_aon_active|PON]] ([[284_pon_passive_optical_network_vs_aon_active|Passive Optical Network]]) / AON ([[483_active_vs_passive_ftp|Active]] Optical Network)

## 6. 네트워크 계층 - IP [[295_protocol_field_tcp_udp_icmp|프로토콜]] 및 주소체계 (80개)
285. 네트워크 계층의 핵심 3기능 - [[339_routing_overview_best_path_selection|라우팅]](경로 [[009_config|설정]]), 디스패칭(포워딩), 혼잡 제어
286. [[286_ipv4_internet_protocol_version_4_rfc_791|IPv4]] (Internet [[295_protocol_field_tcp_udp_icmp|Protocol]] Version 4) - RFC 791, 32비트, 비연결성/최선노력 전송
287. [[286_ipv4_internet_protocol_version_4_rfc_791|IPv4]] 헤더 구조 (기본 20바이트 ~ 최대 60바이트)
288. [[288_version_ihl_tos_total_length|버전]] ([[288_version_ihl_tos_total_length|IV]]), 헤더 길이 (IHL), [[090_service_kubernetes_network_load_balancing|서비스]] 타입 (TOS/DSCP), 전체 길이 (Total Length)
289. [[289_identification_flags_fragmentation_offset|식별자]] ([[289_identification_flags_fragmentation_offset|Identification]]), [[186_character_stuffing_dle_stx_etx|플래그]] (Flags), [[291_fragmentation_and_reassembly_process|단편화]] 오프셋 ([[291_fragmentation_and_reassembly_process|Fragmentation]] Offset)
290. DF (Don't Fragment) [[073_bit|비트]] / MF (More Fragment) [[073_bit|비트]]
291. [[291_fragmentation_and_reassembly_process|단편화]] ([[291_fragmentation_and_reassembly_process|Fragmentation]]) 및 재조립 (Reassembly)
292. 패킷 캡슐화, MTU ([[292_packet_encapsulation_mtu_ethernet_1500_bytes|Maximum Transmission Unit]]) - [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 1500바이트
293. [[293_pmtu_path_mtu_discovery|PMTU]] ([[293_pmtu_path_mtu_discovery|Path MTU Discovery]]) - 경로 최소 MTU [[396_validation|확인]] [[001_algorithm_definition|알고리즘]]
294. [[294_ttl_time_to_live_looping_prevention|TTL]] ([[294_ttl_time_to_live_looping_prevention|Time to Live]]) - 루핑 방지, 홉 감소
295. [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[295_protocol_field_tcp_udp_icmp|Protocol]]) 필드 - [[405_tcp_transmission_control_protocol_connection_oriented|TCP]](6), [[406_udp_user_datagram_protocol_connectionless_fast|UDP]](17), [[318_icmp_internet_control_message_protocol_diagnostics|ICMP]](1) 등
296. [[296_header_checksum_ipv4_integrity|헤더 체크섬]] ([[296_header_checksum_ipv4_integrity|Header Checksum]]) - [[286_ipv4_internet_protocol_version_4_rfc_791|IPv4]] 헤더만 [[003_integrity|무결성]] [[395_verification_process_review|검증]]
297. IP 주소 고갈 문제, 클라스풀 ([[297_ip_address_exhaustion_classful_addressing|Classful]]) 주소체계
298. 클래스 A, B, C, D ([[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]]), E (실험용)
299. 사설 IP ([[299_private_ip_ranges_10_172_192|Private IP]]) 영역: [[489_raid_10_hybrid|10]].x, 172.16.x~172.31.x, 192.168.x
300. 루프백 IP ([[300_loopback_ip_127_0_0_1_localhost|Loopback IP]]) - 127.0.0.1 (로컬호스트)
301. APIPA / [[329_ipv6_link_local_fe80_site_local|링크 로컬 주소]] (169.254.x.x)
302. [[302_broadcast_address_network_limited_255_255_255_255|브로드캐스트 주소]] - 네트워크 브로드캐스트, 리미티드 브로드캐스트(255.255.255.255)
303. [[303_cidr_classless_inter_domain_routing|클래스리스]] ([[303_cidr_classless_inter_domain_routing|Classless]]) [[339_routing_overview_best_path_selection|라우팅]] (CIDR, [[303_cidr_classless_inter_domain_routing|Classless]] Inter-[[064_relation_domain|Domain]] [[339_routing_overview_best_path_selection|Routing]])
304. [[304_subnetting_network_division_and_operation|서브네팅]] ([[304_subnetting_network_division_and_operation|Subnetting]]) - 네트워크 분할 (AND 연산)
305. [[305_supernetting_route_summarization|슈퍼네팅]] ([[305_supernetting_route_summarization|Supernetting]]) / 경로 요약 (Route Summarization)
306. [[306_vlsm_variable_length_subnet_mask|VLSM]] (Variable Length [[963_subnet_mask_cidr_classless_inter_domain_routing|Subnet Mask]]) - 가변 길이 [[963_subnet_mask_cidr_classless_inter_domain_routing|서브넷 마스크]]
307. [[307_nat_network_address_translation_router_principles|NAT]] ([[307_nat_network_address_translation_router_principles|Network Address Translation]]) - 공유기 원리
308. [[308_static_dynamic_nat_pat_port_address_translation|Static NAT]] (1:1) / Dynamic [[307_nat_network_address_translation_router_principles|NAT]] (M:N) / PAT ([[446_port_and_bus|Port]] Address Translation = NAPT, 1:N)
309. 헤어핀 [[307_nat_network_address_translation_router_principles|NAT]] (Hairpin [[307_nat_network_address_translation_router_principles|NAT]], [[307_nat_network_address_translation_router_principles|NAT]] Loopback)
310. [[310_alg_application_layer_gateway_nat_traversal|ALG]] ([[310_alg_application_layer_gateway_nat_traversal|Application Layer Gateway]]) - [[307_nat_network_address_translation_router_principles|NAT]] 횡단 지원 ([[482_ftp_file_transfer_protocol|FTP]] 능동모드 등 해결)
311. STUN, TURN, ICE ([[307_nat_network_address_translation_router_principles|NAT]] 횡단/Traversing 기법, VoIP/[[505_webrtc_web_real_time_communication|WebRTC]])
312. [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] ([[312_arp_address_resolution_protocol_ip_to_mac|Address Resolution Protocol]]) - [[369_logic_bomb|논리]] 주소를 물리 주소로 (IP -> [[673_mac_message_authentication_code|MAC]])
313. [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] 프레임 (요청-브로드캐스트, 응답-유니캐스트)
314. [[314_rarp_reverse_arp_mac_to_ip|RARP]] ([[314_rarp_reverse_arp_mac_to_ip|Reverse ARP]]) - MAC으로 IP 얻기 ([[522_dhcp_dynamic_host_configuration_protocol|DHCP]] 이전)
315. [[315_proxy_arp_subnet_proxy_response|Proxy ARP]] ([[264_proxy_pattern_surrogate_access_control|프록시]] [[312_arp_address_resolution_protocol_ip_to_mac|ARP]]) - 다른 서브넷의 IP에 응답 대행
316. [[316_gratuitous_arp_g_arp_ip_conflict_cache_update|Gratuitous ARP]] ([[316_gratuitous_arp_g_arp_ip_conflict_cache_update|G-ARP]]) - 자신의 IP 충돌 감지 및 캐시 갱신 목적
317. [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] 캐시 오염 ([[318_arp_cache_poisoning|ARP Cache Poisoning]], [[598_spoofing|스푸핑]] 공격)
318. [[318_icmp_internet_control_message_protocol_diagnostics|ICMP]] (Internet Control Message [[295_protocol_field_tcp_udp_icmp|Protocol]]) 진단/오류 알림
319. [[318_icmp_internet_control_message_protocol_diagnostics|ICMP]] [[389_mesh_topology|메시]]지 종류 - Query, Error Reporting
320. [[320_icmp_time_exceeded_ttl_expiration_traceroute|Time Exceeded]] ([[294_ttl_time_to_live_looping_prevention|TTL]] 만료, Traceroute 원리)
321. Destination Unreachable (목적지 도달 불가 - [[446_port_and_bus|포트]], 호스트 차단)
322. Echo Request/Reply (Ping 원리) / Source Quench (혼잡 제어, 구형)
323. Redirect [[389_mesh_topology|메시]]지 - 더 나은 라우터 경로 통보
324. [[324_ipv6_128bit_next_generation_address|IPv6]] (Internet [[295_protocol_field_tcp_udp_icmp|Protocol]] Version 6) - 128비트 차세대 주소
325. [[324_ipv6_128bit_next_generation_address|IPv6]] 단순화된 헤더 - 40바이트 고정 ([[296_header_checksum_ipv4_integrity|헤더 체크섬]] 삭제, [[291_fragmentation_and_reassembly_process|단편화]] 삭제)
326. [[326_traffic_class_flow_label_ipv6_qos|트래픽 클래스]] ([[326_traffic_class_flow_label_ipv6_qos|Traffic Class]]) / 플로우 레이블 (Flow Label)
327. Next Header, 홉 제한 (Hop Limit, [[294_ttl_time_to_live_looping_prevention|TTL]] 대응)
328. 유니캐스트, [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]], 애니캐스트(Anycast, 가장 가까운 노드 응답) - 브로드캐스트 없음
329. [[329_ipv6_link_local_fe80_site_local|링크 로컬 주소]] ([[324_ipv6_128bit_next_generation_address|IPv6]] Link Local, FE80::) / 사이트 로컬 주소
330. [[330_eui_64_mac_to_ipv6_interface_id|EUI-64]] ([[673_mac_message_authentication_code|MAC]] 기반 [[324_ipv6_128bit_next_generation_address|IPv6]] 호스트 주소 자동생성)
331. [[331_slaac_stateless_address_autoconfiguration_ndp|SLAAC]] ([[331_slaac_stateless_address_autoconfiguration_ndp|Stateless Address Autoconfiguration]]) 무상태 주소 자동 [[009_config|설정]] - [[336_ndp_neighbor_discovery_protocol_ipv6|NDP]] 활용
332. [[286_ipv4_internet_protocol_version_4_rfc_791|IPv4]]-[[324_ipv6_128bit_next_generation_address|IPv6]] 전환 기술: 듀얼 [[057_stack|스택]] ([[332_ipv4_ipv6_transition_dual_stack_tunneling_nat64|Dual Stack]]), [[377_tunneling_mechanism_overview|터널링]] (ISATAP, 6to4), 주소 변환 (NAT64/DNS64)
333. [[333_igmp_internet_group_management_protocol_multicast|IGMP]] (Internet Group [[372_management|Management]] [[295_protocol_field_tcp_udp_icmp|Protocol]]) - [[286_ipv4_internet_protocol_version_4_rfc_791|IPv4]] [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] 그룹 가입/탈퇴
334. [[334_igmp_snooping_multicast_traffic_control|IGMP Snooping]] ([[238_switch_operation_principles|스위치]]가 [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] 트래픽 불필요한 [[446_port_and_bus|포트]]에 차단)
335. [[335_mld_multicast_listener_discovery_ipv6|MLD]] ([[335_mld_multicast_listener_discovery_ipv6|Multicast Listener Discovery]]) - IGMP의 [[324_ipv6_128bit_next_generation_address|IPv6]] [[288_version_ihl_tos_total_length|버전]]
336. [[336_ndp_neighbor_discovery_protocol_ipv6|NDP]] ([[336_ndp_neighbor_discovery_protocol_ipv6|Neighbor Discovery Protocol]]) - IPv6의 [[312_arp_address_resolution_protocol_ip_to_mac|ARP]]/[[318_icmp_internet_control_message_protocol_diagnostics|ICMP]] 대체, RS/[[161_ra_registration_authority|RA]]/NS/NA 교환

## 7. 네트워크 계층 - [[339_routing_overview_best_path_selection|라우팅]], [[377_tunneling_mechanism_overview|터널링]], [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] (80개)
337. [[337_router_architecture_rib_fib_control_data_plane|라우터 구조 판단]] - [[339_routing_overview_best_path_selection|라우팅]] 테이블(RIB), 포워딩 테이블([[781_fib_circuit_edit|FIB]]), 제어/[[001_dikw_pyramid|데이터]] 평면
338. [[338_cef_cisco_express_forwarding_hardware_switching|CEF]] ([[338_cef_cisco_express_forwarding_hardware_switching|Cisco Express Forwarding]]) 물리적 포워딩 / 하드웨어 스위칭 ([[070_asic|ASIC]])
339. [[339_routing_overview_best_path_selection|라우팅]] ([[339_routing_overview_best_path_selection|Routing]]) 개요 - 최적 경로(Best Path) [[009_config|설정]]
340. [[340_static_routing_default_route_0_0_0_0|정적 라우팅]] ([[340_static_routing_default_route_0_0_0_0|Static Routing]]) - 관리자 수동 [[009_config|설정]] (지속성, [[283_security_tactics|보안성]] 높음) / 디폴트 라우터 (0.0.0.0/0)
341. [[341_dynamic_routing_protocol_operation|동적 라우팅]] ([[341_dynamic_routing_protocol_operation|Dynamic Routing]]) - [[339_routing_overview_best_path_selection|라우팅]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 운영
342. [[342_routing_metric_hop_bandwidth_delay|메트릭]] ([[342_routing_metric_hop_bandwidth_delay|Metric]]) - 최적 경로 산출 기준 (홉 카운트, [[140_bandwidth|대역폭]], [[015_지연_데이터_관점|지연]], 부하 등)
343. [[343_administrative_distance_ad_protocol_priority|관리 거리]] (AD, Administrative Distance) - [[295_protocol_field_tcp_udp_icmp|프로토콜]] 우선순위 판단
344. [[344_as_autonomous_system_asn|AS]] (Autonomous System, 자율 시스템) / ASN 분배
345. [[345_igp_interior_gateway_protocol_rip_ospf|IGP]] ([[345_igp_interior_gateway_protocol_rip_ospf|Interior Gateway Protocol]]) - [[344_as_autonomous_system_asn|AS]] 내부 [[339_routing_overview_best_path_selection|라우팅]] ([[351_rip_routing_information_protocol_distance_vector_hop|RIP]], [[357_ospf_open_shortest_path_first_overview|OSPF]], [[355_eigrp_enhanced_igrp_dual_algorithm|EIGRP]] 등)
346. [[346_egp_exterior_gateway_protocol_bgp|EGP]] ([[346_egp_exterior_gateway_protocol_bgp|Exterior Gateway Protocol]]) - [[344_as_autonomous_system_asn|AS]] 외부간 [[339_routing_overview_best_path_selection|라우팅]] ([[365_bgp_border_gateway_protocol_path_vector|BGP]])
347. [[347_distance_vector_routing_bellman_ford|거리 벡터]] ([[347_distance_vector_routing_bellman_ford|Distance Vector]]) [[339_routing_overview_best_path_selection|라우팅]] [[001_algorithm_definition|알고리즘]] - [[170_bellman_ford|벨만-포드]]([[170_bellman_ford|Bellman-Ford]]) 기반
348. [[348_link_state_routing_dijkstra_spf|링크 상태]] ([[348_link_state_routing_dijkstra_spf|Link State]]) [[339_routing_overview_best_path_selection|라우팅]] [[001_algorithm_definition|알고리즘]] - [[036_dijkstra|다익스트라]]([[036_dijkstra|Dijkstra]]) 기반 (최단경로/[[495_spf_sender_policy_framework|SPF]])
349. [[347_distance_vector_routing_bellman_ford|거리 벡터]] [[339_routing_overview_best_path_selection|라우팅]] 루프 방지 - 스플릿 호라이즌 (Split Horizon), 포이즌 리버스 (Poison Reverse)
350. [[350_distance_vector_hold_down_timer_triggered_update|홀드다운 타이머]] ([[350_distance_vector_hold_down_timer_triggered_update|Hold-down Timer]]), 트리거드 업데이트 (Triggered Update)
351. [[351_rip_routing_information_protocol_distance_vector_hop|RIP]] ([[351_rip_routing_information_protocol_distance_vector_hop|Routing Information Protocol]]) - 거리벡터, 홉 카운트 [[342_routing_metric_hop_bandwidth_delay|메트릭]](최대 15), 30초 업데이트
352. [[352_ripv1_classful_vs_ripv2_classless_vlsm|RIPv1]] (클래스풀, 브로드캐스트) vs RIPv2 ([[303_cidr_classless_inter_domain_routing|클래스리스]]/[[306_vlsm_variable_length_subnet_mask|VLSM]], [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]]: 224.0.0.9)
353. [[353_ripng_ipv6_routing|RIPng]] ([[324_ipv6_128bit_next_generation_address|IPv6]] 용)
354. [[354_igrp_cisco_legacy_composite_metric|IGRP]] - [[539_netflow_sflow_traffic_monitoring|Cisco]] 구형, 복합 [[342_routing_metric_hop_bandwidth_delay|메트릭]] ([[140_bandwidth|대역폭]]+[[015_지연_데이터_관점|지연]] 등)
355. [[355_eigrp_enhanced_igrp_dual_algorithm|EIGRP]] ([[355_eigrp_enhanced_igrp_dual_algorithm|Enhanced IGRP]]) - 하이브리드(고급 거리벡터), DUAL(Diffusing Update [[310_alg_application_layer_gateway_nat_traversal|Alg]]) [[001_algorithm_definition|알고리즘]]
356. [[355_eigrp_enhanced_igrp_dual_algorithm|EIGRP]] 특징: 부분/바운디드 업데이트, Unequal-Cost 부하분산, Successor / Feasible Successor
357. [[357_ospf_open_shortest_path_first_overview|OSPF]] (Open [[547_graph_shortest_path_db_mapping|Shortest Path]] First) - 대표적 [[348_link_state_routing_dijkstra_spf|링크 상태]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]
358. [[357_ospf_open_shortest_path_first_overview|OSPF]] 인접성([[358_ospf_adjacency_hello_lsa_lsdb|Adjacency]]), Hello 패킷, LSA ([[348_link_state_routing_dijkstra_spf|Link State]] Advertisement), [[961_ospf_link_state_database_dijkstra_spf_routing|LSDB]] 교환
359. [[357_ospf_open_shortest_path_first_overview|OSPF]] Area 계층적 구조 - Area 0 (Backbone, 전이 공간), ABR (Area Border 라우터), ASBR
360. [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] ([[360_ospf_dr_bdr_designated_router_lsa_flooding|Designated Router]]), BDR - 브로드캐스트 망에서 LSA 플러딩 최소화
361. [[357_ospf_open_shortest_path_first_overview|OSPF]] 트래픽엔지니어링([[361_ospf_traffic_engineering_te|TE]]) 연동
362. [[362_ospfv3_ipv6_support|OSPFv3]] ([[324_ipv6_128bit_next_generation_address|IPv6]] 지원)
363. [[363_is_is_intermediate_system_clnp_telecom|IS-IS]] (Intermediate System to Intermediate System) - CLNP 기반 [[348_link_state_routing_dijkstra_spf|링크 상태]] [[339_routing_overview_best_path_selection|라우팅]], 통신사/백본 선호
364. L1/L2 라우터, L1/L2 Area 체계, [[363_is_is_intermediate_system_clnp_telecom|IS-IS]] over [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]]/IP
365. [[365_bgp_border_gateway_protocol_path_vector|BGP]] ([[365_bgp_border_gateway_protocol_path_vector|Border Gateway Protocol]]) - [[344_as_autonomous_system_asn|AS]] 간 인터넷 백본 [[339_routing_overview_best_path_selection|라우팅]], 경로 벡터 (Path-Vector)
366. [[366_ibgp_ebgp_split_horizon_rule|iBGP]] ([[366_ibgp_ebgp_split_horizon_rule|내부 맺음]]), eBGP (외부 맺음), [[365_bgp_border_gateway_protocol_path_vector|BGP]] Split Horizon 룰
367. [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[082_attribute_types_er_model|속성]]([[502_file_attributes_metadata|Attributes]]) - NEXT_HOP, AS_PATH, LOCAL_PREF, MED
368. [[365_bgp_border_gateway_protocol_path_vector|BGP]] Route Reflector / Confederation ([[366_ibgp_ebgp_split_horizon_rule|iBGP]] 풀 [[389_mesh_topology|메시]] 문제 해결)
369. [[369_multicast_routing_pim_dense_vs_sparse|멀티캐스트 라우팅]] - [[430_pim|PIM]] ([[295_protocol_field_tcp_udp_icmp|Protocol]] Independent Multicast) - Dense Mode vs Sparse Mode
370. [[370_pim_rp_rendezvous_point_rpf_loop_prevention|RP]] (Rendezvous Point, [[430_pim|PIM]]-SM), RPF (Reverse Path Forwarding) [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] 루프 방지
371. [[371_vrf_virtual_routing_and_forwarding|VRF]] (Virtual [[339_routing_overview_best_path_selection|Routing]] and Forwarding) - 한 라우터 단일 장비에 다수 가상 [[339_routing_overview_best_path_selection|라우팅]] 테이블
372. [[372_policy_based_routing_pbr_route_map|Policy-Based Routing]] ([[372_policy_based_routing_pbr_route_map|PBR]]) / Route Map - 목적지 기준 [[339_routing_overview_best_path_selection|라우팅]] [[164_policy|정책]]
373. [[373_mpls_multiprotocol_label_switching_20bit|MPLS]] ([[373_mpls_multiprotocol_label_switching_20bit|Multiprotocol Label Switching]]) - IP가 아닌 20비트 Label로 스위칭
374. [[374_lsr_label_switch_router_ler_edge|LSR]] ([[374_lsr_label_switch_router_ler_edge|Label Switch Router]]), LER (Label Edge Router)
375. [[375_ldp_label_distribution_protocol_rsvp_te|LDP]] ([[375_ldp_label_distribution_protocol_rsvp_te|Label Distribution Protocol]]), RSVP-[[361_ospf_traffic_engineering_te|TE]]
376. [[376_mpls_vpn_l3_vrf_bgp|MPLS VPN]] - L3 [[376_mpls_vpn_l3_vrf_bgp|MPLS VPN]]
377. [[377_tunneling_mechanism_overview|터널링]] ([[377_tunneling_mechanism_overview|Tunneling]]) 메커니즘 개요
378. [[378_gre_generic_routing_encapsulation|GRE]] ([[378_gre_generic_routing_encapsulation|Generic Routing Encapsulation]]) - 다양한 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 패키징, 비보안
379. [[379_l2tp_layer_2_tunneling_protocol|L2TP]] (Layer 2 [[377_tunneling_mechanism_overview|Tunneling]] [[295_protocol_field_tcp_udp_icmp|Protocol]]) - PPTP+L2F, [[983_vpn_virtual_private_network|VPN]] 확장형
380. [[589_ipsec_offload|IPSec]] ([[380_ipsec_ip_security_framework|IP Security Framework]]) 메커니즘
381. [[381_ah_authentication_header_integrity_auth|AH]] ([[381_ah_authentication_header_integrity_auth|Authentication Header]]) - [[003_integrity|무결성]], [[303_authentication_authorization_patterns|인증]]
382. [[382_esp_encapsulating_security_payload_confidentiality|ESP]] ([[382_esp_encapsulating_security_payload_confidentiality|Encapsulating Security Payload]]) - [[002_confidentiality|기밀성]], [[003_integrity|무결성]]
383. [[383_ike_isakmp_sa_security_association|IKE]] ([[383_ike_isakmp_sa_security_association|Internet Key Exchange]]), ISAKMP, [[767_sa_standalone_5g_core_network|SA]] ([[283_security_tactics|Security]] Associations)
384. [[384_nat_t_ipsec_nat_traversal_udp_4500|NAT-T]] ([[384_nat_t_ipsec_nat_traversal_udp_4500|NAT Traversal]]) - IPsec이 NAT를 우회하는 기법 ([[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 4500)
385. [[283_ssl_vpn|SSL VPN]] / [[694_thread_local_storage_tls|TLS]] [[983_vpn_virtual_private_network|VPN]]
386. [[386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp|DMVPN]] ([[386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp|Dynamic Multipoint VPN]]) - [[378_gre_generic_routing_encapsulation|GRE]] + [[589_ipsec_offload|IPsec]] + NHRP
387. [[387_wireguard_vpn_modern_tunneling|WireGuard]] ([[387_wireguard_vpn_modern_tunneling|와이어가드]]) - 터널/트랜스포트 계층 [[983_vpn_virtual_private_network|VPN]]
388. [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] ([[388_qos_quality_of_service_best_effort_intserv_diffserv|Quality of Service]]) - Best Effort, [[389_intserv_integrated_services_rsvp|IntServ]], [[390_diffserv_differentiated_services_dscp_phb|DiffServ]]
389. [[389_intserv_integrated_services_rsvp|IntServ]] ([[389_intserv_integrated_services_rsvp|Integrated Services]]) - 자원 예약 기반 (RSVP)
390. [[390_diffserv_differentiated_services_dscp_phb|DiffServ]] ([[390_diffserv_differentiated_services_dscp_phb|Differentiated Services]]) - 트래픽 차등 처리, DSCP([[411_tcp_control_flags_urg_ack_psh_rst_syn_fin|6bit]]) PHB
391. [[083_priority_queue|우선순위 큐]] ([[391_qos_queuing_pq_cq_wfq_cbwfq_llq|PQ]]), 맞춤형 큐 (CQ), WFQ, CBWFQ, LLQ
392. [[392_traffic_shaping_and_policing|트래픽 쉐이핑]] ([[392_traffic_shaping_and_policing|Traffic Shaping]]) / 폴리싱 (Traffic Policing)
393. Leaky Bucket / Token Bucket
394. [[394_wred_weighted_random_early_detection|WRED]] (Weighted Random Early [[961_deepfake_detection|Detection]]) 혼잡 제어 꼬리 짜르기 제한
395. [[395_hsrp_fhrp_router_redundancy|HSRP]] ([[457_hot_standby|Hot Standby]] Router [[295_protocol_field_tcp_udp_icmp|Protocol]]) - FHRP 류, 라우터 [[456_dual_redundancy|이중화]]
396. [[396_vrrp_virtual_router_redundancy_protocol|VRRP]] (Virtual Router Redundancy [[295_protocol_field_tcp_udp_icmp|Protocol]]) - 개방형 FHRP
397. [[397_glbp_gateway_load_balancing_protocol|GLBP]] (Gateway [[196_hard_soft_real_time|Load Balancing]] [[295_protocol_field_tcp_udp_icmp|Protocol]])
398. [[398_ip_sla_network_performance_monitoring|IP SLA]] - 네트워크 [[282_performance_tactics|성능]] [[342_routing_metric_hop_bandwidth_delay|메트릭]] [[229_monitor|모니터]]링
399. Anycast [[339_routing_overview_best_path_selection|라우팅]] ([[365_bgp_border_gateway_protocol_path_vector|BGP]] Anycast - [[511_dns_hierarchical_distributed_architecture|DNS]] 서버 [[456_dual_redundancy|이중화]]용)
400. 로케이터/ID 분리 구조 (LISP - Locator/ID Separation [[295_protocol_field_tcp_udp_icmp|Protocol]])

## 8. 전송 계층 - [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/[[406_udp_user_datagram_protocol_connectionless_fast|UDP]] (60개)
401. 전송 계층의 역할: 종단 간([[401_transport_layer_role_end_to_end_multiplexing|End-to-End]]) 오류/흐름/혼잡 제어, [[071_다중화_Multiplexing|다중화]]/역다중화
402. [[402_port_number_16bit_application_process_identification|포트 번호]] ([[402_port_number_16bit_application_process_identification|Port Number]]) - 16비트, 응용 프로세스 [[655_ir_detection_analysis|식별]]
403. Well-Known [[446_port_and_bus|포트]] (0~1023), Registered [[446_port_and_bus|포트]] (1024~49151), Dynamic [[446_port_and_bus|포트]] (49152~65535)
404. [[404_socket_address_ip_port_combination|소켓 주소]] ([[404_socket_address_ip_port_combination|Socket Address]]) = IP 주소 + [[402_port_number_16bit_application_process_identification|포트 번호]]
405. [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] ([[405_tcp_transmission_control_protocol_connection_oriented|Transmission Control Protocol]]) - 연결 지향형, [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 전송, 스트림 기반
406. [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] ([[406_udp_user_datagram_protocol_connectionless_fast|User Datagram Protocol]]) - 비연결형, 비신뢰성, 빠른 속도, [[389_mesh_topology|메시]]지 기반
407. [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 세그먼트 ([[407_tcp_segment_header_structure_20_60_bytes|Segment]]) 헤더 - 기본 20바이트 ~ 60바이트
408. 소스/목적지 [[402_port_number_16bit_application_process_identification|포트 번호]], 일련번호 (Sequence Number, 32bit)
409. [[409_tcp_acknowledgment_number_cumulative_ack|확인응답번호]] (Acknowledgment Number, 32bit) - 다음 수신할 [[074_byte|바이트]] 번호 (누적 ACK)
410. 헤더 길이/[[001_dikw_pyramid|데이터]] 오프셋 ([[001_dikw_pyramid|Data]] Offset, 4bit)
411. [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 제어 [[186_character_stuffing_dle_stx_etx|플래그]]([[411_tcp_control_flags_urg_ack_psh_rst_syn_fin|6bit]]) - URG(긴급), ACK(응답), PSH(푸시), RST([[459_quic_fec_forward_error_correction|초기]]화), SYN([[212_synchronization_mechanisms|동기화]]), FIN(종료)
412. ECN 징후 [[186_character_stuffing_dle_stx_etx|플래그]] - CWR, ECE
413. [[413_tcp_window_size_flow_control_16bit|윈도우 크기]] ([[215_window_size_sender_receiver|Window Size]], 16bit) - 수신측 버퍼 여유 공간 ([[213_flow_control_buffer_overflow|흐름 제어]]용)
414. [[112_checksum|체크섬]] ([[112_checksum|Checksum]]) - 가상 헤더 (Virtual Header) 포함 (IP + [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/[[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 헤더)
415. [[415_tcp_urgent_pointer|긴급 포인터]] ([[415_tcp_urgent_pointer|Urgent Pointer]])
416. [[416_tcp_3_way_handshake_connection_setup|TCP 3-Way Handshake]] - 연결 [[009_config|설정]] 과정 (SYN -> SYN/ACK -> ACK)
417. [[417_isn_initial_sequence_number_randomization|ISN]] ([[417_isn_initial_sequence_number_randomization|Initial Sequence Number]]) 무작위 할당 이유 ([[283_security_tactics|보안성]] 강화)
418. [[418_tcp_4_way_handshake_connection_termination|TCP 4-Way Handshake]] - 연결 종료 과정 (FIN -> ACK -> FIN -> ACK)
419. TIME_WAIT 상태 (기본 2MSL 대기) - [[015_지연_데이터_관점|지연]] 패킷 수신 및 정상 종료 보장
420. CLOSE_WAIT / LAST_ACK 상태
421. [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[213_flow_control_buffer_overflow|흐름 제어]] ([[421_tcp_flow_control_sliding_window_algorithm|Flow Control]]) - 수신자 관점, 슬라이딩 윈도우 [[001_algorithm_definition|알고리즘]]
422. [[422_tcp_window_scale_option|윈도우 스케일옵션]] ([[422_tcp_window_scale_option|Window Scale Option]]) - 최대 1GB까지 윈도우 확장
423. [[423_send_buffer_receive_buffer|송신 버퍼]] ([[423_send_buffer_receive_buffer|Send Buffer]]) / 수신 버퍼 (Receive Buffer)
424. [[424_silly_window_syndrome_problem|어리석은 윈도우 증후군]] ([[424_silly_window_syndrome_problem|Silly Window Syndrome]]) 문제 
425. 네이글 [[001_algorithm_definition|알고리즘]] (Nagle's [[001_algorithm_definition|Algorithm]]) - 작은 패킷 [[015_지연_데이터_관점|지연]] 모음 (송신측 해결)
426. 클라크 해결책 (Clark's Solution) - 수신측 여유 전까지 [[413_tcp_window_size_flow_control_16bit|윈도우 크기]] 0 유지 (수신측 해결)
427. [[015_지연_데이터_관점|지연]]된 ACK ([[427_delayed_ack_tcp_optimization|Delayed ACK]]) - 응답 패킷 모아서 전송
428. [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 혼잡 제어 ([[428_tcp_congestion_control_network_perspective|Congestion Control]]) - 망(네트워크) 관점, 패킷 유실 방지
429. [[429_cwnd_congestion_window_concept|혼잡 윈도우]] (CWND, [[969_congestion_window_cwnd_tcp_network_overload|Congestion Window]])
430. [[430_slow_start_exponential_growth_cwnd|슬로우 스타트]] ([[430_slow_start_exponential_growth_cwnd|Slow Start]]) - CWND 지수적 증가
431. [[431_ssthresh_slow_start_threshold|임계치]] (ssthresh, [[430_slow_start_exponential_growth_cwnd|Slow Start]] Threshold) 
432. [[432_congestion_avoidance_aimd_algorithm|혼잡 회피]] (Congestion Avoidance / AIMD [[001_algorithm_definition|알고리즘]]) - CWND 선형 증가
433. [[433_fast_retransmit_3_dup_ack|빠른 재전송]] ([[433_fast_retransmit_3_dup_ack|Fast Retransmit]]) - 중복 ACK 3개(3 Dup-ACK) 수신 시 [[573_timeout_retry_backoff_strategy|타임아웃]] 전 재전송
434. [[434_fast_recovery_skip_slow_start|빠른 회복]] ([[434_fast_recovery_skip_slow_start|Fast Recovery]]) - 재전송 후 [[430_slow_start_exponential_growth_cwnd|슬로우 스타트]] 생략하고 혼잡회피로 진입
435. [[435_tcp_tahoe_timeout_dup_ack_drop_to_1|TCP Tahoe]] ([[573_timeout_retry_backoff_strategy|타임아웃]], 3 Dup-ACK 모두 1로 하락) 모델
436. [[436_tcp_reno_fast_retransmit_recovery|TCP Reno]] ([[433_fast_retransmit_3_dup_ack|빠른 재전송]]/[[434_fast_recovery_skip_slow_start|빠른 회복]] 지원) 모델
437. [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] NewReno / SACK (선택적 [[396_validation|확인]]응답 옵션, 블록 다중유실 [[233_recovery_database_restoration_overview|회복]])
438. [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] BIC / CUBIC - 현대 리눅스 [[022_kernel_role|커널]] 기본 [[001_algorithm_definition|알고리즘]] (지수함수 기반 고속망 최적화)
439. [[439_bbr_bottleneck_bandwidth_and_rtt_google_congestion_control|BBR]] ([[617_io_bottleneck|Bottleneck]] [[140_bandwidth|Bandwidth]] and Round-trip propagation time) - 구글, [[015_지연_데이터_관점|지연]]시간 기반 혼잡제어
440. [[176_rto_recovery_time_objective|RTO]] ([[440_rto_retransmission_timeout_measurement|Retransmission TimeOut]]) 측정 방식
441. [[441_rtt_round_trip_time_srtt_smoothed|RTT]] ([[441_rtt_round_trip_time_srtt_smoothed|Round Trip Time]]), SRTT (Smoothed [[441_rtt_round_trip_time_srtt_smoothed|RTT]]) - 혼잡 제어 동적 타이머
442. 칸 [[001_algorithm_definition|알고리즘]] (Karn's [[001_algorithm_definition|Algorithm]]) - 재전송 패킷 [[441_rtt_round_trip_time_srtt_smoothed|RTT]] 샘플 제외
443. [[443_spurious_retransmission_unnecessary_recovery|불필요한 재전송]] ([[443_spurious_retransmission_unnecessary_recovery|Spurious Retransmission]]) 해결 방안
444. [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] Keep-Alive 타이머
445. [[445_zero_window_probe_persist_timer|영 윈도우]] ([[445_zero_window_probe_persist_timer|Zero Window]]) 탐색 - Persist [[071_os_timer|Timer]]
446. [[446_mptcp_multipath_tcp_handover|MPTCP]] ([[446_mptcp_multipath_tcp_handover|Multipath TCP]]) - 다중 경로 [[140_bandwidth|대역폭]] 결합, 모바일/Wi-Fi [[556_handover_handoff_types_concept|핸드오버]] 무단절
447. [[447_sctp_multi_stream_multi_homing_4way_handshake|SCTP]] ([[467_http2_stream_multiplexing_tcp_hol|Stream]] Control Transmission [[295_protocol_field_tcp_udp_icmp|Protocol]]) - [[560_multi_stream_file_fork_ads|다중 스트림]], 멀티 호밍 (Multi-homing), 4단계 핸드셰이크([[475_cookie_local_state|쿠키]]방식)
448. [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 헤더 구조 - 8바이트 ([[446_port_and_bus|포트]], 길이, [[112_checksum|체크섬]] 등 최소 기능)
449. 브로드캐스트 / [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] 전송은 UDP만 가능
450. 실시간 전송, 오버헤드 최소화 목적 (VoIP, [[511_dns_hierarchical_distributed_architecture|DNS]], 스트리밍)
451. [[451_rtp_real_time_transport_protocol|RTP]] ([[451_rtp_real_time_transport_protocol|Real-time Transport Protocol]]) - [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 위에서 동작 (순서번호, 타임스탬프)
452. [[452_rtcp_rtp_control_protocol_monitoring|RTCP]] ([[452_rtcp_rtp_control_protocol_monitoring|RTP Control Protocol]]) - 품질 감시 [[229_monitor|모니터]]링
453. [[453_xtp_xpress_transport_protocol|XTP]] ([[453_xtp_xpress_transport_protocol|Xpress Transport Protocol]])
454. [[454_quic_quick_udp_internet_connections|QUIC]] (Quick [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] Internet Connections) - 전송 계층 혁신 (멀티플렉싱, 0-[[441_rtt_round_trip_time_srtt_smoothed|RTT]]/1-[[441_rtt_round_trip_time_srtt_smoothed|RTT]] 핸드셰이크)
455. [[454_quic_quick_udp_internet_connections|QUIC]] 전송 - TCP가 아닌 [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 상위에 구현됨
456. [[456_quic_hol_head_of_line_blocking_resolution|HOL]] ([[456_quic_hol_head_of_line_blocking_resolution|Head-of-Line]]) 블로킹 문제 해결 (독립적 [[229_stream_processing_kafka_flink|스트림 처리]] 적용)
457. [[454_quic_quick_udp_internet_connections|QUIC]] 연결 마이그레이션 ([[457_quic_connection_migration_connection_id|Connection Migration]]) - IP 변경시에도 연결 유지 (Connection ID)
458. [[694_thread_local_storage_tls|TLS]] 1.3 기본 내장 - [[283_security_tactics|보안성]]과 [[015_지연_데이터_관점|지연]] 단축 동시 확보
459. FEC 기능 선택적 포함 ([[459_quic_fec_forward_error_correction|초기]])
460. 패킷 손실 [[658_ir_recovery|복구]] 메커니즘 개선 - 고유 패킷 번호 (재전송시 번호 바뀜)

## 9. 응용 계층 - 웹, 이메일, [[501_file_definition_logical_record|파일]] 전송 (50개)
461. [[461_http_stateless_connection_oriented|HTTP]] ([[461_http_stateless_connection_oriented|HyperText Transfer Protocol]]) 상태 비저장 ([[239_stateless_redis|Stateless]]), 연결형/비연결형 특징
462. [[461_http_stateless_connection_oriented|HTTP]] 메서드 (GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD, TRACE)
463. [[461_http_stateless_connection_oriented|HTTP]] 1.0 (비지속 연결, 단점) - 매 요청마다 3-Way Handshake
464. [[461_http_stateless_connection_oriented|HTTP]] 1.1 - 지속 연결 (Persistent Connection, Keep-Alive), [[123_pipe|파이프]]라이닝 (Pipelining)
465. [[461_http_stateless_connection_oriented|HTTP]] 1.1 [[456_quic_hol_head_of_line_blocking_resolution|HOL]] 블로킹 (선행 응답 대기 [[015_지연_데이터_관점|지연]])
466. [[461_http_stateless_connection_oriented|HTTP]]/2 특징 - 바이너리 [[184_framing_mechanism|프레이밍]] 계층 추가 / SPDY 기반
467. [[461_http_stateless_connection_oriented|HTTP]]/2 스트림 ([[467_http2_stream_multiplexing_tcp_hol|Stream]]) [[071_다중화_Multiplexing|다중화]] ([[071_다중화_Multiplexing|Multiplexing]]) - [[456_quic_hol_head_of_line_blocking_resolution|HOL]] 우회 (단, [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] HOL은 잔존)
468. [[461_http_stateless_connection_oriented|HTTP]]/2 헤더 [[347_compaction|압축]] (HPACK [[001_algorithm_definition|알고리즘]] 활용)
469. [[461_http_stateless_connection_oriented|HTTP]]/2 서버 푸시 ([[469_http2_server_push|Server Push]])
470. [[461_http_stateless_connection_oriented|HTTP]]/3 특징 - [[454_quic_quick_udp_internet_connections|QUIC]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 활용, 완전한 멀티플렉싱, QPACK [[347_compaction|압축]], 연결 [[015_지연_데이터_관점|지연]] 거의 없음
471. [[471_https_http_over_tls|HTTPS]] ([[471_https_http_over_tls|HTTP over TLS]]) - [[002_confidentiality|기밀성]], [[003_integrity|무결성]] 지원 ([[446_port_and_bus|포트]] 443)
472. WWW [[456_caching|캐싱]] 메커니즘 / [[264_proxy_pattern_surrogate_access_control|프록시]]
473. [[473_cache_control_header|캐시 제어 헤더]] (Cache-Control: max-age, no-cache, no-store 등)
474. ETag / Last-Modified [[395_verification_process_review|검증]] ([[474_etag_last_modified_304|304 Not Modified]])
475. [[475_cookie_local_state|쿠키]] ([[475_cookie_local_state|Cookie]]) - 클라이언트 로컬 저장 상태 값
476. [[160_session_controlling_terminal|세션]] ([[160_session_controlling_terminal|Session]]) - 서버 측 상태 저장 값 (SID 발급)
477. [[477_rest_api_architecture|REST API]] ([[477_rest_api_architecture|Representational State Transfer]]) - 자원 중심 구조, [[461_http_stateless_connection_oriented|HTTP]] 메서드 매핑
478. [[246_graphql_query_language_overfetching_solution|GraphQL]] - 메타 개발, 클라이언트 주도 [[298_qkv_attention|쿼리]] 언어, 오버패칭 해소
479. [[479_grpc_protobuf_http2|gRPC]] - 구글 개발, [[535_sync_communication_rest_grpc|Protocol Buffers]] (ProtoBuf), [[461_http_stateless_connection_oriented|HTTP]]/2 기반 [[148_5g_embb_urllc_mmtc|초고속]] [[126_rpc|RPC]], [[302_service_mesh_istio|서비스 메시]]([[619_msa_traffic_hardware|MSA]])
480. [[480_websocket_full_duplex|WebSocket]] - 하나의 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 연결 위 전이중 (Full-Duplex) 실시간 브라우저-서버 통신
481. [[481_sse_server_sent_events|SSE]] ([[481_sse_server_sent_events|Server-Sent Events]]) - [[008_단방향_반이중_전이중|단방향]] 서버 푸시 기술
482. [[482_ftp_file_transfer_protocol|FTP]] ([[482_ftp_file_transfer_protocol|File Transfer Protocol]]) - 양방향 연결 (제어포트 21, [[001_dikw_pyramid|데이터]]포트 20)
483. [[483_active_vs_passive_ftp|액티브]]([[483_active_vs_passive_ftp|Active]]) [[482_ftp_file_transfer_protocol|FTP]] vs 패시브(Passive) [[482_ftp_file_transfer_protocol|FTP]] 동작 원리 차이
484. [[484_tftp_trivial_ftp|TFTP]] ([[484_tftp_trivial_ftp|Trivial FTP]]) - [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 기반 간단 [[501_file_definition_logical_record|파일]] 전송 ([[446_port_and_bus|포트]] 69)
485. [[485_sftp_ssh_file_transfer|SFTP]] ([[485_sftp_ssh_file_transfer|SSH FTP]]) - 보안 채널 위 [[501_file_definition_logical_record|파일]] 전송 ([[446_port_and_bus|포트]] 22)
486. [[486_ftps_ftp_over_ssl_tls|FTPS]] ([[482_ftp_file_transfer_protocol|FTP]] over SSL/[[694_thread_local_storage_tls|TLS]])
487. [[487_email_architecture_mua_mta_mda|이메일 아키텍처]] - MUA(메일 클라이언트), MTA(메일 서버), MDA(메일 수신 에이전트)
488. [[488_smtp_simple_mail_transfer_protocol|SMTP]] (Simple Mail Transfer [[295_protocol_field_tcp_udp_icmp|Protocol]]) - 메일 발송/중계 ([[446_port_and_bus|포트]] 25)
489. [[489_pop3_post_office_protocol_v3|POP3]] (Post Office [[295_protocol_field_tcp_udp_icmp|Protocol]] v3) - 서버 메일을 로컬로 다운(삭제) ([[446_port_and_bus|포트]] 110)
490. [[490_imap4_internet_message_access_protocol|IMAP4]] (Internet Message Access [[295_protocol_field_tcp_udp_icmp|Protocol]] v4) - 서버에 메일 보관 및 다중기기 [[212_synchronization_mechanisms|동기화]] ([[446_port_and_bus|포트]] 143)
491. SMTPS, POP3S, IMAPS ([[491_smtps_pop3s_imaps_secure_email|보안 캡슐화]])
492. [[492_mime_multipurpose_internet_mail_extensions|MIME]] (Multipurpose Internet Mail Extensions) - [[501_file_definition_logical_record|파일]] [[003_integrity|무결성]] 및 바이너리 [[001_dikw_pyramid|데이터]] 텍스트 인코딩 (Base64)
493. S/[[492_mime_multipurpose_internet_mail_extensions|MIME]] - 공개키 암호화 이메일 보안
494. [[494_pgp_pretty_good_privacy_web_of_trust|PGP]] ([[494_pgp_pretty_good_privacy_web_of_trust|Pretty Good Privacy]]) - 웹 오브 트러스트 기반 이메일 암호화 (Phil Zimmermann)
495. [[495_spf_sender_policy_framework|SPF]] ([[495_spf_sender_policy_framework|Sender Policy Framework]]) - 송신 서버 IP 기반 메일 [[598_spoofing|스푸핑]] 방지 ([[511_dns_hierarchical_distributed_architecture|DNS]] TXT [[396_validation|확인]])
496. [[496_dkim_domainkeys_identified_mail|DKIM]] ([[496_dkim_domainkeys_identified_mail|DomainKeys Identified Mail]]) - 디지털 서명 메일 위변조 [[395_verification_process_review|검증]]
497. [[497_dmarc_domain_based_message_authentication|DMARC]] - [[495_spf_sender_policy_framework|SPF]] + [[496_dkim_domainkeys_identified_mail|DKIM]] [[164_policy|정책]] 실패시 처리방침 (수신 거부, 격리 등) 가이드
498. [[498_webhook_rest_api_reverse_callback|웹훅]] ([[498_webhook_rest_api_reverse_callback|Webhook]]) - [[156_rest_representational_state_transfer|REST]] API의 콜백 역방향 호출 구조 (이벤트 발생 시 푸시)
499. [[499_bosh_bidirectional_streams_over_synchronous_http|BOSH]] (Bidirectional-streams Over [[010_동기식_비동기식_전송|Synchronous]] [[461_http_stateless_connection_oriented|HTTP]])
500. [[500_xmpp_extensible_messaging_presence_protocol|XMPP]] (Extensible Messaging and Presence [[295_protocol_field_tcp_udp_icmp|Protocol]]) - XML 기반 실시간 메신저
501. [[535_system_in_package|SIP]] ([[501_sip_session_initiation_protocol_voip|Session Initiation Protocol]]) - VoIP 호/섹션 제어 표준 (텍스트 기반)
502. H.323 - ITU-T 실시간 멀티미디어 화상회의 (바이너리 기반, 구형)
503. [[503_ip_pbx_private_branch_exchange|IP PBX]] - 구내 IP 사설 교환기
504. IPTV [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] ([[333_igmp_internet_group_management_protocol_multicast|IGMP]], [[430_pim|PIM]]) 전송
505. [[505_webrtc_web_real_time_communication|WebRTC]] ([[505_webrtc_web_real_time_communication|Web Real-Time Communication]]) - 플러그인 없는 브라우저간 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 오디오/음성 (Google 주도)
506. [[506_cdn_content_delivery_network_edge_caching|CDN]] (Content Delivery/Distribution Network) - 엣지 노드 위치 [[456_caching|캐싱]]
507. [[507_gslb_global_server_load_balancing_dns|GSLB]] (Global Server [[196_hard_soft_real_time|Load Balancing]]) - 사용자 위치 근접 서버 할당 ([[511_dns_hierarchical_distributed_architecture|DNS]] 이용)
508. Anycast 기반 [[506_cdn_content_delivery_network_edge_caching|CDN]] 설계
509. [[509_ocap_opencable_application_platform|OCAP]] ([[509_ocap_opencable_application_platform|OpenCable Application Platform]])
510. [[510_dash_dynamic_adaptive_streaming_over_http|DASH]] (Dynamic Adaptive Streaming over [[461_http_stateless_connection_oriented|HTTP]]) - 동적 [[140_bandwidth|대역폭]] 적응형 영상 스트리밍

## [[489_raid_10_hybrid|10]]. 응용 계층 - [[511_dns_hierarchical_distributed_architecture|DNS]] 및 네트워크 관리 (40개)
511. [[511_dns_hierarchical_distributed_architecture|DNS]] ([[511_dns_hierarchical_distributed_architecture|Domain Name System]]) 계층적 [[136_variance|분산]] 구조 (루트 - TLD - SLD)
512. [[512_recursive_iterative_dns_query|재귀적 질의]] ([[512_recursive_iterative_dns_query|Recursive Query]]) vs 반복적 질의 (Iterative Query)
513. [[513_forward_reverse_dns_lookup|정방향 조회]] (FQDN -> IP) vs 역방향 조회 (IP -> FQDN, in-addr.arpa)
514. [[511_dns_hierarchical_distributed_architecture|DNS]] 레코드 - A ([[286_ipv4_internet_protocol_version_4_rfc_791|IPv4]]), AAAA ([[324_ipv6_128bit_next_generation_address|IPv6]]), CNAME (별칭), MX (메일), NS (네임서버)
515. [[511_dns_hierarchical_distributed_architecture|DNS]] 레코드 - TXT (텍스트, [[495_spf_sender_policy_framework|SPF]] 등 용도), [[618_soa_hardware|SOA]] (Start of Authority, 존 시작점)
516. [[516_dns_zone_transfer_tcp_53|영역 전송]] ([[516_dns_zone_transfer_tcp_53|Zone Transfer]]) - [[446_port_and_bus|포트]] 53 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] ([[001_dikw_pyramid|데이터]] [[212_synchronization_mechanisms|동기화]]용)
517. 일반 [[511_dns_hierarchical_distributed_architecture|DNS]] 질의 - [[446_port_and_bus|포트]] 53 [[406_udp_user_datagram_protocol_connectionless_fast|UDP]]
518. [[518_dnssec_dns_security_extensions|DNSSEC]] ([[518_dnssec_dns_security_extensions|DNS Security Extensions]]) - [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] [[395_verification_process_review|검증]], 캐시 포이즈닝 대응 (디지털 서명 포함)
519. [[519_dot_dns_over_tls|DoT]] ([[519_dot_dns_over_tls|DNS over TLS]]) - [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 853 [[446_port_and_bus|포트]], 종단간 [[511_dns_hierarchical_distributed_architecture|DNS]] 질의 암호화
520. [[520_doh_dns_over_https|DoH]] ([[520_doh_dns_over_https|DNS over HTTPS]]) - [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 443 내 [[461_http_stateless_connection_oriented|HTTP]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 안에 [[511_dns_hierarchical_distributed_architecture|DNS]] 질의 은닉 (검열 회피/보안)
521. [[521_mdns_multicast_dns_llmnr|mDNS]] ([[521_mdns_multicast_dns_llmnr|Multicast DNS]]) / LMNR - 로컬망 이름 해석 (Apple Bonjour)
522. [[522_dhcp_dynamic_host_configuration_protocol|DHCP]] (Dynamic Host Configuration [[295_protocol_field_tcp_udp_icmp|Protocol]]) [[446_port_and_bus|포트]] 67, 68
523. [[522_dhcp_dynamic_host_configuration_protocol|DHCP]] 과정 4단계 ([[523_dhcp_dora_process|DORA]]) - Discover -> Offer -> Request -> Ack
524. [[524_dhcp_relay_agent|DHCP Relay Agent]] ([[522_dhcp_dynamic_host_configuration_protocol|DHCP]] 릴레이) - 브로드캐스트 패킷을 라우터 넘어로 Unicast 중계 제어
525. [[525_dhcp_lease_t1_t2_timers|DHCP Lease]] ([[525_dhcp_lease_t1_t2_timers|임대 시간]]) / [[522_dhcp_dynamic_host_configuration_protocol|DHCP]] 갱신 (T1/T2 타이머)
526. [[526_dhcp_snooping|DHCP Snooping]] - 불법 [[522_dhcp_dynamic_host_configuration_protocol|DHCP]] 서버 차단 보안기능 ([[238_switch_operation_principles|스위치]])
527. [[307_nat_network_address_translation_router_principles|NAT]]/[[522_dhcp_dynamic_host_configuration_protocol|DHCP]] 결합 환경 (Soho 라우터/공유기)
528. [[528_snmp_simple_network_management_protocol|SNMP]] (Simple Network [[372_management|Management]] [[295_protocol_field_tcp_udp_icmp|Protocol]]) - 네트워크 관리 목적, 기본 [[446_port_and_bus|포트]] 161 (Manager), 162 ([[677_trap_based_system_call_implementation|Trap]])
529. [[529_mib_oid_snmp_architecture|MIB]] ([[529_mib_oid_snmp_architecture|Management Information Base]]) / OID (Object [[088_identifier_in_er_model|Identifier]])
530. [[530_smi_structure_of_management_information|SMI]] (Structure of [[372_management|Management]] Information)
531. SNMPv1, v2c (Community String 노출 단점)
532. [[532_snmp_v3_security_authentication_encryption|SNMPv3]] (사용자 기반 [[303_authentication_authorization_patterns|인증]], [[389_mesh_topology|메시]]지 암호화 지원 [[086_des_data_encryption_standard|DES]]/[[656_aes_advanced_encryption_standard_rijndael|AES]])
533. [[528_snmp_simple_network_management_protocol|SNMP]] 명령 - Get, GetNext, Set
534. [[534_snmp_trap_inform|SNMP Trap]] - 에이전트 단에서 특정 이벤트 발생 시 자발적/[[008_단방향_반이중_전이중|단방향]] 통지 (알람)
535. [[535_syslog_protocol_udp_514|Syslog]] ([[535_syslog_protocol_udp_514|시스템 로그 프로토콜]]) - [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 514, 중앙 로깅
536. [[536_ntp_network_time_protocol_stratum|NTP]] ([[536_ntp_network_time_protocol_stratum|Network Time Protocol]]) - 계층적 시간 [[212_synchronization_mechanisms|동기화]], Stratum 레벨 모델 ([[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 123)
537. [[537_sntp_ptp_precision_time_protocol|SNTP]] ([[537_sntp_ptp_precision_time_protocol|Simple NTP]]) / PTP ([[233_precision_recall_f1_roc_auc_threshold|Precision]] Time [[295_protocol_field_tcp_udp_icmp|Protocol]], IEEE 1588 - 마이크로초 이내 정밀)
538. [[538_ssh_vs_telnet_secure_remote|SSH]] ([[538_ssh_vs_telnet_secure_remote|Secure Shell]]) [[446_port_and_bus|포트]] 22 / Telnet (원격 접속) [[446_port_and_bus|포트]] 23 비교
539. [[539_netflow_sflow_traffic_monitoring|NetFlow]] ([[539_netflow_sflow_traffic_monitoring|Cisco]]) / sFlow 트래픽 흐름 [[229_monitor|모니터]]링 분석 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
540. [[540_rmon_remote_network_monitoring|RMON]] ([[540_rmon_remote_network_monitoring|Remote Network Monitoring]]) - OSI 1,2계층 통계/에러 [[229_monitor|모니터]]링, [[529_mib_oid_snmp_architecture|MIB]] 내장
541. [[541_radius_remote_authentication_aaa|RADIUS]] (Remote [[604_authentication_factors|Authentication]] Dial-In User [[090_service_kubernetes_network_load_balancing|Service]]) - [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 기반 관리자/[[604_authentication_factors|사용자 인증]](AAA), 패스워드만 암호화
542. [[542_tacacs_plus_terminal_access_control_cisco|TACACS]]+ (Terminal Access Controller [[547_access_control_rwx|Access Control]] System Plus) - [[539_netflow_sflow_traffic_monitoring|Cisco]], [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 기반 AAA, 본문 전체 암호화, 명령어별 [[509_authorization_models_rbac_abac|인가]] 제어
543. [[543_ldap_lightweight_directory_access_protocol|LDAP]] (Lightweight [[506_directory_structure_symbol_table|Directory]] Access [[295_protocol_field_tcp_udp_icmp|Protocol]]) - X.500 기반 [[506_directory_structure_symbol_table|디렉터리]] 접근 권한 중앙관리 (AD 연동)
544. AAA 보안 모델 ([[604_authentication_factors|Authentication]] [[303_authentication_authorization_patterns|인증]], [[509_authorization_models_rbac_abac|Authorization]] [[509_authorization_models_rbac_abac|인가]], Accounting 과금/로깅)
545. [[545_kerberos_kdc_ticket_based_auth|커버로스]] ([[545_kerberos_kdc_ticket_based_auth|Kerberos]]) - [[583_kdc|KDC]]([[583_kdc|Key Distribution Center]])/티켓 기반 [[303_authentication_authorization_patterns|인증]], 타임스탬프 재전송 방지
546. OAuth 2.0 - 타사 애플리케이션 보안 [[303_authentication_authorization_patterns|인증]] 위임 프레임워크 (Access Token)
547. SAML 2.0 ([[283_security_tactics|Security]] Assertion Markup Language) - B2B 환경 [[531_sso|SSO]] 구현, XML 기반
548. [[548_openid_connect|OpenID Connect]] - OAuth 2.0 기반 사용자 [[655_ir_detection_analysis|식별]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[515_id_token_jwt|ID Token]], [[549_jwt_json_web_token|JWT]])
549. [[549_jwt_json_web_token|JWT]] ([[549_jwt_json_web_token|JSON Web Token]]) - 비상태 서버형 [[303_authentication_authorization_patterns|인증]] 저장
550. X.509 v3 디지털 [[303_authentication_authorization_patterns|인증]]서 표준 규격

## [[308_static_dynamic_nat_pat_port_address_translation|11]]. 무선통신 및 이동통신 기초/기술 (50개)
551. [[551_cellular_network_concept_reuse_handover|이동통신망]]([[551_cellular_network_concept_reuse_handover|Cellular Network]]) 통신 개념 (재사용, [[556_handover_handoff_types_concept|핸드오버]])
552. [[552_fdd_vs_tdd_wireless_duplexing|주파수 분할 방식]]([[103_fdd|FDD]]) vs 시분할 방식([[164_tdd_test_driven_development|TDD]]) 무선 환경 적용
553. [[553_macro_micro_pico_femto_cell_topology|매크로 뷰]] ([[553_macro_micro_pico_femto_cell_topology|Macro Cell]]) 토폴로지 / 피코 셀(Pico)/마이크로 셀(Micro)
554. [[554_frequency_reuse_cluster_capacity|주파수 재사용]] ([[554_frequency_reuse_cluster_capacity|Frequency Reuse]]) - 클러스터 디자인, 용량 확장 기법
555. [[555_co_channel_adjacent_interference|Co-channel Interference]] ([[555_co_channel_adjacent_interference|동일 채널 간섭]]) / Adjacent Channel Interference (인접 채널 간섭)
556. [[556_handover_handoff_types_concept|핸드오버]] ([[556_handover_handoff_types_concept|Handover]]) / 핸드오프 (Handoff) 종류 개념
557. [[557_hard_handover_break_before_make_lte|하드 핸드오버]] ([[557_hard_handover_break_before_make_lte|Hard Handoff]]) - "Break before make", LTE방식
558. [[558_soft_handoff|소프트 핸드오버]] ([[558_soft_handoff|Soft Handoff]]) - "Make before break", 다중 주파수 동시 수신, [[957_cdma_code_division_multiple_access_dsss_orthogonality|CDMA]] 방식
559. [[559_call_admission_control|호 수락 제어]] (CAC, [[559_call_admission_control|Call Admission Control]])
560. [[560_roaming|로밍]] ([[560_roaming|Roaming]]) - 타 망사업자 통신망간 [[090_service_kubernetes_network_load_balancing|서비스]] 연동
561. [[561_mobility_management_hlr_vlr_paging|이동성 관리]] ([[561_mobility_management_hlr_vlr_paging|Mobility Management]]) - HLR (Home Location [[175_register_addressing|Register]]), VLR ([[275_visitor_pattern|Visitor]]) 구조
562. [[562_mipv4_mobile_ipv4_ha_fa_triangular|MIPv4]] ([[562_mipv4_mobile_ipv4_ha_fa_triangular|Mobile IPv4]]) - FA(Foreign Agent), HA(Home Agent), 세모 [[339_routing_overview_best_path_selection|라우팅]] (Triangular [[339_routing_overview_best_path_selection|Routing]]) 문제 해결방안 (RO)
563. [[563_mipv6_mobile_ipv6_slaac_ro|MIPv6]] ([[563_mipv6_mobile_ipv6_slaac_ro|Mobile IPv6]]) - FA 불필요([[331_slaac_stateless_address_autoconfiguration_ndp|SLAAC]]), 기본 최적 경로(RO) 지원
564. [[170_diversity_system_equalizer|다이버시티 시스템]]([[170_diversity_system_equalizer|Diversity System]]) - 공간([[171_antenna_basic_dipole_resonance|안테나]]), 주파수, 시간, 편파(Polarize) 다이버시티
565. [[565_rake_receiver_multipath_fading_cdma|레이크 수신기]] ([[565_rake_receiver_multipath_fading_cdma|Rake Receiver]]) - 시간 [[015_지연_데이터_관점|지연]]된 다중경로 [[130_signal|신호]] 결합([[957_cdma_code_division_multiple_access_dsss_orthogonality|CDMA]])
566. [[566_equalizer_isi_inter_symbol_interference|등화기]] ([[566_equalizer_isi_inter_symbol_interference|Equalizer]]) - ISI 상쇄 필터
567. [[177_smart_antenna_phased_array|스마트 안테나]] ([[177_smart_antenna_phased_array|Smart Antenna]])
568. [[568_switched_beam_vs_adaptive_array|스위칭 빔]] ([[568_switched_beam_vs_adaptive_array|Switched Beam]]) vs 적응형 어레이 (Adaptive [[055_array|Array]] [[171_antenna_basic_dipole_resonance|안테나]])
569. [[097_MIMO_다중_안테나_기술|MIMO]] 기반 [[100_공간_다중화_Spatial_Multiplexing|공간 다중화]] 체계 (V-BLAST 구조 등)
570. [[570_wimax_802_16_wibro_mobile_broadband|WiMAX]] (IEEE 802.16) / 휴대인터넷(WiBro) 개요 - 와이브로(모바일 [[570_wimax_802_16_wibro_mobile_broadband|WiMAX]])
571. 무선 LAN ([[571_wlan_bss_ess_structure|WLAN]]) 구조 [[136_variance|분산]]: [[083_bss_segment|BSS]](Basic [[090_service_kubernetes_network_load_balancing|Service]] Set), [[164_ess_energy_storage_system|ESS]](Extended [[090_service_kubernetes_network_load_balancing|Service]] Set)
572. [[572_ap_access_point_ds_distribution_system|AP]] ([[572_ap_access_point_ds_distribution_system|Access Point]]) / DS (Distribution System, 분배 시스템)
573. 802.[[308_static_dynamic_nat_pat_port_address_translation|11]] b/g/a/n 표준 세대 발전
574. 802.[[574_802_11n_wifi_4_mimo_channel_bonding|11n]] ([[574_802_11n_wifi_4_mimo_channel_bonding|Wi-Fi 4]]) - [[097_MIMO_다중_안테나_기술|MIMO]] 채용, 채널 본딩 (20->40MHz) 300~600Mbps
575. 802.[[575_802_11ac_wifi_5_mu_mimo|11ac]] ([[575_802_11ac_wifi_5_mu_mimo|Wi-Fi 5]]) - MU-[[097_MIMO_다중_안테나_기술|MIMO]] (다운링크 한정), 5GHz [[140_bandwidth|대역폭]] 80~160MHz 
576. 802.[[576_802_11ax_wifi_6_ofdma_twt|11ax]] ([[576_802_11ax_wifi_6_ofdma_twt|Wi-Fi 6]]) - [[945_ofdma_orthogonal_frequency_division_multiple_access_resource_block|OFDMA]] 도입, 양방향 MU-[[097_MIMO_다중_안테나_기술|MIMO]], 타겟 웨이크 타임(TWT), 고밀도망 속도 저하 해소
577. 802.[[577_802_11ax_6ghz_wifi_6e|11ax 6GHz]] ([[158_wifi_6e|Wi-Fi 6E]]) - 간섭없는 6GHz 대역 무선 환경 확장
578. 802.[[578_802_11be_wifi_7_mlo_4k_qam|11be]] ([[578_802_11be_wifi_7_mlo_4k_qam|Wi-Fi 7]]) - 320MHz 초광대역폭 채널, 4K-QAM 적용, MLO (Multi-Link [[329_delta_encoding|Operation]], 동시 다중링크 작동) 초저지연
579. 무선 LAN 보안 진화 ([[580_wep_wired_equivalent_privacy_rc4|WEP]] -> [[581_wpa_tkip_802_1x_eap|WPA]] -> [[582_wpa2_aes_ccmp_personal_enterprise|WPA2]] -> [[583_wpa3_sae_owe_enhanced_open|WPA3]])
580. [[580_wep_wired_equivalent_privacy_rc4|WEP]] ([[580_wep_wired_equivalent_privacy_rc4|Wired Equivalent Privacy]]) - [[081_rc4_stream_cipher|RC4]] 기반, 취약점(정적키) 노출
581. [[581_wpa_tkip_802_1x_eap|WPA]] (TKIP + 802.[[584_802_1x_pnac_eap_radius|1X]] + [[229_eap_extensible_authentication_protocol|EAP]])
582. [[582_wpa2_aes_ccmp_personal_enterprise|WPA2]] ([[656_aes_advanced_encryption_standard_rijndael|AES]]-CCMP 기반) 강력 암호화, 개인용([[142_psk_pre_shared_key|PSK]])/기업용(Enterprise/[[541_radius_remote_authentication_aaa|RADIUS]])
583. [[583_wpa3_sae_owe_enhanced_open|WPA3]] - SAE (Simultaneous [[604_authentication_factors|Authentication]] of Equals) 핸드셰이크 도입 (오프라인 딕셔너리 공격 완전차단), 관리 프레임 [[571_protection_vs_security|보호]] (PMF, 필수 적용), 192비트 기업급 보안 스위트(CNSA/Suite B)
584. 802.[[584_802_1x_pnac_eap_radius|1X]] (PNAC, [[446_port_and_bus|Port]] Based [[226_nac_network_access_control_ieee_802_1x|Network Access Control]]) [[303_authentication_authorization_patterns|인증]] 및 [[229_eap_extensible_authentication_protocol|EAP]]/[[541_radius_remote_authentication_aaa|RADIUS]] 체계
585. [[585_captive_portal_guest_web_auth|캡티브 포털]] ([[585_captive_portal_guest_web_auth|Captive Portal]]) - 게스트 웹 기반 접속 [[303_authentication_authorization_patterns|인증]]
586. [[171_antenna_basic_dipole_resonance|안테나]] 증폭 측정 지표: dBm 반값 전력각 등
587. [[587_wireless_mesh_network_daisy_chain|무선 메시 네트워크]] ([[587_wireless_mesh_network_daisy_chain|Wireless Mesh Network]]) - [[354_daisy_chain|데이지 체인]] 구조 연결 자동화
588. [[588_manet_mobile_ad_hoc_network|MANET]] ([[588_manet_mobile_ad_hoc_network|Mobile Ad-hoc Network]]) - 기지국 없는 노드 기반 네트워크 [[339_routing_overview_best_path_selection|라우팅]] (AODV 규칙)
589. [[141_v2x_vehicle_to_everything_communication|V2X]] ([[589_v2x_vehicle_to_everything_autonomous|Vehicle to Everything]]) - 차량 자율주행, 차량통신 핵심
590. [[590_wave_ieee_802_11p_dsrc_v2x|WAVE]] (IEEE 802.11p 무선차량통신) [[1025_c_v2x_wave_dsrc|DSRC]](단거리전용)
591. [[143_c_v2x_cellular_based_communication|C-V2X]] ([[143_c_v2x_cellular_based_communication|Cellular V2X]]) - [[751_3gpp_3rd_generation_partnership_project|3GPP]] 표준, 이동통신([[752_lte_long_term_evolution_4g|LTE]]/[[418_5g_embb_urllc_mmtc_slicing|5G]]) 연계 차량 통신
592. [[592_satellite_communication_characteristics|위성 통신]] ([[592_satellite_communication_characteristics|Satellite Comm]].) 특징
593. [[593_geo_geostationary_earth_orbit_satellite|정지 궤도 위성]] ([[593_geo_geostationary_earth_orbit_satellite|GEO]]) - 약 35,800km 고도 통신 위성 ([[015_지연_데이터_관점|지연]] 심함)
594. [[594_meo_medium_earth_orbit_gps|중궤도 위성]] ([[594_meo_medium_earth_orbit_gps|MEO]]) (GPS, 항법시스템)
595. [[595_leo_low_earth_orbit_starlink_6g|저궤도 위성]] ([[595_leo_low_earth_orbit_starlink_6g|LEO]]) - 500~1500km 고도. 초저지연 글로벌 [[419_6g_ntn_thz_ris_next_gen|6G]] 망 구성, Starlink(스타링크), OneWeb(원웹)
596. [[596_haps_high_altitude_platform_station_drone|HAPS]] (고고도 전송 기지국, 성층권 드론 통신)
597. GPS (Global Positioning System) 삼각 측량 / 오차 개선 기법 (DGPS, RTK)
598. [[160_uwb_ultra_wideband|UWB]] ([[598_uwb_ultra_wideband_indoor_positioning|Ultra-Wideband]]) - 초광대역 근거리 정밀 위치인식통신, 임펄스 전송 (Apple AirTag 등)
599. 무선 충전 전송 원리 (자기 유도형 WPC Qi, 자기 공명형 A4WP)
600. RFID / NFC [[295_protocol_field_tcp_udp_icmp|프로토콜]] 기본 구상

## 12. [[101_iot_concept|사물인터넷]]([[101_iot_concept|IoT]]), [[604_wpan_wireless_personal_area_network|WPAN]] 및 엣지 통신 (50개)
601. [[101_iot_concept|사물인터넷]] ([[101_iot_concept|IoT]], Internet of Things)의 3대 요소 (디바이스, 네트워크, 클라우드/플랫폼)
602. [[602_m2m_machine_to_machine_telemetry|사물 통신]] ([[602_m2m_machine_to_machine_telemetry|M2M]]) - 기기 간 직접 연결 (IoT의 근본)
603. [[103_wsn_sensor_network|센서 네트워크]] ([[103_wsn_sensor_network|WSN]], Wireless Sensor Network) / 싱크 노드 (Sink Node) 구성
604. [[604_wpan_wireless_personal_area_network|WPAN]] (Wireless Personal Area Network) - 개인 작업공간 무선
605. [[605_bluetooth_ieee_802_15_1_piconet_scatternet|블루투스]] ([[605_bluetooth_ieee_802_15_1_piconet_scatternet|Bluetooth]]) - IEEE 802.15.1, ISM 대역(2.4GHz), 피코넷(Piconet), 스캐터넷(Scatternet) 마스터/슬레이브
606. [[606_bluetooth_edr_hs_speed_extension|블루투스 버전]] - [[325_edr|EDR]], HS 속도 확장
607. [[607_ble_bluetooth_low_energy_iot|BLE]] ([[607_ble_bluetooth_low_energy_iot|Bluetooth Low Energy]]) - BT 4.0, 저전력 특화, [[101_iot_concept|IoT]] 핵심
608. [[608_beacon_technology_ibeacon_eddystone|비컨]] ([[608_beacon_technology_ibeacon_eddystone|Beacon]]) 기술 - iBeacon(애플 환경), Eddystone(오픈 소스 [[605_bluetooth_ieee_802_15_1_piconet_scatternet|블루투스]] 로케이터)
609. [[609_zigbee_ieee_802_15_4_mesh_iot|ZigBee]] ([[609_zigbee_ieee_802_15_4_mesh_iot|지그비]]) - IEEE 802.15.4 초저전력 제어/감시용 메쉬 네트워킹 표준, 250Kbps
610. [[610_z_wave_900mhz_smart_home_iot|Z-Wave]] (Z웨이브) - 홈네트워크 최적화 900MHz 무선 통신 [[009_semiconductor|반도체]] 생태계 주도
611. [[092_thread_lwp|Thread]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] - [[324_ipv6_128bit_next_generation_address|IPv6]] 통신 기반 [[389_mesh_topology|메시]] [[604_wpan_wireless_personal_area_network|WPAN]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] (스마트홈 [[101_iot_concept|IoT]] 지원)
612. [[612_matter_csa_smart_home_standard|Matter]] ([[612_matter_csa_smart_home_standard|매터]]) 보안 통일 표준(CSA) - 애플/구글/아마존 간 통일형 스마트홈 상호 운용성 표준 (위 Layer 적용)
613. [[117_6lowpan_iot_ipv6|6LoWPAN]] - IEEE 802.15.4 환경의 저전력 장치를 IP 계층인 [[324_ipv6_128bit_next_generation_address|IPv6]] 로 인터넷 연동시키는 헤더 [[347_compaction|압축]]/[[291_fragmentation_and_reassembly_process|단편화]] ([[101_iot_concept|IoT]] 핵심)
614. [[614_rpl_ipv6_routing_low_power_lossy|RPL]] ([[324_ipv6_128bit_next_generation_address|IPv6]] [[339_routing_overview_best_path_selection|Routing]] [[295_protocol_field_tcp_udp_icmp|Protocol]] for Low-[[069_type_1_2_error_statistical_power|Power]] and Lossy Networks) - [[101_iot_concept|IoT]] 무선 최적 [[339_routing_overview_best_path_selection|라우팅]] [[001_algorithm_definition|알고리즘]]
615. [[109_lpwan_low_power_wide_area_network|LPWAN]] ([[615_lpwan_low_power_wide_area_network|Low-Power Wide-Area Network]]) 개요 (저전력 광역 통신) - 수십km 커버리지
616. 비면허 대역 [[109_lpwan_low_power_wide_area_network|LPWAN]] 분야
617. [[617_lora_lorawan_css_chirp_spread_spectrum|LoRa]] ([[617_lora_lorawan_css_chirp_spread_spectrum|Long Range]]) / LoRaWAN 표준 - [[110_unlicensed_lpwan_lorawan_sigfox|CSS]] (Chirp [[068_스펙트럼_확산_Spread_Spectrum|Spread Spectrum]]) 방식의 비면허 글로벌 저전력 장거리
618. [[1030_lpwan_sigfox|Sigfox]] - 초협대역(UNB) 100bps 극초저전력, 소용량/프랑스 기반 상용화
619. 면허 대역 [[109_lpwan_low_power_wide_area_network|LPWAN]] 분야 (이동통신사 기반형 [[101_iot_concept|IoT]])
620. [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]] ([[620_nbiot_narrowband_iot_lte_guardband|Narrowband IoT]]) - [[752_lte_long_term_evolution_4g|LTE]] 주파수 여유 대역/[[571_protection_vs_security|보호]]대역 기반 200kHz 협대역 활용 [[101_iot_concept|IoT]] 표준 ([[751_3gpp_3rd_generation_partnership_project|3GPP]] Rel.13)
621. [[621_ltem_emtc_iot_mobility_voice|LTE-M]] ([[621_ltem_emtc_iot_mobility_voice|eMTC]]) - Cat-M1 등 음성/1Mbps 이동([[556_handover_handoff_types_concept|핸드오버]]) 및 웨어러블 지원 [[101_iot_concept|IoT]]
622. [[622_mqtt_publish_subscribe_qos|MQTT]] (Message Queuing Telemetry Transport) - [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 기반 퍼블리시-서브스크라이브 경량 [[389_mesh_topology|메시]]지 ([[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 0/1/2 등급 지원) 브로커(Broker) 중심 [[136_variance|분산]]형
623. [[120_coap_constrained_application_protocol|CoAP]] ([[120_coap_constrained_application_protocol|Constrained Application Protocol]]) - [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 제어 기반, [[156_rest_representational_state_transfer|REST]]/[[461_http_stateless_connection_oriented|HTTP]] 메타 대응 경량 [[295_protocol_field_tcp_udp_icmp|프로토콜]], 브로커리스 구조([[644_dtls_datagram_tls_coap_security|DTLS]] 접속 지원)
624. [[121_lwm2m_lightweight_m2m|LwM2M]] ([[121_lwm2m_lightweight_m2m|Lightweight M2M]]) 표준 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 관리 메커니즘
625. oneM2M 아키텍처 (국제 표준 통합 [[602_m2m_machine_to_machine_telemetry|M2M]] 구조화 플랫폼)
626. [[235_edge_computing_smart_factory|엣지 컴퓨팅]] ([[235_edge_computing_smart_factory|Edge Computing]], [[106_fog_computing_cisco_architecture|포그 컴퓨팅]] 구분) - 종단 클라이언트 인접 노드 [[001_dikw_pyramid|데이터]] [[136_variance|분산]] 처리 방식
627. [[627_mec_multi_access_edge_computing_5g|MEC]] (Multi-access [[235_edge_computing_smart_factory|Edge Computing]] / Mobile [[235_edge_computing_smart_factory|Edge Computing]]) - [[418_5g_embb_urllc_mmtc_slicing|5G]], 이통망 기지국 근접하여 연산, 초저지연 확보
628. [[161_smart_grid_architecture|스마트 그리드]] ([[161_smart_grid_architecture|Smart Grid]] 파워 네트워크 통신 인프라)
629. [[629_microgrid_ami_smart_meter_plc_rf|마이크로 그리드]] ([[163_microgrid_island_mode|Microgrid]]) / [[162_ami_advanced_metering_infrastructure|AMI]] (원격검침인프라) 통신 ([[896_plc_programmable_logic_controller|PLC]]/RF 장치) 탑재 방식
630. [[630_industrial_ethernet_profinet_ethercat_modbus|산업용 이더넷 표준]] ([[630_industrial_ethernet_profinet_ethercat_modbus|Industrial Ethernet]]) - [[900_profinet|PROFINET]], EtherCAT, Modbus [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] (타임크리티컬)
631. [[631_opc_ua_smart_factory_protocol|OPC UA]] - [[166_smart_factory|스마트 팩토리]], 산업용/제조용 디바이스 안전한 [[001_dikw_pyramid|데이터]] 통신 확장 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 통합
632. [[546_tsn_hardware|TSN]] ([[168_industrial_ethernet_tsn|Time-Sensitive Networking]]) - IEEE 802.1 / 시간 결정형 유선 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]], 정밀 동기(마이크로/나노단위 트래픽 자원 보장/[[212_synchronization_mechanisms|동기화]]) (산업용 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 대체 5G망 연계)
633. [[633_v2v_v2i_autonomous_vehicle_communication|자율주행 차량 통신]] (V2V, V2I 교통인프라 교환)
634. [[123_ocf_open_connectivity_foundation|OCF]] ([[123_ocf_open_connectivity_foundation|Open Connectivity Foundation]]) [[101_iot_concept|IoT]] 통합 관리 계층 표준
635. [[635_ietf_core_working_group_coap|IETF]] (Internet Engineering [[150_task|Task]] Force) 산하 [[101_iot_concept|IoT]] CoRE 워킹그룹 동향
636. [[636_wot_web_of_things_w3c_thing_description|W3C WoT]] ([[636_wot_web_of_things_w3c_thing_description|Web of Things]]) - 모든 기기를 URL 자원으로 통합 제어 개념
637. [[637_iiot_industrial_iot_qos_latency|IIoT]] (공업계 [[101_iot_concept|사물인터넷]]/산업용 [[101_iot_concept|IoT]]) 트래픽 관리 한계/[[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 이슈
638. [[171_smart_city_platform_architecture|스마트 시티]] ([[171_smart_city_platform_architecture|Smart City]] 통신망 [[071_다중화_Multiplexing|다중화]] 연계) 센싱 시스템
639. 드론 통신 [[015_지연_데이터_관점|지연]]시간 관리 및 보안 [[746_c2|C2]] 링크 ([[639_drone_c2_link_command_control_latency|Command & Control]])
640. [[640_aiot_ai_and_iot_edge_cloud_latency|AIoT]] ([[190_ai_llm_requirements_specification|AI]] + [[101_iot_concept|IoT]]) 모델 및 클라우드 [[190_ai_llm_requirements_specification|AI]] 연결 [[015_지연_데이터_관점|지연]] 완화 기술
641. 홈 네트워크 게이트웨이 / 월패드 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 보안 (RS-485 해킹, 분리 [[164_policy|정책]] 논란)
642. [[182_network_separation_model|망분리]] ([[182_network_separation_model|Network Separation]]) 및 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] 연결형 [[369_logic_bomb|논리]]망 [[007_security_policy|보안 정책]]
643. 기기 간 상호인증체계 관리 기법 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 연결 [[303_authentication_authorization_patterns|인증]]서 배포 기술
644. [[644_dtls_datagram_tls_coap_security|DTLS]] ([[644_dtls_datagram_tls_coap_security|Datagram TLS]]) [[295_protocol_field_tcp_udp_icmp|프로토콜]] [[120_coap_constrained_application_protocol|CoAP]] 결합
645. 소형 [[171_antenna_basic_dipole_resonance|안테나]] 시스템/초소형 센서 [[175_ambient_backscatter_communication|백스캐터 통신]] (Ambient Backscatter 통신, 에너지 하베스팅)
646. [[646_passive_iot_intermittent_computing|무전원 통신]] (Passive [[101_iot_concept|IoT]] 통신) 환경 적응
647. [[167_cps_cyber_physical_system|CPS]] (Cyber-Physical System 트윈/메타 [[001_dikw_pyramid|데이터]] 전송 요구사항)
648. [[648_smart_meter_two_way_communication_ami|양방향 스마트 계량기]] (Smart Meter 통신 규격)
649. 홈넷/[[101_iot_concept|IoT]] [[990_botnet_cnc|봇넷]] 방어 기법 (Mirai [[990_botnet_cnc|Botnet]] DDOS 예방 [[446_port_and_bus|포트]] 필터)
650. 저전력/메모리 한계 환경 경량 [[076_symmetric_encryption|대칭키 암호]] (LEA 표준, ARIA 등 최적화 적용)

## 13. [[1117_network_security_zero_trust_policy|네트워크 보안]] (기본 기법) (50개)
651. [[651_cia_triad_confidentiality_integrity_availability|정보보안 3대 요소]] (CIA 트라이어드: [[002_confidentiality|기밀성]], [[003_integrity|무결성]], [[452_availability|가용성]]) + [[303_authentication_authorization_patterns|인증]], 부인방지 요구
652. [[652_cryptography_concept_encryption_decryption|암호학]] ([[652_cryptography_concept_encryption_decryption|Cryptography]]) 개요 통신망 보안 적용 (평문->암호문->평문 변환 체계)
653. [[653_symmetric_key_cryptography_fast_speed|대칭키 암호화]] ([[653_symmetric_key_cryptography_fast_speed|Symmetric Key]]) - 암/복호화 키 동일, 공유기밀 분배, 고속 처리
654. [[654_stream_cipher_rc4_chacha20|스트림 암호]] ([[654_stream_cipher_rc4_chacha20|Stream Cipher]]) - [[081_rc4_stream_cipher|RC4]] ([[580_wep_wired_equivalent_privacy_rc4|WEP]] 등, 최신 사장), ChaCha20
655. [[655_block_cipher_des_3des_feistel|블록 암호]] ([[655_block_cipher_des_3des_feistel|Block Cipher]]) - [[086_des_data_encryption_standard|DES]] (56bit 비권장), [[087_3des|3DES]] (과도기) 모델
656. [[656_aes_advanced_encryption_standard_rijndael|AES]] ([[656_aes_advanced_encryption_standard_rijndael|Advanced Encryption Standard]]) - 국제 대표 표준, Rijndael 구조 (128/192/256bit 체계)
657. SEED, ARIA, LEA - 대한민국의 표준 블록/경량 암호 방식 체계
658. [[655_block_cipher_des_3des_feistel|블록 암호]] 운영 모드 (ECB 기본/취약 모드, [[089_cbc_mode|CBC]]([[288_version_ihl_tos_total_length|IV]] 필요), CFB, OFB, [[090_ctr_mode|CTR]])
659. [[659_gcm_galois_counter_mode_aead|GCM]] (Galois/[[059_counter|Counter]] Mode) 모드 - 암호화와 더불어 [[001_dikw_pyramid|데이터]] [[303_authentication_authorization_patterns|인증]] 기능 탑재 ([[092_aead|AEAD]] - [[694_thread_local_storage_tls|TLS]] 1.3의 핵심 모드)
660. 비대칭키/공개키 암호화 (Asymmetric/Public [[067_db_key_uniqueness_minimality|Key]]) - 암/복호화 키 상이, 서명(개인키)/기밀화(공개키 전송) 가능
661. [[661_asymmetric_key_math_factorization_dlp|수학적 문제 기반]](소인수분해, 이산대수 등)
662. [[110_rsa|RSA]] [[001_algorithm_definition|알고리즘]] - 가장 보편적 (소인수분해 수학 난해성, 2048bit 권장)
663. ElGamal 및 DSA ([[663_elgamal_dsa_discrete_logarithm_digital_signature|디지털 서명용 특화]]) 시스템
664. [[554_ecc_circuit|ECC]] (Elliptical Curve [[652_cryptography_concept_encryption_decryption|Cryptography]], 타원 곡선 통신망 적용) - 짧은 키 (256bit)로 [[110_rsa|RSA]] 3072bit 효과 발휘 ([[148_5g_embb_urllc_mmtc|초고속]], 모바일/[[101_iot_concept|IoT]] 적용)
665. [[097_ecdsa_schnorr_signature_bitcoin|ECDSA]], Ed25519 (고성능 차세대 공개키 디지털 [[675_digital_signature_process_asymmetric_key|전자서명]] 방식)
666. 디피-헬만 상호 키 교환 ([[666_diffie_hellman_key_exchange_mitm|Diffie-Hellman Key Exchange]]) 원리 및 스니핑 취약점
667. [[667_hash_function_integrity_one_way|해시 함수]] ([[667_hash_function_integrity_one_way|Hash Function]]) - [[003_integrity|무결성]] 점검을 위한 일방향 고정길이 [[347_compaction|압축]]
668. [[668_md5_hash_collision_vulnerability|MD5]] (취약성/충돌 노출) 회피 조치, SHA-1 차단
669. SHA-2 패밀리 - SHA-256 / SHA-512 위주 통신망 서명 기본 기술
670. [[101_sha_3|SHA-3]] 패밀리 - 스펀지(Sponge) 펑션 방식 [[101_sha_3|Keccak]] 로직, 기존 방어 [[352_defect_definition|결함]] 해소
671. [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]] ([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]]) 첨가 패스워드 해시 (PBKDF2, bcrypt, Argon2) 체계 - 레인보우 테이블 방지
672. [[003_integrity|무결성]] 및 출처 [[303_authentication_authorization_patterns|인증]]용 서명 [[001_dikw_pyramid|데이터]] 코드 제어
673. [[673_mac_message_authentication_code|MAC]] ([[673_mac_message_authentication_code|Message Authentication Code]]) 변수 및 기능
674. [[674_hmac_hash_based_mac_ipsec|HMAC]] ([[674_hmac_hash_based_mac_ipsec|Hash-based MAC]]) 통신 기반 [[589_ipsec_offload|IPsec]] 등 활용 구조 - 공유키 결합 해시
675. [[675_digital_signature_process_asymmetric_key|전자서명]] ([[675_digital_signature_process_asymmetric_key|Digital Signature]]) [[087_process_state_transition|생성]]/[[395_verification_process_review|검증]] 프로세스 개요 (비대칭키 활용 체계의 [[003_integrity|무결성]] 보증)
676. [[676_pki_public_key_infrastructure|공개키 기반 구조]] ([[159_pki_public_key_infrastructure|PKI]], [[984_pki_public_key_infrastructure_ca_ra_certificate|Public Key Infrastructure]]) 아키텍처 보안 증명 시스템
677. [[677_ca_ra_certificate_authority_registration|인증국]] ([[089_contract_account_smart_contract|CA]], Certificate Authority), 등록기관 ([[161_ra_registration_authority|RA]], [[161_ra_registration_authority|Registration Authority]]), 저장소 체계
678. [[678_crl_certificate_revocation_list|CRL]] ([[678_crl_certificate_revocation_list|Certificate Revocation List]]) 스펙 및 폐기 문제 및 배포 [[015_지연_데이터_관점|지연]] 약점 완화 체계
679. [[679_ocsp_online_certificate_status_protocol|OCSP]] (Online Certificate Status [[295_protocol_field_tcp_udp_icmp|Protocol]]) - 실시간 [[303_authentication_authorization_patterns|인증]]서 상태 응답 검사 체계
680. [[680_ocsp_stapling_tls_handshake_performance|OCSP Stapling]] ([[694_thread_local_storage_tls|TLS]] Handshake 트래픽 [[282_performance_tactics|성능]] 확장용 서버 캐시 상태 전송 메커니즘 개선기법)
681. SSL/[[694_thread_local_storage_tls|TLS]] (Secure [[125_socket|Socket]] Layer / Transport Layer [[283_security_tactics|Security]]) 통신 모델 개요 
682. [[694_thread_local_storage_tls|TLS]] Handshake [[295_protocol_field_tcp_udp_icmp|프로토콜]] (3-Way 유사 연결 [[459_quic_fec_forward_error_correction|초기]]화, [[160_session_controlling_terminal|세션]]키 협상, Cipher Suite 교환 포함)
683. Cipher Suite 모델 표기방식 예시 ([[683_cipher_suite_notation|TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256]]) 이해 방식
684. [[694_thread_local_storage_tls|TLS]] 전방향 안전성 (PFS, Perfect [[235_forward_backward_chaining|Forward]] Secrecy) 보장 원리 ([[110_rsa|RSA]] 직접 복호 문제 해결/임시 [[160_session_controlling_terminal|세션]]키) 
685. [[694_thread_local_storage_tls|TLS]] 1.3 업그레이드 변화와 0-[[441_rtt_round_trip_time_srtt_smoothed|RTT]]/1-[[441_rtt_round_trip_time_srtt_smoothed|RTT]] [[282_performance_tactics|성능]] 향상 차이
686. [[673_mac_message_authentication_code|MAC]]-then-Encrypt 패러다임 / [[092_aead|AEAD]] 전환 보안 구조
687. [[687_tls_session_resumption_ticket|세션 재개]] ([[160_session_controlling_terminal|Session]] Resumption / [[694_thread_local_storage_tls|TLS]] Ticket) 기능 구성
688. [[688_sni_esni_ech_encrypted_client_hello|SNI]] ([[688_sni_esni_ech_encrypted_client_hello|Server Name Indication]]) 개요 와 [[1064_esni_ech_tls_1_3_encrypted_sni|ESNI]] / ECH (Encrypted [[003_audit_stakeholders|Client]] Hello) 검열 우회 
689. [[183_post_quantum_cryptography_key_transition|양자 내성 암호]] ([[351_quantum_computing_pqc_transition|PQC]], [[183_post_quantum_cryptography_key_transition|Post-Quantum Cryptography]]) 체계 및 통신망 교환 표준 (Shor's [[001_algorithm_definition|Algorithm]] 위협 대처)
690. [[690_firewall_generation_evolution|방화벽]] ([[690_firewall_generation_evolution|Firewall]]) 필터링 1,2,3 세대 진화
691. [[691_packet_filter_application_proxy|패킷 필터]] (Packet Filter 라우터/L3,L4), 애플리케이션 상태 필터 및 [[264_proxy_pattern_surrogate_access_control|프록시]]
692. [[692_stateful_inspection_firewall_principle|상태 기반 감시]] ([[992_firewall_stateful_inspection|Stateful Inspection]] / [[160_session_controlling_terminal|세션]] 테이블 체크 메모리) 기술의 원리
693. [[693_nids_network_intrusion_detection_system|NIDS]] (Network [[994_ids_ips_intrusion_detection_prevention_false_positive|Intrusion Detection System]] [[136_variance|분산]] 탐지) 공격
694. [[694_snort_suricata_misuse_anomaly_detection|스노트]] ([[694_snort_suricata_misuse_anomaly_detection|Snort]]), [[240_suricata_multithreaded_nids_ids_ips_engine|Suricata]] ([[430_index_fast_full_scan|병렬]] 룰 지원) 와 오용 탐지(Misuse) vs [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]([[530_anomaly|Anomaly]]) 엔진
695. [[695_ips_network_intrusion_prevention_system|IPS]] (Network Intrusion Prevention System) 차단 아키텍처 (인라인 구조 배치, 폴스 포지티브 문제 대처방안)
696. [[696_waf_web_application_firewall|WAF]] ([[242_waf_web_application_firewall_l7_protection|Web Application Firewall]], 애플리케이션L7 특화)
697. [[147_utm_unmanned_aircraft_system_traffic_management|UTM]] (Unified Threat [[372_management|Management]] 패키징 통합형 장비)
698. [[698_ngfw_next_generation_firewall|NGFW]] (Next-Generation [[690_firewall_generation_evolution|Firewall]], [[216_ngfw_next_generation_firewall_dpi|차세대 방화벽]] 시그니처 융합 모델 딥 패킷 파싱 애플리케이션 ID 제어 적용) 
699. [[699_sandbox_malware_analysis_apt|샌드박스 망분석 시스템]] ([[748_apt|APT]] 이메일 악성 포맷 행위 추적 연동) 
700. [[700_nac_network_access_control|NAC]] ([[226_nac_network_access_control_ieee_802_1x|Network Access Control]] 시스템) 내부 접근 단말기 관리 [[003_integrity|무결성]] 진단

## 14. [[1117_network_security_zero_trust_policy|네트워크 보안]] (공격 및 위협, 대응책) (50개)
701. [[701_sniffing_eavesdropping_promiscuous|도청]] (Sniffing, Eavesdropping) 네트워크 토폴로지 취약 (프론미스큐어스 모드, [[238_switch_operation_principles|스위치]] 잼 체계 해소)
702. [[598_spoofing|스푸핑]] ([[598_spoofing|Spoofing]]) 기만 위장 공격 종류 및 특성 분석
703. [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] [[598_spoofing|스푸핑]] ([[991_arp_spoofing|ARP Spoofing]]) - [[673_mac_message_authentication_code|MAC]] 주소 기만 타겟 [[164_pc|PC]] 트래픽 탈취, 중간자 정적대응 방어 (Static [[312_arp_address_resolution_protocol_ip_to_mac|ARP]])
704. IP [[598_spoofing|스푸핑]] ([[704_ip_spoofing_trust_injection|IP Spoofing]]) - 트러스트 IP 위장 [[480_injection|인젝션]] 우회 및 DDoS 공격 근원
705. [[511_dns_hierarchical_distributed_architecture|DNS]] [[598_spoofing|스푸핑]] / [[265_dns_cache_poisoning|DNS Cache Poisoning]] 매칭 [[352_defect_definition|결함]] [[402_port_number_16bit_application_process_identification|포트 번호]] 난수 제어 취약 노출 방어 기법 ([[518_dnssec_dns_security_extensions|DNSSEC]] 도입 목적)
706. [[706_mitm_man_in_the_middle_hsts|중간자 공격]] (MitM, Man-in-the-Middle) [[701_sniffing_eavesdropping_promiscuous|도청]] 흐름과 통제 조치 ([[694_thread_local_storage_tls|TLS]] 암호 [[395_verification_process_review|검증]] 중요성, [[268_hsts|HSTS]] [[009_config|설정]] 이유)
707. [[707_session_hijacking_tcp_seq_cookie|세션 하이재킹]] ([[271_session_hijacking|Session Hijacking]] / [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] Seq 번호 추정 절도 등 탈취/[[475_cookie_local_state|Cookie]]/토큰 갈취 기법)
708. [[708_replay_attack_timestamp_nonce|재생 공격]] ([[274_replay_attack|Replay Attack]] 방어 타임스탬프 원리 / 비표 넌스 [[519_oidc_nonce|Nonce]] 적용)
709. [[599_dos_ddos_attack|DoS]] (Denial of [[090_service_kubernetes_network_load_balancing|Service]] [[452_availability|가용성]] 타격 위협 목적) 
710. [[136_variance|분산]] [[989_dos_denial_of_service|서비스 거부 공격]] (DDoS, Distributed [[599_dos_ddos_attack|DoS]] 위협) [[990_botnet_cnc|봇넷]] 시스템 C&C 서버 증폭, 감염 및 반사 
711. [[255_syn_flood|SYN Flood]] 공격 ([[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 3way-Handshake 약점 Backlog 큐 포화 자원 마비 유도)
712. [[255_syn_flood|SYN Flood]] 대응 - SYN [[475_cookie_local_state|Cookie]] 기술 (상태비저장 SYN/ACK 암호화 처리 후 최종 ACK서 [[395_verification_process_review|검증]]) 서버 완화 제어
713. [[318_icmp_internet_control_message_protocol_diagnostics|ICMP]] Smurf 공격 (IP 브로드캐스트+[[598_spoofing|스푸핑]]) / 스머핑 라우터 IP Directed Broadcast 차단 설계
714. Ping of Death 대형 패킷 [[291_fragmentation_and_reassembly_process|단편화]] [[591_buffer_overflow|버퍼 오버플로우]] 문제
715. TearDrop 공격 (IP 헤더 오프셋 중복/오류 [[291_fragmentation_and_reassembly_process|단편화]] 무한 재조립 오류 기만 다운)
716. [[256_udp_flood|UDP Flood]] 리소스 고갈 유도 / Null/Christmas Tree [[186_character_stuffing_dle_stx_etx|플래그]] 비대칭공격 타격 
717. [[717_drdos_amplification_reflection_attack|반사 증폭 공격]] (Amplification Attack / DRDoS) 
718. [[536_ntp_network_time_protocol_stratum|NTP]] 증폭 (monlist [[229_monitor|모니터]] 목록 명령 악용/수백배 반사)
719. [[511_dns_hierarchical_distributed_architecture|DNS]] 증폭 (위장 IP로 파싱 [[001_dikw_pyramid|데이터]]/TXT 등 다량 요구 패킷 대형화 수백배 반사 대상자 타격)
720. Memcached 증폭 서버 공격 방어 미흡 ([[720_memcached_amplification_attack|5만배 반사]])
721. SLOW GET / SLOW POST 공격([[258_slowloris|Slowloris]]) 응용 계층 [[125_socket|소켓]] 점유, 헤더/엔티티를 끊임없이 매우 느리게 보내 Connection 지속 자원 무력화 (일시적 [[690_firewall_generation_evolution|방화벽]] 필터링, [[573_timeout_retry_backoff_strategy|타임아웃]] 최소화 대응)  
722. [[722_slowloris_http_get_delay_attack|트래픽 혼잡공격]] ([[883_common_criteria_iso_15408|CC]] Attack [[990_botnet_cnc|봇넷]] [[461_http_stateless_connection_oriented|HTTP]] 임의페이지 무한 요청) 유도 및 캡챠 적용
723. [[730_ransomware|랜섬웨어]] ([[730_ransomware|Ransomware]]) [[501_file_definition_logical_record|파일]]공유 139/445망 자가전파 및 [[752_phishing|피싱]] 방어 [[446_port_and_bus|포트]] 폐쇄 규약 체계 SMBv1 보안 약점 타격 (워너크라이 [[732_wannacry|WannaCry]] 분석) 
724. 다크 웹 (Dark Web) Tor (The Onion Router 은닉망 릴레이 체계 분석)
725. [[725_port_scanning_full_open_vs_stealth_half_open|스키밍]] ([[725_port_scanning_full_open_vs_stealth_half_open|Skimming]]) 공격
726. 무차별 대입 공격 ([[456_brute_force|Brute Force]] / 사전 Dictionary 제어) 통신 [[568_logs_distributed_logging_elk_fluentd|로그]]인/[[538_ssh_vs_telnet_secure_remote|SSH]] 타격
727. SQL [[480_injection|인젝션]] (OWASP 핵심 웹 구조 보안 약점 [[696_waf_web_application_firewall|WAF]] 적용 룰 필터망 파라미터 처리망) 
728. [[500_xss_defense_escaping_csp|크로스 사이트 스크립팅]] ([[726_xss_cross_site_scripting_types|XSS]] - Reflected/Stored, 브라우저 로컬 [[001_dikw_pyramid|데이터]] 탈취 [[475_cookie_local_state|쿠키]] 위협망 통신 [[475_cookie_local_state|쿠키]]보안 [[475_csp|CSP]] [[009_config|설정]] 등 세부망 보안 원리)
729. 크로스 사이트 요청 위조 ([[728_csrf_cross_site_request_forgery_concept|CSRF]] 원리 및 방어 토큰 방식 SameSite [[009_config|설정]])
730. [[748_apt|APT]] ([[374_apt|Advanced Persistent Threat]] 고도화 공격망 - 침투-탐색-수집-유출-유지 킬체인 프로세스) 내부 인트라넷 통제 
731. [[731_buffer_overflow_stack_heap_aslr|버퍼 오버플로우 공격]] ([[090_service_kubernetes_network_load_balancing|서비스]] 다운/원격코드 실행 위협망 타격)
732. [[597_zero_day_exploit|제로 데이]] ([[597_zero_day_exploit|Zero-day]] 방어되지 않은 취약점 노출 즉시 전산자원 위협) 공격 
733. [[600_port_scanning|포트 스캐닝]] 도구 작동 메커니즘 (NMAP 스텔스 스캔 - 반개방형 SYN Scan, FIN Scan 분석망 체계 [[396_validation|확인]]법) 
734. [[734_firewall_bypass_tunneling_fragmentation|방화벽 우회기법]] ([[377_tunneling_mechanism_overview|터널링]] 캡슐화 [[446_port_and_bus|포트]] 우회/[[136_variance|분산]] 패킷 망 회피)
735. 비인가 [[572_ap_access_point_ds_distribution_system|AP]] (Rogue [[572_ap_access_point_ds_distribution_system|AP]] 무선망 트래픽 위조 가로채기 이블트윈 공격 / WIPS 방어 적용망)
736. [[736_port_forwarding_jump_station_bastion_host|포트 포워딩]] ([[446_port_and_bus|Port]] Forwarding 역방향 타격 문제 제어 원격 [[446_port_and_bus|포트]]/점프 스테이션 보안 규정 체계제안)
737. [[737_backdoor_c2_beacon_behavior_analysis|백도어]] ([[727_backdoor|Backdoor]] [[446_port_and_bus|포트]] / [[746_c2|C2]] 서버 [[608_beacon_technology_ibeacon_eddystone|Beacon]] 정주기 통신 이상 징후 망 행위 분석 대응 기계학습 모델 개발 방향) 
738. [[738_zero_trust_architecture_least_privilege|제로 트러스트 보안]] ([[184_zero_trust_architecture|Zero Trust Architecture]], 내부망도 [[395_verification_process_review|검증]], [[010_least_privilege|최소 권한 원칙]] 지속 검토 적용 프레임워크 설계)
739. [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]] ([[049_micro_segmentation|Micro Segmentation]] 시스템망 트래픽 분할 보안통제구조 수평 전파/Lateral Movement 차단 모델) 
740. [[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] (Secure Access [[090_service_kubernetes_network_load_balancing|Service]] Edge 브랜치 사무소 단말 네트워크 엣지 클라우드 보안 통합체계/ [[849_sd_wan_software_defined_wide_area_network|SD-WAN]] + [[742_swg_secure_web_gateway|SWG]]/[[741_casb_cloud_access_security_broker|CASB]] 등 플랫폼 구조 융합 모델 개요)  
741. [[741_casb_cloud_access_security_broker|CASB]] (Cloud Access [[283_security_tactics|Security]] Broker 클라우드 망 접속 보안 [[229_monitor|모니터]]/가시성 유지 시스템)
742. [[742_swg_secure_web_gateway|SWG]] (Secure Web Gateway 시큐어 웹 게이트웨이 / [[264_proxy_pattern_surrogate_access_control|프록시]] 보안 패키지 모델 구조적 설계)
743. [[780_cspm_cloud_security_posture_management|CSPM]] / [[332_cwpp|CWPP]] 보안 [[009_config|설정]] [[229_monitor|모니터]]링 관리 및 워크로드 [[136_variance|분산]]망 보안 맵 체계 가시화 기술 모델화 적용 시스템 
744. 침해 [[009_incident_response|사고 대응]] 체계 분석 (패킷 미러 [[446_port_and_bus|포트]], [[668_network_forensics|네트워크 포렌식]] ([[668_network_forensics|Network Forensics]]), 실시간 [[568_logs_distributed_logging_elk_fluentd|로그]] ([[624_siem|SIEM]] 인프라) 수집 체계 연계 방법)  
745. [[745_soar_security_orchestration_automation_response|SOAR]] ([[283_security_tactics|Security]] [[073_container_orchestration_tools|Orchestration]], Automation and Response) 자동화 [[073_container_orchestration_tools|오케스트레이션]] 적용 망대응 통합 ([[637_playbook|플레이북]] 모델 기술 분석 보안)
746. [[746_ti_threat_intelligence_ioc_stix_taxii|TI]] ([[746_ti_threat_intelligence_ioc_stix_taxii|Threat Intelligence]]) 융합 / STIX, TAXII 표준 지표 관리, IoC (침해지표) 반영 
747. [[747_web_shell_file_upload_vulnerability|웹쉘]] ([[306_web_shell|Web Shell]] [[229_monitor|모니터]], 디렉토리 실행 등 권한 취약 방지 스캔)  
748. [[748_qrng_quantum_random_number_generator|양자 난수 생성기]] (QRNG 적용, 순수 예측불허 난수 보안 [[087_process_state_transition|생성]]장치 모델)
749. [[062_darkdata|다크 데이터]] / [[823_dlp|Data Loss Prevention]] ([[386_dlp|DLP]] 네트워크 기반 메일 메신저 단말 외장 유출 차단 모델 시스템 개념 [[001_dikw_pyramid|데이터]] 기밀 탐지 적용 원리 분석 적용 구조 파편 제어)
750. ISO 27001 네트워크 통제 및 개인정보영향평가 [[303_authentication_authorization_patterns|인증]] 모델망 분리 아키텍처 ([[369_logic_bomb|논리]]/물리) [[183_network_linkage_system|망연계 시스템]] (스트림 분리 체계 연동 기술 [[079_developer_cleanroom_vdi_security|VDI]] 도입 구성망 보안망 체계적 구조 이해 등 설계 방침 기초)

## 15. 차세대 통신망 (4G/[[418_5g_embb_urllc_mmtc_slicing|5G]]/[[419_6g_ntn_thz_ris_next_gen|6G]]) 핵심 아키텍처 (50개)
751. [[751_3gpp_3rd_generation_partnership_project|3GPP]] (3rd Generation Partnership [[042_relational_algebra_project|Project]]) 표준 개발
752. [[752_lte_long_term_evolution_4g|LTE]] (Long Term Evolution 4세대 망 진화) All-IP [[276_packet_switching_vs_circuit_switching_message_switching|패킷 교환]] 완전 전환, [[945_ofdma_orthogonal_frequency_division_multiple_access_resource_block|OFDMA]]
753. [[753_epc_evolved_packet_core_sgw_pgw|EPC]] (Evolved Packet Core 코어망 시스템) S-GW, P-GW 제어 망 트래픽 통합
754. [[754_mme_mobility_management_entity|MME]] ([[561_mobility_management_hlr_vlr_paging|Mobility Management]] Entity 제어 [[001_dikw_pyramid|데이터]] 평면 구조적 통제 [[556_handover_handoff_types_concept|핸드오버]])
755. [[755_hss_home_subscriber_server|HSS]] (Home Subscriber Server 가입자 마스터 정보)
756. 기지국: eNodeB [[136_variance|분산]] [[001_dikw_pyramid|데이터]] 평면 [[339_routing_overview_best_path_selection|라우팅]] 고속망 이동성 통제 진화
757. [[757_ltea_carrier_aggregation|LTE-A]] ([[757_ltea_carrier_aggregation|LTE-Advanced]]) [[1014_carrier_aggregation_lte_advanced_5g|캐리어 어그리게이션]] (Carrier Aggregation [[089_contract_account_smart_contract|CA]] 2~5개 주파수 대역 묶음 전송 캐파 향상 제어 속도 증강 기술 규격 제정 진전 표준 체계 진화)
758. [[758_volte_voice_over_lte_sip_qos|VoLTE]] (Voice over [[752_lte_long_term_evolution_4g|LTE]] 음성 통화 올 IP 패킷망 진화 우선 제어 처리 [[535_system_in_package|SIP]] [[388_qos_quality_of_service_best_effort_intserv_diffserv|QOS]] 제어망 적용 구조 최적화)
759. [[418_5g_embb_urllc_mmtc_slicing|5G]] 통신 [[282_performance_tactics|성능]] 목표 3대 특징 ([[148_5g_embb_urllc_mmtc|초고속]], 초연결, 초저지연) 기능적 체계 진화 특징 비교 
760. [[760_embb_enhanced_mobile_broadband_vr_ar|eMBB]] (Enhanced Mobile Broadband [[148_5g_embb_urllc_mmtc|초고속]] 광대역 대용량 증강 기술 적용) AR/VR 기술 지원 파급 체계 지원
761. [[761_urllc_ultra_reliable_low_latency|uRLLC]] (Ultra-Reliable and Low [[141_latency|Latency]] Communications 초안정/초고신뢰 초저지연망 차량 제어/[[166_smart_factory|스마트 팩토리]] 통신 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 설계 1ms) 
762. [[762_mmtc_massive_machine_type_communications|mMTC]] (Massive Machine-Type Communications 초거대 밀도 초다수 연결 사물 기기 [[101_iot_concept|IoT]] 연결망 배터리 저전력 제어 적용 모델 [[282_performance_tactics|성능]] 지표 적용)
763. [[763_5g_nr_new_radio_scalable_numerology|5G NR]] ([[763_5g_nr_new_radio_scalable_numerology|New Radio]]) 신무선 표준 대역
764. FR1 주파수 (Sub-6GHz 대역, 기존 호환 및 중간 광역/보편 속도 모델 적용 제어) 
765. FR2 주파수 ([[156_mmwave_millimeter_wave|mmWave]] 24Ghz~ [[156_mmwave_millimeter_wave|밀리미터파]] 직진성 극한, 장애물 회절 약화 대형 [[178_small_cell_macro_femto|스몰셀]] 조밀 구성 기술 체계 대역) 
766. [[766_nsa_non_standalone_5g_lte_core|NSA]] (Non-[[150_5g_sa_standalone_architecture|Standalone]] 코어는 [[752_lte_long_term_evolution_4g|LTE]] [[753_epc_evolved_packet_core_sgw_pgw|EPC]] / 기지국 제어 무선 NR 결합 구축 진보 비용 최소 고속도 망 적용 구조 융합 통신 모델)
767. [[767_sa_standalone_5g_core_network|SA]] ([[150_5g_sa_standalone_architecture|Standalone]] 코어까지 [[418_5g_embb_urllc_mmtc_slicing|5G]] Core([[768_5gc_5g_core_network_evolution|5GC]]) 풀 전환 [[531_cloud_native_architecture|클라우드 네이티브]] 슬라이싱 전체 통제 [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]] 해결 구축 모델 최신 릴리즈 채용 방식) 
768. [[768_5gc_5g_core_network_evolution|5GC]] ([[418_5g_embb_urllc_mmtc_slicing|5G]] Core Network 차세대 코어망 [[151_sba_service_based_architecture_5g|SBA]] 아키텍처)
769. [[151_sba_service_based_architecture_5g|SBA]] ([[151_sba_service_based_architecture_5g|Service Based Architecture]] 네트워크 기능 요소가 [[561_container_based_deployment|컨테이너]]/마이크로 [[090_service_kubernetes_network_load_balancing|서비스]] [[974_restful_api_stateless_http_methods_uri|RESTful API]] 간 [[389_mesh_topology|메시]]지 연동 호출 통신 플랫폼 융합 모델 기반 구축 코어 [[090_service_kubernetes_network_load_balancing|서비스]] 규격 표준) 
770. [[770_amf_access_mobility_management_function|AMF]] (Access and [[561_mobility_management_hlr_vlr_paging|Mobility Management]] Function / [[754_mme_mobility_management_entity|MME]] 대체) 
771. [[771_smf_upf_session_management_user_plane|SMF]] ([[771_smf_upf_session_management_user_plane|Session Management Function]]) / UPF (User Plane Function [[001_dikw_pyramid|데이터]] 고속 패킷 엣지 통과 모델 구조 [[015_지연_데이터_관점|지연]] 개선 구조 체계 [[001_dikw_pyramid|데이터]] 평면 전적 담당 [[339_routing_overview_best_path_selection|라우팅]] [[192_module_independence|모듈]] 시스템화 방식 고속 스위칭 처리 최적 관리 기능) 
772. [[772_pcf_policy_control_function_qos|PCF]] ([[164_policy|Policy]] Control Function 사용자 [[164_policy|정책]] 적용 자원 대조 통제 구조 연동 통합 기능 기능망 제어 [[136_variance|분산]] 룰 구조 통제 [[528_provisioning|프로비저닝]] [[002_database_definition|데이터베이스]])  
773. [[149_network_slicing_5g_architecture|네트워크 슬라이싱]] ([[149_network_slicing_5g_architecture|Network Slicing]] 물리적 동일망 복수의 이종 독립 [[369_logic_bomb|논리]]적 인스턴스 전용망 분할 보안, [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 격리([[760_embb_enhanced_mobile_broadband_vr_ar|eMBB]]/[[761_urllc_ultra_reliable_low_latency|URLLC]]/[[762_mmtc_massive_machine_type_communications|mMTC]]) 관리 지원 클라우드 [[041_resource_allocation|자원 할당]] [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] 자원 관리 제어 체계 자동화 [[633_sdn_whitebox|SDN]]/[[865_nfv_network_functions_virtualization_architecture|NFV]] 필수 적용 기술 망)
774. [[265_e2e_end_to_ui_selenium|E2E]] 슬라이싱 보장 모델 관리 (RAN-Transport-Core 종단 통과 자원 보장 체계 통제 연동 규격 파싱 자원 [[369_logic_bomb|논리]] 분배 제어 구성 구조 모델 개념 기술 요약망 적용/배포 방침)  
775. [[627_mec_multi_access_edge_computing_5g|MEC]] 기반 가속 통신망 [[339_routing_overview_best_path_selection|라우팅]] 최적 (User Plane Function UPF 로컬 엣지 트래픽 인터셉트 전환 [[1009_backhaul_network_base_station_core_connection|백홀]] [[015_지연_데이터_관점|지연]] 개선 구조) 로컬 [[015_지연_데이터_관점|지연]] 대책 서버형 응용 처리망 체계 기술 연계)
776. [[099_Massive_MIMO_대규모_다중_안테나|Massive MIMO]] 대거 다중 [[055_array|배열]] [[171_antenna_basic_dipole_resonance|안테나]] 시스템 고주파 전파 빔 관리
777. [[101_beamforming|빔포밍]] 트래킹 기술 체계 (Beam Tracking 개별 단말 핀포인트 추적 지향 전력량 최적화 증폭/간섭억제 타겟 통신 품질 체계 극대화 송수신망 진화 시스템 단말 수신 추정기반) 
778. 3D [[097_MIMO_다중_안테나_기술|MIMO]] 수직/수평 고차원 송수신 구조 공간 활용 극대화 스펙트럼 자원)
779. [[779_bss_coloring_wifi_6_spatial_reuse|BSS Coloring]] (간섭 채널 색상 코드 배정 구분 노이즈 [[130_signal|신호]] 차단 무선 채널 활용 체계 고밀도 효율화 기능망 확장 연대 와이파이 혼선 배제 방식 응용 구조 체제) 
780. [[780_cp_ofdm_cyclic_prefix_5g_waveform|CP-OFDM]] ([[418_5g_embb_urllc_mmtc_slicing|5G]] 표준 [[001_dikw_pyramid|데이터]] 채널 다중 변조 다운 무선통신 파형 방식 적용 분석망 통신망 채택 사양 모델 파형) 
781. [[156_c_ran_cloud_ran|C-RAN]] ([[156_c_ran_cloud_ran|Cloud RAN]] 베이스밴드 Unit 원격 중앙 [[285_pooling_layer|풀링]] 클라우드 관리 [[784_fronthaul_ecpri_split_option|프론트홀]] 망 구조 통제 트래픽 통합 제어 기술 구성 요소망 구축 방법 구조 효율 제어) 
782. [[782_o_ran_open_ran_white_box_interface|O-RAN]] (Open RAN 기지국 장비 인터페이스 화웨이 등 [[051_vendor_lock_in_cloud_computing|벤더 종속]]성 탈피 개방형 오픈 [[014_api_posix|API]] 표준 분할 조합 기술 화이트 박스 [[238_switch_operation_principles|스위치]] 구성 통제망 자립 기지국 연합 관리 기능 체계 연계) 
783. 기지국 DU ([[783_gnodeb_cu_du_ru_split_architecture|Distributed Unit]]) / CU (Centralized Unit) / RU (Radio Unit 전파 [[171_antenna_basic_dipole_resonance|안테나]] 제어망 연결 구조) 고차원 장비 표준화 인터페이스 (스플릿 옵션망 트래픽 부담 체계 [[784_fronthaul_ecpri_split_option|프론트홀]] [[015_지연_데이터_관점|지연]] 파급망 분석 [[136_variance|분산]])  
784. [[784_fronthaul_ecpri_split_option|프론트홀]] ([[1011_fronthaul_network_c_ran_cpri_roef|Fronthaul]] [[171_antenna_basic_dipole_resonance|안테나]]-DU망 광인터페이스 eCPRI 규격 모델 구조 구성 패킷망 확장망) 
785. [[1010_midhaul_network_c_ran_fronthaul_du_cu|미드홀]]/[[1009_backhaul_network_base_station_core_connection|백홀]] 전송계층망 코어 장거리 파장 라우터 [[238_switch_operation_principles|스위치]] 연합망 구성체계 요약 진화) 
786. [[419_6g_ntn_thz_ris_next_gen|6G]] 비전 네트워크 커버리지 입체망 스펙트럼 주파수 광대역 (테라헤르쯔 [[157_terahertz_thz_6g|THz]] 위성 연계망 무지연 대역 확장 구성 기술 예상 지표 모델 기준 규제 표준안 도입 적용 한계 이슈) 
787. [[153_ris_reconfigurable_intelligent_surface|지능형 반사 표면]] (RIS 기능 구조 메타 파트너 물질 적용 주파수 흡수/조절 우회 반사/투과 경로 조작 커버리지 음영 극복 저전력 반사/전파제어 혁신 시스템 모델 [[101_beamforming|빔포밍]] 한계 돌파형 구성망 보조 [[171_antenna_basic_dipole_resonance|안테나]] 환경 연계 연구 동향)
788. [[788_ntn_non_terrestrial_network_leo_satellite|비지상 네트워크망]] ([[154_ntn_non_terrestrial_network_6g|NTN Non-Terrestrial Network]]. 스타링크 연계 도심 항공 모빌리티 [[145_uam_urban_air_mobility_evtol|UAM]] 커버 위성 3D 연계 [[339_routing_overview_best_path_selection|라우팅]] 끊김 보완/위성 [[171_antenna_basic_dipole_resonance|안테나]] 최적화망 구성 기술 발전/해상 통합 통신 지원 기반 연구 궤도 [[015_지연_데이터_관점|지연]] 최적 방침 구조적 구성) 
789. [[126_digital_twin_concept|디지털 트윈]] 네트워크 망 ([[190_ai_llm_requirements_specification|AI]] 동기 시뮬레이션 고장 예측 자가 치유 망 [[231_ai_turing_test|인공지능]] 접목 선행 관측 모형 모델 도입 구성 개념 도입) 
790. 네트워크 프로그래밍 모델 [[874_p4_programming_data_plane_pipeline_int_telemetry|P4]] 지원 고정 하드웨어 규격 [[070_asic|ASIC]] 탈피 자율망 [[339_routing_overview_best_path_selection|라우팅]] 룰 적용 최적 커스텀 프로세싱 (초저지연 [[339_routing_overview_best_path_selection|라우팅]] 룰 [[009_config|설정]] 엔진 고도화 기술 적용 연계 모델 개요)  
791. [[791_autonomous_network_aiops_ibn_zero_touch|자율 주행 넷망]] ([[099_aiops_chatbot_itsm_automation|AIOps]], [[190_ai_llm_requirements_specification|AI]] for Network 통제망 유지보수 자동화 의도 반영 [[164_policy|정책]] [[857_ibn_intent_based_networking_declarative_automation|IBN]] 설계 융합 [[419_6g_ntn_thz_ris_next_gen|6G]] 통합 자력 제어 제로 터치 네트워크 구현 모델)
792. [[190_ai_llm_requirements_specification|AI]] 내재화 ([[792_ai_native_6g_neural_network_radio|AI-Native]]) [[419_6g_ntn_thz_ris_next_gen|6G]] 통신 [[130_signal|신호]] 변복조 채널 추정 물리망 대체 신경망 라디오 적용 모형 진화 기술 통신 딥러닝 [[039_decoder|디코더]] 채택 모델 [[282_performance_tactics|성능]]/오버헤드 한계 극복 대안 통신 기술 
793. 양자 인터넷 [[192_module_independence|모듈]] 기반 네트워크 키 분배 안정성 [[922_qkd_quantum_key_distribution_bb84_eavesdropping|QKD]] 적용 ([[220_quantum_entanglement|양자 얽힘]]/[[016_replication_factor|복제]] 불가능 원리 광파장 탑재 보안 구간 해킹 원천 차단 무선 통신 기기망 연동 체계 구조 방식 인텔 암호 보장 릴레이망 구축)  
794. 프라이빗 5G망 (특화망 e-UM [[418_5g_embb_urllc_mmtc_slicing|5G]] 개념 적용 산업 공장 자체 구축망 라이센스 주파수 사설 구성망 비용 구조 보안 [[015_지연_데이터_관점|지연]] 한계 탈피망 맞춤형 [[331_neuromorphic_ai_db|슬라이스]] 대안 구조 모델 요약 정리)
795. [[418_5g_embb_urllc_mmtc_slicing|5G]] LAN [[238_switch_operation_principles|스위치]] 대체 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 투명 연계형 산업망 구축용 모델 브릿지 구성 기술 (L2 무결 연동 통신망 호환 제어망 융합 구성 요지 모델망 구성망 [[528_provisioning|프로비저닝]] 구조 체계 정리) 
796. 홀로그램 무선 전송 [[347_compaction|압축]]/다시점 비디오 체계 동기망 지터 제어 기술(VTC [[015_지연_데이터_관점|지연]] 민감 체계) 통신망 요구 지표 한계 모델 구조 모델 도입 요망 기술 요소)
797. 텔레햅틱 체계 기술 네트워크 [[138_response_time|응답 시간]]/제어 피드백 (Tactile Internet 극한 응답 한계 분석 및 신뢰 통신 5ms 이내 물리 제어 [[001_dikw_pyramid|데이터]] 패킷 순서 보장 모델 통신 기반 연계 인프라 방식 구성 기초 체재) 
798. 메이커 빔 [[087_process_state_transition|생성]] [[171_antenna_basic_dipole_resonance|안테나]] 메타 표면 적용 무전원 [[101_iot_concept|IoT]] 환경 센서 연계 통신 시스템 구조 파악 설계 통신 방향 제안 
799. 동적 스펙트럼 공유 기술 (DSS 진화 4G/[[418_5g_embb_urllc_mmtc_slicing|5G]] 주파수 시간 단위 혼용 운영 자원 배분 유연성 통신 기술 방식 도입 전파 배급 한계 돌파 통계망 모델)  
800. 주파수 집성 기술 고급 모델 연대 전방위 고밀도 셀 간 간섭 회피 [[1013_comp_coordinated_multipoint_transmission|CoMP]](상호협력 통신 체계 전파 최적화 망) 

## 16. [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 및 클라우드 네트워킹 (50개)
801. [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] ([[801_data_center_3_tier_architecture_core_aggregation_access|Data Center]]) 3-Tier 아키텍처 - Core, Aggregation, Access 계층 
802. [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] Spine-Leaf 아키텍처 - 2-Tier 수평 [[136_variance|분산]] 구조 (East-West 트래픽 최적화)
803. [[803_oversubscription_ratio_data_center_bandwidth|오버서브스크립션 비율]] ([[803_oversubscription_ratio_data_center_bandwidth|Oversubscription Ratio]]) 설계 개념 [[136_variance|분산]]망 대역
804. [[804_ecmp_equal_cost_multi_path_routing_load_balancing|ECMP]] ([[804_ecmp_equal_cost_multi_path_routing_load_balancing|Equal-Cost Multi-Path]]) 스파인-리프 [[430_index_fast_full_scan|병렬]] [[339_routing_overview_best_path_selection|라우팅]] 경로 활성화 
805. Clos 네트워크 - 다단 논블로킹(Non-[[122_sync_async_communication|blocking]]) 스위칭 구조
806. North-South 트래픽 ([[806_north_south_traffic_data_center_gateway|외부 사용자-데이터센터간 흐름]])
807. East-West 트래픽 ([[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 내부 서버-서버/[[532_microservices_decomposition_patterns|마이크로서비스]] 간 가상 통신 흐름)
808. [[808_network_jitter_delay_variation_storage_sync|네트워크 지터]] (Jitter, [[015_지연_데이터_관점|지연]] 변이) [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 스토리지 망 동기 치명적 영향 대안
809. [[697_fcoe|FCoE]] ([[696_fibre_channel_protocol|Fibre Channel]] over [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]]) - SAN과 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 랜망 통합 물리선 단일화 (스토리지 네트워킹)
810. [[698_iscsi|iSCSI]] (Internet Small Computer System Interface) - IP망 기반 스토리지 블록 전송 통신망 표준
811. [[361_infiniband|인피니밴드]] ([[361_infiniband|InfiniBand]]) - [[639_rdma_kernel_bypass|RDMA]] 기반 [[148_5g_embb_urllc_mmtc|초고속]], 초저지연 컴퓨터 클러스터 인터커넥트망 ([[548_automotive_hpc|HPC]], [[190_ai_llm_requirements_specification|AI]] 클러스터 망)
812. [[639_rdma_kernel_bypass|RDMA]] (Remote [[318_dma|Direct Memory Access]]) - CPU 개입/OS [[022_kernel_role|커널]] [[057_stack|스택]] 복사 없이 메모리간 직접 [[001_dikw_pyramid|데이터]] 전송망 기법
813. [[523_roce|RoCE]] ([[639_rdma_kernel_bypass|RDMA]] over Converged [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]]) - [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 환경에서 [[639_rdma_kernel_bypass|RDMA]] 구현 
814. [[814_iwarp_tcp_ip_based_rdma_compatibility|iWARP]] - [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP 기반의 [[639_rdma_kernel_bypass|RDMA]] 구현 망 [[344_compatibility_usability|호환성]] 중시 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 단
815. [[815_overlay_network_virtualization_l2_extension|오버레이 네트워크]] ([[815_overlay_network_virtualization_l2_extension|Overlay Network]]) [[369_logic_bomb|논리]] [[238_switch_operation_principles|스위치]] L2 확장 터널 구조 [[377_tunneling_mechanism_overview|터널링]]
816. [[816_underlay_network_physical_infrastructure_routing|언더레이 네트워크]] ([[816_underlay_network_physical_infrastructure_routing|Underlay Network]]) 오버레이 터널을 품는 물리 망 패킷 포워딩 베이스
817. [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] ([[817_vxlan_virtual_extensible_lan_mac_in_udp|Virtual eXtensible LAN]]) - [[406_udp_user_datagram_protocol_connectionless_fast|UDP]]([[446_port_and_bus|포트]] 4789)로 L2 프레임 캡슐화, [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 4096개 한계 완화 (1,600만개 VNI 지원) 
818. [[818_nvgre_network_virtualization_using_generic_routing_encapsulation|NVGRE]] (Network [[190_virtualization_computing_architecture_cloud|Virtualization]] using [[378_gre_generic_routing_encapsulation|Generic Routing Encapsulation]]) MS 주도 캡슐화 통신 체계
819. [[819_stt_stateless_transport_tunneling_offload|STT]] ([[819_stt_stateless_transport_tunneling_offload|Stateless Transport Tunneling]]) [[015_virtualization|가상화]] 망 패킷 오프로드 LSO 지원 목적 망
820. [[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]] ([[820_evpn_ethernet_vpn_bgp_control_plane|Ethernet VPN]]) - [[365_bgp_border_gateway_protocol_path_vector|BGP]] 제어 평면 기반 L2/L3 오버레이 경로, [[673_mac_message_authentication_code|MAC]]/IP 동적 학습 및 [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] 브로드캐스트 [[656_ir_containment|억제]] 기술 체계 ([[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 결합)
821. [[821_cloud_native_networking_scale_out_msa|클라우드 네이티브 네트워킹]] ([[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]] Networking 개념) 스케일아웃 [[136_variance|분산]] 연동
822. [[822_cni_container_network_interface_kubernetes|컨테이너 네트워킹 인터페이스]] ([[822_cni_container_network_interface_kubernetes|CNI]], [[100_cni_container_network_interface_flannel_calico|Container Network Interface]]) [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 망 포드간 생태계 표준
823. [[823_flannel_overlay_cni_vxlan|Flannel]] - 오버레이 단순 구현체 [[822_cni_container_network_interface_kubernetes|CNI]] 플러그인
824. [[824_calico_bgp_routing_cni_network_policy|Calico]] - [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[339_routing_overview_best_path_selection|라우팅]] 기반 고성능/보안 L3 [[822_cni_container_network_interface_kubernetes|CNI]] 네트워크 구현 플러그인
825. [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] - [[615_ebpf|eBPF]](지정 [[022_kernel_role|커널]] 동작 제어) 기반 고성능 클라우드 네트워크 연결, 로드밸런싱, 보안 [[395_verification_process_review|검증]] 네트워크 프레임워크 
826. Kube-[[264_proxy_pattern_surrogate_access_control|Proxy]] [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[090_service_kubernetes_network_load_balancing|서비스]] 트래픽 부하 [[136_variance|분산]] 룰 [[087_process_state_transition|생성]] (iptables/IPVS 모드) 구조
827. [[094_ingress_kubernetes_l7_routing_gateway|Ingress]] / [[189_egress|Egress]] 트래픽 (클러스터 내부 망 인입/통과 유출 [[339_routing_overview_best_path_selection|라우팅]] 룰 엔진 제어망 [[009_config|설정]])
828. [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]) - [[532_microservices_decomposition_patterns|마이크로서비스]] 간의 통신/보안/[[229_monitor|모니터]]링을 인프라 계층으로 [[198_abstraction_control_data_process|추상화]]
829. [[302_service_mesh_istio|Istio]] ([[829_istio_envoy_service_mesh_control_plane|이스티오]]) - Envoy [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]] 기반 [[302_service_mesh_istio|서비스 메시]] 표준 컨트롤 플레인 엔진 
830. [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] ([[830_sidecar_proxy_architecture_envoy_decoupling|Sidecar Proxy]]) 아키텍처 - 애플리케이션 코드 변경 없이 트래픽 제어 대행 캡슐화 모델
831. [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] ([[187_mtls_mutual_tls_authentication|Mutual TLS]], 상호 [[303_authentication_authorization_patterns|인증]] [[694_thread_local_storage_tls|TLS]]) [[532_microservices_decomposition_patterns|마이크로서비스]] 간 신뢰 통신 양방향 자격 구조 증명 체계 보장망 [[009_config|설정]]
832. [[167_traffic_shadowing_sre_testing|트래픽 섀도잉]] ([[167_traffic_shadowing_sre_testing|Traffic Shadowing]]) 및 [[115_canary_deployment_gradual_rollout|카나리 배포]] 네트워킹 [[339_routing_overview_best_path_selection|라우팅]] [[268_strategy_pattern|전략]] (가치 테스트망) 분배 제어
833. [[833_load_balancing_l4_l7_switch_traffic_distribution|로드 밸런싱]] ([[196_hard_soft_real_time|Load Balancing]] L4/L7 방식 트래픽 폭주 대안 [[238_switch_operation_principles|스위치]] [[136_variance|분산]]망 적용 구조) 
834. [[178_round_robin_scheduling|라운드 로빈]] ([[834_load_balancing_algorithm_round_robin_least_connection|RR]], Round Robin, Least Connection 연결 추정 부하 맵 할당) 
835. [[835_dsr_direct_server_return_load_balancing_asymmetric|DSR]] ([[835_dsr_direct_server_return_load_balancing_asymmetric|Direct Server Return]]) - 로드밸런서 부하 경감 위해 응답 패킷은 서버가 클라이언트로 직배송 비대칭 트래픽망
836. [[836_vpc_virtual_private_cloud_subnet_isolation|VPC]] ([[028_vpc|Virtual Private Cloud]]) - [[007_public_cloud|퍼블릭 클라우드]] 내 격리된 가상 사설 통신망 구조체계
837. 클라우드 서브넷 [[339_routing_overview_best_path_selection|라우팅]], 인터넷 게이트웨이, [[307_nat_network_address_translation_router_principles|NAT]] 게이트웨이 개념 분리 대역 구조망 설계
838. [[838_direct_connect_expressroute_cloud_leased_line|Direct Connect]] / ExpressRoute - [[266_leased_line_basics_e1_t1_t3|전용선]] 클라우드 직접 연계망 [[339_routing_overview_best_path_selection|라우팅]] 고가용성 하이브리드 연결
839. 퍼블릭/프라이빗/하이브리드/멀티 클라우드간 백본망 인터커넥트 연결 구성 [[339_routing_overview_best_path_selection|라우팅]] [[164_policy|정책]]
840. BDI ([[241_bdi_bridge_domain_interface_vxlan_overlay|Bridge Domain Interface]]) / VTEP ([[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] Tunnel End Point 터널 장치 구조 [[369_logic_bomb|논리]] 분배 [[446_port_and_bus|포트]] [[238_switch_operation_principles|스위치]] [[192_module_independence|모듈]] 기능 체계 분석)
841. BUM 트래픽 (Broadcast, Unknown Unicast, Multicast 스파인리프망 홍수 해소 분배 [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] 패킷 체계 관리 방식 설계)
842. 마이크로 터스트 존 [[690_firewall_generation_evolution|방화벽]] 보안 적용 체계 클라우드 구성 기술 템플릿 배포망
843. [[843_hadoop_rack_awareness_data_replication_topology|하둡]]([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]) 랙 인식 ([[017_rack_awareness|Rack Awareness]]) 토폴로지 통신 [[001_dikw_pyramid|데이터]] [[016_replication_factor|복제]] 연계 [[268_strategy_pattern|전략]]
844. 가상머신 ([[598_vm_migration_nic|VM]]) [[054_hypervisor|하이퍼바이저]] [[630_vswitch_vnf_overhead|가상 스위치]] ([[630_vswitch_vnf_overhead|vSwitch]]) 구조 병목 한계 패킷 경로 탐색 기술 방식
845. [[845_lossless_ethernet_dcb_pfc_roce_fcoe|무손실 이더넷]] ([[845_lossless_ethernet_dcb_pfc_roce_fcoe|Lossless Ethernet]], 스토리지/[[190_ai_llm_requirements_specification|AI]] 망 PFC 적용 [[140_bandwidth|대역폭]] [[015_지연_데이터_관점|지연]] 관리 망 구성)
846. [[671_dpdk|DPDK]] ([[001_dikw_pyramid|Data]] Plane Development Kit) [[022_kernel_role|커널]] 우회 사용자 공간 고속 패킷 처리 구조 모델 [[016_interrupt_mechanism|인터럽트]] 프리 [[448_polling_programmed_io|폴링]]
847. [[497_sr_iov_pcie_mapping|SR-IOV]] (Single Root I/O [[190_virtualization_computing_architecture_cloud|Virtualization]] 인터페이스망 가상머신 다이렉트 패스스루 통과 구성 [[356_pcie|PCIe]] 하드웨어 망) 
848. 스마트NIC (SmartNIC) / [[436_dpu|DPU]] ([[229_dpu_ipu_infrastructure_accelerator_offloading|Data Processing Unit]] 인프라 가속망 컨트롤러 CPU 연산 [[440_offloading|오프로딩]] 구조 카드 모델 분석 체계)
849. [[849_sd_wan_software_defined_wide_area_network|SD-WAN]] 가속 오버레이 토폴로지 암호망/다중경로 최적 클라우드 연결 지능 [[339_routing_overview_best_path_selection|라우팅]] 통합 게이트웨이 기술 (차세대 지점망 인프라)

## 17. [[850_sdn_software_defined_networking_concept|소프트웨어 정의 네트워킹]]([[633_sdn_whitebox|SDN]]) 및 네트워크 [[015_virtualization|가상화]]([[865_nfv_network_functions_virtualization_architecture|NFV]]) (40개)
850. [[633_sdn_whitebox|SDN]] ([[215_sdn_software_defined_networking_openflow|Software Defined Networking]] 소프트웨어 정의 네트워크 구조 패러다임 특징 제어/[[001_dikw_pyramid|데이터]] 영역 근본 분리)
851. [[633_sdn_whitebox|SDN]] [[001_dikw_pyramid|데이터]] 평면 ([[001_dikw_pyramid|Data]] Plane = 포워딩 평면 단순 [[123_pipe|파이프]] 라인 패킷 [[238_switch_operation_principles|스위치]] 수행 역할/[[070_asic|ASIC]] 라우터 이관)
852. [[633_sdn_whitebox|SDN]] 제어 평면 (Control Plane 관리망 [[164_policy|정책]] 룰 [[339_routing_overview_best_path_selection|라우팅]] 시야 중앙 [[369_logic_bomb|논리]] 통제 아키텍처) 두뇌 격 구조 
853. [[853_southbound_interface_api_controller_switch|사우스바운드 인터페이스]] (Southbound [[014_api_posix|API]]) - 컨트롤러와 [[001_dikw_pyramid|데이터]] [[238_switch_operation_principles|스위치]] 간 명령 규약 
854. [[854_northbound_interface_api_controller_application|노스바운드 인터페이스]] (Northbound [[014_api_posix|API]]) - 컨트롤러와 응용(보안, [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]]) 애플리케이션 간 통신/[[014_api_posix|API]] 연동 규약 
855. [[855_openflow_standard_protocol_sdn_southbound|OpenFlow]] ([[855_openflow_standard_protocol_sdn_southbound|오픈 플로우 표준]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 사우스바운드 근간) [[633_sdn_whitebox|SDN]] 1세대 표준 규격 
856. [[855_openflow_standard_protocol_sdn_southbound|OpenFlow]] Flow Table (매치 필드, 액션, 통계 수집기 엔트리 파싱 테이블 패치 구조 규정) 
857. [[199_intent_based_networking_ibn_ai_traffic_routing|인텐트 기반 네트워킹]] ([[857_ibn_intent_based_networking_declarative_automation|IBN]], Intent-Based Networking 의도 서술형 [[164_policy|정책]] 번역 [[231_ai_turing_test|인공지능]] 기반 컨트롤러 자동 변환 [[009_config|설정]]망 [[395_verification_process_review|검증]] 모델 구성)
858. [[631_sddc|SDDC]] (Software Defined [[801_data_center_3_tier_architecture_core_aggregation_access|Data Center]] 클라우드 인프라 자산망 컴퓨트/스토리지/네트워크 전체 추상 [[285_pooling_layer|풀링]] 동적 관리 플랫폼 결합)
859. [[859_whitebox_switch_open_hardware_nos|화이트박스 스위치]] (Whitebox [[238_switch_operation_principles|Switch]] 범용 x86 하드웨어 + 개방형 네트워크 OS [[032_firmware|펌웨어]] 탑재 제어 모델 NOS 이식 [[051_vendor_lock_in_cloud_computing|벤더 종속]] 한계 극복 적용 체계) 
860. [[860_ovs_open_vswitch_sdn_openflow|OVS]] ([[860_ovs_open_vswitch_sdn_openflow|Open vSwitch]] 가상 스위칭 리눅스 [[022_kernel_role|커널]] 기반 [[191_oss_license_compliance|오픈소스]]망 [[598_vm_migration_nic|VM]]/[[561_container_based_deployment|컨테이너]] [[446_port_and_bus|포트]] 트래픽 [[855_openflow_standard_protocol_sdn_southbound|OpenFlow]] 제어 통과 인터페이스 모델 활용) 
861. [[861_mininet_sdn_topology_network_emulator|미니넷]] ([[861_mininet_sdn_topology_network_emulator|Mininet]]) [[633_sdn_whitebox|SDN]] 토폴로지 에뮬레이터 연구 평가망 시뮬레이션 환경 (버추얼 환경 제어 체계 분석망 [[087_process_state_transition|생성]] 구조)
862. ONOS / OpenDaylight ([[191_oss_license_compliance|오픈소스]] [[633_sdn_whitebox|SDN]] 컨트롤러 생태계 아키텍처 대형망 [[090_service_kubernetes_network_load_balancing|서비스]] 제공자 구조 [[136_variance|분산]] 설계 특징 비교 분석 코어 모델) 
863. [[633_sdn_whitebox|SDN]] 컨트롤러 [[190_split_brain_zookeeper_fencing_quorum|스플릿 브레인]] 방어 및 [[136_variance|분산]] 클러스터 고가용성 제어기 (컨트롤 평면 [[456_dual_redundancy|이중화]] 트래픽 분할 모델 [[164_policy|정책]]망 [[571_protection_vs_security|보호]] 구상 체계 대응 방침)
864. [[864_network_slice_orchestrator_sdn_nfv_management|네트워크 슬라이스 오케스트레이터]] 중앙 [[369_logic_bomb|논리]] 관리 제어기 배포 연동 [[633_sdn_whitebox|SDN]] 접목 아젠다
865. [[865_nfv_network_functions_virtualization_architecture|NFV]] (Network Functions [[190_virtualization_computing_architecture_cloud|Virtualization]] [[865_nfv_network_functions_virtualization_architecture|네트워크 기능 가상화]] 통신사(ETSI) 주도 아키텍처 전환 장비 소프트웨어 이식 기술 구조 망)
866. [[866_vnf_virtual_network_function_software_appliance|VNF]] (Virtual Network Function 라우터, [[690_firewall_generation_evolution|방화벽]], [[753_epc_evolved_packet_core_sgw_pgw|EPC]] 등 범용 서버 가상 [[369_logic_bomb|논리]] 인스턴스/어플리케이션 동작 구성 소프트웨어 패치 모델)
867. [[867_nfvi_nfv_infrastructure_physical_virtual_resources|NFVI]] ([[865_nfv_network_functions_virtualization_architecture|NFV]] 인프라 컴퓨팅, 스토리지, 네트워킹 구성 물리+가상 자원 연동 자산 모델 개념적 하드 환경 제어) 
868. MANO ([[372_management|Management]] and [[073_container_orchestration_tools|Orchestration]] [[073_container_orchestration_tools|오케스트레이션]] 자동 관리 프레임워크 3단계 분할 요소 통제 망) 
869. [[869_nfvo_nfv_orchestrator_network_service_lifecycle|NFVO]] ([[865_nfv_network_functions_virtualization_architecture|NFV]] Orchestrator 종단간 네트워크 [[090_service_kubernetes_network_load_balancing|서비스]] 라이프사이클 [[866_vnf_virtual_network_function_software_appliance|VNF]] 체인 리소스 총괄 할당 통제기 설계 지휘망 기능) 
870. [[870_vnfm_vnf_manager_lifecycle_scaling_healing|VNFM]] ([[866_vnf_virtual_network_function_software_appliance|VNF]] Manager 개별 [[866_vnf_virtual_network_function_software_appliance|VNF]] 인스턴스 [[528_provisioning|프로비저닝]], [[621_scale_up_system_bus|스케일 업]]다운/에러 [[016_replication_factor|복제]] 상태 관리 체제 역할망 인프라 적용 구조)  
871. [[871_vim_virtualised_infrastructure_manager_openstack_k8s|VIM]] (Virtualised Infrastructure Manager - OpenStack/K8S 등 자원 파편화 할당 [[598_vm_migration_nic|VM]] 배포 생명 주기 통지 자산 플랫폼 하드 할당 기능망 통제)
872. [[872_service_chaining_sfc_vnf_traffic_steering|서비스 체이닝]] ([[090_service_kubernetes_network_load_balancing|Service]] [[103_chaining|Chaining]] / [[872_service_chaining_sfc_vnf_traffic_steering|SFC]] - [[090_service_kubernetes_network_load_balancing|Service]] Function [[103_chaining|Chaining]] 트래픽 패킷 순차적 [[690_firewall_generation_evolution|방화벽]]->[[695_ips_network_intrusion_prevention_system|IPS]]->LB 식 가상 함수 통과 [[339_routing_overview_best_path_selection|라우팅]] [[873_nsh_network_service_header_sfc_metadata|NSH]] 활용망 체계화)
873. [[873_nsh_network_service_header_sfc_metadata|NSH]] (Network [[090_service_kubernetes_network_load_balancing|Service]] Header 패킷 경로 체인 [[012_metadata|메타데이터]] 포워딩 명세 인캡슐레이션 지원 터널 지원 규약 [[009_config|설정]]) 
874. [[874_p4_programming_data_plane_pipeline_int_telemetry|P4]] (Programming [[295_protocol_field_tcp_udp_icmp|Protocol]]-independent Packet Processors - [[001_dikw_pyramid|데이터]] 평면 패킷 처리 순서 [[123_pipe|파이프]]라인 개발자 직접 언어 코딩 정의, 차세대 확장 [[633_sdn_whitebox|SDN]] 구동 개념) 
875. NETCONF (Network Configuration [[295_protocol_field_tcp_udp_icmp|Protocol]] - [[538_ssh_vs_telnet_secure_remote|SSH]]+XML 자원망 환경 [[009_config|설정]] 통계 관리 [[528_snmp_simple_network_management_protocol|SNMP]] 한계 극복 원격 [[009_config|설정]] 커밋/[[098_rollback_strategy_pipeline_error_threshold|롤백]] 표준 지원망 [[191_transaction_concept_states|트랜잭션]] 관리망) 
876. YANG (Yet Another Next Generation - NETCONF가 조작하는 장비/[[192_module_independence|모듈]] [[001_dikw_pyramid|데이터]] 모델링 [[005_schema|스키마]] 구조 언어 서식망 ([[009_config|설정]] 구상 타입 서식)) 
877. RESTCONF ([[461_http_stateless_connection_oriented|HTTP]] 기반 [[343_json|JSON]]/XML 형식 NETCONF/YANG 매핑/간소화 [[014_api_posix|API]] 통신망 [[009_config|설정]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 체계 모델) 
878. [[878_openconfig_vendor_neutral_yang_model|오픈컨피그]] ([[878_openconfig_vendor_neutral_yang_model|OpenConfig]] 구글 주도, 벤더 중립적 공통 YANG [[001_dikw_pyramid|데이터]] 모델망 장비 범용 [[009_config|설정]]/조작 [[005_schema|스키마]] 규격 표준화 진영 구성 통신망 생태 구조) 
879. 텔레메트리 ([[1058_streaming_telemetry_network_monitoring|Streaming Telemetry]] 장비 [[448_polling_programmed_io|폴링]]이 아닌 자발적 푸시/스트리밍 방식 [[479_grpc_protobuf_http2|gRPC]] 등 초정밀 마이크로단위 빅데이터 [[282_performance_tactics|성능]] 정보 중앙 컬렉터 전송망 [[229_monitor|모니터]] 지표 수집 기술 체계 패러다임)   
880. 오버레이 SDN과 언더레이 [[633_sdn_whitebox|SDN]] (분할 관리 구조 제어 평면 이중성 통합망 구조 관리 [[107_gap_analysis_task_identification|차이 분석]] 개념 차)
881. [[881_micro_segmentation_firewall_sdn_policy_automation|마이크로세그멘테이션 방화벽]] [[633_sdn_whitebox|SDN]] 접목 내부 [[369_logic_bomb|논리]] [[164_policy|정책]] 룰 중앙 연동 배포 
882. 화이트박스 [[746_ocp|OCP]] ([[640_open_compute_project|Open Compute Project]] 페이스북 발 하드웨어/[[238_switch_operation_principles|스위치]] 규격 네트워크 개방 장비 기조망 플랫폼) 
883. [[883_sonic_software_for_open_networking_in_the_cloud|SONiC]] (Software for Open Networking in the Cloud MS 주도 [[561_container_based_deployment|컨테이너]] 기반 개방형 네트워크 OS 레이어망 구성 [[365_bgp_border_gateway_protocol_path_vector|BGP]] 등 통신망 앱 탑재 시스템 연동 구조망)
884. [[884_onie_open_network_install_environment_bootloader|ONIE]] (Open Network Install [[066_gitlab_flow_environment_branch_strategy|Environment]] - 맨 하단 [[029_bootloader|부트로더]]/[[001_operating_system_purpose|운영체제]] [[032_firmware|펌웨어]] 다운 설치 오픈망 부트 규약 모델 체계) 
885. [[365_bgp_border_gateway_protocol_path_vector|BGP]]-[[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]] [[339_routing_overview_best_path_selection|라우팅]] 컨트롤러 스파인/리프 패킷 연합망 오버레이 기술 표준화 연계 [[633_sdn_whitebox|SDN]] 설계
886. [[886_vcpe_virtual_customer_premises_equipment_edge_vnf|엣지 가상화]] ([[886_vcpe_virtual_customer_premises_equipment_edge_vnf|vCPE]] 가입자 댁내 게이트웨인 통제 기능을 사업자/통신사 엣지 서버 [[866_vnf_virtual_network_function_software_appliance|VNF]] [[015_virtualization|가상화]] 이관 비용 최소망 트래픽) 
887. [[887_sd_lan_software_defined_local_area_network_campus|SD-LAN]] (캠퍼스/사무실 유무선 접속 [[238_switch_operation_principles|스위치]] 중앙 통제형 와이파이 관리 융합 네트워크 자동 배포 [[633_sdn_whitebox|SDN]] 진화 모델)
888. [[888_multi_tenant_cloud_resource_isolation_noisy_neighbor|멀티 테넌트]] ([[888_multi_tenant_cloud_resource_isolation_noisy_neighbor|Multi-Tenant]] 자원 격리 보안 독립망 인프라 슬라이싱 할당 [[633_sdn_whitebox|SDN]] [[937_environmental_control|환경 통제]]) 
889. [[889_network_function_offloading_dpu_p4_compile|네트워크 펑션 오프로딩]] 다이렉트 처리 [[436_dpu|DPU]] 연동망 [[874_p4_programming_data_plane_pipeline_int_telemetry|P4]] 기능 컴파일 구조 결합 [[015_지연_데이터_관점|지연]] 파급 최소 하드 이양 기술

## 18. 광/차세대 통신 및 자동화 운영 (50개)
890. [[890_optical_ethernet_carrier_ethernet_single_platform|광통신 네트워크 이더넷]](Optical [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]] 단일 플랫폼망 고속 전이 통계 모델 구성)
891. 장거리 백본 [[891_submarine_cable_architecture_edfa_amplifier_topology|해저 광케이블 아키텍처]] 및 증폭기 중계기 토폴로지 구조 연계
892. [[892_ason_automatically_switched_optical_network_gmpls|ASON]] (Automatically Switched Optical Network - 광망 자원 제어 평면 동적 [[009_config|설정]] [[136_variance|분산]] 연결 제어 ITU 표준 도입 아키텍처 모델 시스템 [[339_routing_overview_best_path_selection|라우팅]]망 최적 동적 구성)
893. [[893_otn_optical_transport_network_g709_fec_container|OTN]] (Optical Transport Network 광 [[001_dikw_pyramid|데이터]] 포장 [[561_container_based_deployment|컨테이너]] G.709 표준 [[184_framing_mechanism|프레이밍]] 망 장애 무결 캡슐 규격 [[212_synchronization_mechanisms|동기화]] 방식 체재)
894. OAM (Operations, Administration, and Maintenance 망 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] [[352_defect_definition|결함]] 링크 [[396_validation|확인]] 루프 감지 [[448_polling_programmed_io|폴링]] 오류 관리 통지 프레임 제어 모델망 구조 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 분석 기술)
895. [[895_sdh_synchronous_digital_hierarchy_stm1|SDH]] ([[010_동기식_비동기식_전송|Synchronous]] Digital Hierarchy 동기식 디지털 통신 위계망 STM-1, 백본 멀티플렉스 고전 프레임 구조) 
896. [[896_sonet_synchronous_optical_networking_oc_ring|SONET]] ([[010_동기식_비동기식_전송|Synchronous]] Optical Networking 북미 [[896_sonet_synchronous_optical_networking_oc_ring|동기식 광통신망]] 통신 모델/ OC 규격 프레임 오버헤드 구조망 제어 [[136_variance|분산]] 링 토폴로지 생존망 [[352_defect_definition|결함]] 치유 기반) 
897. [[897_rof_radio_over_fiber_analog_transmission_centralized|ROF]] ([[897_rof_radio_over_fiber_analog_transmission_centralized|Radio over Fiber]] [[156_mmwave_millimeter_wave|밀리미터파]] 등 고주파 [[171_antenna_basic_dipole_resonance|안테나]] 베이스밴드 [[130_signal|신호]] 광섬유로 중앙 기지국 아날로그 파장 전달망 구조 효율화 장비 소형화 기반 연구 동향 구성망 요약 구조)
898. NG-PON2 표준 광통신 파장 동적 분할 시분할 TWDM 결합/대칭 40Gbps 가입자망 구조 확장 연계 [[621_scale_up_system_bus|스케일 업]] 망 토폴로지 적용 모델 광단말(ONT/OLT) 분리 배분 기반)
899. [[899_dark_fiber_unlit_infrastructure_lease|다크 파이버]] ([[899_dark_fiber_unlit_infrastructure_lease|Dark Fiber]] 상용 미사용 예비 여유 광케이블 인프라 자산망의 활용 구성 전용 회선 구축 기술 적용 규제 한도 모델링망 파악 인프라)
900. [[900_fso_free_space_optics_hybrid_rf_backup|무선 광통신]] 대기권 전송 [[900_fso_free_space_optics_hybrid_rf_backup|FSO]] 기상 조건 감쇠(안개/비) 대응 라디오 [[555_backup_and_restore_strategy|백업]] 융합 모델 다이버시티 [[167_fading_large_scale_small_scale|페이딩]] 극복 통제망 시스템 체계.
901. [[099_aiops_chatbot_itsm_automation|AIOps]] ([[001_artificial_intelligence|Artificial Intelligence]] for IT Operations 망 자산 수만 건 텔레메트리/[[535_syslog_protocol_udp_514|Syslog]] [[231_ai_turing_test|인공지능]] [[241_machine_learning_basics|머신러닝]] 분석 이상 전조 통보 자가 치유 자동 네트워크 운영 인프라망 관제([[642_observability_telemetry|Observability]]) 시스템 전환)
902. [[902_adn_autonomous_driving_network_level5_zero_touch|자율-구동 네트워크]] ([[416_autonomous_driving_lidar_sae_level|Autonomous Driving]] Network, [[902_adn_autonomous_driving_network_level5_zero_touch|ADN]] 무개입 레벨 별 0~5망 트래픽 [[190_ai_llm_requirements_specification|AI]] 지능형 최적 [[339_routing_overview_best_path_selection|라우팅]]/침해 자동 결단 차단 통제 룰 [[136_variance|분산]] 적용망 시스템 설계 철학)
903. [[126_digital_twin_concept|디지털 트윈]] 네트워크 실시간 토폴로지 동기 트래픽 시뮬레이션 영향도/병목 사전 [[395_verification_process_review|검증]]망 인프라 연계 메타 공간 결합 통신 검토 망 적용 체계
904. [[904_persistent_topology_graph_db_cloud_mapping|퍼시스턴트 토폴로지]] 관리 (동적 장비/[[561_container_based_deployment|컨테이너]] [[528_provisioning|프로비저닝]] 추적 자산 매핑 [[070_graph_datastructure|그래프]] DB 저장 기반 가시성 확보망 시스템 구현 원리)
905. [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] 오디오/비디오 스트리밍 [[295_protocol_field_tcp_udp_icmp|프로토콜]] (HLS [[461_http_stateless_connection_oriented|HTTP]] Live Streaming) 세그먼트 단편 [[501_file_definition_logical_record|파일]] 분할 + M3U8 [[154_database_index_b_tree_search_optimization|인덱스]] [[501_file_definition_logical_record|파일]] 전송 해상도 [[140_bandwidth|대역폭]] 자동 적응 스트리밍 기술
906. [[906_cmaf_common_media_application_format_low_latency|CMAF]] (Common [[121_transmission_media_guided_unguided|Media]] Application Format [[510_dash_dynamic_adaptive_streaming_over_http|DASH]]/HLS 파편화 인코딩 단일 미디어 [[561_container_based_deployment|컨테이너]] 포맷 규격화 통일 [[015_지연_데이터_관점|지연]] 단축 기술 인프라 규정)
907. 화상 회의 지터 버퍼 (Jitter Buffer 패킷 도달 시간편차 무작위성 완충 재생 [[015_지연_데이터_관점|지연]] 최신 [[212_synchronization_mechanisms|동기화]] 체계망 오디오 왜곡 관리 기술망 트러블슈팅 해법) 
908. FEC 실시간 비디오 손실 은닉 기법 미디어 품질 보상 (에러 패킷 무시 보간 재생 보정망 통신 대역 폭증 대비 잉여 [[073_bit|비트]] 기술 적용망 제어 모델 통신 기초)
909. [[909_mos_mean_opinion_score_qoe_emodel|MOS]] (Mean Opinion Score 음성/영상 체감 품질 사용자 5점 척도 측정 통신망 평가 주관식 및 E-Model [[001_algorithm_definition|알고리즘]] 평가 체제 규약)
910. [[910_network_coding_algebraic_packet_combination|네트워크 코딩]] (Network Coding 중간 노드가 패킷 스토어 앤 포워드가 아닌 대수적 연산 병합/조합 전송 [[140_bandwidth|대역폭]] 절감 [[085_confidence_association_rule_conditional_probability|신뢰도]] 향상 [[136_variance|분산]] 통신 기법 수학 모델 원리 개념) 
911. 에지 보안 [[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] 진화 모델 [[481_sse_server_sent_events|SSE]] ([[289_sse_security_service_edge|Security Service Edge]] 네트워킹 [[339_routing_overview_best_path_selection|라우팅]] 배제 클라우드 순수 보안 [[395_verification_process_review|검증]] 엣지 통제 모델 프레임웍) 적용 플랫폼)
912. [[055_ipfs_interplanetary_file_system|IPFS]] ([[055_ipfs_interplanetary_file_system|InterPlanetary File System]] 콘텐츠 주소 지정 영구 [[136_variance|분산]] [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 해시 기반 웹 스토리지 [[295_protocol_field_tcp_udp_icmp|프로토콜]] [[501_file_definition_logical_record|파일]] 망 탈중앙 [[136_variance|분산]]망 구성 기술 요지 [[461_http_stateless_connection_oriented|HTTP]] 위치 지정 대체망 구조 분석 원리망)
913. V2I 노변 기지국 [[913_v2i_rsu_road_side_unit_mec_autonomous_driving|RSU]] 교통 관제 시스템 인프라망 [[627_mec_multi_access_edge_computing_5g|MEC]] 배치 자율협력주행 오프맵 다운 [[015_지연_데이터_관점|지연]]망 극복 패러다임 로컬 통신 반경 [[015_지연_데이터_관점|지연]]) 
914. [[914_lte_r_railway_communication_qpp_ps_lte|철도 통신망]] [[914_lte_r_railway_communication_qpp_ps_lte|LTE-R]] ([[930_ps_lte_public_safety_mcptt_d2d_survival|PS-LTE]] 기반 고속철도 특화 관제망 QPP 재난망 우선 순위 제어 [[377_tunneling_mechanism_overview|터널링]] 오버랩 구성망 생존 시스템 적용 이중 링 기반 네트워크 [[238_switch_operation_principles|스위치]] 통신 토폴로지 구축망)
915. [[915_lte_m_maritime_communication_e_navigation|해상 통신망]] [[621_ltem_emtc_iot_mobility_voice|LTE-M]] / e-Navigation 인프라 [[140_bandwidth|대역폭]] 전파 초고주파 해수면 반사 (다중경로) 채널 무선 구간 간섭 대응망 설계 모델 선박 통신) 
916. [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] ([[916_p2p_peer_to_peer_networking_super_node_gnutella|Peer-to-Peer]]) 네트워킹 (하이브리드, 순수 [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]], 슈퍼 노드 개념 스카이프/토렌트 트래커 해시 분배 매칭 비집중망 탐색 [[001_algorithm_definition|알고리즘]] Gnutella 망 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 구성 통제망)
917. [[917_bittorrent_choke_unchoke_p2p_incentive_algorithm|비트토렌트]] ([[917_bittorrent_choke_unchoke_p2p_incentive_algorithm|BitTorrent]]) 초크/언초크 리치 통신 [[140_bandwidth|대역폭]] 인센티브 [[001_algorithm_definition|알고리즘]]망 파편화 전송 구성/다운 최적 효율망 동적 탐색 구조)
918. [[004_blockchain|블록체인]] 네트워크 계층 가십 [[295_protocol_field_tcp_udp_icmp|프로토콜]] (Gossip [[295_protocol_field_tcp_udp_icmp|Protocol]] 플러딩 전파망 병목 회피 이웃 랜덤 [[389_mesh_topology|메시]]지 전파 무작위 [[136_variance|분산]]형 노드 [[212_synchronization_mechanisms|동기화]] 상태 머신 통신 메커니즘 구축 개념 원리)
919. [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] (Distributed Ledger Technology 노드 간 [[136_variance|분산]]망 [[001_dikw_pyramid|데이터]] 브로드캐스트 합의 컨센서스 패킷 [[395_verification_process_review|검증]] 동기 트래픽 부하망 처리 병목 [[015_지연_데이터_관점|지연]] 문제 파급 관리 기술 시스템 기반 모델)
920. [[022_smart_contract|스마트 컨트랙트]] [[136_variance|분산]]망 오라클 ([[188_pl_sql_t_sql_procedural|Oracle]] 외부 오프체인 [[001_dikw_pyramid|데이터]] [[014_api_posix|API]] 인터넷 연동 진실성 보장 서명 [[001_dikw_pyramid|데이터]]망 접목 통신 체계 신뢰 취약 모델 극복 구성 체제 검토)
921. [[921_quantum_repeater_entanglement_swapping_no_cloning|양자 중계기]] ([[690_round_robin_time_quantum|Quantum]] [[151_repeater_baseband|Repeater]] 노-클로닝 [[016_replication_factor|복제]] 불가 [[220_quantum_entanglement|양자 얽힘]] 텔레포트 통신 장거리 확산 릴레이 시스템 구현 한계 모델 기술 기초 원리 요약) 
922. [[922_qkd_quantum_key_distribution_bb84_eavesdropping|QKD]] ([[690_round_robin_time_quantum|Quantum]] [[067_db_key_uniqueness_minimality|Key]] Distribution) [[295_protocol_field_tcp_udp_icmp|프로토콜]] (BB84 송수신 편광 빔 측정 스니핑 노출 파동 붕괴 탐지 보안 체계 개념망 인프라 구성 한계 암호 분배 융합 [[266_leased_line_basics_e1_t1_t3|전용선]] 적용 구조 분석) 
923. [[923_semantic_communication_6g_ai_meaning_extraction|시맨틱 통신 망]] (Semantic Communication 단순 [[073_bit|비트]] 전달 섀논 통신 넘어서 의미/맥락 [[190_ai_llm_requirements_specification|AI]] 추출/전달 [[347_compaction|압축]] 복원 대역 절감 패러다임 [[419_6g_ntn_thz_ris_next_gen|6G]] 응용 연구 목적 시스템) 
924. [[924_metaverse_network_qos_rendering_offload_mec|메타버스 네트워크]] 대역/[[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 렌더링 오프로드 [[136_variance|분산]] 처리 동기 통신망 공간 [[655_ir_detection_analysis|식별]] [[001_dikw_pyramid|데이터]] 통신 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 요구 스펙 지표 동향망 적용)
925. 오픈API 클라우드 망 연동 / MaaS (Mobility [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]] 통신망 객체 [[136_variance|분산]]망 연계 [[339_routing_overview_best_path_selection|라우팅]] [[001_dikw_pyramid|데이터]] 통합 통신 처리) 
926. 지향성 [[171_antenna_basic_dipole_resonance|안테나]] [[673_mac_message_authentication_code|MAC]] 계층 노출/은닉 망 탐색 [[001_algorithm_definition|알고리즘]] 무선망 방향 제어 최적화 스위프 전파 관리 체계 기술 통제 모델 진화 
927. 스마트 헬스케어 BAN (Body Area Network [[927_wban_wireless_body_area_network_healthcare_sar|무선 인체 통신망]] [[927_wban_wireless_body_area_network_healthcare_sar|WBAN]] 보안 [[509_authorization_models_rbac_abac|인가]] 전력 최소망 구성 흡수율 대응 전파 송신 제어 통계 모델 망 구성 기초 보안 설계 개념 탑재) 
928. [[928_uwsn_underwater_acoustic_sensor_network_ofdm|수중 통신]] 무선 음파(Acoustic) 다중경로 반사 [[015_지연_데이터_관점|지연]] 한계 OFDM 적용 [[928_uwsn_underwater_acoustic_sensor_network_ofdm|UWSN]] (Underwater Sensor Network 전파 도달 손실 통체 주파수 대안 설계 채널망 적용 [[295_protocol_field_tcp_udp_icmp|프로토콜]] [[136_variance|분산]] 기술)
929. [[929_mi_magnetic_induction_underground_radio_communication|지중 통신]](Underground Radio / MI 자기유도 통신 토양 수분 손실 저주파 전파 터널망 [[101_iot_concept|IoT]] 붕괴 통지 시스템 결합망 구성)
930. [[930_ps_lte_public_safety_mcptt_d2d_survival|재난 통신망]] ([[930_ps_lte_public_safety_mcptt_d2d_survival|PS-LTE]] MCPTT 미션 크리티컬 푸시투톡 단말 개입 고속 통제 무선망 [[658_ir_recovery|복구]] 기지국 애드혹 망 생존 체계 오버레이 구축 연대망 모델 통신 시스템 지표 보장망)
931. [[931_emp_shielding|EMP]] (전자기 펄스 방호 케이블 광망 쉴딩 시스템 [[939_faraday_cage|패러데이 케이지]] 네트워크 장비 물리적 안전 [[571_protection_vs_security|보호]] 시설 지침 템플릿 파악 절연 구성)
932. [[932_sniffing_detection_arp_ping|스니핑 탐지]] - [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] 핑(Ping) 테스트 [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]] 감지 (Promiscuous 모드 응답성 시간차 망 분석 진단 통제 통신 구조 [[396_validation|확인]] 체제 도구 기초)
933. 패킷 [[291_fragmentation_and_reassembly_process|단편화]] 오프셋 중첩 [[395_verification_process_review|검증]] 룰 [[690_firewall_generation_evolution|방화벽]] [[229_monitor|모니터]] (비정상 [[601_ids_ips_syscall_tracing|IDS]] 시그니처 연동 패턴 매치 PCAP 망 추출 페이로드 파싱 정규표현 구조 모델 설계망 원리 지표)  
934. [[339_routing_overview_best_path_selection|라우팅]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] [[303_authentication_authorization_patterns|인증]] 방어망 [[668_md5_hash_collision_vulnerability|MD5]]/SHA [[303_authentication_authorization_patterns|인증]] 해시 키 연동 [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] [[160_session_controlling_terminal|세션]] 탈취 방지 RST [[598_spoofing|스푸핑]] 우회 라우터 연계 BCP(Best [[002_current|Current]] Practice) [[009_config|설정]] 보안 모델 
935. [[935_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention|RPKI]] (Resource [[984_pki_public_key_infrastructure_ca_ra_certificate|Public Key Infrastructure]] - [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[598_spoofing|스푸핑]]/[[365_bgp_border_gateway_protocol_path_vector|BGP]] 하이재킹 경로 위조 공격 차단 인터넷 [[339_routing_overview_best_path_selection|라우팅]] 테이블 서명/[[303_authentication_authorization_patterns|인증]]서 기반 [[509_authorization_models_rbac_abac|인가]] [[395_verification_process_review|검증]] [[339_routing_overview_best_path_selection|라우팅]] [[352_defect_definition|결함]] 예방 [[339_routing_overview_best_path_selection|라우팅]]망 안전 표준 체계 인프라 기술 모델 분석 설계)
936. [[511_dns_hierarchical_distributed_architecture|DNS]] 싱크홀 (Zombie [[164_pc|PC]] [[990_botnet_cnc|봇넷]] C&C 서버 질의 블랙리스트 감지/경로 우회 KISA 차단 연계 악성 [[064_relation_domain|도메인]] 룩업망 접속 [[656_ir_containment|억제]] 무효화 처리 방화 [[164_policy|정책]]) 
937. [[937_hybrid_encryption|하이브리드 암호 시스템]] ([[282_performance_tactics|성능]]과 키배포 장점 결합: 대칭키로 [[001_dikw_pyramid|데이터]] 암호화([[160_session_controlling_terminal|세션]]키), 대칭키를 [[110_rsa|RSA]] 비대칭키로 암호화 분배 통신망 전송 모델 SSL/[[494_pgp_pretty_good_privacy_web_of_trust|PGP]] 기본 원리 기초 개념 정리 체계 비교 모델망 특성)
938. [[938_file_carving|파일 카빙]] ([[938_file_carving|File Carving]] [[668_network_forensics|네트워크 포렌식]] 덤프 이진 PCAP 시그니처 획득 페이로드 헤더/푸터 [[658_ir_recovery|복구]] 멀웨어 캡슐 파싱 통신 재구성 분석 기술 모델 보안 관제 기초 툴킷 활용 방식망 적용)
939. [[939_honeypot_deception|포니팟]] ([[939_honeypot_deception|Honeypot]]) [[695_honey_net|허니넷]](Honeynet) 유인 분리망 분석 시스템 / 사이버 [[693_deception_technology|기만 기술]] ([[693_deception_technology|Deception Technology]], 동적 가짜 자산/호스트 할당 공격 표적 교란망 대응 시스템 지능 체계 통제 모델화)

## 19. 통신/네트워크 시험 빈출 및 토픽 단어 (60개)
940. [[940_baseband_line_coding_nrz_rz_manchester|기저대역]]([[940_baseband_line_coding_nrz_rz_manchester|Baseband]]) 선로 부호 (RZ, NRZ, 맨체스터 등) 
941. [[941_shannon_hartley_theorem_channel_capacity_snr|샤논-하틀리]]([[941_shannon_hartley_theorem_channel_capacity_snr|Shannon-Hartley]]) 
942. [[057_에일리어싱_Aliasing|에일리어싱]] ([[057_에일리어싱_Aliasing|Aliasing]]) 
943. [[943_pcm_pulse_code_modulation_sampling_quantization|펄스부호변조]] ([[943_pcm_pulse_code_modulation_sampling_quantization|PCM]]) 
944. [[944_mux_demux_multiplexer_demultiplexer_circuit_sharing|다중화기]] ([[944_mux_demux_multiplexer_demultiplexer_circuit_sharing|MUX]]) / 역다중화기 (DEMUX)
945. [[945_ofdma_orthogonal_frequency_division_multiple_access_resource_block|직교주파수분할다중접속]] ([[945_ofdma_orthogonal_frequency_division_multiple_access_resource_block|OFDMA]]) 
946. FDM 가드 밴드 ([[946_guard_band_fdm_adjacent_channel_interference|Guard Band]])
947. OFDM 사이클릭 프리픽스 ([[086_CP_순환_전치_GI|Cyclic Prefix]], [[086_CP_순환_전치_GI|CP]])
948. [[110_hamming_distance|해밍 거리]] ([[110_hamming_distance|Hamming Distance]]) 
949. [[949_arq_automatic_repeat_request_go_back_n_selective|자동 재전송 요구]] ([[949_arq_automatic_repeat_request_go_back_n_selective|ARQ]]) 선택적/GBN
950. [[216_hdlc_high_level_data_link_control|HDLC]] [[187_bit_stuffing_flag_mechanism|비트 스터핑]] ([[187_bit_stuffing_flag_mechanism|Bit Stuffing]])
951. [[054_반송파_Carrier_Wave|반송파]] 감지 [[087_다중접속_Multiple_Access|다중 접속]] 및 충돌 검출 ([[104_csma|CSMA]]/CD)
952. [[952_csma_ca_hidden_terminal_rts_cts_wireless|은닉 단말]] ([[952_csma_ca_hidden_terminal_rts_cts_wireless|Hidden Terminal]]) 문제 ([[104_csma|CSMA]]/[[089_contract_account_smart_contract|CA]] RTS/CTS) 
953. [[183_mac_media_access_control|매체 접근 제어]] ([[673_mac_message_authentication_code|MAC]])
954. [[954_spread_spectrum_communication_anti_jamming_cdma|확산 스펙트럼]] ([[068_스펙트럼_확산_Spread_Spectrum|Spread Spectrum]])
955. [[955_fhss_frequency_hopping_spread_spectrum_bluetooth|FHSS]] ([[955_fhss_frequency_hopping_spread_spectrum_bluetooth|주파수 도약]]) 
956. [[956_dsss_direct_sequence_spread_spectrum_chipping_code|DSSS]] ([[956_dsss_direct_sequence_spread_spectrum_chipping_code|직접 확산]])
957. 코드 분할 [[087_다중접속_Multiple_Access|다중 접속]] ([[957_cdma_code_division_multiple_access_dsss_orthogonality|CDMA]])
958. [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 트렁킹 (IEEE 802.1Q 태그)
959. [[959_spanning_tree_protocol_stp_loop_avoidance|스패닝 트리]] 
960. [[960_loop_avoidance_stp_ttl_routing_prevention|루프 어보이던스]] ([[570_stp_vs_mtp|STP]] 적용)
961. [[357_ospf_open_shortest_path_first_overview|OSPF]] [[348_link_state_routing_dijkstra_spf|링크 상태]] [[002_database_definition|데이터베이스]] ([[961_ospf_link_state_database_dijkstra_spf_routing|LSDB]])
962. [[962_bgp_as_path_loop_prevention_path_vector|BGP AS-Path]]
963. [[963_subnet_mask_cidr_classless_inter_domain_routing|서브넷 마스크]] ([[963_subnet_mask_cidr_classless_inter_domain_routing|Subnet Mask]]) / CIDR
964. [[324_ipv6_128bit_next_generation_address|IPv6]] 헤더 [[347_compaction|압축]] / [[331_slaac_stateless_address_autoconfiguration_ndp|SLAAC]]
965. [[307_nat_network_address_translation_router_principles|NAT]] 횡단 ([[384_nat_t_ipsec_nat_traversal_udp_4500|NAT Traversal]])
966. [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] ([[333_igmp_internet_group_management_protocol_multicast|IGMP]], [[430_pim|PIM]])
967. [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 슬라이딩 윈도우 
968. [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 쓰리웨이 핸드셰이크
969. [[429_cwnd_congestion_window_concept|혼잡 윈도우]] ([[969_congestion_window_cwnd_tcp_network_overload|Congestion Window]])
970. [[430_slow_start_exponential_growth_cwnd|슬로우 스타트]] ([[430_slow_start_exponential_growth_cwnd|Slow Start]])
971. [[971_hol_blocking_head_of_line_tcp_http_delay|홀오브라인 블로킹]] ([[971_hol_blocking_head_of_line_tcp_http_delay|HOL Blocking]])
972. [[454_quic_quick_udp_internet_connections|QUIC]] (0-[[441_rtt_round_trip_time_srtt_smoothed|RTT]] 핸드셰이크)
973. [[461_http_stateless_connection_oriented|HTTP]]/2 멀티플렉싱 
974. [[974_restful_api_stateless_http_methods_uri|RESTful API]]
975. [[975_websocket_full_duplex_realtime_http_upgrade|웹소켓]] ([[480_websocket_full_duplex|WebSocket]])
976. [[511_dns_hierarchical_distributed_architecture|DNS]] [[598_spoofing|스푸핑]]
977. [[522_dhcp_dynamic_host_configuration_protocol|DHCP]] 릴레이 에이전트
978. [[528_snmp_simple_network_management_protocol|SNMP]] [[529_mib_oid_snmp_architecture|MIB]] 구조
979. [[589_ipsec_offload|IPSec]] 터널/수송 모드 
980. [[381_ah_authentication_header_integrity_auth|AH]] ([[381_ah_authentication_header_integrity_auth|Authentication Header]]) 
981. [[382_esp_encapsulating_security_payload_confidentiality|ESP]] ([[382_esp_encapsulating_security_payload_confidentiality|Encapsulating Security Payload]])
982. SSL/[[694_thread_local_storage_tls|TLS]] 핸드셰이크
983. [[983_vpn_virtual_private_network|VPN]] ([[983_vpn_virtual_private_network|가상 사설망]])
984. [[159_pki_public_key_infrastructure|PKI]] 공개키 인프라
985. X.509 [[303_authentication_authorization_patterns|인증]]서
986. 대칭키 / 비대칭키 구조 비교 
987. [[667_hash_function_integrity_one_way|해시 함수]] 
988. [[988_digital_signature|전자 서명]]
989. [[989_dos_denial_of_service|서비스 거부 공격]] ([[599_dos_ddos_attack|DoS]])
990. [[990_botnet_cnc|봇넷]] ([[990_botnet_cnc|Botnet]]) C&C 
991. [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] [[598_spoofing|스푸핑]] 
992. [[690_firewall_generation_evolution|방화벽]] ([[992_firewall_stateful_inspection|Stateful Inspection]])
993. [[696_waf_web_application_firewall|WAF]] ([[993_waf_web_application_firewall|웹 방화벽]])
994. [[601_ids_ips_syscall_tracing|IDS]] / [[695_ips_network_intrusion_prevention_system|IPS]] 탐지 차단율 
995. [[149_network_slicing_5g_architecture|네트워크 슬라이싱]] 
996. [[865_nfv_network_functions_virtualization_architecture|NFV]] 기반 [[015_virtualization|가상화]] [[866_vnf_virtual_network_function_software_appliance|VNF]]
997. [[633_sdn_whitebox|SDN]] [[001_dikw_pyramid|데이터]]/컨트롤 플레인
998. [[855_openflow_standard_protocol_sdn_southbound|OpenFlow]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 
999. [[627_mec_multi_access_edge_computing_5g|MEC]] ([[999_mec_mobile_edge_computing|모바일 엣지 컴퓨팅]])
1000. [[1000_cni_cloud_native_network|클라우드 네이티브 네트워크]] ([[822_cni_container_network_interface_kubernetes|CNI]])

## 20. 네트워크 [[282_performance_tactics|성능]] 평가 및 심화/기타 실무 용어 (200개 요약집)
1001. [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] / QoE 차이 비교 
1002. [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]] ([[441_rtt_round_trip_time_srtt_smoothed|Rtt]] vs [[008_단방향_반이중_전이중|단방향]] Delay) 
1003. [[139_throughput|처리량]] ([[139_throughput|Throughput]]) 수식화
1004. [[1004_erlang_traffic_load_unit_calculation|Erlang]] (얼랑, 통신 트래픽 부하 단위량)
1005. 호손율 / 블로킹 [[130_probability|확률]] ([[1005_blocking_probability_erlang_b_qos_call_drop|Blocking Probability]])
1006. [[1006_network_reliability_topology_node_link_connectivity|망 신뢰도]] (네트워크 토폴로지 연결도 계산법) 
1007. [[450_mtbf|MTBF]] ([[450_mtbf|평균 무고장 시간]]) 통신망 생존성
1008. [[451_mttr|MTTR]] ([[451_mttr|평균 수리 시간]]) 회선 [[456_dual_redundancy|이중화]]
1009. [[1009_backhaul_network_base_station_core_connection|백홀]] ([[1009_backhaul_network_base_station_core_connection|Backhaul]]) 
1010. [[1010_midhaul_network_c_ran_fronthaul_du_cu|미드홀]] ([[1010_midhaul_network_c_ran_fronthaul_du_cu|Midhaul]]) 
1011. [[784_fronthaul_ecpri_split_option|프론트홀]] ([[1011_fronthaul_network_c_ran_cpri_roef|Fronthaul]]) 
1012. [[1012_cell_edge_throughput_interference_icic|셀 엣지 수율]] ([[1012_cell_edge_throughput_interference_icic|Cell Edge Throughput]])
1013. [[1013_comp_coordinated_multipoint_transmission|CoMP]] ([[1013_comp_coordinated_multipoint_transmission|협력 통신]]) 
1014. [[1014_carrier_aggregation_lte_advanced_5g|캐리어 어그리게이션]] ([[089_contract_account_smart_contract|CA]]) 
1015. [[1015_unlicensed_band_lte_u_nr_u_wifi_coexistence|언면허 대역망]] (Unlicensed Band [[752_lte_long_term_evolution_4g|LTE]]-U / NR-U) 
1016. [[1016_laa_licensed_assisted_access_lbt_algorithm|LAA]] ([[1016_laa_licensed_assisted_access_lbt_algorithm|Licensed Assisted Access]])
1017. [[1017_wifi_offloading_cellular_traffic_congestion|와이파이 오프로딩]]
1018. [[156_mmwave_millimeter_wave|밀리미터파]] ([[156_mmwave_millimeter_wave|mmWave]]) 전파 감쇠
1019. [[157_terahertz_thz_6g|테라헤르츠]] ([[157_terahertz_thz_6g|THz]]) 대역 
1020. [[136_fso_free_space_optics_laser|자유 공간 광통신]] ([[900_fso_free_space_optics_hybrid_rf_backup|FSO]])
1021. [[158_vlc_lifi_visible_light|가시광 통신]] ([[1021_vlc_lifi|VLC]]) 라이파이 (Li-Fi)
1022. [[1022_leo_satellite_network|저궤도 위성망]] 스타링크 
1023. [[1023_isl_inter_satellite_link_low_earth_orbit_routing|위성 통신 핸드오버]] ([[249_isl_inter_switch_link_cisco|ISL]] - [[1023_satellite_isl_handover|Inter-Satellite Link]]) 
1024. [[141_v2x_vehicle_to_everything_communication|V2X]] (차량사물 연결) 
1025. [[143_c_v2x_cellular_based_communication|C-V2X]] / [[590_wave_ieee_802_11p_dsrc_v2x|WAVE]] ([[1025_c_v2x_wave_dsrc|DSRC]]) [[121_transmission_media_guided_unguided|매체]] 제어 
1026. [[161_smart_grid_architecture|스마트 그리드]] 통신 인프라망
1027. [[1027_underwater_acoustic_network|수중 음파 통신망]]
1028. [[1028_wban_wireless_body_area_network|체내 통신]] ([[927_wban_wireless_body_area_network_healthcare_sar|WBAN]])
1029. [[109_lpwan_low_power_wide_area_network|LPWAN]] [[283_lora_low_rank_adaptation|로라]] ([[617_lora_lorawan_css_chirp_spread_spectrum|LoRa]])
1030. [[1030_lpwan_sigfox|시그폭스]] ([[1030_lpwan_sigfox|SigFox]]) 협대역 통신
1031. [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]] 전력 최적화 (PSM/eDRX)
1032. [[605_bluetooth_ieee_802_15_1_piconet_scatternet|블루투스]] LE ([[607_ble_bluetooth_low_energy_iot|BLE]])
1033. [[609_zigbee_ieee_802_15_4_mesh_iot|지그비]] ([[609_zigbee_ieee_802_15_4_mesh_iot|Zigbee]]) 메쉬
1034. NFC 표준 (13.56MHz) 
1035. RFID 충돌 방지 [[001_algorithm_definition|알고리즘]] (알로하 기반) 
1036. EPCglobal 망 아키텍처
1037. [[1037_ons_object_name_service_rfid_dns|ONS]] ([[1037_ons_object_name_service_rfid_dns|Object Name Service]]) 구조
1038. [[622_mqtt_publish_subscribe_qos|MQTT]] 퍼블리시 서브스크라이브 모드
1039. [[120_coap_constrained_application_protocol|CoAP]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 및 [[156_rest_representational_state_transfer|REST]] 인터페이스
1040. [[092_thread_lwp|Thread]] / [[612_matter_csa_smart_home_standard|Matter]] (스마트홈) 표준 망 
1041. [[849_sd_wan_software_defined_wide_area_network|SD-WAN]] 중앙 [[164_policy|정책]] 관리형 브랜치
1042. [[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] 네트워킹/보안 융합 클라우드
1043. [[1043_ztna_zero_trust_network_access_architecture|제로 트러스트 구조]]
1044. [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]
1045. [[615_ebpf|eBPF]] [[022_kernel_role|커널]] 네트워킹 후킹 시스템
1046. [[874_p4_programming_data_plane_pipeline_int_telemetry|P4]] 네트워크 프로그래밍 모델 플로우 
1047. [[1047_tsn_time_sensitive_networking_deterministic|타임 센시티브 네트워킹]] ([[546_tsn_hardware|TSN]] 인프라망) 
1048. IEEE 1588 PTP 시각 동기망
1049. [[536_ntp_network_time_protocol_stratum|NTP]] / GPS [[212_synchronization_mechanisms|동기화]] 
1050. [[639_rdma_kernel_bypass|RDMA]] / [[523_roce|RoCE]] 스토리지 서버 네트워킹
1051. [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] 오버레이 VTEP [[377_tunneling_mechanism_overview|터널링]] 연결기법
1052. [[820_evpn_ethernet_vpn_bgp_control_plane|EVPN]]-[[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]] [[365_bgp_border_gateway_protocol_path_vector|BGP]] 컨트롤 플레인 전이
1053. Spine-Leaf 대용량 클로스 구조
1054. [[857_ibn_intent_based_networking_declarative_automation|IBN]]([[1054_ibn_intent_based_networking_ai_automation|의도기반망]]) 선행 [[190_ai_llm_requirements_specification|AI]] 설계 
1055. 화이트박스 [[746_ocp|OCP]] [[238_switch_operation_principles|스위치]]
1056. ONOS / OpenDaylight 구조 모델 비교 
1057. NETCONF / YANG 모델링 규격체 
1058. 트래픽 텔레메트리 ([[1058_streaming_telemetry_network_monitoring|Streaming Telemetry]]) 
1059. [[126_digital_twin_concept|디지털 트윈]] 및 관제 시스템 연동 
1060. 양자 암호 키 분배 ([[922_qkd_quantum_key_distribution_bb84_eavesdropping|QKD]] 인프라 기반망)
1061. [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[935_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention|RPKI]] [[339_routing_overview_best_path_selection|라우팅]] 보안 망 
1062. [[518_dnssec_dns_security_extensions|DNSSEC]] 존 
1063. [[520_doh_dns_over_https|DoH]] / [[519_dot_dns_over_tls|DoT]] (웹/전송 보안 계층 [[511_dns_hierarchical_distributed_architecture|DNS]] 암호화)
1064. [[1064_esni_ech_tls_1_3_encrypted_sni|ESNI]] ([[694_thread_local_storage_tls|TLS]] 1.3 평문 노출 보안)
1065. [[461_http_stateless_connection_oriented|HTTP]]/3 [[454_quic_quick_udp_internet_connections|QUIC]] [[429_cwnd_congestion_window_concept|혼잡 윈도우]] 이식
1066. [[532_microservices_decomposition_patterns|마이크로서비스]] [[302_service_mesh_istio|서비스 메시]] 패싱
1067. [[829_istio_envoy_service_mesh_control_plane|이스티오]]([[302_service_mesh_istio|Istio]]) [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]]
1068. [[479_grpc_protobuf_http2|gRPC]] / [[295_protocol_field_tcp_udp_icmp|프로토콜]] 버퍼 [[149_serial_communication_rs232_rs485|직렬]]화 
1069. [[505_webrtc_web_real_time_communication|WebRTC]] [[307_nat_network_address_translation_router_principles|NAT]] 횡단 (STUN/TURN/ICE 통합)
1070. [[506_cdn_content_delivery_network_edge_caching|CDN]] 엣지 노드 [[136_variance|분산]] 
1071. [[507_gslb_global_server_load_balancing_dns|GSLB]] 지리적 [[511_dns_hierarchical_distributed_architecture|DNS]] [[339_routing_overview_best_path_selection|라우팅]] 
1072. [[535_system_in_package|SIP]] INVITE 기반 핸드셰이크
1073. [[503_ip_pbx_private_branch_exchange|IP PBX]] [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]]
1074. [[324_ipv6_128bit_next_generation_address|IPv6]] [[331_slaac_stateless_address_autoconfiguration_ndp|SLAAC]] 자동할당
1075. [[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] [[335_mld_multicast_listener_discovery_ipv6|MLD]] / [[333_igmp_internet_group_management_protocol_multicast|IGMP]] 스누핑 기법
1076. [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] [[598_spoofing|스푸핑]] 중간자 방어 ([[1076_arp_spoofing_mitm_dynamic_arp_inspection_dai|동적 검사 체계]])
1077. DDoS 반사 증폭 원조 ([[536_ntp_network_time_protocol_stratum|NTP]], [[511_dns_hierarchical_distributed_architecture|DNS]] [[446_port_and_bus|포트]]망) 
1078. 클라우스 보안 워크로드 [[332_cwpp|CWPP]] 통제망 
1079. [[182_network_separation_model|망분리]] [[369_logic_bomb|논리]]적 / 물리적 [[079_developer_cleanroom_vdi_security|VDI]] 전이 모델 
1080. [[668_network_forensics|네트워크 포렌식]] 패킷 덤프 파싱
1081. [[695_ips_network_intrusion_prevention_system|IPS]] 시그니처 정규식 
1082. [[747_web_shell_file_upload_vulnerability|웹쉘]] 탐지 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 파서
1083. [[918_gossip_protocol_blockchain_epidemic_network|블록체인 가십 프로토콜]] [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 연결 
1084. 다크 웹 Tor 통신 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 암호화층 
1085. [[589_ipsec_offload|IPsec]] [[280_ikev2|IKEv2]] 터널 협상
1086. [[387_wireguard_vpn_modern_tunneling|WireGuard]] [[339_routing_overview_best_path_selection|라우팅]] 고속망 체계 
1087. [[439_bbr_bottleneck_bandwidth_and_rtt_google_congestion_control|BBR]] 구글 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 동적 모델 [[015_지연_데이터_관점|지연]] 기반 혼잡 
1088. ECN 징후 큐 통지 
1089. [[390_diffserv_differentiated_services_dscp_phb|DiffServ]] DSCP [[104_classification_analysis|분류]] PHB
1090. RSVP 자원 예약 플로우
1091. [[378_gre_generic_routing_encapsulation|GRE]] 일반 캡슐화 포맷 오버헤드 
1092. [[386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp|DMVPN]] [[341_dynamic_routing_protocol_operation|동적 라우팅]] 결합형 지점 
1093. [[376_mpls_vpn_l3_vrf_bgp|MPLS VPN]] L3 경로 격리 라벨 [[238_switch_operation_principles|스위치]]
1094. [[357_ospf_open_shortest_path_first_overview|OSPF]] ABR / ASBR Area 위계 [[136_variance|분산]]망 
1095. [[365_bgp_border_gateway_protocol_path_vector|BGP]] [[082_attribute_types_er_model|속성]] (Local Pref, MED, [[344_as_autonomous_system_asn|AS]]-path 구성비)
1096. [[355_eigrp_enhanced_igrp_dual_algorithm|EIGRP]] DUAL [[015_지연_데이터_관점|지연]] 스케일 [[136_variance|분산]]
1097. [[1097_broadcast_storm_switching_loop_stp|브로드캐스트 스톰]] ([[1097_broadcast_storm_switching_loop_stp|루프 발생]])
1098. LACP [[263_etherchannel_link_aggregation_lacp|이더채널]] [[446_port_and_bus|포트]] [[369_logic_bomb|논리]] [[535_grouping_counting_free_space|그룹화]]
1099. [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 간 [[339_routing_overview_best_path_selection|라우팅]] 
1100. [[1100_port_mirroring_span_tap_network_monitoring|스위치 포트 미러링]] (SPAN/TAP)
1101. [[124_unshielded_twisted_pair|UTP]] 배선 카테고리
1102. [[1102_optical_fiber_single_mode_multi_mode|광섬유 싱글모드 다중모드]] 
1103. WDM 무손실 광 증폭 
1104. [[782_o_ran_open_ran_white_box_interface|O-RAN]] [[784_fronthaul_ecpri_split_option|프론트홀]] 개방 사양 
1105. [[886_vcpe_virtual_customer_premises_equipment_edge_vnf|vCPE]] [[865_nfv_network_functions_virtualization_architecture|NFV]] 고객 구내 망 통합 전환 
1106. [[1106_microgrid_communication_standards_iec61850|마이크로그리드 통신 규격]]
1107. 산업용 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] [[900_profinet|PROFINET]] 망 
1108. [[891_ot_operational_technology|OT]] 망 ([[1108_ot_network_security_air_gap_isolation|운영 기술 망]]) 분리 원단 통제
1109. [[631_opc_ua_smart_factory_protocol|OPC UA]] 자동화 프레임 표준 통신
1110. [[845_lossless_ethernet_dcb_pfc_roce_fcoe|무손실 이더넷]] (PFC 체제) 
1111. [[671_dpdk|DPDK]] 패킷 바이패스 
1112. 스마트NIC 가속 [[440_offloading|오프로딩]] 시스템 
1113. [[150_5g_sa_standalone_architecture|5G SA]]/[[766_nsa_non_standalone_5g_lte_core|NSA]] 아키텍처 비교망
1114. 스몰 셀 조밀화 간섭 통제망
1115. [[099_Massive_MIMO_대규모_다중_안테나|Massive MIMO]] 빔 관리 시스템 
1116. 자율 구동 네트워크 레벨링 
1117. [[1117_network_security_zero_trust_policy|네트워크 보안]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] [[164_policy|정책]]) 
1118. 정보통신 기술사 최근 기출 토픽 기반
1119. [[419_6g_ntn_thz_ris_next_gen|6G]] 융합 [[157_terahertz_thz_6g|테라헤르츠]] 예측 지표망
1120. [[1120_uam_urban_air_mobility_satellite_routing|위성 기반 도심항공교통]]([[145_uam_urban_air_mobility_evtol|UAM]]) [[339_routing_overview_best_path_selection|라우팅]] 통신 구조 모델

---
**총정리 네트워크 키워드 : 총 1,120개 수록** (+관련 항목 파생 개념 수련시 약 1,500개 커버 가능)
(네트워크 기초, 심화, 보안, 최신 클라우드 및 통신 아키텍처 전반을 심도있게 다룬 완전판입니다.)