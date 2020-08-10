import { useState } from 'react';

const initialState = {
  username: '',
  password: '',
  usernameError: '',
  passwordError: '',
};
const useForm = (validateUsername, validatePassword) => {
  const [values, setValues] = useState(initialState);
  const [usernameValid, setUsernameValid] = useState(false);
  const [passwordValid, setPasswordValid] = useState(false);

  // Handles Username changes.
  const changeUsername = (e) => {
    const username = e.target.value;

    // Validation
    const error = validateUsername(username);

    setValues({
      ...values,
      username,
      usernameError: error,
    });
    setUsernameValid(error === '');
  };

  // Handles Username changes.
  const changePassword = (e) => {
    const password = e.target.value;

    // Validation
    const error = validatePassword(password);

    setValues({
      ...values,
      password,
      passwordError: error,
    });
    setPasswordValid(error === '');
  };

  const validate = () => (usernameValid && passwordValid);

  return {
    changeUsername,
    changePassword,
    validate,
    values,
  };
};

export default useForm;
