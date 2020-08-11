import React from 'react';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

/* eslint-disable import/no-named-as-default */
import Actions from '../../containers/Actions/Actions';
import Board from '../../containers/Board/Board';
import Hand from '../../containers/Hand';
import Info from '../../containers/Info/Info';
import Background from '../../images/background_game.jpg';
/* eslint-enable import/no-named-as-default */


const GameScreen = () => {  
  // Modify the DOM Styles with JavaScript
  document.body.style.backgroundImage = `url(${Background})`
  document.body.style.backgroundSize = 'cover';
  document.body.style.backgroundRepeat = 'no-repeat';

  return (
  <Container>
    <Row>
      <Col xs={2}>
        <Actions />
        <Hand />
      </Col>
      <Col xs={8}>
        <Board />
      </Col>
      <Col xs={2}>
        <Info />
      </Col>
    </Row>
  </Container>
);
}
export default GameScreen;
