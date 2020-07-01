import { colours } from './Constants';


//export const path = process.env.REACT_APP_PATH;

export const getToken = () => JSON.parse(localStorage.getItem('token'));

export const request = (url, opts, onSuccess, onFailure, emptyBody) => {
  const options = { ...opts };

  // Add headers.
  if (!options.headers) options.headers = {};

  // Always use json.
  options.headers['Content-Type'] = 'application/json';

  // Add token if logged in.
  const token = getToken();
  if (token) options.headers.Authorization = `Bearer ${token}`;

  fetch(url, options)
    .then((r) => {
      if (!r.ok) throw Error(r.statusText);

      if (emptyBody) return new Promise((f) => f());

      return r.json();
    })
    .then(onSuccess)
    .catch(onFailure);
};

export const getFromPlayers = (ps) => ({
  settlements: ps.map((player) => ({
    colour: colours[player.colour],
    positions: player.settlements,
  })),

  cities: ps.map((player) => ({
    colour: colours[player.colour],
    positions: player.cities,
  })),

  roads: ps.map((player) => ({
    colour: colours[player.colour],
    positions: player.roads,
  })),

  players: ps.map((player) => ({
    username: player.username,
    colour: colours[player.colour],
    developmentCards: player.development_cards,
    resourceCards: player.resources_cards,
    victoryPoints: player.victory_points,
    lastGained: player.last_gained,
  })),
});
