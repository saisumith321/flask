import { createBrowserRouter } from '@datadog/browser-rum-react/react-router-v6';
import { RouterProvider, Navigate } from 'react-router-dom';

import { useNhostAuthContext } from 'frontend/contexts/nhost-auth.provider';
import { SignInPage } from 'frontend/pages/auth/signin';
import { SignUpPage } from 'frontend/pages/auth/signup';
import { ChatPage } from 'frontend/pages/chat/chat';
import { ProtectedRoute } from 'frontend/components/protected-route/protected-route';

export const AppRoutes = () => {
  const { isAuthenticated, isLoading } = useNhostAuthContext();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  const routes = [
    {
      path: '/',
      element: isAuthenticated ? <Navigate to="/chat" replace /> : <Navigate to="/signin" replace />,
    },
    {
      path: '/signin',
      element: isAuthenticated ? <Navigate to="/chat" replace /> : <SignInPage />,
    },
    {
      path: '/signup',
      element: isAuthenticated ? <Navigate to="/chat" replace /> : <SignUpPage />,
    },
    {
      path: '/chat',
      element: (
        <ProtectedRoute>
          <ChatPage />
        </ProtectedRoute>
      ),
    },
  ];

  const router = createBrowserRouter(routes);

  return <RouterProvider router={router} />;
};
