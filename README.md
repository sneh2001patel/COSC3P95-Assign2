# COSC3P95-Assign2

To run the program:

Create a virtual environment (this is to ensure the packages are consistent with what we used.), you can use the command `python3 -m venv venv` after installing make sure to activate it `source venv/bin/activate`

Run the command `pip install -r requirements.txt` to install the necessary packages used.

If you want to run the program without the implementation of any open-telemetry navigate to the `main` branch and open 2 terminal windows one to run the server and another for the client.

- To run the server: `python3 server.py`
- To run the client: `python3 client.py`

If you want to run the program with open-telemetry automatic instrumentation, navigate to the `opentelemetry_auto` branch open 2 terminal windows one to run the server and another for the client.

- To run the server: `opentelemetry-instrument --traces_exporter console --metrics_exporter none python3 server.py`
- To run the client: `python3 client.py`

If you want to run the program with open-telemetry manaul instrumentation, navigate to the `opentelemetry_manaul` branch open 2 terminal windows one to run the server and another for the client.

- To run the server: `python3 server.py`
- To run the client: `python3 client.py`

To visualize the results in Jaegar please download the `Docker Application`, then run the application and write the command
`docker run -d --name jaeger -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 -p 5775:5775/udp -p 6831:6831/udp -p 6832:6832/udp -p 5778:5778 -p 16686:16686 -p 14268:14268 -p 14250:14250 -p 9411:9411 jaegertracing/all-in-one:1.23` to initlize a jaegar container in docker, then while its running, run the open-telemetry (either one is fine), navigate to `localhost:16686`, to view the results.

If you want to run the program with the bug implemented in it navigate to the `bug_on_purpose` branch open 2 terminal windows one to run the server and another for the client.

- To run the server: `python3 server.py`
- To run the client: `python3 client.py`

If you want to see the solution implemented to fix the bug navigate to the `fix_bug` branch open 2 terminal windows one to run the server and another for the client.

- To run the server: `python3 server.py`
- To run the client: `python3 client.py`

All of the data used in this project has retireved from this url: https://www.stats.govt.nz/large-datasets/csv-files-for-download/

Don't know what file to test on, use the csv files in the data folder.
For example, Run the server and client, and then in client type `data/1.csv` to see pass use cases, to see failed use case try typing `noname.txt` it should fail.
