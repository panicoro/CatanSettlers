import React from 'react';
import { shallow, configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jest-enzyme';
import Commerce from '../components/Commerce';

configure({adapter: new Adapter()});

const conF = {
    res: {
        ore: 4,
        lumber: 3,
        brick:6,
        wool:1,
        grain:10
    }
};

describe('Commerce testing', () => {
    describe('Contains form', () => {
        const comm = shallow(<Commerce {...conF}/>);
        it('Contains a single form', () => {
            expect(comm.find('Form').length).toEqual(1)
        });
    });
});