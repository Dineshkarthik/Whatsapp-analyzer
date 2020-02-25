FROM python:3.6.8-slim

LABEL maintainer="Dineshkarthik Raveendran <dineshkarthik.r@gmail.com>"

# App setup
COPY . /whatsapp-analyser
WORKDIR /whatsapp-analyser
RUN make install

EXPOSE 5000

CMD ["wapp-analyzer", "run"]