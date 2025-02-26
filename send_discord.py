import aiohttp
from config import Config

async def send_discord_notification(message: str):
    """
    發送 Discord 通知，利用 webhook 方式。
    """
    async with aiohttp.ClientSession() as session:
        payload = {"content": message}
        async with session.post(Config.DISCORD_WEBHOOK_URL, json=payload) as response:
            if response.status in (200, 204):
                print("Discord 通知已成功發送。")
            else:
                print(f"Discord 通知發送失敗，狀態碼：{response.status}")