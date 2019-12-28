from diskcache import Cache
from flask import Flask, request

from crawler import get_jobinja_jobs

app = Flask(__name__)
jobinja_cache = Cache("jobinja_cache")


@app.route("/query-jobinja", methods=["POST"])
def query_jobinja():
    job_title = request.json["job_title"]
    if job_title in jobinja_cache:
        results = jobinja_cache.get(job_title)
    else:
        results = get_jobinja_jobs(job_title)
        jobinja_cache.set(job_title, results, 24 * 60 * 60)
    return {"results": results}


@app.route("/status", methods=["Get"])
def status():
    return {"response": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000)
# curl --header "Content-Type: application/json" --request POST --data '{"job_title":"c#"}' http://192.168.42.58:5000/query-jobinja


# TODO: pull selenium image to use it
# TODO: Add caching layer
