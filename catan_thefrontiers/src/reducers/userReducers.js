export default function userEdit(user = {name: null, token: null}, action) {
    switch (action.type) {
        case 'ADD_USER':
            return {name: action.username, token: action.token};
        case 'REMOVE_USER':
            return {name: null, token: null};
        default:
            return user
    }
}