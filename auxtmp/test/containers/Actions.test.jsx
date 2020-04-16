/* eslint-disable */
import { expect } from 'chai';
import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';

import { Actions } from '../../src/containers/Actions/Actions';
import { initialState } from '../data/Actions.ducks';


// This connects enzyme to the react adapter.
configure({ adapter: new Adapter() });

const mk = (state) => shallow(
  <MemoryRouter
    initialEntries={['/games/1']}
    initialIndex={0}
  >
    {/* eslint-disable-next-line react/jsx-props-no-spreading */}
    <Actions {...state} />
  </MemoryRouter>,
);

describe('Actions', () => {
  it('should render without crashing', () => {
    const r = mk(initialState);
    expect(r.children().isEmptyRender(), r.debug()).to.be.false;
  });
});
