import React from 'react';
import { shallow, configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jest-enzyme';
import Login from '../components/Login';
import {PATHS} from "../constants";
import {Redirect} from 'react-router-dom';

configure({adapter: new Adapter()});

const isOnline = {
    currentUser: "Mr.Redux",
    addUser: () => null,
    setError: () => null,
};

const isOffline = {
    currentUser: null,
    addUser: () => null,
    setError: () => null,
};

describe('Login testing', () => {
    describe('When user is online', () => {
        const login = shallow(<Login {...isOnline}/>);
        it('Redirects', () => {
            expect(login.find('Redirect').length).toEqual(1)
        });
        it('Redirects to lobby list', () => {
            expect(login.containsMatchingElement(<Redirect to={PATHS.allRooms}/>)).toEqual(true)
        });
    });
    describe('When user is offline', () => {
        const login = shallow(<Login {...isOffline}/>);
        it('Contains a title', () => {
            expect(login.containsMatchingElement(<h2>Login</h2>)).toEqual(true)
        });
        it('Contains a single form', () => {
            expect(login.find('form').length).toEqual(1)
        });
    });
});