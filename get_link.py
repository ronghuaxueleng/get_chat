import re

import requests
from pyhocon import ConfigFactory
from telethon import TelegramClient

from proxyUtils import get_proxy
from send_mail import SendMail

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
        try:
            proxies = get_proxy()
            dialog = await client.get_entity('freenodeme')
            async for msg in client.iter_messages(dialog, limit=1):
                print(msg.message)
                urls = re.findall(r"https://freenode\.me\S+\.html", msg.message)
                data = requests.get(urls[0], proxies=proxies)
                text = data.text
                clashUrls = re.findall(r"https://freenode\.me/wp-content/uploads/\d{4}/\d{2}/\S+\.yaml", text)
                file = requests.get(clashUrls[0], proxies=proxies, stream=True)
                file.encoding='utf-8'
                with open("clash.yaml", "wb") as f:
                    f.write(file.content)
        except Exception as e:
            pass
        dialog = await client.get_entity('kxswa')
        async for msg in client.iter_messages(dialog, limit=10, search="订阅链接"):
            messages.append(msg.message)
        mail_body = "\n".join(messages)
        print(mail_body)
        file_list = ["clash.yaml"]
        SendMail(mail_body, email_password).send(file_list)

    client.loop.run_until_complete(dow())
