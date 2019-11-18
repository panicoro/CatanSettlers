const initialState = {
  user: {
    name: null,
    token: null
  },
  rooms: {
    isFetching: 0,
    needsFetch: 1,
    items: []
  },
  boards: {
    isFetching: 0,
    needsFetch: 1,
    items: []
  },
  games: [],
  error: {
    msg: null,
    path: null
  }
};

export default initialState
