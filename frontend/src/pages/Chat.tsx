import React, { useState } from 'react';
import { Send, Bot, User, Sprout, ArrowLeft, Trash2 } from 'lucide-react';
import type { Message } from '../types/chat';

interface ChatProps {
  onBackToHome: () => void;
  chat: {
    messages: Message[];
    send: (text: string) => Promise<void>;
    isLoading: boolean;
    scrollRef: React.RefObject<HTMLDivElement | null>;
    resetChat: () => Promise<void>;
  };
}

export const Chat: React.FC<ChatProps> = ({ onBackToHome, chat }) => {
  const { messages, send, isLoading, scrollRef, resetChat } = chat;
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      send(input);
      setInput('');
    }
  };

  const handleClear = async () => {
    if (window.confirm("Deseja realmente apagar todo o histórico desta conversa?")) {
      await resetChat();
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto bg-white shadow-2xl border-x">
      <header className="p-4 bg-green-700 text-white flex items-center justify-between shadow-md z-10">
        <div className="flex items-center gap-3">
          <button 
            onClick={onBackToHome} 
            className="p-2 hover:bg-green-800 rounded-full transition-colors"
            title="Voltar para a Home"
          >
            <ArrowLeft size={24} />
          </button>
          <Sprout size={24} className="text-green-200" />
          <h1 className="font-bold text-xl tracking-tight">Frutas & Cia</h1>
        </div>

        <button 
          onClick={handleClear}
          className="flex items-center gap-2 bg-green-800/50 hover:bg-red-600 px-3 py-2 rounded-lg transition-all text-sm font-medium"
          title="Limpar conversa"
        >
          <Trash2 size={18} />
          <span className="hidden sm:inline">Limpar</span>
        </button>
      </header>

      {/* Área das Mensagens */}
      <main className="flex-1 overflow-y-auto p-4 space-y-4 bg-[#f0f7ed]">
        {messages.map((msg, idx) => (
          <div 
            key={idx} 
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-2 duration-300`}
          >
            <div className={`flex gap-3 max-w-[85%] ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              
              {/* Avatar */}
              <div className={`w-9 h-9 rounded-full flex items-center justify-center shrink-0 shadow-sm ${
                msg.sender === 'user' ? 'bg-green-800' : 'bg-white border border-green-100'
              }`}>
                {msg.sender === 'user' 
                  ? <User size={20} color="white" /> 
                  : <Bot size={20} className="text-green-700" />
                }
              </div>

              {/* Balão de Texto */}
              <div className={`p-4 rounded-2xl shadow-sm leading-relaxed ${
                msg.sender === 'user' 
                  ? 'bg-green-600 text-white rounded-tr-none' 
                  : 'bg-white text-gray-800 border border-gray-100 rounded-tl-none whitespace-pre-wrap'
              }`}>
                {msg.text}
              </div>
            </div>
          </div>
        ))}

        {/* Indicador de carregamento (Bot digitando) */}
        {isLoading && (
          <div className="flex justify-start items-center gap-3 animate-pulse">
            <div className="w-9 h-9 rounded-full bg-gray-200"></div>
            <div className="bg-white border border-gray-100 h-12 w-20 rounded-2xl rounded-tl-none flex items-center justify-center gap-1">
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></span>
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
            </div>
          </div>
        )}
        
        {/* Referência para o scroll automático */}
        <div ref={scrollRef as React.RefObject<HTMLDivElement>} />
      </main>

      {/* Input de Mensagem */}
      <footer className="p-4 border-t bg-white shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Pergunte sobre preços ou estoque..."
            disabled={isLoading}
            className="flex-1 p-3.5 bg-gray-50 border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:bg-white transition-all disabled:opacity-50"
          />
          <button 
            type="submit" 
            disabled={isLoading || !input.trim()}
            className="bg-green-600 text-white p-3.5 rounded-2xl hover:bg-green-700 transition-all shadow-lg hover:shadow-green-200 active:scale-95 disabled:opacity-50 disabled:active:scale-100"
          >
            <Send size={24} />
          </button>
        </form>
        <p className="text-[10px] text-center text-gray-400 mt-2">
          Frutas & Cia Inteligência Artificial - Respostas baseadas no estoque atual.
        </p>
      </footer>
    </div>
  );
};