import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';
import PropTypes from 'prop-types';


// Details of a room. If onClick is null,
// no button is shown.
const Body = (props) => {
  const {
    id, maxPlayers, owner, players, gameStarted,
  } = props;
  const { label, disabled, onClick } = props;

  const button = (
    <Button
      onClick={onClick}
      data-testid="room-body-button"
      disabled={disabled}
    >
      {label}
    </Button>
  );

  return (
    <Accordion.Collapse eventKey={id} data-testid="room-body">
      <Card.Body>
        <Table borderless size="sm">
          <tbody>
            <tr>
              <td>{`Owner: ${owner}`}</td>
            </tr>
            <tr>
              <td>{`Players: ${players}`}</td>
            </tr>
            <tr>
              <td>{`Max players: ${maxPlayers}`}</td>
            </tr>
            <tr>
              <td>{gameStarted}</td>
            </tr>
          </tbody>
        </Table>
        { onClick && button }
      </Card.Body>
    </Accordion.Collapse>
  );
};

export default Body;


Body.propTypes = {
  id: PropTypes.number.isRequired,
  disabled: PropTypes.bool.isRequired,
  gameStarted: PropTypes.string.isRequired,
  maxPlayers: PropTypes.number.isRequired,
  onClick: PropTypes.func,
  owner: PropTypes.string.isRequired,
  players: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
};

Body.defaultProps = {
  onClick: null,
};
