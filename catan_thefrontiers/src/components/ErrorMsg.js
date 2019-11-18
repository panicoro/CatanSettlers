import React from 'react'
import {ERROR_TIMER, isNull} from "../constants";

export default class ErrorMsg extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            timer: null,
        }
    }

    componentDidMount() {
        this.setState({
            timer: setTimeout(this.props.clearError, ERROR_TIMER)
        })
    }

    componentWillUnmount() {
        const validTimer = !isNull(this.state.timer);
        if (validTimer) {
            clearTimeout(this.state.timer);
        }
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        const validError = !isNull(this.props.error.msg);
        const validPath = (this.props.error.path === this.props.location.pathname);
        const validTimer = !isNull(this.state.timer);
        const timerShouldUpdate = (prevProps.error.path !== this.props.error.path);
        if (validError && timerShouldUpdate) {
            if (validPath) {
                if (validTimer) {
                    clearTimeout(this.state.timer);
                }
                this.setState({
                    timer: setTimeout(this.props.clearError, ERROR_TIMER)
                })
            } else {
                this.props.clearError();
                if (validTimer) {
                    clearTimeout(this.state.timer);
                    this.setState({
                        timer: null
                    })
                }
            }
        }
    }

    render() {
        const validError = !isNull(this.props.error.msg);
        const validPath = (this.props.error.path === this.props.location.pathname);
        if (validError && validPath) {
            return (
                <div>
                    <br/>
                    <p style={{color: "red"}}>
                        <i>{this.props.error.msg}</i>
                    </p>
                </div>
            )
        } else {
            return null
        }
    }
}