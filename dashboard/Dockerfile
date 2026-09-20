FROM python:3.12-slim

WORKDIR /usr/src/app

# Instala as dependências separadamente para aproveitar o cache do Docker
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

#ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

ENTRYPOINT ["streamlit", "run", "dashboard.py"]
# CMD [ "python", "./your-daemon-or-script.py" ]
