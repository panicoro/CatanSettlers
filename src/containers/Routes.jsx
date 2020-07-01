import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route } from 'react-router-dom';
import PropTypes from 'prop-types';

/* eslint-disable import/no-named-as-default */
import CreateRoom from './Rooms/CreateRoom';
import Game from './Game/Game';
import Login from './Login';
import Rooms from './Rooms/Rooms';
import Signup from './Signup';
import Waiting from './Rooms/Waiting';
/* eslint-enable import/no-named-as-default */

import ConditionalRoute from '../components/ConditionalRoute';
import Landing from '../components/Landing';
import Error from '../components/Error';


const mapStateToProps = (state) => ({
  auth: state.Auth.auth,
});

// Given a condition and a redirection url,
// converts a component (and its path) into a
// conditional route.
const toCondRoute = (condition, redir) => (({ component, path }) => (
  <ConditionalRoute
    component={component}
    condition={condition}
    key={path}
    exact
    path={path}
    redir={redir}
  />
));

export const Routes = ({ auth }) => (
  <Switch>
    {/* Only if authenticated. */}
    {[{ auth, path: '/rooms', component: Rooms },
      { auth, path: '/create', component: CreateRoom },
      { auth, path: '/waiting/:id', component: Waiting },
      { auth, path: '/game/:id', component: Game },
    ].map(toCondRoute(auth, '/'))}

    {/* Only if not authenticated. */}
    {[{ path: '/', component: Landing },
      { path: '/login', component: Login },
      { path: '/signup', component: Signup },
    ].map(toCondRoute(!auth, '/rooms'))}

    {/* Default. */}
    <Route>
      <Error message="Page not found" />
    </Route>
  </Switch>
);

export default connect(mapStateToProps)(Routes);


toCondRoute.propTypes = {
  condition: PropTypes.bool.isRequired,
  redir: PropTypes.string.isRequired,
};

Routes.propTypes = {
  auth: PropTypes.bool.isRequired,
};
