import subprocess
import os
import argparse
import logging
import time

# 配置日志
logging.basicConfig(
    filename='git_auto_update.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)

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
    parser = argparse.ArgumentParser(description='自动更新Git仓库')
    parser.add_argument('--path', type=str, default=os.getcwd(),
                       help='要更新的文件夹路径（默认为当前目录）')
    args = parser.parse_args()
    
    logging.info(f'开始处理目录: {args.path}')
    success = git_auto_update(args.path)
    
    if success:
        logging.info('操作成功完成')
    else:
        logging.error('操作过程中出现错误')
    
    time.sleep(3)  # 留出时间查看结果
    