import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setMessages([...messages, { sender: 'user', text: input }]);
    try {
      const res = await axios.post('http://localhost:8000/chat', { message: input });
      setMessages(msgs => [...msgs, { sender: 'bot', text: res.data.response }]);
    } catch (e) {
      setMessages(msgs => [...msgs, { sender: 'bot', text: 'Error contacting backend.' }]);
    }
    setInput("");
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h2>INGRES Groundwater Chatbot</h2>
      <div style={{ border: '1px solid #ccc', padding: 16, minHeight: 300, background: '#fafafa' }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left', margin: '8px 0' }}>
            <b>{msg.sender === 'user' ? 'You' : 'Bot'}:</b> {msg.text}
          </div>
        ))}
        {loading && <div>Bot is typing...</div>}
      </div>
      <div style={{ marginTop: 16, display: 'flex' }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          style={{ flex: 1, padding: 8 }}
          placeholder="Ask about groundwater data..."
        />
        <button onClick={sendMessage} disabled={loading} style={{ marginLeft: 8 }}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
