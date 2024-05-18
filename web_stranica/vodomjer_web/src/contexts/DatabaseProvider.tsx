import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

type DatabaseContextType = {
  databaseAvailable: boolean;
  setDatabaseAvailable: (available: boolean) => void;
  uploadedFilePath: string | null;
  setUploadedFilePath: (path: string | null) => void;
};

const DatabaseContext = createContext<DatabaseContextType | undefined>(undefined);

type DatabaseProviderProps = {
  children: ReactNode;
};

export const DatabaseProvider = ({ children }: DatabaseProviderProps) => {
  const [databaseAvailable, setDatabaseAvailable] = useState<boolean>(false);
  const [uploadedFilePath, setUploadedFilePath] = useState<string | null>(null);

  // Load initial state from session storage
  useEffect(() => {
    const savedDatabaseAvailable = sessionStorage.getItem('databaseAvailable') === 'true';
    const savedFilePath = sessionStorage.getItem('uploadedFilePath');

    setDatabaseAvailable(savedDatabaseAvailable);
    setUploadedFilePath(savedFilePath);
  }, []);

  // Update session storage when values change
  useEffect(() => {
    sessionStorage.setItem('databaseAvailable', databaseAvailable.toString());
    if (uploadedFilePath) {
      sessionStorage.setItem('uploadedFilePath', uploadedFilePath);
    } else {
      sessionStorage.removeItem('uploadedFilePath');
    }
  }, [databaseAvailable, uploadedFilePath]);

  return (
    <DatabaseContext.Provider value={{ databaseAvailable, setDatabaseAvailable, uploadedFilePath, setUploadedFilePath }}>
      {children}
    </DatabaseContext.Provider>
  );
};

export const useDatabase = () => {
  const context = useContext(DatabaseContext);
  if (!context) {
    throw new Error('useDatabase must be used within a DatabaseProvider');
  }
  return context;
};
