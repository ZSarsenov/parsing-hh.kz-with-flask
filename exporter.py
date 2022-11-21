import csv

def save_to_csv(jobs):
    file = open('jobs.csv', mode='w')
    writter = csv.writer(file)
    writter.writerow(['title', 'company', 'location', 'solary', 'link'])
    for job in jobs:
        writter.writerow(list(job.values()))
    return