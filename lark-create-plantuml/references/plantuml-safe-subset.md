# 飞书画板 PlantUML 安全子集

## 全局安全语法
仅使用这些基础语法：
- @startuml / @enduml
- title ...（不要缩进；如报错直接移除）
- caption ...（可选）
- 注释：' comment 或 /' ... '/

避免：
- skinparam 与样式指令
- 颜色、字体、对齐、布局微调
- 预处理/宏（如 `!define`；ArchiMate 例外，需 `!include <archimate/Archimate>`）
- 行首缩进（粘贴时可能导致解析失败）
- 方向控制指令（如 `left to right direction`，飞书画板可能不支持）

## 流程图与活动图
- start / stop / end
- :动作文本;
- if (...) then (...) / else / endif
- repeat / repeat while (...)
- fork / fork again / end fork（可选）
- |泳道| 可能失效，若不稳定请禁用

## 时序图
- participant / actor
- A -> B: msg
- B --> A: msg
- activate A / deactivate A
- note left/right of A: ...
- note over A,B: ...
- alt / else / end
- opt / end
- loop / end

注意：
- 参与者颜色可能不渲染。
- 文本对齐控制可能被忽略。

## 用例图
- actor 用户
- (登录)
- 用户 --> (登录)
- (A) ..> (B) : <<include>>
- (A) ..> (B) : <<extend>>

## 类图
- class A
- class A { field : type  method() }
- interface I
- B --|> A
- A --> B
- A o-- B
- A *-- B
- A ..|> I
- package X { ... }（若渲染异常就移除）

注意：
- 类成员块可用，但建议仅使用最简写法：
  - 成员行不加可见性标记（如 `+` `-` `#` `~`）
  - 成员行格式用 `field : type` 或 `method()`  

## 组件图/部署式分组图（可用）
- 组件盒子：`[Component]`
- 分组容器：`package "Group" { ... }`
- 节点容器：`node "Node" { ... }`
- 其他容器：`cloud { ... }` / `database "DB" { ... }` / `folder "Folder" { ... }` / `frame "Frame" { ... }`
- 关系：`A --> B` / `A -- B`

注意：
- 避免复杂样式与对齐控制。
- 行首缩进可能导致粘贴解析失败。

组件图模板（飞书画板可用，需无缩进）：

@startuml
package "Some Group" {
HTTP - [First Component]
[Another Component]
}
node "Other Groups" {
FTP - [Second Component]
[First Component] --> FTP
}
cloud {
[Example 1]
}
database "MySql" {
folder "This is my folder" {
[Folder 3]
}
frame "Foo" {
[Frame 4]
}
}
[Another Component] --> [Example 1]
[Example 1] --> [Folder 3]
[Folder 3] --> [Frame 4]
@enduml

## ArchiMate（原生态支持）
- 飞书画板 PlantUML 版本较旧（约 1.2023.13），ArchiMate sprite 不完整。
- 出现 `No such internal sprite: archimate/xxx` 时，说明引用了旧版不存在的元素；需要移除对应 `sprite` 与其引用。
- 原生态语法允许 `skinparam` / `sprite` / `legend` 等，但可能失败；失败时优先改用“无 sprite 兼容模板”，其次退回组件图。

ArchiMate 原生态模板（无缩进）：

@startuml
skinparam rectangle<<behavior>> {
roundCorner 25
}
sprite $bProcess jar:archimate/business-process
sprite $aService jar:archimate/application-service
sprite $aComponent jar:archimate/application-component
rectangle "Handle claim" as HC <<$bProcess>><<behavior>> #Business
rectangle "Capture Information" as CI <<$bProcess>><<behavior>> #Business
rectangle "Notify\nAdditional Stakeholders" as NAS <<$bProcess>><<behavior>> #Business
rectangle "Validate" as V <<$bProcess>><<behavior>> #Business
rectangle "Investigate" as I <<$bProcess>><<behavior>> #Business
rectangle "Pay" as P <<$bProcess>><<behavior>> #Business
HC *-down- CI
HC *-down- NAS
HC *-down- V
HC *-down- I
HC *-down- P
CI -right->> NAS
NAS -right->> V
V -right->> I
I -right->> P
rectangle "Scanning" as scanning <<$aService>><<behavior>> #Application
rectangle "Customer admnistration" as customerAdministration <<$aService>><<behavior>> #Application
rectangle "Claims admnistration" as claimsAdministration <<$aService>><<behavior>> #Application
rectangle Printing <<$aService>><<behavior>> #Application
rectangle Payment <<$aService>><<behavior>> #Application
scanning -up-> CI
customerAdministration -up-> CI
claimsAdministration -up-> NAS
claimsAdministration -up-> V
claimsAdministration -up-> I
Payment -up-> P
Printing -up-> V
Printing -up-> P
rectangle "Document\nManagement\nSystem" as DMS <<$aComponent>> #Application
rectangle "General\nCRM\nSystem" as CRM <<$aComponent>> #Application
rectangle "Home & Away\nPolicy\nAdministration" as HAPA <<$aComponent>> #Application
rectangle "Home & Away\nFinancial\nAdministration" as HFPA <<$aComponent>> #Application
DMS .up.|> scanning
DMS .up.|> Printing
CRM .up.|> customerAdministration
HAPA .up.|> claimsAdministration
HFPA .up.|> Payment
legend left
Example from the "Archisurance case study" (OpenGroup).
See
====
<$bProcess> :business process
====
<$aService> : application service
====
<$aComponent> : application component
endlegend
@enduml

无 sprite 兼容模板（无缩进）：

@startuml
rectangle "业务能力" as Biz
rectangle "应用组件" as App
rectangle "技术服务" as Tech
Biz --> App
App --> Tech
@enduml

最小模板（无缩进，仅在原生态需要时使用）：

@startuml
!include <archimate/Archimate>
archimate #Business "业务能力" as biz
archimate #Application "应用组件" as app
archimate #Technology "技术服务" as tech
biz --> app
app --> tech
@enduml

## ER 图
- entity 用户 { *id : int  name : varchar }
- 关系箭头：-- 或 -->

## 思维导图
- 使用 `@startmindmap` / `@endmindmap`
- 仅使用最基础层级（`*` 或 `+` 递进）
- 可选方向：`top to bottom direction`

注意：
- 避免复杂样式与嵌套代码块。
- 若 mindmap 语法不生效，改用活动图/流程图模拟树形结构。
