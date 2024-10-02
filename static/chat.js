const { useState, useEffect, useRef } = React;

function AIChat() {
    const [isMinimized, setIsMinimized] = useState(false);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [history, setHistory] = useState([]);
    const displayAreaRef = useRef(null);

    // Load chat history
    useEffect(() => {
        const storedHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
        setHistory(storedHistory);

        const initialMessages = [];
        storedHistory.forEach(entry => {
            initialMessages.push({ sender: 'user', text: entry.question });
            initialMessages.push({ sender: 'system', text: formatOutput(entry.answer) });
        });
        setMessages(initialMessages);
    }, []);

    // Auto-scroll to the bottom
    useEffect(() => {
        if (displayAreaRef.current) {
            displayAreaRef.current.scrollTop = displayAreaRef.current.scrollHeight;
        }
    }, [messages, isMinimized]);

    // Toggle minimize state
    const toggleMinimize = () => {
        setIsMinimized(!isMinimized);
    };

    // Clear chat history
    const clearChat = () => {
        setMessages([]);
        setHistory([]);
        localStorage.removeItem('chatHistory');
    };

    // Handle key down in input box
    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };

    // Send message
    const sendMessage = async () => {
        const question = input.trim();

        if (question === '') return;
        setInput('');

        const newMessages = [...messages, { sender: 'user', text: question }];
        setMessages(newMessages);

        // Show loading message
        const loadingMessage = { sender: 'system', text: '正在處理中，請稍候...' };
        setMessages(prev => [...prev, loadingMessage]);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: question,
                    history: history,
                }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }

            const data = await response.json();
            setMessages(prev => prev.filter(msg => msg !== loadingMessage));

            let output;
            try {
                output = JSON.parse(data.output);
            } catch (parseError) {
                console.error('JSON parse error:', parseError);
                throw new Error('解析回傳資料時發生錯誤。');
            }
            const updatedHistory = data.history;

            setHistory(updatedHistory);
            localStorage.setItem('chatHistory', JSON.stringify(updatedHistory));

            setMessages(prev => [...prev, { sender: 'system', text: formatOutput(output) }]);
        } catch (error) {
            console.error('Fetch error:', error);
            setMessages(prev => prev.filter(msg => msg !== loadingMessage));
            setMessages(prev => [...prev, { sender: 'system', text: '發生錯誤，請稍後再試。' }]);
        }
    };

    // Display messages
    const renderMessages = () => {
        return messages.map((msg, index) => (
            <div
                key={index}
                className={`message-container ${
                    msg.sender === 'user' ? 'user-message' : 'system-message'
                }`}
            >
                <div className="message-bubble">{msg.text}</div>
            </div>
        ));
    };

    // Format output
    const formatOutput = (output) => {
        let content = '';
        if (output.product) {
            const { title, product_id, url, description } = output.product;
            content += `產品名稱: ${title || '無'}\n`;
            content += `產品網址: ${url || '無'}\n`;
            content += `產品描述: ${description || '無'}\n\n`;
        }
        if (output.description) {
            content += `推薦原因: ${output.description}\n\n`;
        }
        if (output.advice) {
            content += `使用建議: ${output.advice}\n`;
        }
        return content || '無法獲取產品資訊。';
    };

    return (
        <div id="floatDiv" className={isMinimized ? 'minimized' : ''}>
            <div id="header" onClick={toggleMinimize}>
                {!isMinimized && <span>Dr WU AI助理</span>}
                {!isMinimized && (
                    <button id="toggleButton">
                        －
                    </button>
                )}
            </div>
            {!isMinimized && (
                <>
                    <div id="displayArea" ref={displayAreaRef}>
                        {renderMessages()}
                    </div>
                    <div id="inputContainer">
                        <input
                            type="text"
                            id="inputBox"
                            placeholder="請輸入您的問題..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                        />
                        <button id="clearButton" onClick={clearChat}>
                            清除
                        </button>
                        <button id="sendButton" onClick={sendMessage}>
                            發送
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}

// Render the React component into floatDiv
ReactDOM.createRoot(document.getElementById('chatContainer')).render(<AIChat />);
