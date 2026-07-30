import { mkdir, writeFile } from 'node:fs/promises';
import { JSDOM } from 'jsdom';
import * as Plot from '@observablehq/plot';

const outputDirectory = new URL('../public/diagrams/', import.meta.url);

const samples = [
  { x1: 1.4, x2: 4.7, class: '클래스 A' },
  { x1: 1.9, x2: 3.5, class: '클래스 A' },
  { x1: 2.5, x2: 4.0, class: '클래스 A' },
  { x1: 2.8, x2: 2.5, class: '클래스 A' },
  { x1: 3.0, x2: 5.0, class: '클래스 A', support: true },
  { x1: 4.0, x2: 4.0, class: '클래스 A', support: true },
  { x1: 6.0, x2: 6.0, class: '클래스 B', support: true },
  { x1: 6.3, x2: 7.2, class: '클래스 B' },
  { x1: 7.0, x2: 6.4, class: '클래스 B' },
  { x1: 7.5, x2: 8.2, class: '클래스 B' },
  { x1: 8.1, x2: 7.3, class: '클래스 B' },
  { x1: 8.6, x2: 8.7, class: '클래스 B' },
];

const boundaries = [
  { boundary: '클래스 A 마진', order: 0, x1: 0, x2: 8 },
  { boundary: '클래스 A 마진', order: 1, x1: 8, x2: 0 },
  { boundary: '결정 경계', order: 0, x1: 0, x2: 10 },
  { boundary: '결정 경계', order: 1, x1: 10, x2: 0 },
  { boundary: '클래스 B 마진', order: 0, x1: 2, x2: 10 },
  { boundary: '클래스 B 마진', order: 1, x1: 10, x2: 2 },
];

const colors = {
  '클래스 A': '#dc2626',
  '클래스 B': '#2563eb',
};

function serializeChart(chart, ariaLabel) {
  const svg = chart.tagName.toLowerCase() === 'svg' ? chart : chart.querySelector('svg');
  svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', ariaLabel);
  return svg.outerHTML;
}

function createLineChart({ title, xLabel, yLabel, series, annotations = [] }) {
  const dom = new JSDOM('<!doctype html><html><body></body></html>');
  const document = dom.window.document;
  const names = [...new Set(series.map((point) => point.series))];
  const palette = ['#2563eb', '#dc2626', '#059669', '#7c3aed'];
  const chart = Plot.plot({
    document,
    width: 860,
    height: 520,
    marginTop: 92,
    marginRight: 42,
    marginBottom: 62,
    marginLeft: 74,
    style: {
      background: '#f8fafc',
      color: '#334155',
      fontFamily: 'system-ui, sans-serif',
      fontSize: '15px',
    },
    x: { label: xLabel, grid: true },
    y: { label: yLabel, grid: true },
    color: { domain: names, range: palette.slice(0, names.length), legend: false },
    marks: [
      Plot.text([{ x: 0.5, y: 1, label: title }], {
        x: 'x',
        y: 'y',
        text: 'label',
        frameAnchor: 'top',
        dy: -72,
        fontSize: 20,
        fontWeight: 700,
        fill: '#1f2937',
      }),
      Plot.line(series, { x: 'x', y: 'y', z: 'series', stroke: 'series', strokeWidth: 3 }),
      Plot.dot(series, { x: 'x', y: 'y', fill: 'series', r: 4 }),
      Plot.text(annotations, {
        x: 'x',
        y: 'y',
        text: 'label',
        fill: '#475569',
        fontWeight: 600,
        dy: -12,
      }),
      Plot.dot(
        names.map((name, index) => ({ x: index, y: 0, name })),
        { x: 'x', y: 'y', fill: 'name', r: 6, frameAnchor: 'top', dy: -42 },
      ),
      Plot.text(
        names.map((name, index) => ({ x: index, y: 0, name })),
        {
          x: 'x',
          y: 'y',
          text: 'name',
          frameAnchor: 'top',
          dy: -42,
          dx: 12,
          textAnchor: 'start',
          fill: '#475569',
        },
      ),
    ],
  });
  return serializeChart(chart, `${title}: ${names.join(', ')} 계열 차트`);
}

function createQuantizationChart() {
  const dom = new JSDOM('<!doctype html><html><body></body></html>');
  const document = dom.window.document;
  const scale = 0.5;
  const zeroPoint = 4;
  const values = Array.from({ length: 101 }, (_, index) => -2.5 + index * 0.05).map((x) => {
    const q = Math.max(0, Math.min(7, Math.round(x / scale) + zeroPoint));
    return { x, restored: scale * (q - zeroPoint), original: x };
  });
  const chart = Plot.plot({
    document,
    width: 860,
    height: 520,
    marginTop: 82,
    marginRight: 42,
    marginBottom: 62,
    marginLeft: 74,
    style: { background: '#f8fafc', color: '#334155', fontFamily: 'system-ui, sans-serif', fontSize: '15px' },
    x: { label: '실숫값 x', grid: true },
    y: { label: '복원값 x̂', domain: [-2.5, 2.5], grid: true },
    marks: [
      Plot.text([{ x: 0, y: 2.42, label: '균일 비대칭 양자화 매핑' }], {
        x: 'x', y: 'y', text: 'label', fontSize: 20, fontWeight: 700, fill: '#1f2937',
      }),
      Plot.line(values, { x: 'x', y: 'original', stroke: '#94a3b8', strokeDasharray: '6,5' }),
      Plot.line(values, { x: 'x', y: 'restored', curve: 'step-after', stroke: '#2563eb', strokeWidth: 3 }),
      Plot.text([
        { x: -2.25, restored: -2, label: '포화' },
        { x: 0.25, restored: 0.5, label: '반올림 오차' },
        { x: 2.25, restored: 1.5, label: '포화' },
      ], { x: 'x', y: 'restored', text: 'label', dy: -12, fill: '#475569', fontWeight: 600 }),
    ],
  });
  return serializeChart(chart, '스케일 0.5와 영점 4를 적용한 균일 비대칭 양자화 계단 함수');
}

function createDistillationChart() {
  const dom = new JSDOM('<!doctype html><html><body></body></html>');
  const document = dom.window.document;
  const logits = [4, 2, 1];
  const classes = ['클래스 A', '클래스 B', '클래스 C'];
  const temperatures = [1, 3];
  const values = temperatures.flatMap((temperature) => {
    const exps = logits.map((logit) => Math.exp(logit / temperature));
    const sum = exps.reduce((total, value) => total + value, 0);
    return exps.map((value, index) => ({
      class: classes[index],
      temperature: `T=${temperature}`,
      probability: value / sum,
    }));
  });
  const chart = Plot.plot({
    document,
    width: 860,
    height: 520,
    marginTop: 82,
    marginRight: 42,
    marginBottom: 62,
    marginLeft: 74,
    style: { background: '#f8fafc', color: '#334155', fontFamily: 'system-ui, sans-serif', fontSize: '15px' },
    x: { label: '클래스' },
    y: { label: '소프트맥스 확률', domain: [0, 1], grid: true },
    color: { domain: ['T=1', 'T=3'], range: ['#2563eb', '#dc2626'], legend: false },
    marks: [
      Plot.barY(values, { x: 'class', y: 'probability', fill: 'temperature', fx: 'temperature', inset: 12 }),
      Plot.text(values, {
        x: 'class', y: 'probability', fx: 'temperature',
        text: (d) => d.probability.toFixed(3), dy: -10, fontWeight: 600,
      }),
      Plot.text([{ class: '클래스 B', probability: 0.95, label: '템퍼러처 증가 → 분포 평활화' }], {
        x: 'class', y: 'probability', text: 'label', fontSize: 18, fontWeight: 700, fill: '#1f2937',
      }),
    ],
  });
  return serializeChart(chart, '고정 로짓 4, 2, 1에서 템퍼러처 1과 3의 소프트 타깃 확률 비교');
}

function createObservablePlot() {
  const dom = new JSDOM('<!doctype html><html><body></body></html>');
  const document = dom.window.document;
  const supportVectors = samples.filter((sample) => sample.support);

  const chart = Plot.plot({
    document,
    width: 860,
    height: 520,
    marginTop: 54,
    marginRight: 42,
    marginBottom: 62,
    marginLeft: 70,
    style: {
      background: '#f8fafc',
      color: '#334155',
      fontFamily: 'system-ui, sans-serif',
      fontSize: '15px',
    },
    x: { domain: [0, 10], label: '특징 x₁', grid: true },
    y: { domain: [0, 11], label: '특징 x₂', grid: true },
    color: {
      domain: Object.keys(colors),
      range: Object.values(colors),
      legend: false,
    },
    symbol: {
      domain: ['클래스 A', '클래스 B'],
      range: ['circle', 'square'],
      legend: false,
    },
    marks: [
      Plot.text(
        [{ x1: 5, x2: 10.75, label: 'Observable Plot — SVM 최대 마진과 서포트 벡터' }],
        {
          x: 'x1',
          y: 'x2',
          text: 'label',
          fontSize: 20,
          fontWeight: 700,
          fill: '#1f2937',
        },
      ),
      Plot.dot(
        [
          { x1: 3.8, x2: 10.2, class: '클래스 A' },
          { x1: 5.8, x2: 10.2, class: '클래스 B' },
        ],
        {
          x: 'x1',
          y: 'x2',
          fill: 'class',
          symbol: 'class',
          r: 6,
        },
      ),
      Plot.text(
        [
          { x1: 4.0, x2: 10.2, label: '클래스 A' },
          { x1: 6.0, x2: 10.2, label: '클래스 B' },
        ],
        {
          x: 'x1',
          y: 'x2',
          text: 'label',
          textAnchor: 'start',
          dx: 5,
          fill: '#475569',
        },
      ),
      Plot.line(
        boundaries.filter((line) => line.boundary !== '결정 경계'),
        {
          x: 'x1',
          y: 'x2',
          z: 'boundary',
          stroke: '#64748b',
          strokeDasharray: '7,6',
          strokeWidth: 2,
        },
      ),
      Plot.line(
        boundaries.filter((line) => line.boundary === '결정 경계'),
        {
          x: 'x1',
          y: 'x2',
          stroke: '#111827',
          strokeWidth: 4,
        },
      ),
      Plot.dot(samples, {
        x: 'x1',
        y: 'x2',
        fill: 'class',
        symbol: 'class',
        r: 7,
        stroke: 'white',
        strokeWidth: 1.5,
      }),
      Plot.dot(supportVectors, {
        x: 'x1',
        y: 'x2',
        r: 14,
        fill: 'none',
        stroke: '#f59e0b',
        strokeWidth: 3,
      }),
      Plot.arrow(
        [{ x1: 5.1, x2: 5.1, x1End: 5.8, x2End: 6.2 }],
        {
          x1: 'x1',
          y1: 'x2',
          x2: 'x1End',
          y2: 'x2End',
          stroke: '#475569',
          headLength: 9,
        },
      ),
      Plot.text([{ x1: 4.95, x2: 4.85, label: '결정 경계' }], {
        x: 'x1',
        y: 'x2',
        text: 'label',
        textAnchor: 'end',
        fontWeight: 700,
      }),
      Plot.text(
        [
          { x1: 2.2, x2: 7.3, label: '마진 경계' },
          { x1: 7.8, x2: 3.5, label: '마진 경계' },
          { x1: 5.9, x2: 6.55, label: '서포트 벡터' },
        ],
        {
          x: 'x1',
          y: 'x2',
          text: 'label',
          fill: '#475569',
          fontWeight: 600,
        },
      ),
    ],
  });

  return serializeChart(
    chart,
    '두 클래스와 최대 마진 결정 경계, 마진 경계, 서포트 벡터를 나타낸 Observable Plot 산점도',
  );
}

await mkdir(outputDirectory, { recursive: true });
await Promise.all([
  writeFile(new URL('svm-observable-plot.svg', outputDirectory), createObservablePlot()),
  writeFile(
    new URL('positional-encoding.svg', outputDirectory),
    createLineChart({
      title: '위치에 따른 사인 인코딩 값',
      xLabel: '토큰 위치',
      yLabel: '인코딩 값',
      series: Array.from({ length: 51 }, (_, x) => [
        { x, y: Math.sin(x), series: 'sin(pos)' },
        { x, y: Math.sin(x / 10), series: 'sin(pos/10)' },
      ]).flat(),
      annotations: [
        { x: 8, y: Math.sin(8), label: '빠른 주기: 인접 위치 구분' },
        { x: 28, y: Math.sin(2.8), label: '느린 주기: 넓은 범위 구분' },
      ],
    }),
  ),
  writeFile(
    new URL('context-resource-growth.svg', outputDirectory),
    createLineChart({
      title: '컨텍스트 길이에 따른 자원 증가 개념도',
      xLabel: '상대 토큰 길이',
      yLabel: '상대 자원량',
      series: [1, 2, 4, 8, 16].flatMap((x) => [
        { x, y: x ** 2, series: '전체 어텐션 관계 계산량 N²' },
        { x, y: x, series: 'KV 캐시 저장량 N' },
      ]),
      annotations: [{ x: 16, y: 256, label: '길이 2배 → 관계 계산량 약 4배' }],
    }),
  ),
  writeFile(
    new URL('long-context-attention-growth.svg', outputDirectory),
    createLineChart({
      title: '문맥 길이에 따른 어텐션 상호작용 증가 개념도',
      xLabel: '정규화 문맥 길이 n',
      yLabel: '정규화 상호작용 수',
      series: [1, 2, 4, 8, 16].flatMap((x) => [
        { x, y: x ** 2, series: '전체 어텐션 n²' },
        { x, y: x, series: '고정 윈도우 어텐션 n' },
      ]),
      annotations: [{ x: 16, y: 256, label: '문맥 2배 → 상호작용 약 4배' }],
    }),
  ),
  writeFile(
    new URL('test-time-compute.svg', outputDirectory),
    createLineChart({
      title: '추론 예산에 따른 품질 한계효용 개념도',
      xLabel: '정규화 추론 예산',
      yLabel: '정규화 품질',
      series: [0.4, 0.62, 0.75, 0.82, 0.86].map((y, index) => ({
        x: index + 1,
        y,
        series: '추론 품질',
      })),
      annotations: [{ x: 4, y: 0.82, label: '추가 이득 감소 → 종료 임계값 검토' }],
    }),
  ),
  writeFile(
    new URL('kv-cache-memory.svg', outputDirectory),
    createLineChart({
      title: '문맥 길이·KV 헤드 수별 캐시 메모리 이론값',
      xLabel: '문맥 길이(K tokens)',
      yLabel: 'KV 캐시(GiB)',
      series: [1, 2, 4, 8, 16, 32].flatMap((x) => [
        { x, y: 0.5 * x, series: 'MHA 32 KV 헤드' },
        { x, y: 0.125 * x, series: 'GQA 8 KV 헤드' },
        { x, y: 0.015625 * x, series: 'MQA 1 KV 헤드' },
      ]),
      annotations: [{ x: 8, y: 4, label: 'KV 헤드 공유 → 캐시 감소' }],
    }),
  ),
  writeFile(
    new URL('slm-weight-memory.svg', outputDirectory),
    createLineChart({
      title: '파라미터 수·정밀도별 가중치 메모리 이론값',
      xLabel: '파라미터 수(B)',
      yLabel: '가중치 메모리(GB)',
      series: [0.5, 1, 3, 7].flatMap((x) => [
        { x, y: x * 2, series: 'FP16 16bit' },
        { x, y: x, series: 'INT8 8bit' },
        { x, y: x * 0.5, series: 'INT4 4bit' },
      ]),
      annotations: [{ x: 1, y: 2, label: '1B FP16 = 2GB' }],
    }),
  ),
  writeFile(
    new URL('npu-roofline.svg', outputDirectory),
    createLineChart({
      title: '연산 집약도에 따른 NPU 처리량 상한 개념도',
      xLabel: '정규화 연산 집약도',
      yLabel: '정규화 처리량 상한',
      series: [0.25, 0.5, 1, 2, 4, 8, 16].flatMap((x) => [
        { x, y: x, series: '메모리 대역폭 상한' },
        { x, y: 8, series: '계산 성능 상한' },
        { x, y: Math.min(x, 8), series: '달성 가능 처리량' },
      ]),
      annotations: [
        { x: 2, y: 2, label: '메모리 대역폭 제한' },
        { x: 8, y: 8, label: 'Ridge Point' },
        { x: 14, y: 8, label: '연산 배열 성능 제한' },
      ],
    }),
  ),
  writeFile(new URL('quantization-mapping.svg', outputDirectory), createQuantizationChart()),
  writeFile(new URL('distillation-temperature.svg', outputDirectory), createDistillationChart()),
]);
