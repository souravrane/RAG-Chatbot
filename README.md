# RAG Chatbot Application

A powerful Retrieval-Augmented Generation (RAG) chatbot that answers questions based on your documents using OpenAI embeddings and comprehensive logging capabilities.

## 📁 Project Structure

## Features

- **AI-Powered Q&A**: Get intelligent answers from your documents
- **OpenAI Integration**: Uses state-of-the-art OpenAI embeddings and language models
- **Comprehensive Logging**: Detailed logging with multiple log files for monitoring
- **Colored Terminal Output**: Beautiful, color-coded responses and status messages
- **Similarity Scoring**: Intelligent document retrieval with relevance scores
- **Source Attribution**: Always shows which documents were used for answers
- **Error Handling**: Robust error handling with detailed error messages
- **Multiple Document Formats**: Supports PDF, Markdown, and other formats

## 📁 Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **OpenAI API key** (for embeddings and language model)

### Step 1: Clone or Download the Project

```bash
# If using git:
git clone <your-repository-url>
cd RAG-Chatbot

# Or download and extract the ZIP file to your desired location
```

### Step 2: Create Virtual Environment

```bash
# Create a virtual environment
python -m venv rag_env

# Activate the virtual environment
# On Windows:
rag_env\Scripts\activate

# On macOS/Linux:
source rag_env/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Note**: This will install all dependencies including:
- `langchain` and related packages for RAG functionality
- `openai` for API integration
- `chromadb` for vector database
- `loguru` for advanced logging
- `colorama` for colored terminal output
- `sentence-transformers` for local embeddings
- And many other supporting packages

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# On Windows:
echo OPENAI_API_KEY=your_api_key_here > .env

# On macOS/Linux:
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

**Or manually create `.env` file with:**
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 5: Verify Installation

```bash
# Test logging functionality
python test_logging.py
```

You should see colored log output indicating successful setup.

## 📚 Usage

### 1. Creating a Vector Database

First, you need to create a vector database from your documents:

```bash
# Create database from sample data
python openai_create_database.py
```

This will:
- Load documents from `./sample_data/`
- Split them into chunks
- Create embeddings using OpenAI
- Store them in `./chroma_db_openai/`

**Expected Output:**
```
2025-06-29 18:XX:XX | INFO | === Starting OpenAI RAG Chatbot Database Creation ===
2025-06-29 18:XX:XX | INFO | Loading documents from directory: ./sample_data/aws_lambda
2025-06-29 18:XX:XX | INFO | Starting document chunking process
2025-06-29 18:XX:XX | INFO | Starting Chroma database creation
2025-06-29 18:XX:XX | INFO | Saved X chunks to ./chroma_db_openai.
2025-06-29 18:XX:XX | INFO | === Database Creation Completed Successfully ===
```

### 2. Querying the Database

Now you can ask questions about your documents:

```bash
# Ask a question
python openai_query_data.py "What is AWS Lambda?"
```

**Example Queries for AWS Lambda:**
```bash
python openai_query_data.py "How do I create my first Lambda function?"
python openai_query_data.py "What are the benefits of serverless computing?"
python openai_query_data.py "How does Lambda handle concurrent executions?"
python openai_query_data.py "What security best practices should I follow?"
```

**Example Queries for Alice in Wonderland:**
```bash
python openai_query_data.py "What is Alice's adventure about?"
python openai_query_data.py "Who is the White Rabbit?"
python openai_query_data.py "What happens when Alice drinks the potion?"
```

### 3. Understanding the Output

The application provides rich, colored output:

```
Search Results:
  1. Score: 0.856 - AWS Lambda is a serverless compute service that runs your code...
  2. Score: 0.743 - Lambda functions are event-driven and automatically scale...
  3. Score: 0.689 - You can use Lambda to run code without provisioning servers...

================================================================================
🤖 AI RESPONSE 
================================================================================
AWS Lambda is a serverless compute service that allows you to run code without 
provisioning or managing servers. It automatically scales your applications and 
you only pay for the compute time you consume.

--------------------------------------------------------------------------------
📚 Sources:
  1. sample_data/aws_lambda/lambda-dg.pdf
  2. sample_data/aws_lambda/lambda-dg.pdf
================================================================================
```

## ⚙️ Configuration

### Logging Configuration

The application uses a sophisticated logging system with multiple log files:

- **`logs/app.log`**: General application logs
- **`logs/requests.log`**: Request tracking
- **`logs/responses.log`**: Response tracking
- **`logs/payloads.log`**: Detailed payload information
- **`logs/errors.log`**: Error tracking

### Database Configuration

- **Database Path**: `./chroma_db_openai/`
- **Sample Data**: `./sample_data/`

### Customizing Document Sources

To use your own documents:

1. **Add your documents** to the `sample_data/` directory
2. **Update the DATA_PATH** in `openai_create_database.py`:
   ```python
   DATA_PATH = "./sample_data/your_documents"
   ```
3. **Run the database creation** script again:
   ```bash
   python openai_create_database.py
   ```

## 🐛 Troubleshooting

### Common Issues

#### 1. OpenAI API Key Error
```
Error: No API key found. Please set OPENAI_API_KEY environment variable.
```
**Solution**: 
- Add your OpenAI API key to the `.env` file
- Make sure the `.env` file is in the project root directory

#### 2. Database Not Found
```
Error: Database directory not found
```
**Solution**: 
- Run the database creation script first: `python openai_create_database.py`
- Check if `chroma_db_openai/` directory exists

#### 3. Low Similarity Scores
```
Warning: Best match has low similarity score: 0.45
```
**Solutions**: 
- Try rephrasing your question
- Add more relevant documents to the database
- Lower the similarity threshold in the code (currently 0.7)

#### 4. Missing Dependencies
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: 
- Install dependencies: `pip install -r requirements.txt`
- Make sure your virtual environment is activated

#### 5. Permission Errors
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: 
- Run as administrator (Windows)
- Check file permissions
- Make sure you have write access to the project directory

### Debug Mode

Enable debug logging by modifying `logger_config.py`:

```python
# Change log level to DEBUG
logger.add(sys.stdout, level="DEBUG")
```

## 🔒 Security Considerations

- **API Keys**: Never commit your `.env` file to version control
- **Log Files**: Review log files for sensitive information
- **Network**: Ensure secure connections when using OpenAI API
- **Documents**: Be careful with sensitive documents in your database

## 📈 Performance Optimization

### For Large Document Collections

1. **Increase chunk size** for better context
2. **Adjust overlap** for better document coverage
3. **Use batch processing** for large files
4. **Monitor memory usage** during database creation

### For Faster Queries

1. **Reduce k value** in similarity search (currently 3)
2. **Optimize prompt length**
3. **Cache frequently asked questions**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📈 Acknowledgments

- **LangChain** for the RAG framework
- **OpenAI** for the embedding and language models
- **Chroma** for the vector database
- **Loguru** for advanced logging capabilities

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the log files in the `logs/` directory
3. Create an issue in the repository
4. Contact the development team

---

**Happy Querying! 🚀**
