import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Bot, User, Sprout } from 'lucide-react';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Olá! Sou o assistente da Frutas e Cia. Como posso te ajudar com nosso estoque hoje?", sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll para a última mensagem
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { text: userMsg, sender: 'user' }]);
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/chat/', { message: userMsg });
      setMessages(prev => [...prev, { text: response.data.reply, sender: 'bot' }]);
    } catch (error) {
      setMessages(prev => [...prev, { text: "Erro ao conectar com o servidor. Tente novamente mais tarde", sender: 'bot' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto border-x bg-white shadow-xl">
      {/* Header */}
      <header className="p-4 border-b bg-green-600 text-white flex items-center gap-2">
        <Sprout size={24} />
        <h1 className="font-bold text-xl">Frutas e Cia - Atendimento</h1>
      </header>

        {/* Chat Messages */}
        <main className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`flex gap-2 max-w-[80%] ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.sender === 'user' ? 'bg-blue-500' : 'bg-green-500'}`}>
                  {msg.sender === 'user' ? <User size={18} color="white" /> : <Bot size={18} color="white" />}
                </div>
                <div className={`p-3 rounded-2xl shadow-sm ${msg.sender === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-white text-slate-800 rounded-tl-none border'}`}>
                  {msg.text}
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start animate-pulse">
              <div className="bg-slate-200 h-10 w-24 rounded-2xl"></div>
            </div>
          )}
          <div ref={scrollRef} />
        </main>

        {/* Input Area */}
        <footer className="p-4 border-t bg-white">
          <form onSubmit={sendMessage} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Pergunte sobre frutas, preços ou estoque..."
              className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="bg-green-600 text-white p-2 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
            >
              <Send size={20} />
            </button>
          </form>
      </footer>
    </div>
  );
}

export default App;