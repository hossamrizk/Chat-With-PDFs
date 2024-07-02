# Chatbot Application

Welcome to the Chatbot Application! This platform allows you to upload your PDFs and start a conversation with the chatbot about the content. The chatbot is designed to help you extract insights, answer questions, and provide a deeper understanding of your documents.

## Features

- Upload multiple PDFs.
- Ask questions about the content of your PDFs.
- Receive accurate and context-aware responses.
- Easy-to-use interface for seamless interaction.

## Installation

1. Clone the repository:
    ```sh
    https://github.com/hossamrizk/Chat-With-PDFs.git
    cd Chat-With-PDFs
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501` to interact with the application.

## Project Structure

- `app.py`: Main application file.
- `handle_text.py`: Contains the `PDFProcess` class for processing PDFs.
- `chatbot.py`: Contains functions to create conversation chains for Hugging Face and OpenAI models.
- `web_pages`: Contains application pages.
- `vectorestore`: Contains Embedding and Faiss files incase you will run application local.
- `Embeddings`: Contains Notebook for processing embeddings for the pdf on colab.
- `requirements.txt`: List of required Python packages.

## Example Usage

1. **Home Page**: 
   - The home page provides a brief introduction and lists the features of the application.

2. **Upload PDFs**:
   - Navigate to the chat page.
   - Upload one or more PDF files using the file uploader.

3. **Interact with the Chatbot**:
   - After uploading, the application processes the PDFs.
   - Ask questions about the content of your PDFs in the provided text input field.
   - The chatbot will respond with accurate and context-aware answers.

## Contact

If you have any questions or need further assistance, feel free to reach out:

**Hossam Eldein Rizk**
- **Email**: hossamrizk048@gmail.com
- **LinkedIn**: [Hossam Eldein Rizk](https://www.linkedin.com/in/hossamrizk10/)
- **GitHub**: [Hossam Rizk](https://github.com/hossamrizk)
- **Kaggle**: [Hossam Rizk](https://www.kaggle.com/hossamrizk)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

