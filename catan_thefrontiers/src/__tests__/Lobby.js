import React from 'react';
import { shallow, configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jest-enzyme';
import Lobby from '../components/Lobby';
import {PATHS} from "../constants";
import {Redirect} from 'react-router-dom'

configure({adapter: new Adapter()});

// user is owner (of an existing room) but can't yet start the game
const isOwner = {
    id: 123,
    name: "Colonos23",
    owner: "DonBarredora",
    players: ["DonBarredora", "Mr.Redux"],
    max_players: 4,
    game_has_started: false,
    game_id: 456,
    isLoading: false,
    shouldFetch: false,
    currentUser: "DonBarredora",
    terminateLobby: () => null,
    startGame: () => null,
    fetchRoomsHard: () => null,
    fetchRoomsSoft: () => null,
    setError: () => null,
};

// user is the owner, and can manually start the game
const canStart = {
    id: 123,
    name: "Colonos23",
    owner: "DonBarredora",
    players: ["DonBarredora", "Mr.Redux", "Fran"],
    max_players: 4,
    game_has_started: false,
    game_id: 456,
    isLoading: false,
    shouldFetch: false,
    currentUser: "DonBarredora",
    terminateLobby: () => null,
    startGame: () => null,
    fetchRoomsHard: () => null,
    fetchRoomsSoft: () => null,
    setError: () => null,
};

// user is in the room (which exists) but is not owner
const isPlayer = {
    id: 123,
    name: "Colonos23",
    owner: "DonBarredora",
    players: ["DonBarredora", "Mr.Redux"],
    max_players: 4,
    game_has_started: false,
    game_id: 456,
    isLoading: false,
    shouldFetch: false,
    currentUser: "Mr.Redux",
    terminateLobby: () => null,
    startGame: () => null,
    fetchRoomsHard: () => null,
    fetchRoomsSoft: () => null,
    setError: () => null,
};

// user is not in the room
const isNotPlayer = {
    id: 123,
    name: "Colonos23",
    owner: "DonBarredora",
    players: ["DonBarredora", "Mr.Redux"],
    max_players: 4,
    game_has_started: false,
    game_id: 456,
    isLoading: false,
    shouldFetch: false,
    currentUser: "Fran",
    terminateLobby: () => null,
    startGame: () => null,
    fetchRoomsHard: () => null,
    fetchRoomsSoft: () => null,
    setError: () => null,
};

// no logged user; as this should be the first check, we don't need any useful data
const isOffline = {
    id: 123,
    name: undefined,
    owner: undefined,
    players: undefined,
    max_players: undefined,
    game_has_started: undefined,
    game_id: undefined,
    isLoading: false,
    shouldFetch: false,
    currentUser: null,
    terminateLobby: () => null,
    startGame: () => null,
    fetchRoomsHard: () => null,
    fetchRoomsSoft: () => null,
    setError: () => null,
};

// game has already started
const hasStarted = {
    id: 123,
    name: "Colonos23",
    owner: "DonBarredora",
    players: ["DonBarredora", "Mr.Redux", "Fran"],
    max_players: 4,
    game_has_started: true,
    game_id: 456,
    isLoading: false,
    shouldFetch: false,
    currentUser: "DonBarredora",
    terminateLobby: () => null,
    startGame: () => null,
    fetchRoomsHard: () => null,
    fetchRoomsSoft: () => null,
    setError: () => null,
};

// is fetching
const isLoading = {
    id: 123,
    name: "Colonos23",
    owner: "DonBarredora",
    players: ["DonBarredora", "Mr.Redux", "Fran"],
    max_players: 4,
    game_has_started: false,
    game_id: 456,
    isLoading: true,
    shouldFetch: false,
    currentUser: "Mr.Redux",
    terminateLobby: () => null,
    startGame: () => null,
    fetchRoomsHard: () => null,
    fetchRoomsSoft: () => null,
    setError: () => null,
};

// old data
const shouldFetch = {
    id: 123,
    name: "Colonos23",
    owner: "DonBarredora",
    players: ["DonBarredora", "Mr.Redux", "Fran"],
    max_players: 4,
    game_has_started: false,
    game_id: 456,
    isLoading: false,
    shouldFetch: true,
    currentUser: "Mr.Redux",
    terminateLobby: () => null,
    startGame: () => null,
    fetchRoomsHard: () => null,
    fetchRoomsSoft: () => null,
    setError: () => null,
};

// room does not exist (even having all data fetched before)
const noRoom = {
    id: 123,
    name: undefined,
    owner: undefined,
    players: undefined,
    max_players: undefined,
    game_has_started: undefined,
    game_id: undefined,
    isLoading: false,
    shouldFetch: false,
    currentUser: "Mr.Redux",
    terminateLobby: () => null,
    startGame: () => null,
    fetchRoomsHard: () => null,
    fetchRoomsSoft: () => null,
    setError: () => null,
};

describe('Lobby testing', () => {
    describe('When user is owner', () => {
        const lobby = shallow(<Lobby {...isOwner}/>);
        it('Has the name as a title', () => {
            expect(lobby.containsMatchingElement(<h2>{isOwner.name}</h2>)).toEqual(true);
        });
        it('Contains a list with as many members as players', () => {
            expect(lobby.find('li').length).toEqual(isOwner.players.length)
        });
        it('Contains 4 different buttons', () => {
            expect(lobby.find('button').length).toEqual(4)
        });
    });
    describe('When user is not owner', () => {
        const lobby = shallow(<Lobby {...isPlayer}/>);
        it('Has the name as a title', () => {
            expect(lobby.containsMatchingElement(<h2>{isPlayer.name}</h2>)).toEqual(true);
        });
        it('Contains a list with as many members as players', () => {
            expect(lobby.find('li').length).toEqual(isPlayer.players.length)
        });
        it('Contains 2 different buttons', () => {
            expect(lobby.find('button').length).toEqual(2)
        });
    });
    describe('When user is not logged in', () => {
        const lobby = shallow(<Lobby {...isOffline}/>);
        it('Redirects', () => {
            expect(lobby.find('Redirect').length).toEqual(1);
        });
        it('Redirects to login', () => {
            expect(lobby.containsMatchingElement(<Redirect to={PATHS.login}/>)).toEqual(true);
        });
    });
    describe('When user is not in the room', () => {
        const lobby = shallow(<Lobby {...isNotPlayer}/>);
        it('Redirects', () => {
            expect(lobby.find('Redirect').length).toEqual(1);
        });
        it('Redirects to lobby list', () => {
            expect(lobby.containsMatchingElement(<Redirect to={PATHS.allRooms}/>)).toEqual(true);
        });
    });
    describe('When room does not exist', () => {
        const lobby = shallow(<Lobby {...noRoom}/>);
        it('Redirects', () => {
            expect(lobby.find('Redirect').length).toEqual(1);
        });
        it('Redirects to lobby list', () => {
            expect(lobby.containsMatchingElement(<Redirect to={PATHS.allRooms}/>)).toEqual(true);
        });
    });
    describe('When game has started', () => {
        const lobby = shallow(<Lobby {...hasStarted}/>);
        it('Redirects', () => {
            expect(lobby.find('Redirect').length).toEqual(1);
        });
        it('Redirects to game', () => {
            expect(lobby.containsMatchingElement(<Redirect to={PATHS.game(hasStarted.game_id)}/>)).toEqual(true);
        });
    });
    describe('When API fetch is in process', () => {
        const lobby= shallow(<Lobby {...isLoading}/>);
        it('Shows loading animation', () => {
            expect(lobby.find('Loading').length).toEqual(1)
        });
    });
});