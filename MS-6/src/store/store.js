import { configureStore } from "@reduxjs/toolkit";
import rootReducer from "./0-root-reducer";

const store = configureStore({
	reducer: rootReducer,
	middleware: (getDefaultMiddleware) => getDefaultMiddleware(),
	devTools: true,
});

export default store;
