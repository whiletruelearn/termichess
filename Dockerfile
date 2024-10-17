FROM python:3.10-slim
ENV TERM=xterm-256color COLORTERM=truecolor

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y build-essential libasound2-dev stockfish
RUN pip install --no-cache-dir -r requirements.txt

RUN mv /usr/games/stockfish /usr/local/bin/

RUN pip install -e . 

