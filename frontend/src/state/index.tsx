import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { PaletteMode } from "@mui/material";
import { useNavigate } from "react-router-dom";

interface User {
    username: string;
    firstname: string;
    lastname: string;
    email: string
}

export interface InitialState {
    mode: PaletteMode;
    user: null | User;
    token: null | string;
}

const initialState: InitialState = {
    mode: 'light',
    user: null,
    token: null,
}

export const authSlice = createSlice({
    name: "auth",
    initialState,
    reducers: {
        setMode: (state) => {
            state.mode = state.mode === "light" ? "dark" : "light";
        },  
        setLogin: (state,action: PayloadAction<{ user: User; token: string }>) => {
            state.user = action.payload.user;
            state.token = action.payload.token;
        },
        setLogout: (state) => {
            state.user = null;
            state.token = null;
        }
    }
})

export const {setMode, setLogin, setLogout} = authSlice.actions;
export default authSlice.reducer;