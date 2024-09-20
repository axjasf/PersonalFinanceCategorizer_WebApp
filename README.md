# Personal Finance Tracker

A Streamlit-based web application for tracking personal finances. This app allows users to view, add, and analyze their financial transactions using data stored in a Google Sheet.

## Features

- View existing transactions
- Add new transactions
- Basic financial analytics
- Integration with Google Sheets for data storage

## Current Status

**[In Development]**

The application is currently in its initial development phase. Basic functionality for viewing and adding transactions is implemented. The app successfully connects to a Google Sheet for data storage and retrieval.

Next steps:
- Implement data filtering and sorting capabilities
- Enhance the analytics dashboard
- Improve the user interface
- Add data visualization features

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/personal-finance-tracker.git
   cd personal-finance-tracker
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up Google Sheets API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Sheets API
   - Create credentials (OAuth client ID) for a desktop application
   - Download the credentials and save them as `credentials.json` in the project root

5. Update the `SPREADSHEET_ID` in `data/data_loader.py` with your Google Sheet ID.

6. Run the Streamlit app:
   ```
   streamlit run personalfinance/app.py
   ```

## Usage

After starting the app, you can:
- View your existing transactions
- Add new transactions using the provided form
- See basic financial analytics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Development Setup

1. Install development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

2. Set up pre-commit hooks:
   ```
   pre-commit install
   ```

3. Code Formatting and Linting:
   This project uses Black for code formatting and Flake8 for linting. They are configured to run automatically as pre-commit hooks. However, you can also run them manually:

   ```
   black .
   flake8
   ```

   Black will automatically format your code, while Flake8 will check for style and potential errors.

4. Before committing changes:
   The pre-commit hooks will automatically run Black and Flake8 when you attempt to commit. If there are any issues, the commit will be aborted, allowing you to fix the problems before trying again.

   Note: If Black makes any changes, you'll need to stage those changes and attempt the commit again.

5. Continuous Integration:
   The project is set up with GitHub Actions to run Black and Flake8 on every push and pull request to ensure code quality and consistency.
