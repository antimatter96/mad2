function getBase64(file) {
  console.log("getBase64")
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result.split(',').pop());
    reader.onerror = error => reject(error);
  });
}

export {
  getBase64,
}
