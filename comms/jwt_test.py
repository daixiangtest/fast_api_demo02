import time
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from comms.settings import SECRET_KEY


def create_token(token_data: dict):
    """
    创建token
    :param token_data:
    :return:
    """
    secret_key = SECRET_KEY
    token_data.update({"exp": time.time() + 3600 * 24})
    token_value = jwt.encode(token_data, secret_key, algorithm="HS256")
    return token_value


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
def verify_token(token_value: str = Depends(oauth2_scheme)):
    """
    校验token是否有效
    :param token_value:
    :return:
    """
    secret_key = SECRET_KEY
    try:
        token_data = jwt.decode(token_value, secret_key, algorithms=["HS256"])
        return token_data
    except Exception as e:
        raise HTTPException(status_code=401, detail="token验证失败")


if __name__ == '__main__':
    data = {"id": 1, "name": "dx"}
    token = create_token(data)
    print(token)
    time.sleep(2)
    print(verify_token(token))
