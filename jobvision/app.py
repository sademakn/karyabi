from flask import Flask, request

from crawler import get_jobvision_jobs
from diskcache import Cache

app = Flask(__name__)
jobvision_cache = Cache("jobvision_cache")


@app.route("/query-jobvision", methods=["POST"])
def query_jobvision():
    job_title = request.json["job_title"]
    if job_title in jobvision_cache:
        results = jobvision_cache.get(job_title)
    else:
        results = get_jobvision_jobs(job_title)
        jobvision_cache.set(job_title, results, 24 * 60 * 60)
    return {"results": results}


@app.route("/status", methods=["Get"])
def status():
    return {"response": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000)
# curl --header "Content-Type: application/json" --request POST --data '{"job_title":"c#"}' http://localhost:5000/query-jobvision


# TODO: Add caching layer
