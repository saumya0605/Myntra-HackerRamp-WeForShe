import React from "react";
// for styling
import styled from "@emotion/styled";

// CSS - Material UI
const useStyles = styled({
  image: {
    width: "100%",
    height: "auto",
  },
});

const PosterImage = (props) => {
  const classes = useStyles();

  return (
    <>
      {/* getting data from props */}
      <img src={props.url} alg={props.alt} className={classes.image} />
    </>
  );
};

export default PosterImage;
