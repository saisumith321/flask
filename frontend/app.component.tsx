import { ErrorBoundary } from '@datadog/browser-rum-react';
import React, { useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import { NhostProvider } from '@nhost/react';
import { NhostApolloProvider } from '@nhost/react-apollo';

import { ErrorFallback } from './pages/error';
import { Logger } from './utils/logger';

import { AccountProvider } from 'frontend/contexts';
import { NhostAuthProvider } from 'frontend/contexts/nhost-auth.provider';
import { Config } from 'frontend/helpers';
import { AppRoutes } from 'frontend/routes';
import InspectLet from 'frontend/vendor/inspectlet';
import { nhost } from './config/nhost';

Logger.init();

export default function App(): React.ReactElement {
  useEffect(() => {
    const inspectletKey = Config.getConfigValue('inspectletKey');

    if (inspectletKey) {
      InspectLet();
    }
  }, []);

  return (
    <ErrorBoundary fallback={ErrorFallback}>
      <NhostProvider nhost={nhost}>
        <NhostApolloProvider nhost={nhost}>
          <NhostAuthProvider>
            <AccountProvider>
              <Toaster />
              <AppRoutes />
            </AccountProvider>
          </NhostAuthProvider>
        </NhostApolloProvider>
      </NhostProvider>
    </ErrorBoundary>
  );
}
