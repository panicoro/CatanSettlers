import React from 'react'
import Select from 'react-select'
import Form from 'react-bootstrap/Form'
import {NotificationContainer, NotificationManager} from 'react-notifications'
import Button from 'react-bootstrap/Button'
import {ACTIONS, API} from "../constants"
import axios from 'axios'


//import PropTypes from 'prop-types'

export default class Commerce extends React.Component {

    constructor(props) {
        super(props);
        this.state = {give: '',
                    receive: ''};
        this.handleClick = this.handleClick.bind(this);
     }

    handleClick() {
        axios.post(API.playerActions(this.props.id), {type: ACTIONS.bank_trade, payload: {
            give: this.state.give,
            receive: this.state.receive
        }})
            .then(() => {
                NotificationManager.success('Se ha comerciado correctamente', 'Bien!');
                this.props.update(this.props.id, this.props.user);
            })
    }

    handleGive(event) {
        console.log(event);
        this.setState({give: event.value});
    }    

    handleReceive(event) {
        this.setState({receive: event.value});
    } 

    render() {
        const options = [
            { value: 'lumber', label: 'Madera', valor: this.props.res.lumber },
            { value: 'brick', label: 'Arcilla', valor: this.props.res.brick },
            { value: 'wool', label: 'Lana', valor: this.props.res.wool },
            { value: 'grain', label: 'Cereales', valor: this.props.res.grain },
            { value: 'ore', label: 'Minerales', valor: this.props.res.ore }
        ];
        return (
            <div>
                <Form style={{ margin: '15px' }}>
                    <Form.Group id="d1">
                        <Form.Label>Oferta - 4 unidades del recurso:</Form.Label>
                        <Select 
                        onChange={this.handleGive.bind(this)}
                        options={options.filter(recurso => recurso.valor > 3)}/>
                    </Form.Group>

                    <Form.Group id="d2">
                        <Form.Label>Ganancia - 1 unidad del recurso:</Form.Label>
                        <Select options={options} 
                        
                         onChange={this.handleReceive.bind(this)}/>
                    </Form.Group>
                    <Button variant="dark" onClick={this.handleClick.bind(this)}>
                        Comerciar
                    </Button>
                    <NotificationContainer/>
                </Form>
            </div>
        )
    }

}
