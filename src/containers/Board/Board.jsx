import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import SVG from 'svg.js';

import { dispatchDraw } from './Board.ducks';
import {
  WIDTH, HEIGHT,
} from '../../components/Board/BoardUtils';
import showHexagons from '../../components/Board/ShowHexagons';
import showRobber from '../../components/Board/ShowHCenter';
import showEdges from '../../components/Board/ShowEdges';
import showVertices from '../../components/Board/ShowVertices';
import {
  BuildingType, HexagonPosition, HexagonType, RoadType,
} from '../../utils/ApiTypes';


const mapStateToProps = (state) => ({
  cities: state.Game.board.cities,
  hexagons: state.Game.board.hexagons,
  roads: state.Game.board.roads,
  robber: state.Game.board.robber,
  settlements: state.Game.board.settlements,
  draw: state.Board.draw,
});

const mapDispatchToProps = ({
  setDraw: dispatchDraw,
});

// Show cities, roads or settlements for each player.
const showConstructions = (display, draw, constructions, type) => {
  constructions.forEach((x) => {
    display(draw, x.positions, x.colour, type);
  });
};

export const Board = (props) => {
  const {
    cities, hexagons, roads, robber, settlements,
  } = props;
  const { draw, setDraw } = props;

  // Set draw when component has mounted.
  // This must be done exactly one time.
  useEffect(() => {
    setDraw(SVG('board').size(WIDTH, HEIGHT));
  }, [setDraw]);

  useEffect(() => {
    if (draw) {
    // Clear current board.
      draw.clear();
      // Show hexagons and tokens.
      showHexagons(draw, hexagons);
      // Show robber.
      showRobber(draw, [robber]);
      // Show roads for each player.
      // Roads need to be drawn first, for aesthetic purposes.
      showConstructions(showEdges, draw, roads);
      // Show settlements for each player.
      showConstructions(showVertices, draw, settlements, 'settlement');
      // Show cities for each player.
      showConstructions(showVertices, draw, cities, 'city');
    }
  });

  return (<div id="board" />);
};

export default connect(mapStateToProps, mapDispatchToProps)(Board);


Board.propTypes = {
  cities: PropTypes.arrayOf(BuildingType).isRequired,
  draw: PropTypes.shape({
    clear: PropTypes.func.isRequired,
    type: PropTypes.string.isRequired,
  }),
  hexagons: PropTypes.arrayOf(HexagonType).isRequired,
  roads: PropTypes.arrayOf(RoadType).isRequired,
  robber: HexagonPosition.isRequired,
  settlements: PropTypes.arrayOf(BuildingType).isRequired,
  setDraw: PropTypes.func.isRequired,
};

Board.defaultProps = {
  draw: null,
};
