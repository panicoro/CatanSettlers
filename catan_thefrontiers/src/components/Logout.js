import React from "react";
import {Redirect} from 'react-router-dom'
import {PATHS} from "../constants";
import Loading from "./Loading";

export default class Logout extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            shouldRedirect: false
        }
    }

    componentDidMount() {
        this.props.removeUser();
        this.setState({
            shouldRedirect: true
        })
    }

    render() {
        if (this.state.shouldRedirect) {
            return <Redirect to={PATHS.home}/>
        } else {
            return <Loading color={'#af2423'} size={'10%'}/>
        }
    }

}