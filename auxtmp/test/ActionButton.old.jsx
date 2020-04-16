import { expect } from 'chai';
import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import React from 'react';
import Button from 'react-bootstrap/Button';

import { ActionButton } from '../src/containers/Actions/ActionButton';


// This connects enzyme to the react adapter.
configure({ adapter: new Adapter() });

const mk = (
  actions = [],
  component = Button,
  onClick = () => 'actionOnClick',
) => shallow(
  <ActionButton
    actions={actions}
    C={component}
    type="buy_card"
    actionOnClick={() => (() => onClick)}
  />,
);

describe('ActionButton', () => {
  it('should render without crashing', () => {
    const r = mk();
    expect(r.isEmptyRender(), r.debug()).to.be.false;
  });

  it('should show one button', () => {
    const r = mk();
    expect(r.find(Button), r.debug()).to.have.lengthOf(1);
  });

  it('should show a disabled button', () => {
    const r = mk();
    const expected = (
      <Button disabled size="sm">
        Buy card
      </Button>
    );
    expect(r.matchesElement(expected), r.debug()).to.be.true;
  });

  it('should show an enabled button', () => {
    const r = mk([{ type: 'buy_card' }]);
    const expected = (
      <Button disabled={false} size="sm">
        Buy card
      </Button>
    );
    expect(r.matchesElement(expected), r.debug()).to.be.true;
  });
});
