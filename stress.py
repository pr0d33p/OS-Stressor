import argparse
from opensearchpy import OpenSearch
import concurrent.futures
import time
import threading
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOTAL_HIT_REQUEST = 0
RESP_COUNT = {}
TIME_TAKEN = []

def requester(thread_id, opensearch, lock):
    global TOTAL_HIT_REQUEST, RESP_COUNT, TIME_TAKEN

    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        req_time = time.time()
        try:
            opensearch.search(index=INDEX_NAME, body=QUERY)
        except Exception as e:
            print(f"Thread {thread_id + 1} | Error: {e}")
        end_time = time.time()
        with lock:
            TOTAL_HIT_REQUEST += 1
            TIME_TAKEN.append(end_time - req_time)

    print(f"Thread {thread_id + 1} is done!")

def main():
    global TOTAL_HIT_REQUEST, RESP_COUNT, TIME_TAKEN, INDEX_NAME, THREADS, TIMEOUT, QUERY

    parser = argparse.ArgumentParser(description="Simple OpenSearch stress testing tool.")
    parser.add_argument("--opensearch-host", default='localhost', help="OpenSearch host")
    parser.add_argument("--opensearch-port", type=int, default=9200, help="OpenSearch port")
    parser.add_argument("--index-name", default='*', help="Index name")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads.")
    parser.add_argument("-s", "--timeout", type=int, default=5, help="Time to Run")
    parser.add_argument("-u", "--username", default='admin', help="Username")
    parser.add_argument("-p", "--password", default='admin', help="Password")
    parser.add_argument("-q", "--query", default='{"query": {"match_all": {}}}', help="Query")
    args = parser.parse_args()

    OPENSEARCH_HOST = args.opensearch_host
    OPENSEARCH_PORT = args.opensearch_port
    INDEX_NAME = args.index_name
    THREADS = args.threads
    TIMEOUT = args.timeout
    QUERY = args.query
    OS_USER = args.username
    OS_PASS = args.password

    opensearch = OpenSearch(
        hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
        # use_ssl=True,
        verify_certs=False,
        http_compress=True,
        ssl_show_warn=False,
        http_auth=(OS_USER, OS_PASS)
    )

    print(f"{'OpenSearch Host':>15}: {OPENSEARCH_HOST}")
    print(f"{'OpenSearch Port':>15}: {OPENSEARCH_PORT}")
    print(f"{'Index Name':>15}: {INDEX_NAME}")
    print(f"{'Threads':>15}: {THREADS}")
    print(f"{'Time':>15}: {TIMEOUT}")

    threads = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            print(f"Starting Thread {i + 1}")
            threads.append(executor.submit(requester, i, opensearch, threading.Lock()))
        concurrent.futures.wait(threads, timeout=TIMEOUT)
        print("Shutting down threads...")

    print("Threads are done!")

    max_time, min_time, avg_time = max(TIME_TAKEN), min(TIME_TAKEN), sum(TIME_TAKEN) / len(TIME_TAKEN)

    print("-" * 30)
    print(f"Total Hits: {TOTAL_HIT_REQUEST}")
    print(f"Max Time: {max_time:.2f}")
    print(f"Min Time: {min_time:.2f}")
    print(f"Avg Time: {avg_time:.2f}")
    print("-" * 30)

if __name__ == "__main__":
    main()
