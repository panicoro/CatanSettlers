import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { Redirect } from 'react-router-dom';

import {
  Rooms, mapStateToProps, mapDispatchToProps,
} from '../../src/containers/Rooms/Rooms';
import {
  dispatchError,
  dispatchRunning,
  dispatchRooms,
  dispatchCreate,
} from '../../src/containers/Rooms/Rooms.ducks';
import { getRooms } from '../../src/utils/Api';
import useInterval from '../../src/utils/UseInterval';


jest.mock('react-router-dom', () => ({
  Redirect: jest.fn(() => null),
}));

jest.mock('../../src/utils/Api', () => ({
  getRooms: jest.fn(() => null),
}));

jest.mock('../../src/utils/UseInterval', () => ({
  __esModule: true,
  default: jest.fn(() => null),
}));

const setError = jest.fn(() => null);
const setRunning = jest.fn(() => null);
const setRooms = jest.fn(() => null);
const setCreate = jest.fn(() => null);

afterEach(() => {
  Redirect.mockClear();
  getRooms.mockClear();
  useInterval.mockClear();
  setError.mockClear();
  setRunning.mockClear();
  setRooms.mockClear();
  setCreate.mockClear();
});

const mk = (rooms, stage) => render(
  <Rooms
    rooms={rooms}
    stage={stage}
    setError={setError}
    setRunning={setRunning}
    setRooms={setRooms}
    setCreate={setCreate}
  />,
);

test('returns rooms and stage', () => {
  const state = {
    Rooms: {
      rooms: [],
      stage: 'stage',
      other: 1,
    },
    other: 1,
  };
  const expected = {
    rooms: state.Rooms.rooms,
    stage: state.Rooms.stage,
  };

  expect(mapStateToProps(state)).toStrictEqual(expected);
});

test('returns all dispatch functions', () => {
  const expected = {
    setError: dispatchError,
    setRunning: dispatchRunning,
    setRooms: dispatchRooms,
    setCreate: dispatchCreate,
  };
  expect(mapDispatchToProps).toStrictEqual(expected);
});

test('is empty', () => {
  const { queryAllByTestId, queryByTestId } = mk([], 'empty');

  expect(queryAllByTestId('rooms-empty')).toHaveLength(1);

  const r = queryByTestId('rooms-empty');
  expect(r).toBeEmpty();

  expect(getRooms).toHaveBeenCalledTimes(1);
  expect(useInterval).toHaveBeenCalledTimes(1);
});

test('shows an error', () => {
  getRooms.mockImplementationOnce((onSuccess, onFailure) => onFailure());

  const { queryAllByTestId, queryByTestId } = mk([], 'error');

  expect(queryAllByTestId('error')).toHaveLength(1);

  const r = queryByTestId('error');
  expect(r).not.toBeEmpty();

  expect(getRooms).toHaveBeenCalledTimes(1);
  expect(useInterval).toHaveBeenCalledTimes(1);
  expect(setError).toHaveBeenCalledTimes(1);
});

test('redirects to /create', () => {
  mk([], 'create');

  expect(getRooms).toHaveBeenCalledTimes(1);
  expect(useInterval).toHaveBeenCalledTimes(1);
  expect(Redirect).toHaveBeenCalledTimes(1);
  expect(Redirect).toHaveBeenCalledWith({ to: '/create', push: true }, {});
});

test('shows no rooms', () => {
  const { queryAllByTestId } = mk([], 'running');

  // It should show the rooms screen, a button and an accordion.
  expect(queryAllByTestId('rooms')).toHaveLength(1);
  expect(queryAllByTestId('rooms-button')).toHaveLength(1);
  expect(queryAllByTestId('rooms-accordion')).toHaveLength(1);

  // It should show no rooms.
  expect(queryAllByTestId('rooms-card')).toHaveLength(0);
});

test('refreshes', () => {
  getRooms.mockImplementation((onSuccess) => onSuccess([]));
  useInterval.mockImplementationOnce((f) => f());
  mk([], 'running');

  // It should refresh.
  expect(getRooms).toHaveBeenCalledTimes(2);
  expect(useInterval).toHaveBeenCalledTimes(1);
  expect(setRooms).toHaveBeenCalledTimes(2);
  expect(setRunning).toHaveBeenCalledTimes(2);

  getRooms.mockImplementation(() => null);
});

test('button sets Create stage', () => {
  const { queryByTestId } = mk([], 'running');

  const b = queryByTestId('rooms-button');
  expect(b).not.toBeEmpty();
  expect(b).toBeEnabled();

  fireEvent.click(b);

  expect(getRooms).toHaveBeenCalledTimes(1);
  expect(useInterval).toHaveBeenCalledTimes(1);
  expect(setCreate).toHaveBeenCalledTimes(1);
});
