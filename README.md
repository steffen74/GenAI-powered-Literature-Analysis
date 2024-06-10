# GenAI-powered Literature Analysis

This project uses AI to analyze literature, providing a GUI for easy interaction. It leverages OpenAI's GPT-4 for generating summaries and includes several other features to assist researchers in efficiently reviewing literature.

For more information, please refer to our [presentation](./2024.01.16%20LLM%20Reviewer.pptx).

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Features

- **Automated Analysis**: Generates summaries, extracts metadata, and analyzes PDF files.
- **GUI**: Easy-to-use graphical interface for interacting with the application.
- **Integration**: Supports integration with Zotero libraries.
- **Detailed Output**: Creates detailed `.docx` files with summaries, keywords, images, and more.

## Setup

1. Clone the repository:

    ```sh
    git clone git@github.com:kaan1derful/GenAI-powered-Literature-Analysis.git
    ```

2. Navigate to the project directory:

    ```sh
    cd GenAI-powered-Literature-Analysis
    ```

3. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```
    Note: If you're using Ubuntu/Debian, you may need to install the tkinter package via your OS package manager:
    
    ```sh
    sudo apt-get install python3-tk
    ```

4. Set up the display for WSL2 (if applicable):
    
    If you are running this application on WSL2 and encounter an error related to the display (e.g., `tkinter.create()... no display name and no $DISPLAY environment variable was found`), follow these steps:

    ### Install VcXsrv

    1. **Download and Install VcXsrv:**
       - Download VcXsrv from [here](https://sourceforge.net/projects/vcxsrv/).
       - Run the installer and follow the installation steps.

    2. **Run VcXsrv:**
       - Launch VcXsrv. You can use the default settings for the initial setup:
         - Select "Multiple windows".
         - Start no client.
         - Extra settings can be left at their defaults.
       - Ensure to check the option "Disable access control" to allow connections from WSL2.

    ### Configure WSL2 to Use VcXsrv

    1. **Set the DISPLAY Environment Variable:**
       - Open your WSL2 terminal.
       - Set the DISPLAY variable to `localhost:0.0`:
       
         ```sh
         export DISPLAY=localhost:0.0
         ```

       - To make this change permanent, add the export command to your `.bashrc` file:

         ```sh
         echo 'export DISPLAY=localhost:0.0' >> ~/.bashrc
         source ~/.bashrc
         ```

5. Run the application:

    ```sh
    python3 -m src.main
    ```
    Note: If you're using PowerShell, replace `python3 -m src.main` with `python3 -m src\main`.

## Usage
After setting up the application, you can use the GUI to analyze literature. For more details on how to use the application, please refer to our presentation.

## Kiosk Mode

The application can be started in kiosk mode. In this mode, the application will start in full screen and the close button will be disabled.

To start the application in kiosk mode, use the `--kiosk` command line argument:

```sh
python3 -m src.main --kiosk
```

## Contributing
Contributions are welcome. Please open an issue to discuss your idea or submit a pull request.

## License
This project is licensed under the terms of the MIT license.
