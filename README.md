## Opensearch Stressor

This is a simple tool to stress test OpenSearch clusters. It is written in Python and uses the `opensearchpy` library to interact with the cluster.

![OpenSearch Stressor](https://img.shields.io/badge/Opensearch-Stressor-blue?style=for-the-badge&logo=OpenSearch)
![Python](https://img.shields.io/badge/Python-3.6%2B-blue?style=for-the-badge&logo=python)

## What does it do?

The tool searches for a given query in a loop, with a given concurrency, for a given duration. It measures the time taken for each search request and logs the results.

## How to use it?

The tool is a Python script and requires Python 3.6 or later. It uses the `opensearchpy` library to interact with the cluster. You can install the library using pip:

```bash
pip install opensearch-py
```

You can then run the script using the following command:

```bash
python stressor.py --opensearch-host localhost --opensearch-port 9200 --index-name security-auditlog-* --threads 4 --timeout 10 --query '{"query": {"match_all": {}}}' --username <user> --password <password>
```

The script takes the following arguments:

- `--opensearch-host`: The hostname of the OpenSearch cluster.
- `--opensearch-port`: The port of the OpenSearch cluster.
- `--index-name`: The name of the index to search.
- `--threads`: The number of concurrent search requests to make.
- `--timeout`: The timeout for each search request.
- `--query`: The query to search for.
- `--username`: The username to use for authentication.
- `--password`: The password to use for authentication.

> ChatGPT is used to generate the README.MD file