import React from 'react';
import Button from 'react-bootstrap/Button';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { LinkContainer } from 'react-router-bootstrap';
import PropTypes from 'prop-types';
import icon from '../images/catan_icon.png';

const NavBar = ({ auth, logout }) => {
  const items = (
    <>
      <LinkContainer to="/signup">
        <Button variant="outline-light"
          className="mr-sm-2">
            Register
        </Button>
      </LinkContainer>
      <LinkContainer to="/login">
        <Button variant="outline-light">Log in</Button>
      </LinkContainer>
    </>
  );

  const logoutButton = (
    <LinkContainer to="/">
      <Button onClick={logout}
              variant="outline-light">
        Log out
      </Button>
    </LinkContainer>
  );

  return (
    <Navbar  expand="lg" variant="dark" bg="dark" 
             className="justify-content-between">
      <Navbar.Brand  href="/"> 
      <img
        alt=""
        src={icon}
        width="30"
        height="30"
        className="d-inline-block align-top"
      />{' '}Settlers of Catan</Navbar.Brand>

      <Navbar.Collapse className="justify-content-end">
        <Nav >
          {auth ? logoutButton : items}
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default NavBar;


NavBar.propTypes = {
  auth: PropTypes.bool.isRequired,
  logout: PropTypes.func.isRequired,
};
