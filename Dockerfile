FROM ubuntu:22.04

# Install system dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get -y update 
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -y install build-essential g++ gfortran mpich gcc python3-dev python3-pip python3-venv virtualenv wget zlib1g-dev vim htop libnetcdf-dev libnetcdff-dev bzip2 cmake cpio curl git gosu libblas-dev liblapack-dev libmpich-dev 
RUN apt-get -y install default-jre

# Create working directory and copy files
RUN mkdir -p /TuvaluForecast
COPY ./ /TuvaluForecast/
WORKDIR /TuvaluForecast/codes

# Create Python venv and install dependencies
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/python -m ensurepip --upgrade && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r /TuvaluForecast/requirements_working.txt

# Make executables executable and add to PATH
RUN chmod +x /TuvaluForecast/executables/* || true
ENV PATH="/TuvaluForecast/executables:/opt/venv/bin:$PATH"

CMD ["python", "main_run_operational.py"]
