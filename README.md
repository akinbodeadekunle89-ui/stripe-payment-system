# FastAPI & Stripe Payment Engine

A robust, production-ready backend payment service built with FastAPI, SQLModel, and Stripe Checkout, designed to handle secure checkout sessions and asynchronous event webhooks.

## ✨ Features

* **Secure Stripe Checkout Integration:** Instantly generate secure Stripe Checkout sessions for seamless payment flows.
* **Verified Webhook Listener:** Implements cryptographic HMAC SHA-256 signature verification to securely process asynchronous payment events from Stripe.
* **Relational Database Management:** Persistent state management and data modeling powered by SQLModel and SQLite/PostgreSQL.
* **Automated Testing Suite:** Comprehensive unit and integration testing built using `pytest` and FastAPI's `TestClient`.
* **Enterprise Automation Ready:** Architected to integrate cleanly with workflow platforms like Workato for automated business logic.

## 🏗️ Tech Stack

* **Framework:** FastAPI
* **Database & ORM:** SQLModel / SQLite / PostgreSQL
* **Payment Gateway:** Stripe API & Stripe Checkout
* **Validation & Settings:** Pydantic & pydantic-settings
* **Testing:** Pytest & HTTPX

## 🚀 Getting Started

### Prerequisites

* Python 3.10+ installed locally

### Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/akinbodeadekunle89-ui/stripe-payment-system.git](https://github.com/akinbodeadekunle89-ui/stripe-payment-system.git)
   cd stripe-payment-system
