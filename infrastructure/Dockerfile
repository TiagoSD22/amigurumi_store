FROM localstack/localstack:3.0

# Install Terraform and AWS CLI
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    awscli \
    && wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip \
    && unzip terraform_1.6.0_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_1.6.0_linux_amd64.zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy terraform files
COPY terraform/ /terraform/
WORKDIR /terraform

# Copy initialization script
COPY scripts/init-localstack.sh /etc/localstack/init/ready.d/init-localstack.sh
RUN chmod +x /etc/localstack/init/ready.d/init-localstack.sh

# Set environment variables for better S3 compatibility
ENV SERVICES=s3
ENV DEBUG=1
ENV DATA_DIR=/var/lib/localstack
ENV DOCKER_HOST=unix:///var/run/docker.sock
ENV TMPDIR=/var/lib/localstack/tmp
ENV LEGACY_DIRECTORIES=1
ENV S3_SKIP_SIGNATURE_VALIDATION=1
ENV DISABLE_CORS_CHECKS=1
ENV FORCE_NONINTERACTIVE=1
