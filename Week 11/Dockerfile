FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir pytest
CMD ["python", "inventory_manager.py"]