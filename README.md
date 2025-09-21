# Distributed_Systems_Workflow_Optimizer

## 📌 Overview
This project demonstrates a **Spark-based distributed systems workflow optimizer** with two major components:
1. **Graph Optimizer (Dijkstra’s Algorithm)** – implemented in PySpark to compute shortest paths across large graphs efficiently.
2. **Fault-tolerant Streaming Pipeline** – built with **Spark Structured Streaming** and checkpointing for real-time word count and recovery from failures.

It combines **batch + streaming workloads** and showcases how Spark can be used for scalable graph analytics and streaming data reliability.

---

## 🚀 Features
- ✅ **Dijkstra Graph Optimizer** – computes shortest paths using PySpark RDD/DataFrames.  
- ✅ **Streaming Checkpoint Demo** – ensures recovery after failures with Spark’s checkpoint mechanism.  
- ✅ **Fault Tolerance** – recovers state automatically via checkpoints (`tmp/chk`).  
- ✅ **Structured Streaming WordCount** – processes new input files in `tmp/stream_in` continuously.  
- ✅ **Colab-Friendly** – runs end-to-end inside Google Colab without external cluster setup.  

---

## 📂 Project Structure

Distributed_Systems_Workflow_Optimizer/  
├── data/                # Graph input data (CSV)  
├── out/                 # Streaming output (word counts)  
├── scripts/             # Utility shell scripts for running jobs  
├── src/                 # Core PySpark programs  
│   ├── dijkstra_spark.py  
│   └── streaming_checkpoint_demo.py  
├── tmp/                 # Temporary directory for input/checkpoints  
│   ├── stream_in/       # Streaming input files  
│   └── chk/             # Checkpoint directory  
├── README.md            # Project documentation  
└── notebook.ipynb       # End-to-end runnable notebook (Colab)  

---

## 🛠️ How It Works

### 1. Graph Optimization (Batch Mode)

Run shortest path computation:  

```bash
!python src/dijkstra_spark.py --input data/graph_edges.csv --source A --destination Z
```

### 2. Streaming WordCount (with Checkpointing)

Start the streaming job:

```bash
!python src/streaming_checkpoint_demo.py \
  --inputDir tmp/stream_in \
  --checkpointDir tmp/chk \
  --triggerSec 5
```

Feed streaming input while job is running:

```bash
!echo "hello spark streaming test" > tmp/stream_in/batch1.txt
!echo "spark streaming checkpoint recovery" > tmp/stream_in/batch2.txt
```

- ✅Spark will process these files in micro-batches and update word counts.
- ✅Checkpointing ensures recovery if the job crashes and restarts.

## 📌 Why This Project is Important

- Shows how distributed graph algorithms (like Dijkstra) scale on big datasets with Spark.  
- Demonstrates fault tolerance in streaming, critical for production pipelines (finance, IoT, logging, fraud detection, etc.).  
- Provides a Colab-ready workflow, lowering barriers for testing Spark-based distributed systems.  

---

## ⚠️ Difficulties Faced

We encountered multiple real-world debugging challenges:

❌ **Concurrent Queries Error** – Spark threw `SparkConcurrentModificationException` when multiple queries used the same checkpoint.  

❌ **Output Modes Mismatch** – Writing to Parquet with *complete mode* caused errors; required using *append mode*.  

❌ **Colab Limitation** – Couldn’t run two cells in parallel (stream job + data feeding). We solved this by pre-creating input batches before starting the job.  

❌ **File Path Issues** – Misplaced script files weren’t included in the zip until we confirmed proper saving in  
`/content/Distributed_Systems_Workflow_Optimizer/scripts`.  

❌ **Git Push Authentication** – Faced credential issues in Colab; solved by downloading locally and pushing manually.  

➡️ These reflect the practical hurdles in distributed systems, reinforcing concepts beyond just code.  

---

## 📑 Future Improvements

- Add Kafka source for real-time streaming instead of file-based.  
- Extend graph optimizer to handle weighted directed acyclic graphs and multi-source shortest paths.  
- Build a Dockerfile for easier reproducibility outside Colab.


👤 Author
Bharathraaj Nagarajan

