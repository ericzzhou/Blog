/**
 * https://medium.com/jspoint/service-workers-your-first-step-towards-progressive-web-apps-pwa-e4e11d1a2e85
 */

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("./sw.js");

  //navigator.serviceWorker.ready always resolve
  navigator.serviceWorker.ready
    .then((registration) => {
      console.log(
        "Service worker successfully registered on scope",
        registration.scope
      );
      console.log(registration);
    })
    .catch((error) => {
      console.log("Service worker failed to register");
    });
}
