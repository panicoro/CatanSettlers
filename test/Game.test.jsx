import { expect } from 'chai';
import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';

import { Game } from '../src/containers/Game/Game';
import GameScreen from '../src/components/Game/Game';


// This connects enzyme to the react adapter.
configure({ adapter: new Adapter() });

const mk = (state) => shallow(
  <MemoryRouter
    initialEntries={['/game/1']}
    initialIndex={0}
  >
    {/* eslint-disable-next-line react/jsx-props-no-spreading */}
    <Game {...state} />
  </MemoryRouter>,
);

const emptyState = {
  stage: 'empty',
  setError: () => {},
  setRunningStage: () => {},
  setRefresh: () => {},
};

const errorState = {
  stage: 'error',
  setError: () => {},
  setRunningStage: () => {},
  setRefresh: () => {},
};

describe('Game', () => {
  it('should render without crashing', () => {
    const g = mk(emptyState);
    expect(g.isEmptyRender(), g.debug()).to.be.false;
  });

  it('should start empty', () => {
    const g = mk(emptyState).dive().dive();
    expect(g.matchesElement(<Game {...emptyState} />), g.debug()).to.be.true;
  });

  it('should show an error', () => {
    const g = mk(errorState).dive().dive();
    expect(g.matchesElement(<Game {...errorState} />), g.debug()).to.be.true;
  });
});
