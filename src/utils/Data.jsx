import {
  boards, cards, cities, hexagons,
  resources, roads, robber, settlements, info,
} from './BoardData';
import { actions } from './ActionsData';
import { room, rooms } from './RoomData';
import { users } from './UsersData';


const data = {
  timeout: 0,
  waiting: {},
  totalWait: 100,
  cardsToBuy: 3,
  resourcesToBuy: 3,
  actions,
  boards,
  board: {
    cities, hexagons, roads, robber, settlements,
  },
  hand: {
    resources,
    cards,
  },
  info,
  rooms,
  room,
  users,
};

export default data;
