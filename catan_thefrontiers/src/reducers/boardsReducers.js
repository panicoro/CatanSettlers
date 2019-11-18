import {BOARDS, minusOrZero} from "../constants";

export default function boardsEdit(boards = {isFetching: 0, needsFetch: 1, items: []}, action) {
    switch (action.type) {
        case 'REQUEST_ITEMS':
            return (action.itemType === BOARDS)
                ? {...boards, isFetching: boards.isFetching + 1}
                : boards;
        case 'RECEIVE_ITEMS':
            return (action.itemType === BOARDS)
                ? {...boards, needsFetch: minusOrZero(boards.needsFetch), items: action.items}
                : boards;
        case 'END_FETCH':
            return (action.itemType === BOARDS)
                ? {...boards, isFetching: boards.isFetching - 1}
                : boards;
        case 'REMOVE_USER':
            return {...boards, needsFetch: boards.needsFetch + 1};
        default:
            return boards;
    }
}