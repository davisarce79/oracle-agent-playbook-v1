const { TwitterApi } = require('twitter-api-v2');
const fs = require('fs');

async function testTweet() {
  const content = fs.readFileSync('.openclaw/credentials/x.txt', 'utf8');
  const lines = content.split('\n');
  const creds = {};
  lines.forEach(line => {
    const [key, value] = line.split('=');
    if (key && value) creds[key.trim()] = value.trim();
  });

  const client = new TwitterApi({
    appKey: creds.CONSUMER_KEY,
    appSecret: creds.CONSUMER_SECRET,
    accessToken: creds.ACCESS_TOKEN,
    accessSecret: creds.ACCESS_SECRET,
  });

  try {
    // Attempting V1.1 tweet as a fallback
    console.log('Attempting V1.1 Tweet...');
    const tweet = await client.v1.tweet('Agent Gunna is testing the V1 fallback. 🦞💨 #OpenClaw #AI');
    console.log('Tweet successful via V1.1:', tweet.id_str);
  } catch (error) {
    console.log('V1.1 Failed.');
    if (error.data) {
        console.log('Error Data:', JSON.stringify(error.data, null, 2));
    }
  }
}

testTweet();
