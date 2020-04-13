import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';


// Renders C if user is authenticated.
// Otherwise, redirects to path.
const ConditionalRoute = ({
  component: C, condition, redir, ...rest
}) => (
  <Route
    // eslint-disable-next-line react/jsx-props-no-spreading
    {...rest}
    render={(props) => (
      condition
      // eslint-disable-next-line react/jsx-props-no-spreading
        ? <C {...props} />
        : <Redirect to={redir} push />
    )}
  />
);

export default ConditionalRoute;


ConditionalRoute.propTypes = {
  component: PropTypes.elementType.isRequired,
  condition: PropTypes.bool.isRequired,
  redir: PropTypes.string.isRequired,
};
