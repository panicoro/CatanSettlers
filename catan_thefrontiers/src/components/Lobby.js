import React from 'react'
import axios from 'axios'
import {Redirect} from 'react-router-dom'
import Loading from "./Loading";
import {API, isNull, isUndefined, PATHS, REFRESH_RATE_ROOMS, ERRORS} from "../constants";

export default class Lobby extends React.Component {
    constructor(props) {
        super(props);

        this.handleExit = this.handleExit.bind(this);
        this.handleCancel = this.handleCancel.bind(this);
        this.handleStart = this.handleStart.bind(this);
        this.generateError = this.generateError.bind(this);

        this.state = {
            interval: null,
        }
    }

    generateError() {
        const loggedIn = !isNull(this.props.currentUser);
        const validRoom = !isUndefined(this.props.name);
        const userPermited = (validRoom && loggedIn && this.props.players.includes(this.props.currentUser));

        if (!loggedIn) {
            this.props.setError(ERRORS.notLogged, PATHS.login);
        } else if (!userPermited) {
            this.props.setError(ERRORS.notValidRoom, PATHS.allRooms);
        }
    }

    handleExit() {
        this.props.history.push(PATHS.allRooms)
    }

    handleCancel() {
        axios.delete(API.room(this.props.id))
            .then(() => {
                this.props.history.replace(PATHS.allRooms);
                this.props.terminateLobby(this.props.id);
            })
            .catch(() => {
                this.props.setError(ERRORS.serverError, PATHS.room(this.props.id));
            })
    }

    handleStart() {
        axios.patch(API.room(this.props.id))
            .then(() => {
                this.props.startGame(this.props.id, this.props.game_id);
                this.props.history.replace(PATHS.game(this.props.game_id));
            })
            .catch(() => {
                this.props.setError(ERRORS.serverError, PATHS.room(this.props.id));
            })
    }

    componentDidMount() {
        const loggedIn = !isNull(this.props.currentUser);
        if (loggedIn) {
            if (this.props.shouldFetch) {
                this.props.fetchRoomsHard()
            } else {
                this.setState({
                    interval: setInterval(() => this.props.fetchRoomsSoft(), REFRESH_RATE_ROOMS)
                })
            }
        }
        this.generateError();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        this.generateError();
        if (isNull(this.state.interval)) {
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
        const loggedIn = !isNull(this.props.currentUser);
        const validRoom = !isUndefined(this.props.name);
        const userPermited = (validRoom && loggedIn && this.props.players.includes(this.props.currentUser));
        if (loggedIn) {
            if (this.props.isLoading || this.props.shouldFetch) {
                return <Loading color={'#af2423'} size={'10%'}/>
            } else if (userPermited && this.props.game_has_started) {
                return <Redirect to={PATHS.game(this.props.game_id)}/>
            } else if (!userPermited) {
                return <Redirect to={PATHS.allRooms}/>
            } else {
                return (
                    <div>
                        <h2>
                            {this.props.name}
                        </h2>
                        <ul>
                            {this.props.players.map((player, index) => (
                            <li key={index}>
                                {player}
                                {(player === this.props.owner) && " (Creador)"}
                                {(player === this.props.currentUser) && " (Yo)"}
                            </li>
                            ))}
                        </ul>
                        {
                            (this.props.owner === this.props.currentUser) &&
                            <div>
                                <button
                                    onClick={this.handleStart}
                                    disabled={this.props.players.length < 3}>
                                    Empezar partida
                                </button>
                                <button onClick={this.handleCancel}>Cancelar partida</button>
                            </div>
                        }
                        <button onClick={this.handleExit}>Volver a la lista</button>
                        <button onClick={this.props.fetchRoomsHard}>Refrescar</button>
                    </div>
                )
            }
        } else {
            return <Redirect to={PATHS.login}/>
        }
    }
}
