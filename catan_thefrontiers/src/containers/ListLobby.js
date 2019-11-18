import {connect} from "react-redux";
import PostList from "../components/PostList"
import {addPlayer} from "../actions/userActions";
import {fetchItems, setErrorMsg} from "../actions/appActions";
import {ROOMS} from "../constants";

function mapStateToProps(state) {
  console.log(state.rooms)
  return {
    username: state.user.name,
    rooms: state.rooms.items,
    isLoading: state.rooms.isFetching,
    shouldFetch: state.rooms.needsFetch,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    addPlayer: (idRoom,username) => {
      dispatch(addPlayer(idRoom,username))
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

const ListLobby_container = connect(
  mapStateToProps,
  mapDispatchToProps
)(PostList);

export default ListLobby_container