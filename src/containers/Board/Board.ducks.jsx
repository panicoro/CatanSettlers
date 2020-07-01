import PropTypes from 'prop-types';


const SET_DRAW = 'board/SET_DRAW';

export const dispatchDraw = (draw) => ({
  type: SET_DRAW,
  payload: { draw },
});

export const initialState = {
  draw: null,
};

const reducer = (state = initialState, action = {}) => {
  const { type, payload } = action;
  switch (type) {
    case SET_DRAW:
      return { ...state, draw: payload.draw };

    default: return state;
  }
};

export default reducer;


dispatchDraw.propTypes = {
  draw: PropTypes.shape({
    type: PropTypes.string.isRequired,
  }).isRequired,
};

reducer.propTypes = {
  action: PropTypes.string.isRequired,
  payload: PropTypes.shape({
    type: PropTypes.string.isRequired,
  }).isRequired,
};
