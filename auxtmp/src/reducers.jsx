import { combineReducers } from 'redux';

import Actions from './containers/Actions/Actions.ducks';
import Auth from './containers/Auth.ducks';
import Board from './containers/Board/Board.ducks';
import Game from './containers/Game/Game.ducks';
import Rooms from './containers/Rooms/Rooms.ducks';
import Info from './containers/Info/Info.ducks';

export default combineReducers({
  Actions,
  Auth,
  Board,
  Game,
  Rooms,
  Info,
});
