# Pizza_Delivery_WebApp

Pizza_Delivery_WebApp is a Django-based web application for ordering pizzas online. It includes features such as user registration, login, password reset, cart management, and integration with Stripe for payments.

## Features

- User registration and login
- Password reset functionality
- Add pizzas to cart
- View and manage cart items
- Checkout and payment using Stripe
- Responsive design

## Requirements

- Python 3.8+
- Django 5.0
- Stripe API keys
- Sendinblue API key for email functionality

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://https://github.com/OlaitanSalam/LastPizzaApp.git
    cd LastPizzaApp
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following:

    ```env
    SECRET_KEY=your_secret_key
    STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
    STRIPE_SECRET_KEY=your_stripe_secret_key
    SENDINBLUE_API_KEY=your_sendinblue_api_key
    ```

5. **Apply migrations:**

    ```sh
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

8. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000/`.

## Configuration

### Email Configuration

Ensure your email backend is configured in `settings.py`:

```python
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
DEFAULT_FROM_EMAIL = "Pizza Support <support@PizzaGarden.com>"
ANYMAIL = {
    "SENDINBLUE_API_KEY": config("SENDINBLUE_API_KEY"),
}

STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")

## PROJECT STRUCTURE

lastpizza/
├── lastpizza/
│   ├── __init__.py
│   ├── [settings.py](http://_vscodecontentref_/0)
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── pizzadelivery/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   │   └── pizzadelivery/
│   │   |    ├── base.html
|   |   |    ├── billing.html
|   |   |    ├── cart_items.html
|   |   |    ├── chechout.html
│   │   |    ├── home.html
│   │   |    ├── register.html
|   |   |    ├── order_failure.html
|   |   |    ├── order_success.html
|   |   |    ├── profile.html
│   │   |    ├── login.html
│   │   ├── passwordreset/
│   │        ├── password_reset.html
│   │        ├── password_reset_done.html
│   │        ├── password_reset_confirm.html
│   │        ├── password_reset_complete.html
│   ├── static/
│   │   ├── css/
│   │   │   
│   │   ├── js/
│   │   │   └── cart.js
│   │   └── images/
│   │       └── pizza_logo.png
├── manage.py
└── [requirements.txt](http://_vscodecontentref_/1)
└── README.md
└──venv
