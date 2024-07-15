import React from "react";
import { useState } from "react";
// For Styling
import styled from "@emotion/styled";
import { Card, Col } from "react-bootstrap";

// CSS -Material UI
const useStyles = styled((theme) => ({
  image: {
    width: "100%",
    height: "450px",
    [theme.breakpoints.down("sm")]: {
      height: "300px",
    },
  },
  link: {
    textDecoration: "none",
    color: "inherit",
  },
  txt: {
    [theme.breakpoints.down("sm")]: {
      fontSize: "14px",
    },
  },
}));

const ProductCard = (props) => {
  const classes = useStyles();

  const [result, setResult] = useState("");

  const handleTryAll = async (input) => {
    try {
      const CART = [input]; // Replace with actual CART array or fetch from state/props
      console.log("CART:", CART);
      const formData = new FormData();
      formData.append("mydata", CART.join(" "));

      const response = await fetch("http://localhost:5001/tryall", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.text(); // Assuming server responds with plain text
      setResult(data); // Display the response from the server
      console.log("SAUMYA:", data);
    } catch (error) {
      console.error("Error during tryAll fetch request:", error);
      // Handle error
      setResult("Error during Try All request");
    }
  };

  const addToCart = (input) => {
    // if (CART.indexOf(input) == -1) {
    //   CART.push(input);
    // }
    // // alert("Added Product To Cart")
  };

  const tryAll = async (input) => {
    handleTryAll(input)
      .then((data) => {
        console.log("Received data from server:", data);
        // Handle the data received from the server
      })
      .catch((error) => {
        console.error("Error during request:", error);
        // Handle errors that occurred during the request
      });
  };

  return (
    <>
      {/* Getting data from props */}
      <Col xs={6} md={4} lg={4}>
        <a href={`/${props.title}`} className={classes.link}>
          <Card>
            <Card.Img variant="top" src={props.url} className={classes.image} />
            <Card.Body>
              <Card.Title className={classes.txt}>{props.title}</Card.Title>
              <Card.Text className={classes.txt}>{props.type}</Card.Text>
              <Card.Text>
                ₹ {props.price}
                <span
                  style={{ textDecoration: "line-through", marginLeft: "10px" }}
                >
                  ₹ {props.aPrice}
                </span>
                <span style={{ color: "red", marginLeft: "10px" }}>
                  {(
                    ((props.aPrice - props.price) / props.aPrice) *
                    100
                  ).toFixed()}
                  %OFF
                </span>
              </Card.Text>
            </Card.Body>
            <Card.Footer>
              <Card.Text>Inclusive of All Taxes</Card.Text>
            </Card.Footer>
          </Card>
        </a>
      </Col>
    </>
  );
};

export default ProductCard;
