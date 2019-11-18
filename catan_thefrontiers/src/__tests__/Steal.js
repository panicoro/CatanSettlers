import React from 'react';
import { shallow, configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jest-enzyme';
import Steal from '../components/Steal';

configure({adapter: new Adapter()});

const conF = {
    
};

describe('Steal testing', () => {
    describe('Contains form', () => {
        const comm = shallow(<Steal {...conF}/>);
        it('Contains a single form', () => {
            expect(comm.find('Form').length).toEqual(1)
        });
    });
});