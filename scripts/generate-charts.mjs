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

function createEmbeddingChart() {
  const dom = new JSDOM('<!doctype html><html><body></body></html>');
  const document = dom.window.document;
  const points = [
    { x: 1.2, y: 4.2, topic: '검색', label: '검색 엔진' },
    { x: 1.8, y: 3.6, topic: '검색', label: '문서 검색' },
    { x: 2.5, y: 4.4, topic: '검색', label: '질의 응답' },
    { x: 6.1, y: 1.6, topic: '보안', label: '접근 통제' },
    { x: 6.8, y: 2.2, topic: '보안', label: '권한 관리' },
    { x: 7.4, y: 1.3, topic: '보안', label: '인증 정책' },
  ];
  const chart = Plot.plot({
    document,
    width: 860,
    height: 520,
    marginTop: 82,
    marginRight: 54,
    marginBottom: 54,
    marginLeft: 58,
    style: {
      background: '#f8fafc',
      color: '#334155',
      fontFamily: 'system-ui, sans-serif',
      fontSize: '15px',
    },
    x: { label: '임베딩 차원 1', domain: [0, 9], grid: true },
    y: { label: '임베딩 차원 2', domain: [0, 6], grid: true },
    color: { domain: ['검색', '보안'], range: ['#2563eb', '#dc2626'], legend: false },
    marks: [
      Plot.text([{ x: 4.5, y: 5.75, label: '의미가 가까운 표현의 벡터 공간 배치' }], {
        x: 'x', y: 'y', text: 'label', fontSize: 20, fontWeight: 700, fill: '#1f2937',
      }),
      Plot.dot(points, { x: 'x', y: 'y', fill: 'topic', stroke: '#fff', strokeWidth: 2, r: 9 }),
      Plot.text(points, { x: 'x', y: 'y', text: 'label', dy: -16, fill: '#334155', fontWeight: 600 }),
      Plot.link([{ x1: 2.5, y1: 4.4, x2: 6.1, y2: 1.6 }], {
        x1: 'x1', y1: 'y1', x2: 'x2', y2: 'y2', stroke: '#64748b', strokeDasharray: '6,5',
      }),
      Plot.text([{ x: 4.3, y: 3.05, label: '주제가 다르면 거리 증가' }], {
        x: 'x', y: 'y', text: 'label', fill: '#475569', fontWeight: 600, dy: -8,
      }),
    ],
  });
  return serializeChart(chart, '검색 주제와 보안 주제의 문장이 각각 가까운 위치에 모인 임베딩 벡터 공간 개념도');
}

function createShapWaterfallChart() {
  const dom = new JSDOM('<!doctype html><html><body></body></html>');
  const document = dom.window.document;
  const contributions = [
    { feature: '소득 +0.18', x1: 0.42, x2: 0.60, direction: '양의 기여' },
    { feature: '부채 -0.11', x1: 0.60, x2: 0.49, direction: '음의 기여' },
    { feature: '연령 +0.06', x1: 0.49, x2: 0.55, direction: '양의 기여' },
    { feature: '거래 이력 +0.09', x1: 0.55, x2: 0.64, direction: '양의 기여' },
  ];
  const chart = Plot.plot({
    document,
    width: 860,
    height: 520,
    marginTop: 82,
    marginRight: 54,
    marginBottom: 58,
    marginLeft: 128,
    style: {
      background: '#f8fafc',
      color: '#334155',
      fontFamily: 'system-ui, sans-serif',
      fontSize: '15px',
    },
    x: { label: '모델 출력값', domain: [0.35, 0.7], grid: true },
    y: { label: null },
    color: { domain: ['양의 기여', '음의 기여'], range: ['#2563eb', '#dc2626'], legend: false },
    marks: [
      Plot.text([{ x: 0.525, feature: '소득 +0.18', label: 'SHAP 특징 기여의 가산 원리' }], {
        x: 'x', y: 'feature', text: 'label', frameAnchor: 'top', dy: -64,
        fontSize: 20, fontWeight: 700, fill: '#1f2937',
      }),
      Plot.rectX(contributions, {
        x1: 'x1', x2: 'x2', y: 'feature', fill: 'direction', insetTop: 7, insetBottom: 7,
      }),
      Plot.ruleX([0.42], { stroke: '#64748b', strokeDasharray: '5,4' }),
      Plot.ruleX([0.64], { stroke: '#111827', strokeWidth: 2 }),
      Plot.text([
        { x: 0.42, feature: '거래 이력 +0.09', label: '기준값 0.42' },
        { x: 0.64, feature: '부채 -0.11', label: '예측값 0.64' },
      ], { x: 'x', y: 'feature', text: 'label', dy: -25, fontWeight: 700, fill: '#334155' }),
    ],
  });
  return serializeChart(chart, '기준값 0.42에 특징별 양의 기여와 음의 기여를 누적해 예측값 0.64에 도달하는 SHAP 워터폴 개념도');
}

function createAdversarialExampleChart() {
  const dom = new JSDOM('<!doctype html><html><body></body></html>');
  const document = dom.window.document;
  const samples = [
    { x: 2.1, y: 2.0, class: '클래스 A' }, { x: 2.8, y: 3.0, class: '클래스 A' },
    { x: 3.5, y: 1.5, class: '클래스 A' }, { x: 6.3, y: 2.0, class: '클래스 B' },
    { x: 7.0, y: 3.1, class: '클래스 B' }, { x: 7.7, y: 1.4, class: '클래스 B' },
  ];
  const chart = Plot.plot({
    document,
    width: 860,
    height: 520,
    marginTop: 82,
    marginRight: 54,
    marginBottom: 56,
    marginLeft: 58,
    style: {
      background: '#f8fafc', color: '#334155',
      fontFamily: 'system-ui, sans-serif', fontSize: '15px',
    },
    x: { label: '입력 특징 1', domain: [0, 10], grid: true },
    y: { label: '입력 특징 2', domain: [0, 5], grid: true },
    color: { domain: ['클래스 A', '클래스 B'], range: ['#2563eb', '#dc2626'], legend: false },
    marks: [
      Plot.text([{ x: 5, y: 4.75, label: 'ε 제약 안의 교란과 결정 경계 통과' }], {
        x: 'x', y: 'y', text: 'label', fontSize: 20, fontWeight: 700, fill: '#1f2937',
      }),
      Plot.ruleX([5], { stroke: '#111827', strokeWidth: 2 }),
      Plot.dot(samples, { x: 'x', y: 'y', fill: 'class', r: 7 }),
      Plot.dot([{ x: 4.3, y: 2.7 }], { x: 'x', y: 'y', stroke: '#2563eb', fill: 'none', r: 42, strokeDasharray: '5,4' }),
      Plot.dot([{ x: 4.3, y: 2.7 }], { x: 'x', y: 'y', fill: '#2563eb', r: 9 }),
      Plot.dot([{ x: 5.35, y: 2.9 }], { x: 'x', y: 'y', fill: '#dc2626', symbol: 'times', r: 10 }),
      Plot.link([{ x1: 4.3, y1: 2.7, x2: 5.35, y2: 2.9 }], {
        x1: 'x1', y1: 'y1', x2: 'x2', y2: 'y2', stroke: '#7c3aed', strokeWidth: 3,
      }),
      Plot.text([
        { x: 4.3, y: 2.7, label: '정상 x' },
        { x: 5.35, y: 2.9, label: '교란 x′' },
      ], { x: 'x', y: 'y', text: 'label', dy: -18, fontWeight: 700 }),
    ],
  });
  return serializeChart(chart, '정상 표본이 엡실론 허용 범위 안에서 이동해 결정 경계를 넘어 오분류되는 적대적 예제 개념도');
}

function createStreamingWatermarkChart() {
  const dom = new JSDOM('<!doctype html><html><body></body></html>');
  const document = dom.window.document;
  const events = [
    { process: 2, event: 1.5, status: '정상' },
    { process: 4, event: 3.2, status: '정상' },
    { process: 6, event: 4.4, status: '허용 지연' },
    { process: 8, event: 5.0, status: '기준 밖 지연' },
    { process: 9, event: 7.5, status: '허용 지연' },
  ];
  const watermark = [2, 4, 6, 8, 10].map((process) => ({ process, event: process - 2 }));
  const chart = Plot.plot({
    document, width: 860, height: 520, marginTop: 82, marginRight: 54, marginBottom: 58, marginLeft: 66,
    style: { background: '#f8fafc', color: '#334155', fontFamily: 'system-ui, sans-serif', fontSize: '15px' },
    x: { label: '처리 시각', domain: [0, 10], grid: true },
    y: { label: '이벤트 시각', domain: [0, 10], grid: true },
    color: { domain: ['정상', '허용 지연', '기준 밖 지연'], range: ['#2563eb', '#f59e0b', '#dc2626'], legend: false },
    marks: [
      Plot.text([{ process: 5, event: 9.6, label: '이벤트 시간과 워터마크 판정 개념도' }], {
        x: 'process', y: 'event', text: 'label', fontSize: 20, fontWeight: 700, fill: '#1f2937',
      }),
      Plot.line(watermark, { x: 'process', y: 'event', stroke: '#111827', strokeDasharray: '6,5', strokeWidth: 2 }),
      Plot.dot(events, { x: 'process', y: 'event', fill: 'status', r: 9, stroke: '#fff', strokeWidth: 2 }),
      Plot.text([{ process: 7.3, event: 5.3, label: '워터마크: 처리 시각-2' }], {
        x: 'process', y: 'event', text: 'label', fill: '#111827', fontWeight: 700, dy: -12,
      }),
    ],
  });
  return serializeChart(chart, '처리 시각과 이벤트 시각 좌표에서 워터마크 선 아래의 기준 밖 지연 이벤트를 구분하는 개념도');
}

function createPueBreakdownChart() {
  const dom = new JSDOM('<!doctype html><html><body></body></html>');
  const document = dom.window.document;
  const data = [
    { category: 'IT 장비 에너지', value: 100, type: 'IT' },
    { category: '시설 오버헤드', value: 50, type: '시설' },
    { category: '총 시설 에너지', value: 150, type: '총량' },
  ];
  const chart = Plot.plot({
    document, width: 860, height: 520, marginTop: 82, marginRight: 54, marginBottom: 70, marginLeft: 70,
    style: { background: '#f8fafc', color: '#334155', fontFamily: 'system-ui, sans-serif', fontSize: '15px' },
    x: { label: null },
    y: { label: '정규화 에너지', domain: [0, 170], grid: true },
    color: { domain: ['IT', '시설', '총량'], range: ['#2563eb', '#f59e0b', '#059669'], legend: false },
    marks: [
      Plot.text([{ category: '시설 오버헤드', value: 165, label: 'PUE = 총 시설 에너지 / IT 장비 에너지' }], {
        x: 'category', y: 'value', text: 'label', fontSize: 20, fontWeight: 700, fill: '#1f2937',
      }),
      Plot.barY(data, { x: 'category', y: 'value', fill: 'type', inset: 24 }),
      Plot.text(data, { x: 'category', y: 'value', text: (d) => `${d.value}`, dy: -10, fontWeight: 700 }),
    ],
  });
  return serializeChart(chart, 'IT 장비 에너지 100과 시설 오버헤드 50이 총 시설 에너지 150을 이루어 PUE 1.5가 되는 예시 막대 차트');
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
  writeFile(new URL('embedding-semantic-space.svg', outputDirectory), createEmbeddingChart()),
  writeFile(
    new URL('lora-rank-parameter-growth.svg', outputDirectory),
    createLineChart({
      title: 'LoRA 랭크에 따른 학습 매개변수 이론값',
      xLabel: '랭크 r',
      yLabel: '매개변수 수(M)',
      series: [4, 8, 16, 32, 64].flatMap((x) => [
        { x, y: (x * (4096 + 4096)) / 1e6, series: 'LoRA A·B 행렬' },
        { x, y: (4096 * 4096) / 1e6, series: '전체 가중치 행렬' },
      ]),
      annotations: [
        { x: 4, y: (4 * 8192) / 1e6, label: 'r=4: 0.0328M' },
        { x: 64, y: (64 * 8192) / 1e6, label: 'r=64: 0.5243M' },
      ],
    }),
  ),
  writeFile(
    new URL('complexity-growth-rates.svg', outputDirectory),
    createLineChart({
      title: '입력 크기에 따른 대표 시간복잡도 증가율',
      xLabel: '입력 크기 n',
      yLabel: '정규화 기본 연산량',
      series: [1, 2, 4, 8, 16].flatMap((x) => [
        { x, y: Math.log2(x + 1), series: 'O(log n)' },
        { x, y: x, series: 'O(n)' },
        { x, y: x * Math.log2(x + 1), series: 'O(n log n)' },
        { x, y: x ** 2, series: 'O(n²)' },
      ]),
      annotations: [{ x: 16, y: 256, label: 'n 증가 시 차수별 격차 확대' }],
    }),
  ),
  writeFile(
    new URL('big-o-upper-bound.svg', outputDirectory),
    createLineChart({
      title: '비용 함수와 점근 상한 개념도',
      xLabel: '입력 크기 n',
      yLabel: '상대 비용',
      series: [1, 2, 3, 4, 5].flatMap((x) => [
        { x, y: x ** 2 + 2 * x, series: '비용 함수 T(n)' },
        { x, y: 2 * x ** 2, series: '상한 함수 2n²' },
      ]),
      annotations: [{ x: 2, y: 8, label: 'n₀=2 이후 상한 성립' }],
    }),
  ),
  writeFile(
    new URL('sorting-comparison-growth.svg', outputDirectory),
    createLineChart({
      title: '정렬 비교 연산 증가율 개념도',
      xLabel: '입력 크기 n',
      yLabel: '상대 비교 연산량',
      series: [1, 2, 4, 8, 16].flatMap((x) => [
        { x, y: x * Math.log2(x), series: 'n log₂ n' },
        { x, y: x ** 2, series: 'n²' },
      ]),
      annotations: [{ x: 16, y: 256, label: '입력 증가 시 격차 확대' }],
    }),
  ),
  writeFile(
    new URL('binary-search-growth.svg', outputDirectory),
    createLineChart({
      title: '이진 탐색과 선형 탐색 증가율 개념도',
      xLabel: '입력 크기 n',
      yLabel: '상대 비교 횟수',
      series: [1, 2, 4, 8, 16].flatMap((x) => [
        { x, y: Math.log2(x), series: '이진 탐색 log₂ n' },
        { x, y: x, series: '선형 탐색 n' },
      ]),
      annotations: [{ x: 16, y: 4, label: '입력 2배당 한 단계 증가' }],
    }),
  ),
  writeFile(
    new URL('gnn-oversmoothing.svg', outputDirectory),
    createLineChart({
      title: '메시지 전파 깊이에 따른 노드 표현 과평활 개념도',
      xLabel: 'GNN 전파 층수',
      yLabel: '정규화 노드 간 표현 분산',
      series: [1, 2, 3, 4, 5].map((x, index) => ({
        x,
        y: [1, 0.72, 0.5, 0.34, 0.25][index],
        series: '노드 간 표현 분산',
      })),
      annotations: [
        { x: 2, y: 0.72, label: '이웃 정보 확장' },
        { x: 5, y: 0.25, label: '표현 수렴·구별력 저하' },
      ],
    }),
  ),
  writeFile(
    new URL('bellman-residual-convergence.svg', outputDirectory),
    createLineChart({
      title: '할인율별 벨만 반복 잔차 수렴 이론값',
      xLabel: '반복 횟수 k',
      yLabel: '정규화 잔차 γᵏ',
      series: Array.from({ length: 9 }, (_, x) => [
        { x, y: 0.5 ** x, series: 'γ=0.5' },
        { x, y: 0.9 ** x, series: 'γ=0.9' },
      ]).flat(),
      annotations: [
        { x: 3, y: 0.5 ** 3, label: '낮은 γ: 빠른 수렴' },
        { x: 7, y: 0.9 ** 7, label: '높은 γ: 장기 보상 반영' },
      ],
    }),
  ),
  writeFile(
    new URL('uct-exploration-bonus.svg', outputDirectory),
    createLineChart({
      title: '자식 방문 수에 따른 UCT 탐험 보너스',
      xLabel: '자식 방문 수 n (부모 방문 N=100)',
      yLabel: '탐험 보너스 √(ln N/n)',
      series: [1, 2, 5, 10, 20, 50, 100].map((x) => ({
        x,
        y: Math.sqrt(Math.log(100) / x),
        series: 'UCT 탐험 보너스',
      })),
      annotations: [
        { x: 1, y: Math.sqrt(Math.log(100)), label: '미방문 분기 우선 탐색' },
        { x: 50, y: Math.sqrt(Math.log(100) / 50), label: '방문 증가 시 보너스 감소' },
      ],
    }),
  ),
  writeFile(new URL('shap-additive-contribution.svg', outputDirectory), createShapWaterfallChart()),
  writeFile(
    new URL('hash-load-factor.svg', outputDirectory),
    createLineChart({
      title: '적재율별 실패 조회 후보 수 이론값',
      xLabel: '적재율 α',
      yLabel: '기대 후보·탐사 횟수',
      series: [0.2, 0.4, 0.6, 0.8, 0.9].flatMap((x) => [
        { x, y: x, series: '체이닝 α' },
        { x, y: 1 / (1 - x), series: '개방 주소법 1/(1-α)' },
      ]),
      annotations: [{ x: 0.9, y: 10, label: '높은 적재율에서 탐사 급증' }],
    }),
  ),
  writeFile(
    new URL('linked-list-access.svg', outputDirectory),
    createLineChart({
      title: '목표 위치에 따른 원소 접근 단계',
      xLabel: '목표 위치 k',
      yLabel: '접근 단계',
      series: [1, 2, 4, 8, 16].flatMap((x) => [
        { x, y: x, series: '연결 리스트 k' },
        { x, y: 1, series: '동적 배열 1' },
      ]),
      annotations: [{ x: 16, y: 16, label: '링크 순차 추적' }],
    }),
  ),
  writeFile(
    new URL('balanced-tree-height.svg', outputDirectory),
    createLineChart({
      title: '키 증가에 따른 균형 이진 트리 높이 상한',
      xLabel: '키 수 n',
      yLabel: '높이 상한',
      series: [2, 4, 8, 16, 32].flatMap((x) => [
        { x, y: 1.44 * Math.log2(x + 2) - 0.328, series: 'AVL 높이 상한' },
        { x, y: 2 * Math.log2(x + 1), series: '레드블랙 높이 상한' },
      ]),
      annotations: [{ x: 32, y: 1.44 * Math.log2(34) - 0.328, label: 'AVL의 강한 균형' }],
    }),
  ),
  writeFile(
    new URL('dp-epsilon-likelihood-bound.svg', outputDirectory),
    createLineChart({
      title: '프라이버시 예산에 따른 출력 확률비 상한',
      xLabel: '프라이버시 예산 ε',
      yLabel: '허용 확률비 상한 eᵋ',
      series: [0, 0.25, 0.5, 1, 1.5, 2, 3].map((x) => ({
        x,
        y: Math.exp(x),
        series: 'eᵋ',
      })),
      annotations: [
        { x: 1, y: Math.exp(1), label: 'ε=1: 2.72' },
        { x: 2, y: Math.exp(2), label: 'ε=2: 7.39' },
      ],
    }),
  ),
  writeFile(
    new URL('tree-traversal-stack-growth.svg', outputDirectory),
    createLineChart({
      title: '트리 형태별 순회 스택 공간 증가율',
      xLabel: '노드 수 n',
      yLabel: '복귀 문맥 수',
      series: [1, 2, 4, 8, 16].flatMap((x) => [
        { x, y: Math.log2(x), series: '균형 트리 log₂ n' },
        { x, y: x, series: '편향 트리 n' },
      ]),
      annotations: [{ x: 16, y: 16, label: '편향 시 깊이 n' }],
    }),
  ),
  writeFile(new URL('adversarial-perturbation.svg', outputDirectory), createAdversarialExampleChart()),
  writeFile(
    new URL('graph-frontier-growth.svg', outputDirectory),
    createLineChart({
      title: '이진 분기 깊이별 탐색 프런티어 크기',
      xLabel: '탐색 깊이 d',
      yLabel: '보관 노드 수',
      series: [1, 2, 3, 4, 5].flatMap((x) => [
        { x, y: 2 ** x, series: 'BFS 2ᵈ' },
        { x, y: x, series: 'DFS d' },
      ]),
      annotations: [{ x: 5, y: 32, label: 'BFS 큐 후보 급증' }],
    }),
  ),
  writeFile(
    new URL('ai-accelerator-roofline.svg', outputDirectory),
    createLineChart({
      title: '연산 집약도에 따른 AI 가속기 처리량 상한',
      xLabel: '연산 집약도(ops/byte)',
      yLabel: '이론 처리량(TOPS)',
      series: [1, 2, 4, 8, 16, 32, 64, 128, 256, 500, 1024].flatMap((x) => [
        { x, y: 0.2 * x, series: '메모리 대역폭 상한' },
        { x, y: 100, series: '최대 연산 성능' },
        { x, y: Math.min(100, 0.2 * x), series: '달성 가능 상한' },
      ]),
      annotations: [{ x: 500, y: 100, label: 'Ridge Point 500 ops/byte' }],
    }),
  ),
  writeFile(
    new URL('chiplet-die-yield.svg', outputDirectory),
    createLineChart({
      title: '다이 면적에 따른 상대 수율 모형',
      xLabel: '다이 면적 A(mm²)',
      yLabel: '상대 수율 exp(-D₀A)',
      series: [25, 50, 100, 200, 400].map((x) => ({
        x,
        y: Math.exp(-0.005 * x),
        series: '단일 다이 상대 수율',
      })),
      annotations: [{ x: 400, y: Math.exp(-2), label: '면적 증가 시 결함 노출 증가' }],
    }),
  ),
  writeFile(
    new URL('divide-conquer-depth.svg', outputDirectory),
    createLineChart({
      title: '분할 균형에 따른 최대 재귀 깊이',
      xLabel: '입력 크기 n',
      yLabel: '호출 깊이',
      series: [1, 2, 4, 8, 16].flatMap((x) => [
        { x, y: Math.log2(x), series: '균형 분할 log₂ n' },
        { x, y: x, series: '최악 불균형 n' },
      ]),
      annotations: [{ x: 16, y: 16, label: '불균형 시 스택 깊이 증가' }],
    }),
  ),
  writeFile(
    new URL('all-reduce-stage-growth.svg', outputDirectory),
    createLineChart({
      title: '참여자 수에 따른 All-Reduce 통신 단계 수',
      xLabel: '참여자 수 p',
      yLabel: '축약+배포 단계 수',
      series: [2, 4, 8, 16, 32].flatMap((x) => [
        { x, y: 2 * (x - 1), series: '링 2(p-1)' },
        { x, y: 2 * Math.log2(x), series: '트리 2log₂p' },
      ]),
      annotations: [{ x: 32, y: 62, label: '링 62단계·트리 10단계' }],
    }),
  ),
  writeFile(
    new URL('monte-carlo-standard-error.svg', outputDirectory),
    createLineChart({
      title: '표본 수 증가에 따른 상대 표준오차',
      xLabel: '표본 수 n',
      yLabel: '상대 표준오차(%)',
      series: [1, 4, 16, 64, 256].map((x) => ({
        x,
        y: 100 / Math.sqrt(x),
        series: '1/√n',
      })),
      annotations: [{ x: 64, y: 12.5, label: '표본 4배 → 오차 절반' }],
    }),
  ),
  writeFile(new URL('streaming-watermark.svg', outputDirectory), createStreamingWatermarkChart()),
  writeFile(new URL('pue-energy-breakdown.svg', outputDirectory), createPueBreakdownChart()),
  writeFile(
    new URL('gelu-swish-activation.svg', outputDirectory),
    createLineChart({
      title: 'GELU 활성과 SwiGLU의 Swish 게이트 성분',
      xLabel: '입력 x',
      yLabel: '활성값',
      series: [-3, -2, -1, 0, 1, 2, 3].flatMap((x) => [
        {
          x,
          y: 0.5 * x * (1 + Math.tanh(Math.sqrt(2 / Math.PI) * (x + 0.044715 * x ** 3))),
          series: 'GELU 근사',
        },
        { x, y: x / (1 + Math.exp(-x)), series: 'Swish' },
      ]),
      annotations: [{ x: -1, y: -1 / (1 + Math.E), label: '부드러운 음수 억제' }],
    }),
  ),
]);
