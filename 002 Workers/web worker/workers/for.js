setTimeout(function () {
  self.postMessage("hello world !!{for} , after 5s");
}, 5000);

self.onmessage = function (event) {
  console.log(event.data);

  if (event.data === "btnClick") {
    self.postMessage("hello world !!{for} , after btnClick");
  } else {
  }
};
