FROM python:3.9-buster

# Install nginx, gunicorn, vim, and other required dependencies
RUN apt-get update && \
    apt-get install -y nginx netcat gunicorn vim --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Copy Nginx config file
COPY nginx.default /etc/nginx/sites-available/default

# Redirect Nginx logs to stdout/stderr
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Create necessary directories and copy source code
RUN mkdir -p /opt/app/pip_cache /opt/app/techblog

COPY requirements.txt /opt/app/
COPY start-server.sh /opt/app/
RUN chmod +x /opt/app/start-server.sh
COPY techblog /opt/app/techblog/

# Set working directory
WORKDIR /opt/app

# Install Python dependencies

RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache

# Adjust user permissions and file ownership
RUN usermod -u 10001 www-data && \
    chown -R www-data:www-data /opt/app /var/lib/nginx && \
    chmod -R 775 /var/lib/nginx

# Create Nginx PID file and set permissions
RUN touch /run/nginx.pid && \
    chown www-data:www-data /run/nginx.pid && \
    chmod 644 /run/nginx.pid

# Set user for the container
USER 10001

# Expose necessary port
EXPOSE 8020

# Set the stop signal for graceful shutdown
STOPSIGNAL SIGTERM

# Start the server with the provided script
CMD ["/opt/app/start-server.sh"]
