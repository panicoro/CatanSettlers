import React, { useState } from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';
import PropTypes from 'prop-types';

import { resourceNames } from '../../utils/Constants';
import counter from '../../utils/Counter';
import {
  dispatchError,
  dispatchWaiting,
} from './Actions.ducks';
import {
  setRunning as dispatchGameRunning,
  setState as dispatchGameState,
} from '../Game/Game.ducks';
import BankTradeScreen from '../../components/Actions/BankTrade';
import { bankTrade, getGameStatus } from '../../utils/Api';

const mapStateToProps = (state) => ({
  resources: state.Game.hand.resources,
});

const mapDispatchToProps = ({
  setError: dispatchError,
  setWaiting: dispatchWaiting,
  setGameRunning: dispatchGameRunning,
  setGameState: dispatchGameState,
});

export const BankTrade = (props) => {
  const { resources } = props;
  const { setError, setWaiting } = props;
  const { setGameRunning, setGameState } = props;
  const { id } = useParams();
  const [offer, setOffer] = useState('');
  const [request, setRequest] = useState('');

  const refresh = () => {
    setWaiting();
    setGameRunning();
    getGameStatus(id, setGameState, setError);
  };

  const trade = () => {
    bankTrade(id, offer, request, refresh, setError);
  };

  const disabled = offer === '' || request === '' || offer === request;
  const available = resourceNames.filter((r) => counter(resources, r) >= 4);

  return (
    <BankTradeScreen
      setOffer={setOffer}
      setRequest={setRequest}
      trade={trade}
      offer={offer}
      request={request}
      cancel={refresh}
      resources={available}
      disabled={disabled}
    />
  );
};

export default connect(mapStateToProps, mapDispatchToProps)(BankTrade);


BankTrade.propTypes = {
  setError: PropTypes.func.isRequired,
  setWaiting: PropTypes.func.isRequired,
  setGameRunning: PropTypes.func.isRequired,
  setGameState: PropTypes.func.isRequired,
  resources: PropTypes.arrayOf(PropTypes.string).isRequired,
};
