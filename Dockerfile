FROM continuumio/miniconda3


FROM continuumio/miniconda3
ADD . boulder-stats
WORKDIR boulder-stats
RUN conda env create -f environment.yml
# Pull the environment name out of the environment.yml
RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH
RUN pip install .

ENTRYPOINT [ "boulder_stats" ]
