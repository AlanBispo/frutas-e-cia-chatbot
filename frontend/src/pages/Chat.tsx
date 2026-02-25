import React, { useState } from 'react';
import { Send, Bot, User, Sprout, ArrowLeft } from 'lucide-react';
import { useChat } from '../hooks/useChat';

interface ChatProps {
  onBackToHome: () => void;
}

export const Chat: React.FC<ChatProps> = ({ onBackToHome }) => {
  const { messages, send, isLoading, scrollRef } = useChat();
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      send(input);
      setInput('');
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto bg-white shadow-2xl font-sans">
      <header className="p-4 border-b bg-green-700 text-white flex items-center gap-3">
        <button onClick={onBackToHome} className="hover:bg-green-800 p-2 rounded-full transition-colors">
            <ArrowLeft size={24} />
        </button>
        <Sprout size={24} className="text-green-200" />
        <h1 className="font-bold text-xl">Frutas e Cia - Atendimento</h1>
      </header>

      <main className="flex-1 overflow-y-auto p-4 space-y-4 bg-[#f8fdf8]">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex gap-2 max-w-[80%] ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.sender === 'user' ? 'bg-green-800' : 'bg-gray-200'}`}>
                {msg.sender === 'user' ? <User size={18} color="white" /> : <Bot size={18} className="text-green-800" />}
              </div>

              {/* Balões de Mensagem*/}
              <div className={`p-3 rounded-2xl shadow-sm ${
                  msg.sender === 'user' 
                    ? 'bg-green-600 text-white rounded-tr-none' // Usuário: Verde escuro
                    : 'bg-white text-gray-800 border border-gray-200 rounded-tl-none' // Bot: Branco
                }`}>
                {msg.text}
              </div>
            </div>
          </div>
        ))}
        
        {/* Loading Skeleton */}
        {isLoading && (
          <div className="flex justify-start animate-pulse items-center gap-2">
             <div className="w-8 h-8 rounded-full bg-gray-200 shrink-0"></div>
             <div className="bg-gray-100 h-10 w-24 rounded-2xl rounded-tl-none border border-gray-200"></div>
          </div>
        )}
        <div ref={scrollRef} />
      </main>

      {/* Input Area */}
      <footer className="p-4 border-t bg-white">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Pergunte sobre frutas, preços ou estoque..."
            disabled={isLoading}
            className="flex-1 p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-green-600 text-white p-3 rounded-xl hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={22} />
          </button>
        </form>
      </footer>
    </div>
  );
};