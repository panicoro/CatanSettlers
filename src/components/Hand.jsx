import React from 'react';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Table from 'react-bootstrap/Table';
import PropTypes from 'prop-types';

import { cardNames, resourceNames } from '../utils/Constants';


const counter = (list, string) => {
  let count = 0;
  list.forEach((element) => {
    if (element === string) {
      count += 1;
    }
  });
  return count;
};

export const resToTable = (resources) => {
  const lumber = counter(resources, 'lumber');
  const wool = counter(resources, 'wool');
  const ore = counter(resources, 'ore');
  const grain = counter(resources, 'grain');
  const brick = counter(resources, 'brick');

  return (
    <tbody>
      <tr>
        <td>Lumber: </td>
        <td>{lumber}</td>
      </tr>
      <tr>
        <td>Wool: </td>
        <td>{wool}</td>
      </tr>
      <tr>
        <td>Ore: </td>
        <td>{ore}</td>
      </tr>
      <tr>
        <td>Grain: </td>
        <td>{grain}</td>
      </tr>
      <tr>
        <td>Brick: </td>
        <td>{brick}</td>
      </tr>
    </tbody>
  );
};

export const cardsToTable = (cards) => {
  const roadBuilding = counter(cards, 'road_building');
  const yearOfPlenty = counter(cards, 'year_of_plenty');
  const monopoly = counter(cards, 'monopoly');
  const victoryPoint = counter(cards, 'victory_point');
  const knight = counter(cards, 'knight');

  return (
    <tbody>
      <tr>
        <td>Road building: </td>
        <td>{roadBuilding}</td>
      </tr>
      <tr>
        <td>Year of plenty: </td>
        <td>{yearOfPlenty}</td>
      </tr>
      <tr>
        <td>Monopoly: </td>
        <td>{monopoly}</td>
      </tr>
      <tr>
        <td>Victory point: </td>
        <td>{victoryPoint}</td>
      </tr>
      <tr>
        <td>Knight: </td>
        <td>{knight}</td>
      </tr>
    </tbody>
  );
};


const Hand = ({ cards, resources }) => (
  <Container>
    <Row>
      <Col>
        <h1>Resources</h1>
        <Table borderless size="sm">
          {resToTable(resources)}
        </Table>
      </Col>
      <Col>
        <h1>Cards</h1>
        <Table borderless size="sm">
          {cardsToTable(cards)}
        </Table>
      </Col>

    </Row>
  </Container>
);

export default Hand;


Hand.propTypes = {
  cards: PropTypes.arrayOf(PropTypes.oneOf(cardNames)).isRequired,
  resources: PropTypes.arrayOf(PropTypes.oneOf(resourceNames)).isRequired,
};
