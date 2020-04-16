/* eslint-disable */
import { expect } from 'chai';
import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import React from 'react';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import Game from '../../src/components/Game/Game';
/* eslint-disable import/no-named-as-default */
import Actions from '../../src/containers/Actions/Actions';
import Board from '../../src/containers/Board/Board';
import Hand from '../../src/containers/Hand';
import Info from '../../src/containers/Info/Info';
/* eslint-enable import/no-named-as-default */


// This connects enzyme to the react adapter.
configure({ adapter: new Adapter() });

describe('GameScreen', () => {
  it('should render without crashing', () => {
    const g = shallow(<Game />);
    expect(g.isEmptyRender(), g.debug()).to.be.false;
  });

  it('should have its four containers', () => {
    const g = shallow(<Game />);
    expect(g.contains(<Actions />)).to.be.true;
    expect(g.contains(<Hand />)).to.be.true;
    expect(g.contains(<Info />)).to.be.true;
    expect(g.contains(<Board />)).to.be.true;
  });

  it('should be displayed in Rows and Cols', () => {
    const g = shallow(<Game />);
    expect(g.find(Container)).to.have.lengthOf(1);
    expect(g.find(Row)).to.have.lengthOf(2);
    expect(g.find(Col)).to.have.lengthOf(4);
  });
});
