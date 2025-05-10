// src/components/SidebarLayout.js
import { useState } from "react";
import { useTranslation } from "react-i18next";
import LanguageSelector from "./LanguageSelector";
import { Link } from "react-router-dom";

export default function SidebarLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { t } = useTranslation();

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className={`bg-white shadow-md transition-all duration-300 ${sidebarOpen ? "w-64" : "w-16"}`}>
        <div className="flex items-center justify-between px-4 py-4 border-b">
          <span className={`font-bold text-gray-700 ${!sidebarOpen && "hidden"}`}>CRM STO</span>
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="focus:outline-none">
            <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                d={sidebarOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
            </svg>
          </button>
        </div>
        <nav className="mt-4 space-y-2">
          <Link to="/dashboard" className="block px-4 py-2 text-gray-700 hover:bg-gray-200 rounded">
            {sidebarOpen ? t("dashboard.home") : "🏠"}
          </Link>
          <Link to="/orders" className="block px-4 py-2 text-gray-700 hover:bg-gray-200 rounded">
            {sidebarOpen ? t("dashboard.orders") : "📦"}
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-6">
        <div className="flex justify-end mb-4">
          <LanguageSelector />
        </div>
        {children}
      </main>
    </div>
  );
}
