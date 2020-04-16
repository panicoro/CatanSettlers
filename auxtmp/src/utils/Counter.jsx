const counter = (list, string) => {
  let count = 0;
  list.forEach((element) => {
    if (element === string) {
      count += 1;
    }
  });
  return count;
};

export default counter;
