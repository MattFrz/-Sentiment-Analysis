"""
CS1026a 2023
Assignment 03
Matt Farzaneh
251370889
mfarzan
Date Completed: November, 19, 2023
"""
from sentiment_analysis import read_tweets, read_keywords, make_report, write_report


def main():
    keyword_file = input('Input keyword filename (.tsv file): ').strip()
    tweet_file = input('Input tweet filename (.csv file): ').strip()
    report_file = input('Input filename to output report in (.txt file): ').strip()

    try:
        # Check if the files have the correct extensions
        if not keyword_file.endswith('.tsv'):
            raise ValueError('Keyword file must have a .tsv extension!')
        if not tweet_file.endswith('.csv'):
            raise ValueError('Tweet file must have a .csv extension!')

        # Read data and generate report
        tweets_data = read_tweets(tweet_file)
        keywords_data = read_keywords(keyword_file)

        # Write report to the specified file
        report_data = make_report(tweets_data, keywords_data)
        write_report(report_data, report_file)

        print(f'Wrote report to {report_file}')

    except Exception as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    main()
