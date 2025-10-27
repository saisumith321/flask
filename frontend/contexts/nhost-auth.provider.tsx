import React, { createContext, PropsWithChildren, useContext } from 'react';
import { useAuthenticated, useEmailPasswordSignIn, useEmailPasswordSignUp, useSignOut, useUserId, useUserEmail } from '@nhost/react';
import { Nullable } from 'frontend/types/common-types';

type NhostAuthContextType = {
  isLoading: boolean;
  isAuthenticated: boolean;
  userId: Nullable<string>;
  userEmail: Nullable<string>;
  signUp: (email: string, password: string) => Promise<void>;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  signUpLoading: boolean;
  signInLoading: boolean;
  signUpError: any;
  signInError: any;
};

const NhostAuthContext = createContext<Nullable<NhostAuthContextType>>(null);

export const useNhostAuthContext = (): NhostAuthContextType =>
  useContext(NhostAuthContext) as NhostAuthContextType;

export const NhostAuthProvider: React.FC<PropsWithChildren> = ({ children }) => {
  const isAuthenticated = useAuthenticated();
  const userId = useUserId();
  const userEmail = useUserEmail();
  
  const {
    signUp: signUpEmailPassword,
    isLoading: signUpLoading,
    error: signUpError,
  } = useEmailPasswordSignUp();

  const {
    signIn: signInEmailPassword,
    isLoading: signInLoading,
    error: signInError,
  } = useEmailPasswordSignIn();

  const { signOut } = useSignOut();

  const signUp = async (email: string, password: string) => {
    signUpEmailPassword(email, password);
  };

  const signIn = async (email: string, password: string) => {
    signInEmailPassword(email, password);
  };

  const handleSignOut = async () => {
    signOut();
  };

  return (
    <NhostAuthContext.Provider
      value={{
        isLoading: signUpLoading || signInLoading,
        isAuthenticated,
        userId: userId || null,
        userEmail: userEmail || null,
        signUp,
        signIn,
        signOut: handleSignOut,
        signUpLoading,
        signInLoading,
        signUpError,
        signInError,
      }}
    >
      {children}
    </NhostAuthContext.Provider>
  );
};