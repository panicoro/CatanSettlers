import { buyCard, endTurn } from '../../utils/Api';


// Returns an onClickMaker function for actions.
export const actionOnClick = (id, eventHandlers) => ((type) => {
  const {
    refresh, setError, setRobbing, setBuying, set2Roads,
    setBuildingCity, setBuildingRoad, setBuildingSettlement,
  } = eventHandlers;
  const { setGameFrozen } = eventHandlers;

  switch (type) {
    case 'build_settlement':
      return () => {
        setGameFrozen();
        setBuildingSettlement();
      };

    case 'build_road':
      return () => {
        setGameFrozen();
        setBuildingRoad();
      };

    case 'upgrade_city':
      return () => {
        setGameFrozen();
        setBuildingCity();
      };

    case 'bank_trade':
      return () => { setBuying(); };

    case 'buy_card':
      return () => { buyCard(id, refresh, setError); };

    case 'play_knight_card':
      return () => {
        setGameFrozen();
        setRobbing();
      };

    case 'end_turn':
      return () => { endTurn(id, refresh, setError); };

    case 'move_robber':
      return () => {
        setGameFrozen();
        setRobbing();
      };

    case 'play_road_building_card':
      return () => {
        setGameFrozen();
        set2Roads();
      };

    default:
      return setError;
  }
}
);

export default actionOnClick;
