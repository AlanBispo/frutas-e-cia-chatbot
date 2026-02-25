import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import { Home } from './pages/Home';
import { Chat } from './pages/Chat';
import AdminPanel from './pages/AdminPanel';
import Navbar from './components/Navbar';
import { useChat } from './hooks/useChat';
import { getDailyOffers } from './api/chatService';


function AppContent() {
  const chatLogic = useChat();
  const navigate = useNavigate();

  const handleStartNormalChat = () => {
    chatLogic.resetChat();
    navigate('/chat');
  };

  const handleShowOffers = async () => {
    try {
      const data = await getDailyOffers();
      await chatLogic.startConversationWithContext(data.texto);
      navigate('/chat');
    } catch (error) {
      console.error("Erro ao carregar ofertas:", error);
      chatLogic.resetChat();
      navigate('/chat');
    }
  };

  return (
    <div className="antialiased font-sans bg-gray-50 min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow">
        <Routes>
          <Route path="/" element={
            <Home 
              onStartChat={handleStartNormalChat}
              onShowOffers={handleShowOffers} 
            />
          } />
          
          <Route path="/chat" element={
            <Chat 
              chat={chatLogic} 
              onBackToHome={() => navigate('/')} 
            />
          } />

          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;