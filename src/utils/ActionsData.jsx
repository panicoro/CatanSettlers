export const actions = [
  {
    type: 'upgrade_city',
    payload: [
      {
        level: 1,
        index: 8,
      },
      {
        level: 1,
        index: 12,
      },
    ],
  },
  {
    type: 'build_road',
    payload: [
      [
        {
          level: 1,
          index: 12,
        },
        {
          level: 0,
          index: 4,
        },
      ],
      [
        {
          level: 1,
          index: 12,
        },
        {
          level: 1,
          index: 11,
        },
      ],
      [
        {
          level: 1,
          index: 13,
        },
        {
          level: 1,
          index: 14,
        },
      ],
      [
        {
          level: 1,
          index: 8,
        },
        {
          level: 1,
          index: 9,
        },
      ],
      [
        {
          level: 1,
          index: 8,
        },
        {
          level: 1,
          index: 7,
        },
      ],
      [
        {
          level: 2,
          index: 14,
        },
        {
          level: 2,
          index: 13,
        },
      ],
      [
        {
          level: 2,
          index: 16,
        },
        {
          level: 1,
          index: 10,
        },
      ],
      [
        {
          level: 2,
          index: 17,
        },
        {
          level: 2,
          index: 18,
        },
      ],
      [
        {
          level: 2,
          index: 21,
        },
        {
          level: 2,
          index: 20,
        },
      ],
      [
        {
          level: 2,
          index: 21,
        },
        {
          level: 2,
          index: 22,
        },
      ],
    ],
  },
  {
    type: 'build_settlement',
    payload: [
      {
        level: 2,
        index: 17,
      },
      {
        level: 2,
        index: 21,
      },
    ],
  },
  {
    type: 'bank_trade',
  },
  {
    type: 'buy_card',
  },
  {
    type: 'move_robber',
    payload: [
      {
        position: { level: 1, index: 0 },
        players: ['user3'],
      },
      {
        position: { level: 1, index: 1 },
        players: ['user2'],
      },
      {
        position: { level: 1, index: 2 },
        players: ['user2'],
      },
      {
        position: { level: 1, index: 3 },
        players: [],
      },
      {
        position: { level: 1, index: 4 },
        players: ['user3'],
      },
      {
        position: { level: 1, index: 5 },
        players: ['user2', 'user3'],
      },
      {
        position: { level: 2, index: 0 },
        players: ['user2', 'user3'],
      },
      {
        position: { level: 2, index: 1 },
        players: ['user3'],
      },
      {
        position: { level: 2, index: 2 },
        players: [],
      },
      {
        position: { level: 2, index: 3 },
        players: [],
      },
      {
        position: { level: 2, index: 4 },
        players: [],
      },
      {
        position: { level: 2, index: 5 },
        players: [],
      },
      {
        position: { level: 2, index: 6 },
        players: [],
      },
      {
        position: { level: 2, index: 7 },
        players: [],
      },
      {
        position: { level: 2, index: 8 },
        players: [],
      },
      {
        position: { level: 2, index: 9 },
        players: [],
      },
      {
        position: { level: 2, index: 10 },
        players: ['user3'],
      },
      {
        position: { level: 2, index: 11 },
        players: ['user2'],
      },
    ],
  },
  {
    type: 'play_knight_card',
    payload: [
      {
        position: { level: 1, index: 0 },
        players: ['user3'],
      },
      {
        position: { level: 1, index: 1 },
        players: ['user2'],
      },
      {
        position: { level: 1, index: 2 },
        players: ['user2'],
      },
      {
        position: { level: 1, index: 3 },
        players: [],
      },
      {
        position: { level: 1, index: 4 },
        players: ['user3'],
      },
      {
        position: { level: 1, index: 5 },
        players: ['user2', 'user3'],
      },
      {
        position: { level: 2, index: 0 },
        players: ['user2', 'user3'],
      },
      {
        position: { level: 2, index: 1 },
        players: ['user3'],
      },
      {
        position: { level: 2, index: 2 },
        players: [],
      },
      {
        position: { level: 2, index: 3 },
        players: [],
      },
      {
        position: { level: 2, index: 4 },
        players: [],
      },
      {
        position: { level: 2, index: 5 },
        players: [],
      },
      {
        position: { level: 2, index: 6 },
        players: [],
      },
      {
        position: { level: 2, index: 7 },
        players: [],
      },
      {
        position: { level: 2, index: 8 },
        players: [],
      },
      {
        position: { level: 2, index: 9 },
        players: [],
      },
      {
        position: { level: 2, index: 10 },
        players: ['user3'],
      },
      {
        position: { level: 2, index: 11 },
        players: ['user2'],
      },
    ],
  },
  { type: 'end_turn' },
  {
    type: 'play_road_building_card',
    payload: [
      [
        {
          level: 1,
          index: 12,
        },
        {
          level: 0,
          index: 4,
        },
      ],
      [
        {
          level: 1,
          index: 12,
        },
        {
          level: 1,
          index: 11,
        },
      ],
      [
        {
          level: 1,
          index: 13,
        },
        {
          level: 1,
          index: 14,
        },
      ],
      [
        {
          level: 1,
          index: 8,
        },
        {
          level: 1,
          index: 9,
        },
      ],
      [
        {
          level: 1,
          index: 8,
        },
        {
          level: 1,
          index: 7,
        },
      ],
      [
        {
          level: 2,
          index: 14,
        },
        {
          level: 2,
          index: 13,
        },
      ],
      [
        {
          level: 2,
          index: 16,
        },
        {
          level: 1,
          index: 10,
        },
      ],
      [
        {
          level: 2,
          index: 17,
        },
        {
          level: 2,
          index: 18,
        },
      ],
      [
        {
          level: 2,
          index: 21,
        },
        {
          level: 2,
          index: 20,
        },
      ],
      [
        {
          level: 2,
          index: 21,
        },
        {
          level: 2,
          index: 22,
        },
      ],
    ],
  },
];

export default actions;
