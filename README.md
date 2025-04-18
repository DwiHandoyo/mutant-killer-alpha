To run the Flask app:

1.  Ensure you have Python and pip installed.
2.  Install the required Python packages:

    ```bash
    pip install Flask gitpython
    ```
3.  Run the app:

    ```bash
    python app.py
    ```

The app will start on `http://127.0.0.1:9002`. You can send POST requests to the `/analyze` endpoint with a JSON payload containing the `git_url`.
