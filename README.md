# 🐝 Hive-Based Data Warehouse on Highly Available Hadoop Cluster

This project sets up a **Highly Available Hadoop Cluster with Apache Hive** using Docker. It integrates PostgreSQL for the Hive Metastore, supports ACID and non-ACID Hive tables, and includes an automated ELT pipeline built with Python and Hive SQL.

---

## 📁 Project Structure

- **config_ha/**: Contains configuration files for Hadoop, Hive, and ZooKeeper.
- **docker-compose.yml**: Orchestrates the full cluster and services.
- **Dockerfile**: Multi-stage Dockerfile for building Hadoop + Hive images efficiently.
- **entrypoint.sh**: Initializes Hive metastore schema and starts services.
- **ha_setup.sh**: Automates the setup of Hadoop HA components.
- **scale_datanodes.sh**: Adds new DataNodes dynamically.
- **cleanup.sh**: Removes all cluster containers and volumes.
- **health_check.sh**: Verifies NameNode and ResourceManager availability.
- **scripts/**: Contains Python ELT scripts, Hive SQL (HQL) transformations, and cron automation.

---

## 🧩 Cluster Components

- **ZooKeeper Nodes**: `zk1`, `zk2`, `zk3`
- **JournalNodes**: `jn1`, `jn2`, `jn3`
- **NameNodes**: `nn1`, `nn2`, `nn3` (configured for HA failover)
- **DataNode**: `dn1` (scalable)
- **ResourceManagers**: Included in masters, with failover support
- **HiveServer2**: `hive-server`
- **PostgreSQL**:
  - For Hive Metastore
  - For OLTP source system (used in ELT)
- **Python Node**: Runs `Python + HDFS + Hive Client` to perform ELT operations

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/otifi3/hadoop_cluster.git
cd hadoop_cluster
```

### 2. Build and Launch the Cluster

```bash
docker-compose up --build
```

This will start:
- 3x HA NameNodes with ZooKeeper failover
- 1x DataNode (scalable)
- Hive Metastore (PostgreSQL) and HiveServer2
- OLTP PostgreSQL for extraction
- Python-enabled containers for ELT scripts

---

## 🌐 Accessing Web Interfaces

| Service           | URL                          |
|------------------|-------------------------------|
| HDFS NameNode 1  | http://localhost:9870         |
| HDFS NameNode 2  | http://localhost:9871         |
| HDFS NameNode 3  | http://localhost:9872         |
| YARN RM (1–3)    | http://localhost:8088/89/90   |
| HiveServer2 (JDBC)| `jdbc:hive2://localhost:10000` |

---

## ⚙️ Scaling

To add DataNodes dynamically:

```bash
chmod +x scale_datanodes.sh
./scale_datanodes.sh <number>
```

---

## 🧹 Clean Up

```bash
chmod +x cleanup.sh
./cleanup.sh
```

---

## 📦 Hive Architecture Overview

### ✅ Phase 1: Cluster + Hive Setup

- Hive Metastore backed by **PostgreSQL**
- HiveServer2 for JDBC/ODBC queries
- Entry scripts initialize Hive schema on startup
- Tez as the default execution engine with vectorized query support
- Hive configuration mounted via `hive-site.xml`
- Container networking and volumes handle persistence
- **Python Node**: Installed with HDFS client, Hive client, and Python to run ELT jobs

### ✅ Phase 2: Data Warehouse & ELT Pipeline

#### Goals:
- Migrate data from Amazon Redshift → Hive
- Implement incremental ELT with history tracking (SCD2)
- Optimize schema for distributed analytics

#### Key Features:
- ACID and non-ACID tables
- ORC format with partitioning & bucketing
- PySpark-style extraction using Python
- Hive SQL transformations via `schedule_elt.hql`
- Cronjob for automated execution via `run_elt.sh`

---

## 🔁 ELT Workflow

### 1. Python-Based Extraction

- Connects to OLTP PostgreSQL
- Extracts data into CSV format
- Saves files to shared volume (`/tmp_data`)

### 2. Upload to HDFS

- Bash script copies CSV to `/staging/<table>/<table>.csv`

### 3. Hive Transformation

- External tables read staged data
- Transforms + inserts into final tables
- Supports ACID merges and full refresh for non-ACID

### 4. Incremental Logic

- Extract deltas using timestamps
- Merge/update in Hive using SCD2 strategies

---

## 🧠 Schema Design

### 🔄 SCD2 Handling
- **ACID Tables**: Use Hive `MERGE` for updates + inserts
- **Non-ACID**: Overwrite entire table per load with versioning

### 🗃 Fact Table Optimizations
- Denormalized wide tables for fewer joins
- Partitioned on keys like `reservation_date_key`
- Bucketed large tables to reduce shuffle

---

## 🕒 Automation with Cron

On the Docker host:

```bash
crontab -e
```

Add:

```cron
0 0 * * * docker exec hadoop_hive_1 bash /home/hadoop/scripts/run_elt.sh
```

---

## 🛠 Tools Used

- Hive + Hadoop
- Docker + Docker Compose
- Apache Tez
- Python
- PostgreSQL (OLTP + Metastore)
- HDFS
- Bash / Cron

---

## 👤 Author

Created by **Ahmed Otifi**  
🔗 [https://github.com/otifi3](https://github.com/otifi3)
