import { useState } from 'react';
import { Home } from './pages/Home';
import { Chat } from './pages/Chat';

function App() {
  const [currentScreen, setCurrentScreen] = useState<'home' | 'chat'>('home');

  return (
    <div className="antialiased font-sans">
      {currentScreen === 'home' ? (
        <Home onStartChat={() => setCurrentScreen('chat')} />
      ) : (
        <Chat onBackToHome={() => setCurrentScreen('home')} />
      )}
    </div>
  );
}

export default App;