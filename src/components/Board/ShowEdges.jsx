import PropTypes from 'prop-types';

import { roadStroke, vertexCenter } from './BoardUtils';
import { RoadPosition } from '../../utils/ApiTypes';


const showEdges = (draw, ps, colour, onClickMaker = () => null) => {
  const drawEdge = ([p0, p1]) => {
    const { level: level0, index: index0 } = p0;
    const { level: level1, index: index1 } = p1;

    const { x: x0, y: y0 } = vertexCenter[level0][index0];
    const { x: x1, y: y1 } = vertexCenter[level1][index1];

    draw.line(x0, y0, x1, y1)
      .stroke(roadStroke(colour))
      .click(onClickMaker([p0, p1]));
  };

  ps.forEach(drawEdge);
};

export default showEdges;


showEdges.proptypes = {
  draw: PropTypes.shape({
    type: PropTypes.string.isRequired,
  }),
  colour: PropTypes.string.isRequired,
  ps: PropTypes.arrayOf(RoadPosition).isRequired,
  onClickMaker: PropTypes.func,
};
