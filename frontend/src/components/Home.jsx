import React from "react";
import { Container, Row, Col, Card } from "react-bootstrap";

const Home = () => {
  // You can fetch real data via useEffect + useState
  const dummyStats = {
    totalSales: 1520,
    earnings: 24500,
    bestSellers: ["Product A", "Product B", "Product C"],
    customersAdded: 97,
  };

  return (
    <Container className="mt-5 pt-5">
      <h1 className="mb-4">Dashboard</h1>
      <Row className="g-4">
        <Col md={6} lg={3}>
          <Card className="text-center shadow-sm">
            <Card.Body>
              <Card.Title>Total Sales</Card.Title>
              <Card.Text className="fs-4">{dummyStats.totalSales}</Card.Text>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6} lg={3}>
          <Card className="text-center shadow-sm">
            <Card.Body>
              <Card.Title>Earnings</Card.Title>
              <Card.Text className="fs-4">${dummyStats.earnings.toLocaleString()}</Card.Text>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6} lg={3}>
          <Card className="text-center shadow-sm">
            <Card.Body>
              <Card.Title>Customers Added</Card.Title>
              <Card.Text className="fs-4">{dummyStats.customersAdded}</Card.Text>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6} lg={3}>
          <Card className="text-center shadow-sm">
            <Card.Body>
              <Card.Title>Best-Selling Products</Card.Title>
              <ul className="list-unstyled mb-0">
                {dummyStats.bestSellers.map((item, idx) => (
                  <li key={idx}>• {item}</li>
                ))}
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Home;
