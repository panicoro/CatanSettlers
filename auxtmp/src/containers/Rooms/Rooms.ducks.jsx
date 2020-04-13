import PropTypes from 'prop-types';

import { RoomType } from '../../utils/ApiTypes';


const SET_CREATE = 'rooms/SET_CREATE';
const SET_ERROR = 'rooms/SET_ERROR';
const SET_ROOM = 'waiting/SET_ROOM';
const SET_ROOMS = 'rooms/SET_ROOMS';
const SET_RUNNING = 'rooms/SET_RUNNING';
const SET_STAGE = 'waiting/SET_STAGE';
const SET_LOADING = 'waiting/SET_LOADING';

export const dispatchCreate = () => ({
  type: SET_CREATE,
});

export const dispatchError = () => ({
  type: SET_ERROR,
});

export const dispatchRoom = (room) => ({
  type: SET_ROOM,
  payload: room,
});

export const dispatchRooms = (rooms) => ({
  type: SET_ROOMS,
  payload: rooms,
});

export const dispatchRunning = () => ({
  type: SET_RUNNING,
});

export const dispatchWaiting = (stage) => ({
  type: SET_STAGE,
  payload: stage,
});

export const dispatchLoading = (loading) => ({
  type: SET_LOADING,
  payload: loading,
});

export const initialState = {
  stage: 'empty',
  waitingStage: 'empty',
  createLoading: false,
  refresh: null,
  rooms: [],
  room: null,
};

const reducer = (state = initialState, action = {}) => {
  const { type, payload } = action;

  switch (type) {
    case SET_CREATE:
      return { ...state, stage: 'create' };

    case SET_ERROR:
      return { ...initialState, stage: 'error' };

    case SET_ROOM:
      return { ...state, room: payload };

    case SET_ROOMS:
      return { ...state, rooms: payload };

    case SET_RUNNING:
      return { ...state, stage: 'running' };

    case SET_STAGE:
      return { ...state, waitingStage: payload };

    case SET_LOADING:
      return { ...state, createLoading: payload };

    default: return state;
  }
};

export default reducer;


dispatchRoom.propTypes = {
  room: RoomType.isRequired,
};

dispatchRooms.propTypes = {
  rooms: PropTypes.arrayOf(RoomType).isRequired,
};

reducer.propTypes = {
  action: PropTypes.string.isRequired,
  payload: PropTypes.oneOfType([
    PropTypes.func,
    PropTypes.arrayOf(RoomType),
  ]).isRequired,
};
