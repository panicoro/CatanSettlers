import React from 'react';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import PropTypes from 'prop-types';


const Positioning = ({ message, onCancel, onConfirm }) => {
  const head = (
    <Row>
      <Col>
        <h1 data-testid="actions-positioning-head">
          {message}
        </h1>
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
        >
          Confirm
        </Button>
      </Col>
      <Col>
        <Button
          onClick={onCancel}
          data-testid="actions-positioning-cancel"
        >
          Cancel
        </Button>
      </Col>
    </Row>

  );

  return (
    <Container data-testid="actions-positioning">
      {head}
      {body}
    </Container>
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
