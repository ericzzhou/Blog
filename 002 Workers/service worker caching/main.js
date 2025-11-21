/**
 * https://developers.google.cn/web/fundamentals/primers/service-workers?hl=zh-cn
 * https://medium.com/jspoint/service-workers-your-first-step-towards-progressive-web-apps-pwa-e4e11d1a2e85
 */

if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    this.navigator.serviceWorker
      .register("./sw.js")
      .then(function (registration) {
        console.log("service worker注册成功,范围:", registration.scope);
      })
      .catch(function (error) {
        console.log("service workers 注册失败", error);
      });
  });
}
