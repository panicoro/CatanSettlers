import React from 'react'
import {isNull, PATHS} from "../constants";

function Buttons({currentUser}) {
    return (
      (isNull(currentUser)
        ? <div className="dtc v-mid w-75 tr">
            <a
              className="link dim dark-gray f6 f5-ns dib mr3 mr4-ns"
              href={PATHS.register} title="Register">
                Nueva Cuenta
            </a>
            <a
              className="link dim dark-gray f6 f5-ns dib mr3 mr4-ns"
              href={PATHS.login}
              title="Login">
              Entrar
            </a>
          </div>
        : <div className="dtc v-mid w-75 tr">
            <a
              className="link dim dark-gray f6 f5-ns dib mr3 mr4-ns"
              href={PATHS.allRooms}
              title="Rooms">
              Salas
            </a>
            <a className="link dim dark-gray f6 f5-ns dib mr3 mr4-ns"
               href={PATHS.logout}
               title="Logout">
              Cerrar Sesión
            </a>
            <p className="link dim dark-gray f6 f5-ns dib mr3 mr4-ns">/////</p>
            <p className="link dim dark-gray f6 f5-ns dib mr3 mr4-ns">{currentUser}</p>
          </div>)
    )
}

export default class NavBar extends React.Component {
    render() {
      return (
          <nav className="dt w-100 border-box pa3 ph5-ns">
            <a className="dtc v-mid mid-gray link dim w-25" href="/" title="Home">
              <img src="/img/colon.png"
                      className="dib w2 h2 br-100"
                      alt="Site Name"/>
            </a>
            <Buttons currentUser={this.props.currentUser}/>
          </nav>
      )
    }
}