## ecommerce-deal-scraper

### 功能
- 這個程式可以定時爬取你所指定的多個網站，透過有關優惠的關鍵字搜索文字段落，如果有變動則將文字透過 Google Gemini LLM 解析，並發送至 discord 通知。
- 只需要修改config.json就可以根據你的需求，應用在你需要的場景上。

### 主要特性
- **定時爬取**：透過 crontab 或其他排程工具定期執行爬蟲，保持資料的最新狀態。
- **關鍵字過濾**：自訂優惠相關關鍵字，僅抓取你所感興趣的文字段落。
- **變更檢測與解析**：當網站內容有更新時，利用 Google Gemini LLM 進行智能解析，避免重複處理無意義的 Token 消耗。
- **Discord 通知**：將重要變更或解析後的內容推送至指定 Discord 頻道，確保你不會錯過任何優惠信息。

### 使用步驟
#### 1. Git Clone 專案
在終端機中執行以下命令以取得專案：
```bash
git clone https://github.com/andyuan997/ecommerce-deal-scraper.git
```

#### 2. 進入專案目錄
```bash
cd ecommerce-deal-scraper
```

#### 3. 生成依賴文件 (Requestment)
```bash
pip install -r requirements.txt
```

#### 4. 設定 config.json
根據你的需求修改 config.json 中的設定（例如目標網站列表、關鍵字、Discord Webhook URL、Google Gemini API Key 等）。

#### 5-1. 純執行
你可以直接執行主程式以測試：
```bash
python main.py
```

#### 5-2. 使用 Cron Tab 每日執行
編輯 `crontab`，加入如下排程，每天執行一次程式：
1. 開啟編輯
```bash
crontab -e
```
2. 根據你的路徑設定每日排程
```bash
0 0 * * * /usr/bin/python /path/to/ecommerce-deal-scraper/main.py >> /path/to/ecommerce-deal-scraper/cron.log 2>&1
```



