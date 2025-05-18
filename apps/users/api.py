import time
from fastapi import BackgroundTasks, HTTPException, APIRouter, Depends
from typing import Union
from comms.jwt_test import create_token,verify_token
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from apps.users.models import UserInfoModel
from apps.users.schemas import UserModel, RegisterModel, LoginModel


router= APIRouter(
    # 路由配置
    prefix="/api/user", # 路由前缀
    tags=["用户中心"],# 路由分组
)


@router.post("/register", status_code=201,response_model=UserModel,description="用户注册描述",summary="用户注册") # 接口的描述和名称
async def register(item: RegisterModel):
    #  密码一致性验证
    if item.password != item.password_confirm:
        raise HTTPException(status_code=400, detail="密码不一致")
    #  验证用户名是否重复
    if await UserInfoModel.filter(userName=item.userName).first():
        raise HTTPException(status_code=400, detail="用户名重复")
    user = await UserInfoModel.create(**item.model_dump())
    return UserModel(**user.__dict__)


@router.post("/login",response_model=UserModel,description="用户登录描述",summary="用户登录")
async def login(item: LoginModel):
    # 验证用户名密码是否正确
    user = await UserInfoModel.get_or_none(userName=item.userName, password=item.password)
    if user:
        return UserModel(**user.__dict__)
    else:
        raise HTTPException(status_code=400, detail="用户名密码错误")


def send_email(id:int):
    print(f"{id}开始发送邮件")
    time.sleep(id)
    print(f"{id}发送邮件成功")
@router.get("/test",description="后台异步任务执行",summary="后台任务")
async def test(task:BackgroundTasks,id:int):
    # send_email(id)
    # 添加异步执行任务，无需等待函数执行完成
    task.add_task(send_email,id)
    return {"message":"任务已开始"}


async def common_parameters(q: Union[str,None] = None, page:int=0, size:int=10):
    return {"q": q, "page": page, "size": size}

@router.get("/depends/demo",description="依赖项测试参数",summary="依赖项测试参数")
#当请求到达时，fastapi 会调用Depends(common_parameters)函数来将函数结果到接口参数中，
async def depends_demo(commons: dict = Depends(common_parameters)):
    return commons

###########注册接口保存加密密码#############
@router.post("/register/token",description="注册接口保存加密密码",summary="注册接口保存加密密码")
async def register_token(item: RegisterModel):
    #  密码一致性验证
    if item.password != item.password_confirm:
        raise HTTPException(status_code=400, detail="密码不一致")
    #  验证用户名是否重复
    if await UserInfoModel.filter(userName=item.userName).first():
        raise HTTPException(status_code=400, detail="用户名重复")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user = await UserInfoModel.create(userName=item.userName,password=pwd_context.hash(item.password))
    return UserModel(**user.__dict__)
###########登录接口保存token和返回token应答#############
@router.post("/login/token",description="登录接口保存token和返回token应答",summary="登录接口保存token和返回token应答")
async def login_token(item: LoginModel):
    # 验证用户名密码是否正确
    user = await UserInfoModel.get_or_none(userName=item.userName)
    if user:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if pwd_context.verify(item.password,user.password):
            # 生成token
            token_data={"userName":user.userName,"id":user.id}
            token=create_token(token_data)
            return {"token":token}
        else:
            raise HTTPException(status_code=400, detail="用户名密码错误")
    else:
        raise HTTPException(status_code=400, detail="用户名不存在")

###########查询接口判断用户token来进行查询#############
@router.get("/query/token",description="查询接口判断用户token来进行查询",summary="查询接口判断用户token来进行查询")
async def query_token(res:Union[dict,None]=Depends(verify_token)):
    """
    Depends(OAuth2PasswordBearer) 方法判断接口有没有上送 bearer token 信息
    Depends 是声明依耐项， OAuth2PasswordBearer 是token的参数格式校验 bearer token_value
    :param res:
    :param token:
    :return:
    """
    if res:
        return {"token_data":res}