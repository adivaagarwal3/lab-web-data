# Load master_2009.json through master_2018.json, analyze the tweets, and make a bar chart.
# Follow the linked course assignment in README.md.
#!/usr/bin/python3
'''Count phrase frequencies in the tweet archive and plot them.'''
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FILES = [f'master_{year}.json' for year in range(2009, 2019)]

PHRASES = [
    'Obama',
    'Trump',
    'Mexico',
    'Russia',
    'Fake News',
    'Jobs',
    'Border',
    'Drain the Swamp',
]


def load_tweets(files):
    tweets = []
    for filename in files:
        with open(filename, encoding='utf-8') as f:
            tweets.extend(json.load(f))
    return tweets


def tweet_text(tweet):
    return tweet.get('full_text') or tweet.get('text') or ''


def count_phrases(tweets, phrases):
    texts = [tweet_text(t).lower() for t in tweets]
    counts = {}
    for phrase in phrases:
        p = phrase.lower()
        counts[phrase] = sum(1 for text in texts if p in text)
    return counts


def make_table(phrases, percentages):
    width = max(len(p) for p in phrases)
    lines = [
        f"| {'Phrase':>{width}} | Percentage |",
        f"| {'-' * (width - 1)}: | ---------: |",
    ]
    for phrase in phrases:
        pct = f"{percentages[phrase]:05.2f}%"
        lines.append(f"| {phrase:>{width}} | {pct:>10} |")
    return '\n'.join(lines)


def make_chart(phrases, percentages, filename='tweets.png'):
    values = [percentages[p] for p in phrases]
    plt.figure(figsize=(9, 5))
    plt.barh(phrases, values)
    plt.xlabel('Percentage of tweets containing phrase (%)')
    plt.ylabel('Phrase')
    plt.title('Phrase frequency in tweets, 2009-2018')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def main():
    tweets = load_tweets(FILES)
    total = len(tweets)
    print('Total tweets:', total)

    counts = count_phrases(tweets, PHRASES)
    for phrase in PHRASES:
        print(f'{phrase}: {counts[phrase]}')

    percentages = {p: 100 * counts[p] / total for p in PHRASES}

    table = make_table(PHRASES, percentages)
    print()
    print(table)

    make_chart(PHRASES, percentages)
    print('\nSaved chart to tweets.png')


if __name__ == '__main__':
    main()