from selenium import webdriver


url = "https://jobinja.ir/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--maximize")


def get_jobinja_jobs(job_query):
    driver = webdriver.Chrome(
        executable_path="driver_files/chromedriver", options=chrome_options
    )
    res = driver.get(url)

    fillable_job_title_element = driver.find_element_by_class_name(
        "c-jobSearchTop__blockInput"
    )
    fillable_job_title_element.clear()
    fillable_job_title_element.send_keys(job_query)

    button = driver.find_element_by_name("button")
    button.click()

    job_list = driver.find_elements_by_class_name("o-listView__itemInfo")
    jobs = []
    for job in job_list:

        job_link = job.find_element_by_class_name(
            "o-listView__itemIndicator"
        ).get_property("href")
        job_title = job.find_element_by_class_name("c-jobListView__titleLink").text
        job_complement_info = job.find_element_by_class_name(
            "o-listView__itemComplementInfo"
        ).text
        jobs.append(
            {
                "job_link": job_link,
                "job_title": job_title,
                "job_complement_info": job_complement_info,
            }
        )
    return jobs
