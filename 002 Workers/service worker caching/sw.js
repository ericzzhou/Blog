var cacheName = "www-v4";
var filesToCache = [
  "/", // index.html
  "/main.js",
  "/styles.css",
  "/assets/logo.png",
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(cacheName).then(function (cache) {
      console.info("[sw.js] cached all files");
      return cache.addAll(filesToCache);
    })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (cacheNames) {
      return Promise.all(
        cacheNames.map(function (cName) {
          if (cName !== cacheName) {
            return caches.delete(cName);
          }
        })
      );
    })
  );
});

// self.addEventListener("fetch", function (event) {
//   event.respondWith(
//     caches.match(event.request)
//     .then((response) => {
//       if (response) {
//         return response;
//       }
//       // 不在缓存中，从网络, 这里还需要继续把新文件缓存起来
//       return fetch(event.request, { credentials: "include" });
//     })
//   );
// });

self.addEventListener("fetch", function (event) {
  event.respondWith(
    caches.match(event.request).then((response) => {
      if (response) {
        return response;
      }
      /**
       * 不在缓存中，从网络请求
       * 克隆 request stream 因为 请求流只能被使用一次
       */

      var reqCopy = event.request.clone();
      return fetch(reqCopy, { credentials: "include" }).then((response) => {
        // bad response
        // response.type !== 'basic' means third party origin request
        if (!response || response.status !== 200 || response.type !== "basic") {
          return response; // response stream consumed
        }

        // clone response stream
        // as stream once consumed, can not be used again
        var resCopy = response.clone();

        // ================== IN BACKGROUND ===================== //

        // add response to cache and return response
        caches.open(cacheName).then(function (cache) {
          return cache.put(reqCopy, resCopy); // reqCopy, resCopy streams consumed
        });

        // ====================================================== //

        return response; // response stream consumed
      });
    })
  );
});
