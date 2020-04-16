import React from 'react';
import PropTypes from 'prop-types';

import Button from 'react-bootstrap/Button';
import Table from 'react-bootstrap/Table';
import { RoomType } from '../../utils/ApiTypes';


export const Waiting = ({
  room, onStart, onCancel, loading,
}) => {
  const {
    // eslint-disable-next-line camelcase
    max_players, name, owner, players,
  } = room;

  const head = (
    <thead>
      <tr>
        <th colSpan="2">{name}</th>
      </tr>
    </thead>
  );

  const body = (
    <tbody>
      <tr>
        <td>{`Owner: ${owner}`}</td>
      </tr>
      <tr>
        <td>{`Players: ${players.join(', ')}`}</td>
      </tr>
      <tr>
        {/* eslint-disable-next-line camelcase */}
        <td>{`Max players: ${max_players}`}</td>
      </tr>
    </tbody>
  );

  const roomIsFull = room.players.length === room.max_players;

  const buttons = (
    <div data-testid="waiting-buttons">
      <Button
        data-testid="start-button"
        disabled={!onStart || !roomIsFull || loading}
        onClick={onStart}
        className="start"
      >
        {loading ? 'Loading...' : 'Start game'}
      </Button>
      <Button
        data-testid="cancel-button"
        disabled={!onCancel || loading}
        onClick={onCancel}
        className="cancel"
      >
        Cancel Room
      </Button>
    </div>
  );

  return (
    <div data-testid="waiting-running">
      <Table borderless size="sm">
        {head}
        {body}
      </Table>
      {onStart ? buttons : null}
    </div>
  );
};

export default Waiting;

Waiting.propTypes = {
  room: RoomType.isRequired,
  onStart: PropTypes.func,
  onCancel: PropTypes.func,
  loading: PropTypes.bool.isRequired,
};

Waiting.defaultProps = {
  onStart: null,
  onCancel: null,
};
