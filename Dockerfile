# Use the official Python base image
FROM python:3.11

# Set the working directory of the container
WORKDIR /app

# Copy the requirements file containing your dependencies list into the container
COPY . .

# Install necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code of the app (there is only one file), can copy all current dir using `.`
COPY app.py .

# Expose port 5000, the default port used by flask
EXPOSE 8050
# Start the Dash app
CMD ["python", "app.py"]
