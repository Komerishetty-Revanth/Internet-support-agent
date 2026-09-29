// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const escalateBtn = document.getElementById('escalateBtn');
const resetBtn = document.getElementById('resetBtn');
const clearBtn = document.getElementById('clearBtn');
const customerId = document.getElementById('customerId');
const customerEmail = document.getElementById('customerEmail');
const customerName = document.getElementById('customerName');

// Status elements
const ticketIdEl = document.getElementById('ticketId');
const ticketStatusEl = document.getElementById('ticketStatus');
const issueCategoryEl = document.getElementById('issueCategory');
const stageEl = document.getElementById('stage');
const stepEl = document.getElementById('step');
const progressFillEl = document.getElementById('progressFill');
const msgCountEl = document.getElementById('msgCount');

// State
let isLoading = false;
let currentIssueCategory = null;
let currentStep = 0;
let maxSteps = 6;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    generateTicketId();
    setupEventListeners();
});

function setupEventListeners() {
    sendBtn.addEventListener('click', sendMessage);
    escalateBtn.addEventListener('click', escalateTicket);
    resetBtn.addEventListener('click', resetConversation);
    clearBtn.addEventListener('click', newTicket);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.ctrlKey && !isLoading) {
            sendMessage();
        }
    });
}

/**
 * Generate unique ticket ID
 */
function generateTicketId() {
    const timestamp = Date.now().toString().slice(-5);
    const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
    ticketIdEl.textContent = `TKT-${timestamp}${random}`;
}

/**
 * Send message to API
 */
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    isLoading = true;
    sendBtn.disabled = true;
    messageInput.disabled = true;
    
    addMessageToChat('user', message);
    messageInput.value = '';
    
    try {
        const response = await fetch('http://localhost:8000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                customer_id: customerId.value || 'CUST001',
                message: message,
                email: customerEmail.value || '',
                name: customerName.value || ''
            })
        });
        
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        
        const data = await response.json();
        addMessageToChat('agent', data.message);
        updateTicketStatus(data);
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('agent', '❌ Error processing message. Please try again.');
    } finally {
        isLoading = false;
        sendBtn.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

/**
 * Add message to chat
 */
function addMessageToChat(role, content) {
    const messageGroup = document.createElement('div');
    messageGroup.className = 'message-group';
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const avatar = role === 'agent' ? '🤖' : '👤';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-bubble">${escapeHtml(content)}</div>
            <span class="message-time">${time}</span>
        </div>
    `;
    
    messageGroup.appendChild(messageDiv);
    chatMessages.appendChild(messageGroup);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    updateMessageCount();
}

/**
 * Update ticket status
 */
function updateTicketStatus(data) {
    // Update category
    if (data.issue_category) {
        currentIssueCategory = data.issue_category;
        issueCategoryEl.textContent = data.issue_category.replace(/_/g, ' ');
    }
    
    // Update stage
    stageEl.textContent = data.stage || 'START';
    
    // Update step
    currentStep = data.step || 0;
    stepEl.textContent = `Step ${currentStep + 1}`;
    
    // Update progress
    const progress = Math.min(((currentStep + 1) / maxSteps) * 100, 100);
    progressFillEl.style.width = progress + '%';
    
    // Update status
    if (data.resolved) {
        ticketStatusEl.textContent = 'Resolved';
        ticketStatusEl.className = 'status-badge resolved';
        disableInput('Issue resolved!');
    } else if (data.escalated) {
        ticketStatusEl.textContent = 'Escalated';
        ticketStatusEl.className = 'status-badge escalated';
        disableInput('Escalated to support');
    } else {
        ticketStatusEl.textContent = 'Open';
        ticketStatusEl.className = 'status-badge open';
    }
}

/**
 * Escalate ticket
 */
function escalateTicket() {
    if (confirm('Escalate to human support?')) {
        addMessageToChat('agent', '📞 Your ticket has been escalated. A human support specialist will contact you shortly.');
        disableInput('Escalated');
    }
}

/**
 * Reset conversation
 */
function resetConversation() {
    if (confirm('Reset conversation?')) {
        const lastMessage = chatMessages.querySelector('.message-group');
        while (chatMessages.children.length > 1) {
            chatMessages.removeChild(chatMessages.lastChild);
        }
        messageInput.value = '';
        messageInput.disabled = false;
        sendBtn.disabled = false;
        updateMessageCount();
    }
}

/**
 * New ticket
 */
function newTicket() {
    if (confirm('Start a new ticket?')) {
        generateTicketId();
        chatMessages.innerHTML = `
            <div class="message-group">
                <div class="message agent">
                    <div class="message-avatar">🤖</div>
                    <div class="message-content">
                        <div class="message-bubble">
                            <p>Hello! I'm your AI support agent. I'm here to help you troubleshoot any internet connectivity issues.</p>
                            <p style="margin-top: 8px;">Please describe what's happening with your internet connection, and I'll guide you through the diagnostic process.</p>
                        </div>
                        <span class="message-time">Now</span>
                    </div>
                </div>
            </div>
        `;
        issueCategoryEl.textContent = 'Unclassified';
        stageEl.textContent = 'START';
        stepEl.textContent = 'Step 1';
        ticketStatusEl.textContent = 'Open';
        ticketStatusEl.className = 'status-badge open';
        progressFillEl.style.width = '10%';
        messageInput.disabled = false;
        sendBtn.disabled = false;
        messageInput.value = '';
        messageInput.focus();
        currentStep = 0;
        updateMessageCount();
    }
}

/**
 * Disable input
 */
function disableInput(reason) {
    messageInput.disabled = true;
    sendBtn.disabled = true;
    escalateBtn.disabled = true;
    sendBtn.textContent = reason;
}

/**
 * Update message count
 */
function updateMessageCount() {
    msgCountEl.textContent = chatMessages.querySelectorAll('.message').length;
}

/**
 * Escape HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
