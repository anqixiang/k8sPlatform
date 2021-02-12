from django.shortcuts import render
from django.http import JsonResponse
from kubernetes import client,config
import os,hashlib,random
from k8sPlatform import k8s

# Create your views here.
@k8s.self_login_required
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        # print(request.POST)
        # 验证token
        token = request.POST.get("token", None)   # 获取前端的token
        if token:
            if k8s.auth_check("token", token):
                # 定义sesseion信息
                request.session['is_login'] = True
                request.session['auth_type'] = 'token'
                request.session['token'] = token
                # 返回前端消息
                code = 0
                msg = "认证成功"
            else:
                code = 1
                msg = "token无效！"
        else:
            file_obj = request.FILES.get("file")    # 获取前端上传的文件
            random_str = hashlib.md5(str(random.random()).encode()).hexdigest()     # 生成经过MD5加密的随机数,用作kubeconfig的名字
            file_path = os.path.join("kubeconfig", random_str)
            try:
                with open(file_path, 'w', encoding="utf8") as f:
                    data = file_obj.read().decode()     # bytes转str
                    f.write(data)

            except Exception:
                code = 1
                msg = "文件类型错误！"
                res = {"code": code, "msg": msg}
                return JsonResponse(res)
            if k8s.auth_check("kubeconfig", random_str):
                # 定义sesseion信息
                request.session['is_login'] = True
                request.session['auth_type'] = 'kubeconfig'
                request.session['token'] = random_str
                # 返回前端消息
                code = 0
                msg = "认证成功"
            else:
                code = 1
                msg = "认证文件无效！"
        res = {"code": code, "msg": msg}
        return JsonResponse(res)