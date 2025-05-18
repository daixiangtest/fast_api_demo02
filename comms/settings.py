
# 迁移配置信息数据库
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "123456",
                "database": "demo02",
            }
        }
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "apps.users.models"],
            "default_connection": "default",
        }
    }
}
# jwt token秘钥
SECRET_KEY="fed1db48d2c825f964b2a15ed17410c3754a519df5c053de964fd75ed14c4a25"