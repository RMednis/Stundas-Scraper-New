FROM python:3.7-alpine3.10

# Install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip&& \
    pip install --no-cache-dir -r requirements.txt

# Install firefox
RUN apk add firefox-esr

# Install geckodriver
# GlibC Compatability Layer for Alpine
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk
RUN apk add glibc-2.30-r0.apk
RUN apk add glibc-bin-2.30-r0.apk

# Downloading and Installing geckodriver itself
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
RUN	tar -zxf geckodriver-v0.26.0-linux64.tar.gz && \
    cp geckodriver /usr/local/bin/
RUN chmod +x usr/local/bin/geckodriver

# Copy over all other files
COPY . .

# Execute on launch
CMD ["python3", "Main.py"]
