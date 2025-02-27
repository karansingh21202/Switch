import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const LoginRegister = ({ onLoginSuccess }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Custom confirmation using toastify
  const confirmRegistration = () =>
    new Promise((resolve) => {
      toast.info(
        <div>
          <p className="text-sm">
            An account already exists. Registering a new account will override the existing one.
          </p>
          <div className="flex justify-end space-x-4 mt-4">
            <button
              className="px-4 py-1 bg-green-500 text-white rounded hover:bg-green-600"
              onClick={() => {
                toast.dismiss();
                resolve(true);
              }}
            >
              Yes
            </button>
            <button
              className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
              onClick={() => {
                toast.dismiss();
                resolve(false);
              }}
            >
              No
            </button>
          </div>
        </div>,
        { autoClose: false, closeOnClick: false }
      );
    });

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    if (password !== confirmPassword) {
      setError('Passwords do not match!');
      return;
    }
    // Check if an account already exists
    if (sessionStorage.getItem('user')) {
      const proceed = await confirmRegistration();
      if (!proceed) return;
    }
    // Save the new account data to sessionStorage
    const user = { email, username, password };
    sessionStorage.setItem('user', JSON.stringify(user));
    sessionStorage.setItem('loggedIn', 'true');
    // Clear form fields if desired
    setEmail('');
    setUsername('');
    setPassword('');
    setConfirmPassword('');
    // Redirect to Home-page after successful registration
    navigate('/Home-page');
    onLoginSuccess && onLoginSuccess();
  };

  const handleLogin = (e) => {
    e.preventDefault();
    setError('');
    const storedUser = sessionStorage.getItem('user');
    if (!storedUser) {
      setError('No registered user found. Please register first.');
      return;
    }
    const user = JSON.parse(storedUser);
    if (username === user.username && password === user.password) {
      sessionStorage.setItem('loggedIn', 'true');
      navigate('/Home-page');
      onLoginSuccess && onLoginSuccess();
    } else {
      setError('Invalid username or password.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <ToastContainer />
      <div className="w-full max-w-md bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-center text-gray-800 dark:text-gray-200 mb-6">
          {isRegister ? 'Register' : 'Login'}
        </h2>
        {error && <div className="mb-4 text-red-500 text-center">{error}</div>}
        <form onSubmit={isRegister ? handleRegister : handleLogin}>
          {/* Username Field */}
          <div className="mb-4">
            <label htmlFor="username" className="block text-gray-700 dark:text-gray-300 mb-2">
              Username
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
              required
            />
          </div>
          {/* Email Field for Registration */}
          {isRegister && (
            <div className="mb-4">
              <label htmlFor="email" className="block text-gray-700 dark:text-gray-300 mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
                required
              />
            </div>
          )}
          {/* Password Field */}
          <div className="mb-4">
            <label htmlFor="password" className="block text-gray-700 dark:text-gray-300 mb-2">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
              required
            />
          </div>
          {/* Confirm Password Field for Registration */}
          {isRegister && (
            <div className="mb-4">
              <label htmlFor="confirmPassword" className="block text-gray-700 dark:text-gray-300 mb-2">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
                required
              />
            </div>
          )}
          <button
            type="submit"
            className="w-full bg-indigo-500 text-white py-2 rounded hover:bg-indigo-600 transition-colors"
          >
            {isRegister ? 'Register' : 'Login'}
          </button>
        </form>
        <p className="mt-4 text-center text-gray-600 dark:text-gray-300">
          {isRegister ? 'Already have an account?' : "Don't have an account?"}{' '}
          <button
            onClick={() => {
              setIsRegister(!isRegister);
              setError('');
              // Optionally clear form fields when toggling
              setUsername('');
              setPassword('');
              setConfirmPassword('');
              setEmail('');
            }}
            className="text-indigo-500 hover:underline focus:outline-none"
          >
            {isRegister ? 'Login' : 'Register'}
          </button>
        </p>
      </div>
    </div>
  );
};

export default LoginRegister;
