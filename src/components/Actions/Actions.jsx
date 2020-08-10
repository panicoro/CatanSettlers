import React from 'react';
import Table from 'react-bootstrap/Table';
import PropTypes from 'prop-types';

/* eslint-disable import/no-named-as-default */
import ActionButton from '../../containers/Actions/ActionButton';
import CardDropdown from '../../containers/Actions/CardDropdown';
/* eslint-enable import/no-named-as-default */


const toButton = (type) => (
  <td key={type}>
    <ActionButton type={type} />
  </td>
);

const firstRow = [
  'build_settlement',
  'build_road',
  'upgrade_city',
];

const secondRow = [
  'bank_trade',
  'transaction',
  'end_turn',
];

export const Actions = () => (
  <>
    <h1>Actions</h1>
    <Table borderless size="sm">
      <tbody>
        <tr>
          {firstRow.map(toButton)}
        </tr>
        <tr>
          {secondRow.map(toButton)}
        </tr>
      </tbody>
    </Table>
    <CardDropdown />
  </>
);

export default Actions;


toButton.propTypes = PropTypes.string.isRequired;
