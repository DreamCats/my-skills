# Lark CLI 故障排除指南

本文档提供 Lark CLI 工具常见问题的解决方案和调试技巧。

## 常见错误及解决方案

### 1. 认证相关错误

#### 错误：`APP_ID` 或 `APP_SECRET` 未配置
**错误信息：**
```
配置错误：缺少必要的环境变量 APP_ID 或 APP_SECRET
```

**解决方案：**
1. 确认 `.env` 文件位置正确（与 `lark-cli` 可执行文件同目录）
2. 检查 `.env` 文件内容：
```bash
# 应包含这两行
APP_ID=your_actual_app_id
APP_SECRET=your_actual_app_secret
```
3. 验证环境变量加载：
```bash
# 在可执行文件目录执行
ls -la .env
cat .env
```

#### 错误：认证失败
**错误信息：**
```
API错误：认证失败，请检查 APP_ID 和 APP_SECRET 是否正确
```

**解决方案：**
1. 验证 App ID 和 Secret 是否正确
2. 确认应用权限是否已开通
3. 检查应用是否已启用相关 API
4. 使用调试模式查看详细错误：
```bash
lark-cli -v get-node test_token
```

### 2. 权限相关错误

#### 错误：没有权限访问资源
**错误信息：**
```
API错误：没有权限，code: 99991401
```

**解决方案：**
1. 确认应用有对应 API 权限
2. 检查文档/文件夹的访问权限
3. 如果是企业应用，确认应用已安装到企业
4. 使用文档所有者身份添加权限：
```bash
lark-cli add-permission doc_token \
  --doc-type docx \
  --member-type openid \
  --member-id app_openid \
  --perm view
```

### 3. 文档/节点不存在错误

#### 错误：文档不存在
**错误信息：**
```
API错误：资源不存在，code: 99991400
```

**解决方案：**
1. 验证文档 ID 或 token 是否正确
2. 确认文档未被删除
3. 检查文档访问权限
4. 获取知识空间节点列表确认：
```bash
lark-cli get-node space_token --obj-type wiki
```

### 4. 文件操作错误

#### 错误：文件不存在
**错误信息：**
```
错误：文件不存在：/path/to/file.txt
```

**解决方案：**
1. 检查文件路径是否正确
2. 确认文件权限（可读）
3. 使用绝对路径：
```bash
lark-cli upload-media "/full/path/to/file.png" docx_image block_id
```

#### 错误：文件过大
**错误信息：**
```
API错误：文件过大，code: 99991419
```

**解决方案：**
1. 检查文件大小（限制 100MB）
2. 压缩文件后再上传
3. 考虑使用云存储分享链接

### 5. 网络相关错误

#### 错误：请求超时
**错误信息：**
```
网络错误：请求超时
```

**解决方案：**
1. 检查网络连接
2. 尝试使用代理：
```bash
export HTTPS_PROXY=http://proxy.example.com:8080
lark-cli get-content doc_id
```
3. 重试操作：
```bash
# 简单重试脚本
for i in {1..3}; do
  if lark-cli get-content doc_id; then
    break
  fi
  sleep 2
done
```

#### 错误：频率限制
**错误信息：**
```
API错误：请求过于频繁，code: 99991408
```

**解决方案：**
1. 降低请求频率
2. 批量操作时添加延迟：
```bash
while read user_id; do
  lark-cli send-message "$user_id" ...
  sleep 2  # 避免频率限制
done < users.txt
```

## 调试技巧

### 1. 启用详细日志
```bash
# 查看详细的请求和响应
lark-cli -v get-content doc_id

# 结合 JSON 输出
lark-cli -v --format json get-node token
```

### 2. 使用 JSON 输出分析问题
```bash
# 保存完整响应
lark-cli --format json get-content doc_id > response.json

# 格式化查看
cat response.json | jq .

# 检查错误码
ERROR_CODE=$(cat response.json | jq -r '.code')
if [ "$ERROR_CODE" != "0" ]; then
  echo "错误码: $ERROR_CODE"
  echo "错误信息: $(cat response.json | jq -r '.msg')"
fi
```

### 3. 测试 API 连接
```bash
# 使用简单命令测试连接
lark-cli --help

# 测试认证
lark-cli get-node "test_token" -v
```

### 4. 检查环境配置
```bash
# 查看可执行文件位置
which lark-cli

# 查看 .env 文件
LARK_DIR=$(dirname $(which lark-cli))
ls -la "$LARK_DIR/.env"

# 测试环境变量
cd "$LARK_DIR"
export $(cat .env | xargs)
echo $APP_ID
```

## 性能优化

### 1. 大文档处理优化
```bash
# 分页获取大量块
PAGE_TOKEN=""
PAGE_SIZE=100

while true; do
  if [ -n "$PAGE_TOKEN" ]; then
    RESULT=$(lark-cli --format json get-blocks doc_id \
      --page-size $PAGE_SIZE \
      --page-token "$PAGE_TOKEN")
  else
    RESULT=$(lark-cli --format json get-blocks doc_id \
      --page-size $PAGE_SIZE)
  fi

  # 处理当前页
  echo "$RESULT" | jq '.items[]'

  # 检查是否有下一页
  HAS_MORE=$(echo "$RESULT" | jq -r '.has_more')
  if [ "$HAS_MORE" = "false" ]; then
    break
  fi

  PAGE_TOKEN=$(echo "$RESULT" | jq -r '.page_token')
done
```

### 2. 批量操作优化
```bash
# 使用并行处理（需要 GNU parallel）
cat user_list.txt | parallel -j 5 \
  'lark-cli send-message {} --receive-id-type open_id --msg-type text '\''{"text":"批量消息"}'\'''

# 或者使用 xargs
cat user_list.txt | xargs -I {} -P 5 \
  lark-cli send-message {} --receive-id-type open_id --msg-type text '{"text":"批量消息"}'
```

### 3. 内存使用优化
```bash
# 流式处理大文件
while IFS= read -r line; do
  # 逐行处理，避免加载整个文件到内存
  echo "Processing: $line"
  # ... 处理逻辑 ...
done < large_file.txt
```

## 日志分析

### 1. 解析详细日志
```bash
# 启用日志输出
lark-cli -v get-content doc_id 2> debug.log

# 分析日志
grep -E "(Request|Response|Error)" debug.log
```

### 2. 监控 API 调用
```bash
# 包装脚本来监控调用
#!/bin/bash
log_api_call() {
  echo "[$(date)] API Call: $*" >> api_calls.log
  lark-cli "$@"
}

# 使用包装器
log_api_call get-content doc_id
```

## 常见问题 FAQ

### Q: 为什么某些文档无法访问？
A: 可能原因：
1. 文档已删除
2. 没有访问权限
3. 文档不在已授权的知识空间中
4. 应用未安装到对应企业

### Q: 如何处理中文内容乱码？
A: 解决方案：
1. 确保终端支持 UTF-8
2. 使用 JSON 格式输出
3. 检查文件编码：
```bash
file -I document.txt
iconv -f GBK -t UTF-8 document.txt > document_utf8.txt
```

### Q: 批量操作时如何避免重复？
A: 使用幂等性参数：
```bash
UUID=$(uuidgen)
lark-cli send-message user_id \
  --msg-type text \
  '{"text":"消息"}' \
  --uuid "$UUID"
```

### Q: 如何处理大文件上传？
A: 建议方案：
1. 压缩文件
2. 分片上传（如果支持）
3. 使用云存储分享链接
4. 检查网络稳定性

### Q: 为什么消息发送失败？
A: 检查项目：
1. 接收者 ID 是否正确
2. 接收者类型是否匹配
3. 消息格式是否符合要求
4. 是否有发送权限

## 联系支持

如果问题仍未解决：

1. 收集错误信息：
```bash
lark-cli -v --format json <command> > debug.json 2>&1
```

2. 提供环境信息：
```bash
echo "OS: $(uname -a)"
echo "lark-cli version: $(lark-cli --version)"
echo "Env file: $(ls -la $(dirname $(which lark-cli))/.env)"
```

3. 记录复现步骤和期望结果

4. 通过以下渠道寻求帮助：
- 项目 GitHub Issues
- 官方技术支持
- 开发者社区