self.addEventListener("install", (event) => {
  console.log("Installed sw.js", event);
});

self.addEventListener("activate", (event) => {
  console.log("Activated sw.js", event);
});

// self.addEventListener("fetch", function (event) {
//   console.log(event.request);
//   event.respondWith(fetch(event.request));
// });

function modify(obj) {
  return obj;
}
self.addEventListener("fetch", function (event) {
  event.respondWith(
    new Promise((resolve, reject) => {
      var req = modify(event.request); // 修改请求

      fetch(req)
        .then((r) => {
          resolve(modify(r));
        })
        .catch((e) => reject(a));
    })
  );
});
