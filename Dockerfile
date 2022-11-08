FROM python

COPY . /app
WORKDIR /app
RUN python -m pip install -r requirements.txt

CMD ["python", "bot_main.py"]
