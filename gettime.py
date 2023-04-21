from datetime import datetime
from datetime import timedelta
from datetime import timezone

SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)

# 协调世界时
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_now, utc_now.tzname())
print(utc_now.date(), utc_now.tzname())

# 北京时间
beijing_now = utc_now.astimezone(SHA_TZ)
print(beijing_now.strftime('%Y-%m-%d %H:%M:%S'))
print(beijing_now, beijing_now.tzname())
print(beijing_now.date(), beijing_now.tzname())

# 系统默认时区
local_now = utc_now.astimezone()
print(local_now, local_now.tzname())
print(local_now.date(), local_now.tzname())
