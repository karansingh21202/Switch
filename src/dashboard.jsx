import React from 'react';
import { Link } from 'react-router-dom';
import { Brain, Target, Terminal } from 'lucide-react';

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-5xl font-bold text-gray-800 mb-2 text-center">Welcome to PrepMaster</h1>
        <p className="text-gray-600 text-center mb-12 text-lg">Your AI-powered companion for comprehensive interview and exam preparation</p>
        
        <div className="grid gap-8 grid-cols-1 md:grid-cols-3">
          {/* AI Mock Interview Card */}
          <Link to="/Technical-interview" className="group">
            <div className="bg-white h-full p-8 rounded-2xl shadow-md hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
              <div className="bg-indigo-100 rounded-full w-16 h-16 flex items-center justify-center mb-6 group-hover:bg-indigo-200 transition-colors">
                <Brain className="w-8 h-8 text-indigo-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">AI Mock Interview</h2>
              <div className="space-y-4">
                <p className="text-gray-600 leading-relaxed">Practice interviews for any field with our adaptive AI system. Perfect for:</p>
                <ul className="text-gray-600 space-y-2">
                  <li>• Academic interviews </li>
                  <li>• Professional role interviews</li>
                  <li>• Subject-specific preparations</li>
                  <li>• Personalized feedback and tips</li>
                </ul>
              </div>
            </div>
          </Link>

          {/* Multiple Choice Questions Card */}
          <Link to="/tests" className="group">
            <div className="bg-white h-full p-8 rounded-2xl shadow-md hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
              <div className="bg-rose-100 rounded-full w-16 h-16 flex items-center justify-center mb-6 group-hover:bg-rose-200 transition-colors">
                <Target className="w-8 h-8 text-rose-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Multiple Choice Questions</h2>
              <div className="space-y-4">
                <p className="text-gray-600 leading-relaxed">Comprehensive question bank covering various domains:</p>
                <ul className="text-gray-600 space-y-2">
                  <li>• Academic subjects (Physics, Chemistry, Math)</li>
                  <li>• Competitive exam preparation</li>
                  <li>• Professional certification practice</li>
                  <li>• Custom quiz generation</li>
                </ul>
              </div>
            </div>
          </Link>

          {/* Practice Section Card */}
          <Link to="/code" className="group">
            <div className="bg-white h-full p-8 rounded-2xl shadow-md hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
              <div className="bg-emerald-100 rounded-full w-16 h-16 flex items-center justify-center mb-6 group-hover:bg-emerald-200 transition-colors">
                <Terminal className="w-8 h-8 text-emerald-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Coding Practice</h2>
              <div className="space-y-4">
                <p className="text-gray-600 leading-relaxed">Level up your coding skills with our interactive platform featuring:</p>
                <ul className="text-gray-600 space-y-2">
                  <li>• Real-time code compilation</li>
                  <li>• Custom test case creation</li>
                  <li>• Performance metrics</li>
                  <li>• Solution explanations</li>
                </ul>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;