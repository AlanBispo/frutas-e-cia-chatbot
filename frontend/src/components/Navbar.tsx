import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar: React.FC = () => {
  const location = useLocation();

  const activeClass = (path: string) => 
    location.pathname === path ? "bg-green-700" : "hover:bg-green-600";

  return (
    <nav className="bg-green-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🍎</span>
            <span className="font-bold text-xl tracking-tight">Frutas & Cia</span>
          </div>
          
          <div className="flex space-x-4">
            <Link 
              to="/" 
              className={`px-3 py-2 rounded-md text-sm font-medium transition ${activeClass('/')}`}
            >
              Chat do Cliente
            </Link>
            
            <Link 
              to="/admin" 
              className={`px-3 py-2 rounded-md text-sm font-medium transition ${activeClass('/admin')}`}
            >
              Painel Admin
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;