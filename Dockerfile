FROM continuumio/miniconda3:4.9.2


# Make RUN commands use `bash --login` (always source ~/.bashrc on each RUN)
SHELL ["/bin/bash", "--login", "-c"]

# install apt dependencies and update conda
RUN apt-get  --allow-releaseinfo-change  update && apt-get install git -y \
    && apt-get install -y apt-transport-https ca-certificates wget unzip bzip2 libfontconfig1 \
    && update-ca-certificates \
    && apt-get -qq -y remove curl \
    && apt-get install -y g++ gcc \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log 

# Set up conda environment
ENV PATH /opt/conda/bin:$PATH
RUN conda config --set ssl_verify no
COPY ./environment.yml /opt/environment.yml
RUN conda env create -f /opt/environment.yml

SHELL ["conda", "run", "-n", "AGAVE", "/bin/bash", "-c"]



# COPY ./controllers/proteins /opt/proteins
# COPY ./controllers/mappings /opt/mappings
# COPY ./controllers/src /opt/app/controllers
# COPY ./src /opt/app/src
# COPY ./*json /opt/app/
# COPY ./*.js /opt/app/vue.config.js




WORKDIR /opt/app
RUN git clone https://github.com/jhuapl-bio/AGAVE.git
WORKDIR /opt/app/AGAVE
RUN npm install 
RUN npm build

#To copy data into the appropriate location, run: cp output.json /opt/app/AGAVE/dist/data/default.json



