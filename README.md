# Team 4


# Getting Started with Flink-Placement
Follow these steps to set up and deploy the Flink-Placement project on your system.

## Step 1: Clone the Repository
Clone the Flink-Placement repository using the `git clone` command.

## Step 2: Load and Build the Project
Load the project in IntelliJ and build it using Maven configuration:

    clean package -DskipTests

## Step 3: Copy Build Contents
Copy the contents from the `build-target` folder to the `/opt/flink` folder.

## Step 4: Copy Scripts Folder
Copy the scripts folder to the `/opt/flink` directory.

## Step 5: Modify Configuration Files
In the scripts folder, modify the following files:

    workers
    masters
    slots
    flink-conf.yaml

## Step 6: Run the Deployment Script
Run the `deployflink.py` script. This script will automatically copy the Flink folder and respective configs to every worker (Raspberry Pis in our case).

## Step 7: Start the Flink Cluster
Start the Flink cluster using the following command:

    ./bin/start-cluster.sh

## Step 8: Modify the Scheduler Configuration
Modify the `schedulercfg` in the `scripts` folder according to your job and placement. Make sure you have the correct `schedulercfg` and `flink-conf.yaml`.

## Step 9: Submit the Job
Submit the job, and you can monitor the JobManager logs for now to see logs related to our cost model.
<br/>

# Experiments
Use the `flink_exp.py` script to run the experiments after submitting the job. This script would change the bandwidth, as well as manually switch the operator to each location `server` or the `Raspberry Pis`. This script would also add the timestamps, so that we can use it analyse the metrics collected in the `metrics.json` file in `/opt/flink/scripts` folder.


# Tests
We have implemented a query `Query11` in the example folder of the repository. Running a job of this query tests our cost model and switching of the operators automatically. It can be easily customized for different complexity and selectivity for the tests. There is also a version of it `Query11S70` with a different selectivity inside the same folder.

# Auxiliary codes and scripts

In the `scripts` folder, we have the following helper scripts -
1. deploy_flink.py - Used to deploy the newly build target of the flink project to all the master and worker nodes, and place the correct configurations.
2. flink_exp.py - Used to run experiments, while varying the bandwidth and placement of the operators (the choice value).
3. clean_exp.py - Resets the bandwidth of the Raspberry Pis.
4. limitcpu.py - Limits the CPU performance of the Raspberry Pis incase they are faster than your server to simulate real world.
5. switch_operator.py - Switches the filter operator from Server to Raspberry Pi or vice-versa based on the choice value sent.

# Apache Flink

For more information follow the instructions on how to setup and build on [Flink repository.](https://github.com/apache/flink)