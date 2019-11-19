import PropTypes from 'prop-types';

import { resourceNames } from './Constants';


/* Game */

export const HexagonPosition = PropTypes.shape({
  level: PropTypes.number.isRequired,
  index: PropTypes.number.isRequired,
});

export const BuildingPosition = HexagonPosition;

export const RoadPosition = PropTypes.arrayOf(
  BuildingPosition,
);

export const HexagonType = PropTypes.shape({
  position: HexagonPosition.isRequired,
  terrain: PropTypes.oneOf(resourceNames.concat(['desert'])).isRequired,
  token: PropTypes.number.isRequired,
});

export const BuildingType = PropTypes.shape({
  colour: PropTypes.string.isRequired,
  positions: PropTypes.arrayOf(BuildingPosition).isRequired,
});

export const RoadType = PropTypes.shape({
  colour: PropTypes.string.isRequired,
  positions: PropTypes.arrayOf(RoadPosition).isRequired,
});

export const ActionType = PropTypes.oneOfType([
  PropTypes.shape({
    type: PropTypes.string.isRequired,
    payload:
      PropTypes.arrayOf(
        PropTypes.oneOfType([
          BuildingPosition,
          PropTypes.arrayOf(
            BuildingPosition,
          ),
        ]),
      ),
  }).isRequired,
  PropTypes.shape({
    type: PropTypes.string.isRequired,
  }),
]);

export const BoardType = PropTypes.shape({
  cities: PropTypes.arrayOf(BuildingType).isRequired,
  hexagons: PropTypes.arrayOf(PropTypes.shape({
    level: PropTypes.number.isRequired,
    index: PropTypes.number.isRequired,
  })).isRequired,
  robber: HexagonPosition.isRequired,
  settlements: PropTypes.arrayOf(BuildingType).isRequired,
});

export const HandType = PropTypes.shape({
  resources: PropTypes.arrayOf(PropTypes.oneOf(resourceNames)).isRequired,
  cards: PropTypes.arrayOf(PropTypes.string).isRequired,
});

export const InfoType = PropTypes.shape({
  players: PropTypes.arrayOf(PropTypes.shape({})).isRequired,
  currentTurn: PropTypes.shape({}).isRequired,
  winner: PropTypes.string,
}).isRequired;

export const GameStateType = PropTypes.shape({
  actions: PropTypes.arrayOf(ActionType),
  board: BoardType,
  hand: HandType,
  info: InfoType,
  stage: PropTypes.string,
});

export const PlayerType = PropTypes.shape({
  username: PropTypes.string,
  colour: PropTypes.string,
});


/* Rooms */

export const RoomType = PropTypes.shape({
  id: PropTypes.number.isRequired,
  name: PropTypes.string.isRequired,
  owner: PropTypes.string.isRequired,
  players: PropTypes.arrayOf(PropTypes.string).isRequired,
  max_players: PropTypes.number.isRequired,
  game_has_started: PropTypes.bool.isRequired,
  game_id: PropTypes.number,
});

export const RoomsStateType = PropTypes.shape({
  stage: PropTypes.string.isRequired,
  refresh: PropTypes.func.isRequired,
  rooms: PropTypes.arrayOf(RoomType).isRequired,
});


/* Boards */

export const BoardListType = PropTypes.shape({
  id: PropTypes.number.isRequired,
  name: PropTypes.string.isRequired,
});
