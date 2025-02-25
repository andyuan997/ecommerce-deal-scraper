import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def fetch_page_text(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # 無頭模式
        page = await browser.new_page()
        # 設定 User-Agent
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        })
        print(f"正在打開頁面: {url}")
        await page.goto(url, timeout=60000)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(3)  # 根據實際情況調整等待時間

        # 取得整頁 HTML
        html = await page.content()
        await browser.close()

        # 使用 BeautifulSoup 解析並清洗 HTML
        soup = BeautifulSoup(html, "html.parser")
        # 移除不必要的區塊
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            tag.decompose()
        # 提取純文字（以空白分隔）
        text = soup.get_text(separator=" ", strip=True)
        return text

