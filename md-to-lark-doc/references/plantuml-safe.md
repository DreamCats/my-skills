# 飞书画板 PlantUML 安全子集

## 全局安全语法
仅使用这些基础语法：
- @startuml / @enduml
- title ...
- caption ...（可选）
- 注释：' comment 或 /' ... '/

避免：
- skinparam 与样式指令
- 颜色、字体、对齐、布局微调

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
- class A { +field : type  +method() }
- interface I
- B --|> A
- A --> B
- A o-- B
- A *-- B
- A ..|> I
- package X { ... }（若渲染异常就移除）

## ER 图
- entity 用户 { *id : int  name : varchar }
- 关系箭头：-- 或 -->

## 思维导图
- 仅使用最基础层级，无样式。
- 若 mindmap 语法不生效，改用活动图/流程图模拟树形结构。
