import React from 'react'
import village from '../assets/village.png';

export default class Vertex extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            building : '',
            level: this.props.level,
            index: this.props.index,
            showMenu: false,
        };


        this.buildVillage = this.buildVillage.bind(this);
    }

    buildVillage(){
        this.setState({
            building: 'village'
        })
    }
/*
    sendAction(payload){
        axios.post(`/games/${this.props.gameId}/player/actions`, payload).then(response => {
            this.props.boardUpdate();
        }).catch(e => {
            console.log(e);
        });
    }
*/
    render() {
        const actions = this.props.actions  
        let building = '';
        if (actions.length!==0 && this.state.building === ''){
            building =
                <circle cx={this.props.x} cy={this.props.y} r="10" stroke="red" stroke-width="2" fill="green" fill-opacity="0.5" />
        }

        else if (this.state.building === 'village' )
            building =
                <svg>
                    <filter id='village' x="0%" y="0%" width="100%" height="100%">
                        <feImage href={village}/>
                    </filter>

                    <circle cx={this.props.x} cy={this.props.y} r="50" fill="black" fill-opacity="1" filter='url(#village)'/>
                </svg>;
        else{
            building =
                    <circle cx={this.props.x} cy={this.props.y} r="10" stroke="black" stroke-width="2" fill="black" fill-opacity="0.3" />
        }


        return (
            <svg id={`vertex:${this.state.level},${this.state.index}`}>
                {building}
            </svg>
        )
    }
}
