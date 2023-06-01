# scripts for placement experiments

## configuration

in this example we have 4 TaskManagers. each TaskManager has 4 slots. -> 16 slots in total

0. setup all nodes. make sure the JobManager node can `ssh` to all TaskManager nodes without password (by adding ssh pub key of the JobManager node to `authorized_keys` of all TaskManager nodes)

1. change IP address of TaskManager in `workers`

2. change IP address of JobManager in `masters` and `flink-conf.yaml`

3. change numberOfTaskSlots in `flink-conf.yaml` (num of slots per TaskManager)

4. If you wish to use custom scheduling, you need to finish the following steps:

   4.1 Set `jobmanager.scheduler: Custom` in `flink-conf.yaml`

   4.2 Write the placement plan in `schedulercfg`. For each line, specify task name and the IP address of corresponding task manager. For example, for Nexmark Query1 with 1 source, 2 map and 1 sink, the `schedulercfg` file is:

    ```
    Latency Sink (1/1); 192.168.1.180
    Mapper (2/2); 192.168.1.181
    Mapper (1/2); 192.168.1.181
    Source: Bids Source (1/1); 192.168.1.180
    ```

    We have provided a helper script `permutation.py` that could help you generate the `schedulercfg` file for all possible placement plans for a given job and cluster.  

5. Deploy Flink

    We have provided a helper script to deploy the cluster. On JobManager node, run 
    
    ```
    cd scripts
    python3 deployflink.py start
    ```

6. Submit the job on Flink WebUI. Then you can check the placement of the job.

7. Shutdown Flink
    
    After you finished the experiment, on JobManager, run 

    ```
    cd scripts
    python3 deployflink.py stop
    ```
   
## How to start

Here is an example guideline to help you understand the goal of the project, but feel free to come up with your own design!

#### 1. Start with a simple query. 
  - We have implemented 4 queries from Nexmark Benchmark. You can find them in [example](../example/) folder. Choose one of them.  
  - Fix the parallelism of the operators. Disable slot sharing and operator chaining, so that each subtask will use 1 slot.

#### 2. Start with a simple setting with 1 RPi and 1 Server(e.g. your laptop) with the following scheduling policy:
  - Deploy a Flink cluster with 1 TaskManager on RPi and 1 TaskManager on Server. 
  - Place the source operator on RPi side to simulate collecting data on edge side. Also, put some lightweight pre-processing operators(e.g. filter) on RPi side.
  - Place more computation heavy operation(e.g. window or join) and sink operator on Server side.
  - Use `tc` command to limit the outbound bandwidth and add extra latency on RPi in order to simulate Wide Area Network. For example, 50Mbps bandwidth and 50ms latency.   

#### 3. Deploy the job and collect performance metrics
  - You can write some scripts to automatically change placement, deploy Flink cluster and jobs, and collect the metrics from Flink. There is a python library [flink-res-client](https://pypi.org/project/flink-rest-client/) that may help you.

#### 4. Run the experiment again with another scheduling policy. 
   - For example, only place Source operators on RPi and all others on Server. Compare the performance/resource usage under different policy. 

#### 5. Think about the following questions. Design algorithms/experiments to answer these questions.  
  - Are there any difference on performance under different placement plan? Why?
  - Can we offload some operators to RPi side in order to reduce network traffic through WAN/reduce resource usage on server side? 
    - How to ensure the performance in this case? Can we provide some guarantee on the latency/throughput?
  - Can we design an algorithm to decide which operator should be offloaded to RPi side?
    - Based on performance characteristics like true processing rate

#### 6. Use other queries that is more realistic for IoT scenarios. Redo the experiments above.
  - You might see more obvious difference on the performance of different policy.
  - We can provide some suitable queries. For example, do a machine learning inference on images collected from edge
  - You may use more RPis to simulate collecting data from edge devices at different locations. 


