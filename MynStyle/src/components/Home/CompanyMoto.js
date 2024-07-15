import React from "react";

// For styling
import { Box, Typography } from "@mui/material";
import styled from "@emotion/styled";

// CSS - Material UI
const useStyles = styled((theme) => ({
  bTxt: {
    marginTop: "10px",
    marginBottom: "10px",
    backgroundColor: "red",
    height: "60px",
    textAlign: "center",
    width: "100%",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  boxTxt: {
    fontSize: "30px",
    fontWeight: "bold",
    color: "white",
    textAlign: "center",
    [theme.breakpoints.down("sm")]: {
      fontSize: "20px",
    },
  },
  txt: {
    textAlign: "center",
    fontSize: "30px",
    fontWeight: "bold",
    marginTop: "10px",
    marginBottom: "10px",
    [theme.breakpoints.down("sm")]: {
      fontSize: "20px",
    },
  },
}));

const CompanyMoto = () => {
  const classes = useStyles();
  return (
    <>
      <Box className={classes.bTxt}>
        <Typography className={classes.boxTxt}>
          India's No.1 Fashion Brand
        </Typography>
      </Box>
      <Typography className={classes.txt}>
        Over 10 Million Happy Customers
      </Typography>
    </>
  );
};

export default CompanyMoto;
