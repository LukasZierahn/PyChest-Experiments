# PyChest Experiments
This repository was used to produce the results presented in the paper "PyChEst: A software package for the retrospective estimation of distributional changes in  piece-wise stationary time series". The results used in Table 1 of the paper can be found in the error_log.csv and errors.csv.  
To recreate the other figures of the paper, please refer to the Graphics folder.

## Docker
The results can be replicated easily if [Docker](https://www.docker.com/) is installed by running
> `docker build -t pychest_experiments .`  
> `docker run -it --name pychest_experiments pychest_experiments `

Keep in mind that the experiments might take multiple hours or even days and might require up to 16 GB of memory. After the code returns, the docker container now contains the full results, which can be retrieved with: 
> `docker cp pychest_experiments:/app/error_log.csv .`  
> `docker cp pychest_experiments:/app/errors.csv .`

## Manual
However the experiments can also be run manually. First [Python 3](https://www.python.org/downloads/) needs to be installed, then one can install the depencies needed to execute the code by running:  
> `pip install Cython && pip install -r requirements.txt`

\
Now `prepare_tests.py` can be used to setup a series of sequences that are then later being run by the changepoint detection algorithms. It then needs to be supplied a couple of commandline arguments in this order: `Start Length`, `End Length`, `Step Size`, `Iteration Count`, `Seed`.  
To recreate the exact sequences used in the experiments in the paper one ought to run:  
> `python prepare_tests.py 60000 60000 60000 200 1`

Note here that the all previous sequences as well as the `error_log.csv` will be overwritten, all data that will be run can be found in the sequences folder now.\
\
\
Since the implementation of WBS is being called from [R](https://www.r-project.org/), we first need to start the corresponding [R](https://www.r-project.org/)-Deamon and ensure that the CRAN package [wbs](https://CRAN.R-project.org/package=wbs) is installed. This requires [R](https://www.r-project.org/) to be installed on the system before running:  
> `Rscript enable_r_connection.r`

The script will install the missing libraries if it needs to.  
\
Next the changepoint detection algorithms will be executed, this can take multiple hours or even days and requires up to 16 GB of memory, both of which might depend on the system in question and is done by running:
> `python run_algorithms.py`

After concluding the previously empty `error_log.csv` now contains all estimates of changepoints for each sequence for each iteration and algorithm. This can be conveniently compiled into a readable format by executing:
> `python create_tables.py`

`error.csv` will now contain the final results.
