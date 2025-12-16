#!/usr/bin/env python3
"""
ByteDance MCP 服务器 Python 包装器
方便集成到 Claude Code Skill 中使用
"""

import subprocess
import json
import sys
import os
from typing import Dict, Any, Optional

class ByteDanceMCP:
    """ByteDance MCP 服务器客户端"""

    def __init__(self,
                 psm: str = "bytedance.mcp.codebase",
                 region: str = "CN",
                 call_tool_headers: str = "Authorization=Bearer code_pat_UPByoMOUvKmqTforneex",
                 timeout: int = 60):
        """
        初始化 MCP 客户端

        Args:
            psm: MCP 服务 PSM
            region: 网关区域
            timeout: 超时时间（秒）
        """
        self.psm = psm
        self.region = region
        self.call_tool_headers = call_tool_headers
        self.timeout = timeout

    def _execute_command(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """执行 MCP 命令"""
        # 构建命令
        cmd = [
            "npx",
            "--registry", "https://bnpm.byted.org",
            "-y",
            "@byted/mcp-proxy@latest"
        ]

        # 设置环境变量
        env = os.environ.copy()
        env["MCP_SERVER_PSM"] = self.psm
        env["MCP_GATEWAY_REGION"] = self.region
        env["MCP_SERVER_CALL_TOOL_HEADERS"] = self.call_tool_headers

        try:
            # 执行命令
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )

            # 先发送初始化请求
            init_request = {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "clientInfo": {
                        "name": "bytedance-mcp-wrapper",
                        "version": "1.0.0"
                    }
                }
            }

            # 发送初始化请求
            init_cmd = json.dumps(init_request) + '\n'
            process.stdin.write(init_cmd)
            process.stdin.flush()

            # 读取初始化响应（忽略错误输出）
            init_response = process.stdout.readline()

            # 构建实际请求
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params or {}
            }

            # 发送实际请求
            actual_cmd = json.dumps(request) + '\n'
            process.stdin.write(actual_cmd)
            process.stdin.flush()

            # 读取响应，跳过初始化响应
            # 跳过所有输出直到找到第二个 JSON 响应
            json_count = 0
            buffer = ""

            while True:
                line = process.stdout.readline()
                if not line:
                    break

                buffer += line

                # 查找可能的 JSON 对象
                start_idx = buffer.find('{')
                if start_idx >= 0:
                    # 查找匹配的右括号
                    bracket_count = 0
                    in_string = False
                    escape_next = False

                    for i in range(start_idx, len(buffer)):
                        char = buffer[i]

                        if escape_next:
                            escape_next = False
                            continue

                        if char == '\\' and in_string:
                            escape_next = True
                            continue

                        if char == '"':
                            in_string = not in_string
                            continue

                        if not in_string:
                            if char == '{':
                                bracket_count += 1
                            elif char == '}':
                                bracket_count -= 1
                                if bracket_count == 0:
                                    # 找到完整的 JSON 对象
                                    json_str = buffer[start_idx:i+1]
                                    try:
                                        response = json.loads(json_str)
                                        json_count += 1
                                        if json_count == 2:  # 第二个 JSON 是实际响应
                                            process.terminate()
                                            return response
                                        # 清理已处理的缓冲区
                                        buffer = buffer[i+1:]
                                        break
                                    except json.JSONDecodeError:
                                        continue

                    # 如果缓冲区太大，清理它
                    if len(buffer) > 10000:
                        buffer = buffer[start_idx:]

            # 等待进程结束
            stdout, stderr = process.communicate(timeout=self.timeout)

            if process.returncode != 0:
                raise RuntimeError(f"MCP 服务器错误: {stderr}")

            # 如果没有获得响应，抛出错误
            raise RuntimeError("无法从 MCP 服务器获得有效响应")

        except subprocess.TimeoutExpired:
            process.kill()
            raise RuntimeError(f"请求超时（{self.timeout}秒）")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"解析响应失败: {e}")
        except Exception as e:
            raise RuntimeError(f"执行失败: {e}")

    
    def list_tools(self) -> Dict[str, Any]:
        """列出所有可用工具"""
        return self._execute_command("tools/list")

    def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """调用特定工具"""
        params = {
            "name": tool_name,
            "arguments": arguments or {}
        }
        return self._execute_command("tools/call", params)

def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='ByteDance MCP 服务器包装器')
    parser.add_argument('command', choices=['list-tools', 'call', 'init'], help='命令')
    parser.add_argument('--tool', help='工具名称（用于 call 命令）')
    parser.add_argument('--params', help='JSON 格式的参数', default='{}')
    parser.add_argument('--psm', default='bytedance.mcp.codebase', help='MCP 服务 PSM')
    parser.add_argument('--region', default='CN', help='网关区域')
    parser.add_argument('--call-tool-headers', default='Authorization=Bearer code_pat_UPByoMOUvKmqTforneex', help='调用工具时的 HTTP 头')
    parser.add_argument('--timeout', type=int, default=60, help='超时时间（秒）')

    args = parser.parse_args()

    # 创建 MCP 客户端
    mcp = ByteDanceMCP(
        psm=args.psm,
        region=args.region,
        call_tool_headers=args.call_tool_headers,
        timeout=args.timeout
    )

    try:
        # 执行命令
        if args.command == 'init':
            # init 不再需要，因为初始化在每个调用中自动处理
            result = {"status": "ok", "message": "初始化将在每次调用时自动处理"}
        elif args.command == 'list-tools':
            result = mcp.list_tools()
        elif args.command == 'call':
            if not args.tool:
                print("错误：call 命令需要指定 --tool 参数", file=sys.stderr)
                sys.exit(1)

            # 解析参数
            try:
                params = json.loads(args.params)
            except json.JSONDecodeError as e:
                print(f"错误：参数不是有效的 JSON: {e}", file=sys.stderr)
                sys.exit(1)

            result = mcp.call_tool(args.tool, params)

        # 输出结果
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()