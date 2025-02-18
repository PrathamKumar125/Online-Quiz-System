import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider, createBrowserRouter, Navigate } from 'react-router-dom';
import App from './App';
import Login from './components/auth/Login';
import QuizDashboard from './components/quiz/QuizDashboard';
import CreateQuiz from './components/quiz/CreateQuiz';
import UserQuiz from './components/quiz/UserQuiz';
import UserScore from './components/quiz/UserScore';
import PrivateRoute from './components/common/PrivateRoute';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <Navigate to="/login" replace />
      },
      {
        path: "login",
        element: <Login />
      },
      {
        path: "dashboard",
        element: <PrivateRoute><QuizDashboard /></PrivateRoute>
      },
      {
        path: "create-quiz",
        element: <PrivateRoute><CreateQuiz /></PrivateRoute>
      },
      {
        path: "quiz/:quizId",
        element: <PrivateRoute><UserQuiz /></PrivateRoute>
      },
      {
        path: "score/:quizId",
        element: <PrivateRoute><UserScore /></PrivateRoute>
      },
      {
        path: "*",
        element: <Navigate to="/login" replace />
      }
    ]
  }
], {
  future: {
    v7_startTransition: true,
    v7_relativeSplatPath: true
  }
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider 
      router={router} 
      future={{
        v7_startTransition: true
      }}
    />
  </React.StrictMode>
);