---
name: x-twitter
description: "Interact with X (Twitter) using the twitter-api-v2 library. Use for posting tweets, reading timelines, and managing DMs."
---

# X (Twitter) Skill

Use the `twitter-api-v2` library to interact with X (Twitter). This skill provides basic functionality for posting tweets, reading timelines, and managing DMs.

## Setup

1. Install the `twitter-api-v2` package:
   ```bash
   npm install -g twitter-api-v2
   ```

2. Set up your API keys. You'll need:
   - API Key
   - API Key Secret
   - Access Token
   - Access Token Secret

   Store them as environment variables:
   ```bash
   export TWITTER_API_KEY="your_api_key"
   export TWITTER_API_SECRET="your_api_secret"
   export TWITTER_ACCESS_TOKEN="your_access_token"
   export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
   ```

## Usage

### Post a Tweet
```bash
node -e "
const { TwitterApi } = require('twitter-api-v2');
const client = new TwitterApi({
  appKey: process.env.TWITTER_API_KEY,
  appSecret: process.env.TWITTER_API_SECRET,
  accessToken: process.env.TWITTER_ACCESS_TOKEN,
  accessSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

(async () => {
  try {
    const tweet = await client.v2.tweet('Your tweet text here');
    console.log('Tweet posted:', tweet.data.id);
  } catch (error) {
    console.error('Error posting tweet:', error);
  }
})();
"
```

### Read Home Timeline
```bash
node -e "
const { TwitterApi } = require('twitter-api-v2');
const client = new TwitterApi({
  appKey: process.env.TWITTER_API_KEY,
  appSecret: process.env.TWITTER_API_SECRET,
  accessToken: process.env.TWITTER_ACCESS_TOKEN,
  accessSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

(async () => {
  try {
    const timeline = await client.v2.tweet('Your tweet text here');
    console.log('Tweet posted:', tweet.data.id);
  } catch (error) {
    console.error('Error posting tweet:', error);
  }
})();
"
```

### Get User Info
```bash
node -e "
const { TwitterApi } = require('twitter-api-v2');
const client = new TwitterApi({
  appKey: process.env.TWITTER_API_KEY,
  appSecret: process.env.TWITTER_API_SECRET,
  accessToken: process.env.TWITTER_ACCESS_TOKEN,
  accessSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

(async () => {
  try {
    const user = await client.v2.userByUsername('twitter_username');
    console.log('User info:', user.data);
  } catch (error) {
    console.error('Error getting user:', error);
  }
})();
"
```

## Common Operations

### Post a Tweet with Media
```bash
node -e "
const fs = require('fs');
const { TwitterApi } = require('twitter-api-v2');
const client = new TwitterApi({
  appKey: process.env.TWITTER_API_KEY,
  appSecret: process.env.TWITTER_API_SECRET,
  accessToken: process.env.TWITTER_ACCESS_TOKEN,
  accessSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

(async () => {
  try {
    const media = fs.readFileSync('path/to/image.jpg');
    const uploadedMedia = await client.v2.uploadMedia(media, 'image/jpeg');
    const tweet = await client.v2.tweet('Check this out!', {
      media: { media_ids: [uploadedMedia.media_id_string] }
    });
    console.log('Tweet with media posted:', tweet.data.id);
  } catch (error) {
    console.error('Error posting tweet with media:', error);
  }
})();
"
```

### Reply to a Tweet
```bash
node -e "
const { TwitterApi } = require('twitter-api-v2');
const client = new TwitterApi({
  appKey: process.env.TWITTER_API_KEY,
  appSecret: process.env.TWITTER_API_SECRET,
  accessToken: process.env.TWITTER_ACCESS_TOKEN,
  accessSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

(async () => {
  try {
    const tweet = await client.v2.tweet('Your reply text here', {
      in_reply_to_tweet_id: 'tweet_id_to_reply_to'
    });
    console.log('Reply posted:', tweet.data.id);
  } catch (error) {
    console.error('Error posting reply:', error);
  }
})();
"
```

### Like a Tweet
```bash
node -e "
const { TwitterApi } = require('twitter-api-v2');
const client = new TwitterApi({
  appKey: process.env.TWITTER_API_KEY,
  appSecret: process.env.TWITTER_API_SECRET,
  accessToken: process.env.TWITTER_ACCESS_TOKEN,
  accessSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

(async () => {
  try {
    await client.v2.like('tweet_id_to_like');
    console.log('Tweet liked');
  } catch (error) {
    console.error('Error liking tweet:', error);
  }
})();
"
```

## Notes

- This skill uses the Twitter API v2, which has different endpoints than the older v1.1 API.
- Rate limits apply - check the Twitter API documentation for current limits.
- Always handle errors gracefully in production code.
- Consider using environment variables or a secure secrets manager for API keys.
- The Twitter API requires authentication for most endpoints.