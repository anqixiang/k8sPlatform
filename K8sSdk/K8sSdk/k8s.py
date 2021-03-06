#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :k8s.py
# @Time      :2021/3/6 10:41
# @Author    :运维@小兵
# @Function  :

from kubernetes import config,client

# config.load_kube_config(r'E:\学习\python\django\project\k8sPlatform\K8sSdk\K8sSdk\config')
# apps_api = client.AppsV1Api()

configuration = client.Configuration()
configuration.host = "https://192.168.137.2:6443"
configuration.ssl_ca_cert = r'E:\学习\python\django\project\k8sPlatform\K8sSdk\K8sSdk\ca.crt'
configuration.verify_ssl = True
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImlZVXc5RHZQckZubUotZzNES3BtSEROejRyT3QySG1kMlZ6TXNrYW5UWFUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tOGhsOHEiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiYzAyZDQ1MzktNDY4My00YWE5LWIxODctNDBkZDBkNWIwZWRlIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.0nx74MKfOrToRTkjF8Uv-CawmlhCNa2cx9ORdXiOvQkSzvrwlgIF_R2Fgm4CfcJgnMI6oBqpKfhBOSnF-N3akjC4lf5OcTMeJvq_1cw8iKlfp9f16AN5y-4mR8TERELKPtiGElp53vsHsTEhyjKwDNip5mrzWOx7FP9uKlcJofnn-EE_SRZnouYHrtlZaJgJPZ2zo8-Sx8oLLgbTrG_PR-idZAgpsWAKlYBdquSeFQ9nQ16i-AhgpdrPRttFVSiSH90avPEjzSmU0cgyy0WrHGe4-pRtD7r0zSWFv_7vkjRh2A3P7nmn7Pr2TeTTLR9X74JSj5N3BYace-y_CtVkLw"
configuration.api_key = {"authorization": "Bearer " + token}    # 指定Token字符串
client.Configuration.set_default(configuration)

apps_api = client.AppsV1Api()
for info in apps_api.list_namespaced_deployment(namespace="kube-system").items:
    print(info.metadata.name)

if __name__ == "__main__":
    run_code = 0