import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";

import "../style/style.css";

export default function Navigation() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const offset = window.scrollY;
      if (offset > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener("scroll", handleScroll);

    // Cleanup on unmount
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav
      id="nav1"
      className={`navbar navbar-expand-lg fixed-top navbar-scroll px-3 mb-3 ${
        scrolled ? "navbar-scrolled" : ""
      }`}
    >
      <NavLink className="navbar-brand" to="/">
        CMS
      </NavLink>

      <button
        className="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span className="navbar-toggler-icon" />
      </button>

      <div className="collapse navbar-collapse" id="navbarNav">
        <ul className="nav nav-pills">
          {/* <li className="nav-item">
            <a className="nav-link" href="#About">
              About
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#Education">
              Education
            </a>
          </li>
           */}
        <li className="nav-item">
            <NavLink
              to="/"
              className={({ isActive }) =>
                "nav-link" + (isActive ? " active" : "")
              }
            >
              Home
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink
              to="/products"
              className={({ isActive }) =>
                "nav-link" + (isActive ? " active" : "")
              }
            >
              Products
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink
              to="/customers"
              className={({ isActive }) =>
                "nav-link" + (isActive ? " active" : "")
              }
            >
              Customers
            </NavLink>
          </li>
            <li className="nav-item">
                <NavLink
                to="/sales"
                className={({ isActive }) =>
                    "nav-link" + (isActive ? " active" : "")
                }
                >
                Sales
                </NavLink>
            </li>
        </ul>
      </div>

      {/* <ul className="nav me-1">
        <li className="nav-item">
          <a
            className="nav-link rounded-pill text-bg-danger"
            href="!#"
            target="_blank"
            rel="noreferrer"
          >
            ...
          </a>
        </li>
      </ul> */}
    </nav>
  );
}
