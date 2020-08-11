import React from 'react';
import Jumbotron from 'react-bootstrap/Jumbotron';
import './General.css'
import Background from '../images/background.gif'; 

const Landing = () => {
  // Modify the DOM Styles with JavaScript
  document.body.style.backgroundImage = `url(${Background})`
  document.body.style.backgroundSize = 'cover';
  document.body.style.backgroundRepeat = 'no-repeat';

  return (
    <div className='container'>
      <Jumbotron id='jumbotron'>
        <h1> Welcome to the game Settlers of Catan </h1>
          <p>This is an implementation of the classic board game for a subset of rules.</p>
          <p>For an introduction to the game it is recommended to read its  
          <a href='https://drive.google.com/file/d/1xAtBKKUcGGNYGmStsaMez-lXh7LsySiM/view'>  basic rules </a> 
          in principle and then its <a href='https://drive.google.com/file/d/11sOYT_F_m4w6JRAGLTlwvNwMjfuMlXPN/view'> 
          detailed rules </a>.</p>
          <p>If you feel ready to play, singup and start playing!</p>
          <p>Good Luck!</p>
      </Jumbotron>
    </div>
    );
}

export default Landing;
