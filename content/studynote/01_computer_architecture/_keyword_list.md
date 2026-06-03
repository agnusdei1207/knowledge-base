---
title: 01. 컴퓨터구조 키워드 목록
date: '2026-03-04'
tags:
- studynote-computer-architecture
---
[[267_weight_bias_activation|weight]] = 9999

# 컴퓨터구조 심화 키워드 목록 (기술사 최적화 1000제)

정보관리기술사, 컴퓨터응용시스템기술사 시험에 가장 적합한 범위로 엄선한 1,000여 개의 컴퓨터구조 핵심 및 심화 키워드입니다. 

너무 지엽적인 물리·전자공학적 레벨은 지양하고, **IT 시스템 엔지니어링, 아키텍처, [[282_performance_tactics|성능]] 평가, 메모리 및 스토리지 시스템, [[430_index_fast_full_scan|병렬]] 컴퓨팅, 최신 [[190_ai_llm_requirements_specification|AI]] 가속기([[424_npu|NPU]]/[[425_tpu|TPU]]), 그리고 클라우드 및 보안 하드웨어**에 초점을 맞추어 재구성하였습니다.

---

## 1. 기초 전기전자 및 디지털 [[369_logic_bomb|논리]]회로 (Basic Electronics & Logic)
1. [[001_voltage|전압]] ([[001_voltage|Voltage]])
2. [[002_current|전류]] ([[002_current|Current]])
3. [[003_resistance|저항]] ([[003_resistance|Resistance]])
4. [[004_impedance|임피던스]] ([[004_impedance|Impedance]])
5. [[005_capacitor|커패시터]] ([[005_capacitor|Capacitor]], 축전기)
6. [[006_capacitance|정전용량]] ([[006_capacitance|Capacitance]])
7. [[007_inductor|인덕터]] ([[007_inductor|Inductor]])
8. [[008_conductor|도체]] ([[008_conductor|Conductor]])
9. [[009_semiconductor|반도체]] ([[009_semiconductor|Semiconductor]])
[[489_raid_10_hybrid|10]]. [[010_insulator|절연체]] ([[010_insulator|Insulator]])
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[011_diode|다이오드]] ([[011_diode|Diode]])
12. [[012_rectifier|정류 회로]] ([[012_rectifier|Rectifier]])
13. [[013_led|발광 다이오드]] ([[013_led|LED]])
14. [[014_transistor|트랜지스터]] ([[014_transistor|Transistor]])
15. [[015_bjt|BJT]] ([[015_bjt|Bipolar Junction Transistor]])
16. [[016_fet|FET]] ([[016_fet|전계효과 트랜지스터]])
17. [[017_mosfet|MOSFET]]
18. [[018_cmos|CMOS]] ([[018_cmos|Complementary MOS]])
19. [[019_finfet|핀펫]] ([[019_finfet|FinFET]])
20. [[020_gaa|GAA]] ([[020_gaa|Gate-All-Around]])
21. 디지털 시스템 vs 아날로그 시스템
22. [[022_boolean_algebra|부울 대수]] ([[022_boolean_algebra|Boolean Algebra]])
23. 드모르간의 법칙 (De Morgan's Law)
24. [[024_truth_table|진리표]] ([[024_truth_table|Truth Table]])
25. [[025_karnaugh_map|카르노 맵]] ([[025_karnaugh_map|Karnaugh Map]])
26. 최소항 (Minterm)과 최대항 (Maxterm)
27. [[027_logic_gates|논리 게이트]] ([[027_logic_gates|Logic Gates]])
28. AND, OR, NOT 게이트
29. NAND, NOR 게이트
30. XOR, XNOR 게이트
31. 범용 게이트 ([[031_universal_gate|Universal Gate]])
32. 조합 [[369_logic_bomb|논리]]회로 ([[032_combinational_logic|Combinational Logic]])
33. [[033_half_adder|반가산기]] ([[033_half_adder|Half Adder]])
34. [[034_full_adder|전가산기]] ([[034_full_adder|Full Adder]])
35. [[035_ripple_carry_adder|리플 캐리 가산기]] ([[035_ripple_carry_adder|Ripple Carry Adder]])
36. 캐리 예측 가산기 (Carry Look-ahead Adder)
37. [[037_subtractor|감산기]] ([[037_subtractor|Subtractor]])
38. [[038_parallel_adder_subtractor|병렬 가감산기]]
39. [[039_decoder|디코더]] ([[039_decoder|Decoder]])
40. [[040_encoder|인코더]] ([[040_encoder|Encoder]])
41. [[041_multiplexer|멀티플렉서]] ([[041_multiplexer|Multiplexer]], [[944_mux_demux_multiplexer_demultiplexer_circuit_sharing|MUX]])
42. [[042_demultiplexer|디멀티플렉서]] ([[042_demultiplexer|Demultiplexer]], DEMUX)
43. [[043_comparator|비교기]] ([[043_comparator|Comparator]])
44. 순차 [[369_logic_bomb|논리]]회로 ([[044_sequential_logic|Sequential Logic]])
45. 클럭 ([[045_clock|Clock]])
46. 에지 [[507_acid_properties|트리거]] ([[046_edge_trigger|Edge Trigger]])
47. 레벨 [[507_acid_properties|트리거]] ([[047_level_trigger|Level Trigger]])
48. 래치 ([[048_latch|Latch]])
49. SR 래치
50. D 래치
51. [[051_flip_flop|플립플롭]] ([[051_flip_flop|Flip-Flop]])
52. SR [[051_flip_flop|플립플롭]]
53. D [[051_flip_flop|플립플롭]]
54. JK [[051_flip_flop|플립플롭]]
55. T [[051_flip_flop|플립플롭]]
56. [[056_master_slave_flip_flop|마스터-슬레이브 플립플롭]]
57. [[057_register|레지스터]] ([[175_register_addressing|Register]])
58. [[058_shift_register|시프트 레지스터]] ([[058_shift_register|Shift Register]])
59. [[059_counter|카운터]] ([[059_counter|Counter]])
60. [[060_synchronous_counter|동기식 카운터]] ([[060_synchronous_counter|Synchronous Counter]])
61. [[061_asynchronous_counter|비동기식 카운터]] ([[061_asynchronous_counter|리플 카운터]])
62. 업/다운 [[059_counter|카운터]]
63. [[063_ring_counter|링 카운터]] ([[063_ring_counter|Ring Counter]])
64. [[064_johnson_counter|존슨 카운터]] ([[064_johnson_counter|Johnson Counter]])
65. [[065_state_diagram|상태도]] ([[065_state_diagram|State Diagram]])
66. [[066_state_table|상태표]] ([[066_state_table|State Table]])
67. [[067_moore_machine|무어 머신]] ([[067_moore_machine|Moore Machine]])
68. [[068_mealy_machine|밀리 머신]] ([[068_mealy_machine|Mealy Machine]])
69. [[606_dynamic_partial_reconfiguration|FPGA]] (Field Programmable Gate [[055_array|Array]])
70. [[070_asic|ASIC]] ([[070_asic|주문형 반도체]])
71. [[071_cpld|CPLD]]
72. [[072_hdl|하드웨어 기술 언어]] (VHDL, Verilog)

## 2. [[001_dikw_pyramid|데이터]] 표현과 연산 ([[001_dikw_pyramid|Data]] Representation & Arithmetic)
73. [[073_bit|비트]] ([[086_fenwick_tree|Bit]])
74. [[074_byte|바이트]] ([[074_byte|Byte]])
75. [[075_word|워드]] ([[075_word|Word]])
76. [[076_double_word|더블 워드]] ([[076_double_word|Double Word]])
77. [[077_radix|기수]] ([[077_radix|Radix]])
78. [[078_numeral_systems|진법 변환]] (2진수, 8진수, 10진수, 16진수)
79. [[079_lsb|LSB]] ([[079_lsb|Least Significant Bit]])
80. [[080_msb|MSB]] ([[080_msb|Most Significant Bit]])
81. [[081_unsigned_integer|부호 없는 정수]] ([[081_unsigned_integer|Unsigned Integer]])
82. [[082_signed_integer|부호 있는 정수]] ([[082_signed_integer|Signed Integer]])
83. [[083_sign_magnitude|부호와 절댓값]] ([[083_sign_magnitude|Sign-Magnitude]])
84. 1의 보수 (1's Complement)
85. 2의 보수 (2's Complement)
86. [[086_fixed_point|고정소수점]] ([[086_fixed_point|Fixed Point]])
87. [[087_floating_point|부동소수점]] ([[087_floating_point|Floating Point]])
88. [[088_ieee_754|IEEE 754]] 표준
89. [[089_single_precision|단정밀도]] ([[089_single_precision|Single Precision]], FP32)
90. [[090_double_precision|배정밀도]] ([[090_double_precision|Double Precision]], FP64)
91. [[091_half_precision|반정밀도]] ([[091_half_precision|Half Precision]], FP16)
92. [[092_bfloat16|bfloat16]] ([[092_bfloat16|Brain Floating Point]])
93. [[093_normalization|정규화]] ([[093_normalization|Normalization]])
94. [[094_bias|편향 지수]] ([[094_bias|Bias]])
95. [[095_overflow|오버플로우]] ([[095_overflow|Overflow]])
96. [[096_underflow|언더플로우]] ([[096_underflow|Underflow]])
97. [[097_nan|NaN]] ([[097_nan|Not a Number]])
98. [[098_bcd|BCD]] 코드 ([[098_bcd|Binary Coded Decimal]])
99. 팩드 [[098_bcd|BCD]] ([[099_packed_bcd|Packed BCD]])
100. 언팩드 [[098_bcd|BCD]] ([[100_unpacked_bcd|Unpacked BCD]])
101. [[101_excess_3|3초과 코드]] ([[101_excess_3|Excess-3 Code]])
102. [[102_gray_code|그레이 코드]] ([[102_gray_code|Gray Code]])
103. [[103_ascii|ASCII]] 코드
104. [[104_unicode|유니코드]] ([[104_unicode|Unicode]])
105. [[105_utf8|UTF-8]]
106. [[106_utf16|UTF-16]]
107. [[107_parity_bit|패리티 비트]] ([[107_parity_bit|Parity Bit]])
108. [[108_even_parity|짝수 패리티]] ([[108_even_parity|Even Parity]])
109. [[109_odd_parity|홀수 패리티]] ([[109_odd_parity|Odd Parity]])
110. [[110_hamming_distance|해밍 거리]] ([[110_hamming_distance|Hamming Distance]])
111. [[111_hamming_code|해밍 코드]] ([[111_hamming_code|Hamming Code]])
112. [[112_checksum|체크섬]] ([[112_checksum|Checksum]])
113. [[113_crc|CRC]] ([[113_crc|Cyclic Redundancy Check]])
114. [[114_big_endian|빅 엔디안]] ([[114_big_endian|Big-Endian]])
115. [[115_little_endian|리틀 엔디안]] ([[115_little_endian|Little-Endian]])
116. [[074_byte|바이트]] 오더링 ([[116_byte_ordering|Byte Ordering]])
117. [[117_alu|ALU]] (산술 [[369_logic_bomb|논리]] 연산 장치)
118. 가산기/[[037_subtractor|감산기]] [[369_logic_bomb|논리]]
119. [[119_shift_operations|시프트 연산]] (Shift)
120. [[120_logical_shift|논리 시프트]] ([[120_logical_shift|Logical Shift]])
121. [[121_arithmetic_shift|산술 시프트]] ([[121_arithmetic_shift|Arithmetic Shift]])
122. [[122_circular_shift|순환 시프트]] (Rotate)

## 3. 컴퓨터 구조 개론 및 [[282_performance_tactics|성능]] 평가 ([[319_architecture|Architecture]] Basics & [[282_performance_tactics|Performance]])
123. 컴퓨터의 4대 구성요소 (연산, 제어, 기억, 입출력)
124. [[124_von_neumann|폰 노이만 아키텍처]] ([[124_von_neumann|Von Neumann Architecture]])
125. 프로그램 내장 방식 ([[125_stored_program|Stored Program]] [[120_concept|Concept]])
126. [[126_harvard_architecture|하버드 아키텍처]] ([[126_harvard_architecture|Harvard Architecture]])
127. [[127_system_bus|시스템 버스]] ([[127_system_bus|System Bus]])
128. [[128_von_neumann_bottleneck|폰 노이만 병목현상]] ([[500_von_neumann_bottleneck|Von Neumann Bottleneck]])
129. [[129_microprocessor|마이크로프로세서]] ([[129_microprocessor|Microprocessor]])
130. [[130_microcontroller|마이크로컨트롤러]] ([[130_microcontroller|Microcontroller]], MCU)
131. [[131_soc|SoC]] ([[131_soc|System on Chip]])
132. [[132_clock_frequency|클럭 주파수]] ([[132_clock_frequency|Clock Frequency]])
133. [[133_clock_cycle_time|클럭 주기]] ([[133_clock_cycle_time|Clock Cycle Time]])
134. [[158_cpi_cost_performance_index|CPI]] ([[134_cpi|Cycles Per Instruction]])
135. [[117_ipc|IPC]] ([[135_ipc|Instructions Per Cycle]])
136. [[201_mips|MIPS]] (Million Instructions Per Second)
137. [[137_flops|FLOPS]] (Floating-point Operations Per Second)
138. [[138_response_time|응답 시간]] ([[138_response_time|Response Time]])
139. [[139_throughput|처리량]] ([[139_throughput|Throughput]])
140. [[140_bandwidth|대역폭]] ([[140_bandwidth|Bandwidth]])
141. [[141_latency|지연 시간]] ([[141_latency|Latency]])
142. [[142_performance_equation|컴퓨터 성능 방정식]] ([[142_performance_equation|Performance Equation]])
143. 암달의 법칙 (Amdahl's Law)
144. [[144_speedup|속도 향상도]] ([[144_speedup|Speedup]])
145. 구스타프슨의 법칙 (Gustafson's Law)
146. 무어의 법칙 (Moore's Law)
147. 황의 법칙 (Hwang's Law)
148. [[148_dennard_scaling|데나드 스케일링]] ([[148_dennard_scaling|Dennard Scaling]])
149. [[149_benchmark|벤치마크 프로그램]] ([[149_benchmark|Benchmark]])
150. SPEC 벤치마크
151. [[151_dhrystone|Dhrystone]]
152. [[152_whetstone|Whetstone]]
153. [[153_linpack|Linpack]]
154. [[154_tpc|TPC]] 벤치마크
155. [[155_dark_silicon|다크 실리콘]] ([[155_dark_silicon|Dark Silicon]])
156. [[156_power_performance_tradeoff|전력-성능 트레이드오프]]

## 4. [[158_instruction|명령어]] 집합 구조 ([[157_isa|ISA]], [[157_isa|Instruction Set Architecture]])
157. [[157_isa|ISA]] ([[157_isa|Instruction Set Architecture]])
158. [[158_instruction|명령어]] ([[158_instruction|Instruction]])
159. [[159_opcode|연산 코드]] ([[159_opcode|Opcode]])
160. [[160_operand|피연산자]] ([[160_operand|Operand]])
161. [[161_accumulator|누산기]] ([[161_accumulator|Accumulator]])
162. [[162_gpr|범용 레지스터]] ([[162_gpr|GPR]])
163. [[163_spr|특수 목적 레지스터]] ([[163_spr|SPR]])
164. [[164_pc|프로그램 카운터]] ([[164_pc|PC]])
165. [[165_ir|명령어 레지스터]] ([[165_ir|IR]])
166. [[166_sp|스택 포인터]] ([[166_sp|SP]])
167. [[167_status_register|상태 레지스터]] ([[167_status_register|Status Register]] / [[186_character_stuffing_dle_stx_etx|Flag]] [[175_register_addressing|Register]])
168. [[168_zero_flag|제로 플래그]] ([[168_zero_flag|Zero Flag]])
169. [[169_carry_flag|캐리 플래그]] ([[169_carry_flag|Carry Flag]])
170. [[170_instruction_format|명령어 형식]] ([[170_instruction_format|Instruction Format]])
171. [[171_fixed_length_instruction|고정 길이 명령어]]
172. [[172_variable_length_instruction|가변 길이 명령어]]
173. [[173_addressing_modes|주소 지정 방식]] ([[173_addressing_modes|Addressing Modes]])
174. [[174_immediate_addressing|즉시 주소 지정]] ([[174_immediate_addressing|Immediate]])
175. [[175_register_addressing|레지스터 주소 지정]] ([[175_register_addressing|Register]])
176. [[176_direct_addressing|직접 주소 지정]] ([[176_direct_addressing|Direct]])
177. [[177_indirect_addressing|간접 주소 지정]] ([[177_indirect_addressing|Indirect]])
178. [[057_register|레지스터]] [[177_indirect_addressing|간접 주소 지정]] ([[178_register_indirect_addressing|Register Indirect]])
179. [[179_displacement_addressing|변위 주소 지정]] ([[179_displacement_addressing|Displacement]])
180. 베이스 [[175_register_addressing|레지스터 주소 지정]] ([[329_base_register|Base Register]])
181. [[181_indexed_addressing|인덱스 주소 지정]] ([[181_indexed_addressing|Indexed]])
182. [[164_pc|PC]] 상대 주소 지정 ([[182_relative_addressing|PC-Relative]])
183. [[183_data_transfer_instructions|데이터 전송 명령어]]
184. [[184_arithmetic_instructions|산술 연산 명령어]]
185. [[185_logical_operations|논리 연산 명령어]]
186. [[186_control_flow_instructions|제어 흐름 명령어]] ([[186_control_flow_instructions|Control Flow]])
187. [[187_conditional_branch|조건부 분기]] ([[187_conditional_branch|Conditional Branch]])
188. [[188_unconditional_branch|무조건 분기]] ([[188_unconditional_branch|Unconditional Branch]])
189. [[189_subroutine_call_return|서브루틴 호출]] ([[189_subroutine_call_return|Call]]) 및 복귀 (Return)
190. [[190_stack_machine|스택 머신]] ([[190_stack_machine|Stack Machine]])
191. [[191_0_address_instruction|0-주소 명령어]]
192. [[192_1_address_instruction|1-주소 명령어]]
193. [[193_2_address_instruction|2-주소 명령어]]
194. [[194_3_address_instruction|3-주소 명령어]]
195. [[195_risc|RISC]] (Reduced [[158_instruction|Instruction]] Set Computer)
196. [[196_cisc|CISC]] (Complex [[158_instruction|Instruction]] Set Computer)
197. 로드/스토어 아키텍처 (Load/Store)
198. [[198_x86_architecture|x86 아키텍처]]
199. ARM 아키텍처
200. [[200_riscv|RISC-V]]
201. [[201_mips|MIPS]]
202. [[202_isa_extensions|명령어 집합 확장]] ([[202_isa_extensions|ISA Extensions]])
203. [[370_simd|SIMD]] [[158_instruction|명령어]] 확장 (AVX, NEON)

## 5. [[206_control_unit|제어 유닛]] 및 파이프라이닝 ([[206_control_unit|Control Unit]] & Pipelining)
204. [[204_microarchitecture|마이크로아키텍처]] ([[204_microarchitecture|Microarchitecture]])
205. [[205_datapath|데이터패스]] ([[205_datapath|Datapath]])
206. [[206_control_unit|제어 유닛]] ([[206_control_unit|Control Unit]])
207. [[207_instruction_cycle|명령어 사이클]] ([[207_instruction_cycle|Instruction Cycle]])
208. [[208_fetch_cycle|인출 사이클]] ([[208_fetch_cycle|Fetch Cycle]])
209. [[209_decode_cycle|해독 사이클]] ([[209_decode_cycle|Decode Cycle]])
210. [[210_execute_cycle|실행 사이클]] ([[210_execute_cycle|Execute Cycle]])
211. [[211_indirect_cycle|간접 사이클]] ([[211_indirect_cycle|Indirect Cycle]])
212. [[212_interrupt_cycle|인터럽트 사이클]] ([[212_interrupt_cycle|Interrupt Cycle]])
213. [[213_micro_operation|마이크로 오퍼레이션]] ([[213_micro_operation|Micro-operation]])
214. [[214_hardwired_control|하드와이어드 제어]] ([[214_hardwired_control|Hardwired Control]])
215. [[215_microprogrammed_control|마이크로프로그래밍]] ([[215_microprogrammed_control|Microprogrammed Control]])
216. [[216_control_memory|제어 메모리]] ([[216_control_memory|Control Memory]])
217. [[217_microinstruction|마이크로명령어]] ([[217_microinstruction|Microinstruction]])
218. [[218_instruction_pipelining|명령어 파이프라이닝]] ([[218_instruction_pipelining|Instruction Pipelining]])
219. [[219_pipeline_stages|파이프라인 단계]] (IF, ID, EX, MEM, WB)
220. [[220_pipeline_depth|파이프라인 깊이]] ([[220_pipeline_depth|Pipeline Depth]])
221. [[221_pipeline_hazards|파이프라인 해저드]] ([[221_pipeline_hazards|Pipeline Hazards]])
222. [[222_structural_hazard|구조적 해저드]] ([[222_structural_hazard|Structural Hazard]])
223. [[223_data_hazard|데이터 해저드]] ([[223_data_hazard|Data Hazard]])
224. [[224_control_hazard|제어 해저드]] ([[224_control_hazard|Control Hazard]] / Branch Hazard)
225. [[225_raw|RAW]] ([[225_raw|Read After Write]])
226. [[226_war|WAR]] ([[226_war|Write After Read]])
227. [[227_waw|WAW]] ([[227_waw|Write After Write]])
228. [[228_data_forwarding|데이터 포워딩]] ([[228_data_forwarding|Data Forwarding]] / Bypassing)
229. [[229_pipeline_stall|파이프라인 스톨]] ([[229_pipeline_stall|Pipeline Stall]] / Bubble)
230. 분기 [[015_지연_데이터_관점|지연]] ([[230_delayed_branch|Delayed Branch]])
231. [[231_branch_prediction|분기 예측]] ([[231_branch_prediction|Branch Prediction]])
232. [[232_static_prediction|정적 분기 예측]] ([[232_static_prediction|Static Prediction]])
233. [[233_dynamic_prediction|동적 분기 예측]] ([[233_dynamic_prediction|Dynamic Prediction]])
234. [[234_btb|분기 목적지 버퍼]] ([[234_btb|BTB]])
235. [[235_bht|분기 역사 표]] ([[235_bht|BHT]])
236. [[236_superscalar|수퍼스칼라]] ([[236_superscalar|Superscalar]])
237. [[237_issue_width|명령어 발급 폭]] ([[237_issue_width|Issue Width]])
238. [[238_out_of_order_execution|비순차 실행]] (Out-of-Order Execution, OoO)
239. [[239_register_renaming|레지스터 리네이밍]] ([[239_register_renaming|Register Renaming]])
240. [[240_reorder_buffer|재주문 버퍼]] (ROB, [[240_reorder_buffer|Reorder Buffer]])
241. [[241_reservation_station|예약역]] ([[241_reservation_station|Reservation Station]])
242. 토마술로 [[001_algorithm_definition|알고리즘]] (Tomasulo's [[001_algorithm_definition|Algorithm]])
243. [[243_vliw|VLIW]] (Very Long [[158_instruction|Instruction]] [[075_word|Word]])
244. [[244_epic|EPIC]] (Explicitly Parallel [[158_instruction|Instruction]] Computing)

## 6. [[252_memory_hierarchy|메모리 계층 구조]] 및 캐시 ([[252_memory_hierarchy|Memory Hierarchy]] & Cache)
245. [[252_memory_hierarchy|메모리 계층 구조]] ([[252_memory_hierarchy|Memory Hierarchy]])
246. [[253_locality_of_reference|참조의 지역성]] ([[253_locality_of_reference|Locality of Reference]])
247. [[247_temporal_locality|시간적 지역성]] ([[247_temporal_locality|Temporal Locality]])
248. [[248_spatial_locality|공간적 지역성]] ([[248_spatial_locality|Spatial Locality]])
249. [[249_sequential_locality|순차적 지역성]] ([[249_sequential_locality|Sequential Locality]])
250. [[250_sram|SRAM]] ([[250_sram|Static RAM]])
251. [[251_dram|DRAM]] ([[251_dram|Dynamic RAM]])
252. [[252_sdram|SDRAM]] ([[252_sdram|Synchronous DRAM]])
253. [[253_ddr_sdram|DDR SDRAM]] ([[253_ddr_sdram|Double Data Rate]])
254. [[254_memory_interleaving|메모리 인터리빙]] ([[254_memory_interleaving|Memory Interleaving]])
255. [[255_rom|ROM]] ([[255_rom|Read Only Memory]])
256. [[256_flash_memory|플래시 메모리]] ([[256_flash_memory|Flash Memory]])
257. NAND 플래시
258. NOR 플래시
259. [[259_cache_memory|캐시 메모리]] ([[259_cache_memory|Cache Memory]])
260. L1 캐시
261. L2 캐시
262. L3 캐시
263. [[263_cache_hit_miss|캐시 히트]] ([[263_cache_hit_miss|Hit]]) 및 미스 (Miss)
264. [[264_hit_ratio|적중률]] ([[359_effective_access_time|Hit Ratio]])
265. 평균 메모리 접근 시간 ([[265_amat|AMAT]])
266. [[266_cache_mapping|캐시 맵핑 방식]] ([[266_cache_mapping|Cache Mapping]])
267. [[267_direct_mapping|직접 사상]] ([[267_direct_mapping|Direct Mapping]])
268. [[268_fully_associative|완전 연관 사상]] ([[268_fully_associative|Fully Associative]])
269. [[269_set_associative_mapping|집합 연관 사상]] ([[269_set_associative_mapping|Set Associative Mapping]])
270. [[270_cache_miss_3c|캐시 미스의 원인]] (3C: Compulsory, Capacity, Conflict)
271. [[271_replacement_policy|캐시 교체 알고리즘]] ([[271_replacement_policy|Replacement Policy]])
272. [[262_lru_page_replacement|LRU]] ([[262_lru_page_replacement|Least Recently Used]])
273. [[263_lfu_page_replacement|LFU]] ([[263_lfu_page_replacement|Least Frequently Used]])
274. [[261_fifo_page_replacement|FIFO]] (First In First Out)
275. [[275_write_policy|캐시 쓰기 정책]] ([[275_write_policy|Write Policy]])
276. [[276_write_through|Write-Through]] ([[276_write_through|동시 쓰기]])
277. [[277_write_back|Write-Back]] ([[277_write_back|나중 쓰기]])
278. [[278_dirty_bit|더티 비트]] ([[396_dirty_bit|Dirty Bit]])
279. [[158_instruction|명령어]] 캐시와 [[001_dikw_pyramid|데이터]] 캐시 분리 ([[279_split_cache|Split Cache]])
280. 프리패칭 ([[280_prefetching|Prefetching]])
281. 희생 캐시 ([[281_victim_cache|Victim Cache]])

## 7. [[381_virtual_memory|가상 메모리]] 및 OS 메모리 관리 ([[381_virtual_memory|Virtual Memory]] & OS Integration)
282. [[381_virtual_memory|가상 메모리]] ([[381_virtual_memory|Virtual Memory]])
283. [[323_physical_address|물리 주소]] ([[323_physical_address|Physical Address]])와 [[322_logical_virtual_address|논리 주소]] (Logical Address)
284. [[328_mmu|MMU]] ([[284_mmu|Memory Management Unit]])
285. [[259_paging|페이징]] ([[259_paging|Paging]])
286. [[286_page_frame|페이지]] ([[286_page_frame|Page]])와 프레임 (Frame)
287. [[341_internal_fragmentation|내부 단편화]] ([[341_internal_fragmentation|Internal Fragmentation]])
288. [[353_page_table|페이지 테이블]] ([[353_page_table|Page Table]])
289. [[289_multilevel_page_table|다단계 페이지 테이블]]
290. [[363_inverted_page_table|역 페이지 테이블]] ([[363_inverted_page_table|Inverted Page Table]])
291. [[357_tlb|TLB]] ([[291_tlb|Translation Lookaside Buffer]])
292. [[357_tlb|TLB]] 히트 및 미스
293. [[364_segmentation|세그멘테이션]] ([[364_segmentation|Segmentation]])
294. [[365_segment_table|세그먼트 테이블]]
295. [[342_external_fragmentation|외부 단편화]] ([[342_external_fragmentation|External Fragmentation]])
296. [[296_paging_segmentation_hybrid|페이징과 세그멘테이션 혼용]] 기법
297. [[255_demand_paging|요구 페이징]] ([[255_demand_paging|Demand Paging]])
298. [[387_page_fault|페이지 부재]] ([[387_page_fault|Page Fault]])
299. [[720_page_fault_isr|페이지 폴트]] 처리 과정
300. [[401_page_replacement_algorithms|페이지 교체 알고리즘]] ([[260_page_replacement|Page Replacement]])
301. [[724_optimal_page_replacement_unrealizable|OPT]] ([[301_opt_replacement|최적 교체]])
302. [[264_clock_algorithm_nur|클럭 알고리즘]] ([[302_clock_algorithm|Clock Algorithm]])
303. [[303_nur|NUR]] ([[303_nur|Not Used Recently]])
304. [[257_thrashing|스래싱]] ([[257_thrashing|Thrashing]])
305. [[265_working_set|워킹 셋]] ([[265_working_set|Working Set]]) 모델
306. [[306_pff|PFF]] ([[266_page_fault_frequency|Page Fault Frequency]])
307. [[307_memory_protection|메모리 보호]] ([[307_memory_protection|Memory Protection]])
308. [[131_mmap_ipc|메모리 맵 파일]] ([[308_memory_mapped_file|Memory-Mapped File]])

## 8. 입출력 및 스토리지 시스템 (I/O & Storage Systems)
309. [[309_io_controller|입출력 모듈]] (I/O [[192_module_independence|Module]])
310. 메모리 맵 I/O (Memory-Mapped I/O)
311. 분리형 I/O (Isolated I/O)
312. 프로그램 제어 I/O (Programmed I/O)
313. [[448_polling_programmed_io|폴링]] ([[747_io_polling_overhead|Polling]])
314. [[016_interrupt_mechanism|인터럽트]] 구동 I/O ([[016_interrupt_mechanism|Interrupt]]-driven I/O)
315. [[016_interrupt_mechanism|인터럽트]] ([[016_interrupt_mechanism|Interrupt]])
316. [[019_interrupt_vector|인터럽트 벡터]] ([[019_interrupt_vector|Interrupt Vector]])
317. [[020_isr|ISR]] ([[317_isr|Interrupt Service Routine]])
318. [[746_io_direct_memory_access_dma|DMA]] ([[318_dma|Direct Memory Access]])
319. [[451_cycle_stealing|사이클 스틸링]] ([[451_cycle_stealing|Cycle Stealing]])
320. [[320_burst_mode|버스트 모드]] ([[320_burst_mode|Burst Mode]])
321. [[321_iop_channel|IOP]] (I/O Processor / Channel)
322. [[465_hdd_structure|하드 디스크 드라이브]] ([[465_hdd_structure|HDD]])
323. 트랙, 섹터, 실린더
324. [[324_seek_time|탐색 시간]] ([[467_disk_access_time|Seek Time]])
325. [[325_rotational_latency|회전 지연]] ([[325_rotational_latency|Rotational Latency]])
326. [[326_transfer_time|전송 시간]] ([[326_transfer_time|Transfer Time]])
327. [[327_ssd|SSD]] ([[327_ssd|Solid State Drive]])
328. [[380_garbage_collection|가비지 컬렉션]] ([[380_garbage_collection|Garbage Collection]] in [[327_ssd|SSD]])
329. [[479_wear_leveling|마모 평준화]] ([[479_wear_leveling|Wear Leveling]])
330. [[478_ftl_flash_translation_layer|FTL]] ([[478_ftl_flash_translation_layer|Flash Translation Layer]])
331. [[483_raid_overview|RAID]] (Redundant [[055_array|Array]] of Independent Disks)
332. [[484_raid_0_striping|RAID 0]] ([[332_raid_0|스트라이핑]])
333. [[485_raid_1_mirroring|RAID 1]] ([[333_raid_1|미러링]])
334. [[487_raid_5_distributed_parity|RAID 5]] ([[334_raid_5|분산 패리티]])
335. [[488_raid_6_dual_parity|RAID 6]] ([[335_raid_6|이중 패리티]])
336. [[489_raid_10_hybrid|RAID 10]] / 01
337. [[493_san_storage_area_network|SAN]] ([[493_san_storage_area_network|Storage Area Network]])
338. [[492_nas_network_attached_storage|NAS]] ([[492_nas_network_attached_storage|Network Attached Storage]])
339. [[339_das|DAS]] ([[339_das|Direct Attached Storage]])
340. SCSI 및 SAS ([[340_scsi_sas|Serial Attached SCSI]])
341. [[341_sata|SATA]] ([[341_sata|Serial ATA]])
342. [[482_nvme|NVMe]] ([[482_nvme|Non-Volatile Memory Express]])
343. [[499_nvme_over_fabrics|NVMe-oF]] ([[499_nvme_over_fabrics|NVMe over Fabrics]])

## 9. [[127_system_bus|시스템 버스]] 및 고속 인터커넥트 ([[127_system_bus|System Bus]] & Interconnects)
344. [[344_bus|버스]] ([[344_bus|Bus]])
345. [[345_data_bus|데이터 버스]] ([[345_data_bus|Data Bus]])
346. [[346_address_bus|주소 버스]] ([[346_address_bus|Address Bus]])
347. [[347_control_bus|제어 버스]] ([[347_control_bus|Control Bus]])
348. [[348_synchronous_bus|동기식 버스]] ([[348_synchronous_bus|Synchronous Bus]])
349. [[349_asynchronous_bus|비동기식 버스]] ([[349_asynchronous_bus|Asynchronous Bus]])
350. [[350_bus_master|버스 마스터]] ([[350_bus_master|Bus Master]])
351. [[351_bus_arbitration|버스 중재]] ([[351_bus_arbitration|Bus Arbitration]])
352. [[352_centralized_arbitration|중앙 집중식 중재]]
353. [[353_distributed_arbitration|분산식 중재]]
354. [[354_daisy_chain|데이지 체인]] ([[354_daisy_chain|Daisy Chain]])
355. [[355_pci|PCI]] ([[355_pci|Peripheral Component Interconnect]])
356. [[356_pcie|PCIe]] ([[356_pcie|PCI Express]])
357. [[356_pcie|PCIe]] 레인 (Lanes - x1, x4, x8, x16)
358. [[356_pcie|PCIe]] 루트 컴플렉스 ([[358_root_complex|Root Complex]])
359. [[359_usb|USB]] ([[359_usb|Universal Serial Bus]])
360. [[360_thunderbolt|Thunderbolt]]
361. [[361_infiniband|인피니밴드]] ([[361_infiniband|InfiniBand]])
362. [[639_rdma_kernel_bypass|RDMA]] (Remote [[318_dma|Direct Memory Access]])
363. [[523_roce|RoCE]] ([[639_rdma_kernel_bypass|RDMA]] over Converged [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]])
364. [[364_northbridge_southbridge|노스브리지]] ([[364_northbridge_southbridge|Northbridge]])와 사우스브리지 (Southbridge)
365. [[365_fsb|프론트 사이드 버스]] ([[365_fsb|FSB]])
366. [[366_on_chip_bus|온칩 버스]] (AMBA, AXI, AHB, APB)
367. [[367_noc|NoC]] ([[367_noc|Network on Chip]])

## [[489_raid_10_hybrid|10]]. [[430_index_fast_full_scan|병렬]] 처리 아키텍처 (Parallel Processing [[319_architecture|Architecture]])
368. 플린의 [[104_classification_analysis|분류]]법 (Flynn's Taxonomy)
369. [[369_sisd|SISD]] (단일 [[158_instruction|명령어]] 단일 [[001_dikw_pyramid|데이터]])
370. [[370_simd|SIMD]] (단일 [[158_instruction|명령어]] 다중 [[001_dikw_pyramid|데이터]])
371. [[371_misd|MISD]]
372. [[372_mimd|MIMD]] (다중 [[158_instruction|명령어]] 다중 [[001_dikw_pyramid|데이터]])
373. [[373_vector_processor|벡터 프로세서]] ([[373_vector_processor|Vector Processor]])
374. [[374_array_processor|배열 프로세서]] ([[374_array_processor|Array Processor]])
375. [[375_multiprocessor|다중 프로세서]] ([[375_multiprocessor|Multiprocessor]])
376. [[376_multicomputer|다중 컴퓨터]] ([[376_multicomputer|Multicomputer]])
377. [[377_shared_memory|공유 메모리 시스템]] ([[118_shared_memory|Shared Memory]])
378. [[378_distributed_memory|분산 메모리 시스템]] ([[378_distributed_memory|Distributed Memory]])
379. [[379_uma|UMA]] ([[379_uma|Uniform Memory Access]])
380. [[377_numa_allocation|NUMA]] ([[377_numa_allocation|Non-Uniform Memory Access]])
381. [[381_coma|COMA]] ([[381_coma|Cache-Only Memory Access]])
382. [[382_smp|대칭형 다중 처리]] ([[195_real_time_scheduling|SMP]], Symmetric Multiprocessing)
383. [[383_cluster_computing|클러스터 컴퓨팅]] ([[383_cluster_computing|Cluster Computing]])
384. [[051_grid_computing|그리드 컴퓨팅]] ([[051_grid_computing|Grid Computing]])
385. [[385_tlp|스레드 레벨 병렬성]] ([[385_tlp|TLP]], [[092_thread_lwp|Thread]]-Level Parallelism)
386. [[386_dlp|데이터 레벨 병렬성]] ([[386_dlp|DLP]])
387. [[387_interconnection_network|상호 연결망]] ([[387_interconnection_network|Interconnection Network]])
388. [[388_crossbar_switch|크로스바 스위치]] ([[388_crossbar_switch|Crossbar Switch]])
389. [[389_mesh_topology|메시]] ([[389_mesh_topology|Mesh]]) 토폴로지
390. [[390_torus|토러스]] ([[390_torus|Torus]])
391. [[391_hypercube|하이퍼큐브]] ([[391_hypercube|Hypercube]])
392. [[392_multistage_interconnection_network|다단 연결망]] (MIN, [[392_multistage_interconnection_network|Multistage Interconnection Network]])

## [[308_static_dynamic_nat_pat_port_address_translation|11]]. 멀티코어 및 [[212_synchronization_mechanisms|동기화]] (Multi-core & [[212_synchronization_mechanisms|Synchronization]])
393. [[393_multicore_processor|멀티코어 프로세서]] ([[393_multicore_processor|Multi-core Processor]])
394. [[394_cmp|CMP]] ([[394_cmp|Chip Multi-Processor]])
395. [[395_heterogeneous_multicore|이기종 멀티코어]] ([[395_heterogeneous_multicore|Heterogeneous Multi-core]])
396. big.LITTLE 아키텍처
397. [[397_multithreading|멀티스레딩]] ([[095_multithreading_benefits|Multithreading]])
398. [[398_coarse_grained_multithreading|거친 멀티스레딩]] ([[398_coarse_grained_multithreading|Coarse-grained]])
399. [[399_fine_grained_multithreading|세밀한 멀티스레딩]] ([[399_fine_grained_multithreading|Fine-grained]])
400. [[400_smt|동시 멀티스레딩]] ([[400_smt|SMT]], Simultaneous [[095_multithreading_benefits|Multithreading]])
401. [[199_interrupt_scheduling|하이퍼스레딩]] ([[199_interrupt_scheduling|Hyper-Threading]])
402. [[402_cache_coherence|캐시 일관성]] ([[402_cache_coherence|Cache Coherence]])
403. [[403_snooping_protocol|스누핑 프로토콜]] ([[403_snooping_protocol|Snooping Protocol]])
404. [[404_directory_based_protocol|디렉터리 기반 프로토콜]] ([[404_directory_based_protocol|Directory-based Protocol]])
405. [[405_write_invalidate|무효화 정책]] ([[405_write_invalidate|Write-Invalidate]])
406. [[406_write_update|갱신 정책]] ([[406_write_update|Write-Update]])
407. MESI [[295_protocol_field_tcp_udp_icmp|프로토콜]] (Modified, Exclusive, Shared, Invalid)
408. MOESI [[295_protocol_field_tcp_udp_icmp|프로토콜]]
409. [[409_false_sharing|거짓 공유]] ([[409_false_sharing|False Sharing]])
410. [[410_memory_consistency_model|메모리 일관성 모델]] ([[410_memory_consistency_model|Memory Consistency Model]])
411. [[411_sequential_consistency|순차적 일관성]] ([[411_sequential_consistency|Sequential Consistency]])
412. [[412_relaxed_consistency|완화된 일관성]] ([[412_relaxed_consistency|Relaxed Consistency]])
413. [[413_hardware_synchronization|하드웨어 동기화]] ([[413_hardware_synchronization|Hardware Synchronization]])
414. Test-and-Set 연산
415. [[415_compare_and_swap|Compare-and-Swap]] ([[768_cas_compare_and_swap_lock_free|CAS]]) 연산
416. [[416_memory_barrier|메모리 배리어]] ([[416_memory_barrier|Memory Barrier]] / Fence)

## 12. 차세대 가속기 및 [[190_ai_llm_requirements_specification|AI]] [[009_semiconductor|반도체]] (Accelerators & [[190_ai_llm_requirements_specification|AI]] Hardware)
417. [[417_hardware_accelerator|하드웨어 가속기]] ([[417_hardware_accelerator|Hardware Accelerator]])
418. [[418_gpu|GPU]] ([[418_gpu|Graphics Processing Unit]])
419. [[419_gpgpu|GPGPU]] ([[419_gpgpu|General-Purpose GPU]])
420. [[420_cuda|CUDA]] (Compute Unified Device [[319_architecture|Architecture]])
421. [[421_streaming_multiprocessor|스트리밍 멀티프로세서]] ([[421_streaming_multiprocessor|SM]])
422. [[422_thread_block_and_warp|스레드 블록]] ([[422_thread_block_and_warp|Thread Block]])과 워프 (Warp)
423. [[423_simt|SIMT]] (Single [[158_instruction|Instruction]] Multiple Threads)
424. [[424_npu|NPU]] ([[424_npu|Neural Processing Unit]])
425. [[425_tpu|TPU]] ([[425_tpu|Tensor Processing Unit]])
426. [[426_systolic_array|시스톨릭 어레이]] ([[426_systolic_array|Systolic Array]])
427. [[427_tensor_core|텐서 코어]] ([[427_tensor_core|Tensor Core]])
428. [[673_mac_message_authentication_code|MAC]] 연산 ([[428_mac_operation|Multiply-Accumulate]])
429. [[429_dla|DLA]] ([[429_dla|Deep Learning Accelerator]])
430. [[430_pim|PIM]] ([[430_pim|Processing-In-Memory]])
431. [[431_pnm|PNM]] ([[431_pnm|Processing-Near-Memory]])
432. [[432_cim|CIM]] ([[432_cim|Computing-In-Memory]])
433. [[433_memory_wall|메모리 월]] ([[433_memory_wall|Memory Wall]])
434. [[434_quantization|양자화]] ([[434_quantization|Quantization]], INT8, INT4)
435. [[435_pruning_hardware|가지치기]] ([[435_pruning_hardware|Pruning]]) 지원 하드웨어
436. [[436_dpu|DPU]] ([[229_dpu_ipu_infrastructure_accelerator_offloading|Data Processing Unit]] / SmartNIC)
437. [[437_ipu|IPU]] ([[437_ipu|Intelligence Processing Unit]])
438. [[438_lpu|LPU]] ([[317_lpu_language_processing_unit|Language Processing Unit]], [[263_llm_large_language_model|LLM]] 가속기)
439. [[439_heterogeneous_computing|이기종 컴퓨팅]] ([[439_heterogeneous_computing|Heterogeneous Computing]])
440. [[440_offloading|오프로딩]] ([[440_offloading|Offloading]])
441. [[441_cxl|CXL]] ([[441_cxl|Compute Express Link]])
442. [[442_memory_pooling|메모리 풀링]] ([[442_memory_pooling|Memory Pooling]])
443. [[443_ucie|UCIe]] (Universal [[497_chiplet|Chiplet]] Interconnect Express)
444. NVLink / NVSwitch
445. [[445_neuromorphic_computing|뉴로모픽 컴퓨팅]] ([[445_neuromorphic_computing|Neuromorphic Computing]])
446. [[446_snn|스파이킹 신경망]] ([[446_snn|SNN]])
447. [[447_quantum_computer|양자 컴퓨터]] ([[447_quantum_computer|Quantum Computer]]) 기초
448. [[448_qubit|큐비트]] ([[448_qubit|Qubit]])

## 13. 고신뢰성 보장 및 전력 관리 ([[345_reliability_security|Reliability]] & [[069_type_1_2_error_statistical_power|Power]] [[372_management|Management]])
449. [[449_ras|RAS]] ([[345_reliability_security|Reliability]], [[452_availability|Availability]], Serviceability)
450. [[450_mtbf|MTBF]] ([[450_mtbf|평균 무고장 시간]])
451. [[451_mttr|MTTR]] ([[451_mttr|평균 수리 시간]])
452. [[452_availability|가용성]] ([[452_availability|Availability]])
453. [[453_fault_tolerance|고장 허용 시스템]] ([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]])
454. [[454_spof|단일 장애점]] ([[454_spof|SPOF]], Single Point of Failure)
455. [[455_tmr|TMR]] (Triple Modular Redundancy, 삼중 [[192_module_independence|모듈]] 중복)
456. [[456_dual_redundancy|이중화]] ([[456_dual_redundancy|Dual Redundancy]])
457. [[457_hot_standby|핫 스탠바이]] ([[457_hot_standby|Hot Standby]])
458. [[458_cold_standby|콜드 스탠바이]] ([[458_cold_standby|Cold Standby]])
459. [[459_fail_safe|페일 세이프]] ([[459_fail_safe|Fail-Safe]])
460. [[460_fail_soft|페일 소프트]] ([[460_fail_soft|Fail-Soft]])
461. [[461_watchdog_timer|워치독 타이머]] ([[461_watchdog_timer|Watchdog Timer]])
462. [[462_soft_error_hard_error|소프트 에러]] ([[462_soft_error_hard_error|Soft Error]])와 하드 에러 (Hard Error)
463. [[554_ecc_circuit|ECC]] 메모리 ([[463_ecc_memory|Error-Correcting Code]])
464. [[464_memory_mirroring|메모리 미러링]] ([[464_memory_mirroring|Memory Mirroring]])
465. [[465_lockstep_architecture|락스텝]] ([[465_lockstep_architecture|Lockstep]]) 아키텍처
466. [[466_power_consumption|전력 소모]] ([[466_power_consumption|Power Consumption]])
467. [[467_dynamic_power|동적 전력]] ([[467_dynamic_power|Dynamic Power]])
468. [[468_static_power|정적 전력]] ([[468_static_power|Static Power]] / 누설 전력)
469. [[469_dvfs|DVFS]] (동적 [[001_voltage|전압]] 및 주파수 [[249_scaling_normalization_standardization|스케일링]])
470. [[470_clock_gating|클럭 게이팅]] ([[470_clock_gating|Clock Gating]])
471. [[471_power_gating|전력 게이팅]] ([[471_power_gating|Power Gating]])
472. 열 설계 전력 (TDP, Thermal Design [[069_type_1_2_error_statistical_power|Power]])
473. [[473_thermal_throttling|서멀 스로틀링]] ([[473_thermal_throttling|Thermal Throttling]])
474. [[474_energy_proportional_computing|에너지 비례 컴퓨팅]] ([[474_energy_proportional_computing|Energy Proportional Computing]])

## 14. 최신 하드웨어 보안 및 트렌드 (Hardware [[283_security_tactics|Security]] & Trends)
475. [[475_hsm|하드웨어 보안 모듈]] ([[475_hsm|HSM]])
476. [[476_tpm|TPM]] ([[476_tpm|Trusted Platform Module]])
477. [[608_secure_boot|보안 부팅]] ([[608_secure_boot|Secure Boot]])
478. [[478_tee|신뢰 실행 환경]] ([[478_tee|TEE]], [[972_tee_based_ml|Trusted Execution Environment]])
479. [[479_arm_trustzone|ARM TrustZone]]
480. [[480_intel_sgx|Intel SGX]]
481. [[481_side_channel_attack|사이드 채널 공격]] ([[481_side_channel_attack|Side-channel Attack]])
482. [[482_meltdown|멜트다운]] ([[482_meltdown|Meltdown]])
483. [[483_spectre|스펙터]] ([[483_spectre|Spectre]])
484. [[484_rowhammer|로우해머 공격]] ([[484_rowhammer|Rowhammer]])
485. 물리적 [[016_replication_factor|복제]] 방지 기능 ([[485_puf|PUF]])
486. [[486_trng|난수 생성기]] ([[669_hardware_trng_kernel_entropy_pool|TRNG]])
487. [[487_root_of_trust|루트 오브 트러스트]] ([[487_root_of_trust|Root of Trust]])
488. [[488_smm|시스템 관리 모드]] ([[488_smm|SMM]])
489. [[489_fhe_accelerator|동형 암호 가속기]] ([[489_fhe_accelerator|FHE Accelerator]])
490. [[490_edge_computing_hw|엣지 컴퓨팅 하드웨어]] ([[490_edge_computing_hw|Edge Computing HW]])
491. [[491_fog_computing_hw|포그 컴퓨팅 하드웨어]]
492. [[492_cloud_native_processor|클라우드 네이티브 프로세서]] (ARM Neoverse 등)
493. [[493_scm_pram_mram|차세대 비휘발성 메모리]] ([[167_scm_software_configuration_management|SCM]]: PRAM, MRAM, ReRAM)
494. [[494_optane_memory|옵테인 메모리]] ([[494_optane_memory|3D XPoint]])
495. [[495_hbm|HBM]] ([[495_hbm|High Bandwidth Memory]])
496. [[496_tsv|TSV]] (Through-Silicon Via, 실리콘 관통 전극)
497. [[497_chiplet|칩렛]] ([[497_chiplet|Chiplet]]) 아키텍처
498. 2.5D 및 3D 패키징 기술
499. [[499_sdi_hardware_dependency|소프트웨어 정의 인프라]] ([[499_sdi_hardware_dependency|SDI]]) 하드웨어 [[008_dependencies|종속성]]

## 15. 심화 토픽 및 추가 주요 용어 (기술사 논술/단답형 빈출 보충)
500. 폰 노이만 병목 개선 기법
501. [[501_superscalar_issue_queue|수퍼스칼라 발급 큐]]
502. [[502_ooo_window|비순차 실행 윈도우]]
503. [[231_branch_prediction|분기 예측]] 실패 페널티
504. [[504_cache_way_prediction|캐시 웨이 예측]]
505. [[505_cache_line_prefetch|캐시 라인 프리패치]]
506. [[506_ooo_memory_access|비순차 메모리 접근]]
507. [[507_memory_dependence_predictor|메모리 의존성 예측기]]
508. [[508_load_store_queue|로드-스토어 큐]] (LSQ)
509. [[509_register_file_ports|레지스터 파일 포트]]
510. 스누핑 [[344_bus|버스]] 병목 현상
511. [[511_directory_cache|디렉터리 캐시]]
512. [[389_mesh_topology|메시]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 상태 전이도
513. [[513_htm|트랜잭셔널 메모리]] ([[513_htm|HTM]])
514. [[268_software_transactional_memory|소프트웨어 트랜잭셔널 메모리]] ([[268_software_transactional_memory|STM]])
515. 작업 스케줄링 하드웨어 지원
516. 이종 컴퓨팅 메모리 공유
517. [[371_huge_pages|거대 페이지]] ([[517_huge_page|Huge Page]])
518. [[357_tlb|TLB]] 슈팅다운
519. [[627_iommu_dma_isolation|IOMMU]] [[282_performance_tactics|성능]] 오버헤드
520. [[356_pcie|PCIe]] [[238_switch_operation_principles|스위치]] 패브릭
521. [[482_nvme|NVMe]] 오버 패브릭 ([[499_nvme_over_fabrics|NVMe-oF]])
522. [[361_infiniband|인피니밴드]] [[639_rdma_kernel_bypass|RDMA]]
523. [[523_roce|RoCE]] ([[639_rdma_kernel_bypass|RDMA]] over Converged [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]])
524. [[524_scm_tiering|스토리지 클래스 메모리]] ([[167_scm_software_configuration_management|SCM]]) 계층화
525. 메인 메모리 [[347_compaction|압축]] 기술
526. 비휘발성 메모리 [[479_wear_leveling|마모 평준화]]
527. [[527_hardware_assisted_virtualization|가상화 오버헤드 감소]] ([[527_hardware_assisted_virtualization|하드웨어 보조]])
528. [[497_sr_iov_pcie_mapping|SR-IOV]] (Single Root I/O [[190_virtualization_computing_architecture_cloud|Virtualization]])
529. 가상 머신 제어 구조 ([[529_vmcs|VMCS]])
530. [[530_hypervisor_trap|하이퍼바이저 트랩]]
531. [[531_emulation_latency|에뮬레이션 지연]]
532. [[532_dynamic_thermal_management|동적 써멀 관리]] ([[532_dynamic_thermal_management|DTM]])
533. [[156_power_performance_tradeoff|전력-성능 트레이드오프]] 파레토 곡선
534. [[534_more_than_moore|무어의 법칙 이후]] ([[534_more_than_moore|More than Moore]])
535. [[535_system_in_package|시스템 온 패키지]] ([[535_system_in_package|SiP]])
536. [[536_llvm_ir|LLVM IR]] 변환 (컴파일러-HW 인터페이스)
537. [[537_auto_vectorization|오토 벡터라이제이션]] ([[537_auto_vectorization|Auto-vectorization]])
538. [[538_loop_unrolling|루프 언롤링]] ([[538_loop_unrolling|Loop Unrolling]])
539. [[539_loop_tiling|루프 타일링]] ([[539_loop_tiling|Loop Tiling]])
540. [[591_buffer_overflow|버퍼 오버플로우]] 하드웨어 방어 ([[540_intel_cet|Intel CET]] 등)
541. [[541_stack_smashing_protector|스택 스매싱 프로텍터]]
542. [[542_pointer_authentication|포인터 인증]] ([[542_pointer_authentication|Pointer Authentication]], ARM PAC)
543. [[183_post_quantum_cryptography_key_transition|양자 내성 암호]] 가속기
544. [[544_secure_context_switching|안전한 컨텍스트 스위칭]]
545. [[545_interrupt_latency|인터럽트 지연 시간]] ([[545_interrupt_latency|Interrupt Latency]]) 최소화
546. [[546_tsn_hardware|결정론적 이더넷]] ([[546_tsn_hardware|TSN]]) 하드웨어
547. [[547_rtos_timer|실시간 시스템 타이머]]
548. [[548_automotive_hpc|자율주행용 고성능 컴퓨터]] ([[548_automotive_hpc|HPC]])
549. ADAS [[139_sensor_fusion_camera_lidar_radar|센서 퓨전]] 가속기
550. [[166_smart_factory|스마트 팩토리]] 엣지 게이트웨이 HW
551. 비디오 코덱 하드웨어 가속 (H.265/AV1)
552. 이미지 센서 [[101_isp_information_strategy_planning_4_steps|ISP]] ([[552_isp|Image Signal Processor]])
553. [[148_5g_embb_urllc_mmtc|초고속]] [[553_serdes|SerDes]]
554. [[158_error_correcting_codes|오류 정정 부호]] ([[554_ecc_circuit|ECC]]) 회로
555. [[555_memory_scrubbing|메모리 스크러빙]] ([[555_memory_scrubbing|Memory Scrubbing]])
556. [[462_soft_error_hard_error|소프트 에러]] [[658_ir_recovery|복구]] 매커니즘
557. [[032_firmware|펌웨어]] OTA 하드웨어 지원
558. [[558_nmi|NMI]] ([[558_nmi|Non-Maskable Interrupt]])
559. [[559_vic_nvic|벡터형 인터럽트 컨트롤러]] (VIC, NVIC)
560. [[560_multicore_interrupt_routing|멀티코어 인터럽트 라우팅]] (GIC, APIC)
561. [[561_msi|MSI]] ([[561_msi|Message Signaled Interrupts]])
562. [[562_burst_bus_transaction|버스트 버스 트랜잭션]]
563. [[563_split_transaction_bus|분리 트랜잭션 버스]] ([[563_split_transaction_bus|Split Transaction]])
564. 비동기 [[344_bus|버스]] 핸드셰이크 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
565. [[389_mesh_topology|메시]]지 패싱 하드웨어 큐
566. [[566_hardware_lock_elision|하드웨어 락 엘리전]] (HLE)
567. [[567_atomic_rmw|원자적 읽기-수정-쓰기]] (RMW)
568. ABA 문제 ([[212_synchronization_mechanisms|동기화]] 이슈)
569. 멀티코어 칩 온도 불균형 ([[569_thermal_gradient_dark_silicon|Thermal Gradient]])
570. [[570_stp_vs_mtp|단일 스레드 성능]] ([[570_stp_vs_mtp|STP]]) vs [[095_multithreading_benefits|다중 스레드]] [[282_performance_tactics|성능]] (MTP)
571. [[571_instruction_prefetch_buffer|명령어 프리패치 버퍼]]
572. [[572_loop_prefetcher|루프 프리패처]]
573. [[573_stream_prefetcher|스트림 프리패처]]
574. [[335_swapping|스와핑]] ([[335_swapping|Swapping]]) 메커니즘
575. [[382_virtual_address_space|가상 주소 공간]] 분리
576. [[374_aslr|ASLR]] 하드웨어 기반 우회 방어
577. [[577_branch_target_injection|분기 목표 주입]] ([[577_branch_target_injection|Branch Target Injection]])
578. [[022_kernel_role|커널]] [[353_page_table|페이지 테이블]] 격리 ([[578_kpti|KPTI]])
579. 간접 분기 추측 제어 ([[579_ibpb|IBPB]])
580. [[580_retpoline|Retpoline]] ([[580_retpoline|Return Trampoline]])
581. 마이크로코드 보안 패치 원리
582. [[582_hardware_obfuscation|하드웨어 기반 난독화]]
583. [[001_dikw_pyramid|데이터]] [[140_bandwidth|대역폭]] [[347_compaction|압축]] 인코딩
584. 딥러닝 텐서 희소성 (Sparsity) [[040_encoder|인코더]]
585. 영([[585_zero_skipping|Zero]]) [[001_dikw_pyramid|데이터]] 건너뛰기 로직 ([[585_zero_skipping|Zero]]-skipping)
586. [[586_fpu_multiplier_pipeline|부동소수점 곱셈기 파이프라인]]
587. [[587_nic_offloading|네트워크 인터페이스 카드]] ([[587_nic_offloading|NIC]]) [[440_offloading|오프로딩]]
588. [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 오프로드 엔진 ([[588_toe|TOE]])
589. [[589_ipsec_offload|IPsec]] 오프로드 가속기
590. [[590_vswitch_offload|가상 스위치 오프로드]] ([[590_vswitch_offload|vSwitch Offload]])
591. 패킷 [[104_classification_analysis|분류]] [[001_algorithm_definition|알고리즘]] ([[591_tcam_packet_classification|TCAM]] 기반)
592. 오픈 채널 [[327_ssd|SSD]] 구조
593. [[593_zoned_storage|존 스토리지]] ([[593_zoned_storage|Zoned Storage]])
594. [[594_kv_ssd|키-밸류 스토리지]] (KV-[[327_ssd|SSD]])
595. 스마트 [[327_ssd|SSD]] (연산 기능 포함)
596. [[498_computational_storage|컴퓨테이셔널 스토리지]] ([[498_computational_storage|Computational Storage]])
597. [[597_slc_caching|SLC]] [[456_caching|캐싱]] ([[597_slc_caching|SLC Caching]]) 기법
598. 가상 머신 마이그레이션 네트워크 칩
599. [[001_dikw_pyramid|데이터]] 방향성 패브릭 ([[599_data_centric_fabric|Data-centric Fabric]])
600. 엑사스케일 컴퓨팅 노드 보드
601. [[601_liquid_cooling|액체 냉각 시스템]] ([[601_liquid_cooling|Liquid Cooling]])
602. [[602_immersion_cooling|이머전 쿨링]] ([[602_immersion_cooling|Immersion Cooling]])
603. [[603_software_defined_accelerator|소프트웨어 정의 엑셀러레이터]]
604. 오픈 소스 IP 코어
605. [[605_high_level_synthesis|고수준 합성]] (HLS, High-Level Synthesis)
606. [[606_dynamic_partial_reconfiguration|FPGA]] 동적 재구성 (Dynamic Reconfiguration)
607. [[607_clock_domain_crossing|클럭 도메인 교차]] ([[217_cdc_binlog_change_capture_debezium|CDC]], [[607_clock_domain_crossing|Clock Domain Crossing]])
608. 비동기식 [[261_fifo_page_replacement|FIFO]] 버퍼
609. [[609_single_event_latchup|단일 이벤트 래치업]] (SEL)
610. 보안 [[667_hash_function_integrity_one_way|해시 함수]] 회로 ([[101_sha_3|SHA-3]] / [[101_sha_3|Keccak]])
611. [[611_distributed_arithmetic|분산 산술]] ([[611_distributed_arithmetic|Distributed Arithmetic]]) 매크로
612. [[161_matrix_decomposition|행렬 분해]] (LU, QR) 전용 [[430_index_fast_full_scan|병렬]] 구조
613. [[613_graph_bfs_memory|그래프 탐색]] ([[035_bfs|BFS]]/[[034_dfs|DFS]]) 전용 메모리 서브시스템
614. [[286_page_frame|페이지]] 랭크 [[001_algorithm_definition|알고리즘]] 하드웨어 맵핑
615. [[022_smart_contract|스마트 컨트랙트]] [[395_verification_process_review|검증]] 보조 코프로세서
616. [[229_zkp_data_clean_room|영지식 증명]] ([[354_did_decentralized_identity_zkp|ZKP]]) 가속 [[009_semiconductor|반도체]] (ZK-Rollup)
617. [[617_fhe_modular_multiplier|완전 동형 암호]] ([[617_fhe_modular_multiplier|FHE]])용 대규모 [[192_module_independence|모듈]]러 곱셈기
618. [[618_soa_hardware|SOA]] ([[618_soa_hardware|Service Oriented Architecture]]) HW 고려사항
619. [[619_msa_traffic_hardware|MSA]] ([[619_msa_traffic_hardware|Microservices]]) 트래픽 처리용 하드웨어
620. [[150_serverless_computing_faas|서버리스 컴퓨팅]] [[561_container_based_deployment|컨테이너]] 분리 하드웨어 기술
621. [[621_scale_up_system_bus|스케일 업]] ([[621_scale_up_system_bus|Scale-Up]]) [[127_system_bus|시스템 버스]]
622. [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]] ([[202_scale_out_distributed_horizontal_expansion|Scale-Out]]) 클러스터 망
623. [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] [[237_pue_power_usage_effectiveness_datacenter_metric|PUE]] ([[623_datacenter_pue|Power Usage Effectiveness]])
624. [[624_bmt_procedure|BMT]] ([[624_bmt_procedure|Bench Mark Test]]) 절차 및 평가 항목
625. [[085_sla|SLA]] ([[085_sla|Service Level Agreement]]) 하드웨어 [[452_availability|가용성]]
626. [[175_drs_bcp_strategy|재해 복구 시스템]] ([[626_drs_storage_mirroring|DRS]]) 스토리지 [[333_raid_1|미러링]]
627. [[177_rpo_recovery_point_objective|RPO]] ([[177_rpo_recovery_point_objective|Recovery Point Objective]])
628. [[176_rto_recovery_time_objective|RTO]] ([[176_rto_recovery_time_objective|Recovery Time Objective]])
629. [[629_bare_metal_cloud|베어메탈 클라우드]] ([[629_bare_metal_cloud|Bare Metal Cloud]])
630. [[630_hci|하이퍼컨버지드 인프라]] ([[630_hci|HCI]])
631. [[631_sddc|SDDC]] (Software Defined [[801_data_center_3_tier_architecture_core_aggregation_access|Data Center]])
632. [[632_sds|SDS]] ([[632_sds|Software Defined Storage]])
633. [[633_sdn_whitebox|SDN]] ([[633_sdn_whitebox|Software Defined Network]]) [[859_whitebox_switch_open_hardware_nos|화이트박스 스위치]]
634. 엣지 [[190_ai_llm_requirements_specification|AI]] 칩 아키텍처
635. 온디바이스 [[190_ai_llm_requirements_specification|AI]] ([[635_on_device_ai|On-Device AI]])
636. [[256_federated_learning_privacy_model_security|연합 학습]] ([[256_federated_learning_privacy_model_security|Federated Learning]]) [[136_variance|분산]] 아키텍처
637. TinyML 하드웨어 제약
638. [[638_resource_pooling_cxl|자원 풀링]] (Resource [[285_pooling_layer|Pooling]], [[441_cxl|CXL]] 기반)
639. [[639_rack_scale_architecture|랙 스케일 아키텍처]] ([[639_rack_scale_architecture|Rack Scale Architecture]])
640. [[640_open_compute_project|오픈 컴퓨트 프로젝트]] ([[746_ocp|OCP]], [[640_open_compute_project|Open Compute Project]])
641. [[208_data_lake_schema_on_read|데이터 레이크]] ([[208_data_lake_schema_on_read|Data Lake]]) 스토리지 아키텍처
642. [[642_observability_telemetry|옵저버빌리티]] ([[642_observability_telemetry|Observability]]) HW 텔레메트리
643. [[099_aiops_chatbot_itsm_automation|AIOps]] 기반 하드웨어 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]
644. [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]]) 아키텍처의 하드웨어 [[487_root_of_trust|루트 오브 트러스트]]
645. [[645_data_pipeline_acceleration|데이터 파이프라인]] ([[645_data_pipeline_acceleration|Data Pipeline]]) 가속
646. [[004_blockchain|블록체인]] 노드 스토리지 병목 현상
647. [[647_bft_verification|비잔틴 장애 허용]] ([[647_bft_verification|BFT]]) [[136_variance|분산]] 시스템 [[395_verification_process_review|검증]]
648. [[648_cap_theorem_storage|캡 정리]] ([[219_cap_pacelc_distributed_tradeoff|CAP Theorem]])와 [[136_variance|분산]] 스토리지
649. [[342_pacelc|PACELC]] 정리
650. [[650_eventual_consistency|결과적 일관성]] ([[650_eventual_consistency|Eventual Consistency]])
651. 서버 랙 PDU ([[651_server_rack_pdu|Power Distribution Unit]])
652. [[652_ups_architecture|무정전 전원 장치]] ([[652_ups_architecture|UPS]])
653. ARM Cortex-A 시리즈 특징
654. ARM Cortex-R 시리즈
655. ARM Cortex-M 시리즈
656. x86 Ring 0, 1, 2, 3 [[571_protection_vs_security|보호]] 모드
657. [[015_virtualization|가상화]] VMX root 모드
658. [[658_intel_vtx|Intel VT-x]]
659. [[659_amd_v|AMD-V]]
660. [[660_nested_page_table|중첩 페이지 테이블]] ([[660_nested_page_table|Nested Page Table]], NPT)
661. [[661_extended_page_table|확장 페이지 테이블]] ([[661_extended_page_table|Extended Page Table]], EPT)
662. [[662_shadow_page_table|그림자 페이지 테이블]] ([[626_shadow_page_table_vs_ept|Shadow Page Table]])
663. [[058_paravirtualization|반가상화]] ([[058_paravirtualization|Paravirtualization]]) I/O
664. [[057_full_virtualization|전가상화]] ([[057_full_virtualization|Full Virtualization]]) I/O
665. Virtio 드라이버 모델
666. VFIO 프레임워크
667. [[628_container_runtime_oci|컨테이너 런타임]] ([[667_container_runtime_hw_isolation|runc]]) HW [[061_namespace|네임스페이스]]
668. [[062_cgroups|cgroups]] ([[668_cgroups_hw_resource_allocation|Control Groups]]) [[041_resource_allocation|자원 할당]]
669. [[069_ebpf|BPF]] ([[069_ebpf|Berkeley Packet Filter]]) HW [[440_offloading|오프로딩]]
670. [[670_xdp|XDP]] ([[661_ebpf_xdp_express_data_path|eXpress Data Path]])
671. [[671_dpdk|DPDK]] ([[001_dikw_pyramid|Data]] Plane Development Kit)
672. [[672_spdk|SPDK]] (Storage [[282_performance_tactics|Performance]] Development Kit)
673. [[673_rdma_iwarp|RDMA iWARP]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]
674. [[674_storage_tiering|스토리지 티어링]] ([[674_storage_tiering|Storage Tiering]])
675. [[675_hot_data_caching|핫 데이터]] ([[675_hot_data_caching|Hot Data]]) [[456_caching|캐싱]]
676. [[676_cold_data_archiving|콜드 데이터]] ([[676_cold_data_archiving|Cold Data]]) 아카이빙
677. [[494_object_storage|오브젝트 스토리지]] ([[494_object_storage|Object Storage]])
678. Ceph 스토리지 아키텍처
679. [[679_glusterfs|GlusterFS]] [[136_variance|분산]] 스토리지
680. [[013_hdfs|HDFS]] ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[553_distributed_file_system|Distributed File System]])
681. [[681_erasure_coding|Erasure Coding]] ([[681_erasure_coding|삭제 코딩]]) HW 연산
682. [[546_data_deduplication|데이터 중복 제거]] ([[546_data_deduplication|Data Deduplication]])
683. [[683_inline_compression|인라인 압축]] ([[683_inline_compression|Inline Compression]])
684. [[684_thin_provisioning|씬 프로비저닝]] ([[684_thin_provisioning|Thin Provisioning]])
685. [[685_lun_masking|LUN]] ([[685_lun_masking|Logical Unit Number]]) 마스킹
686. 멀티패스 I/O ([[500_multipath_io|Multipath]] I/O)
687. 스토리지 컨트롤러 캐시 [[333_raid_1|미러링]]
688. [[688_bbu|배터리 백업 캐시]] ([[688_bbu|BBU]])
689. NVRAM 로깅
690. [[690_disk_spindown|디스크 스핀다운]] ([[690_disk_spindown|Disk Spin-down]])
691. [[691_maid_storage|MAID]] (Massive [[055_array|Array]] of [[611_cpu_idle_wait_optimization|Idle]] Disks)
692. [[692_tape_library|테이프 라이브러리]] ([[692_tape_library|Tape Library]])
693. [[590_worm|WORM]] (Write Once Read Many) 스토리지
694. [[694_optical_disc_jukebox|광 디스크 주크박스]]
695. [[695_storage_topology|스토리지 네트워크 토폴로지]] ([[696_fibre_channel_protocol|FC]]-AL, [[696_fibre_channel_protocol|FC]]-SW)
696. [[696_fibre_channel_protocol|Fibre Channel]] ([[696_fibre_channel_protocol|FC]]) [[295_protocol_field_tcp_udp_icmp|프로토콜]]
697. [[697_fcoe|FCoE]] ([[696_fibre_channel_protocol|Fibre Channel]] over [[230_ethernet_structure_and_principles_ieee_802_3|Ethernet]])
698. [[698_iscsi|iSCSI]] (Internet Small Computer System Interface)
699. [[482_nvme|NVMe]] 큐 쌍 ([[699_nvme_queue_pairs|Queue Pairs]])
700. [[482_nvme|NVMe]] [[061_namespace|네임스페이스]] ([[700_nvme_namespaces|Namespaces]])
701. [[482_nvme|NVMe]] 서브시스템
702. [[702_multi_stream_write|다중 스트림 쓰기]] ([[702_multi_stream_write|Multi-stream Write]])
703. [[703_zns_ssd|ZNS]] ([[703_zns_ssd|Zoned Namespace]]) [[327_ssd|SSD]]
704. [[704_host_memory_buffer|호스트 메모리 버퍼]] (HMB, [[704_host_memory_buffer|Host Memory Buffer]])
705. [[705_open_source_firmware_coreboot|오픈소스 펌웨어]] (Coreboot, LinuxBoot)
706. [[706_uefi|UEFI]] (Unified Extensible [[032_firmware|Firmware]] Interface)
707. [[075_acpi|ACPI]] (Advanced Configuration and [[069_type_1_2_error_statistical_power|Power]] Interface)
708. [[708_nvme_queue_management|SMBIOS]] ([[708_nvme_queue_management|System Management BIOS]])
709. [[709_ipmi|IPMI]] (Intelligent Platform [[372_management|Management]] Interface)
710. [[710_bmc|BMC]] ([[710_bmc|Baseboard Management Controller]])
711. Redfish 관리 [[014_api_posix|API]]
712. [[712_oob_management|서버 대역외 관리]] ([[712_oob_management|OOB Management]])
713. [[713_kvm_over_ip|KVM]] (Keyboard, Video, Mouse) 오버 IP
714. [[714_virtual_media_mount|원격 미디어 마운트]]
715. [[715_hw_health_monitoring|하드웨어 헬스 모니터링]] ([[715_hw_health_monitoring|센서 레지스터]])
716. [[716_pcie_aer|PCIe AER]] ([[716_pcie_aer|Advanced Error Reporting]])
717. 메모리 MCA ([[717_memory_mca|Machine Check Architecture]])
718. [[718_edac|EDAC]] ([[040_error_detection|Error Detection]] and Correction)
719. CPU 클럭 다운클럭킹 ([[719_cpu_downclocking|안전 모드]])
720. PROCHOT# 핀 ([[720_prochot_pin|프로세서 핫 시그널]])
721. 패키지 [[077_c_states|C-States]]
722. 코어 [[077_c_states|C-States]]
723. [[078_p_states|P-States]] ([[723_p_states|Performance States]])
724. [[724_t_states|T-States]] ([[724_t_states|Throttling States]])
725. [[725_acpi_s_states|ACPI S-States]] (S0 ~ S5)
726. [[726_modern_standby_s0ix|모던 스탠바이]] (Modern Standby, S0ix)
727. S0ix 저전력 유휴 상태
728. [[728_speedstep|인텔 스피드스텝]] ([[728_speedstep|SpeedStep]])
729. [[729_cool_n_quiet|AMD Cool]]'n'Quiet
730. [[730_turbo_boost|인텔 터보부스트]] ([[730_turbo_boost|Turbo Boost]])
731. AMD 프리시전 부스트 ([[731_amd_precision_boost|Precision Boost]])
732. [[732_smartshift_dynamic_power|스마트 시프트]] ([[732_smartshift_dynamic_power|SmartShift]])
733. [[733_tvb|동적 주파수 한계]] ([[733_tvb|Thermal Velocity Boost]])
734. PL1, PL2 ([[069_type_1_2_error_statistical_power|Power]] Limit 1, 2)
735. [[735_tjmax|TjMax]] ([[735_tjmax|Tunction Max Temperature]])
736. [[736_ihs_integrated_heat_spreader|히트스프레더]] (IHS, Integrated Heat Spreader)
737. [[737_thermal_paste_tim|서멀 페이스트]] ([[737_thermal_paste_tim|TIM]])
738. [[738_vapor_chamber|베이퍼 체임버]] ([[738_vapor_chamber|Vapor Chamber]])
739. [[739_heatpipe|히트파이프]] ([[739_heatpipe|Heatpipe]])
740. 서버 섀시 팬 핫스왑
741. [[456_dual_redundancy|이중화]] 전원 공급 장치 ([[741_redundant_power_supply|Redundant Power Supply]])
742. [[742_vrm|전압 조정기 모듈]] ([[742_vrm|VRM]])
743. [[743_multi_phase_vrm|다상 전원부]] ([[743_multi_phase_vrm|Multi-phase VRM]])
744. [[744_load_line_calibration|로드 라인 캘리브레이션]] ([[744_load_line_calibration|LLC]])
745. [[745_ovp|과전압 보호]] ([[745_ovp|OVP]], Over [[001_voltage|Voltage]] [[571_protection_vs_security|Protection]])
746. [[746_ocp|과전류 보호]] ([[746_ocp|OCP]], Over [[002_current|Current]] [[571_protection_vs_security|Protection]])
747. [[747_scp|단락 보호]] ([[747_scp|SCP]], Short Circuit [[571_protection_vs_security|Protection]])
748. [[748_otp|과열 보호]] ([[748_otp|OTP]], Over [[386_llm_temperature|Temperature]] [[571_protection_vs_security|Protection]])
749. [[749_non_stop_operation|무정전 운영]] ([[749_non_stop_operation|Non-Stop Operation]]) 아키텍처
750. [[750_fault_injection_test|결함 주입 테스트]] ([[750_fault_injection_test|Fault Injection Test]])
751. [[751_chaos_engineering|카오스 엔지니어링]] ([[751_chaos_engineering|Chaos Engineering]]) HW 모의
752. [[752_fmea|FMEA]] (Failure Mode and Effects Analysis)
753. [[753_fta|FTA]] ([[753_fta|Fault Tree Analysis]])
754. [[754_rbd|신뢰성 블록 다이어그램]] ([[754_rbd|RBD]])
755. [[755_markov_model|마르코프 모델]] ([[755_markov_model|Markov Model]]) [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 분석
756. [[756_bathtub_curve|배스터브 곡선]] ([[756_bathtub_curve|Bathtub Curve]]) 고장률
757. [[459_quic_fec_forward_error_correction|초기]] 고장기, 우발 고장기, 마모 고장기
758. [[758_burn_in_test|번인]] ([[758_burn_in_test|Burn-in]]) 테스트
759. [[759_halt|HALT]] (Highly Accelerated Life Test)
760. [[760_hass|HASS]] (Highly Accelerated Stress Screen)
761. MIL-HDBK-217 고장률 예측
762. [[762_accelerated_life_testing|가속 수명 시험]] ([[762_accelerated_life_testing|ALT]])
763. [[763_software_rejuvenation|소프트웨어 회춘]] ([[763_software_rejuvenation|Software Rejuvenation]])과 HW 리부트
764. [[764_mds|마이크로아키텍처 데이터 샘플링]] ([[764_mds|MDS]]) 공격
765. [[765_ridl_attack|리들]] ([[765_ridl_attack|RIDL]]) 공격
766. [[766_fallout_attack|폴아웃]] ([[766_fallout_attack|Fallout]]) 공격
767. [[767_zombieload_attack|좀비로드]] ([[767_zombieload_attack|ZombieLoad]])
768. SGAxe 및 [[030_누화_크로스토크|CrossTalk]] 공격
769. [[769_plundervolt|플런더버그]] ([[769_plundervolt|Plundervolt]])
770. PACMAN 공격 (ARM PAC 우회)
771. [[771_voltage_glitching|볼티지 글리칭]] ([[771_voltage_glitching|Voltage Glitching]])
772. [[772_clock_glitching|클럭 글리칭]] ([[772_clock_glitching|Clock Glitching]])
773. [[773_emfi|EMFI]] ([[773_emfi|Electromagnetic Fault Injection]])
774. [[668_side_channel_attack_meltdown_spectre_kpti|부채널 공격]] - 캐시 타이밍 공격
775. Prime+Probe 기법
776. Flush+Reload 기법
777. Evict+Time 기법
778. 전력 분석 공격 - DPA ([[778_dpa_resistant_logic|Differential Power Analysis]])
779. 전자기 분석 공격 - EMA
780. [[780_reverse_engineering|물리적 분해 분석]] ([[780_reverse_engineering|Reverse Engineering]])
781. [[781_fib_circuit_edit|FIB]] ([[781_fib_circuit_edit|Focused Ion Beam]]) 수정
782. [[782_decapping_probing|디캡핑]] ([[782_decapping_probing|Decapping]]) 및 프로빙 (Probing)
783. [[783_anti_tamper_mesh|안티 탬퍼]] ([[783_anti_tamper_mesh|Anti-Tamper]]) [[389_mesh_topology|메시]]/쉴드
784. [[784_zeroization_circuit|제로화]] ([[784_zeroization_circuit|Zeroization]]) 회로
785. [[785_secure_key_erasure|보안 키 소거]] ([[785_secure_key_erasure|Secure Key Erasure]])
786. [[669_hardware_trng_kernel_entropy_pool|TRNG]] (True Random Number Generator) [[151_entropy|엔트로피]] 소스
787. [[787_ring_oscillator_trng|링 오실레이터]] ([[787_ring_oscillator_trng|Ring Oscillator]]) [[669_hardware_trng_kernel_entropy_pool|TRNG]]
788. [[788_sram_puf|SRAM PUF]] ([[788_sram_puf|Physical Unclonable Function]])
789. [[789_challenge_response_pair|도전-응답 쌍]] (Challenge-Response Pair)
790. [[666_secure_enclave_trustzone_sgx_tee|보안 엔클레이브]] ([[790_secure_enclave|Secure Enclave]])
791. 애플 [[790_secure_enclave|Secure Enclave]] Processor ([[791_apple_sep|SEP]])
792. [[792_google_titan|Google Titan]] 보안 칩
793. [[793_microsoft_titan|Microsoft Titan]] 보안 칩
794. [[794_aws_nitro_enclaves|AWS Nitro Enclaves]]
795. [[795_confidential_computing|Confidential Computing]] ([[795_confidential_computing|기밀 컴퓨팅]])
796. [[796_memory_encryption|메모리 암호화]] (Intel MKTME, AMD SME/SEV)
797. [[797_dynamic_memory_encryption|동적 메모리 암호화]]
798. [[798_tdi|TDI]] ([[798_tdi|Trust Domain Interconnect]])
799. [[799_arm_cca|ARM CCA]] ([[799_arm_cca|Confidential Compute Architecture]])
800. [[800_riscv_pmp|RISC-V PMP]] ([[800_riscv_pmp|Physical Memory Protection]])
801. [[801_riscv_epmp|RISC-V ePMP]] ([[801_riscv_epmp|Enhanced PMP]])
802. [[191_oss_license_compliance|오픈소스]] 하드웨어 RoT ([[802_opentitan|OpenTitan]])

---
**총합 요약 : 총 802개의 핵심 키워드 수록**
(지나치게 지엽적인 [[009_semiconductor|반도체]] 공학 및 물리학 용어는 제거하고, 기술사 시험(정보관리, 컴퓨터응용시스템)에서 실질적으로 출제되는 **시스템 아키텍처, [[430_index_fast_full_scan|병렬]] 처리, 메모리 계층, 스토리지 시스템, [[015_virtualization|가상화]]/클라우드 하드웨어, [[190_ai_llm_requirements_specification|AI]] 가속기 및 하드웨어 보안** 위주로 심화 확장하여 1000여 개의 실전 키워드로 재구성하였습니다.)
