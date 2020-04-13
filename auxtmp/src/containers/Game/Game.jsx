import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';
import PropTypes from 'prop-types';

import {
  setError as dispatchError,
  setRunning as dispatchRunning,
  setState as dispatchState,
} from './Game.ducks';
import Error from '../../components/Error';
import GameScreen from '../../components/Game/Game';
import { getGameStatus } from '../../utils/Api';
import useInterval from '../../utils/UseInterval';


const mapStateToProps = (state) => ({
  actions: state.Game.actions,
  board: state.Game.board,
  hand: state.Game.hand,
  info: state.Game.info,
  stage: state.Game.stage,
});

const mapDispatchToProps = ({
  setError: dispatchError,
  setRunning: dispatchRunning,
  setState: dispatchState,
});

export const Game = (props) => {
  const { stage } = props;
  const {
    setError, setRunning, setState,
  } = props;
  const { id } = useParams();

  // Initialise state.
  useEffect(() => {
    const init = (actions, board, hand, info) => {
      setState(actions, board, hand, info);
      setRunning();
    };
    getGameStatus(id, init, setError);
  }, [id, setError, setRunning, setState]);

  // Fetch data from API every 5 seconds.
  useInterval(() => { if (stage !== 'frozen') getGameStatus(id, setState, setError); }, 2000);

  if (stage === 'empty') return (<></>);

  if (stage === 'running' || stage === 'frozen') return (<GameScreen />);

  return (<Error />);
};

export default connect(mapStateToProps, mapDispatchToProps)(Game);


Game.propTypes = PropTypes.shape({
  stage: PropTypes.string.isRequired,
  setError: PropTypes.func.isRequired,
  setRunning: PropTypes.func.isRequired,
  setState: PropTypes.func.isRequired,
}).isRequired;
