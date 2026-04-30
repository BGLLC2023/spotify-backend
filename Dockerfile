
# python image with version 3.10
FROM python:3.10

WORKDIR /app
# requirement to be installed
COPY requirements.txt /app/requirements.txt

# installing the requirements
RUN pip install -r /app/requirements.txt

# copying the files to the container
COPY . .

# running the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]