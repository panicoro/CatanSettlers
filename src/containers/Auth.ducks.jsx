import PropTypes from 'prop-types';


// Actions.
export const SET_AUTH = 'app/SET_AUTH';
export const SET_USERNAME = 'app/SET_USERNAME';

export const initialState = {
  auth: false,
  username: localStorage.getItem('username'),
};

const reducer = (state = initialState, action = {}) => {
  switch (action.type) {
    case SET_AUTH:
      return { ...state, auth: action.payload };

    case SET_USERNAME:
      return { ...state, username: action.payload };

    default: return state;
  }
};

export const setAuth = (value) => ({ type: SET_AUTH, payload: value });
export const setUser = (username) => ({ type: SET_USERNAME, payload: username });

export default reducer;


reducer.propTypes = {
  state: PropTypes.shape({
    auth: PropTypes.bool,
    username: PropTypes.string,
  }),
  action: PropTypes.shape({
    type: PropTypes.string,
    payload: PropTypes.oneOfType([PropTypes.string, PropTypes.bool]),
  }),
};

setAuth.propTypes = {
  value: PropTypes.bool.isRequired,
};
setUser.propTypes = {
  username: PropTypes.string.isRequired,
};
