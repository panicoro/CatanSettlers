import PropTypes from 'prop-types';

import {
  ActionType, BoardType, HandType, InfoType,
} from '../../utils/ApiTypes';

const SET_ERROR = 'game/SET_ERROR';
const SET_FROZEN = 'game/SET_FROZEN';
const SET_RUNNING = 'game/SET_RUNNING';
const SET_STATE = 'game/SET_STATE';

export const setError = () => ({
  type: SET_ERROR,
});

export const setFrozen = () => ({
  type: SET_FROZEN,
});

export const setRunning = () => ({
  type: SET_RUNNING,
});

export const setState = (
  actions, board, hand, info,
) => ({
  type: SET_STATE,
  payload: {
    actions,
    board,
    hand,
    info,
  },
});

export const initialState = {
  stage: 'empty',
  actions: {},
  board: {},
  hand: {},
  info: {},
  refresh: null,
};

const reducer = (state = initialState, action = {}) => {
  switch (action.type) {
    case SET_ERROR:
      return { ...initialState, stage: 'error' };

    case SET_FROZEN:
      return { ...state, stage: 'frozen' };

    case SET_RUNNING:
      return { ...state, stage: 'running' };

    case SET_STATE:
      if (state.stage !== 'frozen') return { ...state, ...action.payload };
      return state;

    default: return state;
  }
};

export default reducer;


setRunning.propTypes = {
  actions: PropTypes.arrayOf(ActionType),
  board: BoardType,
  hand: HandType,
  info: InfoType,
};

reducer.propTypes = {
  action: PropTypes.string.isRequired,
  payload: PropTypes.oneOfType([
    PropTypes.func,
    PropTypes.shape({
      stage: PropTypes.string.isRequired,
      actions: PropTypes.arrayOf(ActionType),
      board: BoardType,
      hand: HandType,
      info: InfoType,
    }),
  ]),
};
