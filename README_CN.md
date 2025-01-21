# Git Commit Notifier

[English](README.md) | 中文

一个自动将 Git 提交信息推送到企业微信的通知工具。当有新的 Git 合并操作时, 例如, git pull，会自动发送通知到指定的企业微信用户或群组。

## 功能特点

- 自动监控 Git 合并操作
- 发送最近 5 次提交的详细信息
- 支持多个项目同时使用
- 显示提交作者、时间和内容
- 通过企业微信应用发送消息

## 开发思路

该工具旨在监控 Git 仓库的分支合并操作。它利用 `post-merge` 钩子来触发通知。当监测的 Git 仓库中有分支合并时，`post-merge` 钩子会执行脚本 'git_commit_notifier.py'，将提交详情发送到企业微信，确保所有相关人员实时获知信息。

## 安装步骤

1. 克隆项目到指定目录：
```bash
cd /opt
git clone https://github.com/bigfoot88/git_notifier.git
chmod +x /opt/git_notifier/git_commit_notifier.py
```

2. 创建配置文件：
```bash
sudo cp config.ini.example /opt/git_notifier/config.ini
sudo chmod 600 /opt/git_notifier/config.ini  # 设置安全的文件权限
```

3. 编辑 `/opt/git_notifier/config.ini` 文件，填入您的企业微信配置：
```ini
[wecom]
corpid = your_corpid_here
secret = your_secret_here
bot_id = your_bot_id_here
userid = your_userid_here
```

4. 在需要通知的 Git 仓库中设置 hooks, 例如代码仓库是b8water：
```bash
cd /path/to/b8water
cd .git/hooks
sudo cp /opt/git_notifier/post-merge.sample .git/hooks/post-merge
chmod +x .git/hooks/post-merge
```

## 配置说明

- `corpid`: 企业微信的企业 ID
- `secret`: 企业微信应用的密钥
- `bot_id`: 企业微信应用的 AgentId
- `userid`: 接收消息的用户 ID（譬如 raymond；也可以是 @all）

## 使用方法

安装配置完成后，工具会自动在以下情况发送通知：

- 例如在 b8water 仓库中执行 `git pull` 并成功合并后

通知消息包含：
- 项目名称
- 最近 5 次提交的详细信息
- 每次提交的作者、时间和提交信息

## 依赖要求

- Python 3.6+
- requests 库
- 企业微信应用配置

## 注意事项

- 请确保 `config.ini` 文件的权限设置正确，防止敏感信息泄露
- 建议定期检查企业微信的 API 调用频率限制
- 如遇到问题，可查看命令行输出的错误信息

## 许可证

MIT License

Copyright (c) 2024 Raymond Ho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## 作者

Raymond Ho

## 贡献

欢迎提交 Issue 和 Pull Request！