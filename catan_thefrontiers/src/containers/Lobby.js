import {connect} from "react-redux";
import Lobby from "../components/Lobby"
import {removeRoom, startGame} from "../actions/userActions";
import {fetchItems, setErrorMsg} from "../actions/appActions";
import {ROOMS} from "../constants"

function mapStateToProps(state, ownProps) {
    return {
        ...state.rooms.items.find(room => (room.id === ownProps.id)),
        isLoading: state.rooms.isFetching,
        shouldFetch: state.rooms.needsFetch,
        currentUser: state.user.name
    }
}

function mapDispatchToProps(dispatch) {
    return {
        terminateLobby: (id) => {
            dispatch(removeRoom(id))
        },
        startGame: (id, game_id) => {
            dispatch(startGame(id, game_id))
        },
        fetchRoomsHard: () => {
            dispatch(fetchItems(ROOMS, true))
        },
        fetchRoomsSoft: () => {
            dispatch(fetchItems(ROOMS, false))
        },
        setError: (error, path) => {
            dispatch(setErrorMsg(error, path))
        }
    }
}

const Lobby_container = connect(
    mapStateToProps,
    mapDispatchToProps
)(Lobby);

export default Lobby_container