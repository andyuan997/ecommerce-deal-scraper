import re

from config import Config

def extract_context_by_sentence(text, keyword):
    """
    利用正則表達式將文本拆分成句子，然後回傳包含關鍵字的所有句子。
    這裡使用的句子分割規則會以中文或英文標點作為結尾符。
    """
    # 使用中文或英文句號、問號、驚嘆號作為句子結尾符進行分割
    sentences = re.split(r'(?<=[。！？.!?])\s+', text)
    matched = []
    for sentence in sentences:
        if re.search(re.escape(keyword), sentence, re.IGNORECASE):
            matched.append(sentence)
    return matched

async def keywords_filter_with_context(text):
    """
    遍歷關鍵字列表，檢查每個關鍵字是否出現在文本中，
    如果出現則利用句子分割方法提取包含該關鍵字的上下文（句子），
    返回一個字典：{keyword: [句子列表]}。
    """
    results = {}
    for kw in Config.keywords:
        contexts = extract_context_by_sentence(text, kw)
        if contexts:
            results[kw] = contexts
    return results

