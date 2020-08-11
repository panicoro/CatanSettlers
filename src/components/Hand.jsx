import React from 'react';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Table from 'react-bootstrap/Table';
import PropTypes from 'prop-types';

import { cardNames, resourceNames } from '../utils/Constants';

import './General.css'
import lumber_icon from '../images/lumber_icon.png';
import wool_icon from '../images/wool_icon.png';
import grain_icon from '../images/grain_icon.png';
import ore_icon from '../images/ore_icon.png';
import brick_icon from '../images/brick_icon.png';


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
        <img
          alt=""
          src={lumber_icon}
          width="35"
          height="35"
          className="d-inline-block align-top"
        />
        <td>Lumber: </td>
        <td>{lumber}</td>
      </tr>
      <tr>
        <img
          alt=""
          src={wool_icon}
          width="35"
          height="35"
          className="d-inline-block align-top"
        />
        <td>Wool: </td>
        <td>{wool}</td>
      </tr>
      <tr>
      <img
          alt=""
          src={ore_icon}
          width="35"
          height="35"
          className="d-inline-block align-top"
        />
        <td>Ore: </td>
        <td>{ore}</td>
      </tr>
      <tr>
        <img
          alt=""
          src={grain_icon}
          width="35"
          height="35"
          className="d-inline-block align-top"
        />
        <td>Grain: </td>
        <td>{grain}</td>
      </tr>
      <tr>
      <img
          alt=""
          src={brick_icon}
          width="35"
          height="35"
          className="d-inline-block align-top"
        />
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
        <Jumbotron id='jumbo_info'>
        <h3>Resources</h3>
        <Table borderless size="sm">
          {resToTable(resources)}
        </Table>
        </Jumbotron>
      </Col>
      <Col>
      <Jumbotron id='jumbo_info'>
        <h3>Cards</h3>
        <Table borderless size="sm">
          {cardsToTable(cards)}
        </Table>
      </Jumbotron>
      </Col>
    </Row>
  </Container>
);

export default Hand;


Hand.propTypes = {
  cards: PropTypes.arrayOf(PropTypes.oneOf(cardNames)).isRequired,
  resources: PropTypes.arrayOf(PropTypes.oneOf(resourceNames)).isRequired,
};
