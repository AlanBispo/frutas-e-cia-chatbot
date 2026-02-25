import React from 'react';
import appleMascot from '../assets/apple_mascot.png';

interface HomeProps {
  onStartChat: () => void;
  onShowOffers: () => void;
}

export const Home: React.FC<HomeProps> = ({ onStartChat, onShowOffers }) => {
  return (
    <div className="min-h-screen bg-[#e1f5db] flex items-center justify-center p-4 relative overflow-hidden">
      <div className="absolute top-10 left-10 opacity-20 text-4xl">🍃</div>
      <div className="absolute bottom-20 right-20 opacity-20 text-4xl rotate-45">🍃</div>

      {/* Card Principal */}
      <div className="max-w-[850px] w-full bg-white rounded-[40px] shadow-2xl overflow-hidden flex flex-col relative">
        
        {/* Banner Superior */}
        <div className="bg-green-700 p-10 flex justify-between items-center relative">
          <div className="text-white">
            <h1 className="text-5xl font-extrabold tracking-tight">Frutas & Cia</h1>
            <p className="text-green-100 text-xl mt-2">Seu hortifruti inteligente</p>
          </div>

          <div className="absolute right-12 top-1/2 -translate-y-1/2 w-44 h-44 bg-white rounded-full border-8 border-white shadow-xl overflow-hidden flex items-center justify-center">
            <img 
              src={appleMascot} 
              alt="Mascote Frutas e Cia" 
              className="w-full h-full object-cover"
            />
          </div>
        </div>

        {/* Conteúdo de Boas-vindas */}
        <div className="p-14 bg-white">
          <div className="flex items-start gap-5 mb-10 bg-gray-50 p-6 rounded-3xl border border-gray-100 max-w-2xl">
            <div className="w-12 h-12 rounded-full bg-green-600 flex items-center justify-center text-white shrink-0 shadow-inner">
               <img src={appleMascot} alt="bot-icon" className="w-full h-full object-cover" />
            </div>
            <div>
              <p className="text-gray-800 text-lg font-semibold">Olá! Sou o seu assistente virtual.</p>
              <p className="text-gray-600">Posso te informar sobre preços, disponibilidade e nossas promoções exclusivas.</p>
            </div>
          </div>

          {/* Botões de Ação */}
          <div className="flex gap-5">
            <button 
              onClick={onStartChat}
              className="bg-green-700 text-white px-10 py-4 rounded-2xl font-bold text-lg hover:bg-green-800 transition-all shadow-lg hover:-translate-y-1 cursor-pointer"
            >
              Iniciar conversa
            </button>
            
            {/* BOTÃO OFERTAS DO DIA */}
            <button 
              onClick={onShowOffers}
              className="bg-white text-green-700 border-2 border-green-700 px-10 py-4 rounded-2xl font-bold text-lg hover:bg-green-50 transition-all shadow-sm cursor-pointer"
            >
              Ofertas do Dia
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};