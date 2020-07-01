import React from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

// eslint-disable-next-line import/no-named-as-default
import ActionButton from './ActionButton';
import { cardActionNames } from '../../utils/Constants';
import { ActionType } from '../../utils/ApiTypes';


const toButton = ({ type }) => (
  <ActionButton
    C={Dropdown.Item}
    key={type}
    type={type}
  />
);

const mapStateToProps = (state) => ({
  actions: state.Game.actions,
});

// Renders a dropdown view of the available actions
// related to development cards.
export const CardDropdown = ({ actions }) => {
  const cardActions = actions.filter(((x) => x && cardActionNames.includes(x.type)));

  return (
    <Dropdown>
      <Dropdown.Toggle disabled={!cardActions.length}>
      Development Cards
      </Dropdown.Toggle>

      <Dropdown.Menu>
        {cardActions.map(toButton)}
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default connect(mapStateToProps)(CardDropdown);


toButton.propTypes = {
  type: PropTypes.oneOf(cardActionNames).isRequired,
};

CardDropdown.propTypes = {
  actions: PropTypes.arrayOf(
    ActionType,
  ).isRequired,
};
