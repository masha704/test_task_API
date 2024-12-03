   FROM python:3.9

   WORKDIR /app

   COPY requirements.txt .
   RUN python -m venv /venv
   ENV PATH="/venv/bin:$PATH"


   RUN pip install --no-cache-dir --upgrade pip
   RUN pip install --no-cache-dir -r requirements.txt

   COPY app/ .

   CMD ["python", "load_bd.py"]   

   CMD ["python", "app.py"]

