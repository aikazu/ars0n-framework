FROM kalilinux/kali-rolling

# Set non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Update package list and install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv git wget curl nmap

# Install required tools for toolkit (based on install.py)
# Note: This may need to be expanded based on the actual requirements of the toolkit
RUN apt-get install -y \
    libpcap-dev \
    jq \
    npm \
    golang-go \
    amass \
    whatweb \
    dnsutils \
    whois \
    iputils-ping

# Set up Python virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create directory for temporary files and logs
RUN mkdir -p /app/toolkit/temp /app/logs

# Copy requirements first to utilize Docker caching
COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy the toolkit code
COPY . .

# Set entry point to the toolkit service
CMD ["python3", "toolkit-service.py"] 