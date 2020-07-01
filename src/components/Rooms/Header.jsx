import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import PropTypes from 'prop-types';


const Header = ({ id, name }) => (
  <Card.Header>
    <Accordion.Toggle
      as={Button}
      eventKey={id}
      variant="link"
    >
      {name}
    </Accordion.Toggle>
  </Card.Header>
);

export default Header;


Header.propTypes = {
  id: PropTypes.number.isRequired,
  name: PropTypes.string.isRequired,
};
