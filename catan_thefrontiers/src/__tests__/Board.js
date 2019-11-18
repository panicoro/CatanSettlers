import React from 'react';
import { shallow, configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jest-enzyme';
import {PATHS} from "../constants";
import {Redirect} from 'react-router-dom'
import Board from "../components/Board";
import {actions0, game0, hexes0, player0} from "../apiMocks";

configure({adapter: new Adapter()});

// no logged user; as this should be the first check, we don't need any useful data
const isOffline = {
    id: 123,
    game: {},
    user: null,
    fetchGameSoft: () => null,
    fetchGameHard: () => null,
    setError: () => null,
};

// old/not existing data
const shouldFetch = {
    id: 123,
    game: {
        id: 123,
        isFetching: 0,
        needsFetch: 2,
        players: [],
        myActions: [],
        myResources: undefined,
        myCards: undefined,
        robber: undefined,
        current_turn: undefined,
        winner: undefined,
        board: undefined,
        game_has_started: true,
    },
    user: "Mr.Redux",
    fetchGameSoft: () => null,
    fetchGameHard: () => null,
    setError: () => null,
};

// API fetch in process
const isFetching = {
    id: 123,
    game: {
        id: 123,
        isFetching: 3,
        needsFetch: 0,
        players: [],
        myActions: [],
        myResources: undefined,
        myCards: undefined,
        robber: undefined,
        current_turn: undefined,
        winner: undefined,
        board: undefined,
        game_has_started: true,
    },
    user: "Mr.Redux",
    fetchGameSoft: () => null,
    fetchGameHard: () => null,
    setError: () => null,
};

// game does not exist (even having all data fetched before)
const noGame = {
    id: 123,
    game: {
        id: 123,
        isFetching: 0,
        needsFetch: 0,
        players: [],
        myActions: [],
        myResources: undefined,
        myCards: undefined,
        robber: undefined,
        current_turn: undefined,
        winner: undefined,
        board: undefined,
        game_has_started: true,
    },
    user: "Mr.Redux",
    fetchGameSoft: () => null,
    fetchGameHard: () => null,
    setError: () => null,
};

// user is not in the game
const isNotPlayer = {
    id: 123,
    game: {
        id: 123,
        isFetching: 0,
        needsFetch: 0,
        ...game0,
        myActions: [],
        myResources: undefined,
        myCards: undefined,
        board: hexes0.hexes,
        game_has_started: true,
    },
    user: "Mr.Redux",
    fetchGameSoft: () => null,
    fetchGameHard: () => null,
    setError: () => null,
};

// game has not started yet
const notStarted = {
    id: 123,
    game: {
        id: 123,
        isFetching: 0,
        needsFetch: 0,
        ...game0,
        myActions: [],
        myResources: undefined,
        myCards: undefined,
        board: hexes0.hexes,
        game_has_started: false,
    },
    user: "DonBarredora",
    fetchGameSoft: () => null,
    fetchGameHard: () => null,
    setError: () => null,
};

// game exists, has started, user is logged in, in game and in turn; data already fetched.
const myTurn = {
    id: 123,
    game: {
        id: 123,
        isFetching: 0,
        needsFetch: 0,
        ...game0,
        myActions: actions0,
        myResources: player0.resources,
        myCards: player0.cards,
        board: hexes0.hexes,
        game_has_started: true,
    },
    user: "DonBarredora",
    fetchGameSoft: () => null,
    fetchGameHard: () => null,
    setError: () => null,
};

// game exists, has started, user is logged in, in game but without turn; data already fetched.
const notMyTurn = {
    id: 123,
    game: {
        id: 123,
        isFetching: 0,
        needsFetch: 0,
        ...game0,
        myActions: actions0,
        myResources: player0.resources,
        myCards: player0.cards,
        board: hexes0.hexes,
        game_has_started: true,
    },
    user: "eva01",
    fetchGameSoft: () => null,
    fetchGameHard: () => null,
    setError: () => null,
};

// same as notMyTurn, but there is a winner proclaimed.
const withWinner = {
    id: 123,
    game: {
        id: 123,
        isFetching: 0,
        needsFetch: 0,
        ...{...game0, winner: "DonBarredora"},
        myActions: actions0,
        myResources: player0.resources,
        myCards: player0.cards,
        board: hexes0.hexes,
        game_has_started: true,
    },
    user: "eva01",
    fetchGameSoft: () => null,
    fetchGameHard: () => null,
    setError: () => null,
};

describe('Board testing', () => {
    describe('When user is not logged in', () => {
        const board = shallow(<Board {...isOffline}/>);
        it('Redirects', () => {
            expect(board.find('Redirect').length).toEqual(1);
        });
        it('Redirects to login', () => {
            expect(board.containsMatchingElement(<Redirect to={PATHS.login}/>)).toEqual(true);
        });
    });
    describe('When user is not in the game', () => {
        const board = shallow(<Board {...isNotPlayer}/>);
        it('Redirects', () => {
            expect(board.find('Redirect').length).toEqual(1);
        });
        it('Redirects to lobby list', () => {
            expect(board.containsMatchingElement(<Redirect to={PATHS.allRooms}/>)).toEqual(true);
        });
    });
    describe('When game does not exist', () => {
        const board = shallow(<Board {...noGame}/>);
        it('Redirects', () => {
            expect(board.find('Redirect').length).toEqual(1);
        });
        it('Redirects to lobby list', () => {
            expect(board.containsMatchingElement(<Redirect to={PATHS.allRooms}/>)).toEqual(true);
        });
    });
    describe('When game has not started', () => {
        const board = shallow(<Board {...notStarted}/>);
        it('Redirects', () => {
            expect(board.find('Redirect').length).toEqual(1);
        });
        it('Redirects to lobby list', () => {
            expect(board.containsMatchingElement(<Redirect to={PATHS.allRooms}/>)).toEqual(true);
        });
    });
    describe('When API fetch is in process', () => {
        const board = shallow(<Board {...isFetching}/>);
        it('Shows loading animation', () => {
            expect(board.find('Loading').length).toEqual(1)
        });
    });
    describe('When game and user are valid, but user does not have the turn', () => {
        const board = shallow(<Board {...notMyTurn}/>);
        it('Render the dices', () => {
            expect(board.find('Dice').length).toEqual(1)
        });
        it('Render exactly 19 hexagons', () => {
            expect(board.find('Hexagon').length).toEqual(19)
        });
        it('Render my cards', () => {
            expect(board.find('Cards').length).toEqual(1)
        });
        it('Render my resources', () => {
            expect(board.find('Resources').length).toEqual(1)
        });
        it('Do not render steal screen', () => {
            expect(board.find('Steal').length).toEqual(0)
        });
        it('Do not render commerce screen', () => {
            expect(board.find('Commerce').length).toEqual(0)
        });
        it('Do not render end turn button', () => {
            expect(board.find('button').length).toEqual(0)
        });
    });
    describe('When game and user are valid, and user has the turn', () => {
        const board = shallow(<Board {...myTurn}/>);
        it('Render the dices', () => {
            expect(board.find('Dice').length).toEqual(1)
        });
        it('Render exactly 19 hexagons', () => {
            expect(board.find('Hexagon').length).toEqual(19)
        });
        it('Render my cards', () => {
            expect(board.find('Cards').length).toEqual(1)
        });
        it('Render my resources', () => {
            expect(board.find('Resources').length).toEqual(1)
        });
        it('Render steal screen', () => {
            expect(board.find('Steal').length).toEqual(1)
        });
        it('Render commerce screen', () => {
            expect(board.find('Commerce').length).toEqual(1)
        });
        it('Render end turn button', () => {
            expect(board.find('button').length).toEqual(1)
        });
    });
    describe('When th API names a winner', () => {
        const board = shallow(<Board {...withWinner}/>);
        it('Render the Game Over title', () => {
            expect(board.containsMatchingElement(<h1>Partida terminada!</h1>)).toEqual(true);
        });
        it('Announce the winner', () => {
            expect(board.containsMatchingElement(<h3>{"Ganador: " + withWinner.game.winner}</h3>)).toEqual(true);
        });
    });
});