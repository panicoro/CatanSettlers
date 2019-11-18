import {connect} from "react-redux";
import {addUser} from "../actions/userActions";
import Login from "../components/Login";
import {setErrorMsg} from "../actions/appActions";

function mapStateToProps(state) {
    return {
        currentUser: state.user.name
    }
}

function mapDispatchToProps(dispatch) {
    return {
        addUser: (user, token) => {
            dispatch(addUser(user, token))
        },
        setError: (error, path) => {
            dispatch(setErrorMsg(error, path))
        }
    }
}

const Login_container = connect(
    mapStateToProps,
    mapDispatchToProps
)(Login);

export default Login_container