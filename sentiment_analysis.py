"""
CS1026a 2023
Assignment 03
Matt Farzaneh
251370889
mfarzan
Date Completed: November, 19, 2023
"""


# reads keywords
def read_keywords(keyword_file_name):
    # checking if it is a tsv file
    if not keyword_file_name.endswith('.tsv'):
        raise ValueError('Keyword file must have a .tsv extension!')
    try:
        keyword_file = open(keyword_file_name, 'r')
        # checking if file is empty or not
        if not keyword_file.read().strip():
            raise ValueError('The tweet list or keyword is empty')
        # sets reference point to 0
        keyword_file.seek(0)
        keyword_dict = {}
        # cleans the lines in the file and splits words and data points with a tab
        # adds score into dictionary
        for line in keyword_file:
            keyword, score = line.strip().split('\t')
            keyword_dict[keyword] = int(score)
        keyword_file.close()
        return keyword_dict
    # error checking
    except IOError:
        print(f'Error: Unable to open file [{keyword_file_name}]!')
        return {}


# cleans the text in the tweet to make it easier to work with
def clean_tweet_text(tweet_text):
    processed_tweet = tweet_text.lower()
    processed_tweet = ''.join([c for c in processed_tweet if c.isalpha() or c.isspace()])
    return processed_tweet


# calculates sentiment
def calc_sentiment(tweet_text, keyword_dict):
    tot = 0
    tweet_text = tweet_text.split(' ')
    for word in tweet_text:
        if word in keyword_dict:
            tot = tot + keyword_dict[word]
    return tot


# classifies the score in a word
def classify(score):
    if score > 0:
        return 'positive'
    elif score < 0:
        return 'negative'
    else:
        return 'neutral'


def read_tweets(tweet_file_name):
    # makes sure file entered is a csv file
    if '.csv' not in tweet_file_name:
        raise Exception('please ensure the file has a .csv extension!')
    try:
        # checks if file is empty or not
        tweet_file = open(tweet_file_name, 'r')
        if not tweet_file.read().strip():
            raise Exception('The tweet list or keyword dictionary is empty!')
        tweet_file.seek(0)
        tweet_list = []
        for line in tweet_file:
            # cleans up file and puts comma between words and data points
            fields = line.strip().split(',')
            # checks latitude
            try:
                latitude = float(fields[9])
            except ValueError:
                latitude = fields[9]
            # checks longitude
            try:
                longitude = float(fields[10])
            except ValueError:
                longitude = fields[10]
            # adds data to tweet list
            tweet_list.append({
                'date': fields[0],
                'text': clean_tweet_text(fields[1]),
                'user': fields[2],
                'retweet': int(fields[3]),
                'favorite': int(fields[4]),
                'lang': fields[5],
                'country': fields[6],
                'state': fields[7],
                'city': fields[8],
                'lat': latitude,
                'lon': longitude
            })
        tweet_file.close()
        return tweet_list
    # exception if file can't be opened
    except IOError:
        print(f'Error: Could not open file [{tweet_file_name}]!')
        return []


def sort_key(item):
    return item[1]


# function that makes the report
def make_report(tweet_list, keyword_dict):
    num_fav, num_ret, num_tweets = 0, 0, 0
    fav_sentiment, ret_sentiment, tot_sentiment = 0, 0, 0
    country_sentiment = []
    num_pos, num_neg, num_neu = 0, 0, 0

    for tweet in tweet_list:
        # constructs the report using previous functions
        sentiment_score = calc_sentiment(tweet['text'], keyword_dict)

        num_tweets = num_tweets + 1
        tot_sentiment = tot_sentiment + sentiment_score
        # sums up the numbers
        sentiment_category = classify(sentiment_score)
        num_pos = num_pos + (sentiment_category == 'positive')
        num_neg = num_neg + (sentiment_category == 'negative')
        num_neu = num_neu + (sentiment_category == 'neutral')

        # updates num and sentiment variables
        if tweet['retweet'] > 0:
            num_ret = num_ret + 1
            ret_sentiment = ret_sentiment + sentiment_score
        if tweet['favorite'] > 0:
            num_fav = num_fav + 1
            fav_sentiment = fav_sentiment + sentiment_score

        # adds country, sentiment score and count to country_sentiment
        country = tweet['country']
        if country != 'NULL':
            if country in country_sentiment:
                country_sentiment[country][1] = country_sentiment[country][1] + 1
            else:
                country_sentiment.append((country, sentiment_score, 1))

    # sort country_sentiment in descending order
    country_sentiment = sorted(country_sentiment, key=sort_key, reverse=True)

    # extract top five countries for the report
    top_five_countries_list = []
    # adds data unto top 5 countries list
    for country in country_sentiment[:5]:
        if country not in top_five_countries_list:
            top_five_countries_list.append(country[0])
        else:
            top_five_countries_list.append("")
    top_five_countries = ', '.join(top_five_countries_list)

    # calculates averages
    if num_fav:
        avg_favorite_sentiment = round(fav_sentiment / num_fav, 2)
    else:
        avg_favorite_sentiment = 0

    if num_ret:
        avg_retweet_sentiment = round(ret_sentiment / num_ret, 2)
    else:
        avg_retweet_sentiment = 0

    if num_tweets:
        avg_total_sentiment = round(tot_sentiment / num_tweets, 2)
    else:
        avg_total_sentiment = 0

    # puts everything into report
    report = {
        'avg_favorite': avg_favorite_sentiment,
        'avg_retweet': avg_retweet_sentiment,
        'avg_sentiment': avg_total_sentiment,
        'num_favorite': num_fav,
        'num_negative': num_neg,
        'num_neutral': num_neu,
        'num_positive': num_pos,
        'num_retweet': num_ret,
        'num_tweets': num_tweets,
        'top_five': top_five_countries
    }
    return report


# writes report
def write_report(report, output_file):
    # makes sure txt file is inputted
    if '.txt' not in output_file:
        raise ValueError('Please ensure the file has a .txt extension!')
    # adds everything into output file
    try:
        output_file = open(output_file, 'w')
        output_file.write(f'Average sentiment of all tweets: {report["avg_sentiment"]}\n')
        output_file.write(f'Total number of tweets: {report["num_tweets"]}\n')
        output_file.write(f'Number of positive tweets: {report["num_positive"]}\n')
        output_file.write(f'Number of negative tweets: {report["num_negative"]}\n')
        output_file.write(f'Number of neutral tweets: {report["num_neutral"]}\n')
        output_file.write(f'Number of favorited tweets: {report["num_favorite"]}\n')
        output_file.write(f'Average sentiment of favorited tweets: {report["avg_favorite"]}\n')
        output_file.write(f'Number of retweeted tweets: {report["num_retweet"]}\n')
        output_file.write(f'Average sentiment of retweeted tweets: {report["avg_retweet"]}\n')
        output_file.write(f'Top five countries by average sentiment: {report["top_five"]}\n')
        output_file.close()
    # if file can't be opened
    except IOError:
        print(f'Error: Unable to open file [{output_file}]')
