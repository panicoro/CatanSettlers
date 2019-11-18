import React from 'react';
import axios from 'axios'
import {Redirect} from 'react-router-dom'
import {isNull, PATHS, REFRESH_RATE_ROOMS, API, ERRORS, CODES} from "../constants";
import Loading from "./Loading";

class PostList extends React.Component {
  constructor(props){
    super(props);
    this.joinGame = this.joinGame.bind(this);
    this.createRoom = this.createRoom.bind(this);
    this.alreadyjoined = this.alreadyjoined.bind(this);

    this.state = {
      interval: null
    }
  }

  joinGame(idRoom,player) {
    console.log("JOINGAME")
    console.log('http://localhost:8000'+API.room(idRoom))
    axios.put('http://localhost:8000'+API.room(idRoom))
        .then(res => {
          console.log(res)
          this.props.addPlayer(idRoom,player);
          this.props.history.push(PATHS.room(idRoom))
        })
        .catch(error => {
          console.log(error.response)
          if (CODES.clientError(error.response.status)) {
            this.props.setError(ERRORS.roomTooLate, PATHS.allRooms);
          } else {
            this.props.setError(ERRORS.serverError, PATHS.allRooms);
          }
        });
  }

  alreadyjoined(idRoom) {
    this.props.history.push(PATHS.room(idRoom))
  }

  amIjoined(my_username,players) {
    return players.some(item => my_username === item)
  }

  createRoom() {
    this.props.history.push(PATHS.createRoom)
  }

  componentDidMount() {
    if (this.props.shouldFetch) {
      this.props.fetchRoomsHard()
    } else {
      this.setState({
        interval: setInterval(() => this.props.fetchRoomsSoft(), REFRESH_RATE_ROOMS)
      })
    }
  }

  componentWillUnmount() {
    if (!isNull(this.state.interval)) {
      clearInterval(this.state.interval)
    }
  }

  render() {
    let isLogged = !isNull(this.props.username);
    if (isLogged) {
      if (this.props.isLoading || this.props.shouldFetch) {
        return <Loading color={'#af2423'} size={'10%'}/>
      } else {
        return (
            <div>
              <div className={"tc"}>
                <button className={""} onClick={() => this.createRoom()}>Crear Game</button>
              </div>

              {this.props.rooms.map((postDetail) => {
                let cond_comp = null;
                if (this.amIjoined(this.props.username,postDetail.players)){
                  cond_comp = <button
                              onClick={() => this.alreadyjoined(postDetail.id)}>
                            Entrar room</button>
                } else {
                    if (!postDetail.game_has_started && postDetail.players.length < 4){
                    cond_comp = <button
                              onClick={() => this.joinGame(postDetail.id,this.props.username)}>
                            Unirse
                          </button>
                    }
                    else{
                      if(postDetail.game_has_started){
                        cond_comp = <p>La partida ya empezo</p>
                      }
                      else{
                        cond_comp = <p>La partida está llena</p>
                      }
                    }
                }
                return(
                    <div key={postDetail.id}>
                      <h1>Nombre tablero: {postDetail.name}</h1>
                      <p>Creador: {postDetail.owner}</p>
                      {postDetail.players.map((item,index) => (
                        <p key={index}>Jugador {index + 1}: {item}</p>
                      ))}
                      <p>max jug: {postDetail.max_players}</p>
                      {cond_comp}
                    </div>)
              })}
            </div>
        );
      }
    } else {
      this.props.setError(ERRORS.notLogged, PATHS.login);
      return <Redirect to={PATHS.login}/>
    }
  }
}

export default PostList;
