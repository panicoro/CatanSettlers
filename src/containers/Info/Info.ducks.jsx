import PropTypes from 'prop-types';


const SET_CLICK = 'info/SET_CLICK';

export const dispatchOnClick = (playerOnClick) => ({
  type: SET_CLICK,
  payload: { playerOnClick },
});

export const initialState = {
  playerOnClick: () => null,
};

const reducer = (state = initialState, action = {}) => {
  const { type, payload } = action;

  switch (type) {
    case SET_CLICK:
      return { ...state, ...payload };

    default: return state;
  }
};

export default reducer;


dispatchOnClick.propTypes = {
  playerOnClick: PropTypes.func.isRequired,
};

reducer.propTypes = {
  state: PropTypes.shape({
    playerOnClick: PropTypes.func.isRequired,
  }).isRequired,
  action: PropTypes.shape({
    type: PropTypes.string.isRequired,
    payload: PropTypes.func.isRequired,
  }).isRequired,
};
