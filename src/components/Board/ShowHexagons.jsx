import PropTypes from 'prop-types';

import {
  colour, hexCenter, hexPath,
} from './BoardUtils';
import { HexagonType } from '../../utils/ApiTypes';


const showHexagons = (draw, hexagons) => {
  const showHexagon = (hexagon) => {
    const { position, terrain, token } = hexagon;
    const { level, index } = position;
    const { x, y } = hexCenter[level][index];

    draw.polygon(hexPath)
      .center(x, y)
      .rotate(90)
      .fill(colour[terrain]);

    draw.text(String(token))
      .center(x, y)
      .font({ size: 20 });
  };

  hexagons.forEach(showHexagon);
};

export default showHexagons;


showHexagons.propTypes = {
  draw: PropTypes.shape({
    type: PropTypes.string.isRequired,
  }).isRequired,
  hexagons: PropTypes.arrayOf(
    HexagonType,
  ).isRequired,
};
