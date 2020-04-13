import { hexCenter, robberShape, robberSize } from './BoardUtils';
import { colours } from '../../utils/Constants';


const showHCenter = (draw, ps, colour = colours.Robber, onClickMaker = () => null) => {
  const drawPosition = ({ level, index }) => {
    const { x, y } = hexCenter[level][index];
    draw[robberShape](robberSize)
      .center(x, y)
      .fill(colour)
      .click(onClickMaker({ level, index }));
  };

  ps.forEach(drawPosition);
};

export default showHCenter;
