import React from 'react';
import Button from 'react-bootstrap/Button';
import FormControl from 'react-bootstrap/FormControl';
import FormGroup from 'react-bootstrap/FormGroup';
import FormLabel from 'react-bootstrap/FormLabel';
import PropTypes from 'prop-types';

import Error from './Error';


const Signup = (props) => {
  const {
    values, error, validate, loading,
    handleSubmit, changeUsername, changePassword,
  } = props;
  const {
    username, password, usernameError, passwordError,
  } = values;

  const userForm = (
    <FormGroup bssize="large">
      <FormLabel htmlFor="username">
        Username
      </FormLabel>
      <FormControl
        autoFocus
        id="username"
        name="username"
        isInvalid={!!usernameError}
        onChange={changeUsername}
        type="text"
        value={username}
      />
      <FormControl.Feedback type="invalid">
        {usernameError}
      </FormControl.Feedback>
    </FormGroup>
  );

  const passForm = (
    <FormGroup bssize="large">
      <FormLabel htmlFor="password">
        Password
      </FormLabel>
      <FormControl
        id="password"
        name="password"
        isInvalid={!!passwordError}
        onChange={changePassword}
        type="password"
        value={password}
      />
      <FormControl.Feedback type="invalid">
        {passwordError}
      </FormControl.Feedback>
    </FormGroup>
  );

  const button = (
    <Button
      block
      bssize="large"
      disabled={!validate()}
      data-testid="button"
      type="submit"
    >
      {loading ? 'Loading...' : 'Signup'}
    </Button>
  );

  return (
    <div className="Forms">
      <h1>Signup</h1>
      {error && <Error message={error} />}
      <form
        onSubmit={handleSubmit}
        data-testid="signup-form"
      >
        {userForm}
        {passForm}
        {button}
      </form>
    </div>
  );
};

export default Signup;


Signup.propTypes = {
  values: PropTypes.shape({
    username: PropTypes.string.isRequired,
    password: PropTypes.string.isRequired,
    usernameError: PropTypes.string.isRequired,
    passwordError: PropTypes.string.isRequired,
  }).isRequired,
  loading: PropTypes.bool.isRequired,
  error: PropTypes.string.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  changeUsername: PropTypes.func.isRequired,
  changePassword: PropTypes.func.isRequired,
  validate: PropTypes.func.isRequired,
};
