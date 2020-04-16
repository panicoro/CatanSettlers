import React from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';
import PropTypes from 'prop-types';

import {
  dispatchWaiting,
  dispatchError,
  dispatchRobberPayload,
} from './Actions.ducks';
import {
  setRunning as dispatchGameRunning,
  setState as dispatchGameState,
} from '../Game/Game.ducks';
import { dispatchOnClick } from '../Info/Info.ducks';
import RobbingScreen from '../../components/Actions/Positioning';
import showHCenter from '../../components/Board/ShowHCenter';
import { colours } from '../../utils/Constants';
import { getGameStatus, moveRobber, playKnight } from '../../utils/Api';
import { HexagonPosition } from '../../utils/ApiTypes';


const request = {
  move_robber: moveRobber,
  play_knight_card: playKnight,
};

export const mapStateToProps = (state, ownProps) => {
  const { type } = ownProps;
  const action = state.Game.actions.find((a) => a && a.type === type);
  const { position, player } = state.Actions.robberPayload;

  return ({
    draw: state.Board.draw,
    payload: action.payload,
    position,
    player,
  });
};

export const mapDispatchToProps = {
  setError: dispatchError,
  setWaiting: dispatchWaiting,
  setGameRunning: dispatchGameRunning,
  setGameState: dispatchGameState,
  setRobberPayload: dispatchRobberPayload,
  setInfoOnClick: dispatchOnClick,
};

export const Robbing = (props) => {
  const {
    draw, payload, position, type, player,
  } = props;
  const { setError, setRobberPayload, setWaiting } = props;
  const { setGameRunning, setGameState } = props;
  const { setInfoOnClick } = props;
  const { id } = useParams();

  const refresh = () => {
    setWaiting();
    setGameRunning();
    getGameStatus(id, setGameState, setError);
  };
  const onConfirm = () => {
    setInfoOnClick(() => null);
    request[type](id, position, player, refresh, setError);
  };
  const onCancel = () => {
    setInfoOnClick(() => null);
    refresh();
  };

  // Shows all available robber positions.
  const showPositions = () => {
    const ps = payload.map((x) => x.position);
    const onClickMaker = (p) => () => {
      // If position changed, we must change InfoOnClick.
      setInfoOnClick(() => null);

      // We need to create a new position to re-render the component.
      setRobberPayload(JSON.parse(JSON.stringify(p)), null);
    };
    showHCenter(draw, ps, colours.Building, onClickMaker);
  };
  // Makes players clickable.
  const showPlayers = (players) => {
    setInfoOnClick((p) => {
      // If user can be chosen, make them clickable.
      if (players.includes(p)) return () => { setRobberPayload(position, p); };
      return null;
    });
  };

  let players;

  showPositions();

  // Once position is set, show it.
  if (position) {
    showHCenter(draw, [position], colours.Chosen, () => () => null);

    if (!player) {
    // Find available players for the chosen position.
      players = payload.find((x) => (x
      && x.position.level === position.level
      && x.position.index === position.index)).players;

      // Show players only if needed.
      if (players.length >= 1) showPlayers(players);
    }
  }

  // User must choose a player if they can.
  const playerSet = player || (players && players.length < 1);

  let message = 'Choose a position';
  if (position && !playerSet) message = 'Choose a player';
  if (playerSet) message = 'Confirm';

  return (
    <RobbingScreen
      message={message}
      onCancel={onCancel}
      onConfirm={position && playerSet ? onConfirm : null}
    />
  );
};

export default connect(mapStateToProps, mapDispatchToProps)(Robbing);


Robbing.propTypes = {
  position: HexagonPosition,
  player: PropTypes.string,
  draw: PropTypes.shape({}).isRequired,
  payload: PropTypes.arrayOf(PropTypes.exact({
    players: PropTypes.arrayOf(PropTypes.string).isRequired,
    position: HexagonPosition.isRequired,
  })).isRequired,
  setError: PropTypes.func.isRequired,
  setRobberPayload: PropTypes.func.isRequired,
  setWaiting: PropTypes.func.isRequired,
  setGameRunning: PropTypes.func.isRequired,
  setGameState: PropTypes.func.isRequired,
  setInfoOnClick: PropTypes.func.isRequired,
  type: PropTypes.oneOf(['move_robber', 'play_knight_card']).isRequired,
};

Robbing.defaultProps = {
  position: null,
  player: null,
};
