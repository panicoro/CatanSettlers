import React, { useState } from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';

import Error from '../../components/Error';
import RoomBody from '../../components/Rooms/Body';
import { joinRoom } from '../../utils/Api';


export const mapStateToProps = (state, ownProps) => ({
  username: state.Auth.username,
  ...ownProps,
});

export const Body = (props) => {
  const {
    id, owner, players, maxPlayers, gameHasStarted,
  } = props;
  const { username } = props;

  const [stage, setStage] = useState('running');
  const [loading, setLoading] = useState(false);

  const joined = players.includes(username);
  const full = players.length >= maxPlayers;

  const redir = () => { setStage('redirect'); };
  const join = () => {
    setLoading(true);
    joinRoom(id, redir, () => { setStage('error'); });
  };

  let onClick;
  if (joined) onClick = redir;
  else if (!gameHasStarted && !full) onClick = join;
  else onClick = null;

  if (stage === 'running') {
    return (
      <RoomBody
        id={id}
        disabled={loading}
        maxPlayers={maxPlayers}
        onClick={onClick}
        owner={owner}
        players={players.join(', ')}
        gameStarted={gameHasStarted ? 'Game Started' : 'Waiting to start'}
        label={joined ? 'Enter' : 'Join'}
      />
    );
  }

  if (stage === 'redirect') return (<Redirect to={`/waiting/${id}`} push />);

  return (<Error />);
};

export default connect(mapStateToProps)(Body);


Body.propTypes = {
  id: PropTypes.number.isRequired,
  maxPlayers: PropTypes.number.isRequired,
  owner: PropTypes.string.isRequired,
  players: PropTypes.arrayOf(PropTypes.string).isRequired,
  username: PropTypes.string,
  gameHasStarted: PropTypes.bool.isRequired,
};

Body.defaultProps = {
  username: '',
};
