# henrik-svendeopgave

## CoinControl

CoinControl is a Django-based web application for managing financial transactions and accounts.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher
- pip (Python package installer)
- Node.js and npm (for Tailwind CSS)

### Installation

Follow these steps to set up the project:

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Aarhus-tech-project/henrik-svendeopgave.git
    cd henrik-svendeopgave
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m virtualenv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required Python packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Update your NPM_BIN_PATH:**

    - Go to 'CoinControl\CoinControl\settings.py'
    - Replace NPM_BIN_PATH with:

    ```py
    NPM_BIN_PATH = r'your NPM_BIN_PATH'
    ```

5. **Set up the database:**

    - Go to 'CoinControl\CoinControl\settings.py'
    - Delete `tmpPostgres`
    - Replace `DATABASES` with:

    ```py
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ```

6. **Set up the `.env`:**

    - Generate a encryption key:

    ```sh
    python generate_key.py
    ```

    - Create a `.env` file in the project root directory and add your database credentials:

    ```env
    FIELD_ENCRYPTION_KEY=your_field_encryption_key
    ```

7. **Apply database migrations:**

    ```sh
    cd coincontrol
    python manage.py migrate
    ```

8. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

9. **Install Tailwind CSS:**

    ```sh
    python manage.py tailwind install
    ```

10. **Start Tailwind CSS:**

    ```sh
    python manage.py tailwind start
    ```

11. **Run the development server:**

    - Open A new terminal and run:

    ```sh
    cd henrik-svendeopgave
    venv/bin/activate
    cd coincontrol
    python manage.py runserver
    ```

12. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000`.

## Usage

- Log in with the superuser credentials you created.
- Add, update, and delete transactions and accounts.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
