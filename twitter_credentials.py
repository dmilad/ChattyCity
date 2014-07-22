import tweepy

consumer_key="o9P560AKPUcACYY1hPFmfQUVX"
consumer_secret="xmF127RAYgH7qKHnWJkKtchU7ocSLq12sh8CLys3tQjzbAprw3"

access_token="18185125-cU0fb3TdTR2pVIZHOqkHkZzaywt6ORp5JNEyBPDV3"
access_token_secret="IbVSOJaHDuX108FawfDSNgdjqfijA4eCny72k2KRy5O0c"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
