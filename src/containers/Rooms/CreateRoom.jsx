import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';

import { dispatchRunning } from './Rooms.ducks';
import Error from '../../components/Error';
import CreateScreen from '../../components/Rooms/CreateRoom';
import { createRoom, getBoards, joinRoom } from '../../utils/Api';


const initialState = {
  roomName: '',
  boardId: '',
  roomNameValid: false,
  roomNameError: '',
  boardIdValid: false,
  boardIdError: '',
  loading: false,

};

export const mapDispatchToProps = ({
  setRunning: dispatchRunning,
});

export const CreateRoom = ({ setRunning }) => {
  const [boards, setBoards] = useState([]);
  const [error, setError] = useState('');
  const [redir, setRedir] = useState(null);
  const [formData, setFormData] = useState(initialState);

  useEffect(() => {
    const onSuccess = (res) => { setBoards(res); };
    const onFailure = () => {
      setError('Connection error, the boards could not be obtained');
    };
    getBoards(onSuccess, onFailure);
  }, []);

  // Handles roomName changes.
  const changeRoomName = (e) => {
    let roomName = e.target.value;
    let valid = true;
    let errorMsg = '';

    if (!roomName) {
      roomName = '';
      valid = false;
      errorMsg = 'This field is required';
    } else if (roomName.length < 4) {
      valid = false;
      errorMsg = 'Please enter at leaset 4 characters';
    }

    setFormData({
      ...formData,
      roomName,
      roomNameValid: valid,
      roomNameError: errorMsg,
    });
  };

  // Handles boardId changes.
  const changeBoardId = (e) => {
    let boardId = e.target.value;
    let valid = true;
    let errorMsg = '';

    if (!boardId) {
      boardId = '';
      valid = false;
      errorMsg = 'Choose a board is required';
    }

    setFormData({
      ...formData,
      boardId,
      boardIdValid: valid,
      boardIdError: errorMsg,
    });
  };

  // Send data via API.
  // First create room, then join and redirect to Waiting screen.
  const handleSubmit = (e) => {
    e.preventDefault();

    const onJoinSuccess = (id) => () => {
      setRedir(id);
      setRunning();
    };

    const onFailure = (err) => { setError(err.message); };

    const onCreateSuccess = (room) => {
      joinRoom(room.id, onJoinSuccess(room.id), onFailure);
    };

    const { roomName, boardId } = formData;

    createRoom(roomName, boardId, onCreateSuccess, onFailure);
  };

  const validate = () => {
    const { roomNameValid, boardIdValid } = formData;
    return (roomNameValid && boardIdValid);
  };

  const {
    roomName, roomNameError, boardIdError, loading,
  } = formData;

  if (redir) return (<Redirect to={`/waiting/${redir}`} push />);

  if (error) return (<Error message={error} onClose={() => setError(null)} />);

  return (
    <CreateScreen
      boards={boards}
      loading={loading}
      roomName={roomName}
      roomNameError={roomNameError}
      boardIdError={boardIdError}
      handleSubmit={handleSubmit}
      changeRoomName={changeRoomName}
      changeBoardId={changeBoardId}
      validate={validate}
    />
  );
};

export default connect(null, mapDispatchToProps)(CreateRoom);


CreateRoom.propTypes = {
  setRunning: PropTypes.func.isRequired,
};
