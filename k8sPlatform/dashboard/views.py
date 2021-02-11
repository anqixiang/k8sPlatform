from django.shortcuts import render
from django.http import JsonResponse
from kubernetes import client,config
import os,hashlib,random

# Create your views here.
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
            conf = client.Configuration()
            conf.host = "https://192.168.137.2:6443"    # apiserver地址
            conf.ssl_ca_cert = r"E:\学习\python\django\project\k8sPlatform\k8sPlatform\ca.crt"    # CA证书
            conf.verify_ssl = True      # 启用证书验证，必须指定CA证书
            conf.api_key = {"authorization": "Bearer " + token}     # 指定token
            client.Configuration.set_default(conf)

            try:
                core_api = client.CoreApi()
                core_api.get_api_versions()     # 查询api版本
                code = 0
                msg = "认证成功"
            except Exception as e:
                code = 1
                msg = "token无效！"
        else:
            file_obj = request.FILES.get("file")    # 获取前端上传的文件
            random_str = hashlib.md5(str(random.random()).encode()).hexdigest()     # 生成经过MD5加密的随机数
            file_path = os.path.join('kubeconfig', random_str)  # 拼接路径
            try:
                with open(file_path, 'w', encoding="utf8") as f:
                    data = file_obj.read().decode()     # bytes转str
                    f.write(data)
                # 连接K8S
                config.load_kube_config(r"%s" %file_path)
                core_api = client.CoreApi()
                core_api.get_api_versions()
                code = 0
                msg = "认证成功"
            except Exception:
                code = 1
                msg = "认证文件无效"
                os.remove(file_path)    # 删除无效文件

        res = {"code": code, "msg": msg}
        return JsonResponse(res)