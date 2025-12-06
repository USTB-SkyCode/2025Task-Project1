// 获取DOM元素
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');
const chooseDialog = document.querySelector('.side .dialogs');
const newDialog = document.querySelector('.side .dialogs label');

const allIDs = [];


// 清空当前聊天界面
function clearMessageList(){
    chatMessages.innerHTML = ""
}

// 添加AI初始打招呼信息到当前聊天界面
function addInitialMsg(){
    chatMessages.innerHTML += `
    <div class="message ai-message">
        <div class="avatar ai-avatar">AI</div>
        <div class="message-content">
            <div class="message-bubble">
                你好！我是AI助手，很高兴为你服务。请问有什么可以帮助你的吗？
            </div>
            <div class="message-time" id="initial-time"></div>
        </div>
    </div>
    `
}

// 添加消息到聊天界面
function addMessage(content, sender) {
    var messageDiv = document.createElement('div')
    sender = sender === 'user' ? sender : 'ai'  // 临时代码，适配类名对应css
    messageDiv.className = `message ${sender}-message`;
    var avatarStr = `<div class="avatar ${sender}-avatar">${sender === 'user' ? '你' : 'AI'}</div>`
    var htmlStr = `
        <div class="message-content">
            <div class="message-bubble">
                ${content}
            </div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `
    htmlStr = sender === 'user' ? htmlStr + avatarStr : avatarStr + htmlStr;
    messageDiv.innerHTML = htmlStr;
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

// 交互-向后台发送数据并获取模型结果
function sendToBackend(id, msg) {
    $.ajax({
        url: "/getAnswer",
        data: { id:id, msg:msg },
        success: (result) => {
            if (result.success === 0) {
                // alert('success, ready to process result')
                // alert(result['reply'])
                addMessage(result['reply'], 'ai')
                hideTypingIndicator();
            } else {
                void 0
                // alert('failed, check!')
            }
        }
    })
}

// 交互-向后台发送数据并获取聊天历史
function loadDialogHistory(id){
    $.ajax({
        url: "/loadHistory",
        data:{id},
        success: (result) => {
            if (result.success === 0) {
                // Array.from(JSON.parse(result.history)).forEach(msg => addMessage(msg.content, msg.sender))
                Array.from(result.history).forEach((msg) => {
                    if (msg.role === "system") { return; }
                    addMessage(msg.content, msg.role)}
                )
            }else{
                alert('loading failed...')
            }
        }
    })
}

// 初始化当前对话框显示
function initMessageList(){
    clearMessageList();
    addInitialMsg();
}

// 创建新聊天对应选项
function createDialogSelect(id, selected=false){
    var newDialogDiv = document.createElement('div');
    newDialogDiv.classList.add('dialog')
    if (selected) {
        changeDialog(null,newDialogDiv)
        newDialogDiv.classList.add('selected')
    }
    newDialogDiv.dataset.id = id;
    newDialogDiv.innerHTML = `chat#${id}`
    chooseDialog.insertBefore(newDialogDiv, chooseDialog.children[1])
    return newDialogDiv

}

// 创建新聊天
function createDialog(selected){
    var selectedDialog = document.querySelector('.side .dialogs .selected');
    if (selectedDialog){selectedDialog.classList.remove('selected')};
    // 创建选择框
    var id = Math.floor(Math.random() * 100000) + 100000;
    console.log('id of new dialog:',String(id));
    var currentDialog = createDialogSelect(id,selected);
    // 初始化主界面
    initMessageList();
    // 准备新上下文
    $.ajax({
        url: "/createNewChat",
        data: { id },
        success: (result) => {
            if (result.success === 0) {
                Array.from(result.history).forEach((msg) => {
                    if (msg.role === "system") { return; }
                    addMessage(msg.content, msg.role)
                    allIDs.push(id);
                })
                return currentDialog;
            } else {
                void 0
                // alert('failed, check!')
            }
        }
    })
    return currentDialog;
}

// 更换聊天记录
function changeDialog(currentdialog, targetdialog){
    console.log('dialog window changed');
    clearMessageList();
    addInitialMsg();
    loadDialogHistory(targetdialog.dataset.id);
    if (currentdialog){
        currentdialog.classList.remove('selected')
    }
    targetdialog.classList.add('selected')
}

// 交互-向后台获取所有聊天
function loadAllID(){
    $.ajax({
        url: "/loadAllID",
        success: (result) => {
            if (result.success === 0) {
                Array.from(result.ids).forEach((id, index, arr) => {
                    var currentDialog = createDialogSelect(id);
                    allIDs.push(id);
                    if (index === arr.length-1){
                        changeDialog(null, currentDialog);
                    }
                }
                )
            } else {
                void 0
                // alert('failed, check!')
            }
        }
    })
}


// 获取当前时间
function getCurrentTime() {
    const now = new Date();
    return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
}


// 发送信息
function sendMessage() {
    var currentDialog = document.querySelector('.side .dialog.selected')
    if (!currentDialog){
        currentDialog = createDialog();
        changeDialog(null,currentDialog);
    }
    const message = messageInput.value.trim();
    if (message === '') {return};
    // 添加用户消息到聊天界面
    addMessage(message, 'user');

    // 清空输入框
    messageInput.value = '';

    // 显示AI正在输入
    showTypingIndicator();

    // 发送消息到后端
    sendToBackend(currentDialog.dataset.id, message);
}

// 事件监听
sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

chooseDialog.addEventListener('click',(e)=>{
    if (!e.target.classList.contains('dialog') || (e.target.tagName !== 'DIV')){ 
        return; 
    }
    
    var currentDialog = document.querySelector('.side .selected');
    var targetDialog = e.target;
    changeDialog(currentDialog, targetDialog)
})

newDialog.addEventListener('click', (e) => {
    console.log('new dialog created');
    createDialog(true);
})



// 初始化操作
initMessageList();
loadAllID();

