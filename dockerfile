# Use the PyTorch image as the base image
FROM pytorch/pytorch:2.4.1-cuda11.8-cudnn9-runtime

# Set the working directory in the container
WORKDIR /ResidualScheduling_IEEE_access

# Copy your local project directory (optional if you have files to add)
COPY . /ResidualScheduling_IEEE_access

# Install necessary packages
RUN pip install --upgrade pip \
                torch-geometric==2.3.1 \
                opencv-python \
                plotly \
                matplotlib \
                gym \
                tensorboard \
                pandas \
                colorhash

# Set the entry point to start the container in interactive mode
CMD ["bash"]
