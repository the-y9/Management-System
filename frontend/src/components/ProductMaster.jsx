import "../style/style.css";
import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { FormControl, InputGroup } from "react-bootstrap";
import * as Icon from "react-bootstrap-icons";

// import AddEmp from "./AddEmp"; // Rename to AddProduct if needed
// import AdminManageModal from "./AdminMan";
import GenericTable from "./GenericTable";
// import UpEmp from "./EditEmp"; // Rename to EditProduct if needed

function Display() {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState("");

  const colHeaders = [
    { key: "stock_no", label: "Stock No." },
    { key: "name", label: "Product Name" },
    { key: "category", label: "Category" },
    { key: "qty_per_unit", label: "Qty." },
    { key: "volume_points", label: "Volume Points" },
    { key: "mrp", label: "MRP" },
    { key: "retail_price", label: "Retail Price" },
    { key: "earn_base", label: "*Earn Base" },
    { key: "per_25", label: "Associates - 25%" },
    { key: "per_35", label: "Senior Consultant - 35%" },
    { key: "per_42", label: "Qualified Producer/Success Builder - 42%" },
    { key: "per_50", label: "Supervisor - 50%" },
  ];


  const searchableFields = colHeaders.map((col) => col.key);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/products");
        const data = await response.json();
        setProducts(data);
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    };

    fetchData();
  }, []);

  const filteredData = products.filter((item) => {
    return (
      search === "" ||
      searchableFields.some((field) =>
        item[field]?.toString().toLowerCase().includes(search.toLowerCase())
      )
    );
  });

  const clearFilter = () => {
    setSearch("");
  };

  const renderCustomActions = (item) => (
    <>
      <Button variant="danger" onClick={() => console.log("Delete", item.stockNo)}>
        Delete
      </Button>
      {/* <UpEmp data={item} /> */}
    </>
  );

  return (
    <div className="display-container">
      <h1 className="text-center my-4">Product Master</h1>

      <Container>
        <Row className="align-items-start">
          <Col md={8}>
            <InputGroup className="mb-3">
              <InputGroup.Text>
                <Icon.Search />
              </InputGroup.Text>
              <FormControl
                type="search"
                placeholder="Search products"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </InputGroup>
            <h5 className="text-muted">Search: {search}</h5>
          </Col>

          <Col md={4} className="d-flex flex-column gap-2">
            <Button variant="warning" onClick={clearFilter}>
              Clear Search
            </Button>
            {/* <AddEmp /> */}
            {/* <AdminManageModal /> */}
          </Col>
        </Row>
      </Container>

      <Container fluid className="mt-4">
        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <span>Rows Returned: {filteredData.length}</span>
        </div>
        <GenericTable
          colHeaders={colHeaders}
          data={filteredData}
          renderActions={renderCustomActions}
          variant="light"
        />
      </Container>
    </div>
  );
}

export default Display;
