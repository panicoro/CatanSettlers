import React from "react";
import axios from 'axios'
import {API, isNull, PATHS, ERRORS, CODES} from "../constants";
import Loading from "./Loading";
import {Redirect} from 'react-router-dom'

export default class CreateLobby extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            lobbyName: "",
            selectedBoard: ""
        };

        this.handleNameChange = this.handleNameChange.bind(this);
        this.handleBoardSelect = this.handleBoardSelect.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleNameChange(event) {
        this.setState({
            lobbyName: event.target.value
        })
    }

    handleBoardSelect(event) {
        this.setState({
            selectedBoard: event.target.value
        })
    }

    handleSubmit() {
        axios.post(API.rooms, {name: this.state.lobbyName, board_id: this.state.selectedBoard})
            .then(res => {
                this.props.createRoom(this.state.lobbyName, this.props.currentUser, res.data.id, res.data.game_id, this.state.selectedBoard);
                this.props.history.replace(PATHS.room(res.data.id));
            })
            .catch(error => {
                if (CODES.clientError(error.response.status)) {
                    this.props.setError(ERRORS.createRoomInvalid, PATHS.createRoom);
                } else {
                    this.props.setError(ERRORS.serverError, PATHS.createRoom);
                }
            })
    }

    componentDidMount() {
        const loggedIn = !isNull(this.props.currentUser);
        if (loggedIn && this.props.shouldFetch) {
            this.props.fetchBoardsHard()
        } else if (!loggedIn) {
            this.props.setError(ERRORS.notLogged, PATHS.login);
        }
    }

    render() {
        if (!isNull(this.props.currentUser)) {
            if (this.props.isLoading || this.props.shouldFetch) {
                return <Loading color={'#af2423'} size={'10%'}/>
            } else if (!this.props.boards.length) {
                return (
                    <div>
                        <h1>Oops!</h1>
                        <h2>No se puede jugar sin tableros!</h2>
                        <p>Si hay tableros cargados que no se muestran acá, por favor, comuníquelo al administrador</p>
                    </div>
                )
            } else {
                return (
                    <div>
                        <h2>Crear Sala</h2>
                        <form>
                            <label>
                                {"Nombre del juego: "}
                                <input type="text" value={this.state.lobbyName} onChange={this.handleNameChange}/>
                            </label>
                            <br/><br/>
                            <label>
                                {"Tablero: "}
                                <select value={this.state.selectedBoard} onChange={this.handleBoardSelect}>
                                    <option value={0} disabled={this.state.selectedBoard}>
                                        Elegir...
                                    </option>
                                    {this.props.boards.map(board => (
                                        <option key={board.id} value={board.id}>{board.name}</option>
                                    ))}
                                </select>
                            </label>
                            <br/><br/>
                            <button
                                disabled={!this.state.selectedBoard || !this.state.lobbyName.length}
                                onClick={this.handleSubmit}>
                                Crear
                            </button>
                        </form>
                    </div>
                )
            }
        } else {
            return <Redirect to={PATHS.login}/>
        }
    }
}