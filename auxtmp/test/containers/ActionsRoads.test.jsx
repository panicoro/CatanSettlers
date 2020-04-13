import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { useParams } from 'react-router-dom';

import showEdges from '../../src/components/Board/ShowEdges';
import {
  Roads, mapStateToProps, mapDispatchToProps,
} from '../../src/containers/Actions/Roads';
import {
  dispatchWaiting,
  dispatchError,
  dispatch2RoadsPayload,
} from '../../src/containers/Actions/Actions.ducks';
import {
  setRunning as dispatchGameRunning,
  setState as dispatchGameState,
} from '../../src/containers/Game/Game.ducks';
import { colours } from '../../src/utils/Constants';
import { getGameStatus, play2Roads } from '../../src/utils/Api';


const setError = jest.fn(() => null);
const setWaiting = jest.fn(() => null);
const setGameRunning = jest.fn(() => null);
const setGameState = jest.fn(() => null);
const set2RoadsPayload = jest.fn(() => null);
const dispatchs = [
  setError,
  setWaiting,
  setGameRunning,
  setGameState,
  set2RoadsPayload,
];

jest.mock('../../src/components/Board/ShowEdges', () => ({
  __esModule: true,
  default: jest.fn(() => null),
}));

jest.mock('../../src/utils/Api', () => ({
  getGameStatus: jest.fn(() => null),
  play2Roads: jest.fn(() => null),
}));

const mockFns = [
  getGameStatus,
  play2Roads,
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
  payload = [], p0, p1,
) => render(
  <Roads
    draw={{}}
    payload={payload}
    p0={p0}
    p1={p1}
    setError={setError}
    setWaiting={setWaiting}
    setGameRunning={setGameRunning}
    setGameState={setGameState}
    set2RoadsPayload={set2RoadsPayload}
  />,
);

test('returns draw, actionPayload and robberPayload ', () => {
  const p0 = { level: 1, index: 2 };
  const p1 = { level: 1, index: 1 };
  const payload = [{ level: 2, index: 1 }];

  const state = {
    Board: { draw: {} },
    Game: { actions: [{ type: 'play_road_building_card', payload }] },
    Actions: { roadsPayload: { p0, p1 } },
  };
  const expected = {
    draw: {},
    payload,
    p0,
    p1,
  };

  expect(mapStateToProps(state)).toStrictEqual(expected);
});

test('returns all dispatch functions', () => {
  const expected = {
    setError: dispatchError,
    setWaiting: dispatchWaiting,
    setGameRunning: dispatchGameRunning,
    setGameState: dispatchGameState,
    set2RoadsPayload: dispatch2RoadsPayload,
  };

  expect(mapDispatchToProps).toStrictEqual(expected);
});

test('shows its component', () => {
  const { queryAllByTestId } = mk();

  const components = queryAllByTestId('actions-positioning');
  expect(components).toHaveLength(1);
});

test('shows available positions', () => {
  showEdges.mockImplementationOnce((draw, ps, colour, onClickMaker) => {
    const p0 = { level: 0, index: 0 };
    onClickMaker(p0)();
    expect(set2RoadsPayload).toHaveBeenCalledTimes(1);
    expect(set2RoadsPayload).toHaveBeenCalledWith(p0, null);
  });

  mk([]);

  // It should call useParams.
  expect(useParams).toHaveBeenCalledTimes(1);
  expect(useParams).not.toHaveBeenCalledWith(expect.anything());

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => f !== set2RoadsPayload)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());

  // It should show available positions.
  expect(showEdges).toHaveBeenCalledTimes(1);
  expect(showEdges).toHaveBeenCalledWith({}, [], colours.Building, expect.any(Function));
});

test('shows available positions and a chosen one', () => {
  const p0 = { level: 1, index: 1 };

  showEdges.mockImplementationOnce((draw, ps, colour, onClickMaker) => {
    const p1 = { level: 0, index: 0 };
    onClickMaker(p1)();
    expect(set2RoadsPayload).toHaveBeenCalledTimes(1);
    expect(set2RoadsPayload).toHaveBeenCalledWith(p0, p1);
  });

  mk([], p0);

  // It should call useParams.
  expect(useParams).toHaveBeenCalledTimes(1);
  expect(useParams).not.toHaveBeenCalledWith(expect.anything());

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => f !== set2RoadsPayload)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());

  // It should show available positions.
  expect(showEdges).toHaveBeenCalledTimes(2);
  expect(showEdges)
    .toHaveBeenNthCalledWith(1, {}, [], colours.Building, expect.any(Function));
  expect(showEdges)
    .toHaveBeenNthCalledWith(2, {}, [p0], colours.Chosen, expect.any(Function));
});

test('shows no available positions and two chosen ones', () => {
  const p0 = { level: 0, index: 0 };
  const p1 = { level: 1, index: 1 };

  showEdges.mockImplementation((draw, ps, colour, onClickMaker) => {
    [onClickMaker(p0)(),
      onClickMaker(p1)(),
      onClickMaker({})(),
    ].forEach((r) => expect(r).toBe(null));
  });

  mk([], p0, p1);

  expect(showEdges).toHaveBeenCalledTimes(3);

  // It shouldn't call any of these.
  dispatchs.forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());

  showEdges.mockImplementation(() => null);
});

test('calls refresh on confirm', () => {
  play2Roads.mockImplementationOnce((id, p0, p1, onSuccess) => {
    onSuccess();
  });

  const p0 = { level: 0, index: 0 };
  const p1 = { level: 1, index: 1 };

  const { queryByTestId } = mk([], p0, p1);

  fireEvent.click(queryByTestId('actions-positioning-confirm'));

  // It should call play2Roads.
  expect(play2Roads).toHaveBeenCalledTimes(1);
  expect(play2Roads).toHaveBeenCalledWith('1', p0, p1, expect.any(Function), setError);

  // It should refresh.
  expect(setWaiting).toHaveBeenCalledTimes(1);
  expect(setWaiting).not.toHaveBeenCalledWith(expect.anything());
  expect(setGameRunning).toHaveBeenCalledTimes(1);
  expect(setGameRunning).not.toHaveBeenCalledWith(expect.anything());
  expect(getGameStatus).toHaveBeenCalledTimes(1);
  expect(getGameStatus).toHaveBeenCalledWith('1', setGameState, setError);

  const calledDispatchs = [setWaiting, setGameRunning];
  const calledMocks = [play2Roads, getGameStatus];

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => !calledDispatchs.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns
    .filter((f) => !calledMocks.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
});

test('calls refresh on cancel', () => {
  play2Roads.mockImplementationOnce((id, p0, p1, onSuccess) => {
    onSuccess();
  });

  const p0 = { level: 0, index: 0 };
  const p1 = { level: 1, index: 1 };

  const { queryByTestId } = mk([], p0, p1);

  fireEvent.click(queryByTestId('actions-positioning-cancel'));

  // It should refresh.
  expect(setWaiting).toHaveBeenCalledTimes(1);
  expect(setWaiting).not.toHaveBeenCalledWith(expect.anything());
  expect(setGameRunning).toHaveBeenCalledTimes(1);
  expect(setGameRunning).not.toHaveBeenCalledWith(expect.anything());
  expect(getGameStatus).toHaveBeenCalledTimes(1);
  expect(getGameStatus).toHaveBeenCalledWith('1', setGameState, setError);

  const calledDispatchs = [setWaiting, setGameRunning];

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => !calledDispatchs.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns
    .filter((f) => f !== getGameStatus)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
});
