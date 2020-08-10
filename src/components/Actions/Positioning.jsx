import React from 'react';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import PropTypes from 'prop-types';
import Jumbotron from 'react-bootstrap/Jumbotron';

import '../General.css'


const Positioning = ({ message, onCancel, onConfirm }) => {
  const head = (
    <Row>
      <Col>
        <h3 data-testid="actions-positioning-head">
          {message}
        </h3>
      </Col>
    </Row>
  );

  const body = (
    <Row data-testid="actions-positioning-body">
      <Col>
        <Button
          disabled={!onConfirm}
          onClick={onConfirm}
          data-testid="actions-positioning-confirm"
          variant="danger"
        >
          Confirm
        </Button>
      </Col>
      <Col>
        <Button
          onClick={onCancel}
          data-testid="actions-positioning-cancel"
          variant="danger"
        >
          Cancel
        </Button>
      </Col>
    </Row>

  );

  return (
    <Jumbotron id='jumbo_actions'>
    <Container data-testid="actions-positioning">
      {head}
      {body}
    </Container>
    </Jumbotron>
  );
};

export default Positioning;


Positioning.propTypes = {
  onConfirm: PropTypes.func,
  onCancel: PropTypes.func.isRequired,
  message: PropTypes.string.isRequired,
};

Positioning.defaultProps = {
  onConfirm: null,
};
