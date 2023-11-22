from tortoise import fields
from tortoise import Model

import datetime
import secrets


# Create your Model here.
class CodeStorage(Model):
    email = fields.CharField(max_length=20)
    code = fields.CharField(max_length=6, unique=True)
    last_sent = fields.DatetimeField()  # 这里的auto_created=True是为了解决makemigrations时的报错
    count = fields.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Code_Storage"

    async def add_code(self, email, code):
        self.email = email
        self.code = code
        self.last_sent = datetime.datetime.now(datetime.timezone.utc)
        self.count = 1
        await self.save()

    async def verify_code(self, code, email):
        if self.code == code and self.email == email:
            return True
        else:
            return False

    async def delete(self, using=None, keep_parents=False):
        await super().delete(using, keep_parents)
        return True


class TotalUsage(Model):
    count = fields.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Total_Usage"

    async def add_usage(self):
        self.count += 1
        await self.save()

    async def get_usage(self):
        return self.count


class LazyEmailVerify(Model):
    """
    :param: None
    :structure: email, temp_email, verify_value, expire_time
    """
    email = fields.CharField(max_length=20)
    temp_email = fields.CharField(max_length=20)
    verify_value = fields.CharField(max_length=24)
    expire_time = fields.DatetimeField()

    class Meta:
        verbose_name_plural = "Lazy_Email_Verify"

    async def add_verify(self, email):
        self.email = email
        self.temp_email = email
        self.verify_value = secrets.token_hex()[:24]
        self.expire_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
        await self.save()


class BlockedDomain(Model):
    domain = fields.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Blocked_Domain"

    async def add_blocked_domain(self, domain):
        self.domain = domain
        await self.save()

    async def check_block_domain(self, domain):
        if self.domain == domain:
            return True
        else:
            return False
