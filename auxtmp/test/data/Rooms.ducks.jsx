export const initialState = {
  rooms: [],
  stage: 'empty',
  setError: () => {},
  setRunning: () => {},
  setRooms: () => {},
  setCreate: () => {},
};

export const errorState = {
  rooms: [],
  stage: 'error',
  setError: () => {},
  setRunning: () => {},
  setRooms: () => {},
  setCreate: () => {},
};

export const runningState = {
  rooms: [
    {
      id: 1,
      name: 'nombre1',
      owner: 'owner1',
      players: ['user1.1', 'user1.2', 'user1.3'],
      max_players: 1,
      game_has_started: false,
    },
    {
      id: 2,
      name: 'nombre2',
      owner: 'owner2',
      players: ['user2.1', 'user2.2'],
      max_players: 2,
      game_has_started: false,
    },
    {
      id: 3,
      name: 'nombre3',
      owner: 'owner3',
      players: ['user3.1', 'user3.2'],
      max_players: 3,
      game_has_started: true,
    },
  ],
  stage: 'running',
  setError: () => {},
  setRunning: () => {},
  setRooms: () => {},
  setCreate: () => {},
};
