# Use the official Python 3.12 image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install Git and update package list
RUN apt-get update && \
    apt-get install -y git

# Clone the repository
RUN git clone https://github.com/rafaelcoelho1409/COELHOLibraryStreamlit .

# Install uv and create a virtual environment
RUN pip install uv && \
    uv venv

# Install dependencies using uv
RUN . .venv/bin/activate && \
    uv pip install -r requirements.txt

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD [".venv/bin/streamlit", "run", "app.py"]