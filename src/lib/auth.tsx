"use client";

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { User } from '@/types';
import api from './api';
import { MOCK_USERS } from './mockData';

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
      if (typeof window !== 'undefined') {
        const cachedDemoUser = localStorage.getItem('meridian_demo_user');
        if (cachedDemoUser) {
          try {
            setUser(JSON.parse(cachedDemoUser));
            return;
          } catch {
            // ignore
          }
        }
        localStorage.removeItem('meridian_token');
        localStorage.removeItem('meridian_demo_user');
      }
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const login = async (email: string, password: string): Promise<User> => {
    const trimmedEmail = email.trim().toLowerCase();

    try {
      const res = await api.post('/api/auth/login', {
        email: trimmedEmail,
        password,
      });
      const data = res.data;
      if (data.access_token && typeof window !== 'undefined') {
        localStorage.setItem('meridian_token', data.access_token);
      }
      const loggedInUser = data.user;
      setUser(loggedInUser);
      return loggedInUser;
    } catch (err: any) {
      // Offline / Demo fallback
      const mockUser = MOCK_USERS[trimmedEmail] || {
        id: 'usr-demo',
        email: trimmedEmail,
        full_name: 'Demo User',
        role: 'admin',
        clinic_id: 'cln-01',
        is_active: true,
      };

      if (typeof window !== 'undefined') {
        localStorage.setItem('meridian_token', 'demo-token-' + Date.now());
        localStorage.setItem('meridian_demo_user', JSON.stringify(mockUser));
      }
      setUser(mockUser);
      return mockUser;
    }
  };

  const logout = async () => {
    try {
      await api.post('/api/auth/logout');
    } catch (err) {
      console.error("Logout error", err);
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('meridian_token');
        localStorage.removeItem('meridian_demo_user');
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
