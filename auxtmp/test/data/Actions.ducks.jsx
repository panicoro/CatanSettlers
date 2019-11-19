export const initialState = {
  stage: 'running',
  refresh: () => 'refresh',
  setError: () => 'setError',
  setOnClick: () => 'setOnClick',
  setRunning: () => 'setRunning',
};

export const errorState = {
  stage: 'error',
  refresh: () => 'refresh',
  setError: () => 'setError',
  setOnClick: () => 'setOnClick',
  setRunning: () => 'setRunning',
};
