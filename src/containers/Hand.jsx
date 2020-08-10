import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import HandScreen from '../components/Hand';


const mapStateToProps = (state) => ({
  cards: state.Game.hand.cards,
  resources: state.Game.hand.resources,
});

export const Hand = ({ cards, resources }) => (
  <HandScreen
    cards={cards}
    resources={resources}
  />
);

export default connect(mapStateToProps)(Hand);


Hand.propTypes = {
  cards: PropTypes.arrayOf(PropTypes.string).isRequired,
  resources: PropTypes.arrayOf(PropTypes.string).isRequired,
};
