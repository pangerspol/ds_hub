import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, BarChart, FileText, Settings, HelpCircle } from 'lucide-react';

const navItems = [
  { name: 'Home', icon: <Home size={18} />, path: '/' },
  { name: 'Analytics', icon: <BarChart size={18} />, path: '/analytics' },
  { name: 'Records', icon: <FileText size={18} />, path: '/records' },
  { name: 'Settings', icon: <Settings size={18} />, path: '/settings' },
  { name: 'Help', icon: <HelpCircle size={18} />, path: '/help' },
];

function Sidebar() {
  return (
    <aside className="w-64 bg-gray-800 p-4 space-y-6 shadow-lg">
      <div className="text-2xl font-bold text-purple-400">MediDash</div>
      <nav className="flex flex-col space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-4 py-2 rounded-md hover:bg-gray-700 transition ${
                isActive ? 'bg-gray-700 text-white' : 'text-gray-400'
              }`
            }
          >
            <span>{item.icon}</span>
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;