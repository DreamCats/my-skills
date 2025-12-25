---
name: polish-image-prompt
description: 润色并扩写用户的图片生成描述为高质量英文 Prompt（面向 doubao-seedream-4.5），自动判断类型（photo/illustration/3D/graphic design），并追加固定 Negative。用于用户要求“润色/优化/补全/增强图片提示词/生成 prompt”等场景。
---

# Polish Image Prompt

## Overview

把用户的描述润色为 Seedream 4.5 适配的英文提示词，保持原意、补齐画面要素，输出固定格式的 Prompt 与 Negative。

## Workflow

### 1) 解析用户意图
- 提取主体、场景、动作、关键约束（数量、风格、时代、地点、材质等）。
- 保留专有名词与品牌名，不翻译。
- 缺少必要主体时先追问；否则继续。

### 2) 判断类型
- 用户明确指定类型时直接采用。
- 未指定时按关键词推断：
  - photo：photo, photograph, realistic, camera, lens, bokeh, DSLR, 摄影, 写实, 相机
  - illustration：illustration, anime, comic, watercolor, sketch, 插画, 手绘, 动漫
  - 3D：3D, render, blender, c4d, octane, unreal, 3D渲染
  - graphic design：graphic design, poster, logo, branding, vector, infographic, 平面, 海报, 标志, 版式
- 多个命中时优先级：3D > illustration > graphic design > photo（除非用户显式声明）。

### 3) 组装 Prompt（英文、逗号分隔）
按顺序拼接并保持单行：
Subject -> Environment -> Action -> Composition -> Lighting -> Style/Medium -> Materials/Details -> Color -> Quality

- 只补“保守默认”，避免引入冲突元素。
- 风格标签最多 1–2 个，避免互相打架。
- 除非用户要求，否则不要加入文字/水印类描述。

### 4) 追加类型默认补充词
按类型追加（可按需微调，不要与用户明确要求冲突）：
- photo: photorealistic, 35mm lens, shallow depth of field, soft natural light, realistic textures, high detail
- illustration: digital illustration, clean linework, subtle shading, soft lighting, high detail
- 3D: 3D render, PBR materials, ray-traced lighting, studio lighting, high detail
- graphic design: vector style, clean layout, grid-based composition, high contrast, crisp edges, negative space

### 5) 输出格式（固定）
只输出两行：
```
Prompt: <English prompt>
Negative: <固定 Negative 列表>
```

固定 Negative：
lowres, blurry, jpeg artifacts, watermark, text, logo, signature, bad anatomy, extra limbs, missing limbs, deformed, mutated, duplicate, cropped, out of frame, noisy, grain, oversaturated, overexposed, underexposed, motion blur

## Examples

### Example A (photo)
Input: “雨夜街头，穿风衣的人在路灯下走过，氛围电影感”
Output:
Prompt: A lone person in a trench coat walking under a street lamp on a rainy night, wet pavement reflections, medium shot, moody atmosphere, cinematic, photorealistic, 35mm lens, shallow depth of field, soft natural light, realistic textures, high detail
Negative: lowres, blurry, jpeg artifacts, watermark, text, logo, signature, bad anatomy, extra limbs, missing limbs, deformed, mutated, duplicate, cropped, out of frame, noisy, grain, oversaturated, overexposed, underexposed, motion blur

### Example B (illustration)
Input: “温暖的童话森林，有小鹿和蘑菇屋，手绘插画风”
Output:
Prompt: A warm fairytale forest with a deer and a mushroom house, cozy atmosphere, gentle composition, digital illustration, clean linework, subtle shading, soft lighting, high detail
Negative: lowres, blurry, jpeg artifacts, watermark, text, logo, signature, bad anatomy, extra limbs, missing limbs, deformed, mutated, duplicate, cropped, out of frame, noisy, grain, oversaturated, overexposed, underexposed, motion blur

### Example C (3D)
Input: “玻璃质感的机器人站在极简展厅，3D渲染”
Output:
Prompt: A glass-textured robot standing in a minimalist showroom, centered composition, studio setup, 3D render, PBR materials, ray-traced lighting, studio lighting, high detail
Negative: lowres, blurry, jpeg artifacts, watermark, text, logo, signature, bad anatomy, extra limbs, missing limbs, deformed, mutated, duplicate, cropped, out of frame, noisy, grain, oversaturated, overexposed, underexposed, motion blur

### Example D (graphic design)
Input: “科技会议海报，未来感，蓝色系”
Output:
Prompt: A futuristic tech conference poster, bold hierarchy, clean layout, grid-based composition, cool blue palette, vector style, high contrast, crisp edges, negative space
Negative: lowres, blurry, jpeg artifacts, watermark, text, logo, signature, bad anatomy, extra limbs, missing limbs, deformed, mutated, duplicate, cropped, out of frame, noisy, grain, oversaturated, overexposed, underexposed, motion blur
