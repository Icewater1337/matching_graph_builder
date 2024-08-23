# matching_graph_builder
Library that builds the matching-graphs 
In order to get this to run you need: 
1. a fresh python installation of python 3.9 \
1.1 Download python 3.9.18 from here https://www.python.org/downloads/release/python-3918/ \
1.2  ```   sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev```\
1.3 Inside the downloaded and extracted python folder do  ```./configure``` and afterwards ```sudo make & sudo make install```\
1.4 Create a virtual environment based on the new python ```/path/to/the/python -m venv /path/to/venv```
3. Install numpy using ```pip install numpy```
4. CLone https://github.com/Icewater1337/graph-matching-core  and install using
``` pip install -e . ``` inside the cloned folder (pay attention that the venv is active)
## Usage 
Examples of how to use can be found in the test/builders folder. 
