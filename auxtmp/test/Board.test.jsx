import { expect } from 'chai';
import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import React from 'react';

import { Board } from '../src/containers/Board/Board';
import {
  cities, hexagons, roads, robber, settlements,
} from '../src/utils/BoardData';


// This connects enzyme to the react adapter.
configure({ adapter: new Adapter() });

// eslint-disable-next-line react/jsx-props-no-spreading
const mk = (state) => shallow(<Board {...state} />);

const st = {
  cities,
  hexagons,
  roads,
  robber,
  settlements,
  setDraw: () => {},
};

describe('Board', () => {
  it('should render without crashing', () => {
    const b = mk(st);
    expect(b.isEmptyRender(), b.debug()).to.be.false;
  });

  it('should be <div id="board">', () => {
    const b = mk(st);
    expect(b.equals(<div id="board" />), b.debug()).to.be.true;
  });
});
