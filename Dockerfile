FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

COPY . /app
# Set the working directory
WORKDIR /app

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["/bin/bash", "-c", "uv venv && source .venv/bin/activate && uv pip install -r requirements.txt && streamlit run app.py"]