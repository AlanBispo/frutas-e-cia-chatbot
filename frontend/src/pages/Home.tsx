import React from 'react';
import appleMascot from '../assets/apple_mascot.png'; 

interface HomeProps {
  onStartChat: () => void;
}

export const Home: React.FC<HomeProps> = ({ onStartChat }) => {
  return (
    <div className="min-h-screen bg-[#e1f5db] flex items-center justify-center p-4 relative overflow-hidden font-sans">
      <div className="absolute text-green-200 text-4xl top-10 left-10 opacity-50">🍃</div>
      <div className="absolute text-green-200 text-3xl bottom-20 right-20 opacity-50">🍓</div>
      <div className="absolute text-yellow-200 text-3xl top-40 right-10 opacity-50">🍊</div>
      
      {/* Card Principal */}
      <div className="max-w-[800px] w-full bg-white rounded-[30px] shadow-2xl overflow-hidden flex flex-col relative z-10">
        
        <div className="bg-gradient-to-r from-green-700 to-green-600 h-48 p-8 flex items-center relative overflow-hidden">
           <div className="text-white z-10">
             <h1 className="text-4xl font-extrabold mb-2">Frutas & Cia</h1>
             <p className="text-green-100 text-lg">Fruit shop chatbot</p>
           </div>
           
           <div className="absolute right-8 top-1/2 -translate-y-1/2 w-40 h-40 bg-white rounded-full border-4 border-white shadow-md flex items-center justify-center overflow-hidden">
             <img src={appleMascot} alt="Mascote Maçã Robô" className="w-full h-full object-cover" />
           </div>
        </div>

        {/* Corpo do Card */}
        <div className="p-12 bg-[#f8fdf8]">
          <div className="flex items-start gap-4 mb-8 max-w-xl bg-white p-4 rounded-2xl shadow-sm border border-gray-100">
            <div className="w-12 h-12 rounded-full overflow-hidden bg-green-100 border-2 border-green-500 shrink-0">
               <img src={appleMascot} alt="Bot" className="w-full h-full object-cover" />
            </div>
            <div>
              <p className="text-gray-800 font-medium">Olá! Sou seu assistente da Frutas & Cia.</p>
              <p className="text-gray-600">Como posso ajudar hoje?</p>
            </div>
          </div>

          {/* Botões de Ação */}
          <div className="flex flex-wrap gap-4 font-bold">
            <button 
              onClick={onStartChat}
              className="bg-green-700 text-white px-8 py-3 rounded-xl hover:bg-green-800 transition-colors shadow-md cursor-pointer"
            >
              Iniciar conversa
            </button>
            <button className="bg-white text-green-700 border-2 border-green-700 px-8 py-3 rounded-xl hover:bg-green-50 transition-colors cursor-pointer">
              Ofertas do Dia
            </button>
          </div>
        </div>
      </div>
      
      {/* Ícone de chat flutuante no canto inferior direito */}
      <div className="fixed bottom-6 right-6 w-14 h-14 bg-green-600 rounded-full flex items-center justify-center shadow-lg text-white cursor-pointer hover:bg-green-700 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
      </div>
    </div>
  );
};