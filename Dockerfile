FROM ubuntu:latest
FROM python:latest

# Copy the tool over, organized as a Python package to facilitate local installation/execution
# Different step so we can keep modifying requirements without reinstalling pip every time
COPY ugc/ /root/ugc/
COPY setup.cfg setup.py /root/

# Install the automation tool as a local package
RUN pip3 install -e /root

ENTRYPOINT ["ugc"]
CMD ["--help"]
