import {connect} from "react-redux";
import CreateLobby from "../components/CreateLobby";
import {fetchItems, setErrorMsg} from "../actions/appActions";
import {BOARDS} from "../constants";
import {addRoom} from "../actions/userActions";

function mapStateToProps(state) {
    return {
        boards: state.boards.items,
        isLoading: state.boards.isFetching,
        shouldFetch: state.boards.needsFetch,
        currentUser: state.user.name
    }
}

function mapDispatchToProps(dispatch) {
    return {
        fetchBoardsHard: () => {
            dispatch(fetchItems(BOARDS, true))
        },
        createRoom: (name, owner, id, game_id, board_id) => {
            dispatch(addRoom(name, owner, 4, id, game_id, board_id))
        },
        setError: (error, path) => {
            dispatch(setErrorMsg(error, path))
        }
    }
}

const CreateLobby_container = connect(
    mapStateToProps,
    mapDispatchToProps
)(CreateLobby);

export default CreateLobby_container