import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';

import { Waiting } from '../../src/components/Rooms/Waiting';
import { ownerState, notOwnerState } from '../data/Waiting.ducks';

const mk = (state) => render(<Waiting {...state} />);

test('should be enable buttons', () => {
  const { queryAllByTestId } = mk(ownerState);
  const container = queryAllByTestId('waiting-buttons');
  expect(container[0]).not.toBeEmpty();
  expect(container[0]).toHaveTextContent(/Start game/i);
  expect(container[0]).toHaveTextContent(/Cancel room/i);
});

test('should be disable buttons', () => {
  const { queryAllByTestId } = mk(notOwnerState);
  const container = queryAllByTestId('waiting-buttons');
  expect(container).toHaveLength(0);
});
