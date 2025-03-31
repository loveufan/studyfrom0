import tkinter as tk
from tkinter import messagebox
import subprocess
import logging
import os
import threading

class GitAutoUpdater:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Git自动更新工具")
        
        # 初始化日志
        self.log_path = os.path.join(os.path.dirname(__file__), 'git_auto_update.log')
        logging.basicConfig(filename=self.log_path, level=logging.INFO,
                          format='%(asctime)s - %(levelname)s: %(message)s')
        
        # 路径初始化
        self.path_label = tk.Label(self.root, text="请选择Git仓库路径")
        
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack()
        
        # 添加路径选择按钮
        path_frame = tk.Frame(frame)
        path_frame.pack(fill='x', pady=5)
        
        self.path_label = tk.Label(path_frame, text="当前路径：未选择")
        self.path_label.pack(side='left', padx=5)
        
        select_btn = tk.Button(path_frame, text="选择目录", command=self.select_directory,
                             width=10, bg="#2196F3", fg="white")
        select_btn.pack(side='right')

        self.update_btn = tk.Button(frame, text="更新仓库", command=self.update_repo,
                             width=15, height=2, bg="#4CAF50", fg="white")
        self.update_btn.pack(pady=10)

        exit_btn = tk.Button(frame, text="退出", command=self.root.destroy,
                           width=15, height=2, bg="#f44336", fg="white")
        exit_btn.pack(pady=10)

    def select_directory(self):
        from tkinter import filedialog
        selected_path = filedialog.askdirectory()
        if selected_path:
            self.project_path = selected_path
            self.path_label.config(text="当前路径：" + selected_path)
            if not os.path.exists(os.path.join(selected_path, '.git')):
                messagebox.showerror("错误", "所选目录不是Git仓库！")
                delattr(self, 'project_path')

    def run_git_command(self, command):
        try:
            if not hasattr(self, 'project_path'):
                messagebox.showerror("错误", "请先选择项目目录！")
                return False
            repo_path = self.project_path
            if not os.path.exists(os.path.join(repo_path, '.git')):
                messagebox.showerror("错误", "未找到Git仓库，请检查项目路径！")
                return False
            result = subprocess.run(command, cwd=repo_path,
                                  capture_output=True, text=True, check=True,
                                  encoding='utf-8', errors='ignore')
            logging.info(f"命令成功: {' '.join(command)}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"错误: {e.stderr}")
            messagebox.showerror("错误", f"执行失败: {e.stderr}")
            return False

    def update_repo(self):
        self.update_btn.config(state='disabled')
        threading.Thread(target=self._execute_git_commands).start()

    def _execute_git_commands(self):
        steps = [
            ["git", "add", "."],
            ["git", "commit", "-m", "自动提交更新"],
            ["git", "push"]
        ]

        try:
            for step in steps:
                if not self.run_git_command(step):
                    return
            messagebox.showinfo("成功", "所有文件已更新到GitHub仓库！")
        finally:
            self.root.after(0, lambda: self.update_btn.config(state='normal'))
        logging.info("仓库更新完成")

if __name__ == "__main__":
    # 确保日志文件存在
    log_dir = os.path.dirname(__file__)
    log_file = os.path.join(log_dir, 'git_auto_update.log')
    if not os.path.exists(log_file):
        open(log_file, 'w').close()
    
    app = GitAutoUpdater()
    app.root.mainloop()