// script.js
document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    addMessageToChat('user', 'การได้มาซึ่งอำนาจต้องทำอย่างไร?');
    addMessageToChat('bot', 'การจะได้มาซึ่งอำนาจนั้นต้องใช้กลยุทธ์ กฎข้อที่ 1 แนะนำว่าอย่าโดดเด่นเกินผู้เป็นนาย เพื่อให้ผู้ที่อยู่เหนือกว่ารู้สึกเหนือกว่าอยู่เสมอ กฎข้อที่ 3 แนะนำให้ซ่อนเจตนาของคุณไว้ เพื่อป้องกันไม่ให้ผู้อื่นล่วงรู้ถึงแรงจูงใจที่แท้จริงของคุณ ตลอดทั้ง 48 กฎแห่งอำนาจนั้น เน้นย้ำถึงการคำนวณ การชักจูง และการใช้ประโยชน์จากจุดอ่อนของผู้อื่น');

    messageForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = messageInput.value.trim();
        if (query) {
            sendMessage(query);
            messageInput.value = '';
        }
    });

    async function sendMessage(query) {
        addMessageToChat('user', query);
        const botMessageElement = addMessageToChat('bot', 'Thinking...');

        try {
            const response = await fetch(`/ask?query=${encodeURIComponent(query)}`);

            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            botMessageElement.innerHTML = ''; 

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const dataStr = line.substring(6);
                        try {
                            const data = JSON.parse(dataStr);
                            if (data.text) {
                                botMessageElement.innerHTML += data.text.replace(/\n/g, '<br>');
                            }
                            if (data.error) {
                                botMessageElement.innerText = `Error: ${data.error}`;
                                break;
                            }
                        } catch (e) {
                            console.error("Error parsing stream data:", e);
                        }
                    }
                }
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        } catch (error) {
            botMessageElement.innerText = `Error: Could not connect to the advisor. ${error.message}`;
        }
    }

    function addMessageToChat(sender, text) {
        const messageWrapper = document.createElement('div');
        messageWrapper.className = `chat-bubble ${sender}-message`;
        messageWrapper.innerText = text;
        chatContainer.appendChild(messageWrapper);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return messageWrapper;
    }
});