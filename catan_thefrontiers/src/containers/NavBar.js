import {connect} from "react-redux";
import NavBar from "../components/NavBar";

function mapStateToProps(state) {
    return {
        currentUser: state.user.name
    }
}

const NavBar_container = connect(
    mapStateToProps,
    null
)(NavBar);

export default NavBar_container