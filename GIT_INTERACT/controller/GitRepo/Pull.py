from flask_restful import Resource, reqparse
from flask import current_app,abort,Response,jsonify
import os
from utils.filemanage import foldertree
from utils.gitmanage import nowcommit
from utils.gitmanage import pull,diff

class Pull(Resource):
    
    @staticmethod
    def post():
        # https://blog.csdn.net/qq_27371025/article/details/126721511
        parse = reqparse.RequestParser()
        parse.add_argument('reponame', type=str, help='need reponame', required=True, trim=True, location='form')

        args = parse.parse_args()
        
        reponame=args["reponame"]
        repodir=os.path.join(current_app.config['localstore'],reponame)
        thefoldertree = foldertree(os.path.join(current_app.config['localstore'], reponame),iteractive=True)
        nowcommitid=nowcommit(os.path.join(current_app.config['localstore'], reponame))
        if(pull(repodir)):
            return {"foldertree":thefoldertree,
                    "commitid":nowcommitid}
        else:
            # 显示冲突
            return {'msg':"Some files conflict","foldertree":thefoldertree,'files':diff(repodir)},400
        
