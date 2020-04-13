import React from 'react';
import Card from 'react-bootstrap/Card';
import PropTypes from 'prop-types';
import Button from 'react-bootstrap/Button';
import Table from 'react-bootstrap/Table';

import './PlayerInfo.css';


const PlayerInfo = ({ player, onTurn, playerOnClick }) => {
  const {
    username, colour, developmentCards,
    resourceCards, victoryPoints, lastGained,
  } = player;

  const title = (
    <Card.Title>
      <Button
        id="player-button"
        block
        disabled={!playerOnClick}
        onClick={playerOnClick}
      >
        {username}
      </Button>
    </Card.Title>
  );

  const body = (
    <Table borderless size="sm">
      <tbody>
        <tr>
          <td>Victory Points:</td>
          <td>{victoryPoints}</td>
        </tr>
        <tr>
          <td>Development Cards:</td>
          <td>{developmentCards}</td>
        </tr>
        <tr>
          <td>Resources:</td>
          <td>{resourceCards}</td>
        </tr>
        <tr>
          <td>Gained:</td>
          <td>{lastGained.join(', ')}</td>
        </tr>
      </tbody>
    </Table>
  );

  return (
    <Card
      data-testid="card"
      style={{
        borderColor: colour,
        backgroundColor: onTurn ? colour : 'white',
        fontWeight: onTurn ? 'bold' : 'normal',
      }}
    >
      {title}
      {body}
    </Card>
  );
};


export default PlayerInfo;

PlayerInfo.propTypes = {
  player: PropTypes.shape({
    username: PropTypes.string.isRequired,
    colour: PropTypes.string.isRequired,
    developmentCards: PropTypes.number.isRequired,
    resourceCards: PropTypes.number.isRequired,
    victoryPoints: PropTypes.number.isRequired,
    lastGained: PropTypes.arrayOf(PropTypes.string).isRequired,
  }).isRequired,
  onTurn: PropTypes.bool.isRequired,
  playerOnClick: PropTypes.func,
};

PlayerInfo.defaultProps = {
  playerOnClick: null,
};
