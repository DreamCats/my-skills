# Utools - Information

**Pages:** 6

---

## 使用 uTools API 提示 ​

**URL:** https://www.u-tools.cn/docs/developer/information/tools/typescript.html

**Contents:**
- 使用 uTools API 提示 ​
- utools-api-types ​
  - 安装 ​
  - 配置 tsconfig ​

当你需要在项目中使用 TypeScript 时，一般会遇到无法正常使用 utools 的 API 的情况。

因此 uTools 官方推出了完整的类型定义文件，这份类型文件完整的列举了目前 utools 对象下所有的 API，并会根据版本的迭代同步更新。

utools-api-types 是官方开源的一个 TypeScript 类型定义代码库，你可以直接访问 https://github.com/uTools-Labs/utools-api-types 进行查看相关信息。

当然，若要使用到项目中，可以通过 npm 进行安装，并通过简单的配置启用。

**Examples:**

Example 1 (unknown):
```unknown
npm install utools-api-types --save-dev
```

Example 2 (unknown):
```unknown
{
  "compilerOptions": {
    "types": ["utools-api-types"]
  },
  "includes": [
    // 如果使用ts或者框架，请添加需要类型提示的文件范围
    // 案例：
    // src/**/*.ts
    // preload.js
  ]
}
```

---

## 使用 Node.js ​

**URL:** https://www.u-tools.cn/docs/developer/information/preload-js/nodejs.html

**Contents:**
- 使用 Node.js ​
- 引入 Node.js 原生模块 ​
- 引入自己编写的模块 ​
- 引入第三方模块 ​
  - 通过 npm 安装 ​
  - 通过源码引入 ​
- 引入 Electron 渲染进程 API ​

preload js 文件遵循 CommonJS 规范，通过 require 引入 Node.js (16.x 版本) 模块

可以引入 Node.js 所有原生模块，开发者自己编写的 Node.js 模块以及第三方 Node.js 模块。

在 preload.js 同级目录下，保证存在一个独立的 package.json，并且设置 type 为 commons。

在 preload.js 同级目录下，执行 npm install 安装第三方模块，保证 node_modules 目录存在。

以下是通过 npm 引入 colord 的示例:

在 preload.js 同级目录下，下载源码，并使用 require 引入。

比如从 github 下载 nodemailer：

**Examples:**

Example 1 (javascript):
```javascript
const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");
const { execSync } = require("node:child_process");

window.services = {
  readFile: (filename) => {
    return fs.readFileSync(filename, { encoding: "utf-8" });
  },
  getFolder: (filepath) => {
    return path.dirname(filepath);
  },
  getOSInfo: () => {
    return { arch: os.arch(), cpus: os.cpus(), release: os.release() };
  },
  execCommand: (command) => {
    execSync(command);
  },
};
```

Example 2 (javascript):
```javascript
const writeText = require("./libs/writeText.js");

window.services = {
  writeText,
};
```

Example 3 (javascript):
```javascript
const fs = require("fs");
const path = require("path");

module.exports = function writeText(text, filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(filePath, text);
    return true;
  }
  return false;
};
```

Example 4 (unknown):
```unknown
{
  "type": "commonjs"
  "dependencies": {}
}
```

---

## plugin.json 配置提示 ​

**URL:** https://www.u-tools.cn/docs/developer/information/tools/jsonschema.html

**Contents:**
- plugin.json 配置提示 ​
- 如何使用 ​
  - 远程地址 ​
  - 本地访问 ​
  - 跟随 utools-api-type 安装 ​

在进行 uTools 的插件开发时， plugin.json 文件是必不可少的。

但是 plugin.json 目前只能使用 JSON 文件进行编写，而插件配置的字段比较繁多且复杂，所以配置时，需要经常翻看文档，容易造成开发流程的不通畅。

为了提高开发效率，uTools 官方开源了 plugin.json 相关的 JSONSchema 文件。

关于 JSONSchema，请参考 https://json-schema.org/

JSONSchema 通常作为 JSON 文件一种默认支持的协议文件，支持多种加载方式，同时支持远程加载跟本地加载。

当你网络足够友好，能够直接访问 GitHub 时，可以通过直接在 plugin.json 中加入以下代码实现。

一般情况下，为了能够正常访问，我们可以考虑将 JSONSchema 文件下载到项目文件夹内，并通过相对路径（相对于 plugin.json 文件）进行访问。

我们假设 plugin.json 目前位于项目的 public 文件夹下，而 JSONScchema 位于项目的 resource 文件夹下，则编写如下代码

目前，JSONSchema 并没有被单独开源，而是跟随 utools-api-type 一同开源，因此当你安装过 utools-api-type 时，可以直接在项目中访问 JSONSchema 。

我们假设 plugin.json 目前位于项目的 public 文件夹下，而 JSONScchema 位于项目的 resource 文件夹下，则编写如下代码

**Examples:**

Example 1 (unknown):
```unknown
{
  "$schema": "https://raw.githubusercontent.com/uTools-Labs/utools-api-types/refs/heads/main/resource/utools.schema.json"
}
```

Example 2 (unknown):
```unknown
{
  "$schema": "../resource/utools.schema.json"
}
```

Example 3 (unknown):
```unknown
{
  "$schema": "../node_modules/utools-api-types/resource/utools.schema.json"
}
```

---

## 插件应用目录结构 ​

**URL:** https://www.u-tools.cn/docs/developer/information/file-structure.html

**Contents:**
- 插件应用目录结构 ​
- 源码编译 ​
- 第三方依赖 ​

此部分会帮助你了解，通常情况下，一个插件应用的文件目录结构。

插件应用至少要有一个 plugin.json 作为入口，并配置 logo 字段以及 main 或者 preload 字段。

一个相对完整可打包成插件应用的目录可能是这样的：

uTools 仅识别 html + css + javascript, 通常我们在开发过程中可能会使用各种的工具来辅助开发，比如 vite、webpack 等等，也可能会引入各种前端框架，比如 vue、react、svelte 等等，而这些代码并不是直接可以被 uTools 识别的，当我们打包插件应用前应该先将框架代码编译成普通的 html 、css、js 文件。通常是将源码编译输出到 dist 文件夹，然后将 dist 文件夹打包成插件应用，切勿将整个项目的根目录打包成插件应用。

当你使用第三方依赖时，根据项目情况进行区分：

当你使用前端依赖时，只需要在项目的根目录下安装即可，对前端项目进行正常的编译，输出到 dist 文件夹。

当你使用 nodejs 的第三方依赖时，应当保证你的模块存在于 preload.js 同级目录，并且不要对它们进行编译操作，保证提交插件应用时的目录结构不变，并且源码清晰可读。

**Examples:**

Example 1 (unknown):
```unknown
/{plugin}
|-- plugin.json
|-- preload.js
|-- index.html
|-- index.js
|-- index.css
|-- logo.png
```

---

## plugin.json 配置 ​

**URL:** https://www.u-tools.cn/docs/developer/information/plugin-json.html

**Contents:**
- plugin.json 配置 ​
- 配置文件格式 ​
- 基础字段说明 ​
  - main ​
  - logo ​
  - preload ​
- 开发模式字段说明 ​
  - development ​
  - development.main ​
- 插件应用设置字段说明 ​

plugin.json 文件是插件应用的配置文件，它是最重要的一个文件，用来定义这个插件应用将如何与 uTools 集成。 每当你创建一个插件应用时，都需要从创建一个 plugin.json 文件开始。

plugin.json 文件是一个标准的 JSON 文件，它的结构如下：

必填：main 与 preload 至少存在一个

必须是一个相对于 plugin.json的相对路径，且只能是一个 .html 文件。

插件应用 Logo，必须为 png 或 jpg 文件

必填：main 与 preload 至少存在一个

预加载 js 文件，这是一个关键文件，你可以在此文件内调用 nodejs、 electron 提供的 api。查看更多关于 preload.js

开发模式下的配置，对象的同名字段会会覆盖基础配置字段。

开发模式下，插件应用的入口文件，与基础配置字段 main 字段相同，但是此处可以配置为一个 http 协议的地址（不推荐）。

支持 http 协议的地址，是为了方便开发者配合前端框架或者各种构建工具的使用，请勿将基础字段 main 字段配置为 http 协议的地址。

插件应用设置，可以配置一些插件在基座中的默认行为或者样式。

是否单例，默认为 true，表示插件在基座中只能存在一个应用实例。

插件应用初始高度。可以通过 utools.setExpendHeight 动态修改。

features 定义插件应用的指令集合，一个插件应用可定义多个功能，一个功能可配置多条指令。

features 的每个元素都是一个 feature 对象，对象中包含以下字段：

功能编码，此字段的值必须唯一。进入插件应用会将该编码带入，根据不同编码实现功能区分执行

类型：Array<string>|string

指定功能可用平台，可设置的值是 ["win32","darwin","linux"] 分别对应 Windows、macOS、Linux 平台

若配置为true，打开此功能不主动显示搜索框。

类型：Array<string|object>

配置该功能的指令集合，指令分「功能指令」和「匹配指令」

搜索框输入任意文本或粘贴图片、文件(夹)匹配出可处理它的指令

正则表达式存如果在斜杠 "" 需要多加一个，"\"

**Examples:**

Example 1 (unknown):
```unknown
{
  "main": "index.html",
  "logo": "logo.png",
  "preload": "preload.js",
  "features": [
    {
      "code": "hello",
      "explain": "hello world",
      "cmds": ["hello", "你好"]
    }
  ]
}
```

Example 2 (unknown):
```unknown
{
  "features": [
    {
      "code": "text",
      "cmds": ["测试", "你好"]
    }
  ]
}
```

Example 3 (unknown):
```unknown
{
  "features": [
    {
      "code": "regex",
      "cmds": [
        {
          // 类型标记（必须）
          "type": "regex",
          // 指令名称（必须）
          "label": "打开网址",
          // 正则表达式字符串
          // 注意: 正则表达式存如果在斜杠 "\" 需要多加一个，"\\"
          // 注意：“任意匹配的正则” 会被 uTools 忽视，例如：/.*/ 、/(.)+/、/[\s\S]*/ ...
          "match": "/^https?:\\/\\/[^\\s/$.?#]\\S+$|^[a-z0-9][-a-z0-9]{0,62}(\\.[a-z0-9][-a-z0-9]{0,62}){1,10}(:[0-9]{1,5})?$/i",
          // 最少字符数 (可选)
          "minLength": 1,
          // 最多字符数 (可选)
          "maxLength": 1000
        }
      ]
    }
  ]
}
```

Example 4 (unknown):
```unknown
{
  "features": [
    {
      "code": "over",
      "cmds": [
        {
          // 类型标记（必须）
          "type": "over",
          // 指令名称（必须）
          "label": "百度一下",
          // 排除的正则表达式字符串 (任意文本中排除的部分) (可选)
          "exclude": "/\\n/",
          // 最少字符数 (可选)
          "minLength": 1,
          // 最多字符数 (默认最多为 10000) (可选)
          "maxLength": 500
        }
      ]
    }
  ]
}
```

---

## 认识 preload ​

**URL:** https://www.u-tools.cn/docs/developer/information/preload-js/preload-js.html

**Contents:**
- 认识 preload ​
- 为什么需要 preload ​
- preload 的定义 ​
- 前端使用 preload ​
- preload js 规范 ​

当你在 plugin.json 文件配置了 preload 字段，指定的 js 文件将被预加载，该 js 文件可以调用 Node.js API 的本地原生能力和 Electron 渲染进程 API。

在传统的 web 开发中，为了保持用户运行环境的安全，JavaScript 被做了很强的沙箱限制，比如不能访问本地文件，不能访问跨域网络资源，不能访问本地存储等。

uTools 基于 Electron 构建，通过 preload 机制，在渲染线程中，释放了沙箱限制，使得用户可以通过调用 Node.js 的 API 来访问本地文件、跨域网络资源、本地存储等。

preload 是完全独立于前端项目的一个特殊文件，它应当与 plugin.json 位于同一目录或其子目录下，保证可以在打包插件应用时可以被一起打包。

preload js 文件遵循 CommonJS 规范，因此你可以使用 require 来引入 Node.js 模块，此部分可以参考 Node.js 文档。

只需给 window 对象自定义一个属性，前端就可直接访问该属性。

由于 preload js 文件可使用本地原生能力，为了防止开发者滥用各种读写文件、网络等能力，uTools 规定：

**Examples:**

Example 1 (javascript):
```javascript
const fs = require("fs");

window.customApis = {
  readFile: (path) => {
    return fs.readFileSync(path, "utf8");
  },
};
```

Example 2 (python):
```python
import { useEffect, useState } from "react";
export default function App() {
  const [file, setFile] = useState("");
  useEffect(() => {
    window.customApis.readFile("/path/to/README.md").then((data) => {
      setFile(data);
    }
  }, []);

  return (
    <div>
      <pre>{file}</pre>
    <div>
  )
}
```

---
