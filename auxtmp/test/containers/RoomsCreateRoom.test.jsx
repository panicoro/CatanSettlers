import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { Redirect } from 'react-router-dom';

import Error from '../../src/components/Error';
import {
  CreateRoom, mapDispatchToProps,
} from '../../src/containers/Rooms/CreateRoom';
import { dispatchRunning } from '../../src/containers/Rooms/Rooms.ducks';
import { createRoom, getBoards, joinRoom } from '../../src/utils/Api';


jest.mock('react-router-dom', () => ({
  Redirect: jest.fn(() => null),
}));

jest.mock('../../src/utils/Api', () => ({
  createRoom: jest.fn(() => null),
  getBoards: jest.fn(() => null),
  joinRoom: jest.fn(() => null),
}));

jest.mock('../../src/components/Error', () => ({
  __esModule: true,
  default: jest.fn(() => null),
}));

const setRunning = jest.fn(() => null);
const dispatchs = [setRunning];
const mockFns = [
  createRoom,
  getBoards,
  joinRoom,
  Redirect,
  Error,
];

afterEach(() => {
  dispatchs.forEach((f) => f.mockClear());
  mockFns.forEach((f) => f.mockClear());
});

const defaultBoards = [
  { id: 1, name: 'board1' },
  { id: 2, name: 'board2' },
  { id: 3, name: 'board3' },
];

const defaultRoom = {
  id: 1,
  name: 'room',
  owner: 'owner',
  players: ['1', '2'],
  max_players: 4,
  game_has_started: false,
};

getBoards.mockImplementation((onSuccess) => {
  onSuccess(defaultBoards);
});

test('returns all dispatchs', () => {
  const expected = {
    setRunning: dispatchRunning,
  };

  expect(mapDispatchToProps).toStrictEqual(expected);
});

test('inserts lobby name, selects board', () => {
  const { getAllByTestId, queryByTestId } = render(
    <CreateRoom setRunning={setRunning} />,
  );

  const boardList = getAllByTestId('board-name');
  expect(boardList).toHaveLength(3);
  expect(queryByTestId('button')).toBeDisabled();

  const roomInput = queryByTestId('room-name');
  const input = { target: { value: defaultRoom.name } };
  fireEvent.change(roomInput, input);
  expect(roomInput.value).toEqual(defaultRoom.name);

  const boardInput = queryByTestId('board-select');
  const select = { target: { value: defaultBoards[1].id } };
  fireEvent.change(boardInput, select);
  expect(Number(boardInput.value)).toEqual(defaultBoards[1].id);

  expect(queryByTestId('button')).toBeEnabled();
});

test('inserts lobby, selects board and redirects', () => {
  createRoom.mockImplementationOnce((roomName, boardId, onSuccess) => {
    onSuccess(defaultRoom);
    expect(joinRoom).toHaveBeenCalledTimes(1);
  });

  joinRoom.mockImplementationOnce((id, onSuccess) => {
    onSuccess(defaultRoom);
    expect(setRunning).toHaveBeenCalledTimes(1);
  });

  const { queryByTestId } = render(
    <CreateRoom setRunning={setRunning} />,
  );

  const roomInput = queryByTestId('room-name');
  const input = { target: { value: defaultRoom.name } };
  fireEvent.change(roomInput, input);

  const select = { target: { value: defaultBoards[1].id } };
  fireEvent.change(queryByTestId('board-select'), select);

  const button = queryByTestId('button');
  fireEvent.click(button);

  expect(Redirect).toHaveBeenCalledTimes(1);

  const redirect = `/waiting/${defaultRoom.id}`;
  expect(Redirect).toHaveBeenCalledWith({ to: redirect, push: true }, {});
});

test('shows an error when getBoards fails', () => {
  getBoards.mockImplementationOnce((onSuccess, onFailure) => {
    onFailure();
  });

  Error.mockImplementationOnce(({ message }) => {
    expect(message).toBe('Connection error, the boards could not be obtained');
    return null;
  });

  render(<CreateRoom setRunning={setRunning} />);

  expect(Error).toHaveBeenCalledTimes(1);
  expect(getBoards).toHaveBeenCalledTimes(1);

  const calledMocks = [Error, getBoards];
  mockFns
    .filter((f) => !calledMocks.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
});

test('shows an error when createRoom fails', () => {
  createRoom.mockImplementationOnce((roomName, boardId, onSuccess, onFailure) => {
    onFailure({ message: 'Error' });
  });

  Error.mockImplementationOnce(({ message, onClose }) => {
    expect(message).toBe('Error');
    onClose();
    return null;
  });

  const { queryByTestId } = render(
    <CreateRoom setRunning={setRunning} />,
  );

  const roomInput = queryByTestId('room-name');
  const input = { target: { value: defaultRoom.name } };
  fireEvent.change(roomInput, input);

  const select = { target: { value: defaultBoards[1].id } };
  fireEvent.change(queryByTestId('board-select'), select);

  const button = queryByTestId('button');
  fireEvent.click(button);

  expect(Error).toHaveBeenCalledTimes(1);
  expect(Redirect).not.toHaveBeenCalled();
  expect(joinRoom).not.toHaveBeenCalled();
});

test('shows an error when joinRoom fails', () => {
  createRoom.mockImplementationOnce((roomName, boardId, onSuccess) => {
    onSuccess(defaultRoom);
  });

  joinRoom.mockImplementationOnce((id, onSuccess, onFailure) => {
    onFailure({ message: 'Error' });
  });

  const { queryByTestId } = render(
    <CreateRoom setRunning={setRunning} />,
  );

  const roomInput = queryByTestId('room-name');
  const input = { target: { value: defaultRoom.name } };
  fireEvent.change(roomInput, input);

  const select = { target: { value: defaultBoards[1].id } };
  fireEvent.change(queryByTestId('board-select'), select);

  const button = queryByTestId('button');
  fireEvent.click(button);

  expect(Error).toHaveBeenCalledTimes(1);
  expect(Redirect).not.toHaveBeenCalled();
});
