# RepoMap
A Python script to generate and display the directory structure of any GitHub repository in a tree view format.

## Features

- Fetches repository structure using the GitHub API
- Displays the directory and file structure in a tree view format
- Handles rate limiting and retries requests automatically
- Provides error handling for common issues

## Requirements

- Python 3.7 or higher
- `requests` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/GitTreeVisualizer.git
    cd GitTreeVisualizer
    ```

2. (Optional) Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install requests
    ```

## Usage

Run the script and input the GitHub repository URL or `author/repo` format when prompted:

```sh
python repo_tree.py