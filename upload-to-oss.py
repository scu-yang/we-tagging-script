# -*- coding=utf-8
# 使用 pip 安装sdk：pip install -U cos-python-sdk-v5
import argparse
import os.path

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

# 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKIDU5ZrxtkQMFxSkrnYAB72rUwDIAoIbgW9'     # 替换为用户的 SecretId，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
secret_key = 'XpBPTLzOwU6fBxjNtEPxKYaRJ5jFZs34'   # 替换为用户的 SecretKey，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
region = 'ap-chengdu'    # 替换为用户的 region，已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                           # COS支持的所有region列表参见https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
client = CosS3Client(config)


parser = argparse.ArgumentParser()

parser.add_argument('-f', '--filePath', type=str,  help='file path')
args = parser.parse_args()
path = args.filePath
name = os.path.basename(path)

if __name__ == '__main__':
  with open(path) as fd:
    response = client.put_object(
      Bucket='normal-dev-1308032423',
      Body=fd,
      Key=name,
      EnableMD5=False
    )
    print(response)

