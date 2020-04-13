import React from 'react';
import {
  render, fireEvent,
} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';

import Roads from '../../src/components/Actions/Positioning';


const onCancel = jest.fn(() => null);
const onConfirm = jest.fn(() => null);

const mk = (message) => render(
  <Roads
    message={message}
    onCancel={onCancel}
    onConfirm={onConfirm}
  />,
);

afterEach(() => {
  onCancel.mockClear();
  onConfirm.mockClear();
});

test('shows a head and a body with a message and two buttons', () => {
  const { queryAllByTestId, queryByTestId } = mk('message');

  [queryAllByTestId('actions-positioning'),
    queryAllByTestId('actions-positioning-head'),
    queryAllByTestId('actions-positioning-body'),
    queryAllByTestId('actions-positioning-cancel'),
    queryAllByTestId('actions-positioning-confirm'),
  ].forEach((r) => expect(r).toHaveLength(1));

  const head = queryByTestId('actions-positioning-head');
  const bCancel = queryByTestId('actions-positioning-cancel');
  const bConfirm = queryByTestId('actions-positioning-confirm');

  [queryByTestId('actions-positioning'),
    queryByTestId('actions-positioning-body'),
    head,
    bCancel,
    bConfirm,
  ].forEach((r) => expect(r).not.toBeEmpty());

  expect(head.textContent).toBe('message');
  expect(bCancel).toBeEnabled();
  expect(bConfirm).toBeEnabled();
});

test('calls onCancel', () => {
  const { queryByTestId } = mk();

  const b = queryByTestId('actions-positioning-cancel');

  expect(onCancel).not.toHaveBeenCalled();
  expect(onConfirm).not.toHaveBeenCalled();

  fireEvent.click(b);

  expect(onCancel).toHaveBeenCalledTimes(1);
  expect(onConfirm).not.toHaveBeenCalled();
});

test('calls onCofirm', () => {
  const { queryByTestId } = mk();

  const b = queryByTestId('actions-positioning-confirm');

  expect(onCancel).not.toHaveBeenCalled();
  expect(onConfirm).not.toHaveBeenCalled();

  fireEvent.click(b);

  expect(onConfirm).toHaveBeenCalledTimes(1);
  expect(onCancel).not.toHaveBeenCalled();
});
