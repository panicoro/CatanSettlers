import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';

import {
  dispatchError,
  dispatchRunning,
  dispatchRooms,
  dispatchCreate,
} from './Rooms.ducks';
import Error from '../../components/Error';
import RoomsScreen from '../../components/Rooms/Rooms';
import { getRooms } from '../../utils/Api';
import { RoomType, RoomsStateType } from '../../utils/ApiTypes';
import useInterval from '../../utils/UseInterval';


export const mapStateToProps = (state) => ({
  rooms: state.Rooms.rooms,
  stage: state.Rooms.stage,
});

export const mapDispatchToProps = ({
  setError: dispatchError,
  setRunning: dispatchRunning,
  setRooms: dispatchRooms,
  setCreate: dispatchCreate,
});

export const Rooms = (props) => {
  const { rooms, stage } = props;
  const {
    setError, setRunning, setRooms, setCreate,
  } = props;

  const refresh = () => {
    getRooms((rs) => { setRunning(); setRooms(rs); }, setError);
  };

  // Refresh every 5 seconds and when mounted.
  useEffect(refresh, []);
  useInterval(refresh, 2000);

  if (stage === 'empty') return (<div data-testid="rooms-empty" />);

  if (stage === 'create') {
    setRunning();
    return (<Redirect to="/create" push />);
  }

  if (stage === 'running') {
    return (
      <RoomsScreen
        rooms={rooms}
        createRoom={setCreate}
      />
    );
  }

  return (<Error />);
};

export default connect(mapStateToProps, mapDispatchToProps)(Rooms);


mapStateToProps.propTypes = {
  state: RoomsStateType,
};

Rooms.propTypes = {
  rooms: PropTypes.arrayOf(RoomType).isRequired,
  stage: PropTypes.string.isRequired,
  setError: PropTypes.func.isRequired,
  setRooms: PropTypes.func.isRequired,
  setRunning: PropTypes.func.isRequired,
  setCreate: PropTypes.func.isRequired,
};
