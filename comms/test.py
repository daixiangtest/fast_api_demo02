"""
密码和token的加密校验
pip install passlib[bcrypt]
"""
import time

# from passlib.context import CryptContext
# # ++++++++++++++++++++++密码加密和校验++++++++++++++++++++++++
# # 创建一个加密对象
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# passwd="Dx123456"
# res=pwd_context.hash(passwd)
# print(res)
#
# # 密码校验
# res=pwd_context.verify(passwd,res)
# print(res)


#========================token的处理生成、校验=========================

# import jwt
#
# # 生成一个秘钥
# secret_key="1234567890"
# import secrets
# key=secrets.token_hex(32)
# print(key) #fed1db48d2c825f964b2a15ed17410c3754a519df5c053de964fd75ed14c4a25
#
# key="fed1db48d2c825f964b2a15ed17410c3754a519df5c053de964fd75ed14c4a25"
# data={"id":1,"name":"dx",
#       "exp":time.time()+3  #  过期时间
#       }
# # 生成token
# token=jwt.encode(data,key,algorithm="HS256")
# print(token)
# time.sleep(4)
# # 校验token
# res2=jwt.decode(token,key,algorithms=["HS256"])
# print(res2)