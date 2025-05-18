import time
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from apps.users.api import router as user_router
from apps.ws.api import router as ws_router
from comms.settings import TORTOISE_ORM

# 创建应用
app = FastAPI(
    title="fastapi测试练习项目",
    description="学习和联系使用的项目",
    version="0.0.1",
    debug=True,
)

# 注册路由
app.include_router(user_router)
# 注册websocket路由
app.include_router(ws_router)

# 自定义全局异常处理应答
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    全局请求参数异常处理
    :param request:
    :param exc:
    :return:
    """
    body = await request.body()
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "request_body": body.decode("utf-8")}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    全局 http 异常处理
    :param request:
    :param exc:
    :return:
    """
    body = await request.body()
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "request_body": body.decode("utf-8")}
    )


#  注册数据库
register_tortoise(app=app, config=TORTOISE_ORM)

# 跨域请求和中间件设置
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"])

# 中间件处理（夹具）

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    中间件处理（夹具）
    :param request:
    :param call_next:
    :return:
    """
    start_time = time.time()
    # 记录接口每次执行的时间
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8002)
    """
    项目运行步骤
    首次迁移数据
        初始化模型生成迁移文件
        aerich init -t main.TORTOISE_ORM
        初始化数据库连接并创建表
        aerich init-db
    后续变更模型执行
        修改模型后执行生成新的迁移文件
        aerich migrate
        更改表结构
        aerich upgrade
    运行文件启动服务
    通过fastapi 终端运行

    """
