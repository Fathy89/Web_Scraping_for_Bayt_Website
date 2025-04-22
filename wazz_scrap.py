from bs4 import BeautifulSoup
import csv
import requests
import re
import time

def main():
    base_url = 'https://www.bayt.com/ar/international/jobs/software-engineer-jobs/?page='
    res = []

    for page_num in range(1, 25):  
        url = base_url + str(page_num)  
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to load page {page_num}")
            continue  

        soup = BeautifulSoup(response.content, 'lxml')
        job_cards = soup.find_all("li", {"class": "has-pointer-d"})

        def get_job_info(job):
            try:
                job_title = job.contents[1].text.strip() if len(job.contents) > 1 else "N/A"
                company_info = job.contents[3] if len(job.contents) > 3 else None

                if company_info:
                    company_location = company_info.find("div", {"class": "t-mute t-small"})
                    company_name = company_info.find("span")

                    company_location = company_location.text.strip() if company_location else "N/A"
                    company_name = company_name.text.strip() if company_name else "N/A"
                else:
                    company_location = "N/A"
                    company_name = "N/A"

                job_description = job.contents[5].text.strip() if len(job.contents) > 5 else "N/A"
                job_description = re.sub(r"^[=+\-0-9\s]+", "", job_description)

                about = job.contents[7] if len(job.contents) > 7 else None

                if about:
                    salary_tag = about.find("dt", {"class": "p0 m20r jb-label-salary"})
                    expected_salary = salary_tag.text.strip() if salary_tag else "N/A"

                    career = about.find("dt", {"class": "p0 m20r jb-label-careerlevel"})
                    required_years = career.text.strip() if career else "N/A"

                    work_type = about.find("dt", {"class": "p0 m20r jb-label-remote"})
                    work = work_type.text.strip() if work_type else "من المكتب"

                    additional = about.find("dt", {"class": "p0 m20r jb-label-citizenship"})
                    additional_terms = additional.text.strip() if additional else "N/A"
                else:
                    expected_salary = "N/A"
                    required_years = "N/A"
                    work = "N/A"
                    additional_terms = "N/A"

                res.append({
                    "Job Title": job_title,
                    "Company Name": company_name,
                    "Company Location": company_location,
                    "Job Description": job_description,
                    "Expected Salary": expected_salary,
                    "Years of Experience": required_years,
                    "Working Place": work,
                    "Additional Terms": additional_terms
                })

                time.sleep(2)  # Avoid getting blocked by the website

            except Exception as e:
                print(f"Error processing job listing: {e}")

        for job in job_cards:
            get_job_info(job)

    if res:
        csv_file_path = r"C:\Users\2M\Desktop\result.csv"
        keys = res[0].keys()

        with open(csv_file_path, mode="w", newline="", encoding="utf-8-sig") as out:
            dict_out = csv.DictWriter(out, fieldnames=keys)
            dict_out.writeheader()
            dict_out.writerows(res)
            print(f"File Created: {csv_file_path}")

main()
