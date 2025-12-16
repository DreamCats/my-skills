# Utools - Api-Reference

**Pages:** 13

---

## ubrowser 管理 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/ubrowser/manage.html

**Contents:**
- ubrowser 管理 ​
- utools.getIdleUBrowsers() ​
  - 类型定义 ​
  - 示例代码 ​
- utools.setUBrowserProxy(config) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.clearUBrowserCache() ​
  - 类型定义 ​
  - 示例代码 ​

用于管理 ubrowser 的实例对象，以及设置 ubrowser 的代理对象等。

获取所有空闲的 ubrowser 实例对象。

**Examples:**

Example 1 (unknown):
```unknown
function getIdleUBrowsers(): UBrowserInstance[];
```

Example 2 (javascript):
```javascript
const idleUBrowsers = utools.getIdleUBrowsers();
console.log(idleUBrowsers);
if (idleUBrowsers.length > 0) {
  utools.ubrowser.goto('https://www.u-tools.cn').run(idleUBrowsers[0].id)
}
```

Example 3 (unknown):
```unknown
function setUBrowserProxy(config: ProxyConfig): boolean;
```

Example 4 (unknown):
```unknown
utools.setUBrowserProxy({
  proxyRules: "http://127.0.0.1:1080",
});
```

---

## 系统 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/utools/system.html

**Contents:**
- 系统 ​
- utools.showNotification(body[, clickFeatureCode]) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.shellOpenPath(fullPath) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.shellTrashItem(fullPath) ​
  - 类型定义 ​
  - 示例代码 ​

提供一些系统级 API 的封装，也包含部分对于 uTools 底座功能的封装。

读取当前文件管理器窗口路径 (linux 不支持)，前提当前活动系统窗口是「文件管理器」

读取当前浏览器窗口路径 (linux 不支持)，前提当前活动系统窗口是浏览器

由于浏览器差异，目前仅对以下浏览器完成测试：

插件应用开发环境是指：插件应用项目在 uTools 开发者工具中接入开发打开的

**Examples:**

Example 1 (unknown):
```unknown
function showNotification(body: string, clickFeatureCode?: string): void;
```

Example 2 (unknown):
```unknown
utools.showNotification("hello test");
```

Example 3 (unknown):
```unknown
function shellOpenPath(fullPath: string): void;
```

Example 4 (unknown):
```unknown
utools.shellOpenPath("C:\\Users\\Public\\Desktop\\test.txt");
```

---

## 本地数据库 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/db/local-db.html

**Contents:**
- 本地数据库 ​
- utools.db.put(doc) / utools.db.promises.put(doc) ​
  - 类型定义 ​
    - 字段说明 ​
    - 字段说明 ​
  - 示例代码 ​
- utools.db.get(id) / utools.db.promises.get(id) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.db.remove(doc) / utools.db.promises.remove(doc) ​

uTools 提供了本地数据库的 API，基于 nosql 的设计，通过它可以实现一些简单的数据存储和读取。 它可以很方便的使用，数据存储在本地计算机系统，如果用户开启数据同步，可备份到 uTools 服务端同时可在用户的多个设备间实现秒级同步。 uTools 的插件应用是一个轻型的应用程序，在没有远端服务器提供数据存储，提供本地数据持久化存储至关重要。

在多个设备编辑同一个数据库文档时，将产生冲突，数据库会统一选择一个版本作为最终版本，为了尽可能避免冲突，应该将内容合理的分散在多个文档，而不是都存放在一个数据库文档中。

创建或更新数据库文档，文档内容不超过 1M

根据文档 ID id 获取文档，不存在则返回 null

删除数据库文档，可以通过文档对象或者文档 id 删除

筛选获取插件应用文档数组，参数为字符串则匹配文档 ID 前缀来过滤。参数为数组则查找数组内 id 对应的文档。不传参数则返回所有文档。

存储附件到新文档，附件只能被创建不能被更新，创建的附件最大不超过 10M

云端同步数据到本地的状态，该 API 是解决在某些环境下需要判断数据是否从云端复制完成。

**Examples:**

Example 1 (unknown):
```unknown
function put(doc: DbDoc): DbResult;
```

Example 2 (unknown):
```unknown
function put(doc: DbDoc): Promise<DbResult>;
```

Example 3 (unknown):
```unknown
interface DbDoc {
  _id: string;
  _rev?: string;
  [key:string]: unknown
}
```

Example 4 (unknown):
```unknown
interface DbResult {
  id: string,
  rev?: string,
  ok?: boolean,
  error?: boolean,
  name?: string,
  message?: string
}
```

---

## 用户 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/utools/user.html

**Contents:**
- 用户 ​
- utools.getUser() ​
  - 类型定义 ​
    - 字段说明 ​
  - 示例代码 ​
- utools.fetchUserServerTemporaryToken() ​
  - 类型定义 ​
    - 字段说明 ​
  - 示例代码 ​

通过用户接口，可以获取到用户的基本信息、临时 token 等。

获取当前登录的用户信息，包括头像、昵称等。

**Examples:**

Example 1 (unknown):
```unknown
function getUser(): UserInfo | null;
```

Example 2 (unknown):
```unknown
interface UserInfo {
  avatar: string;
  nickname: string;
  type: "member" | "user";
}
```

Example 3 (javascript):
```javascript
const user = utools.getUser();
if (user) {
  console.log(user);
}
```

Example 4 (unknown):
```unknown
function fetchUserServerTemporaryToken(): Promise<TempToken>;
```

---

## 事件 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/utools/events.html

**Contents:**
- 事件 ​
- utools.onPluginEnter(callback) ​
  - 类型定义 ​
    - 字段说明 ​
  - 示例代码 ​
- utools.onPluginOut(callback) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.onMainPush(callback, onSelect) ​
  - 类型定义 ​

你可以根据需要，事先传递一些回调函数给这些事件，uTools 会在对应事件被触发时调用它们。

进入插件应用时，uTools 将会主动调用这个方法。

推送内容到搜索框，并设置从推送的内容选项中打开插件应用的回调

向搜索框推送消息(需要设置 feature.mainPush 设置为 true)，详情请参考 plugin.json#feature.mainPush

当此插件应用的数据在其他设备上被更改后同步到此设备时触发

**Examples:**

Example 1 (javascript):
```javascript
function onPluginEnter(callback: (action: PluginEnterAction) => void): void;
```

Example 2 (unknown):
```unknown
interface PluginEnterAction {
  code: string;
  type: "text" | "img" | "file" | "regex" | "over" | "window";
  payload: string | MatchFile[] | MatchWindow;
  from: "main" | "panel" | "hotkey" | "reirect";
  option?: {
    mainPush: boolean;
  };
}
```

Example 3 (unknown):
```unknown
interface MatchFile {
  isFile: boolean;
  isDirectory: boolean;
  name: string;
  path: string;
}
```

Example 4 (unknown):
```unknown
interface MatchWindow {
  id: number;
  class: string;
  title: string;
  x: number;
  y: number;
  width: number;
  height: number;
  appPath: string;
  pid: number;
  app: string;
}
```

---

## 复制 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/utools/copy.html

**Contents:**
- 复制 ​
- utools.copyText(text) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.copyFile(filePath) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.copyImage(image) ​
  - 类型定义 ​
  - 示例代码 ​

获取系统剪贴板中复制的文件列表，返回一个数组，数组中的元素为文件路径。

**Examples:**

Example 1 (unknown):
```unknown
function copyText(text: string): boolean;
```

Example 2 (unknown):
```unknown
utools.copyText("Hello World!");
```

Example 3 (unknown):
```unknown
function copyFile(filePath: string | string[]): boolean;
```

Example 4 (unknown):
```unknown
utools.copyFile("C:\\Users\\Administrator\\Desktop\\test.txt");
```

---

## 屏幕 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/utools/screen.html

**Contents:**
- 屏幕 ​
- utools.screenColorPick(callback) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.screenCapture(callback) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.getPrimaryDisplay() ​
  - 类型定义 ​
  - 示例代码 ​

屏幕取色，弹出一个取色器，用户取完色执行回调函数

屏幕截图，会进入截图模式，用户截图完执行回调函数

在下列获取屏幕对象时，Display 类型定义见 Display

获取鼠标当前位置，为鼠标在系统中的绝对位置

**Examples:**

Example 1 (javascript):
```javascript
function screenColorPick(callback: (colors: { hex: string; rgb: string }) => void): void;
```

Example 2 (javascript):
```javascript
// 取色
utools.screenColorPick((colors) => {
  const { hex, rgb } = colors;
  console.log(hex, rgb);
});
```

Example 3 (javascript):
```javascript
function screenCapture(callback: (image: string) => void): void;
```

Example 4 (javascript):
```javascript
// 截图完将图片发送到「OCR 文字识别」再跳转到进行翻译
utools.screenCapture((image) => {
  utools.redirect(['OCR 文字识别', '文字识别+翻译'], image)
});
```

---

## 动态指令 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/utools/features.html

**Contents:**
- 动态指令 ​
- utools.getFeatures([codes]) ​
  - 类型定义 ​
    - 字段说明 ​
  - 示例代码 ​
- utools.setFeature(feature) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.removeFeature(code) ​
  - 类型定义 ​

很多时候，插件应用中会提供一些功能供用户进行个性化设置（例如：网页快开插件应用），这部分配置无法在 plugin.json 事先定义好，所以我们提供了以下方法对插件应用功能进行动态增减。

跳转(前往) uTools 设置界面，引导用户配置指令全局快捷键

跳转(前往) uTools 自定义 AI 模型设置界面，可引导用户自定义 AI 模型，一次配置全平台通用

**Examples:**

Example 1 (unknown):
```unknown
function getFeatures(codes?: string[]): Feature[];
```

Example 2 (unknown):
```unknown
interface Feature {
  code: string;
  explain?: string;
  icon?: string;
  platform?: string | string[];
  mainHide?: boolean;
  mainPush?: boolean;
  cmds: Cmd[];
}
```

Example 3 (javascript):
```javascript
// 获取所有动态功能
const features = utools.getFeatures();
console.log(features);
// 获取特定 code
const features = utools.getFeatures(["code-1", "code-2"]);
console.log(features);
```

Example 4 (unknown):
```unknown
function setFeature(feature: Feature): void;
```

---

## 可编程浏览器 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/ubrowser/ubrowser.html

**Contents:**
- 可编程浏览器 ​
  - ubrowser.goto(url[, headers][, timeout]) ​
    - 类型定义 ​
  - ubrowser.useragent(ua) ​
    - 类型定义 ​
  - ubrowser.viewport(width, height) ​
    - 类型定义 ​
  - ubrowser.hide() ​
    - 类型定义 ​
  - ubrowser.show() ​

uTools browser 简称 ubrowser，是根据 uTools 的特性，量身打造的一个可编程浏览器。利用 ubrowser 可以轻而易举连接一切互联网服务，且与 uTools 完美结合。

ubrowser 拥有优雅的链式调用接口，可以用口语化的数行代码，实现一系列匪夷所思的操作。例如：

打开一个 ubrowser 窗口，并跳转到指定网页

ubrowser 支持网页内容魔改，即在网页加载前对网页内容进行修改，例如添加自定义 CSS、JavaScript 等。

对网页进行截屏并保持到指定路径，将会保存成为 png 格式

清空 ubrowser 的 cookie 信息。

开始运行 ubrowser 实例，并返回执行结果

**Examples:**

Example 1 (unknown):
```unknown
function goto(
  url: string,
  headers?: Record<string, string>,
  timeout?: number
): UBrowser;
```

Example 2 (unknown):
```unknown
function useragent(ua: string): UBrowser;
```

Example 3 (unknown):
```unknown
function viewport(width: number, height: number): UBrowser;
```

Example 4 (unknown):
```unknown
function hide(): UBrowser;
```

---

## 窗口 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/utools/window.html

**Contents:**
- 窗口 ​
- utools.hideMainWindow(isRestorePreWindow) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.showMainWindow() ​
  - 类型定义 ​
  - 示例代码 ​
- utools.setExpendHeight(height) ​
  - 类型定义 ​
  - 示例代码 ​

用来实现一些跟 uTools 窗口相关的功能

执行该方法将会隐藏 uTools 主窗口，包括此时正在主窗口运行的插件应用，分离的插件应用不会被隐藏。

执行该方法将会显示 uTools 主窗口，包括此时正在主窗口运行的插件应用。

设置插件应用在主窗口中的高度，单位为像素。

设置子输入框，进入插件应用后，原本 uTools 的搜索条主输入框将会变成子输入框，子输入框可以为插件应用所使用。

跳转到另一个插件应用，并可以携带匹配指令的内容，如果插件应用不存在，则跳转到插件应用市场进行下载。

停止查找，与findInPage 配合使用

从插件中拖拽文件到其他窗口，拖拽产生一系列原生文件

获取当前窗口类型, 'main' 主窗口、'detach' 分离窗口、'browser' 由 createBrowserWindow 创建的窗口

**Examples:**

Example 1 (unknown):
```unknown
function hideMainWindow(isRestorePreWindow?: boolean): boolean;
```

Example 2 (unknown):
```unknown
utools.hideMainWindow();
```

Example 3 (unknown):
```unknown
function showMainWindow(): boolean;
```

Example 4 (unknown):
```unknown
utools.showMainWindow();
```

---

## 模板插件应用 ​

**URL:** https://www.u-tools.cn/docs/developer/information/window-exports.html

**Contents:**
- 模板插件应用 ​
- 使你的插件应用成为模板插件应用 ​
- 支持的模板 ​
  - 无 UI 模式 ​
  - 列表模式 ​
  - 文档模式 ​
- 示例项目 ​
  - 无 UI 模式 ​
  - 列表模式 ​
  - 文档模式 ​

uTools 为插件开发者提供了自由的插件设计方式，你可以使用任意的前端框架、任意的样式对插件进行开发。

但是有时候，你可能会需要更加轻量、快捷并且符合 uTools 官方设计规范的插件，你的插件可能只需要较为简单的交互逻辑，亦或者你不是一个前端开发者，你希望使用一个现成的模板来快速开发。

uTools 提供了模板插件应用，你可以使用模板插件来快速开发你的插件。

uTools 的模板插件提供了以下的优势：

当你使用模板插件应用时，将无法同时启用自定义的插件界面，但是你可以将多个插件界面同时启用，所以根据你真实的需求进行选择。

通过将 mode 设置为 none，即可开启无 UI 模式。

无 UI 模式下，插件将不会显示插件界面，你可以用来实现一些对用户无干扰的交互逻辑。

通过设置 args.enter 字段来设置对应的功能指令入口。

通过将 mode 设置为 list，即可开启列表模式。

列表模式下，插件将显示一个列表界面，你可以通过列表来选择一个选项，然后执行对应的交互逻辑。

通过设置 args.enter 字段来设置对应的功能指令入口。

通过设置 args.placeholder + args.search 字段来支持搜索功能，其中 args.placeholder 字段是搜索框的提示文字。

通过设置 args.select 字段来支持选择功能。

通过将 mode 设置为 doc，即可开启文档模式。

文档模式下，插件将显示一个文档列表界面，你可以通过切换列表项来查看对应的文档内容。

通过设置 args.indexes 字段，传递一个索引数组，用于指定显示的文档列表。

文档模式下，默认启动了文档搜索功能，但是你可以通过设置 args.placeholder 字段来修改搜索框的提示文字，默认为 搜索。

**Examples:**

Example 1 (unknown):
```unknown
{
  "main": "index.html", ,
  "preload": "preload.js", 
  "logo": "logo.png",
  "features": [
    {
      "code": "hello",
      "explain": "hello world",
      "icon": "icon.png",
      "cmds": ["hello"]
    }
  ]
}
```

Example 2 (javascript):
```javascript
window.exports = {
  // 这里的hello与plugin.json中的code一致
  hello: {
    mode: "none", // 无UI模式
    args: {
      // 插件执行入口
      enter: () => {
        utools.showNotification("hello world");
      },
    },
  },
};
```

Example 3 (javascript):
```javascript
window.exports = {
  // 这里的hello与plugin.json中的code一致
  hello: {
    mode: "none", // 无UI模式
    args: {
      // 插件执行入口
      enter: () => {
        utools.showNotification("hello world");
      },
    },
  },
};
```

Example 4 (javascript):
```javascript
window.exports = {
  "features.code": {
    // 注意：键对应的是 plugin.json 中的 features.code
    mode: "list", // 列表模式
    args: {
      // 进入插件应用时调用（可选）
      enter: (action, callbackSetList) => {
        // 如果进入插件应用就要显示列表数据
        callbackSetList([
          {
            title: "这是标题",
            description: "这是描述",
            icon: "", // 图标(可选)
          },
        ]);
      },
      // 子输入框内容变化时被调用 可选 (未设置则无搜索)
      search: (action, searchWord, callbackSetList) => {
        // 获取一些数据
        // 执行 callbackSetList 显示出来
        callbackSetList([
          {
            title: "这是标题",
            description: "这是描述",
            icon: "", // 图标
            url: "https://yuanliao.info",
          },
        ]);
      },
      // 用户选择列表中某个条目时被调用
      select: (action, itemData, callbackSetList) => {
        window.utools.hideMainWindow();
        const url = itemData.url;
        require("electron").shell.openExternal(url);
        window.utools.outPlugin();
      },
      // 子输入框为空时的占位符，默认为字符串"搜索"
      placeholder: "搜索",
    },
  },
};
```

---

## 输入 ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/utools/input.html

**Contents:**
- 输入 ​
- utools.hideMainWindowPasteFile(filePath) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.hideMainWindowPasteImage(image) ​
  - 类型定义 ​
  - 示例代码 ​
- utools.hideMainWindowPasteText(text) ​
  - 类型定义 ​
  - 示例代码 ​

对外部应用进行一些输入操作，粘贴文本、粘贴图像、粘贴文件。

输入文本，与输入法原理类似，可以输入任意字符串

**Examples:**

Example 1 (unknown):
```unknown
function hideMainWindowPasteFile(filePath: string | string[]): boolean;
```

Example 2 (unknown):
```unknown
utools.hideMainWindowPasteFile("C:\\Users\\Administrator\\Desktop\\test.txt");
```

Example 3 (unknown):
```unknown
function hideMainWindowPasteImage(image: string | Uint8Array): boolean;
```

Example 4 (unknown):
```unknown
// base64
utools.hideMainWindowPasteImage("data:image/png;base64,......");
// 路径
utools.hideMainWindowPasteImage("/path/to/test.png");
```

---

## AI ​

**URL:** https://www.u-tools.cn/docs/developer/api-reference/utools/ai.html

**Contents:**
- AI ​
- utools.ai(option[, streamCallback]) ​
  - 类型定义 ​
    - AiOption 字段说明 ​
    - Message 字段说明 ​
    - Tool 字段说明 ​
    - PromiseLike 字段说明 ​
  - 示例代码 ​
    - AI 对话 ​
    - Function Calling 调用 ​

调用 AI 能力，支持 Function Calling

PromiseLike 是 Promise 的扩展类型，包含 abort() 函数

默认情况下，你可以单纯把它当作 Promise 来使用，但是扩展了 abort() 函数，可以让你在调用 AI 过程中，执行 abort() 中止调用。

Function Calling 功能调用的函数必须挂到 window 对象上，例如：window.getSystemInfo

**Examples:**

Example 1 (javascript):
```javascript
function ai(
  option: AiOption,
  streamCallback: (chunk: Message) => void
): PromiseLike<void>; // 版本：>=7.0.0
```

Example 2 (unknown):
```unknown
function ai(option: AiOption): PromiseLike<Message>; // 版本：>=7.0.0
```

Example 3 (unknown):
```unknown
interface AiOption {
  model?: string;
  messages: Message[];
  tools?: Tool[];
}
```

Example 4 (unknown):
```unknown
interface Message {
  role: "system" | "user" | "assistant";
  content?: string;
  reasoning_content?: string;
}
```

---
