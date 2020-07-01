import React from 'react';
import Table from 'react-bootstrap/Table';
import PropTypes from 'prop-types';


const GameStatus = ({ currentTurn, winner }) => {
  if (winner) {
    return (
      <Table borderless size="sm">
        <tbody>
          <tr>
            <td><h1>Winner:</h1></td>
          </tr>
          <tr>
            <td data-testid="winner"><h1>{winner}</h1></td>
          </tr>
        </tbody>
      </Table>
    );
  }

  return (
    <Table borderless size="sm">
      <tbody>
        <tr>
          <td>Dice:</td>
          <td data-testid="dice">
            {`${currentTurn.dice[0]}, ${currentTurn.dice[1]}`}
          </td>
        </tr>
      </tbody>
    </Table>
  );
};

export default GameStatus;


GameStatus.propTypes = {
  currentTurn: PropTypes.shape({
    user: PropTypes.string.isRequired,
    dice: PropTypes.arrayOf(PropTypes.number).isRequired,
  }).isRequired,
  winner: PropTypes.string,
};

GameStatus.defaultProps = {
  winner: null,
};
