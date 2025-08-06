import { useState, useEffect } from "react";
import { Modal, Button, Form } from "react-bootstrap";

const AddModal = ({ show, onClose, fields, onSave }) => {
  const [formData, setFormData] = useState({});

  // Initialize form data with empty strings for each field when modal opens
  useEffect(() => {
    if (show) {
      const initialData = {};
      fields.forEach((field) => {
        initialData[field.key] = "";
      });
      setFormData(initialData);
    }
  }, [show, fields]);

  const handleChange = (key, value) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async () => {
    await onSave(formData);
    onClose();
  };

  return (
    <Modal show={show} onHide={onClose}>
      <Modal.Header closeButton>
        <Modal.Title>Add New Item</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          {fields.map((field) => (
            <Form.Group className="mb-3" key={field.key}>
              <Form.Label>{field.label}</Form.Label>
              {field.type === "textarea" ? (
                <Form.Control
                  as="textarea"
                  rows={3}
                  value={formData[field.key] || ""}
                  onChange={(e) => handleChange(field.key, e.target.value)}
                />
              ) : (
                <Form.Control
                  type={field.type || "text"}
                  value={formData[field.key] || ""}
                  onChange={(e) => handleChange(field.key, e.target.value)}
                />
              )}
            </Form.Group>
          ))}
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onClose}>
          Cancel
        </Button>
        <Button variant="success" onClick={handleSubmit}>
          Add Item
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default AddModal;
