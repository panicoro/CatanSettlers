import React from 'react';
import axios from 'axios'
import {Redirect} from 'react-router-dom'
import {isNull, PATHS, ERRORS, CODES, API_URL, API} from "../constants";
import "react-mdl/extra/material.css";
import "react-mdl/extra/material.js";
import {Textfield, Button} from 'react-mdl';
import {FormControl} from "@material-ui/core";
import "../css/register-login.css"

export default class Register extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      user: "",
      password: ""
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const {name, value} = event.target;
    this.setState({
      [name]: value
    })
  }

  handleSubmit(e) {
    e.preventDefault()
    axios.post(API_URL+API.register, {user: this.state.user, pass: this.state.password})
      .then(() => {
        axios.post(API_URL+API.login, 
                   {user: this.state.user, pass: this.state.password})
          .then(res => {
            this.props.addUser(this.state.user, res.token);
            this.props.history.replace(PATHS.allRooms);
          })
          .catch(error => {
            if (CODES.clientError(error.response.status)) {
              this.props.setError(ERRORS.loginInvalid, PATHS.login);
            } else {
              this.props.setError(ERRORS.serverError, PATHS.login);
            }
            this.props.history.replace(PATHS.login);
          })
      })
      .catch(error => {
        if (CODES.clientError(error.response.status)) {
          this.props.setError(ERRORS.registerInvalid, PATHS.register);
        } else {
          this.props.setError(ERRORS.serverError, PATHS.register);
        }
      })
  }

  componentDidMount() {
    if (!isNull(this.props.currentUser)) {
      this.props.setError(ERRORS.logged, PATHS.allRooms);
    }
  }

  render() {
    if (isNull(this.props.currentUser)) {
      return (
        <div>
          <link rel="stylesheet" href="material.css"/>
          <script src="material.js"></script>
          <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"/>

          <form noValidate autoComplete="off" >
            <div className={"tc"}>
              <h2>Registrar Cuenta</h2>
              <FormControl >
                <Textfield
                  floatingLabel
                  style={{"width": '400px'}}
                  autoFocus={true}
                  id="filled-dense"
                  label="Username"
                  type="text"
                  name="user"
                  value={this.state.user}
                  onChange={this.handleChange}
                  pattern="^[a-zA-Z0-9]*$"
                  error={!"pattern" ? "": "Solo letras mínusculas y/o mayúsculas y/o números"}
                />

                <Textfield
                  style={{"width": '400px'}}
                  label="Password"
                  type="password"
                  name="password"
                  value={this.state.password}
                  onChange={this.handleChange}
                  pattern="(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
                  error={!"pattern" ? "" : "Mínimo 8 caracteres, una mayúscula, una minúscula, y un número"}
                />

                <Button
                  raised accent ripple
                  disabled={!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/g.test(this.state.password)
                  || !/^[a-zA-Z0-9]*$/gm.test(this.state.user)
                  }
                  onClick={this.handleSubmit}>
                    Registrar
                </Button>
              </FormControl>
            </div>
          </form>
        </div>
      )
    } else {
      return <Redirect to={PATHS.allRooms}/>
    }
  }
}
