import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';

import Rooms from '../../src/components/Rooms/Rooms';
/* eslint-disable import/no-named-as-default */
import Body from '../../src/containers/Rooms/Body';
/* eslint-enable import/no-named-as-default */
import { rooms } from '../../src/utils/RoomData';


jest.mock('../../src/containers/Rooms/Body', () => ({
  __esModule: true,
  default: jest.fn(() => null),
}));

const createRoom = jest.fn(() => null);

const mk = (rs) => render(
  <Rooms
    rooms={rs}
    createRoom={createRoom}
  />,
);

afterEach(() => {
  createRoom.mockClear();
});

test('shows no rooms', () => {
  const { queryAllByTestId } = mk([]);

  // It should show the rooms screen, a button and an accordion.
  expect(queryAllByTestId('rooms')).toHaveLength(1);
  expect(queryAllByTestId('rooms-button')).toHaveLength(1);
  expect(queryAllByTestId('rooms-accordion')).toHaveLength(1);

  // It should show no rooms.
  expect(queryAllByTestId('rooms-card')).toHaveLength(0);
  expect(createRoom).not.toHaveBeenCalled();
});

test('shows all rooms', () => {
  const { queryAllByTestId } = mk(rooms);

  // It should show the rooms screen, a button and an accordion.
  expect(queryAllByTestId('rooms')).toHaveLength(1);
  expect(queryAllByTestId('rooms-button')).toHaveLength(1);
  expect(queryAllByTestId('rooms-accordion')).toHaveLength(1);

  // It should show no rooms.
  expect(queryAllByTestId('rooms-card')).toHaveLength(rooms.length);
  expect(Body).toHaveBeenCalledTimes(rooms.length);

  for (let i = 0; i < rooms.length; i += 1) {
    const props = {
      id: rooms[i].id,
      maxPlayers: rooms[i].max_players,
      owner: rooms[i].owner,
      players: rooms[i].players,
      gameHasStarted: rooms[i].game_has_started,
    };
    expect(Body).toHaveBeenNthCalledWith(i + 1, props, {});
  }

  expect(createRoom).not.toHaveBeenCalled();
});

test('calls createRoom', () => {
  const { queryByTestId } = mk([]);

  const button = queryByTestId('rooms-button');
  fireEvent.click(button);

  expect(createRoom).toHaveBeenCalledTimes(1);
});

test('calls createRoom', () => {
  const { queryByTestId } = mk(rooms);

  const button = queryByTestId('rooms-button');
  fireEvent.click(button);

  expect(createRoom).toHaveBeenCalledTimes(1);
});
