import { useState, useEffect } from "react";
import { Modal, Button, Form } from "react-bootstrap";

const EditModal = ({ show, onClose, item, fields, onSave }) => {
  const [formData, setFormData] = useState({});

  useEffect(() => {
    if (item) setFormData(item);
  }, [item]);

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
        <Modal.Title>Edit Item</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          {fields.map((field) => (
            <Form.Group className="mb-3" key={field.key}>
              <Form.Label>{field.label}</Form.Label>
              <Form.Control
                type={field.type || "text"}
                value={formData[field.key] || ""}
                onChange={(e) => handleChange(field.key, e.target.value)}
              />
            </Form.Group>
          ))}
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onClose}>
          Cancel
        </Button>
        <Button variant="primary" onClick={handleSubmit}>
          Save Changes
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default EditModal;
