from time import sleep
from selenium import webdriver

url = "https://jobvision.ir/Jobs?Page=1&JobTitle="
Base_url = "https://jobvision.ir"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--maximize")


def get_jobvision_jobs(job_query):
    # debug mode :
    driver = webdriver.Chrome(
        executable_path="driver_files/chromedriver", options=chrome_options
    )

    # ## production mode :
    # driver = webdriver.Remote(
    #     command_executor="http://selenium:4444/wd/hub",
    #     desired_capabilities=webdriver.common.desired_capabilities.DesiredCapabilities.CHROME,
    # )

    driver.get(url)

    try:
        btn = driver.find_element_by_class_name("btn-default")
        btn.click()
    except Exception as e:
        print(e)

    txtJobTitle = driver.find_element_by_id("txtJobTitle")
    txtJobTitle.clear()
    txtJobTitle.send_keys(job_query)

    job_post_search_sender = driver.find_element_by_id("job-post-search-sender")
    job_post_search_sender.click()
    print(">>>> btn clicked !!!!!!!!!!!!!!!!!!!!")
    try:
        driver.switch_to_default_content()
    except:
        pass
    # TODO: fix iframe
    jobs = []
    for jobpost in driver.find_elements_by_class_name("jobpost-box"):
        job_link = Base_url + jobpost.get_attribute("data-href")
        job_title = jobpost.find_element_by_class_name("jobpost-title").text
        company_title = jobpost.find_element_by_class_name("company-title").text
        city = jobpost.find_element_by_class_name("citySpan").text
        type_of_time = jobpost.find_element_by_class_name("typeOfWorkSpan").text
        jobs.append(
            {
                "job_link": job_link,
                "job_title": job_title,
                "company_title": company_title,
                "city": city,
                "type_of_time": type_of_time,
            }
        )
    driver.close()
    return jobs
