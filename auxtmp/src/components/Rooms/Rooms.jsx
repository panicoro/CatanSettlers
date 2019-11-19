import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import PropTypes from 'prop-types';

import { RoomType } from '../../utils/ApiTypes';
import Header from './Header';
// eslint-disable-next-line import/no-named-as-default
import Body from '../../containers/Rooms/Body';


const Rooms = ({ rooms, createRoom }) => (
  <div data-testid="rooms">
    <Button
      data-testid="rooms-button"
      onClick={createRoom}
    >
      Create
    </Button>

    <Accordion data-testid="rooms-accordion">
      {rooms.map(({
        // eslint-disable-next-line camelcase
        id, max_players, name, owner, players, game_has_started,
      }) => (
        <Card key={id} data-testid="rooms-card">
          <Header
            id={id}
            name={name}
          />
          <Body
            id={id}
            // eslint-disable-next-line camelcase
            maxPlayers={max_players}
            owner={owner}
            players={players}
            // eslint-disable-next-line camelcase
            gameHasStarted={game_has_started}
          />
        </Card>
      ))}
    </Accordion>
  </div>
);

export default Rooms;


Rooms.propTypes = {
  rooms: PropTypes.arrayOf(RoomType).isRequired,
  createRoom: PropTypes.func.isRequired,
};
