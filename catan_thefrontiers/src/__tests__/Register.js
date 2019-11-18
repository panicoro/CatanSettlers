import React from 'react';
import { shallow, configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jest-enzyme';
import {PATHS} from "../constants";
import {Redirect} from 'react-router-dom';
import Register from "../components/Register";

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

describe('Register testing', () => {
    describe('When user is online', () => {
        const register = shallow(<Register {...isOnline}/>);
        it('Redirects', () => {
            expect(register.find('Redirect').length).toEqual(1)
        });
        it('Redirects to lobby list', () => {
            expect(register.containsMatchingElement(<Redirect to={PATHS.allRooms}/>)).toEqual(true)
        });
    });
    describe('When user is offline', () => {
        const register = shallow(<Register {...isOffline}/>);
        it('Contains a title', () => {
            expect(register.containsMatchingElement(<h2>Registrar Cuenta</h2>)).toEqual(true)
        });
        it('Contains a single form', () => {
            expect(register.find('form').length).toEqual(1)
        });
    });
});