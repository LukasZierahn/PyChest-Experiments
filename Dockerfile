FROM r-base:4.0.3
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends build-essential python3 python3-pip python3-setuptools python3-dev
RUN pip3 install --upgrade pip

ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app

ADD *.r .
ADD *.py .
ADD *.txt .
COPY Distributions ./Distributions
COPY Algorithms ./Algorithms

RUN pip3 install Cython

# installing python libraries
RUN pip3 install -r requirements.txt

RUN python3 prepare_tests.py 60000 60000 60000 200 1

RUN Rscript enable_r_connection.r

CMD Rscript enable_r_connection.r && python3 run_algorithms.py && python3 create_tables.py