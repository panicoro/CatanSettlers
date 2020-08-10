/* eslint-disable no-console */
import data from './Data';
import { resourceNames } from './Constants';


const mkPromise = (x) => (
  new Promise((res) => {
    setTimeout(() => {
      console.log('Got response');
      res(x && JSON.parse(JSON.stringify(data[x])));
    }, Math.random() * data.timeout);
  })
);

/* Game */
export const getGameStatus = (id, onSuccess, onFailure) => {
  console.log('Getting game status', id);

  const p0 = mkPromise('actions');
  const p1 = mkPromise('board');
  const p2 = mkPromise('hand');
  const p3 = mkPromise('info');

  Promise.all([p0, p1, p2, p3])
    .then((rs) => {
      if (data.getGameStatus) onFailure();
      else onSuccess(...rs);
    });
};

export const buyCard = (id, onSuccess, onFailure) => {
  console.log('Buying card', id);

  mkPromise()
    .then(() => {
    // Decrement number of cards to buy.
      data.cardsToBuy -= 1;
      if (data.cardsToBuy === 0) {
      // Find action index and remove it.
        const actionId = data.actions.findIndex((x) => x && x.type === 'buy_card');
        delete data.actions[actionId];
      }

      data.actions = JSON.parse(JSON.stringify(data.actions));

      if (data.buyCard) onFailure();
      else onSuccess();
    });
};

export const buildCity = (id, pos, onSuccess, onFailure) => {
  console.log('Building city', id, pos);

  mkPromise()
    .then(() => {
      // Update response.
      data.board.cities = JSON.parse(JSON.stringify(data.board.cities));
      data.board.cities[0].positions.push(pos);

      // Find action index.
      const actionId = data.actions.findIndex((x) => x && x.type === 'upgrade_city');
      // Find payload index.
      const posId = data.actions[actionId].payload
        .findIndex((x) => (x
          && x.level === pos.level && x.index === pos.index));
      // Remove from available positions.
      data.actions[actionId].payload.splice(posId, 1);
      if (data.actions[actionId].payload.length === 0) delete data.actions[actionId];

      if (data.buildCity) onFailure();
      else onSuccess();
    });
};

export const buildRoad = (id, pos, onSuccess, onFailure) => {
  console.log('Building road', id, pos);

  mkPromise()
    .then(() => {
      // Update response.
      data.board.roads = JSON.parse(JSON.stringify(data.board.roads));
      data.board.roads[0].positions.push(pos);

      // Find action index.
      const actionId = data.actions.findIndex((x) => x && x.type === 'build_road');

      // Find payload index.
      const posId = data.actions[actionId].payload
        .findIndex((x) => (x
          && x[0].level === pos[0].level && x[0].index === pos[0].index
          && x[1].level === pos[1].level && x[1].index === pos[1].index));

      // Remove from available positions.
      data.actions[actionId].payload.splice(posId, 1);
      if (data.actions[actionId].payload.length === 0) delete data.actions[actionId];

      if (data.buildRoad) onFailure();
      else onSuccess();
    });
};

export const buildSettlement = (id, pos, onSuccess, onFailure) => {
  console.log('Building settlement', id, pos);

  mkPromise()
    .then(() => {
      // Update response.
      data.board.settlements = JSON.parse(JSON.stringify(data.board.settlements));
      data.board.settlements[0].positions.push(pos);

      // Find action index.
      const actionId = data.actions.findIndex((x) => x && x.type === 'build_settlement');
      // Find payload index.
      const posId = data.actions[actionId].payload
        .findIndex((x) => (x
          && x.level === pos.level && x.index === pos.index));
      // Remove from available positions.
      data.actions[actionId].payload.splice(posId, 1);
      if (data.actions[actionId].payload.length === 0) delete data.actions[actionId];

      if (data.buildSettlement) onFailure();
      else onSuccess();
    });
};

export const bankTrade = (id, offer, request, onSuccess, onFailure) => {
  console.log('Buying resource', offer, request, id);

  mkPromise()
    .then(() => {
      // Decrement number of resources to buy.
      data.resourcesToBuy -= 1;
      if (data.resourcesToBuy === 0) {
        // Find action index and remove it.
        const actionId = data.actions.findIndex((x) => x && x.type === 'bank_trade');
        delete data.actions[actionId];
      }

      data.actions = JSON.parse(JSON.stringify(data.actions));

      if (data.bankTrade) onFailure();
      else onSuccess();
    });
};

export const endTurn = (id, onSuccess, onFailure) => {
  console.log('Ending turn');

  mkPromise()
    .then(() => {
      const { players, currentTurn } = data.info;
      const next = (players.findIndex((p) => p.username === currentTurn.user) + 1) % players.length;

      currentTurn.user = players[next].username;
      currentTurn.dice = [Math.ceil(Math.random() * 6), Math.ceil(Math.random() * 6)];
      // Comment next line to see a fluid game.
      data.actions = [];

      if (data.endTurn) onFailure();
      else onSuccess();
    });
};

/* Rooms */
export const getRooms = (onSuccess, onFailure) => {
  console.log('Getting rooms');

  mkPromise('rooms')
    .then((rooms) => {
      if (data.getRooms) onFailure();
      else onSuccess(rooms);
    });
};

export const joinRoom = (id, onSuccess, onFailure) => {
  console.log('Joining room', id);

  mkPromise()
    .then(() => {
      const username = localStorage.getItem('username');
      const room = data.rooms.find((r) => r && r.id === Number(id));
      room.players.push(username);

      if (data.joinRoom) onFailure();
      else onSuccess();
    });
};

export const getBoards = (onSuccess, onFailure) => {
  console.log('Getting boards');

  mkPromise('boards')
    .then((b) => {
      if (data.joinRoom) onFailure();
      else onSuccess(b);
    });
};

export const createRoom = (name, boardId, onSuccess, onFailure) => {
  console.log('Creating room', name, boardId);

  mkPromise()
    .then(() => {
      if (data.joinRoom) onFailure();
      else onSuccess(JSON.parse(JSON.stringify(data.rooms[0])));
    });
};


export const signup = (username, password, onSuccess, onFailure) => {
  console.log('Signing up', username, password);

  mkPromise()
    .then(() => {
      // Check if user is registered.
      const found = data.users.find((user) => user.username === username);
      if (found) {
        onFailure(Error('User is already registered'));
      } else {
        // Register.
        data.users = [...data.users, { username, password }];
        onSuccess();
      }
    });
};

export const login = (username, password, onSuccess, onFailure) => {
  console.log('Logging in', username, password);

  mkPromise()
    .then(() => {
      // Check if user is registered.
      const user = data.users.find((x) => x.username === username);
      const pass = data.users.find((x) => x.password === password);
      if (user && pass) {
        onSuccess({ token: 'token' });
      } else if (!user) {
        onFailure(Error('Failed to login: You are not registered'));
      } else if (!pass) {
        onFailure(Error('Failed to login: Password invalid'));
      }
    });
};

export const getRoom = (id, onSuccess, onFailure) => {
  console.log('Got room', id);

  mkPromise()
    .then(() => {
      const room = data.rooms.find((r) => r && r.id === Number(id));

      if (!data.waiting[id]) data.waiting[id] = data.totalWait;

      data.waiting[id] -= 1;
      if (data.waiting[id] <= 0) {
        room.game_has_started = true;
        room.game_id = 1;
        data.rooms[data.rooms.indexOf(room)] = { ...room };
      }

      if (data.getRoom) onFailure(500);
      else if (data.canceledRooms) onFailure(404);
      else onSuccess(room);
    });
};

export const startGame = (id, onSuccess, onFailure) => {
  console.log('Started game');

  mkPromise()
    .then(() => {
      const room = data.rooms.find((r) => r && r.id === Number(id));
      room.game_has_started = true;
      room.game_id = 2;
      data.rooms = [...data.rooms];

      if (data.startGame) onFailure(500);
      else onSuccess();
    });
};

export const cancelRoom = (id, onSuccess = () => {}, onFailure) => {
  console.log('Room canceled', id);

  mkPromise()
    .then(() => {
      const room = data.rooms.find((r) => r && r.id === Number(id));
      data.rooms.splice(data.rooms.indexOf(room), 1);

      if (data.cancelRoom) onFailure();
      else onSuccess();
    });
};

const robber = (position, username) => mkPromise().then(() => {
  data.board.robber = position;

  const targetUser = data.info.players.find((p) => (
    p && p.username === username));

  if (username && targetUser.resourcesCards >= 1) {
  // Remove resource from opponent's hand.
    targetUser.resourcesCards -= 1;

    // Get random resource.
    const resourceId = Math.floor(Math.random() * resourceNames.length);
    data.hand.resources.push(resourceNames[resourceId]);

    // Update info.
    const localUsername = localStorage.getItem('username') || 'test';
    const localUser = data.info.players.find((p) => (
      p && p.username === localUsername));
    localUser.resourcesCards += 1;
  }
});

export const moveRobber = (id, position, username, onSuccess, onFailure) => {
  console.log('Moving robber', id);

  // Remove action.
  const aId = data.actions.findIndex((x) => x && x.type === 'move_robber');
  data.actions.splice(aId, 1);

  // If knight card is available, update positions.
  const kId = data.actions.findIndex((x) => x && x.type === 'play_knight_card');

  if (kId !== -1) {
    const posId = data.actions[kId].payload.findIndex((x) => (x
      && x.position.level === position.level
      && x.position.index === position.index));

    // Remove chosen position.
    data.actions[kId].payload.splice(posId, 1);

    // Add previous position.
    data.actions[kId].payload.push({ position: data.board.robber, players: [] });
  }

  robber(position, username)
    .then(() => {
      if (data.moveRobber) onFailure();
      else onSuccess();
    });
};

export const playKnight = (id, position, username, onSuccess, onFailure) => {
  console.log('Playing knight card', id);

  // Update info.
  const localUsername = localStorage.getItem('username');
  const localUser = data.info.players.find((p) => (
    p && p.username === localUsername));
  localUser.developmentCards -= 1;

  // Remove card.
  const cId = data.hand.cards.findIndex((x) => x === 'knight');
  data.hand.cards.splice(cId, 1);

  const aId = data.actions.findIndex(
    (x) => x && x.type === 'play_knight_card',
  );

  // Remove action or position.
  if (!data.hand.cards.find(((x) => x === 'knight'))) {
    data.actions.splice(aId, 1);
  } else {
    const posId = data.actions[aId].payload.findIndex((x) => (x
      && x.position.level === position.level
      && x.position.index === position.index));

    // Remove chosen position.
    data.actions[aId].payload.splice(posId, 1);

    // Add previous position.
    data.actions[aId].payload.push({ position: data.board.robber, players: [] });
  }

  robber(position, username)
    .then(() => {
      if (data.moveRobber) onFailure();
      else onSuccess();
    });
};

export const play2Roads = (id, p0, p1, onSuccess, onFailure) => {
  console.log('Playing 2 Roads', id);

  mkPromise()
    .then(() => {
      data.board.roads[0].positions.push(p0);
      data.board.roads[0].positions.push(p1);

      // Update info.
      const localUsername = localStorage.getItem('username');
      const localUser = data.info.players.find((p) => (
        p && p.username === localUsername));
      localUser.developmentCards -= 1;

      // Remove card.
      const cId = data.hand.cards.findIndex((x) => x === 'road_building');
      data.hand.cards.splice(cId, 1);

      const aId = data.actions.findIndex(
        (x) => x && x.type === 'play_road_building_card',
      );

      // Remove action or position.
      if (!data.hand.cards.some(((x) => x === 'road_building'))) {
        data.actions.splice(aId, 1);
      } else {
        const pId0 = data.actions[aId].payload
          .findIndex((x) => (x
            && x[0].level === p0[0].level && x[0].index === p0[0].index
            && x[1].level === p0[1].level && x[1].index === p0[1].index));
        const pId1 = data.actions[aId].payload
          .findIndex((x) => (x
            && x[0].level === p1[0].level && x[0].index === p1[0].index
            && x[1].level === p1[1].level && x[1].index === p1[1].index));

        // Remove chosen position.
        data.actions[aId].payload.splice(pId0, 1);
        data.actions[aId].payload.splice(pId1, 1);
      }

      if (data.play2Roads) onFailure();
      else onSuccess();
    });
};
