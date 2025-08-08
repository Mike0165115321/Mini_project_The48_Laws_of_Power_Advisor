# core/power_advisor.py (Final Async & Resilient Version)
import google.generativeai as genai
import json
import asyncio
import traceback
from .rag_engine import RAGEngine
from .api_key_manager import ApiKeyManager, AllKeysOnCooldownError
from typing import List

class PowerAdvisor:
    def __init__(self, rag_engine: RAGEngine, key_manager: ApiKeyManager):
        self.rag_engine = rag_engine
        self.key_manager = key_manager
        self.prompt_template = """
        คุณคือ "Power Strategist" ผู้เชี่ยวชาญที่เข้าใจ "The 48 Laws of Power" อย่างลึกซึ้งราวกับเป็นผู้เขียนเอง คุณไม่ใช่แค่ AI แต่เป็นที่ปรึกษาส่วนตัวที่สุขุมและทรงภูมิ

**ภารกิจของคุณ:**
ตอบคำถามของผู้ใช้โดยใช้ความรู้จาก "เนื้อหาอ้างอิง" ที่ให้มาเท่านั้น สังเคราะห์ข้อมูลเหล่านั้นให้กลายเป็นคำแนะนำที่เฉียบคมและนำไปใช้ได้จริง

**ศิลปะแห่งการสนทนา:**
- **เริ่มต้นอย่างทรงพลัง:** เริ่มต้นคำตอบด้วยประโยคสรุปที่ตรงประเด็นและน่าสนใจ
- **อธิบายอย่างชัดเจน:** ขยายความประเด็นหลักด้วยภาษาที่เข้าใจง่าย หลีกเลี่ยงศัพท์เทคนิคที่ไม่จำเป็น
- **ใช้ตัวอย่าง (ถ้ามีในเนื้อหา):** อ้างอิงตัวอย่างจากเนื้อหาเพื่อทำให้คำแนะนำของคุณเห็นภาพชัดเจนขึ้น
- **คงไว้ซึ่งอำนาจ:** ใช้โทนเสียงที่มั่นคง, สุขุม, และให้ความรู้สึกเหมือนกำลังได้รับคำแนะนำจากผู้มีประสบการณ์สูง
- **กฏเหล็ก:** ห้ามตั้งคำถามกลับโดยเด็ดขาด หน้าที่ของคุณคือการให้คำตอบ ไม่ใช่การถาม

---
**เนื้อหาอ้างอิง:**
{context}
---

**คำถาม:** {question}

**คำตอบที่เฉียบคมของคุณ:**
        """
        
        self.canned_responses = {
            "greeting": {
                "keywords": ["สวัสดี", "หวัดดี", "hello"],
                "response": "สวัสดีครับ ผมคือ Power Strategist มีอะไรให้ผมรับใช้เกี่ยวกับกลยุทธ์แห่งอำนาจบ้างครับ"
            },
            "thanks": {
                "keywords": ["ขอบคุณ", "ขอบใจ", "thank"],
                "response": "ด้วยความยินดี หากมีคำถามอื่นใดที่ต้องการความชัดเจน ถามได้เสมอ"
            },
            "farewell": {
                "keywords": ["ลาก่อน", "บ๊ายบาย", "bye"],
                "response": "ลาก่อน ขอให้คุณใช้กลยุทธ์ที่ได้เรียนรู้อย่างชาญฉลาด"
            }
        }

    async def answer_stream(self, query: str):
        normalized_query = query.lower().strip()
        for intent, data in self.canned_responses.items():
            for keyword in data["keywords"]:
                if keyword in normalized_query:
                    yield f"data: {json.dumps({'text': data['response']})}\n\n"
                    return 
        
        api_key = None
        try:
            search_results = self.rag_engine.search_books(query=query, top_k_rerank=3)
            context = search_results.get("context")
            sources = search_results.get("sources", [])

            if not context:
                yield f"data: {json.dumps({'error': 'ในคลังความรู้ของผม ไม่พบข้อมูลที่เกี่ยวข้องกับคำถามนั้น'})}\n\n"
                return

            yield f"data: {json.dumps({'sources': sources})}\n\n"

            api_key = self.key_manager.get_key()
            genai.configure(api_key=api_key)
            
            prompt = self.prompt_template.format(context=context, question=query)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            response = await model.generate_content_async(prompt, stream=True)
            
            async for chunk in response:
                if hasattr(chunk, 'text') and chunk.text:
                    yield f"data: {json.dumps({'text': chunk.text})}\n\n"
                    await asyncio.sleep(0.01)

        except AllKeysOnCooldownError as e:
            yield f"data: {json.dumps({'error': f'ขณะนี้ระบบมีผู้ใช้งานหนาแน่น กรุณาลองใหม่อีกครั้ง ({e})'})}\n\n"
        
        except Exception as e:
            if api_key:
                self.key_manager.report_failure(api_key, error_type='generic')
            
            print(f"--- ❌ Error in PowerAdvisor Stream ---")
            traceback.print_exc()
            yield f"data: {json.dumps({'error': f'เกิดข้อผิดพลาดในการประมวลผล: {type(e).__name__}'})}\n\n"