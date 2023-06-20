import subprocess
from git import Repo
from utils.base64_turn import  str2base64str


def clone(repo, dir):
    '''
    远端仓库地址和保存至本地哪个文件夹下
    '''
    ret, out = subprocess.getstatusoutput(
        'cd {} && git clone {}'.format(dir, repo))
    if ret == 128 or ret == 0:
        aind = out.find("'")
        bind = out.rfind("'")
        # print(ret)
        return {'status': 200, 'reponame': out[aind+1:bind]}
    return {'status': 400, 'info': out}


def commit(commitname, dir):
    ret, out = subprocess.getstatusoutput(
        'cd {} && git add . && git commit -m "{}"'.format(dir, commitname))
    # print(out)
    if ret == 0:
        return True
    print(out)
    return False

def checkout(dir, hashcode):
    """
    通过git切换版本
    """
    # 会有个nul文件里面有checkout相关
    # ret, out = subprocess.getstatusoutput(
    #     'cd {} && git checkout 1>nul 2>nul {}'.format(dir, hashcode))
    ret, out = subprocess.getstatusoutput(
        'cd {} && git checkout {}'.format(dir, hashcode))
    # if ret==0:
    # 成功
    return ret


infomat = ["hash", "name", "time", "title"]


def log(dir):
    '''
    输出commit记录
    :param dir: 本地项目的文件夹绝对路径
    '''
    # hash comitter time title
    try:
        ret, out = subprocess.getstatusoutput(
            'cd {} && git log --all --encoding=GBK --pretty=format:"%H%n%cn%n%ci%n%s%n"'.format(dir))
    except Exception as e:
        ret, out = subprocess.getstatusoutput(
            'cd {} && git log --all --encoding=utf8 --pretty=format:"%H%n%cn%n%ci%n%s%n"'.format(dir))
    return [dict(zip(infomat, each.split("\n"))) for each in out.split("\n\n")]

def nowcommit(dir):
    '''
    现在所处的commit的hash
    '''
    ret, out = subprocess.getstatusoutput(
        'cd {} && git rev-parse HEAD'.format(dir))
    return out

def diff(dir):
    '''
    冲突时 查看远端与本地文件差异
    '''
    repo=Repo(dir)
    diffres=repo.git.diff("--cached").split("\n")

    diffres=[str2base64str(res.strip().split(" ")[3]) for res in diffres]
    return diffres


def push(dir):
    '''
    push
    '''
    repo=Repo(dir)
    res=repo.git.push()
    return res

def pull(dir):
    """
    pull
    """
    repo=Repo(dir)
    try:
        pullres=repo.git.pull()
    except Exception as e:
        if "conflict" in str(e) or "unmerged" in str(e):
            return False
    return True
