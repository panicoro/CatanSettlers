import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';

import { Info, mapStateToProps } from '../../src/containers/Info/Info';
import { dispatchOnClick } from '../../src/containers/Info/Info.ducks';
import { info } from '../../src/utils/BoardData';


const { players, currentTurn } = info;

const playerOnClick = () => () => () => null;

test('should show previously rolled value', () => {
  const initialState = {
    Game: { info: { players, currentTurn } },
    Info: { playerOnClick },
  };

  expect(mapStateToProps(initialState).players).toEqual(players);
});

test('should dispatch info/SET_CLICK action', () => {
  expect(dispatchOnClick(playerOnClick)).toEqual({
    type: 'info/SET_CLICK',
    payload: { playerOnClick },
  });
});

test('render one card for player', () => {
  const { queryAllByTestId } = render(
    <Info
      players={players}
      currentTurn={currentTurn}
      playerOnClick={playerOnClick}
    />,
  );
  const cards = queryAllByTestId('card');
  expect(cards).toHaveLength(players.length);
});

test('render the winning player', () => {
  const winner = 'user3';
  const { getByTestId } = render(
    <Info
      players={players}
      currentTurn={currentTurn}
      winner={winner}
      playerOnClick={playerOnClick}
    />,
  );
  const td = getByTestId('winner');
  expect(td).toHaveTextContent(winner);
});

test('player in turn should have font-weight', () => {
  const { queryAllByTestId } = render(
    <Info
      players={players}
      currentTurn={currentTurn}
      playerOnClick={playerOnClick}
    />,
  );

  const cards = queryAllByTestId('card');
  cards.forEach((card) => {
    const user = card.querySelector('div button').textContent;
    if (user === currentTurn.user) {
      expect(card).toHaveStyle('font-weight: bold');
    } else {
      expect(card).toHaveStyle('font-weight: normal');
      expect(card).toHaveStyle('background-color: white');
    }
  });
});
