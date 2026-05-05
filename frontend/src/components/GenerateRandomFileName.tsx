const getFileName = () => {
  const array = new Uint8Array(6);
  crypto.getRandomValues(array);
  const random = Array.from(array)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");

  return `${random}`;
};

export default getFileName;