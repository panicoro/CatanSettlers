import { expect } from 'chai';
import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import React from 'react';
import Table from 'react-bootstrap/Table';

import { Hand } from '../src/containers/Hand';
import HandScreen, { resToTable, cardsToTable } from '../src/components/Hand';
import { cardNames, resourceNames } from '../src/utils/Constants';


// This connects enzyme to the react adapter.
configure({ adapter: new Adapter() });

// eslint-disable-next-line react/jsx-props-no-spreading
const mk = (hand) => shallow(<Hand {...hand} />);

const initialHand = {
  cards: [],
  resources: [],
};

describe('Hand', () => {
  it('should render without crashing', () => {
    const h = mk(initialHand);
    expect(h.isEmptyRender(), h.debug()).to.be.false;
  });

  it('should render its component', () => {
    const h = mk(initialHand);
    expect(h.equals(<HandScreen {...initialHand} />), h.debug()).to.be.true;
  });

  it('should render resources', () => {
    const h = mk(initialHand).dive();
    const resources = (
      <Table>
        {resToTable(initialHand.resources)}
      </Table>
    );
    expect(h.containsMatchingElement(resources), h.debug()).to.be.true;
  });

  it('should render cards', () => {
    const h = mk(initialHand).dive();
    const cards = (
      <Table>
        {cardsToTable(initialHand.cards)}
      </Table>
    );
    expect(h.containsMatchingElement(cards), h.debug()).to.be.true;
  });

  it('should render all td\'s', () => {
    const h = mk(initialHand).dive();
    // Should render two entries for each card,
    // and two title entries.
    const expected = 2 * (cardNames.length + resourceNames.length);
    expect(h.find('td'), h.debug()).to.have.lengthOf(expected);
  });
});
