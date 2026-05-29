# CodeAlpha MoveAutomation

**CodeAlpha MoveAutomation** is an interactive terminal-based Python application that automates and safely orchestrates moving files between directories. With built-in file scanning, extension-based filtering, input validation, and robust error handling, it helps streamline manual tasks commonly encountered during data reorganization or migrations.

---

## Features

- **Interactive Terminal UI:** Guided menus and input validation for a user-friendly experience.
- **File Scanning:** Lazily scan for files in chosen source directories.
- **Extension-Based Filtering:** Filter files by type (e.g., only JPGs) before moving.
- **Safe File Movement:** Handles conflicts, permissions, and preserves existing files with timestamped backups.
- **Structured Error Reporting:** Semantic error/status messages for all file operations.
- **Configurable & Extensible:** Modular design enables easy additions and custom integrations.

---

## Getting Started

### Prerequisites

- Python 3.11 or above

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/aa8796-tech/CodeAlpha_MoveAutomation.git
   cd CodeAlpha_MoveAutomation
   ```
---

## Usage

Run the main entry point:

```bash
python main.py
```

**Main Menu Options:**
1. **Start Automation Process:**  
   - Specify the source directory containing files to be moved.
   - Specify the destination directory.
   - The app filters for `.jpg` files (default) and moves them, handling name conflicts and permissions.
2. **Read Operational Guidelines:**  
   - View quick instructions and rules for safe operation.
3. **Exit Application Instance:**  
   - Quits the app.

### Example Workflow

- You’ll be prompted for absolute or relative source and destination paths.
- The program will validate paths, perform the move operation, and report detailed status for each file.
- Name conflicts are resolved by timestamped renaming instead of overwriting.

---

## Project Structure

```
.
├── main.py             # Main application entry and control flow
├── files_scanner.py    # Iteration utilities for scanning files in directories
├── filter.py           # Classes for file extension-based filtering
├── move_operation.py   # Utilities for safe file movement with status reporting
├── ui.py               # Terminal UI components and menu rendering
├── utility.py          # Terminal utilities (clearing, pausing, sizing)
├── validation.py       # Input and path validation logic
└── README.md           # Project documentation
```
# Developments in the near future
* Filters: Adding other types of filters as well as merge multiple filters without breaking any old code. 
* Validation: Adding additional validators without breaking any old code, and this is due to the existence of the validation logic away from the way it is implemented. 
* Control flow: Development and separation of responsibilities from the main.py later Without touching any other file .
* UI: Develop and improve the interface by adding file display systems and improving interaction methods.
---

## Customization

- **File Types:**  
  To scan for/filter different file types, modify the `ExtensionFileFilter(["jpg"])` line in `main.py` to any desired list of extensions, e.g., `["png", "txt"]`.

- **Validation:**  
  All path and input validation logic is centralized in `validation.py`, making it easy to add or alter validation rules.

---

## Contributing

Contributions are welcome! If you would like to add new features or improve existing logic, please open an issue or submit a pull request.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes
4. Push to your branch
5. Open a PR

---

## License

Distributed under the MIT License.

---

## Contact

For questions, ideas, or support, please [open an issue](https://github.com/aa8796-tech/CodeAlpha_MoveAutomation/issues) or reach out via GitHub.
 
