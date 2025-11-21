/**
 * https://medium.com/jspoint/achieving-parallelism-in-javascript-using-web-workers-8f921f2d26db
 * web worker是最通用的worker类型。
 * 与service worker和worklet不同，它们没有特定的用例，除了可以与页面线程分开运行之外。
 * 因此，Web Worker可以用于从页面线程分流几乎所有繁重的处理。
 * https://www.jianshu.com/p/e2cdc78ff47c
 * https://www.jianshu.com/p/65ddf1477eb7
 */

//相对于 当前文件的 url 路径解析

/**
 *  在这里，浏览器将尝试worker.js相对于创建它的页面的当前路径进行解析。
 *  如果您在http://localhost，那么它将获取http://localhost/worker.js。
 *  如果你在，http://localhost/app那么它会 fetch http://localhost/app/worker.js。
 *  为避免此问题，您可以在外部 JavaScript 文件中实现它。
 */

var workerFor = new Worker("./workers/for.js");

workerFor.addEventListener("message", function (event) {
  console.log("从 service workder 收到消息：", event.data);

  var div = document.getElementById("result");
  div.innerHTML = "message received => " + event.data;
});

// 监听
workerFor.addEventListener("error", function (event) {
  console.error("error received from workerFor => ", JSON.stringify(event));
});

// index.js 向 service workers 发送消息示例
// 页面按钮点击后
// 从 web worker 加载结果
function loadResult() {
  // 添加加载文本直到 `message` 事件监听器替换它
  var div = document.getElementById("result");
  div.innerHTML = "加载中2...";
  // 向worker发出消息事件
  workerFor.postMessage("btnClick"); // 这里我们不需要有效载荷
}
