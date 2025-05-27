import React, { createContext, useContext, useState, useEffect } from 'react';
import { Auth } from 'aws-amplify';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkUser();
    }, []);

    async function checkUser() {
        try {
            const currentUser = await Auth.currentAuthenticatedUser();
            setUser(currentUser);
        } catch (error) {
            setUser(null);
        }
        setLoading(false);
    }

    const signIn = async (email, password) => {
        try {
            const user = await Auth.signIn(email, password);
            setUser(user);
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    };

    const signOut = async () => {
        try {
            await Auth.signOut();
            setUser(null);
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