FROM   3.13.18-alpine3.24
WORKDIR /app
COPY  . .
EXPOSE 8000
CMD ["python3" , "app.py"]
