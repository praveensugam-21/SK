"use client";

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { User } from '@/types';
import api from './api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<User>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const checkAuth = useCallback(async () => {
    try {
      const res = await api.get('/api/auth/me');
      setUser(res.data);
    } catch (err) {
      setUser(null);
      if (typeof window !== 'undefined') {
        localStorage.removeItem('meridian_token');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const login = async (email: string, password: string): Promise<User> => {
    const res = await api.post('/api/auth/login', {
      email: email.trim(),
      password,
    });
    const data = res.data;
    if (data.access_token && typeof window !== 'undefined') {
      localStorage.setItem('meridian_token', data.access_token);
    }
    const loggedInUser = data.user;
    setUser(loggedInUser);
    return loggedInUser;
  };

  const logout = async () => {
    try {
      await api.post('/api/auth/logout');
    } catch (err) {
      console.error("Logout error", err);
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('meridian_token');
      }
      setUser(null);
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, isAuthenticated: !!user, login, logout, checkAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
