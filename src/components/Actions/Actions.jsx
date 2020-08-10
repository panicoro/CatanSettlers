import React from 'react';
import Table from 'react-bootstrap/Table';
import PropTypes from 'prop-types';

/* eslint-disable import/no-named-as-default */
import ActionButton from '../../containers/Actions/ActionButton';
import CardDropdown from '../../containers/Actions/CardDropdown';
import Jumbotron from 'react-bootstrap/Jumbotron';
/* eslint-enable import/no-named-as-default */

import '../General.css'

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
  <Jumbotron id='jumbo_actions'>
    <h3>Actions</h3>
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
  </Jumbotron>
);

export default Actions;


toButton.propTypes = PropTypes.string.isRequired;
