# Git Commit Notifier

[中文](README_CN.md) | English

A notification tool that automatically pushes Git commit messages to WeCom (Enterprise WeChat). When there are new Git merge operations, such as git pull, it automatically sends notifications to specified WeCom users or groups.

## Features

- Automatically monitors Git merge operations
- Sends detailed information of the last 5 commits
- Supports multiple projects simultaneously
- Displays commit author, time, and content
- Sends messages through WeCom application

## Development Approach

The tool is designed to monitor Git repositories for branch merges. It utilizes a `post-merge` hook to trigger notifications. When a branch is merged in the monitored Git repository, the `post-merge` hook executes a script 'git_commit_notifier.py' that sends the commit details to WeCom, ensuring that all relevant parties are informed in real-time.

## Installation

1. Clone the project to the specified directory:
```bash
cd /opt
git clone https://github.com/bigfoot88/git_notifier.git
chmod +x /opt/git_notifier/git_commit_notifier.py
```

2. Create configuration file:
```bash
sudo cp config.ini.example /opt/git_notifier/config.ini
sudo chmod 600 /opt/git_notifier/config.ini  # Set secure file permissions
```

3. Edit `/opt/git_notifier/config.ini` file, fill in your WeCom configuration:
```ini
[wecom]
corpid = your_corpid_here
secret = your_secret_here
bot_id = your_bot_id_here
userid = your_userid_here
```

4. Set up hooks in the Git repository that needs notifications, for example, if the repository is b8water:
```bash
cd /path/to/b8water
cd .git/hooks
sudo cp /opt/git_notifier/post-merge.sample .git/hooks/post-merge
chmod +x .git/hooks/post-merge
```

## Configuration Details

- `corpid`: WeCom enterprise ID
- `secret`: WeCom application secret key
- `bot_id`: WeCom application AgentId
- `userid`: Recipient user ID (such as raymond; can be @all)

## Usage

After installation and configuration, the tool will automatically send notifications in the following cases:

- For example, after executing `git pull` and successfully merging in the b8water repository

Notification messages include:
- Project name
- Detailed information of the last 5 commits
- Author, time, and commit message for each commit

## Requirements

- Python 3.6+
- requests library
- WeCom application configuration

## Notes

- Ensure proper permissions are set for the `config.ini` file to prevent sensitive information leakage
- Regularly check WeCom API call frequency limits
- Check command line output for error messages if issues occur

## License

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

## Author

Raymond Ho

## Contributing

Issues and Pull Requests are welcome! 