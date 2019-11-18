import React from 'react'
import brickField from '../assets/brickField.png';
import desertField from '../assets/desertField.png';
import lumberField from '../assets/lumberField.png';
import oreField from '../assets/oreField.png';
import sheepField from '../assets/sheepField.png';
import wheatField from '../assets/wheatField.png';
import robber from '../assets/robber.png';

//import PropTypes from 'prop-types'

export default class Hexagon extends React.Component {

    render() {

      const ratio = parseInt(this.props.ratio);
      const centerX= parseInt(this.props.centerX);
      const centerY= parseInt(this.props.centerY);
      let pointsString = "";

      for (let index = 1; index < 7; index++) {
        pointsString+=`${centerX + ratio*(Math.cos(60 * index * Math.PI / 180))},${centerY + ratio*(Math.sin(60 * index * Math.PI / 180))}`;
        if(index<6){
          pointsString+=' ';
        }
      }

      let field;
      switch(this.props.terrain) {
        case 'brick':
          field=brickField;
          break;
        case 'desert':
          field=desertField;
          break;
        case 'ore':
          field=oreField;
          break;
        case 'wheat':
          field=wheatField;
          break;
        case 'lumber':
          field=lumberField;
          break;
        case 'sheep':
          field=sheepField;
          break;
      }


      let textColor;
      if (this.props.token==='6'||this.props.token==='8'){
        textColor = 'red'
      }
      else{
        textColor = 'black'
      }

      let tokenCoin;
      if (this.props.robber){
        tokenCoin =
          <svg>
            <filter id='robber' x="0%" y="0%" width="100%" height="100%">
              <feImage href={robber}/>
            </filter>
            <circle cx={this.props.centerX} cy={this.props.centerY} r={this.props.ratio/2} filter='url(#robber)'/>
          </svg>
      }
      else if (this.props.terrain!=='desert') {
        tokenCoin =
        <svg>
          <circle cx={this.props.centerX} cy={this.props.centerY} r={this.props.ratio/4} stroke="black" stroke-width="3" fill="yellow" fill-opacity="0.4"/>
          <text x={this.props.centerX} y={this.props.centerY} font-family="Verdana" font-size="28" fill={textColor} text-anchor="middle" alignment-baseline="central" >{this.props.token}</text>
        </svg>
      }

      let url= "url(#"+this.props.id.toString()+")";
      return (
        <svg className={this.props.id} >
          <filter id={this.props.id} x="0%" y="0%" width="100%" height="100%">
             <feImage href={field}/>
          </filter>
          <polygon filter={url} points={pointsString} onClick={this.props.onclick}></polygon>
          {tokenCoin}
        </svg>
      )
    }
  }
