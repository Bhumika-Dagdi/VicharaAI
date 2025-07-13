import tweepy
from config import CONFIG
from utils.logger import log_action

def post_tweet(st):
    st.subheader("🐦 Post a Tweet")
    tweet = st.text_area("Tweet Message", key="tweet_message")

    if st.button("Post Tweet"):
        try:
            if not tweet.strip():
                st.error("Tweet cannot be empty!")
                return

            client = tweepy.Client(
                bearer_token=CONFIG['twitter']['bearer_token'],
                consumer_key=CONFIG['twitter']['api_key'],
                consumer_secret=CONFIG['twitter']['api_secret'],
                access_token=CONFIG['twitter']['access_token'],
                access_token_secret=CONFIG['twitter']['access_secret']
            )

            api = client.create_tweet(text=tweet)
            st.success("✅ Tweet posted!")
            st.write(f"Tweet ID: {api.data['id']}")
            log_action("Tweet posted")

        except Exception as e:
            st.error(f"❌ Error posting tweet: {str(e)}")
            log_action(f"Tweet error: {str(e)}")
