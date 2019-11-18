import {connect} from "react-redux";
import Board from "../components/Board"
import {fetchItems, setErrorMsg} from "../actions/appActions";
import {GAMES, isUndefined} from "../constants"

function mapStateToProps(state, ownProps) {
    const game = state.games.find(game => (game.id === ownProps.id));
    return {
        user: state.user.name,
        game: !isUndefined(game) ? game : {},
    }
}

function mapDispatchToProps(dispatch) {
    return {
        fetchGameSoft: (id, user) => {
            dispatch(fetchItems(GAMES, false, id));
            dispatch(fetchItems(GAMES, false, id, 'board'));
            dispatch(fetchItems(GAMES, false, id, 'player', user));
            dispatch(fetchItems(GAMES, false, id, 'player/actions', user));
        },
        fetchGameHard: (id, user) => {
            dispatch(fetchItems(GAMES, true, id));
            dispatch(fetchItems(GAMES, true, id, 'board'));
            dispatch(fetchItems(GAMES, true, id, 'player', user));
            dispatch(fetchItems(GAMES, true, id, 'player/actions', user));
        },
        setError: (error, path) => {
            dispatch(setErrorMsg(error, path))
        }
    }
}

const Game_container = connect(
    mapStateToProps,
    mapDispatchToProps
)(Board);

export default Game_container
