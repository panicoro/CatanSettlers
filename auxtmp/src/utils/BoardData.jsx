export const boards = [
  { id: 1, name: 'board1' },
  { id: 2, name: 'board2' },
  { id: 3, name: 'board3' },
];

export const cards = [
  'road_building',
  'road_building',
  'knight',
  'knight',
  'knight',
];

export const cities = [
  {
    colour: '#ff0000',
    positions: [
      { level: 2, index: 15 },
    ],
  },
  {
    colour: '#00ff00',
    positions: [
      { level: 1, index: 17 },
    ],
  },
  {
    colour: '#0000ff',
    positions: [
      { level: 1, index: 1 },
    ],
  },
];

export const hexagons = [
  {
    position: { level: 0, index: 0 },
    terrain: 'desert',
    token: 1,
  },
  {
    position: { level: 1, index: 0 },
    terrain: 'lumber',
    token: 2,
  },
  {
    position: { level: 1, index: 1 },
    terrain: 'wool',
    token: 2,
  },
  {
    position: { level: 1, index: 2 },
    terrain: 'brick',
    token: 3,
  },
  {
    position: { level: 1, index: 3 },
    terrain: 'ore',
    token: 4,
  },
  {
    position: { level: 1, index: 4 },
    terrain: 'ore',
    token: 5,
  },
  {
    position: { level: 1, index: 5 },
    terrain: 'ore',
    token: 6,
  },
  {
    position: { level: 2, index: 0 },
    terrain: 'ore',
    token: 8,
  },
  {
    position: { level: 2, index: 1 },
    terrain: 'grain',
    token: 8,
  },
  {
    position: { level: 2, index: 2 },
    terrain: 'ore',
    token: 9,
  },
  {
    position: { level: 2, index: 3 },
    terrain: 'ore',
    token: 10,
  },
  {
    position: { level: 2, index: 4 },
    terrain: 'ore',
    token: 11,
  },
  {
    position: { level: 2, index: 5 },
    terrain: 'ore',
    token: 12,
  },
  {
    position: { level: 2, index: 6 },
    terrain: 'ore',
    token: 2,
  },
  {
    position: { level: 2, index: 7 },
    terrain: 'ore',
    token: 3,
  },
  {
    position: { level: 2, index: 8 },
    terrain: 'ore',
    token: 4,
  },
  {
    position: { level: 2, index: 9 },
    terrain: 'ore',
    token: 5,
  },
  {
    position: { level: 2, index: 10 },
    terrain: 'ore',
    token: 6,
  },
  {
    position: { level: 2, index: 11 },
    terrain: 'ore',
    token: 6,
  },
];

export const resources = [
  'lumber',
  'lumber',
  'lumber',
  'lumber',
  'ore',
  'ore',
  'wool',
  'grain',
  'grain',
  'grain',
  'grain',
  'grain',
  'grain',
];

export const roads = [
  {
    colour: '#ff0000',
    positions: [
      [
        { level: 1, index: 12 },
        { level: 1, index: 13 },
      ],
      [
        { level: 1, index: 13 },
        { level: 2, index: 21 },
      ],
      [
        { level: 1, index: 8 },
        { level: 2, index: 14 },
      ],
      [
        { level: 2, index: 14 },
        { level: 2, index: 15 },
      ],
      [
        { level: 2, index: 15 },
        { level: 2, index: 16 },
      ],
      [
        { level: 2, index: 16 },
        { level: 2, index: 17 },
      ],
    ],
  },
  {
    colour: '#00ff00',
    positions: [
      [
        { level: 0, index: 2 },
        { level: 0, index: 3 },
      ],
      [
        { level: 0, index: 3 },
        { level: 0, index: 4 },
      ],
      [
        { level: 1, index: 17 },
        { level: 2, index: 29 },
      ],
    ],
  },
  {
    colour: '#0000ff',
    positions: [
      [
        { level: 1, index: 1 },
        { level: 1, index: 2 },
      ],
      [
        { level: 0, index: 5 },
        { level: 1, index: 15 },
      ],
      [
        { level: 1, index: 2 },
        { level: 2, index: 4 },
      ],
    ],
  },
];

export const info = {
  players: [
    {
      username: 'test',
      colour: '#ff0000',
      developmentCards: 5,
      resourceCards: 13,
      victoryPoints: 0,
      lastGained: [
      ],
    },
    {
      username: 'user2',
      colour: '#00ff00',
      developmentCards: 1,
      resourceCards: 6,
      victoryPoints: 1,
      lastGained: [
        'lumber',
      ],
    },
    {
      username: 'user3',
      colour: '#0000ff',
      developmentCards: 2,
      resourceCards: 5,
      victoryPoints: 2,
      lastGained: [
        'wool',
        'ore',
      ],
    },
  ],
  currentTurn: {
    user: 'test',
    dice: [3, 4],
  },
};

export const robber = { level: 0, index: 0 };

export const settlements = [
  {
    colour: '#ff0000',
    positions: [
      { level: 1, index: 8 },
      { level: 1, index: 12 },
    ],
  },
  {
    colour: '#00ff00',
    positions: [
      { level: 0, index: 2 },
      { level: 1, index: 17 },
    ],
  },
  {
    colour: '#0000ff',
    positions: [
      { level: 1, index: 15 },
    ],
  },
];
