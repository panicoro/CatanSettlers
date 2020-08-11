import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';

import { Login, mapDispatchToProps } from '../../src/containers/Login';
import {
  setAuth as dispatchAuth,
  setUser as dispatchUser,
} from '../../src/containers/Auth.ducks';
import { login } from '../../src/utils/Api';
import useForm from '../../src/containers/UseForm';


jest.mock('../../src/utils/Api', () => ({
  login: jest.fn(() => null),
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
const setLoading = jest.fn(() => null);
const setAuth = jest.fn(() => null);
const setUser = jest.fn(() => null);

const dispatchs = [setError, setLoading, setAuth, setUser];
const mockFns = [login, useForm];

afterEach(() => {
  dispatchs.forEach((f) => f.mockClear());
  mockFns.forEach((f) => f.mockClear());
});


const mk = (rerender = render) => rerender(
  <Login
    setAuth={setAuth}
    setUser={setUser}
  />,
);

test('returns all dispatch functions', () => {
  const expected = {
    setAuth: dispatchAuth,
    setUser: dispatchUser,
  };
  expect(mapDispatchToProps).toEqual(expected);
});

test('render and the form is load', () => {
  const { queryAllByTestId, queryByTestId } = mk();

  expect(queryAllByTestId('login-form')).toHaveLength(1);
  const form = queryByTestId('login-form');
  const b = queryByTestId('button');

  expect(form).not.toBeEmpty();
  expect(b).toBeDisabled();
  expect(useForm).toHaveBeenCalledTimes(1);
});

test('render the form and login fails', () => {
  const {
    rerender, getByLabelText, getByTestId,
  } = mk();

  expect(useForm).toHaveBeenCalledTimes(1);
  expect(getByTestId('button')).toBeDisabled();

  // fill out the form
  fireEvent.change(getByLabelText(/username/i), { target: { value: 'test' } });
  useForm.mockReturnValueOnce({
    changeUsername: (() => null),
    changePassword: (() => null),
    validate: (() => false),
    values: {
      username: 'test',
      password: '',
      usernameError: '',
      passwordError: '',
    },
  });
  mk(rerender);

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

  expect(useForm).toHaveBeenCalledTimes(3);
  expect(getByTestId('button')).toBeEnabled();

  fireEvent.click(getByTestId('button'));
  expect(login).toHaveBeenCalledTimes(1);
  expect(login).toHaveBeenCalledWith('test', 'test', expect.any(Function), expect.any(Function));
  expect(localStorage.getItem('token')).toEqual(null);
  expect(localStorage.getItem('username')).toEqual(null);
});

test('render the form and login success', () => {
  const response = { token: 'token' };
  login.mockImplementationOnce((username, password, onSuccess) => {
    onSuccess(response);
    expect(setAuth).toHaveBeenCalledTimes(1);
    expect(setAuth).toHaveBeenCalledWith(true);
    expect(setUser).toHaveBeenCalledTimes(1);
    expect(setUser).toHaveBeenCalledWith(username);
  });
  const {
    rerender, getByLabelText, getByTestId,
  } = mk();

  expect(useForm).toHaveBeenCalledTimes(1);
  expect(getByTestId('button')).toBeDisabled();

  // fill out the form
  fireEvent.change(getByLabelText(/username/i), { target: { value: 'test' } });
  useForm.mockReturnValueOnce({
    changeUsername: (() => null),
    changePassword: (() => null),
    validate: (() => false),
    values: {
      username: 'test',
      password: '',
      usernameError: '',
      passwordError: '',
    },
  });
  mk(rerender);

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

  expect(useForm).toHaveBeenCalledTimes(3);
  expect(getByTestId('button')).toBeEnabled();

  fireEvent.click(getByTestId('button'));
  expect(login).toHaveBeenCalledTimes(1);
  expect(login).toHaveBeenCalledWith('test', 'test', expect.any(Function), expect.any(Function));
  expect(JSON.parse(localStorage.getItem('token'))).toEqual('token');
  expect(localStorage.getItem('username')).toEqual('test');
});
