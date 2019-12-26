from flask import Flask, request

from crawler import get_jobvision_jobs

app = Flask(__name__)


@app.route("/query-jobvision", methods=["POST"])
def query_jobvision():
    job_title = request.json["job_title"]
    return {"results": get_jobvision_jobs(job_title)}


@app.route("/status", methods=["Get"])
def status():
    return {"response": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000)
# curl --header "Content-Type: application/json" --request POST --data '{"job_title":"c#"}' http://localhost:5000/query-jobvision


# TODO: Add caching layer
