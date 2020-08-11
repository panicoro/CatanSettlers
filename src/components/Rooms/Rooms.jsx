import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Button from 'react-bootstrap/Button';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Card from 'react-bootstrap/Card';
import PropTypes from 'prop-types';
import { RoomType } from '../../utils/ApiTypes';
import Header from './Header';
// eslint-disable-next-line import/no-named-as-default
import Body from '../../containers/Rooms/Body';
import './Room.css'

const Rooms = ({ rooms, createRoom }) => {
  
  return (
  
  <div data-testid="rooms" className="row">
    <div className="col-md-6">
      <Jumbotron id='create-room'>
      <h3>Create a new room</h3>
        <div >
          <Button
            data-testid="rooms-button"
            onClick={createRoom}
            variant="dark"
          >
            Create
          </Button>
        </div>
      </Jumbotron>
    </div>    

    <div className="col-md-6">
    <Jumbotron id='list-rooms'>
      <h3>Join or Enter to a room</h3>
      <Accordion data-testid="rooms-accordion">
        {rooms.map(({
          // eslint-disable-next-line camelcase
          id, max_players, name, owner, players, game_has_started,
        }) => (
          <Card key={id} data-testid="rooms-card" id='accordion'>
            <Header
              id={id}
              name={name}
              variant="dark"
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
    </Jumbotron>
    </div>
  </div>
);
}
export default Rooms;


Rooms.propTypes = {
  rooms: PropTypes.arrayOf(RoomType).isRequired,
  createRoom: PropTypes.func.isRequired,
};
