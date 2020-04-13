import React from 'react';
import { render } from '@testing-library/react';
import GameStatus from '../../src/components/Info/GameStatus';
import { info } from '../../src/utils/BoardData';


const { currentTurn } = info;

test('render GameStatus with no winner', () => {
  const { queryAllByTestId } = render(
    <GameStatus currentTurn={currentTurn} />,
  );

  const dice = queryAllByTestId('dice');
  expect(dice).toHaveLength(1);
  expect(dice[0].textContent).toEqual(`${currentTurn.dice[0]}, ${currentTurn.dice[1]}`);

  const tdWinner = queryAllByTestId('winner');
  expect(tdWinner).toHaveLength(0);
});

test('render GameStatus with one winner', () => {
  const { queryAllByTestId } = render(
    <GameStatus currentTurn={currentTurn} winner="winner" />,
  );

  const winners = queryAllByTestId('winner');
  expect(winners).toHaveLength(1);
  expect(winners[0].textContent).toBe('winner');

  const tdTurn = queryAllByTestId('turn-user');
  expect(tdTurn).toHaveLength(0);

  const tdDice = queryAllByTestId('dice');
  expect(tdDice).toHaveLength(0);
});
