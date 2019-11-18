import {connect} from "react-redux";
import ErrorMsg from "../components/ErrorMsg";
import {cleanErrorMsg} from "../actions/appActions";

function mapStateToProps(state) {
    return {
        error: state.error
    }
}

function mapDispatchToProps(dispatch) {
    return {
        clearError: () => {
            dispatch(cleanErrorMsg())
        }
    }
}

const ErrorMsg_container = connect(
    mapStateToProps,
    mapDispatchToProps
)(ErrorMsg);

export default ErrorMsg_container