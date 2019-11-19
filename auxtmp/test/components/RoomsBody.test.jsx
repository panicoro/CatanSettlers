import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';

import Body from '../../src/components/Rooms/Body';


const room = {
  id: 1,
  maxPlayers: 4,
  owner: 'owner',
  players: 'owner, not owner',
  gameStarted: 'game started',
};

const onClick = jest.fn(() => null);

const extra = {
  label: 'button label',
  onClick,
};

const mk = (disabled) => render(
  <Body
    {...room}
    {...extra}
    disabled={disabled}
  />,
);

afterEach(() => {
  onClick.mockClear();
});

const testBody = (body) => {
  // The body should render.
  expect(body).toBeInTheDocument();
  expect(body).not.toBeEmpty();

  // The body should show information.
  expect(body).toHaveTextContent(`Owner: ${room.owner}`);
  expect(body).toHaveTextContent(`Players: ${room.players}`);
  expect(body).toHaveTextContent(`Max players: ${room.maxPlayers}`);
  expect(body).toHaveTextContent(`${room.gameStarted}`);
};

const testButton = (button) => {
  // The button should render.
  expect(button).toBeInTheDocument();
  expect(button).not.toBeEmpty();

  // The button should show a label.
  expect(button).toHaveTextContent(extra.label);
};

test('shows a body with a enabled button', () => {
  const { queryAllByTestId, queryByTestId } = mk(false);

  // It should show one body.
  expect(queryAllByTestId('room-body')).toHaveLength(1);

  // It should show one button.
  expect(queryAllByTestId('room-body-button')).toHaveLength(1);

  const body = queryByTestId('room-body');
  testBody(body);

  // The button should render.
  const button = queryByTestId('room-body-button');
  testButton(button);

  // The button should be enabled.
  expect(button).toBeEnabled();

  fireEvent.click(button);
  expect(onClick).toHaveBeenCalledTimes(1);
});

test('shows a body with a disabled button', () => {
  const { queryAllByTestId, queryByTestId } = mk(true);

  // It should show one body.
  expect(queryAllByTestId('room-body')).toHaveLength(1);

  // It should show one button.
  expect(queryAllByTestId('room-body-button')).toHaveLength(1);

  // The body should render.
  const body = queryByTestId('room-body');
  testBody(body);

  const button = queryByTestId('room-body-button');
  testButton(button);

  // The button should be disabled.
  expect(button).toBeDisabled();

  fireEvent.click(button);
  expect(onClick).toHaveBeenCalledTimes(0);
});

test('shows a body with no button', () => {
  const { queryAllByTestId, queryByTestId } = render(
    <Body
      {...room}
      {...extra}
      onClick={null}
      disabled={false}
    />,
  );

  // It should show one body.
  expect(queryAllByTestId('room-body')).toHaveLength(1);

  // It should show one button.
  expect(queryAllByTestId('room-body-button')).toHaveLength(0);

  // The body should render.
  const body = queryByTestId('room-body');
  testBody(body);
});
