import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {
  Moon,
  Sun,
  Code,
  Users,
  Brain,
  ChevronRight,
  Cpu,
  Twitter,
  Facebook,
  Linkedin,
  Instagram,
} from 'lucide-react';

const HomePage = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const navigate = useNavigate();

  // Card configurations with Tailwind classes for light & dark themes
  const interviewTypes = [
    {
      title: 'Instant Preparation',
      description: 'Prepare yourself based on the available resources.',
      icon: <Brain className="w-8 h-8" />,
      lightClasses:
        'bg-gradient-to-br from-blue-50 via-blue-100 to-blue-200 text-blue-600 hover:from-blue-100 hover:via-blue-200 hover:to-blue-300',
      darkClasses:
        'bg-gradient-to-br from-gray-800 via-gray-700 to-gray-600 text-white border-2 border-gray-600 hover:from-gray-700 hover:via-gray-600 hover:to-gray-500',
      iconBg:
        'bg-gradient-to-br from-blue-400 to-blue-600 text-black',
      link: '/instant-preparation',
    },
    {
      title: 'Testing Arena',
      description: 'Prepare yourself by practicing interviews, coding problems, and MCQs.',
      icon: <Code className="w-8 h-8" />,
      lightClasses:
        'bg-gradient-to-br from-emerald-50 via-emerald-100 to-emerald-200 text-emerald-600 hover:from-emerald-100 hover:via-emerald-200 hover:to-emerald-300',
      darkClasses:
        'bg-gradient-to-br from-gray-800 via-gray-700 to-gray-600 text-white border-2 border-gray-600 hover:from-gray-700 hover:via-gray-600 hover:to-gray-500',
      iconBg:
        'bg-gradient-to-br from-emerald-400 to-emerald-600 text-white',
      link: '/Test',
    },
    {
      title: 'Job Finder',
      description: 'Find jobs that align with your skills and experience.',
      icon: <Users className="w-8 h-8" />,
      lightClasses:
        'bg-gradient-to-br from-purple-50 via-purple-100 to-purple-200 text-purple-600 hover:from-purple-100 hover:via-purple-200 hover:to-purple-300',
      darkClasses:
        'bg-gradient-to-br from-gray-800 via-gray-700 to-gray-600 text-white border-2 border-gray-600 hover:from-gray-700 hover:via-gray-600 hover:to-gray-500',
      iconBg:
        'bg-gradient-to-br from-purple-400 to-purple-600 text-white',
      link: '/Job',
    },
  ];

  // Sync dark mode state with the document root
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  // Logout function with toast notification
  const handleLogout = () => {
    toast.info("Logging out...", { autoClose: 1500 });
    sessionStorage.setItem('loggedIn', 'false');
    setTimeout(() => {
      navigate('/');
    }, 1500);
  };

  return (
    <div className={`min-h-screen flex flex-col transition-colors duration-300 ${isDarkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      {/* Toast Container for notifications */}
      <ToastContainer />
      
      {/* Header spanning full width */}
      <header className="w-full px-4 py-8 flex justify-between items-center">
        {/* Branding on extreme left */}
        <div className="flex items-center space-x-2">
          <Cpu className="w-10 h-10 text-indigo-500 dark:text-indigo-400" />
          <span className="text-3xl font-bold text-gray-800 dark:text-gray-500">Switch</span>
        </div>
        {/* Right side: dark mode toggle and logout button */}
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setIsDarkMode(!isDarkMode)}
            className={`p-2 rounded-full transition-transform duration-200 transform hover:scale-110 ${
              isDarkMode ? 'bg-gray-800 text-yellow-400 hover:bg-gray-700' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
            title="Toggle Dark/Light Mode"
          >
            {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content Container */}
      <main className="flex-grow max-w-6xl mx-auto px-4">
        {/* Welcome Section */}
        <div className="text-center mb-12">
          <h1 className={`text-5xl font-bold mb-3 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
            Welcome Back
          </h1>
          <p className={`text-xl ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
            Choose your AI preparation path
          </p>
        </div>

        {/* Cards Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          {interviewTypes.map((card, idx) => (
            <Link key={idx} to={card.link}>
              <div
                className={`rounded-xl p-8 shadow-xl transform transition duration-300 hover:scale-105 hover:shadow-2xl backdrop-blur-sm ${isDarkMode ? card.darkClasses : card.lightClasses}`}
              >
                <div
                  className={`rounded-full w-16 h-16 flex items-center justify-center mb-6 shadow-lg transform transition duration-300 hover:rotate-6 ${card.iconBg}`}
                >
                  {card.icon}
                </div>
                <h2 className="text-2xl font-bold mb-3">{card.title}</h2>
                <p className={`mb-6 ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                  {card.description}
                </p>
                <div className="flex items-center text-sm font-medium group">
                  <span className="mr-2">Start Preparing</span>
                  <ChevronRight className="w-4 h-4 transform transition duration-300 group-hover:translate-x-1" />
                </div>
              </div>
            </Link>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="py-8 bg-gray-100 dark:bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            {/* Branding & Contact Info */}
            <div className="mb-4 md:mb-0 text-center md:text-left">
              <div className="flex items-center justify-center md:justify-start space-x-2">
                <Cpu className="w-10 h-10 text-indigo-500 dark:text-indigo-400" />
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100">Switch</h3>
              </div>
              <p className="text-sm mt-2 text-gray-600 dark:text-gray-400">
                Innovating your technical interview preparation.
              </p>
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                Contact us:{' '}
                <a href="mailto:support@switch.com" className="underline hover:text-indigo-500">
                  support@switch.com
                </a>
              </p>
            </div>
            {/* Social Media */}
            <div className="flex space-x-4">
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="text-gray-600 dark:text-gray-400 hover:text-indigo-500">
                <Twitter className="w-6 h-6" />
              </a>
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="text-gray-600 dark:text-gray-400 hover:text-indigo-500">
                <Facebook className="w-6 h-6" />
              </a>
              <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="text-gray-600 dark:text-gray-400 hover:text-indigo-500">
                <Linkedin className="w-6 h-6" />
              </a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="text-gray-600 dark:text-gray-400 hover:text-indigo-500">
                <Instagram className="w-6 h-6" />
              </a>
            </div>
          </div>
          <div className="mt-4 border-t border-gray-300 dark:border-gray-700 pt-4 text-center text-sm text-gray-600 dark:text-gray-400">
            © {new Date().getFullYear()} Switch. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
