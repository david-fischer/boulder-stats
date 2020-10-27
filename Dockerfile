FROM continuumio/miniconda3
ADD . boulder-stats
WORKDIR boulder-stats
# Pull the environment name out of the environment.yml
# RUN echo "source activate $(head -1 environment.yml | cut -d' ' -f2)" > ~/.bashrc
# ENV PATH /opt/conda/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH
RUN conda init bash
RUN conda install python pandas pytables pylint
RUN pip install .

ENTRYPOINT [ "boulder_stats" ]
