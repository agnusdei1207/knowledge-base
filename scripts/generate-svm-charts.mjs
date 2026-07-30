import { mkdir, writeFile } from 'node:fs/promises';
import { JSDOM } from 'jsdom';
import * as Plot from '@observablehq/plot';
import * as vega from 'vega';
import { compile } from 'vega-lite';

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

  const svg = chart.tagName.toLowerCase() === 'svg' ? chart : chart.querySelector('svg');
  svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  svg.setAttribute('role', 'img');
  svg.setAttribute(
    'aria-label',
    '두 클래스와 최대 마진 결정 경계, 마진 경계, 서포트 벡터를 나타낸 Observable Plot 산점도',
  );
  return svg.outerHTML;
}

async function createVegaLitePlot() {
  const specification = {
    $schema: 'https://vega.github.io/schema/vega-lite/v6.json',
    width: 748,
    height: 390,
    background: '#f8fafc',
    title: {
      text: 'Vega-Lite — SVM 최대 마진과 서포트 벡터',
      font: 'system-ui',
      fontSize: 20,
      color: '#1f2937',
      offset: 18,
    },
    config: {
      axis: {
        labelFont: 'system-ui',
        titleFont: 'system-ui',
        labelFontSize: 14,
        titleFontSize: 16,
        gridColor: '#e2e8f0',
      },
      legend: {
        labelFont: 'system-ui',
        titleFont: 'system-ui',
        labelFontSize: 14,
      },
      view: { stroke: null },
    },
    layer: [
      {
        data: { values: boundaries.filter((line) => line.boundary !== '결정 경계') },
        mark: {
          type: 'line',
          stroke: '#64748b',
          strokeWidth: 2,
          strokeDash: [7, 6],
        },
        encoding: {
          x: {
            field: 'x1',
            type: 'quantitative',
            scale: { domain: [0, 10] },
            axis: { title: '특징 x₁' },
          },
          y: {
            field: 'x2',
            type: 'quantitative',
            scale: { domain: [0, 10] },
            axis: { title: '특징 x₂' },
          },
          detail: { field: 'boundary' },
          order: { field: 'order' },
        },
      },
      {
        data: { values: boundaries.filter((line) => line.boundary === '결정 경계') },
        mark: { type: 'line', stroke: '#111827', strokeWidth: 4 },
        encoding: {
          x: { field: 'x1', type: 'quantitative' },
          y: { field: 'x2', type: 'quantitative' },
          order: { field: 'order' },
        },
      },
      {
        data: { values: samples },
        mark: { type: 'point', filled: true, size: 180, stroke: 'white', strokeWidth: 1.5 },
        encoding: {
          x: { field: 'x1', type: 'quantitative' },
          y: { field: 'x2', type: 'quantitative' },
          color: {
            field: 'class',
            type: 'nominal',
            scale: { domain: Object.keys(colors), range: Object.values(colors) },
            legend: { title: '클래스' },
          },
          shape: {
            field: 'class',
            type: 'nominal',
            scale: { domain: ['클래스 A', '클래스 B'], range: ['circle', 'square'] },
            legend: { title: '표식' },
          },
        },
      },
      {
        data: { values: samples.filter((sample) => sample.support) },
        mark: {
          type: 'point',
          filled: false,
          size: 620,
          stroke: '#f59e0b',
          strokeWidth: 3,
        },
        encoding: {
          x: { field: 'x1', type: 'quantitative' },
          y: { field: 'x2', type: 'quantitative' },
        },
      },
      {
        data: {
          values: [
            { x1: 5.35, x2: 5.05, label: '결정 경계' },
            { x1: 2.1, x2: 6.55, label: '마진 경계' },
            { x1: 7.9, x2: 3.45, label: '마진 경계' },
            { x1: 6.0, x2: 6.5, label: '서포트 벡터' },
          ],
        },
        mark: {
          type: 'text',
          font: 'system-ui',
          fontSize: 15,
          fontWeight: 600,
          color: '#475569',
          dy: -8,
        },
        encoding: {
          x: { field: 'x1', type: 'quantitative' },
          y: { field: 'x2', type: 'quantitative' },
          text: { field: 'label' },
        },
      },
    ],
  };

  const runtime = vega.parse(compile(specification).spec);
  return new vega.View(runtime, { renderer: 'none' }).toSVG();
}

await mkdir(outputDirectory, { recursive: true });
await Promise.all([
  writeFile(new URL('svm-observable-plot.svg', outputDirectory), createObservablePlot()),
  writeFile(new URL('svm-vega-lite.svg', outputDirectory), await createVegaLitePlot()),
]);
