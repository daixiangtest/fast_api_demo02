"""
fast api 支持开发websockets 接口
安装依赖： pip install websockets
"""

from fastapi import WebSocket,APIRouter
from starlette.websockets import WebSocketDisconnect

router = APIRouter()
@router.websocket("/ws/demo")
async def websocket_endpoint(websocket: WebSocket):
    """

    :param websocket:
    :return:
    """
    # 等待客户链接
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect as e:
        print("链接关闭")
    finally:
        if websocket.get("type") == "websocket.disconnect":
            await websocket.close()