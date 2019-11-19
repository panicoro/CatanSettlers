import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { useParams } from 'react-router-dom';

import showVertices from '../../src/components/Board/ShowVertices';
import {
  BuildingVertex, mapStateToProps, mapDispatchToProps,
} from '../../src/containers/Actions/BuildingVertex';
import {
  dispatchWaiting,
  dispatchError,
  dispatchVertexPayload,
} from '../../src/containers/Actions/Actions.ducks';
import {
  setRunning as dispatchGameRunning,
  setState as dispatchGameState,
} from '../../src/containers/Game/Game.ducks';
import { colours } from '../../src/utils/Constants';
import {
  getGameStatus, buildCity, buildSettlement,
} from '../../src/utils/Api';


const setError = jest.fn(() => null);
const setWaiting = jest.fn(() => null);
const setGameRunning = jest.fn(() => null);
const setGameState = jest.fn(() => null);
const setVertexPayload = jest.fn(() => null);
const dispatchs = [
  setError,
  setWaiting,
  setGameRunning,
  setGameState,
  setVertexPayload,
];

jest.mock('../../src/components/Board/ShowVertices', () => ({
  __esModule: true,
  default: jest.fn(() => null),
}));

jest.mock('../../src/utils/Api', () => ({
  getGameStatus: jest.fn(() => null),
  buildCity: jest.fn(() => null),
  buildSettlement: jest.fn(() => null),
}));

const mockFns = [
  getGameStatus,
  buildCity,
  buildSettlement,
];

jest.mock('react-router-dom', () => ({
  useParams: jest.fn(() => ({ id: '1' })),
}));

afterEach(() => {
  dispatchs.forEach((f) => { f.mockClear(); });
  mockFns.forEach((f) => { f.mockClear(); });
  useParams.mockClear();
  showVertices.mockClear();
});

const mk = (
  payload, type, position,
) => render(
  <BuildingVertex
    draw={{}}
    payload={payload}
    position={position}
    type={type}
    setError={setError}
    setWaiting={setWaiting}
    setGameRunning={setGameRunning}
    setGameState={setGameState}
    setVertexPayload={setVertexPayload}
  />,
);

test('returns draw, payload, position and type', () => {
  const type = 'type';
  const position = { level: 0, index: 0 };
  const payload = [];
  const state = {
    Board: { draw: {} },
    Game: { actions: [{ type, payload }] },
    Actions: { vertexPayload: position },
  };
  const ownProps = { type };
  const expected = {
    draw: {}, payload, position, type,
  };

  expect(mapStateToProps(state, ownProps)).toStrictEqual(expected);
});

test('returns all dispatch functions', () => {
  const expected = {
    setError: dispatchError,
    setWaiting: dispatchWaiting,
    setGameRunning: dispatchGameRunning,
    setGameState: dispatchGameState,
    setVertexPayload: dispatchVertexPayload,
  };

  expect(mapDispatchToProps).toStrictEqual(expected);
});

test('shows available city positions', () => {
  showVertices.mockImplementationOnce((draw, ps, colour,
    type, onClickMaker) => {
    const p = { level: 0, index: 0 };
    onClickMaker(p)();
    expect(setVertexPayload).toHaveBeenCalledTimes(1);
    expect(setVertexPayload).toHaveBeenCalledWith(p);
  });

  mk([], 'upgrade_city');

  // It should call useParams.
  expect(useParams).toHaveBeenCalledTimes(1);
  expect(useParams).not.toHaveBeenCalledWith(expect.anything());

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => f !== setVertexPayload)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());

  // It should show available positions.
  expect(showVertices).toHaveBeenCalledTimes(1);
  expect(showVertices).toHaveBeenCalledWith({}, [], colours.Building, 'city', expect.any(Function));
});

test('shows available settlement positions', () => {
  showVertices.mockImplementationOnce((draw, ps, colour,
    type, onClickMaker) => {
    const p = { level: 0, index: 0 };
    onClickMaker(p)();
    expect(setVertexPayload).toHaveBeenCalledTimes(1);
    expect(setVertexPayload).toHaveBeenCalledWith(p);
  });

  mk([], 'build_settlement');

  // It should call useParams.
  expect(useParams).toHaveBeenCalledTimes(1);
  expect(useParams).not.toHaveBeenCalledWith(expect.anything());

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => f !== setVertexPayload)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());

  // It should show available positions.
  expect(showVertices).toHaveBeenCalledTimes(1);
  expect(showVertices).toHaveBeenCalledWith({}, [], colours.Building, 'settlement', expect.any(Function));
});

test('shows available positions and a chosen one', () => {
  const position = { level: 0, index: 0 };

  showVertices.mockImplementation((draw, ps, colour, type, onClickMaker) => {
    if (ps.length === 1 && ps[0].level === position.level && ps[0].index === position.index) {
      expect(onClickMaker(position)()).toBe(null);
      expect(onClickMaker({})()).toBe(null);
    }
  });

  mk([], 'build_settlement', position);

  // It should call useParams.
  expect(useParams).toHaveBeenCalledTimes(1);
  expect(useParams).not.toHaveBeenCalledWith(expect.anything());

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => f !== setVertexPayload)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());

  // It should show available positions.
  expect(showVertices).toHaveBeenCalledTimes(2);
  expect(showVertices)
    .toHaveBeenNthCalledWith(1, {}, [],
      colours.Building, 'settlement', expect.any(Function));
  expect(showVertices)
    .toHaveBeenNthCalledWith(2, {}, [position],
      colours.Chosen, 'settlement', expect.any(Function));

  showVertices.mockImplementation(() => null);
});

test('calls refresh on confirm', () => {
  buildSettlement.mockImplementationOnce((id, pos, onSuccess) => {
    onSuccess();
  });

  const position = { level: 0, index: 0 };

  const { queryByTestId } = mk([], 'build_settlement', position);

  fireEvent.click(queryByTestId('actions-positioning-confirm'));

  // It should call buildSettlement.
  expect(buildSettlement).toHaveBeenCalledTimes(1);
  expect(buildSettlement).toHaveBeenCalledWith('1', position, expect.any(Function), setError);

  // It should refresh.
  expect(setWaiting).toHaveBeenCalledTimes(1);
  expect(setWaiting).not.toHaveBeenCalledWith(expect.anything());
  expect(setGameRunning).toHaveBeenCalledTimes(1);
  expect(setGameRunning).not.toHaveBeenCalledWith(expect.anything());
  expect(getGameStatus).toHaveBeenCalledTimes(1);
  expect(getGameStatus).toHaveBeenCalledWith('1', setGameState, setError);

  const calledDispatchs = [setWaiting, setGameRunning];
  const calledMocks = [buildSettlement, getGameStatus];

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => !calledDispatchs.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns
    .filter((f) => !calledMocks.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
});

test('calls refresh on cancel', () => {
  const position = { level: 1, index: 2 };
  const { queryByTestId } = mk([], 'upgrade_city', position);

  fireEvent.click(queryByTestId('actions-positioning-cancel'));

  // It should refresh.
  expect(setWaiting).toHaveBeenCalledTimes(1);
  expect(setWaiting).not.toHaveBeenCalledWith(expect.anything());
  expect(setGameRunning).toHaveBeenCalledTimes(1);
  expect(setWaiting).not.toHaveBeenCalledWith(expect.anything());
  expect(getGameStatus).toHaveBeenCalledTimes(1);
  expect(getGameStatus).toHaveBeenCalledWith('1', setGameState, setError);

  // It shouldn't call any of these.
  const calledDispatchs = [setWaiting, setGameRunning];
  const calledMocks = [getGameStatus];
  dispatchs
    .filter((f) => !calledDispatchs.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns
    .filter((f) => !calledMocks.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
});
