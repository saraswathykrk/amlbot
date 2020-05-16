# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:1.10.0

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
# COPY actions/requirements-actions.txt ./


# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
# RUN pip install -r requirements-actions.txt


# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip3 install bs4
RUN pip3 install nltk
RUN pip3 install tensorflow_text

RUN python3 -m nltk.downloader punkt -d /usr/share/nltk_data
#RUN python3 -c "import nltk; nltk.download('punkt')"


# Copy actions folder to working directory
#COPY ./nltk_data /opt/venv/nltk_data

# By best practices, don't run the code with root user
USER 1001

