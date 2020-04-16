import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { setAuth as dispatchAuth, setUser as dispatchUser } from './Auth.ducks';

import NavBarScreen from '../components/NavBar';


const mapStateToProps = (state) => ({
  auth: state.Auth.auth,
});

const mapDispatchToProps = ({
  setAuth: dispatchAuth,
  setUser: dispatchUser,
});

export const NavBar = ({ auth, setAuth, setUser }) => {
  const logout = () => {
    setAuth(false);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('username');
  };

  return (<NavBarScreen auth={auth} logout={logout} />);
};


export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(NavBar);


mapStateToProps.propTypes = {
  state: PropTypes.shape({
    auth: PropTypes.bool,
  }).isRequired,
};

NavBar.propTypes = {
  auth: PropTypes.bool.isRequired,
  setAuth: PropTypes.func.isRequired,
  setUser: PropTypes.func.isRequired,
};
