import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import GameStatus from '../../components/Info/GameStatus';
import PlayerInfo from '../../components/Info/PlayerInfo';
import { PlayerType } from '../../utils/ApiTypes';


export const mapStateToProps = (state) => ({
  players: state.Game.info.players,
  currentTurn: state.Game.info.currentTurn,
  winner: state.Game.info.winner,
  playerOnClick: state.Info.playerOnClick,
});

export const Info = (props) => {
  const {
    players, currentTurn, winner, playerOnClick,
  } = props;

  return (
    <>
      {players.map((player) => (
        <PlayerInfo
          player={player}
          key={player.username}
          onTurn={player.username === currentTurn.user}
          playerOnClick={playerOnClick(player.username)}
        />
      ))}
      <GameStatus currentTurn={currentTurn} winner={winner} />
    </>
  );
};

export default connect(mapStateToProps)(Info);


Info.propTypes = {
  players: PropTypes.arrayOf(PlayerType).isRequired,
  currentTurn: PropTypes.shape({
    user: PropTypes.string.isRequired,
    dice: PropTypes.arrayOf(PropTypes.number).isRequired,
  }).isRequired,
  winner: PropTypes.string,
  playerOnClick: PropTypes.func.isRequired,
};

Info.defaultProps = {
  winner: null,
};
