FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    texlive-full \
    python3 \
    python3-pip \
    && apt-get clean

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir latexgenlib
RUN python3 main.py
RUN pdflatex -interaction=nonstopmode -output-directory=artifacts artifacts/generated_document.tex

CMD ["/bin/bash"]
