import React from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';
import PropTypes from 'prop-types';

import {
  dispatchWaiting,
  dispatchError,
  dispatchVertexPayload,
} from './Actions.ducks';
import {
  setRunning as dispatchGameRunning,
  setState as dispatchGameState,
} from '../Game/Game.ducks';
import BuildingScreen from '../../components/Actions/Positioning';
import showVertices from '../../components/Board/ShowVertices';
import { colours } from '../../utils/Constants';
import { getGameStatus, buildCity, buildSettlement } from '../../utils/Api';
import { BuildingPosition } from '../../utils/ApiTypes';


const request = {
  upgrade_city: buildCity,
  build_settlement: buildSettlement,
};

export const mapStateToProps = (state, ownProps) => {
  const { type } = ownProps;
  const action = state.Game.actions
    .find((a) => a && a.type === type);

  return ({
    draw: state.Board.draw,
    payload: action.payload,
    position: state.Actions.vertexPayload,
    type,
  });
};

export const mapDispatchToProps = {
  setError: dispatchError,
  setWaiting: dispatchWaiting,
  setGameRunning: dispatchGameRunning,
  setGameState: dispatchGameState,
  setVertexPayload: dispatchVertexPayload,
};

export const BuildingVertex = (props) => {
  const {
    draw, payload, position, type,
  } = props;
  const { id } = useParams();
  const { setError, setVertexPayload, setWaiting } = props;
  const { setGameRunning, setGameState } = props;
  const buildingType = type === 'upgrade_city' ? 'city' : 'settlement';

  const refresh = () => {
    setWaiting();
    setGameRunning();
    getGameStatus(id, setGameState, setError);
  };
  const onConfirm = () => {
    request[type](id, position, refresh, setError);
  };

  const showPositions = () => {
    const onClickMaker = (p) => () => {
      // We need to create a new position to re-render the component.
      setVertexPayload(JSON.parse(JSON.stringify(p)));
    };
    showVertices(draw, payload, colours.Building, buildingType, onClickMaker);
  };

  showPositions();

  // Once position is set, show it.
  if (position) {
    showVertices(draw, [position], colours.Chosen,
      buildingType, () => () => null);
  }

  return (
    <BuildingScreen
      message="Please choose a position"
      onCancel={refresh}
      onConfirm={position && onConfirm}
    />
  );
};

export default connect(mapStateToProps, mapDispatchToProps)(BuildingVertex);


BuildingVertex.propTypes = {
  position: BuildingPosition,
  draw: PropTypes.shape({}).isRequired,
  payload: PropTypes.arrayOf(BuildingPosition).isRequired,
  setError: PropTypes.func.isRequired,
  setVertexPayload: PropTypes.func.isRequired,
  setWaiting: PropTypes.func.isRequired,
  setGameRunning: PropTypes.func.isRequired,
  setGameState: PropTypes.func.isRequired,
  type: PropTypes.oneOf(['upgrade_city', 'build_settlement']).isRequired,
};

BuildingVertex.defaultProps = {
  position: null,
};
