import {removeUser} from "../actions/userActions";
import {connect} from "react-redux";
import Logout from "../components/Logout";

function mapStateToProps(state) {
    return {
        currentUser: state.user.name
    }
}

function mapDispatchToProps(dispatch) {
    return {
        removeUser: () => {
            dispatch(removeUser())
        },
    }
}

const Logout_container = connect(
    mapStateToProps,
    mapDispatchToProps
)(Logout);

export default Logout_container