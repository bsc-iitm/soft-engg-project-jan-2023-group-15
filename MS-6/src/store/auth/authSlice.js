import { createSlice } from "@reduxjs/toolkit";

const authSlice = createSlice({
	name: "auth",
	initialState: {
		user: null,
		tickets: null,
		loader: false,
		specificTicket: {},
		faqs:null,
		staffList: null,
		faqs_request: null,
		blocked_user_lists: null,
	},

	reducers: {
		setUser(state, action) {
			state.user = action.payload;
		},
		setLoader(state, action) {
			state.loader = action.payload;
		},
		setTickets(state, action) {
			state.tickets = action.payload;
		},
		setSpecificTicket(state, action) {
			state.specificTicket = action.payload;
		},
		setFAQs(state, action){
			state.faqs = action.payload;
		},
		setStaffList(state, action){
			state.staffList = action.payload;
		},
		setFAQRequests(state, action){
			state.faqs_request = action.payload;
		},
		setBlockedUserLists(state, action){
			state.blocked_user_lists = action.payload;
		}
	},
});

export const {
	setUser,
	setLoader,
	setTickets,
	setSpecificTicket,
	setFAQs,
	setStaffList,
	setFAQRequests,
	setBlockedUserLists,
} = authSlice.actions;

export default authSlice.reducer;
