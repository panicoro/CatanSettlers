import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { useParams } from 'react-router-dom';

import showEdges from '../../src/components/Board/ShowEdges';
import {
  BuildingEdge, mapStateToProps, mapDispatchToProps,
} from '../../src/containers/Actions/BuildingEdge';
import {
  dispatchWaiting,
  dispatchError,
  dispatchEdgePayload,
} from '../../src/containers/Actions/Actions.ducks';
import {
  setRunning as dispatchGameRunning,
  setState as dispatchGameState,
} from '../../src/containers/Game/Game.ducks';
import { colours } from '../../src/utils/Constants';
import { getGameStatus, buildRoad } from '../../src/utils/Api';


const setError = jest.fn(() => null);
const setWaiting = jest.fn(() => null);
const setGameRunning = jest.fn(() => null);
const setGameState = jest.fn(() => null);
const setEdgePayload = jest.fn(() => null);
const dispatchs = [
  setError,
  setWaiting,
  setGameRunning,
  setGameState,
  setEdgePayload,
];

jest.mock('../../src/components/Board/ShowEdges', () => ({
  __esModule: true,
  default: jest.fn(() => null),
}));

jest.mock('../../src/utils/Api', () => ({
  getGameStatus: jest.fn(() => null),
  buildRoad: jest.fn(() => null),
}));

const mockFns = [
  getGameStatus,
  buildRoad,
];

jest.mock('react-router-dom', () => ({
  useParams: jest.fn(() => ({ id: '1' })),
}));

afterEach(() => {
  dispatchs.forEach((f) => { f.mockClear(); });
  mockFns.forEach((f) => { f.mockClear(); });
  useParams.mockClear();
  showEdges.mockClear();
});

const mk = (
  payload, position,
) => render(
  <BuildingEdge
    draw={{}}
    payload={payload}
    position={position}
    setError={setError}
    setWaiting={setWaiting}
    setGameRunning={setGameRunning}
    setGameState={setGameState}
    setEdgePayload={setEdgePayload}
  />,
);

test('returns draw, payload, position and type', () => {
  const position = { level: 0, index: 0 };
  const payload = [];
  const state = {
    Board: { draw: {} },
    Game: { actions: [{ type: 'build_road', payload }] },
    Actions: { edgePayload: position },
  };
  const expected = {
    draw: {}, payload, position,
  };

  expect(mapStateToProps(state)).toStrictEqual(expected);
});

test('returns all dispatch functions', () => {
  const expected = {
    setError: dispatchError,
    setWaiting: dispatchWaiting,
    setGameRunning: dispatchGameRunning,
    setGameState: dispatchGameState,
    setEdgePayload: dispatchEdgePayload,
  };

  expect(mapDispatchToProps).toStrictEqual(expected);
});

test('shows available positions', () => {
  showEdges.mockImplementationOnce((draw, ps, colour, onClickMaker) => {
    const p0 = { level: 0, index: 0 };
    const p1 = { level: 1, index: 1 };
    onClickMaker([p0, p1])();
    expect(setEdgePayload).toHaveBeenCalledTimes(1);
    expect(setEdgePayload).toHaveBeenCalledWith([p0, p1]);
  });

  mk([]);

  // It should call useParams.
  expect(useParams).toHaveBeenCalledTimes(1);
  expect(useParams).not.toHaveBeenCalledWith(expect.anything());

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => f !== setEdgePayload)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());

  // It should show available positions.
  expect(showEdges).toHaveBeenCalledTimes(1);
  expect(showEdges).toHaveBeenCalledWith({}, [], colours.Building,
    expect.any(Function));
});

test('shows available positions and a chosen one', () => {
  const p0 = { level: 0, index: 0 };
  const p1 = { level: 1, index: 1 };

  showEdges.mockImplementation((draw, ps, colour, onClickMaker) => {
    if (ps.length === 1
      && ps[0][0].level === p0.level
      && ps[0][0].index === p0.index
      && ps[0][1].level === p1.level
      && ps[0][1].index === p1.index) {
      expect(onClickMaker([p0, p1])()).toBe(null);
      expect(onClickMaker([])()).toBe(null);
    }
  });

  mk([], [p0, p1]);

  // It should call useParams.
  expect(useParams).toHaveBeenCalledTimes(1);
  expect(useParams).not.toHaveBeenCalledWith(expect.anything());

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => f !== setEdgePayload)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());

  // It should show available positions.
  expect(showEdges).toHaveBeenCalledTimes(2);
  expect(showEdges)
    .toHaveBeenNthCalledWith(1, {}, [],
      colours.Building, expect.any(Function));
  expect(showEdges)
    .toHaveBeenNthCalledWith(2, {}, [[p0, p1]],
      colours.Chosen, expect.any(Function));

  showEdges.mockImplementation(() => null);
});

test('calls refresh on confirm', () => {
  buildRoad.mockImplementationOnce((id, pos, onSuccess) => {
    onSuccess();
  });

  const p0 = { level: 0, index: 0 };
  const p1 = { level: 1, index: 1 };
  const position = [p0, p1];

  const { queryByTestId } = mk([], position);

  fireEvent.click(queryByTestId('actions-positioning-confirm'));

  // It should call buildRoad.
  expect(buildRoad).toHaveBeenCalledTimes(1);
  expect(buildRoad).toHaveBeenCalledWith('1', position, expect.any(Function), setError);

  // It should refresh.
  expect(setWaiting).toHaveBeenCalledTimes(1);
  expect(setWaiting).not.toHaveBeenCalledWith(expect.anything());
  expect(setGameRunning).toHaveBeenCalledTimes(1);
  expect(setGameRunning).not.toHaveBeenCalledWith(expect.anything());
  expect(getGameStatus).toHaveBeenCalledTimes(1);
  expect(getGameStatus).toHaveBeenCalledWith('1', setGameState, setError);

  const calledDispatchs = [setWaiting, setGameRunning];
  const calledMocks = [buildRoad, getGameStatus];

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => !calledDispatchs.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns
    .filter((f) => !calledMocks.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
});

test('calls refresh on cancel', () => {
  const p0 = { level: 0, index: 0 };
  const p1 = { level: 1, index: 1 };
  const position = [p0, p1];

  const { queryByTestId } = mk([], position);

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
