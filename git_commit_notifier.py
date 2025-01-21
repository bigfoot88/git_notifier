#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Git Commit Notifier
当有新的Git提交时，自动发送通知到企业微信群
"""

import subprocess
import requests
import time
from typing import List, Dict, Optional
import configparser
import os

class WeComNotifier:
    """企业微信通知类"""
    
    def __init__(self):
        self._load_config()
    
    def _load_config(self):
        """从配置文件加载设置"""
        config = configparser.ConfigParser()
        config_path = os.path.expanduser('/opt/git_notifier/config.ini')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
            
        config.read(config_path)
        
        try:
            self.corpid = config['wecom']['corpid']
            self.secret = config['wecom']['secret']
            self.bot_id = config['wecom'].getint('bot_id')
            self.userid = config['wecom']['userid']
        except KeyError as e:
            raise KeyError(f"配置文件中缺少必要的配置项: {e}")

    def get_access_token(self) -> Optional[str]:
        """获取企业微信访问令牌"""
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        params = {
            'corpid': self.corpid,
            'corpsecret': self.secret,
        }
        try:
            response = requests.get(url=url, params=params)
            return response.json()["access_token"]
        except Exception as e:
            print(f"[{self._get_time()}] 获取access token失败: {str(e)}")
            return None

    def push_message(self, message: str) -> Dict:
        """发送消息到企业微信"""
        token = self.get_access_token()
        if not token:
            return {"errcode": -1, "errmsg": "Failed to get access token"}

        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'
        params = {'access_token': token}
        data = {
            "touser": self.userid,
            "msgtype": "text",
            "agentid": self.bot_id,
            "text": {
                "content": message,
            },
        }
        try:
            response = requests.post(url=url, params=params, json=data)
            return response.json()
        except Exception as e:
            return {"errcode": -1, "errmsg": str(e)}

    @staticmethod
    def _get_time() -> str:
        """获取当前时间字符串"""
        return time.strftime('%Y-%m-%d %H:%M:%S')


class GitCommitNotifier:
    """Git提交通知类"""
    
    def __init__(self):
        self.wecom = WeComNotifier()
        # 保存当前工作目录
        self.git_dir = os.getcwd()
    
    def get_recent_commits(self, count: int = 5) -> List[Dict]:
        """获取最近的Git提交信息"""
        result = subprocess.run(
            ['git', '-C', self.git_dir, 'log', f'-{count}', '--pretty=format:%s||%cd||%an', '--date=format:%Y-%m-%d %H:%M:%S'],
            stdout=subprocess.PIPE,
            universal_newlines=True
        )
        commits = []
        for line in result.stdout.split('\n'):
            if line:
                try:
                    message, date, author = line.split('||')
                    commits.append({
                        'message': message.strip(),
                        'date': date.strip(),
                        'author': author.strip()
                    })
                except ValueError:
                    continue
        return commits

    def format_commit_messages(self, commits: List[Dict]) -> str:
        """格式化提交信息"""
        # 获取项目名称（从当前目录）
        project_name = os.path.basename(self.git_dir)
        
        # 在标题中添加项目名称
        formatted = [f"=== {project_name} 最近的Git提交 ===\n"]
        
        for i, commit in enumerate(commits, 1):
            formatted.append(f"[{i}]")
            formatted.append(f"作者: {commit['author']}")
            formatted.append(f"时间: {commit['date']}")
            formatted.append(f"内容: {commit['message']}\n")
        return "\n".join(formatted)

    def notify(self) -> None:
        """发送提交通知"""
        try:
            commits = self.get_recent_commits(5)
            if not commits:
                print(f"[{self.wecom._get_time()}] 没有找到Git提交记录")
                return

            message = self.format_commit_messages(commits)
            response = self.wecom.push_message(message)
            
            if response.get('errcode') == 0:
                print(f"[{self.wecom._get_time()}] 提交通知发送成功")
            else:
                print(f"[{self.wecom._get_time()}] 提交通知发送失败: {response}")
                
        except Exception as e:
            print(f"[{self.wecom._get_time()}] 发生错误: {str(e)}")


def main():
    """主函数"""
    notifier = GitCommitNotifier()
    notifier.notify()


if __name__ == "__main__":
    main() 