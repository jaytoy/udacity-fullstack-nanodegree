import psycopg2

query_three_most_popular_articles = """
    select title, count(log.id) 
    from articles, log 
    where log.path = ('/article/' || articles.slug)
    group by articles.title 
    order by count(log.id) desc
    limit 3;
"""
query_most_popular_authors = """
    select authors.name, count(log.id)
    from authors, articles, log
    where articles.author = authors.id
        and log.path = ('/article/' || articles.slug)
    group by authors.name
    order by count desc;
"""

query_days_with_errors = """
    create view errors as
    select time::date as date, count(*)
    from log
    where status not like '%200%'
    group by date;

    create view requests as
    select time::date as date, count(*)
    from log
    group by date;

    select 
        to_char(errors.date,'Month DD, YYYY') as date, 
        round(((errors.count::decimal/requests.count::decimal)*100), 1) as percentage
    from errors, requests
    where
        requests.date = errors.date
        and ((errors.count::decimal/requests.count::decimal)*100) > 1;
"""

def get(query):
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()
    db.close()

def main():
    print ("Q1. What are the most popular three articles of all time?\n")
    rows = get(query_three_most_popular_articles)
    for row in rows:
        print (row[0] + " - " + str(row[1]) + "views")

    
    print ("\nQ2. Who are the most popular article authors of all time?\n")
    rows = get(query_most_popular_authors)
    for row in rows:
        print (row[0] + " - " + str(row[1]) + "views")

    print ("\nQ3. On which days did more than 1% of requests lead to errors?\n")
    rows = get(query_days_with_errors)
    for row in rows:
        print (row[0] + " - " + str(row[1]) + "% errors")

if __name__ == "__main__":
    main() 