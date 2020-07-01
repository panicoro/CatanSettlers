import React, { useEffect } from 'react';
import { Redirect, useParams, Link } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import Button from 'react-bootstrap/Button';
import Error from '../../components/Error';
import WaitingScreen from '../../components/Rooms/Waiting';
import { getRoom, startGame, cancelRoom } from '../../utils/Api';
import useInterval from '../../utils/UseInterval';
import { dispatchRoom, dispatchWaiting, dispatchLoading } from './Rooms.ducks';
import { RoomType } from '../../utils/ApiTypes';


export const mapStateToProps = (state) => ({
  username: state.Auth.username,
  room: state.Rooms.room,
  stage: state.Rooms.waitingStage,
  loading: state.Rooms.createLoading,
});

export const mapDispatchToProps = ({
  setRoom: dispatchRoom,
  setStage: dispatchWaiting,
  setLoading: dispatchLoading,
});

export const Waiting = ({
  username, room, setRoom, setStage, setLoading, stage, loading,
}) => {
  const { id } = useParams();

  const onSuccess = (r) => {
    setRoom(r);
    setStage(r.game_has_started ? 'started' : 'running');
  };
  const onFailure = () => {
    setStage('error');
    setLoading(false);
  };

  // Refresh every 5 seconds and when mounted.
  const refresh = () => { getRoom(id, onSuccess, onFailure); };
  useEffect(refresh, []);
  useInterval(() => { if (stage !== 'started') refresh(); }, 2000);

  const gameId = !!room && room.game_has_started ? room.game_id : null;
  const iAmOwner = !!room && room.owner === username;
  const onStart = () => {
    setLoading(true);
    startGame(id, refresh, onFailure);
  };
  const onCancel = () => {
    cancelRoom(id, () => setStage('canceled'), () => setStage('error'));
  };

  if (stage === 'empty') return (<div data-testid="waiting-empty" />);

  if (stage === 'canceled') {
    setStage('empty');
    return (<Redirect to="/rooms" push />);
  }

  if (stage === 'started') {
    setStage('empty');
    return (<Redirect to={`/game/${gameId}`} push />);
  }

  if (stage === 'running') {
    return (
      <WaitingScreen
        room={room}
        onStart={iAmOwner ? onStart : null}
        onCancel={iAmOwner ? onCancel : null}
        loading={loading}
      />
    );
  }

  return (
    <div>
      <Error />
      <Link to="/rooms">
        <Button>
          Back to Rooms
        </Button>
      </Link>
    </div>
  );
};

export default connect(mapStateToProps, mapDispatchToProps)(Waiting);


Waiting.propTypes = {
  username: PropTypes.string.isRequired,
  room: RoomType,
  setRoom: PropTypes.func.isRequired,
  setStage: PropTypes.func.isRequired,
  setLoading: PropTypes.func.isRequired,
  stage: PropTypes.string.isRequired,
  loading: PropTypes.bool.isRequired,
};

Waiting.defaultProps = {
  room: null,
};
