import axios from 'axios'
import {isUndefined} from "../constants";

// accion "pedir salas/tableros/partidas"
const requestItems = (itemType, id = undefined) => ({
    type: 'REQUEST_ITEMS',
    itemType,
    id
});

// accion "recibir salas/tableros/partidas"
const receiveItems = (itemType, items, id = undefined, optional = undefined) => ({
    type: 'RECEIVE_ITEMS',
    itemType,
    items,
    id,
    optional
});

// accion para confirmar la finalizacion de fetchItems (con o sin error)
const endFetch = (itemType, id = undefined) => ({
    type: 'END_FETCH',
    itemType,
    id
});

// accion asincrona para actualizar los items en store
// hard fetch: el store se marca como fetching (para la pantalla de carga)
// soft fetch: en algun momento se actualiza el estado (para actualizaciones periodicas)
export function fetchItems(itemType, hard, id = undefined, optional = undefined, user = undefined) {
    let url = `/${itemType}`;
    if (!isUndefined(id)) {
        url += `/${id}`;
        if (!isUndefined(optional)) {
            url += `/${optional}`;
        }
    }

    return function(dispatch) {
        if (hard) {
            dispatch(requestItems(itemType, id));
        }
        return axios.get(url)
            .then(res => {
                dispatch(receiveItems(itemType, res.data, id, optional))
            })
            .finally(() => {
                if (hard) {
                    dispatch(endFetch(itemType, id))
                }
            });
    }
}

// setear mensaje de error
export const setErrorMsg = (error, path) => ({
    type: 'SET_ERR_MSG',
    error,
    path
});

// limpiar mensaje de error
export const cleanErrorMsg = () => ({
    type: 'CLEAN_ERR_MSG'
});
