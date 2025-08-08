# Power Strategist AI 🧠

**Power Strategist AI** คือโปรเจกต์ Full-Stack AI Chatbot ที่ทำหน้าที่เป็นผู้เชี่ยวชาญและที่ปรึกษาส่วนตัวเกี่ยวกับหนังสือ "The 48 Laws of Power" แอปพลิเคชันนี้ถูกสร้างขึ้นเพื่อสาธิตการทำงานของสถาปัตยกรรม RAG (Retrieval-Augmented Generation) ที่ทันสมัย โดยสามารถตอบคำถามที่ซับซ้อนโดยอ้างอิงเนื้อหาจากในหนังสือได้อย่างแม่นยำและมี "บุคลิก" ของผู้เชี่ยวชาญ

![Power Strategist AI Screenshot](URL_ของภาพหน้าจอโปรเจกต์ของคุณ.png)
> **Note:** คุณสามารถถ่ายภาพหน้าจอโปรเจกต์ที่ทำงานเสร็จแล้ว, อัปโหลดไปใน GitHub issue ของ repo นี้, แล้วคัดลอก URL ของภาพมาใส่แทนที่ `URL_ของภาพหน้าจอโปรเจกต์ของคุณ.png` ได้เลย

---

## ✨ Features

- **AI ที่ปรึกษาส่วนตัว:** สนทนากับ AI ที่มีความรู้ความเข้าใจใน "The 48 Laws of Power" อย่างลึกซึ้ง
- **ตอบคำถามด้วย RAG:** คำตอบทั้งหมดถูกสร้างขึ้นโดยอ้างอิงจากเนื้อหาในหนังสือจริง ไม่ใช่การคาดเดา
- **Streaming Responses:** ได้รับคำตอบแบบ Real-time ที่ข้อความจะค่อยๆ พิมพ์ออกมาเหมือน ChatGPT
- **Humanized Conversation:** AI สามารถจัดการบทสนทนาพื้นฐานได้ (ทักทาย, ขอบคุณ)
- **Thematic UI:** หน้าเว็บที่ออกแบบมาอย่างสวยงามในธีมสีแดงทรงพลัง สร้างประสบการณ์ที่ไม่เหมือนใคร

---

## 🏛️ สถาปัตยกรรมและเทคโนโลยี

นี่คือโปรเจกต์ Full-Stack ที่ให้บริการทั้ง Backend และ Frontend จากที่เดียวกัน

### Backend

- **Framework:** FastAPI (Python)
- **AI Model:** Google Gemini 1.5 Flash
- **Core Technology:** RAG (Retrieval-Augmented Generation)
  - **Embedding Model:** `intfloat/multilingual-e5-large` (รองรับภาษาไทย)
  - **Reranker Model:** `BAAI/bge-reranker-base` (เพิ่มความแม่นยำในการค้นหา)
  - **Vector Database:** FAISS (ทำงานบน CPU)
- **Key Features:**
  - **Resilient API Key Manager:** ระบบจัดการ API Key อัจฉริยะที่ทนทานต่อข้อผิดพลาด พร้อมกลไก Smart Throttling
  - **Streaming API:** ให้บริการคำตอบแบบ Real-time ผ่าน `StreamingResponse`

### Frontend

- **Framework:** Vanilla HTML, CSS, JavaScript (ไม่มีเฟรมเวิร์กซับซ้อน)
- **Styling:** Custom CSS ที่ออกแบบมาสำหรับโปรเจกต์นี้โดยเฉพาะ
- **Key Features:**
  - **Single-Page Application (SPA):** ประสบการณ์การใช้งานที่ลื่นไหลในหน้าเดียว
  - **Dynamic UI:** แสดงผลข้อความที่ได้รับจาก Streaming API แบบ Real-time

---

## 🚀 การติดตั้งและใช้งาน

### 1. เตรียมการ

1.  **Clone a Repository:**
    ```bash
    git clone https://github.com/Mike0165115321/The-48-Laws-of-Power-Advisor.git
    cd The-48-Laws-of-Power-Advisor
    ```
2.  **สร้างและเปิดใช้งาน Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **ติดตั้ง Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **สร้างไฟล์ `.env`** ในโฟลเดอร์หลัก และใส่ `GOOGLE_API_KEYS` ของคุณ (คั่นด้วยจุลภาคถ้ามีหลายคีย์):
    ```
    GOOGLE_API_KEYS="your_api_key_1,your_api_key_2"
    ```

### 2. สร้างฐานข้อมูล RAG

-   (ทำแค่ครั้งแรก) รันสคริปต์เพื่อสร้าง Vector Index จากหนังสือ:
    ```bash
    python manage_data.py
    ```

### 3. รันเซิร์ฟเวอร์

-   เริ่มต้นเซิร์ฟเวอร์ FastAPI:
    ```bash
    uvicorn main:app --reload
    ```

### 4. เริ่มใช้งาน

-   เปิดเว็บเบราว์เซอร์ของคุณแล้วไปที่:
    [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

โปรเจกต์นี้สร้างขึ้นเพื่อการเรียนรู้และขัดเกลาความเข้าใจในเทคโนโลยี Full-Stack AI
