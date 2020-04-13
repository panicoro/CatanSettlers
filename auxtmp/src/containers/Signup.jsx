import React, { useState } from 'react';
import { Redirect } from 'react-router-dom';
import SignupScreen from '../components/Signup';
import { signup } from '../utils/Api';
import useForm from './UseForm';
import { validateUsername, validatePassword } from './FormValid';

const Signup = () => {
  const [error, setError] = useState('');
  const [response, setResponse] = useState(undefined);
  const [loading, setLoading] = useState(false);
  const {
    values,
    validate,
    changeUsername,
    changePassword,
  } = useForm(validateUsername, validatePassword);


  // Send data via API.
  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    const onSuccess = () => {
      setResponse(<Redirect to="/login" push />);
    };
    const onFailure = (err) => {
      setError(err.message);
    };

    const { username, password } = values;
    signup(username, password, onSuccess, onFailure);
  };

  return (
    response
    || (
      <SignupScreen
        values={values}
        error={error}
        loading={loading}
        validate={validate}
        handleSubmit={handleSubmit}
        changeUsername={changeUsername}
        changePassword={changePassword}
      />
    )
  );
};

export default Signup;
