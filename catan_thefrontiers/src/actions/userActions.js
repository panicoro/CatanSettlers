// accion "agregar jugador a una sala"
export const addPlayer = (idRoom, player) => ({
    type: 'ADD_PLAYER',
    idRoom,
    player
});

// accion "quitar jugador de una sala"
export const removePlayer = (idRoom, player) => ({
    type: 'REMOVE_PLAYER',
    idRoom,
    player
});

// accion "eliminar sala"
export const removeRoom = idRoom => ({
    type: 'REMOVE_ROOM',
    idRoom
});

// accion "agregar/actualizar sala"
export const addRoom = (name, owner, max_players, idRoom, idGame) => ({
    type: 'ADD_ROOM',
    idRoom,
    name,
    owner,
    max_players,
    idGame,
});

// accion "empezar partida"
export const startGame = (idRoom, idGame) => ({
    type: 'START_GAME',
    idRoom,
    idGame
});

// accion "iniciar sesion" (regitrar usuario actual en el store)
export const addUser = (username, token) => ({
    type: 'ADD_USER',
    username,
    token
});

export const removeUser = () => ({
    type: 'REMOVE_USER'
});
