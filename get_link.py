from pyhocon import ConfigFactory
from telethon import TelegramClient

from send_email import send

if __name__ == '__main__':
    conf = ConfigFactory.parse_file('default.conf')
    phone = conf.get_string('info.phone')
    api_id = conf.get_string('info.api_id')
    api_hash = conf.get_string('info.api_hash')
    useProxy = conf.get_string('info.useProxy')
    email_password = conf.get_string('info.email_password')

    proxy = None
    if useProxy is not None and useProxy != "false":
        host = "127.0.0.1"
        port = 1080
        proxy = ("socks5", host, port)

    client = TelegramClient(phone, api_id, api_hash, proxy=proxy).start()

    async def dow():
        messages = list()
        dialog = await client.get_entity('freenodeme')
        async for msg in client.iter_messages(dialog, limit=1):
            messages.append(msg.message)
        dialog = await client.get_entity('kxswa')
        async for msg in client.iter_messages(dialog, limit=10, search="订阅链接"):
            messages.append(msg.message)
        mail_body = "".join(messages)
        print(mail_body)
        send(mail_body, email_password)

    client.loop.run_until_complete(dow())
