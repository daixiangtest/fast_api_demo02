from tortoise import Model
from tortoise import fields


class UserInfoModel(Model):
    id = fields.IntField(pk=True, description="id")
    userName = fields.CharField(max_length=255, description="用户名")
    addres = fields.TextField(description="地址",default="")
    age = fields.IntField(description="年龄",default=16)
    sex = fields.BooleanField(default=True, description="性别")
    email=fields.CharField(max_length=255, description="邮箱",default="")
    password = fields.CharField(max_length=255, description="密码")
    def __str__(self):
        return self.userName

    class Meta:
        table = 'user_test'