import React from 'react'
import axios from 'axios'
import {Redirect} from 'react-router-dom'
import Hexagon from './Hexagon'
import Vertex from './Vertex'
import Cards from './Cards'
import {
    ACTIONS,
    API,
    API_URL,
    ERRORS,
    isNull,
    isUndefined,
    PATHS,
    REFRESH_RATE_GAMES,
    vertexGrid,
    validActions 
} from "../constants";
import Commerce from "./Commerce";
import Resources from "./Resources";
import Buy from "./Buy";
import Dice from "./Dice";
import Steal from "./Steal";
import Loading from "./Loading";

export default class Board extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            hexRatio : 100,
            margin: 150,
            interval: undefined,
         };

        this.handleTurnEnd = this.handleTurnEnd.bind(this);
        this.generateError = this.generateError.bind(this);
        this.validRender = this.validRender.bind(this);
    }

    handleTurnEnd() {
        axios.post(API_URL+API.playerActions(this.props.id), {type: ACTIONS.endTurn, payload: null})
            .catch(() => {
                this.props.setError(ERRORS.serverError, PATHS.game(this.props.id));
            })
    }

    generateError() {
        const game = this.props.game;
        const loggedIn = !isNull(this.props.user);
        const validGame = !isUndefined(game.board);
        const userPermited = (validGame && loggedIn && game.players.some(p => (p.username === this.props.user)));

        if (!loggedIn) {
            this.props.setError(ERRORS.notLogged, PATHS.login);
        } else if (!userPermited) {
            this.props.setError(ERRORS.notValidGame, PATHS.allRooms);
        }
    }

    componentDidMount() {
        const game = this.props.game;
        const loggedIn = !isNull(this.props.user);

        if (loggedIn) {
            if (game.needsFetch) {
                this.props.fetchGameHard(this.props.id, this.props.user);
            } else {
                this.setState({
                    interval: setInterval(() => {
                        this.props.fetchGameSoft(this.props.id, this.props.user)
                    }, REFRESH_RATE_GAMES)
                });
            }
        }
        this.generateError();
    }

    componentWillUnmount() {
        if (!isNull(this.state.interval)) {
            clearInterval(this.state.interval)
        }
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        this.generateError();
        if (isNull(this.state.interval)) {
            this.setState({
                interval: setInterval(() => {
                    this.props.fetchGameSoft(this.props.id, this.props.user)
                }, REFRESH_RATE_GAMES)
            });
        }
    }

    validRender() {
        const game = this.props.game;
        const board = game.board;
        const playerInfo = game.players.find(player => (player.username === this.props.user));
        const my_turn = (this.props.user === game.current_turn.user);
        const otherPlayers = game.players.filter(p => (p.username !== playerInfo.username));
        ///////////////////////////////////////////////////////////////////////////////////////////
        //Constantes para la colocacion de elementos
        const SIZE = this.state.hexRatio*1.5;
        const HEIGHT = this.state.hexRatio*1.3;
        ///////////////////////////////////////////////////////////////////////////////////////////
        //Constante para la colocacion de vertices
        const margin = this.state.margin*1.1 - this.state.hexRatio;
        const yVertAxys = (index) => {
            if(index===0){
                return margin
            }
            else if ((index % 2) === 1){
                return HEIGHT/3;
            }
            return HEIGHT/1.5;
        };
        const xVertAxys = (index) => {
            const start = this.state.margin + SIZE;
            if([0,11].includes(index)){
                return start
            }
            else if ([1,2,9,10].includes(index)){
                return start - SIZE/2
            }
            else if ([3,4,7,8].includes(index)){
                return start - SIZE
            }
            return start - SIZE*3/2;
        };
        //////////////////////////////////////////////////////////////////////////////////////////
        let vertexHeigth = 0;
        const ROADMAP = vertexGrid.map(
            (level, lIndex) => {
                vertexHeigth = vertexHeigth + yVertAxys(lIndex);
                let vertexLength = 0;
                return level.map(
                    (vertex, vIndex) => {
                        
                        var actions = (game === undefined || game.myActions.length === 0) ? [] :
                        game.myActions.filter(action => 
                            validActions.includes(action.type)  &&
                            (action.payload.filter(item => 
                                    ((item.index === vertex.index) && (item.level === vertex.level))
                                ).length!==0
                            )
                        );

                        vertexLength = xVertAxys(lIndex) + SIZE*vIndex;
                        return <Vertex x={vertexLength} y={vertexHeigth} level={vertex.level}
                                       index={vertex.index} key={`${lIndex},${vIndex}`} actions={actions}/>
                    }
                )
            }
        );
        ///////////////////////////////////////////////////////////////////////////////////////////
        //Ordena el arreglo de objetos de hexagonos segun la linea donde sera renderizada

        const xAxys = (index, plus) => ((this.state.margin + plus + SIZE*index).toString());
        const yAxys = (index) => ((this.state.margin + HEIGHT*index).toString());

        let level0 = [];
        let level1 = [];
        let level2 = [];
        let level3 = [];
        let level4 = [];

        board.forEach((item)=> {
            if(item.HEX_POSITION.level === 2 && ([11,0,1].includes(item.HEX_POSITION.index))){
                level0[[11,0,1].indexOf(item.HEX_POSITION.index)]=item;
            }
            else if (item.HEX_POSITION.level === 2 && ([7,6,5].includes(item.HEX_POSITION.index))) {
                level4[[7,6,5].indexOf(item.HEX_POSITION.index)]=item;
            }
            else if ((item.HEX_POSITION.level === 2 && [10,2].includes(item.HEX_POSITION.index))
                    || (item.HEX_POSITION.level === 1 && [5,0].includes(item.HEX_POSITION.index))) {
                level1[[10,5,0,2].indexOf(item.HEX_POSITION.index)]=item;
            }
            else if ((item.HEX_POSITION.level === 2 && [8,4].includes(item.HEX_POSITION.index))
                    || (item.HEX_POSITION.level === 1 && [3,2].includes(item.HEX_POSITION.index))) {
                level3[[8,3,2,4].indexOf(item.HEX_POSITION.index)]=item;
            }
            else {
                level2[[9,4,0,1,3].indexOf(item.HEX_POSITION.index)]=item;
            }
         });

        ///////////////////////////////////////////////////////////////////////////////////////////
        //implementacion de la lineas de hexagonos que seran implementadas

        let FIRSTLEVEL = level0.map( (elem, index) => {
            let ident= `level0,index${index}`;
            let robberPos = ((elem.HEX_POSITION.level===game.robber.level)
                && (elem.HEX_POSITION.index===game.robber.index));
            return <Hexagon id={ident} robber={robberPos} ratio={this.state.hexRatio}
                            centerX={xAxys(index,SIZE)} key={index} centerY={yAxys(0)}
                            terrain={elem.terrain} token={elem.token} level={elem.level} index={elem.index}/>
        });
        let SECONDLEVEL = level1.map( (elem, index) => {
            let ident= `level1,index${index}`;
            let robberPos = ((elem.HEX_POSITION.level===game.robber.level)
                && (elem.HEX_POSITION.index===game.robber.index));
            return <Hexagon id={ident} robber={robberPos} ratio={this.state.hexRatio}
                            centerX={xAxys(index,SIZE/2)} key={index} centerY={yAxys(1)}
                            terrain={elem.terrain} token={elem.token} level={elem.level} index={elem.index}/>
        });
        let THIRDLEVEL = level2.map( (elem, index) => {
            let ident= `level2,index${index}`;
            let robberPos = ((elem.HEX_POSITION.level===game.robber.level)
                && (elem.HEX_POSITION.index===game.robber.index));
            return <Hexagon id={ident} robber={robberPos} ratio={this.state.hexRatio}
                            centerX={xAxys(index,0)} key={index} centerY={yAxys(2)}
                            terrain={elem.terrain} token={elem.token} level={elem.level} index={elem.index}/>
        });
        let FOURTHLEVEL = level3.map( (elem, index) => {
            let ident= `level3,index${index}`;
            let robberPos = ((elem.HEX_POSITION.level===game.robber.level)
                && (elem.HEX_POSITION.index===game.robber.index));
            return <Hexagon id={ident} robber={robberPos} ratio={this.state.hexRatio}
                            centerX={xAxys(index,SIZE/2)} key={index} centerY={yAxys(3)}
                            terrain={elem.terrain} token={elem.token} level={elem.level} index={elem.index}/>
        });
        let FIFTHLEVEL = level4.map( (elem, index) => {
            let ident= `level4,index${index}`;
            let robberPos = ((elem.HEX_POSITION.level===game.robber.level)
                && (elem.HEX_POSITION.index===game.robber.index));
            return <Hexagon id={ident} robber={robberPos} ratio={this.state.hexRatio}
                            centerX={xAxys(index,SIZE)} key={index} centerY={yAxys(4)}
                            terrain={elem.terrain} token={elem.token} level={elem.level} index={elem.index}/>
        });
        ///////////////////////////////////////////////////////////////////////////////////////////

        return (
        <div className='toolbar' style={{margin:'10px'}}>
            <Dice turn={game.current_turn}/>
            <svg id="canvas" width="1200" height="1200" >
                {FIRSTLEVEL}
                {SECONDLEVEL}
                {THIRDLEVEL}
                {FOURTHLEVEL}
                {FIFTHLEVEL}
                {ROADMAP}
            </svg>
            {my_turn && <Buy
                res={game.myResources}
                id={game.id}
                user={this.props.user}
                update={this.props.fetchGameSoft}
                setError={() => this.props.setError(ERRORS.serverError, PATHS.game(game.id))}/>
            }
            <Cards cards={game.myCards}/>
            <Resources res={game.myResources}/>
            {my_turn && <Commerce res={game.myResources}/>}
            {my_turn && <Steal users={otherPlayers} robber={game.robber} my_turn={my_turn}/>}
            {my_turn && <button onClick={this.handleTurnEnd}>Terminar turno</button>}
        </div>
       )
    }

    render() {

        const game = this.props.game;
        const loggedIn = !isNull(this.props.user);
        const validGame = !isUndefined(game.board);
        const userPermited = (validGame && loggedIn && game.players.some(p => (p.username === this.props.user)));

        if (loggedIn) {
            if (game.isFetching || game.needsFetch) {
                return <Loading color={'#af2423'} size={'10%'}/>
            } else if (userPermited && !game.game_has_started) {
                return <Redirect to={PATHS.allRooms}/>
            } else if (!userPermited) {
                return <Redirect to={PATHS.allRooms}/>
            } else if (game.winner) {
                return (
                    <div className={"tc"}>
                        <h1>Partida terminada!</h1>
                        <br/>
                        <h3>{"Ganador: " + game.winner}</h3>
                        <br/><br/>
                        <img src="/img/hastaLaVista.jpg" alt="Hasta la Vista Baby!"/>
                    </div>
                );
            } else {
                return this.validRender()
            }
        } else {
            return <Redirect to={PATHS.login}/>
        }
    }
}
