import { useState } from 'react';
import { Home } from './pages/Home';
import { Chat } from './pages/Chat';
import { useChat } from './hooks/useChat';
import { getDailyOffers } from './api/chatService';

function App() {
  const [view, setView] = useState<'home' | 'chat'>('home');
  const chatLogic = useChat();

  const handleStartNormalChat = () => {
    chatLogic.resetChat();
    setView('chat');
  };

  const handleShowOffers = async () => {
    try {
      const data = await getDailyOffers();
      await chatLogic.startConversationWithContext(data.texto);
      setView('chat');
    } catch (error) {
      console.error("Erro ao carregar ofertas:", error);
      chatLogic.resetChat();
      setView('chat');
    }
  };

  return (
    <div className="antialiased font-sans bg-gray-50 min-h-screen">
      {view === 'home' ? (
        <Home 
          onStartChat={handleStartNormalChat}
          onShowOffers={handleShowOffers} 
        />
      ) : (
        <Chat 
          chat={chatLogic} 
          onBackToHome={() => setView('home')} 
        />
      )}
    </div>
  );
}

export default App;