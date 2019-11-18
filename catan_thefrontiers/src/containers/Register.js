import {connect} from "react-redux";
import {addUser} from "../actions/userActions";
import Register from "../components/Register";
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

const Register_container = connect(
  mapStateToProps,
  mapDispatchToProps
)(Register);

export default Register_container