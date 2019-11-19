import React from 'react'
import axios from 'axios'
import Form from 'react-bootstrap/Form'
import 'react-notifications/lib/notifications.css';
import {NotificationContainer, NotificationManager} from 'react-notifications';
import Button from 'react-bootstrap/Button'
import 'bootstrap/dist/css/bootstrap.min.css'
import {ACTIONS, API, API_URL} from "../constants";

export default class Buy extends React.Component {

    handleClick() {
        axios.post(API_URL+API.playerActions(this.props.id), {type: ACTIONS.buyCard, payload: null})
            .then(() => {
                NotificationManager.success('Se ha comprado la carta correctamente', 'Bien!');
                this.props.update(this.props.id, this.props.user);
            })
            .catch(() => {
                this.props.setError();
            })
    }

    render() {
        return (
            <div>
                <Form style={{ margin: '15px' }}>
                    <Button variant="warning" onClick={() => (this.props.res.wool>0 && this.props.res.ore>0 && this.props.res.grain>0)
                        ? this.handleClick()
                        : NotificationManager.error('No posee suficientes recursos, se necesita por lo menos, una unidad de trigo, de lana, y de minerales', 'Error')}>
                        Comprar carta de desarrollo
                    </Button>
                    <NotificationContainer/>
                </Form>
            </div>
        )
    }

}
