# 自动将下载下来的压缩包项目上传至GitHub仓库

import os
import zipfile
import shutil
from github import Github


def unzip_and_cd(zip_file_path):
    # 解压缩压缩包至同名文件夹
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.splitext(zip_file_path)[0])

    # 获取解压后的文件夹名称
    folder_name = os.path.splitext(zip_file_path)[0]

    # 利用系统命令cd进入文件夹目录
    os.chdir(folder_name)


def git_init(repository_path):
    # 判断是否存在旧的.git文件夹，如果存在则删除
    git_folder_path = os.path.join(repository_path, '.git')
    if os.path.exists(git_folder_path):
        shutil.rmtree(git_folder_path)      #递归删除文件夹

    os.chdir(repository_path)
    os.system('git init')


def create_github_repo(repo_name, github_token, organization_name, description):
    g = Github(github_token)
    org = g.get_organization(organization_name)
    repo = org.create_repo(repo_name, private=False, description=description)
    return repo.clone_url


def modify_gitignore(repository_path):
    gitignore_path = os.path.join(repository_path, '.gitignore')
    if not os.path.exists(gitignore_path):
        # 如果.gitignore文件不存在，创建一个空的.gitignore文件
        with open(gitignore_path, 'w') as gitignore_file:
            pass
    with open(gitignore_path, 'a') as gitignore_file:
        gitignore_file.write('node_modules \n .DS_Store \n .cache \n .vscode \n .upm \n .config \n')


def git_push(repository_path, remote_url):
    os.chdir(repository_path)
    os.system('git add .')
    os.system('export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890')
    os.system('git commit -m "test commit"')
    os.system(f'git remote add origin {remote_url}')
    os.system('git push -u origin master')


if __name__ == '__main__':
    # macOS 下载文件夹路径
    download_folder = '/Users/lzl/Downloads/'

    ##############################
    file_name = ''  # 必须写
    repo_description = '🍶 飞书 base ' + ''  # 填写简介内容
    repository_name = 'BaseScript-' + file_name    # 替换为你的仓库名
    github_token = ''
    organization_name = 'ConnectAI-E'  # 替换为你的组织名
    ##############################

    zip_file_path = download_folder + file_name + ".zip"
    unzip_and_cd(zip_file_path)

    # 文件夹路径（直接指向压缩包的路径）
    repository_path = os.path.join(download_folder, file_name)

    # 初始化git仓库
    git_init(repository_path)

    # 创建GitHub组织内的仓库并获取远程URL
    remote_url = create_github_repo(repository_name, github_token, organization_name, repo_description)

    # 修改.gitignore文件
    modify_gitignore(repository_path)

    # 将代码推送到GitHub仓库
    git_push(repository_path, remote_url)

    print('自动创建仓库完成！')
