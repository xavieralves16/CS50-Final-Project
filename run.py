"""Convenience entry point for running the Flask development server."""

from app import create_app

# Create the Flask application instance using the factory defined in ``app``.
app = create_app()

if __name__ == "__main__":
    # Enable the debugger so local developers can iterate quickly.
    app.run(debug=True)