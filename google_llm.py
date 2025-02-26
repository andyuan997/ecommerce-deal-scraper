import aiohttp
import asyncio
from config import Config

async def process_with_gemini(text: str) -> dict:
    """
    呼叫 Google Gemini API 處理文字，並回傳生成結果。
    這裡先用一個簡單的 prompt 測試 payload 格式。
    """
    prompt = """請根據以下資料提取所有與優惠、折扣、促銷等相關的資訊，
    並生成一份條列式摘要。摘要應該簡短精煉，
    僅保留與優惠相關的內容，同時保留原始資料中的關鍵文字。
    請移除所有與優惠無關的敘述。""" + text

    # 使用 parts 為物件列表的方式
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    # API endpoint
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={Config.GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                return {"error": f"Request failed with status {response.status}: {error_text}"}

def extract_generated_text(response: dict) -> str:
    try:
        candidate = response.get('candidates', [])[0]
        # 嘗試使用 parts 中的物件格式
        text = candidate.get('content', {}).get('parts', [])[0].get('text', '')
        return text
    except (IndexError, AttributeError):
        return ""

# 測試用範例
if __name__ == "__main__":
    sample_text = "本店現正推出夏季優惠活動，所有夏裝享有20%折扣，買二送一活動僅限本週。"
    result = asyncio.run(process_with_gemini(sample_text))
    if "error" in result:
        print("Error:", result["error"])
    else:
        generated_text = extract_generated_text(result)
        print("生成的文字內容：\n", generated_text)
