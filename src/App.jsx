// import React from 'react';
// import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import HomePage from './HomePage.jsx';
// import CodeEditorPage from './CodeEditor.jsx';
// import TechnicalInterviewPage from './TechnicalInterviewPage.jsx';
// import HrInterviewPage from './HrInterviewPage.jsx';
// import InstantPreparationPage from './InstantPreparationPage.jsx'; // new page
// import Exam from './Exam.jsx'
// import Dashboard from './dashboard.jsx'
// import Job from './Job.jsx';
// import Login from './login.jsx';
// function App() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<Login/>} />
//         <Route path="/Home-page" element={<HomePage />} />
//         <Route path="/Test" element={<Dashboard />} />
//         <Route path="/technical-interview" element={<TechnicalInterviewPage />} />
//         <Route path="/code" element={<CodeEditorPage />} />
//         <Route path="/instant-preparation" element={<InstantPreparationPage />} />
//         <Route path="/tests" element={<Exam />} />
//         <Route path="/Job" element={<Job />} />


//       </Routes>
//     </Router>
//   );
// }

// export default App;


// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import HomePage from './HomePage.jsx';
import CodeEditorPage from './CodeEditor.jsx';
import TechnicalInterviewPage from './TechnicalInterviewPage.jsx';
import HrInterviewPage from './HrInterviewPage.jsx';
import InstantPreparationPage from './InstantPreparationPage.jsx'; // new page
import Exam from './Exam.jsx';
import Dashboard from './dashboard.jsx';
import Job from './Job.jsx';
import Login from './login.jsx';
import Jobls from './list_jb.jsx';

// A ProtectedRoute component to guard private routes
const ProtectedRoute = ({ children }) => {
  // Check if the user is logged in (sessionStorage should have 'loggedIn' set to 'true')
  const isLoggedIn = sessionStorage.getItem('loggedIn') === 'true';
  return isLoggedIn ? children : <Navigate to="/" replace />;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Route */}
        <Route path="/" element={<Login />} />
        
        {/* Protected Routes */}
        <Route
          path="/Home-page"
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/Test"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/technical-interview"
          element={
            <ProtectedRoute>
              <TechnicalInterviewPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/code"
          element={
            <ProtectedRoute>
              <CodeEditorPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/instant-preparation"
          element={
            <ProtectedRoute>
              <InstantPreparationPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/tests"
          element={
            <ProtectedRoute>
              <Exam />
            </ProtectedRoute>
          }
        />
        <Route
          path="/Job"
          element={
            <ProtectedRoute>
              <Job />
            </ProtectedRoute>
          }
        />
        <Route
          path="/job-list"
          element={
            <ProtectedRoute>
              <Jobls/>
            </ProtectedRoute>
          }
        />


      </Routes>
    </Router>
  );
}

export default App;
