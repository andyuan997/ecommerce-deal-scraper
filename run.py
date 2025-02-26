import asyncio
import json
import os

from playwright_scrape import fetch_page_text
from keywords_filter import keywords_filter_with_context
from config import Config
from google_llm import process_with_gemini, extract_generated_text
from send_discord import send_discord_notification

async def main():
    # 複製網站列表以便在 while 迴圈中逐一處理
    websites = Config.websites.copy()

    # 確保儲存結果的資料夾存在
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)

    while websites:
        url = websites.pop(0)
        page_text = await fetch_page_text(url)
        matched_with_context = await keywords_filter_with_context(page_text)

        # 將 URL 轉換為合法的檔名
        safe_url = url.replace("://", "_").replace("/", "_")
        file_path = os.path.join(output_dir, f"{safe_url}.json")

        # 檢查是否已有先前存檔的結果
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                old_content = json.load(f)
            # 比較新舊內容是否不同
            if old_content != matched_with_context:
                print(f"\n【檢測到網站 {url} 內容變動】")
                # 傳送變動內容至 Google Gemini LLM 處理
                gemini_response = await process_with_gemini(str(matched_with_context))
                gemini_result = extract_generated_text(gemini_response)
                print("Google Gemini 處理結果：", gemini_result)

                # 發送 Discord 通知，內容包含變動摘要
                notification_message = f"網站 {url} 內容有更新！\n摘要：\n{gemini_result}"
                await send_discord_notification(notification_message)
            else:
                print(f"\n【網站 {url} 內容無變動】")
        else:
            print(f"\n【第一次抓取網站 {url}，保存內容】")

        # 儲存最新的結果到 JSON 檔案（若已存在則覆蓋）
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(matched_with_context, f, ensure_ascii=False, indent=2)
        print(f"結果已儲存至 {file_path}")

if __name__ == "__main__":
    asyncio.run(main())
