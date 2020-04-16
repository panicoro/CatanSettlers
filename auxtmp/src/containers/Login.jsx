import React, { useState } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import {
  setAuth as dispatchAuth,
  setUser as dispatchUser,
} from './Auth.ducks';
import LoginScreen from '../components/Login';
import { login } from '../utils/Api';
import useForm from './UseForm';


export const mapDispatchToProps = ({
  setAuth: dispatchAuth,
  setUser: dispatchUser,
});

export const Login = ({ setAuth, setUser }) => {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const {
    values,
    validate,
    changeUsername,
    changePassword,
  } = useForm(() => '', () => '');

  // Send data via API.
  const handleSubmit = (event) => {
    event.preventDefault();
    setLoading(true);

    const { username, password } = values;

    const onSuccess = (res) => {
      localStorage.setItem('token', JSON.stringify(res.access));
      localStorage.setItem('username', username);
      setAuth(true);
      setUser(username);
    };

    const onFailure = (err) => {
      setError(err.message);
      setLoading(false);
    };

    login(username, password, onSuccess, onFailure);
  };

  return (
    <LoginScreen
      values={values}
      error={error}
      loading={loading}
      validate={validate}
      handleSubmit={handleSubmit}
      changeUsername={changeUsername}
      changePassword={changePassword}
    />
  );
};

export default connect(
  null,
  mapDispatchToProps,
)(Login);


Login.propTypes = {
  setAuth: PropTypes.func.isRequired,
  setUser: PropTypes.func.isRequired,
};
