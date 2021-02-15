from django.shortcuts import render,redirect
from django.http import JsonResponse,QueryDict
from kubernetes import client
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
                os.remove(file_path)
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
                os.remove(file_path)
        res = {"code": code, "msg": msg}
        return JsonResponse(res)

def logout(request):
    request.session.flush()
    return redirect(login)

# 命名空间API
def namespace_api(request):
    if request.method == "GET":
        auth_type = request.session.get('auth_type')
        token = request.session.get('token')
        k8s.load_auth_config(auth_type, token)
        core_api = client.CoreV1Api()
        search_key = request.GET.get('search_key')
        data = []
        try:
            for ns in core_api.list_namespace().items:
                name = ns.metadata.name
                labels = ns.metadata.labels
                ctime = ns.metadata.creation_timestamp
                namespace = {'name': name, 'labels': labels, 'ctime': ctime}
                # 根据搜索值返回数据
                if search_key:
                    if search_key in name:
                        data.append(namespace)
                else:
                    data.append(namespace)
                code = 0
                msg = '获取数据成功'
        except Exception as e:
            code = 1
            status = getattr(e, "status")
            if status == 403:
                msg = "没有访问权限"
            else:
                msg = "获取数据失败"

        # 分页功能
        count = len(data)
        if request.GET.get("page"):
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get('limit'))
            start = (page -1) * limit
            end = page * limit
            data = data[start:end]
        res = {'code': code, 'msg': msg, 'count': count, 'data': data}
        return JsonResponse(res)
    elif request.method == "DELETE":
        request_data = QueryDict(request.body)
        name = request_data.get('name')
        auth_type = request.session.get('auth_type')
        token = request.session.get('token')
        k8s.load_auth_config(auth_type, token)
        core_api = client.CoreV1Api()
        try:
            core_api.delete_namespace(name)
            code = 0
            msg = '删除成功'
        except Exception as e:
            code = 1
            status = getattr(e, "status")
            if status == 403:
                msg = "没有删除权限"
            else:
                msg = "删除失败"
        res = {'code': code, 'msg': msg}
        return JsonResponse(res)

# 命名空间页面
def namespace(request):
    return render(request, 'k8s/namespace.html')