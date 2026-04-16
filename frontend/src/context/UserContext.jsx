import { createContext } from "react";

export const UserContext = createContext({
    username: import.meta.env.VITE_USERNAME
});