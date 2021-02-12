#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :k8s.py
# @Time      :2021/2/11 15:03
# @Author    :运维@小兵
# @Function  :

from kubernetes import client,config
import os
from django.shortcuts import redirect

# 登录认证
def auth_check(auth_type, str):
    if auth_type == "token":
        token = str
        conf = client.Configuration()
        conf.host = "https://192.168.137.2:6443"  # apiserver地址
        conf.ssl_ca_cert = r"E:\学习\python\django\project\k8sPlatform\k8sPlatform\ca.crt"  # CA证书
        conf.verify_ssl = True  # 启用证书验证，必须指定CA证书
        conf.api_key = {"authorization": "Bearer " + token}  # 指定token
        client.Configuration.set_default(conf)
        try:
            core_api = client.CoreApi()
            core_api.get_api_versions()  # 查询api版本
            return True
        except Exception:
            return False
    elif auth_type == "kubeconfig":
        file_name = str
        file_path = os.path.join("kubeconfig", file_name)
        config.load_kube_config(r"%s" % file_path)
        try:
            core_api = client.CoreApi()
            core_api.get_api_versions()  # 查询api版本
            return True
        except Exception as e:
            print(e)
            return False

# 登录认证装饰器
def self_login_required(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get("is_login", False)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/login')
    return inner

if __name__ == "__main__":
    run_code = 0