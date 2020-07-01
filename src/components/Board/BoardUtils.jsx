export const L = 90;
const r = Math.sqrt(L ** 2 - (L / 2) ** 2); // Adjacent side.
const k = L + L / 2;
const l = (Math.sqrt(3) / 2) * L;

// Should fit 5 hexagons.
export const WIDTH = (2 * 5 + 1) * r;
export const HEIGHT = WIDTH;
const w = WIDTH / 2;
const h = HEIGHT / 2;

export const buildingShape = {
  city: 'rect',
  settlement: 'circle',
};

export const buildingSize = {
  city: [L / 2, L / 2],
  settlement: [L / 2],
};

export const roadStroke = (colour) => ({
  color: colour,
  width: L / 5,
});

export const colour = {
  brick: '#cb7341',
  lumber: '#5a3300',
  wool: '#e8e8e8',
  grain: '#ecc16f',
  ore: '#7b7167',
  desert: '#c19a40',
};

export const hexPath = [[-L / 2, -l],
  [L / 2, -l],
  [L, 0],
  [L / 2, l],
  [-L / 2, l],
  [-L, 0],
];

export const hexCenter = {
  0: {
    0: { x: w, y: h },
  },
  1: {
    0: { x: w + r, y: h - k },
    1: { x: w + 2 * r, y: h },
    2: { x: w + r, y: h + k },
    3: { x: w - r, y: h + k },
    4: { x: w - 2 * r, y: h },
    5: { x: w - r, y: h - k },
  },
  2: {
    0: { x: w, y: h - 3 * L },
    1: { x: w + 2 * r, y: h - 3 * L },
    2: { x: w + 3 * r, y: h - (3 / 2) * L },
    3: { x: w + 4 * r, y: h },
    4: { x: w + 3 * r, y: h + (3 / 2) * L },
    5: { x: w + 2 * r, y: h + 3 * L },
    6: { x: w, y: h + 3 * L },
    7: { x: w - 2 * r, y: h + 3 * L },
    8: { x: w - 3 * r, y: h + (3 / 2) * L },
    9: { x: w - 4 * r, y: h },
    10: { x: w - 3 * r, y: h - (3 / 2) * L },
    11: { x: w - 2 * r, y: h - 3 * L },
  },
};

export const robberShape = 'circle';

export const robberSize = (3 / 5) * L;

export const vertexCenter = {
  0: {
    0: { x: w, y: h - L },
    1: { x: w + r, y: h - L / 2 },
    2: { x: w + r, y: h + L / 2 },
    3: { x: w, y: h + L },
    4: { x: w - r, y: h + L / 2 },
    5: { x: w - r, y: h - L / 2 },
  },
  1: {
    0: { x: w, y: h - 2 * L },
    1: { x: w + r, y: h - (5 / 2) * L },
    2: { x: w + 2 * r, y: h - 2 * L },
    3: { x: w + 2 * r, y: h - L },
    4: { x: w + 3 * r, y: h - L / 2 },
    5: { x: w + 3 * r, y: h + L / 2 },
    6: { x: w + 2 * r, y: h + L },
    7: { x: w + 2 * r, y: h + 2 * L },
    8: { x: w + r, y: h + (5 / 2) * L },
    9: { x: w, y: h + 2 * L },
    10: { x: w - r, y: h + (5 / 2) * L },
    11: { x: w - 2 * r, y: h + 2 * L },
    12: { x: w - 2 * r, y: h + L },
    13: { x: w - 3 * r, y: h + L / 2 },
    14: { x: w - 3 * r, y: h - L / 2 },
    15: { x: w - 2 * r, y: h - L },
    16: { x: w - 2 * r, y: h - 2 * L },
    17: { x: w - r, y: h - (5 / 2) * L },
  },
  2: {
    0: { x: w, y: h - 4 * L },
    1: { x: w + r, y: h - (7 / 2) * L },
    2: { x: w + 2 * r, y: h - 4 * L },
    3: { x: w + 3 * r, y: h - (7 / 2) * L },
    4: { x: w + 3 * r, y: h - (5 / 2) * L },
    5: { x: w + 4 * r, y: h - 2 * L },
    6: { x: w + 4 * r, y: h - L },
    7: { x: w + 5 * r, y: h - L / 2 },
    8: { x: w + 5 * r, y: h + L / 2 },
    9: { x: w + 4 * r, y: h + L },
    10: { x: w + 4 * r, y: h + 2 * L },
    11: { x: w + 3 * r, y: h + (5 / 2) * L },
    12: { x: w + 3 * r, y: h + (7 / 2) * L },
    13: { x: w + 2 * r, y: h + 4 * L },
    14: { x: w + r, y: h + (7 / 2) * L },
    15: { x: w, y: h + 4 * L },
    16: { x: w - r, y: h + (7 / 2) * L },
    17: { x: w - 2 * r, y: h + 4 * L },
    18: { x: w - 3 * r, y: h + (7 / 2) * L },
    19: { x: w - 3 * r, y: h + (5 / 2) * L },
    20: { x: w - 4 * r, y: h + 2 * L },
    21: { x: w - 4 * r, y: h + L },
    22: { x: w - 5 * r, y: h + L / 2 },
    23: { x: w - 5 * r, y: h - L / 2 },
    24: { x: w - 4 * r, y: h - L },
    25: { x: w - 4 * r, y: h - 2 * L },
    26: { x: w - 3 * r, y: h - (5 / 2) * L },
    27: { x: w - 3 * r, y: h - (7 / 2) * L },
    28: { x: w - 2 * r, y: h - 4 * L },
    29: { x: w - r, y: h - (7 / 2) * L },
  },
};
