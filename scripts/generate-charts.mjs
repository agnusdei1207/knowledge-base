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
]);
