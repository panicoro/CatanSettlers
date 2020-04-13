import { expect } from 'chai';
import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import React from 'react';
import Dropdown from 'react-bootstrap/Dropdown';

import { CardDropdown } from '../src/containers/Actions/CardDropdown';
import ActionButton from '../src/containers/Actions/ActionButton';
import { cardActionNames } from '../src/utils/Constants';


// This connects enzyme to the react adapter.
configure({ adapter: new Adapter() });

const mk = (actions = []) => shallow(
  <CardDropdown
    actions={actions}
  />,
);

describe('CardDropdown', () => {
  it('should render without crashing', () => {
    const r = mk();
    expect(r.isEmptyRender(), r.debug()).to.be.false;
  });

  it('should show an empty, disabled dropdown', () => {
    const r = mk();
    const expected = (
      <Dropdown>
        <Dropdown.Toggle disabled>
          Development Cards
        </Dropdown.Toggle>
        <Dropdown.Menu>
        </Dropdown.Menu>
      </Dropdown>
    );
    expect(r.equals(expected), r.debug()).to.be.true;
  });

  it('should show each card separately', () => {
    cardActionNames.forEach((type) => {
      const r = mk([{ type }]);
      const expected = (
        <Dropdown>
          <Dropdown.Toggle disabled={false}>
            Development Cards
          </Dropdown.Toggle>
          <Dropdown.Menu>
            <ActionButton C={Dropdown.Item} key={type} type={type} />
          </Dropdown.Menu>
        </Dropdown>
      );
      expect(r.equals(expected), r.debug()).to.be.true;
    });
  });

  it('should show all cards', () => {
    const r = mk(cardActionNames.map((type) => ({ type })));
    const expected = (
      <Dropdown>
        <Dropdown.Toggle disabled={false}>
            Development Cards
        </Dropdown.Toggle>
        <Dropdown.Menu>
          { cardActionNames.map((type) => (
            <ActionButton C={Dropdown.Item} key={type} type={type} />
          ))}
        </Dropdown.Menu>
      </Dropdown>
    );
    expect(r.equals(expected), r.debug()).to.be.true;
  });
});
