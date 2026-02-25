import { useState, useRef, useEffect } from 'react';
import { sendMessageToBot, clearChatHistory } from '../api/chatService';
import type { Message } from '../types/chat';

export function useChat() {
  const DEFAULT_MESSAGE: Message[] = [
    { text: "Olá! Sou o assistente da Frutas e Cia. Como posso te ajudar com nosso estoque hoje?", sender: 'bot' }
  ];

  const [messages, setMessages] = useState<Message[]>(DEFAULT_MESSAGE);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll para a última mensagem
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const send = async (inputMessage: string) => {
    if (!inputMessage.trim()) return;
    
    // Adiciona mensagem do usuário e inicia loading
    setMessages(prev => [...prev, { text: inputMessage, sender: 'user' }]);
    setIsLoading(true);

    try {
      // Chama a camada de serviço
      const reply = await sendMessageToBot(inputMessage);
      setMessages(prev => [...prev, { text: reply, sender: 'bot' }]);
    } catch (error) {
      setMessages(prev => [...prev, { text: "Erro ao conectar com o servidor. Tente novamente mais tarde", sender: 'bot' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const resetChat = async () => {
    try {
      await clearChatHistory();
      
      setMessages([
        { text: "Olá! Sou o assistente da Frutas e Cia. Como posso te ajudar?", sender: 'bot' }
      ]);
    } catch (error) {
      console.error("Erro ao resetar chat:", error);
    }
  };

  const startConversationWithContext = async (initialBotMessage: string) => {
    setMessages([
      { text: initialBotMessage, sender: 'bot' }
    ]);
  };

  return { messages, send, isLoading, scrollRef, startConversationWithContext, resetChat };
}