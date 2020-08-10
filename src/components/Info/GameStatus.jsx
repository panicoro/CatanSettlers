import React from 'react';
import Table from 'react-bootstrap/Table';
import PropTypes from 'prop-types';
import icon from '../../images/two_dices.png';


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
    <Table borderless size="lg">
      <tbody>
          <div className='container'>
          <td data-testid="dice">
          <img
            alt=""
            src={icon}
            width="60"
            height="60"
            className="d-inline-block"
            />{' '}
            {`${currentTurn.dice[0]} + ${currentTurn.dice[1]} = `}
            { currentTurn.dice[0] + currentTurn.dice[1]}
          </td>
          </div>
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
