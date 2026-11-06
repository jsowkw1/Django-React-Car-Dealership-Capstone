import { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { api } from './api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.me()
      .then((data) => setUser(data.isAuthenticated ? data : null))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (userName, password) => {
    const data = await api.login(userName, password);
    setUser(data.user);
    return data.user;
  }, []);

  const register = useCallback(async (form) => {
    const data = await api.register(form);
    setUser(data.user);
    return data.user;
  }, []);

  const logout = useCallback(async () => {
    const data = await api.logout();
    setUser(null);
    return data.loggedOut;
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
