import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { Redirect } from 'react-router-dom';

import { Body, mapStateToProps } from '../../src/containers/Rooms/Body';
import { rooms } from '../../src/utils/RoomData';
import { joinRoom } from '../../src/utils/Api';


jest.mock('react-router-dom', () => ({
  Redirect: jest.fn(() => null),
}));

jest.mock('../../src/utils/Api', () => ({
  joinRoom: jest.fn((id, onSuccess, onFailure) => {
    if (id === 1) onSuccess();
    else onFailure();
  }),
}));

afterEach(() => {
  Redirect.mockClear();
  joinRoom.mockClear();
});

const mk = (props) => render(
  <Body
    id={props.id}
    owner={props.owner}
    players={props.players}
    maxPlayers={props.max_players}
    gameHasStarted={props.game_has_started}
    username="test"
  />,
);

test('returns a room and a username', () => {
  const state = { Auth: { username: 'test' } };
  const room = rooms[0];
  const ownProps = {
    id: room.id,
    owner: room.owner,
    players: room.players,
    maxPlayers: room.max_players,
    gameHasStarted: room.game_has_started,
  };
  const expected = {
    username: state.Auth.username,
    ...ownProps,
  };

  expect(mapStateToProps(state, ownProps)).toEqual(expected);
});

/* When body is mounted */
test('renders without crashing', () => {
  const { queryAllByTestId } = mk(rooms[0]);
  const bodies = queryAllByTestId('room-body');

  // It should render one body.
  expect(bodies).toHaveLength(1);

  // It should render without crashing.
  expect(bodies[0]).toBeInTheDocument();
  expect(bodies[0]).not.toBeEmpty();

  // It should have one button.
  expect(queryAllByTestId('room-body-button')).toHaveLength(1);
});

/* When user is not the owner
 * And room is not full
 * And user is not joined
 * And game has not started */
test('is able to join', () => {
  const { queryByTestId } = mk(rooms[0]);
  const button = queryByTestId('room-body-button');

  // It should be enabled.
  expect(button).toBeEnabled();

  // User should be able to join.
  expect(button).toHaveTextContent('Join');

  // Should redirect.
  fireEvent.click(button);
  expect(joinRoom).toHaveBeenCalledTimes(1);
  expect(Redirect).toHaveBeenCalledTimes(1);
  expect(Redirect).toHaveBeenCalledWith({ to: '/waiting/1', push: true }, {});
});

/* When user is not the owner
 * And room is not full
 * And user is not joined
 * And game has started */
test('is not able to join or enter', () => {
  const { queryAllByTestId } = mk(rooms[1]);

  // It should not have a button.
  expect(queryAllByTestId('room-body-button')).toHaveLength(0);
});

/* When user is not the owner
 * And room is full
 * And user is not joined
 * And game has not started */
test('is not able to join or enter', () => {
  const { queryAllByTestId } = mk(rooms[2]);

  // It should not have a button.
  expect(queryAllByTestId('room-body-button')).toHaveLength(0);
});

/* When user is not the owner
 * And room is full
 * And user is not joined
 * And game has started */
test('is not able to join or enter', () => {
  const { queryAllByTestId } = mk(rooms[3]);

  // It should not have a button.
  expect(queryAllByTestId('room-body-button')).toHaveLength(0);
});

/* When user is not the owner
 * And room is not full
 * And user is joined
 * And game has not started */
test('is able to enter', () => {
  const { queryByTestId } = mk(rooms[4]);
  const button = queryByTestId('room-body-button');

  // It should be enabled.
  expect(button).toBeEnabled();

  // User should be able to enter.
  expect(button).toHaveTextContent('Enter');
});

/* When user is not the owner
 * And room is not full
 * And user is joined
 * And game has started */
test('is able to enter', () => {
  const { queryByTestId } = mk(rooms[5]);
  const button = queryByTestId('room-body-button');

  // It should be enabled.
  expect(button).toBeEnabled();

  // User should be able to enter.
  expect(button).toHaveTextContent('Enter');
});

/* When user is not the owner
 * And room is full
 * And user is joined
 * And game has not started */
test('is able to enter', () => {
  const { queryByTestId } = mk(rooms[6]);
  const button = queryByTestId('room-body-button');

  // It should be enabled.
  expect(button).toBeEnabled();

  // User should be able to enter.
  expect(button).toHaveTextContent('Enter');
});

/* When user is not the owner
 * And room is not full
 * And user is joined
 * And game has started */
test('is able to enter', () => {
  const { queryByTestId } = mk(rooms[7]);
  const button = queryByTestId('room-body-button');

  // It should be enabled.
  expect(button).toBeEnabled();

  // User should be able to enter.
  expect(button).toHaveTextContent('Enter');
});

/* When user is the owner
 * And room is not full
 * And user is joined
 * And game has not started */
test('is able to enter', () => {
  const { queryByTestId } = mk(rooms[8]);
  const button = queryByTestId('room-body-button');

  // It should be enabled.
  expect(button).toBeEnabled();

  // User should be able to enter.
  expect(button).toHaveTextContent('Enter');
});

/* When user is the owner
 * And room is not full
 * And user is joined
 * And game has started */
test('is able to enter', () => {
  const { queryByTestId } = mk(rooms[9]);
  const button = queryByTestId('room-body-button');

  // It should be enabled.
  expect(button).toBeEnabled();

  // User should be able to enter.
  expect(button).toHaveTextContent('Enter');
});

/* When user is the owner
 * And room is full
 * And user is joined
 * And game has not started */
test('is able to enter', () => {
  const { queryByTestId } = mk(rooms[10]);
  const button = queryByTestId('room-body-button');

  // It should be enabled.
  expect(button).toBeEnabled();

  // User should be able to enter.
  expect(button).toHaveTextContent('Enter');
});

/* When user is the owner
 * And room is full
 * And user is joined
 * And game has started */
test('is able to enter', () => {
  const { queryByTestId } = mk(rooms[9]);
  const button = queryByTestId('room-body-button');

  // It should be enabled.
  expect(button).toBeEnabled();

  // User should be able to enter.
  expect(button).toHaveTextContent('Enter');
});

/* When user is not the owner
 * And room is not full
 * And user is not joined
 * And game has not started */
test('is able to join, but shows an error', () => {
  const { queryByTestId } = mk({ ...rooms[0], id: 2 });
  const button = queryByTestId('room-body-button');

  // It should be enabled.
  expect(button).toBeEnabled();

  // User should be able to join.
  expect(button).toHaveTextContent('Join');

  // Should show an error.
  fireEvent.click(button);
  expect(joinRoom).toHaveBeenCalledTimes(1);
  const error = queryByTestId('error');
  expect(error).toBeInTheDocument();
  expect(error).not.toBeEmpty();
});
