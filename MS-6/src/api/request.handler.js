import axios from "axios";
import { toast } from "react-toastify";
import store from "../store/store";
import { setLoader } from "../store/auth/authSlice";

export const ErrorObject = {
  message: "",
  success: false,
  code: 400,
  data: {},
};

export function isMethodProper(method) {
  return ["get", "post", "put", "delete"].includes(method);
}

export default function request_caller({
  method = "post",
  endpoint = "",
  data = {},
  successToast = false,
  errorToast = true,
  headers = {},
  isAuthenticated = true,
}) {
  return new Promise(async (resolve, reject) => {
    const responseObj = { ...ErrorObject };
    if (!isMethodProper(method)) {
      responseObj.message = "Method is not allowed";
      reject(responseObj);
      return;
    }

    if (isAuthenticated) {
      if (!localStorage.getItem("token") || !localStorage.getItem("key")) {
        responseObj.message = "Please login first";
        toast.warn(responseObj.message);
        reject(responseObj);
        return;
      }
      headers["Authorization"] = localStorage.getItem("token");
      data["key"] = localStorage.getItem("key");
    }

    const req_obj = {
      method: method,
      url: "http://localhost:5000/api" + endpoint,
      params: method === "get" ? data : {},
      data: method !== "get" ? data : {},
      responseType: "json",
      // timeout: 30000,
      headers: headers,
    };
    console.log("sending to req_obj", req_obj);
    store.dispatch(setLoader(true));
    axios
      .request(req_obj)
      .then((res) => {
        const data = res.data;
        if (data.success) {
          if (successToast) {
            toast.success(data.message);
          }
          resolve(data);
        } else {
          reject(data);
        }
      })
      .catch((error) => {
        // ConsoleMsg.log(error.response);
        let err = {};
        if (error && error?.response?.status === 0 && error?.message) {
          responseObj.message = error.message;
          err = responseObj;
        } else if (
          error &&
          error?.response?.data?.success === false &&
          error?.response?.data?.message
        ) {
          err = error.response.data;
        } else if (axios.isCancel(error)) {
          responseObj.code = 100;
          responseObj.message = "Cancelled";
          err = responseObj;
        } else {
          console.log(error, "error");
          responseObj.message =
            "Something went wrong on our side. \
					Please try again. Sorry for the inconvenience";
          err = responseObj;
        }

        if (errorToast) {
          toast.error(err.message);
        }
        reject(err);
      })
      .finally(() => {
        store.dispatch(setLoader(false));
      });
  });
}
