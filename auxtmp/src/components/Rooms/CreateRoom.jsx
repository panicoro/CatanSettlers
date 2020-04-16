import React from 'react';
import Button from 'react-bootstrap/Button';
import FormControl from 'react-bootstrap/FormControl';
import FormGroup from 'react-bootstrap/FormGroup';
import FormLabel from 'react-bootstrap/FormLabel';
import PropTypes from 'prop-types';

import { BoardListType } from '../../utils/ApiTypes';


const CreateRoom = (props) => {
  const {
    boards, roomName, loading,
  } = props;
  const { roomNameError, boardIdError } = props;
  const {
    handleSubmit, changeRoomName, changeBoardId, validate,
  } = props;

  const nameForm = (
    <FormGroup bssize="large">
      <FormLabel>
        Room name
      </FormLabel>
      <FormControl
        autoFocus
        data-testid="room-name"
        type="text"
        value={roomName}
        isInvalid={!!roomNameError}
        onChange={changeRoomName}
      />
      <FormControl.Feedback type="invalid">
        {roomNameError}
      </FormControl.Feedback>
    </FormGroup>
  );

  const options = boards.map((board) => (
    <option
      data-testid="board-name"
      key={board.id}
      value={board.id}
    >
      {board.name}
    </option>
  ));

  const selectForm = (
    <FormGroup>
      <FormLabel>Select Board</FormLabel>
      <FormControl
        as="select"
        data-testid="board-select"
        onChange={changeBoardId}
        isInvalid={!!boardIdError}
      >
        <option value="">
          -- Please choose a board --
        </option>
        {options}
      </FormControl>
      <FormControl.Feedback type="invalid">
        {boardIdError}
      </FormControl.Feedback>
    </FormGroup>
  );

  const button = (
    <Button
      block
      bssize="large"
      disabled={!validate()}
      type="submit"
      data-testid="button"
    >
      {loading ? 'Loading...' : 'Create Room'}
    </Button>
  );

  return (
    <div data-testid="rooms-create">
      <h1>Create Room</h1>
      <form onSubmit={handleSubmit}>
        {nameForm}
        {selectForm}
        {button}
      </form>
    </div>
  );
};

export default CreateRoom;


CreateRoom.propTypes = {
  boards: PropTypes.arrayOf(BoardListType).isRequired,
  loading: PropTypes.bool.isRequired,
  roomNameError: PropTypes.string.isRequired,
  boardIdError: PropTypes.string.isRequired,
  roomName: PropTypes.string.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  changeRoomName: PropTypes.func.isRequired,
  changeBoardId: PropTypes.func.isRequired,
  validate: PropTypes.func.isRequired,
};
