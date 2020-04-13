import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { useParams } from 'react-router-dom';

import showHCenter from '../../src/components/Board/ShowHCenter';
import {
  Robbing, mapStateToProps, mapDispatchToProps,
} from '../../src/containers/Actions/Robbing';
import {
  dispatchWaiting,
  dispatchError,
  dispatchRobberPayload,
} from '../../src/containers/Actions/Actions.ducks';
import {
  setRunning as dispatchGameRunning,
  setState as dispatchGameState,
} from '../../src/containers/Game/Game.ducks';
import { dispatchOnClick } from '../../src/containers/Info/Info.ducks';
import { colours } from '../../src/utils/Constants';
import { getGameStatus, moveRobber, playKnight } from '../../src/utils/Api';


const setError = jest.fn(() => null);
const setWaiting = jest.fn(() => null);
const setGameRunning = jest.fn(() => null);
const setGameState = jest.fn(() => null);
const setRobberPayload = jest.fn(() => null);
const setInfoOnClick = jest.fn(() => null);
const dispatchs = [
  setError,
  setWaiting,
  setGameRunning,
  setGameState,
  setRobberPayload,
  setInfoOnClick,
];

jest.mock('../../src/components/Board/ShowHCenter', () => ({
  __esModule: true,
  default: jest.fn(() => null),
}));

jest.mock('../../src/utils/Api', () => ({
  getGameStatus: jest.fn(() => null),
  moveRobber: jest.fn(() => null),
  playKnight: jest.fn(() => null),
}));

const mockFns = [
  getGameStatus,
  moveRobber,
  playKnight,
];

jest.mock('react-router-dom', () => ({
  useParams: jest.fn(() => ({ id: '1' })),
}));

afterEach(() => {
  dispatchs.forEach((f) => { f.mockClear(); });
  mockFns.forEach((f) => { f.mockClear(); });
  useParams.mockClear();
  showHCenter.mockClear();
});

const mk = (
  payload = [], position,
  player, type = 'move_robber',
) => render(
  <Robbing
    draw={{}}
    payload={payload}
    position={position}
    type={type}
    player={player}
    setError={setError}
    setWaiting={setWaiting}
    setGameRunning={setGameRunning}
    setGameState={setGameState}
    setRobberPayload={setRobberPayload}
    setInfoOnClick={setInfoOnClick}
  />,
);

test('returns draw, actionPayload and robberPayload ', () => {
  const position = { level: 1, index: 2 };
  const player = 'player';
  const payload = [
    { players: ['other player'], position: { level: 2, index: 3 } },
  ];

  const state = {
    Board: { draw: {} },
    Game: { actions: [{ type: 'type', payload }] },
    Actions: { robberPayload: { position, player } },
  };
  const ownProps = {
    type: 'type',
  };
  const expected = {
    draw: {},
    payload,
    position,
    player,
  };

  expect(mapStateToProps(state, ownProps)).toStrictEqual(expected);
});

test('returns all dispatch functions', () => {
  const expected = {
    setError: dispatchError,
    setWaiting: dispatchWaiting,
    setGameRunning: dispatchGameRunning,
    setGameState: dispatchGameState,
    setRobberPayload: dispatchRobberPayload,
    setInfoOnClick: dispatchOnClick,
  };

  expect(mapDispatchToProps).toStrictEqual(expected);
});

test('shows its component', () => {
  const { queryAllByTestId } = mk();

  const components = queryAllByTestId('actions-positioning');
  expect(components).toHaveLength(1);
});

test('shows available positions', () => {
  setInfoOnClick.mockImplementationOnce((fun) => {
    expect(fun()).toBe(null);
  });

  showHCenter.mockImplementationOnce((draw, ps, colour, onClickMaker) => {
    const position = { level: 0, index: 0 };
    onClickMaker(position)();
    expect(setInfoOnClick).toHaveBeenCalledTimes(1);
    expect(setInfoOnClick).toHaveBeenCalledWith(expect.any(Function));
    expect(setRobberPayload).toHaveBeenCalledTimes(1);
    expect(setRobberPayload).toHaveBeenCalledWith(position, null);
  });

  mk([]);

  // It should call useParams.
  expect(useParams).toHaveBeenCalledTimes(1);
  expect(useParams).not.toHaveBeenCalledWith(expect.anything());

  // It shouldn't call any of these.
  const calledDispatchs = [setInfoOnClick, setRobberPayload];
  dispatchs
    .filter((f) => !calledDispatchs.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());

  // It should show available positions.
  expect(showHCenter).toHaveBeenCalledTimes(1);
  expect(showHCenter).toHaveBeenCalledWith({}, [], colours.Building, expect.any(Function));
});

test('shows 0 available players', () => {
  const position = { level: 1, index: 2 };
  const payload = [{ players: [], position }];

  showHCenter.mockImplementation((draw, ps, colour, onClickMaker) => {
    if (showHCenter.mock.calls.length === 2) expect(onClickMaker(position)()).toBe(null);
  });

  mk(payload, position);

  // It should call useParams.
  expect(useParams).toHaveBeenCalledTimes(1);
  expect(useParams).not.toHaveBeenCalledWith(expect.anything());

  // It should show positions.
  expect(showHCenter).toHaveBeenCalledTimes(2);
  expect(showHCenter)
    .toHaveBeenNthCalledWith(1, {}, [position], colours.Building, expect.any(Function));
  expect(showHCenter)
    .toHaveBeenNthCalledWith(2, {}, [position], colours.Chosen, expect.any(Function));

  // It shouldn't call any of these.
  dispatchs.forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());

  showHCenter.mockImplementation(() => null);
});

test('shows 1 available player', () => {
  const position = { level: 1, index: 2 };
  const payload = [{ players: ['player'], position }];
  mk(payload, position);

  // It should call useParams.
  expect(useParams).toHaveBeenCalledTimes(1);
  expect(useParams).not.toHaveBeenCalledWith(expect.anything());

  // It should show positions.
  expect(showHCenter).toHaveBeenCalledTimes(2);
  expect(showHCenter)
    .toHaveBeenNthCalledWith(1, {}, [position], colours.Building, expect.any(Function));
  expect(showHCenter)
    .toHaveBeenNthCalledWith(2, {}, [position], colours.Chosen, expect.any(Function));

  // It should show available players.
  expect(setInfoOnClick).toHaveBeenCalledTimes(1);
  expect(setInfoOnClick).toHaveBeenCalledWith(expect.any(Function));

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => f !== setInfoOnClick)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());
});

test('shows 3 available players', () => {
  const players = ['0', '1', '2'];
  const position = { level: 1, index: 2 };
  const payload = [{ players, position }];

  setInfoOnClick.mockImplementationOnce((onClickMaker) => {
    const wrongPlayers = ['user', 'player', 'test', '', 1];

    // It should call setInfoOnClick with an onClick maker function.
    players.forEach((player) => {
      const n = setRobberPayload.mock.calls.length;
      // It should call setRobberPayload.
      onClickMaker(player)();
      expect(setRobberPayload).toHaveBeenCalledTimes(n + 1);
      expect(setRobberPayload).toHaveBeenCalledWith(position, player);
    });

    setRobberPayload.mockClear();

    // It should do nothing.
    wrongPlayers.forEach((player) => {
      expect(onClickMaker(player)).toBe(null);
      expect(setRobberPayload).not.toHaveBeenCalled();
      expect(setRobberPayload).not.toHaveBeenCalledWith(expect.anything());
    });
  });

  const { queryByTestId } = mk(payload, position);

  // It should force user selection.
  expect(queryByTestId('actions-positioning-confirm')).toBeDisabled();

  // It should set InfoOnClick.
  expect(setInfoOnClick).toHaveBeenCalledTimes(1);
  expect(setInfoOnClick).toHaveBeenCalledWith(expect.any(Function));

  expect(showHCenter).toHaveBeenCalledTimes(2);
  expect(showHCenter)
    .toHaveBeenNthCalledWith(1, {}, [position], colours.Building, expect.any(Function));
  expect(showHCenter)
    .toHaveBeenNthCalledWith(2, {}, [position], colours.Chosen, expect.any(Function));

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => f !== setInfoOnClick)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());
});

test('calls no functions but showHCenter', () => {
  const position = { level: 1, index: 2 };
  mk([], position, 'player');

  // It shouldn't call any of these just yet.
  dispatchs.forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns.forEach((f) => expect(f).not.toHaveBeenCalled());
});

test('calls setInfoOnClick and moveRobber', () => {
  const position = { level: 1, index: 2 };
  const { queryByTestId } = mk([], position, 'player');

  fireEvent.click(queryByTestId('actions-positioning-confirm'));

  // It should unset InfoOnClick.
  expect(setInfoOnClick).toHaveBeenCalledTimes(1);
  expect(setInfoOnClick).toHaveBeenCalledWith(expect.any(Function));

  expect(moveRobber).toHaveBeenCalledTimes(1);
  expect(moveRobber)
    .toHaveBeenCalledWith('1', position, 'player',
      expect.any(Function), expect.any(Function));

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => f !== setInfoOnClick)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns
    .filter((f) => f !== moveRobber)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
});

test('calls setInfoOnClick and playKnight', () => {
  const position = { level: 1, index: 2 };
  const { queryByTestId } = mk([], position, 'player', 'play_knight_card');

  fireEvent.click(queryByTestId('actions-positioning-confirm'));

  // It should unset InfoOnClick.
  expect(setInfoOnClick).toHaveBeenCalledTimes(1);
  expect(setInfoOnClick).toHaveBeenCalledWith(expect.any(Function));

  expect(playKnight).toHaveBeenCalledTimes(1);
  expect(playKnight)
    .toHaveBeenCalledWith('1', position, 'player',
      expect.any(Function), expect.any(Function));

  // It shouldn't call any of these.
  dispatchs
    .filter((f) => f !== setInfoOnClick)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns
    .filter((f) => f !== playKnight)
    .forEach((f) => expect(f).not.toHaveBeenCalled());
});

test('calls refresh on confirm', () => {
  moveRobber.mockImplementationOnce((id, position, player, onSuccess) => {
    onSuccess();
  });

  setInfoOnClick.mockImplementationOnce((fun) => {
    expect(fun()).toBe(null);
  });

  const position = { level: 1, index: 2 };
  const { queryByTestId } = mk([], position, 'player');

  fireEvent.click(queryByTestId('actions-positioning-confirm'));

  // It should refresh.
  expect(setWaiting).toHaveBeenCalledTimes(1);
  expect(setWaiting).not.toHaveBeenCalledWith(expect.anything());
  expect(setGameRunning).toHaveBeenCalledTimes(1);
  expect(setGameRunning).not.toHaveBeenCalledWith(expect.anything());
  expect(getGameStatus).toHaveBeenCalledTimes(1);
  expect(getGameStatus).toHaveBeenCalledWith('1', setGameState, setError);

  // It shouldn't call any of these.
  const calledDispatchs = [setInfoOnClick, setWaiting, setGameRunning];
  const calledMocks = [moveRobber, getGameStatus];
  dispatchs
    .filter((f) => !calledDispatchs.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns
    .filter((f) => !calledMocks.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
});

test('calls refresh on cancel', () => {
  setInfoOnClick.mockImplementationOnce((fun) => {
    expect(fun()).toBe(null);
  });

  const position = { level: 1, index: 2 };
  const { queryByTestId } = mk([], position, 'player');

  fireEvent.click(queryByTestId('actions-positioning-cancel'));

  // It should refresh.
  expect(setWaiting).toHaveBeenCalledTimes(1);
  expect(setWaiting).not.toHaveBeenCalledWith(expect.anything());
  expect(setGameRunning).toHaveBeenCalledTimes(1);
  expect(setWaiting).not.toHaveBeenCalledWith(expect.anything());
  expect(getGameStatus).toHaveBeenCalledTimes(1);
  expect(getGameStatus).toHaveBeenCalledWith('1', setGameState, setError);
  expect(setInfoOnClick).toHaveBeenCalledTimes(1);
  expect(setInfoOnClick).toHaveBeenCalledWith(expect.any(Function));

  // It shouldn't call any of these.
  const calledDispatchs = [setWaiting, setGameRunning, setInfoOnClick];
  const calledMocks = [getGameStatus];
  dispatchs
    .filter((f) => !calledDispatchs.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
  mockFns
    .filter((f) => !calledMocks.includes(f))
    .forEach((f) => expect(f).not.toHaveBeenCalled());
});
