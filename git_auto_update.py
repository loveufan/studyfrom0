import subprocess
import os

def git_auto_update(folder_path):
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

        # 拉取远程仓库的最新提交
        pull_result = subprocess.run(['git', 'pull', 'origin', 'master'], capture_output=True, text=True)
        if pull_result.returncode != 0:
            print(f"拉取远程仓库最新提交时出错: {pull_result.stderr}")
            return False

        # 推送更改到远程仓库
        push_result = subprocess.run(['git', 'push', 'origin', 'master'], capture_output=True, text=True)
        if push_result.returncode != 0:
            print(f"推送更改到远程仓库时出错: {push_result.stderr}")
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
    # 指定要更新的文件夹路径
    folder_path = 'your_folder_path'
    result = git_auto_update(folder_path)
    if result:
        print("脚本执行成功。")
    else:
        print("脚本执行失败。")
    