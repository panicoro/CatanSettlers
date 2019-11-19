import {
  getFromPlayers, getToken, path, request,
} from './ApiUtils';


/* Users */

export const signup = (username, password, onSuccess, onFailure) => {
  const url = `${path}/users/`;
  const data = { user: username, pass: password };
  const options = {
    method: 'POST',
    body: JSON.stringify(data),
  };

  request(url, options, onSuccess, onFailure, true);
};

export const login = (username, password, onSuccess, onFailure) => {
  const url = `${path}/users/login/`;
  const data = { user: username, pass: password };
  const options = {
    method: 'POST',
    body: JSON.stringify(data),
  };

  request(url, options, onSuccess, onFailure);
};


/* Boards */

export const getBoards = (onSuccess, onFailure) => {
  const url = `${path}/boards`;
  const options = { method: 'GET' };

  request(url, options, onSuccess, onFailure);
};


/* Rooms */

export const getRooms = (onSuccess, onFailure) => {
  const url = `${path}/rooms/`;
  const options = { method: 'GET' };

  request(url, options, onSuccess, onFailure);
};

export const createRoom = (name, id, onSuccess, onFailure) => {
  const url = `${path}/rooms/`;
  const data = { name, board_id: id };
  const options = {
    method: 'POST',
    body: JSON.stringify(data),
  };

  request(url, options, onSuccess, onFailure);
};

export const getRoom = (id, onSuccess, onFailure) => {
  const url = `${path}/rooms/${id}/`;
  const options = { method: 'GET' };

  request(url, options, onSuccess, onFailure);
};

export const startGame = (id, onSuccess, onFailure) => {
  const url = `${path}/rooms/${id}/`;
  const options = { method: 'PATCH' };

  request(url, options, onSuccess, onFailure, true);
};

export const cancelRoom = (id, onSuccess, onFailure) => {
  const url = `${path}/rooms/${id}/`;
  const options = { method: 'DELETE' };
  request(url, options, onSuccess, onFailure, true);
};

export const joinRoom = (id, onSuccess, onFailure) => {
  const url = `${path}/rooms/${id}/`;
  const options = { method: 'PUT' };

  request(url, options, onSuccess, onFailure, true);
};


/* Games */

export const getGameStatus = (id, onSuccess, onFailure) => {
  const endPoints = [
    `${path}/games/${id}/player/actions`,
    `${path}/games/${id}/board`,
    `${path}/games/${id}/player`,
    `${path}/games/${id}`,
  ];

  const options = {
    method: 'GET',
    headers: {
      Authorization: `Token ${getToken()}`,
      'Content-Type': 'application/json',
    },
  };

  // Fetch data from all endpoints.
  Promise.all(endPoints.map((e) => fetch(e, options)))

  // Once resolved, get json content.
    .then((rs) => Promise.all(
      rs.map((r) => {
        if (r.ok) return r.json();
        throw Error(r.statusText);
      }),
    ))

  // Return json content.
    .then(([actions, { hexes: hexagons }, hand, gameData]) => {
      const {
        settlements, cities, roads, players,
      } = getFromPlayers(gameData.players);

      const board = {
        hexagons,
        robber: gameData.robber,
        settlements,
        cities,
        roads,
      };
      const info = {
        players,
        currentTurn: gameData.current_turn,
        winner: gameData.winner,
      };

      onSuccess(actions, board, hand, info);
    })
    .catch(onFailure);
};


// Actions

export const playAction = (id, type, payload, onSuccess, onFailure) => {
  const url = `${path}/games/${id}/player/actions`;
  const data = { type, payload };
  const options = {
    method: 'POST',
    body: JSON.stringify(data),
  };

  request(url, options, onSuccess, onFailure, true);
};

export const bankTrade = (id, give, receive, onSuccess, onFailure) => {
  playAction(id, 'bank_trade', { give, receive }, onSuccess, onFailure);
};

export const buildCity = (id, pos, onSuccess, onFailure) => {
  playAction(id, 'upgrade_city', pos, onSuccess, onFailure);
};

export const buildRoad = (id, pos, onSuccess, onFailure) => {
  playAction(id, 'build_road', pos, onSuccess, onFailure);
};

export const buildSettlement = (id, pos, onSuccess, onFailure) => {
  playAction(id, 'build_settlement', pos, onSuccess, onFailure);
};

export const buyCard = (id, onSuccess, onFailure) => {
  playAction(id, 'buy_card', null, onSuccess, onFailure);
};

export const endTurn = (id, onSuccess, onFailure) => {
  playAction(id, 'end_turn', null, onSuccess, onFailure);
};

export const moveRobber = (id, position, player, onSuccess, onFailure) => {
  const body = player ? { position, player } : { position };

  playAction(id, 'move_robber', body, onSuccess, onFailure);
};

export const playKnight = (id, position, player, onSuccess, onFailure) => {
  const body = player ? { position, player } : { position };

  playAction(id, 'play_knight_card', body, onSuccess, onFailure);
};

export const play2Roads = (id, p0, p1, onSuccess, onFailure) => {
  playAction(id, 'play_road_building_card', [p0, p1], onSuccess, onFailure);
};
