from app import create_app

# Entry point of the application
# This will initialize Flask and run the development server
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)