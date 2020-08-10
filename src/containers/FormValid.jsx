export const validateUsername = (username) => {
  let errorMessage = '';
  if (!username) {
    errorMessage = 'This field is required';
  } if (!/^[\S]+$/.test(username)) {
    errorMessage = 'Space are not allowed';
  }
  return errorMessage;
};

export const validatePassword = (password) => {
  let errorMessage = '';
  if (!password) {
    errorMessage = 'This field is required';
  } else if (password.length < 8) {
    errorMessage = 'Please enter at least 8 characters';
  } else if (/^[^a-z]{8,}$/.test(password)) {
    errorMessage = 'Password requires at least one lowercase';
  } else if (/^[^A-Z]{8,}$/.test(password)) {
    errorMessage = 'Password requires at least one uppercase';
  } else if (/^[a-zA-Z\d]{8,}$/.test(password)) {
    errorMessage = 'Password requires at least one special character';
  }
  return errorMessage;
};
