import {minusOrZero, ROOMS} from "../constants";

// reducer "editar una sala"
function itemEdit(item, action) {
    switch (action.type) {
        case 'ADD_PLAYER':
            return {...item, players: [...item.players, action.player]};
        case 'REMOVE_PLAYER':
            return {...item, players: item.players.filter(current => (current !== action.player))};
        case 'START_GAME':
            return {...item, game_has_started: true};
        default:
            return item
    }
}

// reducer "editar salas"
function allItemsEdit(items = [], action) {
    switch (action.type) {
        case 'REMOVE_ROOM':
            return items.filter(room => (room.id !== action.idRoom));
        case 'ADD_ROOM':
            const newRoom = {
                id: action.idRoom,
                name: action.name,
                owner: action.owner,
                players: [action.owner],
                max_players: action.max_players,
                game_has_started: false,
                game_id: action.idGame
            };
            return [...items.filter(room => (room.id !== action.idRoom)), newRoom];
        default:
            return items.map(function(room) {
                return (room.id === action.idRoom) ? itemEdit(room, action) : room
            });
    }
}

// reducer para editar la estructura contenedora de las salas
// REQUEST_ITEMS y END_FETCH solo se usan en hard fetch
export default function roomsEdit(rooms = {isFetching: 0, needsFetch: 1, items: []}, action) {
    switch (action.type) {
        case 'REQUEST_ITEMS':
            return (action.itemType === ROOMS)
                ? {...rooms, isFetching: rooms.isFetching + 1}
                : rooms;
        case 'RECEIVE_ITEMS':
            return (action.itemType === ROOMS)
                ? {...rooms, needsFetch: minusOrZero(rooms.needsFetch), items: action.items}
                : rooms;
        case 'END_FETCH':
            return (action.itemType === ROOMS)
                ? {...rooms, isFetching: rooms.isFetching - 1}
                : rooms;
        case 'REMOVE_USER':
            return {...rooms, needsFetch: rooms.needsFetch + 1};
        default:
            return {...rooms, items: allItemsEdit(rooms.items, action)};
    }
}
