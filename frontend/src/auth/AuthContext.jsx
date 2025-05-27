import React, { createContext, useContext, useState, useEffect } from 'react';
import { Amplify } from 'aws-amplify';
import { signIn as amplifySignIn, signOut as amplifySignOut, getCurrentUser } from 'aws-amplify/auth';

const AuthContext = createContext(null);

// Mock user data
const MOCK_USERS = [
    { email: 'test@example.com', password: 'password123' }
];

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkUser();
    }, []);

    async function checkUser() {
        try {
            // Check localStorage first
            const storedUser = localStorage.getItem('mockUser');
            if (storedUser) {
                setUser(JSON.parse(storedUser));
                setLoading(false);
                return;
            }

            // If no stored user, try AWS Cognito
            try {
                const currentUser = await getCurrentUser();
                setUser(currentUser);
            } catch (error) {
                setUser(null);
            }
        } catch (error) {
            setUser(null);
        }
        setLoading(false);
    }

    const signIn = async (email, password) => {
        try {
            // Check mock users first
            const mockUser = MOCK_USERS.find(
                u => u.email === email && u.password === password
            );

            if (mockUser) {
                const userData = {
                    email: mockUser.email,
                    username: mockUser.email,
                    // Add any other user data you want to store
                };
                localStorage.setItem('mockUser', JSON.stringify(userData));
                setUser(userData);
                return { success: true };
            }

            // If no mock user found, try AWS Cognito
            try {
                const user = await amplifySignIn({ username: email, password });
                setUser(user);
                return { success: true };
            } catch (error) {
                return { success: false, error: error.message };
            }
        } catch (error) {
            return { success: false, error: 'Invalid credentials' };
        }
    };

    const signOut = async () => {
        try {
            // Clear mock user data
            localStorage.removeItem('mockUser');
            setUser(null);

            // Try AWS Cognito sign out
            try {
                await amplifySignOut();
            } catch (error) {
                console.error('AWS Cognito sign out error:', error);
            }

            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    };

    const value = {
        user,
        loading,
        signIn,
        signOut,
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}; 