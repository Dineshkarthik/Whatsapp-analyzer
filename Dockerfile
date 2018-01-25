FROM python:2-onbuild

LABEL maintainer="Dineshkarthik Raveendran <dineshkarthik.r@gmail.com>"

# Cloning repo and installing requirements
RUN git clone https://github.com/Dineshkarthik/Whatsapp-analyzer.git WhatsApp-Analyzer && \
	cd WhatsApp-Analyzer && \
	pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "./analyzer.py"]