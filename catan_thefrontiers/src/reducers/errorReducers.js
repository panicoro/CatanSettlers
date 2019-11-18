export default function errorEdit(error = {msg: null, path: null}, action) {
    switch (action.type) {
        case 'SET_ERR_MSG':
            return {msg: action.error, path: action.path};
        case 'CLEAN_ERR_MSG':
            return {msg: null, path: null};
        default:
            return error
    }
}