import React from "react";

// for styling
import { Typography } from "@mui/material";
import styled from "@emotion/styled";

// CSS - Material UI
const useStyles = styled({
  title: {
    marginTop: "22px",
    fontSize: "30px",
    textAlign: "center",
    fontWeight: "bold",
  },
});

const HeaderContent = (props) => {
  const classes = useStyles();

  return (
    <>
      <Typography className={classes.title}>{props.header}</Typography>
    </>
  );
};

export default HeaderContent;
