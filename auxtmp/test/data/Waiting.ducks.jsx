export const notOwnerState = {
  room: {
    id: 1,
    name: ' ',
    owner: ' ',
    players: [],
    max_players: 2,
    game_has_started: false,
  },
  onStart: null,
  onCancel: null,
};

export const ownerState = {
  room: {
    id: 1,
    name: ' ',
    owner: ' ',
    players: [],
    max_players: 2,
    game_has_started: false,
  },
  onStart: () => {},
  onCancel: () => {},
};

export const ownerContainer = {
  username: 'owner',
  room: {
    id: 1,
    name: 'name',
    owner: 'owner',
    players: ['player'],
    max_players: 2,
    game_has_started: false,
  },
  setRoom: () => {},
};

export const notOwnerContainer = {
  username: 'notOwner',
  room: {
    id: 1,
    name: 'name',
    owner: 'owner',
    players: ['player'],
    max_players: 2,
    game_has_started: false,
  },
  setRoom: () => {},
};
