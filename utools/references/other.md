# Utools - Other

**Pages:** 12

---

## 团队应用 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/team.html

**Contents:**
- 团队应用 ​
- utools.team.info() ​
  - 类型定义 ​
    - 字段说明 ​
  - 示例代码 ​
- utools.team.preset(key) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.team.allPresets([keyStartsWith]) ​
  - 类型定义 ​

提供团队版插件相关的接口，用来获取团队版管理配置的信息。

团队应用 API 需要配合团队管理后台使用，请在团队后台创建对应应用后可以使用。（暂未开放第三方应用）

获取对应的团队配置，获取的配置需要在团队版，返回的数据为一个 JSON 对象

获取当前团队下发的所有配置，支持接收一个 key 前缀或者 keys 来过滤

**Examples:**

Example 1 (unknown):
```unknown
function info(): TeamInfo;
```

Example 2 (unknown):
```unknown
interface TeamInfo {
  teamId: string;
  teamName: string;
  teamLogo: string;
  userId: string;
  userName: string;
  userAvatar: string;
}
```

Example 3 (javascript):
```javascript
const { teamName } = utools.team.info();

console.log(`当前团队为：${teamName}`);
```

Example 4 (unknown):
```unknown
function preset<T>(key: string): T | null;
```

---

## 服务端 API ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/server.html

**Contents:**
- 服务端 API ​
- 公共定义 ​
  - 返回状态码 ​
- 获取用户基础信息 ​
  - 接口定义 ​
  - 请求参数 ​
  - 响应数据 ​
  - 调用步骤 ​
- 支付订单查询接口 ​
  - 接口定义 ​

通过 uTools 的服务端 API，可以将你的应用和 uTools 用户关联，实现帐号互通、接收支付通知、查询用户支付记录等，为保护密钥安全，请仅在服务端调用接口。

此接口用于获取 uTools 用户的基础信息、验证用户真实性，与第三方系统进行帐号打通，实现系统间免登录跳转等。

在客户端获取用户登录凭证 access_token，通过utools.fetchUserServerTemporaryToken获取

此接口用于动态创建商品，主要解决不固定金额商品问题，一般为一次性使用，通过此 API 创建的商品不会出现在开发者工具的商品列表中

当用户通过 uTools 在你的插件应用内完成支付，且在开发者工具中配置了回调地址，在收到付款时，会将信息推送到配置的回调地址。

此处的接口定义指的是开发者工具中配置的回调地址，将会以 POST 方式推送数据到开发者工具中配置的回调地址。

此处的请求参数指的是将对开发者工具中配置的回调地址发起 POST 请求时，会被携带的参数。

**Examples:**

Example 1 (unknown):
```unknown
GET https://open.u-tools.cn/baseinfo
Accept: application/json
```

Example 2 (unknown):
```unknown
{
  "resource": {
    "avatar": "https://res.u-tools.cn/assets/avatars/eZCBIawAkspLw8Xg.png",
    "member": 1, // 是否 uTools 会员（0: 否，1: 是）
    "nickname": "却步.",
    "open_id": "00a50cd81c37c4e381e8161b2d762158", // uTools 用户 ID, 对于此插件应用不变且唯一
    "timestamp": 1624329616
  },
  "sign": "4dbf21a9d5a0f0e3906a0180522fd6393b4e91f738d57cafddf309afc6c547bb" // 签名算法与 1.3 相同
}
```

Example 3 (unknown):
```unknown
{
  "message": "The given data was invalid.", // message 字段始终存在
  "errors": {
    // 可能没有详细错误信息
    "access_token": ["access token 必须是 32 个字符。"]
  }
}
```

Example 4 (javascript):
```javascript
$params = [
  "plugin_id" => "zueadppw", // 可在开发者插件应用中获得
  "access_token" => "user access_token 32位",
  "timestamp" => "1624329435",
];
// 1. 按照键名对数组进行升序排序
ksort($params);
// 2. 生成 URL-encode 之后的请求字符串
$str = http_build_query($params);
// 3. 使用 HMAC 方法生成带有密钥的哈希值
$secret = "your secret 32位"; // secret 在开发者插件应用中通过重置获取
$sign = hash_hmac("sha256", $str, $secret);
```

---

## 用户付费 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/payment.html

**Contents:**
- 用户付费 ​
- utools.isPurchasedUser() ​
  - 类型定义 ​
  - 示例代码 ​
- utools.openPurchase(options, callback) ​
  - 类型定义 ​
    - 字段说明 ​
  - 示例代码 ​
- utools.openPayment(options, callback) ​
  - 类型定义 ​

软件付费指的是，用户按天数购买授权，在授权生效期内，可以使用对应的插件应用功能

服务付费指的是，用户按使用量购买应用服务，在购买后，可以在固定的次数或者数量下，使用应用服务。

**Examples:**

Example 1 (unknown):
```unknown
function isPurchasedUser(): boolean | string
```

Example 2 (javascript):
```javascript
utools.onPluginEnter(({ type, code, payload }) => {
  const purchasedUser = utools.isPurchasedUser();
  if (purchasedUser) {
    // 已付费的合法用户，可使用插件应用完整功能
    // purchasedUser === true 永久授权(付费买断)
    // purchasedUser === "yyyy-mm-dd hh:mm:ss", 授权到期时间
  } else {
    // 打开付费
    utools.openPurchase({ goodsId: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" }, () => {
      console.log("付费成功");
    });
  }
});
```

Example 3 (javascript):
```javascript
function openPurchase(options: OpenPurchaseOptions, callback?: () => void): void
```

Example 4 (unknown):
```unknown
interface OpenPurchaseOptions {
  goodsId: string;
  outOrderId?: string;
  attach?: string;
}
```

---

## 打包为离线安装包 ​

**URL:** https://www.u-tools.cn/docs/developer/basic/offline-plugin.html

**Contents:**
- 打包为离线安装包 ​
- 离线安装包 ​

当你的插件开发完成后，你可以选择将其打包成离线插件安装包（UPXS）。

这种方式下的插件应用，无需通过审核即可分享给其他人使用，不过在安装时会被 uTools 弹出安全提示，需要用户确认安装。

离线插件应用安装更多用于方便测试或者自己内部分享或使用，而不是用于发布。

若想要更多人使用你的插件应用，请参考 发布插件应用。

通过 uTools 开发者工具插件，点击 打包 按钮

点击后，会弹出 打包 窗口，填写版本信息后，点击 确认 按钮后，在弹出的文件保存窗口选择保存路径即可完成打包。

插件应用打包与发布时，都需要填写对应的版本号，这两个版本号并没有关联。

版本号遵守 semver 部分规范 ，在修改过程中要注意确认。

---

## 发布到应用市场 ​

**URL:** https://www.u-tools.cn/docs/developer/basic/publish-plugin.html

**Contents:**
- 发布到应用市场 ​
- 发布前的准备 ​
- 发布流程 ​
- 查看审核结果 ​
- 微信公众号 ​

当你的插件应用完成开发，并且完成测试没有问题之后，就可以发布到插件应用市场了。

发布到市场能让你的插件应用被更多用户使用，也可以强化 uTools 的生态。

插件应用发布时，请尽量提供足够详细的用户使用手册，这将会降低你的插件应用使用门槛。

插件应用的功能尽量简洁，易上手会让你的插件应用变得更受欢迎。

而更加详细的用户手册，会让你的插件应用在功能定位上减少歧义，并大大的提升用户体验。

通过开发者工具，在插件信息页面切换标签到 发布历史 ，即可看到当前插件的审核结果。

当显示 审核通过 后，代表你的插件已经进入插件应用市场，你可以通过插件应用市场的 最新上架 或 最近更新 专栏查看到你的插件。

uTools 通过微信公众号推送用户信息，开发者也可以通过关注微信公众号获取审核信息。

关注 uTools 公众号，可以直接在微信搜索 uTools，也可以通过二维码关注。

---

## 发布到团队内部 ​

**URL:** https://www.u-tools.cn/docs/developer/basic/team-plugin.html

**Contents:**
- 发布到团队内部 ​
- 发布前的准备 ​
  - 注册团队账号 ​
  - 创建团队 ​
  - 邀请团队成员 ​
- 创建团队应用 ​
- 发布插件 ​
- 管理员审核 ​
- 查看审核结果 ​

当你的插件应用仅针对团队内部使用时，你可以将插件发布到团队内部，这样只有团队成员才能使用插件应用。

与发布到市场一样，你需要准备插件应用信息、版本信息、插件应用的截图、检查代码是否符合规范。

访问 uTools 团队版 后，填写手机号，获取验证码，点击 开始使用 即可完成注册。

注册完成后，自动跳转至团队管理后台，点击 创建团队 按钮，填写团队名称、团队 logo，点击 创建团队 即可完成团队创建。

创建团队后，可以进入团队管理后台，切换到 成员管理 页面，点击 邀请成员 按钮，可以获取团队邀请链接，将链接发送给团队成员，团队成员点击链接即可完成加入团队。

在 uTools 开发者工具中创建应用时在 插件应用所属团队 选择团队。

通过团队进行发布的插件应用不会进入官方插件应用市场，而是进入团队内部插件应用市场。因此，该插件的审核权限由团队管理员进行审核。

管理员通过登录团队管理后台，在 应用审核 页面，即可看到当前团队插件的 待审核 状态。

管理员通过点击 通过 按钮，填写审核意见，即可将插件发布到团队内部插件应用市场。

被管理员审核通过后，团队成员即可在 团队应用 页面看到该插件。

团队插件查看审核结果与市场插件一致，通过开发者工具，在插件信息页面切换标签到 发布历史 ，即可看到当前插件的审核结果。

---

## dbCryptoStorage ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/db/db-crypto-storage.html

**Contents:**
- dbCryptoStorage ​
- utools.dbCryptoStorage.setItem(key, value) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.dbCryptoStorage.getItem(key) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.dbCryptoStorage.removeItem(key) ​
  - 类型定义 ​
  - 示例代码 ​

dbCryptoStorage 是基于 本地数据库 基础上，封装的一套类似 LocalStorage 的 API，通过键值对形式加密存储数据。

存储一个键值对数据，若键已存在，则覆盖它的值。

**Examples:**

Example 1 (unknown):
```unknown
function setItem(key: string, value: any): void;
```

Example 2 (unknown):
```unknown
utools.dbCryptoStorage.setItem("key", "value will encrypt");
```

Example 3 (unknown):
```unknown
function getItem(key: string): any;
```

Example 4 (javascript):
```javascript
const value = utools.dbCryptoStorage.getItem("key");
console.log(value);
```

---

## 调试插件应用 ​

**URL:** https://www.u-tools.cn/docs/developer/basic/debug-plugin.html

**Contents:**
- 调试插件应用 ​
- 每次进入插件应用加载最新代码 ​
- 使用开发者调试工具 ​
- 进阶(代码热更新) ​
  - Vite ​
  - Webpack ​

在项目的应用开发界面，点击右上角设置图标弹出的菜单中选择开启 退出到后台立即结束运行

进入开发中的插件应用后，点击右上角应用 Logo - 点击 开发者工具 或者按快捷键 Ctrl + Shift + I 打开

在开发模式下，入口文件是支持 URL 协议的，可配合 Vite、Webpack 等工具，在开发阶段进行热更新。

Vite 默认为各种框架提供了热更新的集成，所以只需要默认启动项目既可使用。

preload.js 代码变更后无法自动热更新，在应用开发点击设置开启 退出到后台立即结束运行

**Examples:**

Example 1 (unknown):
```unknown
npm run dev
```

Example 2 (unknown):
```unknown
{
  "development": {
    "main": "http://127.0.0.1:5173/index.html"
  }
}
```

Example 3 (unknown):
```unknown
npm install webpack-dev-server --save-dev
```

Example 4 (unknown):
```unknown
if (module.hot) {
    module.hot.accept();
}
```

---

## dbStorage ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/db/db-storage.html

**Contents:**
- dbStorage ​
- utools.dbStorage.setItem(key, value) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.dbStorage.getItem(key) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.dbStorage.removeItem(key) ​
  - 类型定义 ​
  - 示例代码 ​

dbStorage 是基于 本地数据库 基础上，封装的一套类似 LocalStorage 的 API，通过键值对形式存储数据，可以快速存取数据。

存储一个键值对数据，若键已存在，则覆盖它的值。

**Examples:**

Example 1 (unknown):
```unknown
function setItem(key: string, value: any): void;
```

Example 2 (unknown):
```unknown
utools.dbStorage.setItem("key", "value");
```

Example 3 (unknown):
```unknown
function getItem(key: string): any;
```

Example 4 (javascript):
```javascript
const value = utools.dbStorage.getItem("key");
console.log(value);
```

---

## 第一个插件应用 ​

**URL:** https://www.u-tools.cn/docs/developer/basic/first-plugin.html

**Contents:**
- 第一个插件应用 ​
  - 打开 uTools 开发者工具 ​
  - 新建项目 ​
  - 创建工程文件夹 ​
  - 工程文件夹下的文件 ​
- 开始编写插件应用 ​
- 接入开发 ​

点击开发者工具左下侧 新建项目 按钮，即可弹出新建项目相关的配置界面。

勾选 "同意 uTools 开发者协议" ，点击右下角的确定，完成创建。

文件夹的名字可以是任意的，但是我们尽量保证跟插件应用有一定关联性以及尽量使用英文。 比如你的第一个插件应用名字可能是“第一个插件”，文件夹名字可以是“my-first-plugin”。

在工程文件夹下，将会存放许多文件，有些文件是必不可少的，请参考官方推荐的文件目录结构。

我们应该先把 logo 文件以及页面对应的 html 入口文件放入工程文件夹下，然后添加必不可少的plugin.json 文件。

关于 plugin.json 更多信息，请查看 配置文件介绍。

要让你的插件应用展示任何内容，必须借助刚刚提前创建好的 “index.html” 文件，因为 uTools 插件应用本身借助了 Web 网页的界面来实现了界面的绘制，这对有 Web 开发经验的开发者来说，是相对简单易上手的方式。

现在，为你的插件应用输出最基础的内容，一行 hello world 。

在深入编写插件应用的过程中，你可能会慢慢运用到 uTools 提供的各种 api，比如：

或者你需要自己定制更强大的系统交互能力，那么可以考虑为你的项目加入 preload.js，并尝试在其中使用 nodejs api。

将项目与创建的工程文件夹关联，需要选择 plugin.json 配置文件。

点击项目的应用开发界面的 选择工程「plugin.json」文件夹 ，选择工程文件夹下的 plugin.json 配置文件

选择工程文件夹下的 plugin.json 文件后，开发者工具就会根据此文件，访问相对路径下的资源，比如 logo 、 main、preload。

此时点击 接入开发，工程文件夹将被识别为开发中的插件应用接入 uTools。

很好🎉🎉🎉，现在你可以看到你的插件应用的界面了。

**Examples:**

Example 1 (unknown):
```unknown
{
  "logo": "logo.png",
  "main": "index.html",
  "features": [
    {
      "code": "test",
      "cmds": [
        "第一个插件"
      ],
      "explain": "第一个插件"
    }
  ]
}
```

Example 2 (unknown):
```unknown
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>我的第一个插件应用</title>
</head>
<body>
  <h1>Hello World</h1>
</body>
</html>
```

---

## FFmpeg ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/utools/ffmpeg.html

**Contents:**
- FFmpeg ​
- utools.runFFmpeg(args[, onProgress]) ​
  - 类型定义 ​
    - PromiseLike 字段说明 ​
    - RunProgress 字段说明 ​
  - 示例代码 ​

FFmpeg 是一款功能强大的开源音视频处理工具，将其以独立扩展的方式集成到 uTools。(首次调用 FFmpeg 会引导用户下载集成)

运行 FFmpeg (首次调用将引导用户下载集成)

PromiseLike 是 Promise 的扩展类型，包含 kill() 和 quit() 函数

默认情况下，你可以单纯把它当作 Promise 来使用，但是扩展了 kill() 和 quit() 函数，可以让你在运行过程中强制结束 FFmpeg 运行，或者通知 FFmpeg 退出。

**Examples:**

Example 1 (javascript):
```javascript
function runFFmpeg(args: string[], onProgress?: (progress: RunProgress) => void): PromiseLike<void>; // 版本：>=6.1.0
```

Example 2 (unknown):
```unknown
interface PromiseLike extends Promise<void> {
  kill(): void;
  quit(): void;
}
```

Example 3 (unknown):
```unknown
interface RunProgress {
  bitrate: string;
  fps: number;
  frame: number;
  percent?: number;
  q: number | string;
  size: string;
  speed: string;
  time: string;
}
```

Example 4 (javascript):
```javascript
// 视频压缩
utools.runFFmpeg(
  ["-i", "/path/to/input.mp4", "-c:v", "libx264", "-tag:v", "avc1-movflags", "faststart", "-crf", "30", "-preset", "superfast", "pathto/output.mp4"],
  (progress) => {
    console.log("压缩中 " + progress.percent + "%");
  }
).then(() => {
  console.log("压缩完成");
}).catch((error) => {
  console.log("出错了：" + error.message);
});
```

---

## 模拟按键 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/utools/simulate.html

**Contents:**
- 模拟按键 ​
- utools.simulateKeyboardTap(key[, ...modifiers]) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.simulateMouseMove(x, y) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.simulateMouseClick(x, y) ​
  - 类型定义 ​
  - 示例代码 ​

**Examples:**

Example 1 (unknown):
```unknown
function simulateKeyboardTap(key: string, ...modifiers: string[]): void;
```

Example 2 (unknown):
```unknown
// 模拟键盘敲击 Enter
utools.simulateKeyboardTap("enter");
// windows linux 模拟粘贴
utools.simulateKeyboardTap("v", "ctrl");
// macOS 模拟粘贴
utools.simulateKeyboardTap("v", "command");
// 模拟 Ctrl + Alt + A
utools.simulateKeyboardTap("a", "ctrl", "alt");
```

Example 3 (unknown):
```unknown
function simulateMouseMove(x: number, y: number): void;
```

Example 4 (unknown):
```unknown
// 将鼠标移动到屏幕左上角
utools.simulateMouseMove(50, 50);
```

---
