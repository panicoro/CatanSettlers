import React from 'react';
import {Switch, Route} from 'react-router-dom';
import Lobby_container from "../containers/Lobby";
import ListLobby_container from "../containers/ListLobby";
import NotFound from "./NotFound";
import CreateLobby_container from "../containers/CreateLobby";
import Login_container from "../containers/Login";
import NavBar_container from "../containers/NavBar";
import Register_container from "../containers/Register";
import Game_container from "../containers/Game";
import Home from "./Home";
import ErrorMsg_container from "../containers/ErrorMsg";
import {PATHS} from "../constants";
import Logout_container from "../containers/Logout";


function App() {
  return (
    <div className="App">
      <header className="App-header bg-light-yellow">
        <NavBar_container/>
      </header>
      <main>
        <Route component={ErrorMsg_container}/>
        <Switch>
          <Route exact path={PATHS.home} component={Home}/>
          <Route path={PATHS.createRoom} component={CreateLobby_container}/>
          <Route path={PATHS.genericRoom} render={(props) => <Lobby_container {...props} id={parseInt(props.match.params.id)}/>}/>
          <Route exact path={PATHS.allRooms} component={ListLobby_container}/>
          <Route path={PATHS.login} component={Login_container}/>
          <Route path={PATHS.logout} component={Logout_container}/>
          <Route path={PATHS.register} component={Register_container}/>
          <Route path={PATHS.genericGame} render={(props) => <Game_container {...props} id={parseInt(props.match.params.id)}/>}/>
          <Route component={NotFound}/>
        </Switch>
      </main>
    </div>
  );
}

export default App;