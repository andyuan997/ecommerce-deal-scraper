import asyncio

from playwright_scrape import fetch_page_text
from keywords_filter import keywords_filter_with_context
from config import Config

async def main():
    # 複製網站列表以便在 while 迴圈中逐一處理
    websites = Config.websites.copy()
    while websites:
        url = websites.pop(0)
        page_text = await fetch_page_text(url)
        matched_with_context = await keywords_filter_with_context(page_text)
        print(f"\n【在網站 {url} 上匹配到的關鍵字及上下文：】")
        for kw, contexts in matched_with_context.items():
            print(f"\n關鍵字: {kw}")
            for i, ctx in enumerate(contexts, 1):
                print(f"  匹配 {i}: {ctx}")


if __name__ == "__main__":
    asyncio.run(main())
