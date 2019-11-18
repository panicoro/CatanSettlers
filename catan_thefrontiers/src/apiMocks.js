import {ACTIONS, API} from "./constants";

const axios = require('axios');
const MockAdapter = require('axios-mock-adapter');

const mock = new MockAdapter(axios);

const anyRoom = new RegExp(API.genericRoom);

const boards = [
    {id: 1, name: "Gallifrey"},
    {id: 3, name: "Ryloth"},
    {id: 4, name: "Baerlon"}
];

const rooms = [
    {
        id: 1,
        name: "Colonos1",
        owner: "Mr.Redux",
        players: ["Mr.Redux", "DonBarredora"],
        max_players: 4,
        game_has_started: false,
        game_id: 15249
    },
    {
        id: 2,
        name: "Colonos2",
        owner: "DonBarredora",
        players: ["Mr.Redux", "Fran", "DonBarredora"],
        max_players: 4,
        game_has_started: false,
        game_id: 2
    }
];

export const game0={
    players: [
        {
            username: 'DonBarredora',
            colour: "red",
            settlements: [],
            cities: [],
            roads: [],
            development_cards: 0,
            resources_cards: 0,
            victory_points: 0,
            last_gained: [],
        },
        {
            username: 'eva01',
            colour: "green",
            settlements: [],
            cities: [],
            roads: [],
            development_cards: 0,
            resources_cards: 0,
            victory_points: 0,
            last_gained: [],
        },
        {
            username: 'eva02',
            colour: "blue",
            settlements: [],
            cities: [],
            roads: [],
            development_cards: 0,
            resources_cards: 0,
            victory_points: 0,
            last_gained: [],
        },
    ],
    robber: {level: 0, index: 0},
    current_turn: {
        user: 'DonBarredora',
        dice: [4,1]
    },
    winner: '',
};

export const hexes0 = {
    hexes:
        [{token:'1',terrain: 'desert', HEX_POSITION: {level: 0, index: 0}},{token:'2',terrain: 'ore', HEX_POSITION: {level: 1, index: 0}},{token:'3',terrain: 'wheat',HEX_POSITION: {level: 1, index: 1}},
            {token:'4',terrain: 'ore',HEX_POSITION: {level: 1, index: 2}},{token:'5',terrain: 'wheat',HEX_POSITION: {level: 1, index: 3}},{token:'6',terrain: 'sheep',HEX_POSITION: {level: 1, index: 4}},{token:'8',terrain: 'brick', HEX_POSITION: {level: 1, index: 5}},
            {token:'9',terrain: 'lumber',HEX_POSITION: {level: 2, index: 0}},{token:'10',terrain: 'ore',HEX_POSITION: {level: 2, index: 1}},{token:'11',terrain: 'wheat',HEX_POSITION: {level: 2, index: 2}},{token:'12',terrain: 'sheep',HEX_POSITION: {level: 2, index: 3}},{token:'1',terrain: 'brick',HEX_POSITION: {level: 2, index: 4}},
            {token:'2',terrain: 'wheat',HEX_POSITION: {level: 2, index: 5}},{token:'3',terrain: 'sheep', HEX_POSITION: {level: 2, index: 6}},{token:'4',terrain: 'lumber', HEX_POSITION: {level: 2, index: 7}},{token:'5',terrain: 'brick',HEX_POSITION: {level: 2, index: 8}},
            {token:'6',terrain: 'lumber',HEX_POSITION: {level: 2, index: 9}},{token:'7',terrain: 'ore', HEX_POSITION: {level: 2, index: 10}},{token:'8',terrain: 'wheat', HEX_POSITION: {level: 2, index: 11}},
        ]
};

export const actions0 = [
    {
        type: ACTIONS.buildSett,
        payload: [{level:0 ,index: 0},{level:1 ,index: 4},{level:2 ,index: 6},{level:1 ,index: 8}]
    },
    {
        type: ACTIONS.buildRoad,
        payload: [[{level:0 ,index: 0},{level:1 ,index: 0}],[{level:0 ,index: 0},{level:0 ,index: 5}],[{level:0 ,index: 0},{level:0 ,index: 1}]]
    },
    {
        type: ACTIONS.upgradeCity,
        payload: [{level: 0, index: 0}, {level: 1, index: 4}, {level: 2, index: 6}, {level: 1, index: 8}],
    },
    {
        type: ACTIONS.moveRobber,
        payload: {
            position: {level:0 ,index: 0},
            players: ["eva02"]
        }
    },
    {
        type: ACTIONS.buyCard,
        payload: null
    },
    {
        type: ACTIONS.playKnight,
        payload: {
            position: {level:0 ,index: 0},
            players: ["eva02"]
        }
    },
    {
        type: ACTIONS.playRoad,
        payload: [[{level:0 ,index: 0},{level:1 ,index: 0}],[{level:0 ,index: 0},{level:0 ,index: 5}],[{level:0 ,index: 0},{level:0 ,index: 1}]]
    },
    {
        type: ACTIONS.playMonopoly,
        payload: null
    },
    {
        type: ACTIONS.playMonopoly,
        payload: null
    },
    {
        type: ACTIONS.playPlenty,
        payload: null
    },
    {
        type: ACTIONS.endTurn,
        payload: null
    },
    {
        type: ACTIONS.bankTrade,
        payload: null
    }
];

export const player0 = {
    resources: {
        brick: 5,
        lumber: 4,
        wool: 3,
        grain: 6,
        ore: 7
    },
    cards: {
        road_building: 2,
        year_of_plenty: 1,
        monopoly: 0,
        victory_point: 1,
        knight: 0,
    }
};

mock.onPost(API.login)
    .reply(200, {token: "6547aw5s1dvs65d4sdf1sd5fsd"});

mock.onPost(API.rooms)
    .reply(200, {id: Math.floor((Math.random() * 1000000) + 1), game_id: Math.floor((Math.random() * 1000000) + 1)});

mock.onDelete(anyRoom)
    .reply(200);

mock.onPatch(anyRoom)
    .reply(200);

mock.onPut(anyRoom)
    .reply(200);

mock.onPost(API.register)
    .reply(200);

mock.onGet(API.rooms)
    .reply(200, rooms);

mock.onGet(API.boards)
    .reply(200, boards);

mock.onGet(API.games)
    .reply(200);

mock.onGet(API.game(2))
    .reply(200, game0);

mock.onGet(API.gameBoard(2))
    .reply(200, hexes0);

mock.onGet(API.playerActions(2))
    .reply(200, actions0);

mock.onGet(API.player(2))
    .reply(200, player0);

mock.onPost(API.playerActions(2), {type: ACTIONS.buyCard, payload: null})
    .reply(200);

mock.reset();
mock.restore();

export default axios
