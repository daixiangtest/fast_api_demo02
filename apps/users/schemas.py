from pydantic import BaseModel,Field


class RegisterModel(BaseModel):
    """
    注册参数
    """
    userName:str=Field(min_length=2,max_length=20,description="用户名")
    password:str=Field(min_length=6,max_length=20,description="密码")
    password_confirm:str=Field(min_length=6,max_length=20,description="确认密码")


class LoginModel(BaseModel):
    """
    登录参数
    """
    userName:str=Field(min_length=2,max_length=20,description="用户名")
    password:str=Field(min_length=6,max_length=20,description="密码")

class UserModel(BaseModel):
    """
    返回的用户信息
    """
    userName:str=Field(min_length=2,max_length=20,description="用户名")
    sex:bool=Field(description="性别")
    age:int=Field(gt=0,lt=100,description="年龄")
    addres:str=Field(min_length=0,max_length=20,description="地址")
    email:str=Field(min_length=0,max_length=20,description="邮箱")
    id:int=Field(gt=0,description="id")