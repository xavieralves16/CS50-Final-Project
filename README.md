# StreamBox Subscriptions

## Overview
StreamBox Subscriptions is my CS50 final project: a subscription-based e-commerce experience inspired by platforms like Netflix, Amazon Prime, and other monthly membership services. The application lets visitors explore digital plans, add them to a cart, and complete their purchase while administrators manage the catalog and keep track of active subscriptions.

Although modern subscription platforms are usually implemented as Single Page Applications (SPAs) with frontend frameworks, I rebuilt the SPA-style experience using **Flask**, the primary web framework covered in CS50. By combining template partials, JavaScript-driven interactions, and Flask blueprints, the project delivers smooth client-side navigation while staying within the course tooling.

## Technologies Used
- **Python 3.12** with **Flask** for routing, authentication, and page rendering.
- **Flask Blueprints** to organize features into modular components (authentication, products, cart, payments, subscriptions, and dashboard).
- **SQLAlchemy** with **SQLite** for ORM-powered persistence of users, subscription plans, carts, and transactions.
- **Stripe Checkout** integration for secure payment processing during plan purchase.
- **WTForms** and custom validators for handling form submissions (login, registration, product management).
- **Bootstrap 5**, custom SCSS/CSS, and vanilla JavaScript for responsive UI components and SPA-like interactions.
- **Docker** and **pip** requirements for reproducible local setup.

## Features
- Visitor onboarding with user registration, login, and session management.
- Admin dashboard that allows administrators to add, edit, and remove subscription products.
- Product catalog displaying curated streaming-style plans with pricing and benefits.
- Cart workflow that keeps track of selected plans and quantities using server-side sessions.
- Stripe-powered checkout that records successful transactions and activates subscriptions automatically.
- Subscription history pages so users can review active and past services.

## Project Structure
```
CS50-Final-Project/
├── app/
│   ├── __init__.py          # Flask factory, configuration, blueprint registration
│   ├── config.py            # Environment-aware configuration values
│   ├── models.py            # SQLAlchemy models for users, products, payments, subscriptions
│   ├── routes/              # Blueprint modules grouped by feature
│   ├── templates/           # Jinja templates that render the SPA-like views
│   └── static/              # CSS, JS, images, and uploaded media assets
├── requirements.txt         # Python dependencies
├── run.py                   # Flask entrypoint used by `flask run`
└── README.md                # Project documentation (this file)
```

## Getting Started
1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/CS50-Final-Project.git
   cd CS50-Final-Project
   ```
2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**
   - Copy `.env.example` to `.env` (or create a new `.env`).
   - Provide values for `SECRET_KEY`, `STRIPE_PUBLIC_KEY`, and `STRIPE_SECRET_KEY`.

5. **Initialize the database**
   - Start the Flask shell to create the SQLite database automatically:
     ```bash
     flask --app run.py shell
     ```
   - Exit the shell once the application context loads; the factory creates tables and seeds an admin user.

6. **Run the development server**
   ```bash
   flask --app run.py --debug run
   ```
   Visit `http://127.0.0.1:5000/` to explore the storefront. Use `admin@example.com` / `1234` to sign in as the default administrator.

## Demo Video
_A walkthrough video demonstrating the project workflow will be linked here._

**Video link:** <PLACEHOLDER_FOR_VIDEO_URL>

## Acknowledgements
- Harvard CS50 for the guidance, lectures, and starter materials that inspired this capstone.
- The Flask and Stripe documentation communities for comprehensive resources.

Enjoy exploring StreamBox Subscriptions! Feel free to open issues or reach out with suggestions.