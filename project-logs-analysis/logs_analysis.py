#! /usr/bin/env python3
import psycopg2

query_three_most_popular_articles = """
    select
        title,
        count(log.id)
    from
        articles,
        log
    where
        log.path = ('/article/' || articles.slug)
    group by
        articles.title
    order by
        count(log.id) desc
    limit 3;
    """
query_most_popular_authors = """
    select
        authors.name,
        count(log.id)
    from
        authors,
        articles,
        log
    where
        articles.author = authors.id
        and log.path = ('/article/' || articles.slug)
    group by
        authors.name
    order by
        count desc;
    """

query_days_with_errors = """
    select
        to_char(errors.date,'Month DD, YYYY')
            as date,
        round(((errors.count::decimal/requests.count::decimal)*100), 1)
            as percentage
    from
        (select time::date as date, count(*) from log
            where status not like '%200%' group by date) as errors,
        ( select time::date as date, count(*) from log
            group by date) as requests
    where
        requests.date = errors.date
        and ((errors.count::decimal/requests.count::decimal)*100) > 1;
    """


def get(query):
    try:
        db = psycopg2.connect("dbname=news")
    except psycopg2.DatabaseError, e:
        print('Unable to connect!')
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def main():
    rows = get(query_three_most_popular_articles)
    print("Q1. What are the most popular three articles of all time?\n")
    for (title, count) in rows:
        print(" {} - {} views".format(title, count))

    rows = get(query_most_popular_authors)
    print("\nQ2. Who are the most popular article authors of all time?\n")
    for (author, count) in rows:
        print(" {} - {} views".format(author, count))

    rows = get(query_days_with_errors)
    print("\nQ3. On which days did more than 1% of requests lead to errors?\n")
    for (date, error) in rows:
        print(" {} - {}% errors".format(date, error))


if __name__ == "__main__":
    main()
