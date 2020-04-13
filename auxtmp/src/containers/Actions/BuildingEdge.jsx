import React from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';
import PropTypes from 'prop-types';

import {
  dispatchWaiting,
  dispatchError,
  dispatchEdgePayload,
} from './Actions.ducks';
import {
  setRunning as dispatchGameRunning,
  setState as dispatchGameState,
} from '../Game/Game.ducks';
import BuildingScreen from '../../components/Actions/Positioning';
import showEdges from '../../components/Board/ShowEdges';
import { colours } from '../../utils/Constants';
import { getGameStatus, buildRoad } from '../../utils/Api';
import { RoadPosition } from '../../utils/ApiTypes';


export const mapStateToProps = (state) => {
  const action = state.Game.actions
    .find((a) => a && a.type === 'build_road');

  return ({
    draw: state.Board.draw,
    payload: action.payload,
    position: state.Actions.edgePayload,
  });
};

export const mapDispatchToProps = {
  setError: dispatchError,
  setWaiting: dispatchWaiting,
  setGameRunning: dispatchGameRunning,
  setGameState: dispatchGameState,
  setEdgePayload: dispatchEdgePayload,
};

export const BuildingEdge = (props) => {
  const { draw, payload, position } = props;
  const { id } = useParams();
  const { setError, setEdgePayload, setWaiting } = props;
  const { setGameRunning, setGameState } = props;

  const refresh = () => {
    setWaiting();
    setGameRunning();
    getGameStatus(id, setGameState, setError);
  };
  const onConfirm = () => {
    buildRoad(id, position, refresh, setError);
  };

  const showPositions = () => {
    const onClickMaker = (p) => () => {
      // We need to create a new position to re-render the component.
      setEdgePayload(JSON.parse(JSON.stringify(p)));
    };
    showEdges(draw, payload, colours.Building, onClickMaker);
  };

  showPositions();

  // Once position is set, show it.
  if (position) {
    showEdges(draw, [position], colours.Chosen, () => () => null);
  }

  return (
    <BuildingScreen
      message="Please choose a position"
      onCancel={refresh}
      onConfirm={position && onConfirm}
    />
  );
};

export default connect(mapStateToProps, mapDispatchToProps)(BuildingEdge);


BuildingEdge.propTypes = {
  position: RoadPosition,
  draw: PropTypes.shape({}).isRequired,
  payload: PropTypes.arrayOf(RoadPosition).isRequired,
  setError: PropTypes.func.isRequired,
  setEdgePayload: PropTypes.func.isRequired,
  setWaiting: PropTypes.func.isRequired,
  setGameRunning: PropTypes.func.isRequired,
  setGameState: PropTypes.func.isRequired,
};

BuildingEdge.defaultProps = {
  position: null,
};
