from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user_test` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id',
    `userName` VARCHAR(255) NOT NULL COMMENT '用户名',
    `addres` LONGTEXT NOT NULL COMMENT '地址',
    `age` INT NOT NULL COMMENT '年龄' DEFAULT 16,
    `sex` BOOL NOT NULL COMMENT '性别' DEFAULT 1,
    `email` VARCHAR(255) NOT NULL COMMENT '邮箱' DEFAULT '',
    `password` VARCHAR(255) NOT NULL COMMENT '密码'
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
