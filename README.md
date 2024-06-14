# RepoTree

RepoTree is a Python script that generates and displays the directory structure of any GitHub repository in a tree view format.

## Features

- **Fetch Repository Structure**: Retrieves the directory and file structure of a GitHub repository using the GitHub API.
- **Tree View Format**: Displays the repository structure in an easy-to-read tree view format.
- **Rate Limiting Handling**: Automatically handles rate limiting and retries requests.
- **Error Handling**: Provides error handling for invalid repository names and unexpected response formats.

## Requirements

- Python 3.7 or higher
- `requests` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Cantue35/RepoTree.git
    cd RepoTree
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
```

#### Example:
```
Enter the GitHub repository URL or author/repo: Cantue35/RepoTree
```

The script will display the directory structure in a tree view format.

```
RepoTree/
├── LICENSE
├── README.md
├── repo_tree.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
