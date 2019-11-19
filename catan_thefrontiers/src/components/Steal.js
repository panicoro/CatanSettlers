import React from 'react'
import Select from 'react-select'
import Form from 'react-bootstrap/Form'
import {NotificationContainer, NotificationManager} from 'react-notifications';
import Button from 'react-bootstrap/Button'
import {ACTIONS, API, API_URL} from "../constants";
import axios from 'axios'

export default class Steal extends React.Component {

    constructor(props) {
        super(props);
        this.state = {player: ''};
        this.handlePlayer = this.handlePlayer.bind(this);
     }
    
    handleClick() {
        axios.post(API_URL+API.playerActions(this.props.id), {type: ACTIONS.move_robber, payload: {
            player: this.state.player
        }})
            .then(() => {
                NotificationManager.success('Se ha comerciado correctamente', 'Bien!');
                this.props.update(this.props.id, this.props.user);
            })
    }

    handlePlayer(event) {
        console.log(event);
        this.setState({player: event.value});
    }  

    render() {
        return (
            <div>
                <Form style={{ margin: '15px' }}>
                    <Form.Group id="d1">
                        <Form.Label>Jugador a robar:</Form.Label>
                        <Select options={this.props.users
                        .filter(user => 
                            user.settlements.filter(
                                sett =>
                                    sett.level === this.props.robber.level || sett.level === this.props.robber.level+1
                                    &&
                                    (this.props.robber.index !== 0 &&
                                    sett.index >= this.props.robber.index*3-2 && this.props.robber.index*3+1 
                                    ) || (
                                    sett.index === 0 || sett.index === 1 || sett.index === ((sett.level*2)+1)*6-1
                                    || sett.index === ((sett.level*2)+1)*6-2
                                    )
                            ).length > 0 || 
                            user.cities.filter(
                                sett =>
                                    sett.level === this.props.robber.level || sett.level === this.props.robber.level+1
                                    &&
                                    (this.props.robber.index !== 0 &&
                                    sett.index >= this.props.robber.index*3-2 && this.props.robber.index*3+1 
                                    ) || (
                                    sett.index === 0 || sett.index === 1 || sett.index === ((sett.level*2)+1)*6-1
                                    || sett.index === ((sett.level*2)+1)*6-2
                                    )
                            ).length > 0
                            )}
                            onChange={this.handlePlayer.bind(this)}/>
                
                    </Form.Group>
                    <Button variant="dark" onClick={() => NotificationManager.success('Se ha robado correctamente', 'Bien!')}>
                        Robar recurso
                    </Button>
                    <NotificationContainer/>
                </Form>
            </div>
        )
    }



}
