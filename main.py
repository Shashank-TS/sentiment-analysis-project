import pandas as pd
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()
    
    # print("Inspecting first few lines of data:")
    # for line in data[:5]:
    #     print(line.strip())
    
    return data

def parse_data(data):
    messages = []
    for line in data:
        match = re.match(r'(\d{1,2}[-/]\d{1}[-/]\d{2}), (\d{1,2}:\d{2} [APM]{2}) - (\w+): (.+)', line)
        if match:
            date, time, sender, message = match.groups()
            messages.append([f"{date}, {time}", sender, message])
        else:
            print("No match for line:", line.strip())

    df = pd.DataFrame(messages, columns=['Date', 'Sender', 'Message'])
    print("Parsed DataFrame:")
    print(df.head())
    
    return df

def analyze_sentiment(df):
    df['Sentiment'] = df['Message'].apply(lambda msg: TextBlob(msg).sentiment.polarity)
    df['Sentiment_Label'] = df['Sentiment'].apply(lambda score: 'Positive' if score > 0 else ('Negative' if score < 0 else 'Neutral'))
    
    print("DataFrame with Sentiment:")
    print(df[['Message', 'Sentiment', 'Sentiment_Label']].head())
    print("Unique Sentiment Labels:")
    print(df['Sentiment_Label'].value_counts())
    
    return df

def plot_sentiment(df):
    if df.empty:
        print("No data to plot.")
        return
    
    print("Sentiment Label Distribution:")
    print(df['Sentiment_Label'].value_counts())
    
    sns.countplot(data=df, x='Sentiment_Label', palette="viridis")
    plt.title("Sentiment Distribution in WhatsApp Chat")
    plt.show()

def main(file_path):
    data = load_data(file_path)
    df = parse_data(data)
    df = analyze_sentiment(df)
    plot_sentiment(df)

if __name__ == "__main__":
    main('chatData.txt')