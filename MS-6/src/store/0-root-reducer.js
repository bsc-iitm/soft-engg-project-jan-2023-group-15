import { combineReducers } from "redux";
import authReducer from "./auth/authSlice";

const reducer = combineReducers({
	auth: authReducer,
});
const rootReducer = (state = {}, action) => reducer(state, action);

export default rootReducer;
