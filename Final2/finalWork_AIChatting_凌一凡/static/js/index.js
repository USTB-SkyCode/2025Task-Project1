
// 初始化时间显示
document.getElementById('initial-time').textContent = getCurrentTime();

// 获取DOM元素
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');

// 发送消息函数
function sendMessage() {
    const message = messageInput.value.trim();
    if (message === '') return;

    // 添加用户消息到聊天界面
    addMessage(message, 'user');

    // 清空输入框
    messageInput.value = '';

    // 显示AI正在输入
    showTypingIndicator();

    // 发送消息到后端
    sendToBackend(message);
}

// 添加消息到聊天界面
function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatarDiv = document.createElement('div');
    avatarDiv.className = `avatar ${sender}-avatar`;
    avatarDiv.textContent = sender === 'user' ? '你' : 'AI';

    const messageContentDiv = document.createElement('div');
    messageContentDiv.className = 'message-content';

    const messageBubbleDiv = document.createElement('div');
    messageBubbleDiv.className = 'message-bubble';
    messageBubbleDiv.textContent = content;

    const messageTimeDiv = document.createElement('div');
    messageTimeDiv.className = 'message-time';
    messageTimeDiv.textContent = getCurrentTime();

    messageContentDiv.appendChild(messageBubbleDiv);
    messageContentDiv.appendChild(messageTimeDiv);

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(messageContentDiv);

    chatMessages.appendChild(messageDiv);

    // 滚动到底部
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 显示AI正在输入
function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 隐藏AI正在输入
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// 获取当前时间
function getCurrentTime() {
    const now = new Date();
    return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
}

// 发送消息到后端
async function sendToBackend(message) {
    try {
        // 这里需要替换为你的实际后端API地址
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error('网络响应异常');
        }

        const data = await response.json();

        // 隐藏正在输入提示
        hideTypingIndicator();

        // 添加AI回复到聊天界面
        addMessage(data.reply, 'ai');

    } catch (error) {
        console.error('与后端通信失败:', error);
        hideTypingIndicator();
        addMessage('抱歉，我现在无法回复你的消息。请稍后再试。', 'ai');
    }
}

// 事件监听
sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// 模拟后端响应（开发阶段使用）
// 实际部署时请注释掉这部分代码
async function sendToBackend(message) {
    // 模拟网络延迟
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

    // 隐藏正在输入提示
    hideTypingIndicator();

    // 简单的回复逻辑（实际应用中应由后端处理）
    let reply;
    if (message.toLowerCase().includes('你好')) {
        reply = '你好！很高兴与你交流。';
    } else if (message.toLowerCase().includes('名字')) {
        reply = '我是AI助手，你可以叫我任何你喜欢的名字！';
    } else if (message.toLowerCase().includes('帮助')) {
        reply = '我可以回答你的问题、提供信息或与你聊天。请告诉我你需要什么帮助。';
    } else {
        reply = `我收到了你的消息："${message}"。这是一个模拟回复，实际应用中我会提供更有意义的回答。`;
    }

    // 添加AI回复到聊天界面
    addMessage(reply, 'ai');
}