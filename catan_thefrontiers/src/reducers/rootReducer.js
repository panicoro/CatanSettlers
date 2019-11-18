import {combineReducers} from "redux";
import roomsEdit from "./roomsReducers";
import boardsEdit from "./boardsReducers";
import userEdit from "./userReducers";
import gamesEdit from "./gamesReducers";
import errorEdit from "./errorReducers";

const rootReducer = combineReducers({
    user: userEdit,
    rooms: roomsEdit,
    boards: boardsEdit,
    games: gamesEdit,
    error: errorEdit
});

export default rootReducer
