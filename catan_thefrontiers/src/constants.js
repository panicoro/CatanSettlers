export const ROOMS = 'rooms';
export const BOARDS = 'boards';
export const GAMES = 'games';

export const REFRESH_RATE_ROOMS = 5000;
export const REFRESH_RATE_GAMES = 5000;
export const ERROR_TIMER = 20000;

export const isUndefined = item => (typeof(item) === "undefined");
export const isNull = item => (item === null);
export const minusOrZero = number => (number > 0) ? number - 1 : 0;
export function arrayCompare (arr1, arr2) {
        if (arr1.length !== arr2.length) {
                return false
        } else {
                for (var i = 0; i < arr1.length; i++) {
                        if (arr1[i] !== arr2[i]) {
                                return false
                        }
                }
                return true
        }
}

export const vertexGrid =
    [
        [{level:2, index:28},{level:2, index:0},{level:2, index:2}],
        [{level:2, index:27},{level:2, index:29},{level:2, index:1},{level:2, index:3}],
        [{level:2, index:26},{level:1, index:17},{level:1, index:1},{level:2, index:4}],
        [{level:2, index:25},{level:1, index:16},{level:1, index:0},{level:1, index:2},{level:2, index:5}],
        [{level:2, index:24},{level:1, index:15},{level:0, index:0},{level:1, index:3},{level:2, index:6}],
        [{level:2, index:23},{level:1, index:14},{level:0, index:5},{level:0, index:1},{level:1, index:4},{level:2, index:7}],
        [{level:2, index:22},{level:1, index:13},{level:0, index:4},{level:0, index:2},{level:1, index:5},{level:2, index:8}],
        [{level:2, index:21},{level:1, index:12},{level:0, index:3},{level:1, index:6},{level:2, index:9}],
        [{level:2, index:20},{level:1, index:11},{level:1, index:9},{level:1, index:7},{level:2, index:10}],
        [{level:2, index:19},{level:1, index:10},{level:1, index:8},{level:2, index:11}],
        [{level:2, index:18},{level:2, index:16},{level:2, index:14},{level:2, index:12}],
        [{level:2, index:17},{level:2, index:15},{level:2, index:13}]
    ];

export const ERRORS = {
        notValidRoom: "Sala inválida; ¿La partida ya terminó?",
        notValidGame: "Partida inválida; ¿Esta ya terminó?",
        gameHasStarted: "¡Esta partida ya empezó!",
        fullRoom: "Oops! Sala llena.",
        notLogged: "No puede hacer eso sin una cuenta. ¿No tiene cuenta? ¡El registro es gratuito!",
        logged: "Ya está logueado con una cuenta. Para entrar con otra, cierre sesión primero.",
        serverError: "Error interno del servidor. Espere unos momentos y vuelva a intentarlo. Si el problema persiste, por favor póngase en contacto con un administrador.",
        fatalServerError: "El servidor no respondió. Si el problema persiste, por favor póngase en contacto con un administrador.",
        roomTooLate: "Oops! Esa partida se llenó o empezó a último momento!",
        loginInvalid: "Usuario o contraseña inválidos; por favor, intente nuevamente.",
        registerInvalid: "Registro rechazado. ¡Quizás ese usuario ya esté en uso!",
        createRoomInvalid: "Creación rechazada. ¡Quizás ese nombre de partida ya esté en uso!",
};

// direcciones del front-end; solo hace falta revisar el correcto
// funcionamiento del router despues de cambiar alguna ruta.
export const PATHS = {
        home: "/",
        createRoom: "/rooms/create",
        genericRoom: "/rooms/:id",
        room: id => `/rooms/${id}`,
        allRooms: "/rooms",
        login: "/users/login",
        register: "/users/register",
        genericGame: "/games/:id",
        game: id => `/games/${id}`,
        logout: "/users/logout",
};

// direcciones de la API; solo hace falta revisar el correcto funcionamiento
// de las acciones asincronas despues de cambiar una ruta.
export const API = {
        register: "/users/",
        login: "/users/login/",
        boards: `/${BOARDS}`,
        rooms: `/${ROOMS}`,
        genericRoom: `/${ROOMS}/*`,
        room: id => `/${ROOMS}/${id}`,
        games: `/${GAMES}`,
        genericGame: `/${GAMES}/*`,
        game: id => `/${GAMES}/${id}`,
        gameBoard: id => `/${GAMES}/${id}/board`,
        player: id => `/${GAMES}/${id}/player`,
        genericPlayerActions: `${GAMES}/*/player/actions`,
        playerActions: id => `/${GAMES}/${id}/player/actions`,
        transactions: id => `/${GAMES}/${id}/transactions`,
};

export const CODES = {
        info: code => (code >= 100 && code < 200),
        success: code => (code >= 200 && code < 300),
        redirect: code => (code >= 300 && code < 400),
        clientError: code => (code >= 400 && code < 500),
        serverError: code => (code >= 500 && code < 600),
};

export const ACTIONS = {
        buildSett: "build_settlement",
        upgradeCity: "upgrade_city",
        buildRoad: "build_road",
        moveRobber: "move_robber",
        buyCard: "buy_card",
        playKnight: "play_knight_card",
        playRoad: "play_road_building_card",
        playMonopoly: "play_monopoly_card",
        playPlenty: "play_year_of_plenty_card",
        endTurn: "end_turn",
        bankTrade: "bank_trade",
};

export const validActions = [ACTIONS.buildSett,ACTIONS.upgradeCity,ACTIONS.buildRoad];
