import subprocess
import os
import argparse
import logging
import time
import threading

# 配置日志
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'git_auto_update.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)

import tkinter as tk
from tkinter import ttk, scrolledtext

class GitAutoUpdater:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Git自动更新工具")
        
        # 初始化组件
        self.status_label = ttk.Label(self.root, text="就绪", font=('Arial', 10))
        btn_frame = ttk.Frame(self.root)
        self.log_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.update_btn = ttk.Button(btn_frame, text="立即更新", command=self.start_update)
        exit_btn = ttk.Button(btn_frame, text="退出程序", command=self.root.destroy)

        # 布局组件
        self.status_label.pack(pady=5)
        btn_frame.pack(pady=5)
        self.log_area.pack(padx=10, pady=10)
        self.update_btn.pack(side=tk.LEFT, padx=5)
        exit_btn.pack(side=tk.RIGHT, padx=5)

    def start_update(self):
        self.update_btn['state'] = 'disabled'
        self.status_label.config(text="更新中...", foreground='blue')
        threading.Thread(target=self._perform_update).start()

    def _perform_update(self):
        try:
            self.log_area.insert(tk.END, "开始更新操作...\n")
            result_text = ""
            success = self.git_auto_update(os.getcwd())
            result_text = "更新成功！\n" if success else "更新失败！\n"
            self.root.after(0, lambda: self.status_label.config(
                text="操作完成" if success else "操作失败",
                foreground='green' if success else 'red'
            ))
        except Exception as e:
            result_text = f"发生未预期错误: {str(e)}\n"
            self.log_area.insert(tk.END, result_text)
            self.root.after(0, lambda: self.status_label.config(text="严重错误", foreground='red'))
        finally:
            self.root.after(0, lambda: self.update_btn.config(state='normal'))
            self.log_area.insert(tk.END, result_text)
            self.log_area.see(tk.END)


    def git_auto_update(self, folder_path):
        try:
            # 打印当前检查的文件夹路径
            print(f"正在检查文件夹: {folder_path}")
            # 检查文件夹是否为 Git 仓库
            git_dir = os.path.join(folder_path, '.git')
            if not os.path.exists(git_dir):
                print(f"{folder_path} 不是一个 Git 仓库，因为未找到 {git_dir}。")
                return False

            # 尝试访问 .git 目录，检查权限
            try:
                os.listdir(git_dir)
            except PermissionError:
                print(f"没有足够的权限访问 {git_dir}。请检查文件夹权限或以管理员身份运行脚本。")
                return False

            # 切换到指定文件夹
            os.chdir(folder_path)

            # 添加所有更改到暂存区
            subprocess.run(['git', 'add', '.'], check=True)

            # 提交更改
            commit_result = subprocess.run(['git', 'commit', '-m', 'Auto update'], capture_output=True, text=True)
            if commit_result.returncode != 0 and 'nothing to commit' not in commit_result.stderr:
                print(f"提交更改时出错: {commit_result.stderr}")
                return False

            # 拉取远程仓库的最新提交（带重试）
            retries = 3
            for attempt in range(retries):
                try:
                    pull_result = subprocess.run(['git', 'pull', 'origin', 'master'], capture_output=True, text=True)
                    if pull_result.returncode == 0:
                        logging.info('拉取远程仓库成功')
                        break
                    else:
                        logging.warning(f'拉取失败，第{attempt+1}次重试...')
                        time.sleep(2)
                except Exception as pull_error:
                    logging.error(f'拉取异常: {str(pull_error)}')
            else:
                logging.error('拉取操作重试次数用尽')
                return False

            # 推送更改到远程仓库（带重试）
            for attempt in range(retries):
                try:
                    push_result = subprocess.run(['git', 'push', 'origin', 'master'], capture_output=True, text=True)
                    if push_result.returncode == 0:
                        logging.info('推送远程仓库成功')
                        break
                    else:
                        logging.warning(f'推送失败，第{attempt+1}次重试...')
                        time.sleep(2)
                except Exception as push_error:
                    logging.error(f'推送异常: {str(push_error)}')
            else:
                logging.error('推送操作重试次数用尽')
                return False

            print("文件夹内容已成功更新到远程仓库。")
            return True
        except subprocess.CalledProcessError as e:
            print(f"执行 Git 命令时出错: {e}")
            return False
        except Exception as e:
            print(f"发生未知错误: {e}")
            return False

if __name__ == "__main__":
    app = GitAutoUpdater()
    app.root.mainloop()
    