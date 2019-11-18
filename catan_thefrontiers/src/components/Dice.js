import React from 'react'
import ReactDice from 'react-dice-complete'
import 'react-dice-complete/dist/react-dice-complete.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import {arrayCompare} from "../constants";

export default class Dice extends React.Component {
    componentDidMount() {
        this.reactDice.rollAll(this.props.turn.dice);
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (!arrayCompare(prevProps.turn.dice, this.props.turn.dice) || prevProps.turn.user !== this.props.turn.user) {
            this.reactDice.rollAll(this.props.turn.dice);
        }
    }

    render() {
        return (
            <div>
                <ReactDice
                    faceColor="#000000"
                    dotColor="#FF0000"
                    outline={true}
                    outlineColor="#FF0000"
                    numDice={2}
                    ref={dice => this.reactDice = dice}
                    disableIndividual
                />
            </div>
        )
    }
}
