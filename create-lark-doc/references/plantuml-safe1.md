1）全局通用：建议只用这些“基础骨架语法”

这些通常最稳：
• @startuml / @enduml
• title ...（标题）
• caption ...（有时可用；不保证样式一致）
• 注释：' comment 或 /' ... '/

尽量少用/先别指望：
• skinparam ...、颜色、主题、字体、对齐、布局微调等（飞书会跟随画板主题，很多会被忽略/降级）。 ￼

⸻

2）各图类型“稳妥可用语法”清单

A. 流程图（Flowchart，通常是活动图语法那套）

优先用这些：
• 节点：:文本;（动作框）
• 分支：if (...) then (...) / else / endif
• 循环：repeat / repeat while (...)
• 开始结束：start / stop 或 end

尽量避免：复杂皮肤、颜色、对齐、布局指令。

⸻

B. 活动图（Activity Diagram）

和流程图同一套，额外常用：
• 并行：fork / fork again / end fork
• 泳道（不保证 100%）：|Lane|（如果你发现飞书里不生效，就别用）

⸻

C. 时序图（Sequence Diagram）

稳妥用这些：
• 参与者：participant / actor（名字尽量简单）
• 消息：A -> B: msg、返回：B --> A: msg
• 激活：activate A / deactivate A
• 注释：note left/right of A: ...、note over A,B: ...
• 分段：alt / else / end、opt / end、loop / end

已知会踩坑的（官方点名）：
• 参与者颜色不展示（你写 #color 或相关样式也可能没效果） ￼
• 连线文字只能在中点，不能左/右对齐（相关对齐语法大概率无效） ￼

⸻

D. 用例图（Use Case Diagram）

稳妥用这些：
• 角色：actor 用户
• 用例：(登录)、(下单)
• 关系：用户 --> (登录)
• include/extend：(A) ..> (B) : <<include>>、<<extend>>

避免：大量皮肤参数、复杂布局控制。

⸻

E. 类图（Class Diagram）

稳妥用这些：
• class A { +field : type +method() }
• 关系：
• 继承：B --|> A
• 关联：A --> B
• 聚合/组合：A o-- B、A \*-- B
• 接口：interface I、实现：A ..|> I
• 包：package xxx { ... }（若发现飞书渲染异常，就改成普通分组/不分包）

避免：复杂泛型展示、很重的自定义样式。

⸻

F. ER 图（Entity Relationship）

稳妥用这些：
• entity 用户 { _id : int 名称 : varchar }
• 关系（看你习惯的 ER 语法写法；若某种箭头不生效就退回最普通的 -- / -->）
• 基本字段/主键标记（_ 这类标识有时可以用；不保证样式一致）

⸻

G. 思维导图（Mindmap）

飞书官方说支持“思维导图”。 ￼
PlantUML 的 mindmap 语法在不同渲染器差异挺大，所以这里给你最保守的写法建议：
• 用最基础层级（少样式、少图标、少颜色）
• 如果你用了 mindmap / \* 层级语法发现飞书不认，就只能改用“活动图/流程图”的方式模拟树形结构（这也是很多平台的现状）
