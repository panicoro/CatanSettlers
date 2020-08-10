import React from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';
import PropTypes from 'prop-types';

import {
  dispatchError,
  dispatchWaiting,
} from './Actions.ducks';
import {
  setRunning as dispatchGameRunning,
  setState as dispatchGameState,
} from '../Game/Game.ducks';
/* eslint-disable import/no-named-as-default */
import ActionsScreen from '../../components/Actions/Actions';
import Error from '../../components/Error';
/* eslint-enable import/no-named-as-default */
import actionsContainers from './ActionsContainers';
import { getGameStatus } from '../../utils/Api';


export const mapStateToProps = (state) => ({
  moveRobber: state.Game.actions.some((x) => x && x.type === 'move_robber'),
  stage: state.Actions.stage,
});

export const mapDispatchToProps = ({
  setError: dispatchError,
  setWaiting: dispatchWaiting,
  setGameRunning: dispatchGameRunning,
  setGameState: dispatchGameState,
});

export const Actions = (props) => {
  const { moveRobber, stage } = props;
  const {
    setError, setWaiting,
    setGameState, setGameRunning,
  } = props;
  const { id } = useParams();

  const refresh = () => {
    setWaiting();
    setGameRunning();
    getGameStatus(id, setGameState, setError);
  };

  if (stage === 'running/buying') return (actionsContainers.buying);

  if (stage === 'running/building/city') {
    return (actionsContainers.buildingCity);
  }

  if (stage === 'running/building/road') {
    return (actionsContainers.buildingRoad);
  }

  if (stage === 'running/building/settlement') {
    return (actionsContainers.buildingSettlement);
  }

  if (stage === 'running/robbing' && moveRobber) {
    return (actionsContainers.robberRobbing);
  }

  if (stage === 'running/robbing' && !moveRobber) {
    return (actionsContainers.knightRobbing);
  }

  if (stage === 'running/2roads') {
    return (actionsContainers.roads);
  }

  if (moveRobber) return (actionsContainers.moveRobber);

  if (stage === 'waiting') return (<ActionsScreen />);

  return (<Error onClose={refresh} />);
};

export default connect(mapStateToProps, mapDispatchToProps)(Actions);


Actions.propTypes = {
  moveRobber: PropTypes.bool.isRequired,
  stage: PropTypes.string.isRequired,
  setError: PropTypes.func.isRequired,
  setWaiting: PropTypes.func.isRequired,
  setGameRunning: PropTypes.func.isRequired,
  setGameState: PropTypes.func.isRequired,
};
