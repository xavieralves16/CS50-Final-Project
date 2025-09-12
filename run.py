import os
from app import create_app
from dotenv import load_dotenv

# Caminho absoluto do ficheiro .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
print("DEBUG - A carregar .env de:", env_path)

# Força o carregamento do ficheiro .env
load_dotenv(dotenv_path=env_path)

# Confirmar se carregou
print("DEBUG - STRIPE_PUBLIC_KEY =", os.environ.get("STRIPE_PUBLIC_KEY"))
# Entry point of the application
# This will initialize Flask and run the development server
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)