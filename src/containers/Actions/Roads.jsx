import React from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';
import PropTypes from 'prop-types';

import {
  dispatchWaiting,
  dispatchError,
  dispatch2RoadsPayload,
} from './Actions.ducks';
import {
  setRunning as dispatchGameRunning,
  setState as dispatchGameState,
} from '../Game/Game.ducks';
import RoadsScreen from '../../components/Actions/Positioning';
import showEdges from '../../components/Board/ShowEdges';
import { colours } from '../../utils/Constants';
import { getGameStatus, play2Roads } from '../../utils/Api';
import { RoadPosition } from '../../utils/ApiTypes';


export const mapStateToProps = (state) => {
  const action = state.Game.actions
    .find((a) => a && a.type === 'play_road_building_card');
  const { p0, p1 } = state.Actions.roadsPayload;

  return ({
    draw: state.Board.draw,
    payload: action.payload,
    p0,
    p1,
  });
};

export const mapDispatchToProps = {
  setError: dispatchError,
  setWaiting: dispatchWaiting,
  setGameRunning: dispatchGameRunning,
  setGameState: dispatchGameState,
  set2RoadsPayload: dispatch2RoadsPayload,
};

export const Roads = (props) => {
  const {
    draw, payload, p0, p1,
  } = props;
  const { id } = useParams();
  const { setError, set2RoadsPayload, setWaiting } = props;
  const { setGameRunning, setGameState } = props;

  const refresh = () => {
    setWaiting();
    setGameRunning();
    getGameStatus(id, setGameState, setError);
  };
  const onConfirm = () => {
    play2Roads(id, p0, p1, refresh, setError);
  };

  const showPositions = () => {
    const onClickMaker = (p) => () => {
      // We need to create a new position to re-render the component.
      if (!p0) set2RoadsPayload(JSON.parse(JSON.stringify(p)), p1);
      else set2RoadsPayload(p0, JSON.parse(JSON.stringify(p)));
    };
    showEdges(draw, payload, colours.Building, onClickMaker);
  };

  // If both roads are set, no need to choose.
  if (p0 && p1) showEdges(draw, payload, colours.Building, () => () => null);

  // If either position is unset, show available positions.
  if (!p0 || !p1) showPositions();

  // If p0 is set, show it as such.
  if (p0) showEdges(draw, [p0], colours.Chosen, () => () => null);

  // If p1 is set, show it as such.
  if (p1) showEdges(draw, [p1], colours.Chosen, () => () => null);

  return (
    <RoadsScreen
      message="Choose two positions"
      onCancel={refresh}
      onConfirm={p0 && p1 && onConfirm}
    />
  );
};

export default connect(mapStateToProps, mapDispatchToProps)(Roads);


Roads.propTypes = {
  p0: RoadPosition,
  p1: RoadPosition,
  draw: PropTypes.shape({}).isRequired,
  payload: PropTypes.arrayOf(RoadPosition).isRequired,
  setError: PropTypes.func.isRequired,
  set2RoadsPayload: PropTypes.func.isRequired,
  setWaiting: PropTypes.func.isRequired,
  setGameRunning: PropTypes.func.isRequired,
  setGameState: PropTypes.func.isRequired,
};

Roads.defaultProps = {
  p0: null,
  p1: null,
};
