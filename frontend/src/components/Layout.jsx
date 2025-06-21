import React from 'react';
import { Link } from 'react-router-dom';
import { FaCog } from 'react-icons/fa';

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Блок 1 - Навигация */}
      <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold">Tape</h2>
        </div>
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            <li>
              <Link to="/profile" className="block p-2 rounded hover:bg-gray-100">Моя страница</Link>
            </li>
            <li>
              <Link to="/friends" className="block p-2 rounded hover:bg-gray-100">Друзья</Link>
            </li>
            <li>
              <Link to="/groups" className="block p-2 rounded hover:bg-gray-100">Группы</Link>
            </li>
            <li>
              <Link to="/messages" className="block p-2 rounded hover:bg-gray-100">Сообщения</Link>
            </li>
            <li>
              <Link to="/music" className="block p-2 rounded hover:bg-gray-100">Музыка</Link>
            </li>
          </ul>
        </nav>
      </div>
      
      {/* Блок 2 - Основной контент */}
      <div className="flex-1 p-8">
        {children}
      </div>
      
      {/* Блок 3 - Настройки с вращающейся шестеренкой */}
      <div className="w-16 bg-white border-l border-gray-200 flex flex-col items-center p-4">
        <Link to="/settings" className="p-2 rounded-full hover:bg-gray-100">
          <FaCog className="text-gray-600 text-2xl animate-spin-slow" />
        </Link>
      </div>
    </div>
  );
}