import React from 'react';
import { shallow, configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jest-enzyme';
import {PATHS} from "../constants";
import {Redirect} from 'react-router-dom';
import CreateLobby from "../components/CreateLobby";

configure({adapter: new Adapter()});

// no current user
const isOffline = {
    boards: [],
    isLoading: false,
    shouldFetch: false,
    currentUser: null,
    fetchBoardsHard: () => null,
    createRoom: () => null,
    setError: () => null,
};

// no boards, with a valid user
const noBoards = {
    boards: [],
    isLoading: false,
    shouldFetch: false,
    currentUser: "Mr.Redux",
    fetchBoardsHard: () => null,
    createRoom: () => null,
    setError: () => null,
};

// user and boards available
const allOk = {
    boards: [{id: 1, name: "Gallifrey"}, {id: 3, name: "Ryloth"}, {id: 4, name: "Baerlon"}],
    isLoading: false,
    shouldFetch: false,
    currentUser: "Mr.Redux",
    fetchBoardsHard: () => null,
    createRoom: () => null,
    setError: () => null,
};

// API fetch in process
const isLoading = {
    boards: [],
    isLoading: true,
    shouldFetch: false,
    currentUser: "Mr.Redux",
    fetchBoardsHard: () => null,
    createRoom: () => null,
    setError: () => null,
};

// old data
const shouldFetch = {
    boards: [],
    isLoading: false,
    shouldFetch: true,
    currentUser: "Mr.Redux",
    fetchBoardsHard: () => null,
    createRoom: () => null,
    setError: () => null,
};

describe('CreateLobby testing', () => {
    describe('When user is not logged in', () => {
        const createLobby = shallow(<CreateLobby {...isOffline}/>);
        it('Redirects', () => {
            expect(createLobby.find('Redirect').length).toEqual(1);
        });
        it('Redirects to login', () => {
            expect(createLobby.containsMatchingElement(<Redirect to={PATHS.login}/>)).toEqual(true);
        });
    });
    describe('When no boards are available', () => {
        const createLobby = shallow(<CreateLobby {...noBoards}/>);
        it('Shows custom message', () => {
            expect(createLobby.containsMatchingElement(<h1>Oops!</h1>)).toEqual(true);
        });
    });
    describe('When user is logged in and boards are available', () => {
        const createLobby = shallow(<CreateLobby {...allOk}/>);
        it('Contains a title', () => {
            expect(createLobby.containsMatchingElement(<h2>Crear Sala</h2>)).toEqual(true);
        });
        it('Contains a single form', () => {
            expect(createLobby.find('form').length).toEqual(1);
        });
    });
    describe('When API fetch is in process', () => {
        const createLobby = shallow(<CreateLobby {...isLoading}/>);
        it('Shows loading animation', () => {
            expect(createLobby.find('Loading').length).toEqual(1);
        });
    });
});