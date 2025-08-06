import "../style/style.css";
import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { FormControl, InputGroup } from "react-bootstrap";
import * as Icon from "react-bootstrap-icons";

import GenericTable from "./GenericTable";
import EditModal from "./EditModal";
import AddModal from "./AddModal";

function Sales() {
  const [sales, setSales] = useState([]);
  const [search, setSearch] = useState("");

  const colHeaders = [
  { key: "sale_id", label: "Sale ID", type: "text" },
  { key: "customer_id", label: "Customer ID", type: "text" },
  { key: "date", label: "Date", type: "date" },
  { key: "mode", label: "Mode", type: "text" },
  { key: "total_amount", label: "Total Amount", type: "number" },
  { key: "total_volume_points", label: "Total Volume Points", type: "number" },
];




  const searchableFields = colHeaders.map((col) => col.key);
  const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/sales");
        const data = await response.json();
        setSales(data);
      } catch (error) {
        console.error("Failed to fetch sales:", error);
      }
    };

  useEffect(() => {
    fetchData();
  }, []);

  const filteredData = sales.filter((item) => {
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

  const [showEditModal, setShowEditModal] = useState(false);
  const [currentItem, setCurrentItem] = useState(null);
  const editableFields = colHeaders;

  const handleSave = async (updatedItem) => {
      try {
        const response = await fetch(`http://localhost:8000/sale/${updatedItem.sale_id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(updatedItem),
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.detail || "Update failed");
        }

        alert("Sale updated successfully");
        await fetchData();
      } catch (error) {
        console.error("Error updating sale:", error.message);
        alert("Failed to update sale: " + error.message);
      }
    };

    const [showAddModal, setShowAddModal] = useState(false);
    const handleAddSave = async (newItem) => {
        try {
            const response = await fetch("http://localhost:8000/sale", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(newItem),
            });

            if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to create sale");
            }

            alert("Sale created successfully!");
            
            // Optionally refresh data
            await fetchData(); // Assuming you have a fetchData function

        } catch (error) {
            console.error("Error adding sale:", error.message);
            alert("Failed to add sale: " + error.message);
        }
        };



  const renderCustomActions = (item) => {
    const handleDelete = async () => {
      try {
        const response = await fetch(`http://localhost:8000/sale/${item.sale_id}`, {
          method: "DELETE",
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.detail || "Delete failed");
        }

        alert("Sale deleted successfully");
        await fetchData();
        
      } catch (error) {
        console.error("Error deleting sale:", error.message);
        alert("Failed to delete sale: " + error.message);
      }
    };


    const handleEditClick = () => {
      setCurrentItem(item);
      setShowEditModal(true);
    };


    return (
      <>
        <Button variant="danger" onClick={handleDelete}>Delete</Button>
        <Button variant="info" onClick={handleEditClick}>Edit</Button>
      </>
    );
  };


  return (
    <div className="display-container">
      <h1 className="text-center my-4">Sale Master</h1>

      <Container>
        <Row className="align-items-start">
          <Col md={8}>
            <InputGroup className="mb-3">
              <InputGroup.Text>
                <Icon.Search />
              </InputGroup.Text>
              <FormControl
                type="search"
                placeholder="Search sales"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </InputGroup>
          </Col>

          <Col md={4} className="d-flex flex-column gap-2">
            <Button variant="warning" onClick={clearFilter}>
              Clear Search
            </Button>
            {/* <AddEmp /> */}
            {/* <AdminManageModal /> */}
          </Col>
        </Row>
            <Button onClick={() => setShowAddModal(true)}>Add Sale</Button>
            <AddModal
                show={showAddModal}
                onClose={() => setShowAddModal(false)}
                fields={colHeaders}
                onSave={handleAddSave}
            />

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
          rowKey="sale_id"
        />
        
        <EditModal
          show={showEditModal}
          onClose={() => setShowEditModal(false)}
          item={currentItem}
          fields={editableFields}
          onSave={handleSave}
        />
      </Container>
    </div>
  );
}

export default Sales;
