import React from "react";
import { Comment } from "react-loader-spinner";
import { useSelector } from "react-redux";

function Loader() {
  const loader = useSelector((state) => state.auth.loader);
  return loader ? (
    <div className="App-loader">
      <Comment
        visible={true}
        height="80"
        width="80"
        ariaLabel="comment-loading"
        wrapperStyle={{}}
        wrapperClass="comment-wrapper"
        color="#fff"
        backgroundColor="#666"
      />
    </div>
  ) : (
    <></>
  );
}

export default Loader;
