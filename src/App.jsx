import React from 'react';

// eslint-disable-next-line import/no-named-as-default
import NavBar from './containers/NavBar';
// eslint-disable-next-line import/no-named-as-default
import Routes from './containers/Routes';

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';


const App = () => (
  <div className="App">
    <NavBar />
    <Routes />
  </div>
);


export default (App);
