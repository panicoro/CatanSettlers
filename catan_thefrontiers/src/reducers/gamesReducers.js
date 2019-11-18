import {GAMES, minusOrZero, isUndefined} from "../constants";

// reducer para editar cada partida por id
function itemEdit(game, action) {
    switch (action.type) {
        case 'REQUEST_ITEMS':
            return (action.itemType === GAMES) ? {...game, isFetching: game.isFetching + 1} : game;
        case 'RECEIVE_ITEMS': {
            if (action.itemType === GAMES) {
                switch (action.optional) {
                    case 'board':
                        return {...game,
                            board : action.items.hexes,
                            needsFetch: minusOrZero(game.needsFetch)
                        };
                    case 'player/actions':
                        return {...game,
                            myActions: action.items,
                            needsFetch: minusOrZero(game.needsFetch)
                        };
                    case 'player':
                        return {
                            ...game,
                            myResources: action.items.resources,
                            myCards: action.items.cards,
                            needsFetch: minusOrZero(game.needsFetch)
                        };
                    default:  // undefined (general game data)
                        return {...game, ...action.items};
                }
            } else {
                return game;
            }
        }
        case 'END_FETCH':
            return (action.itemType === GAMES) ? {...game, isFetching: game.isFetching - 1} : game;
        case 'START_GAME':
            return {...game, game_has_started: true};
        default:
            return game
    }
}

// reducer para editar todas las partidas
export default function gamesEdit(games = [], action) {
    const newGame = {
        id: action.idGame,
        isFetching: 0,
        needsFetch: 3,
        players: [],
        myActions: [],
        myResources: undefined,
        myCards: undefined,
        robber: undefined,
        current_turn: undefined,
        winner: undefined,
        board: undefined,
        game_has_started: false,
    };
    switch (action.type) {
        case 'ADD_ROOM':
            return [...games.filter(game => (game.id !== action.idGame)), {...newGame, id: action.idGame}];
        case 'REMOVE_USER':
            return games.map(function(game) {
                return {...game, needsFetch: minusOrZero(game.needsFetch)}
            });
        default: {
            const anyIdMatch = (id, action) => ((!isUndefined(action.id) && id === action.id)
                || (!isUndefined(action.idGame) && id === action.idGame));
            if (games.some(game => anyIdMatch(game.id, action))) {
                return games.map(function(game) {
                    return (anyIdMatch(game.id, action)) ? itemEdit(game, action) : game
                });
            } else {
                return [
                    ...games,
                    itemEdit({...newGame, id: !isUndefined(action.id) ? action.id : action.idGame}, action)
                ];
            }
        }
    }
}
