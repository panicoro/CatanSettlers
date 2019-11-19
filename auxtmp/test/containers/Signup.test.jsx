import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';

import { Redirect } from 'react-router-dom';
import Signup from '../../src/containers/Signup';
import { signup } from '../../src/utils/Api';
import useForm from '../../src/containers/UseForm';

jest.mock('../../src/utils/Api', () => ({
  signup: jest.fn(() => null),
}));

jest.mock('react-router-dom', () => ({
  Redirect: jest.fn(() => null),
}));

jest.mock('../../src/containers/UseForm', () => ({
  __esModule: true,
  default: jest.fn()
    .mockImplementation((validateUsername, validatePassword) => {
      validateUsername();
      validatePassword();
      return {
        changeUsername: (() => null),
        changePassword: (() => null),
        validate: (() => false),
        values: {
          username: '',
          password: '',
          usernameError: '',
          passwordError: '',
        },
      };
    }),
}));

const setError = jest.fn(() => null);
const dispatchs = [setError];
const mockFns = [signup, useForm, Redirect];

afterEach(() => {
  dispatchs.forEach((f) => f.mockClear());
  mockFns.forEach((f) => f.mockClear());
});

const mk = (rerender = render) => rerender(
  <Signup />,
);

test('render the form and signup fails', () => {
  const error = Error('error message');
  signup.mockImplementationOnce((username, password, onSuccess, onFailure) => {
    onFailure(error);
  });
  const {
    rerender, getByLabelText, getByTestId,
  } = mk();

  expect(useForm).toHaveBeenCalledTimes(1);
  expect(getByTestId('button')).toBeDisabled();

  // fill out the form
  fireEvent.change(getByLabelText(/username/i), { target: { value: 'test' } });
  fireEvent.change(getByLabelText(/password/i), { target: { value: 'test' } });
  useForm.mockReturnValueOnce({
    changeUsername: (() => null),
    changePassword: (() => null),
    validate: (() => true),
    values: {
      username: 'test',
      password: 'test',
      usernameError: '',
      passwordError: '',
    },
  });
  mk(rerender);

  expect(useForm).toHaveBeenCalledTimes(2);
  expect(getByTestId('button')).toBeEnabled();

  fireEvent.click(getByTestId('button'));
  expect(signup).toHaveBeenCalledTimes(1);
  expect(signup).toHaveBeenCalledWith('test', 'test', expect.any(Function), expect.any(Function));
  const alert = getByTestId('error');
  expect(alert).toHaveTextContent(/error message/i);
});

test('render the form and signup success', () => {
  signup.mockImplementationOnce((username, password, onSuccess) => {
    onSuccess();
  });
  const {
    rerender, getByLabelText, getByTestId,
  } = mk();

  expect(useForm).toHaveBeenCalledTimes(1);
  expect(getByTestId('button')).toBeDisabled();

  // fill out the form
  fireEvent.change(getByLabelText(/username/i), { target: { value: 'test' } });
  fireEvent.change(getByLabelText(/password/i), { target: { value: 'test' } });
  useForm.mockReturnValueOnce({
    changeUsername: (() => null),
    changePassword: (() => null),
    validate: (() => true),
    values: {
      username: 'test',
      password: 'test',
      usernameError: '',
      passwordError: '',
    },
  });
  mk(rerender);

  expect(useForm).toHaveBeenCalledTimes(2);
  expect(getByTestId('button')).toBeEnabled();

  fireEvent.click(getByTestId('button'));

  expect(signup).toHaveBeenCalledTimes(1);
  expect(signup).toHaveBeenCalledWith('test', 'test', expect.any(Function), expect.any(Function));
  expect(Redirect).toHaveBeenCalledTimes(1);
  expect(Redirect).toHaveBeenCalledWith({ to: '/login', push: true }, {});
});
