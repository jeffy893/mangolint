# Mangolint Operating Modes

Mangolint can run in two modes: **Mock Mode** (local agent) or **Bedrock Mode** (AWS AI).

## 🎭 Mock Mode (Current - Local Agent)

### What It Is:
- Local Python agent with predefined responses
- No external API calls
- No AWS credentials needed
- Instant responses

### How It Works:
- `linter_mock.py` contains hardcoded responses for 10 ingredients
- Pattern matching detects ingredients in text
- Returns pre-written cultural insights
- Perfect for demos, testing, and development

### Supported Ingredients:
1. mango - 4 indigenous synonyms (Manga, Aam, Māṅgāy, Mangga)
2. turmeric - Ayurvedic context (Haldi, Manjal, Pasupu)
3. coconut - Young vs mature (Nariyal, Thengai, Kelapa)
4. ginger - Fresh vs dried (Adrak, Inji, Shoga)
5. cardamom - Green vs black (Elaichi, Elakkai, Hel)
6. vanilla - Aztec origins (Tlilxochitl, Vainilla)
7. corn - Mesoamerican sacred crop (Maíz, Elote, Choclo)
8. cinnamon - Ceylon vs Cassia (Dalchini, Kurundu)
9. pepper - King of spices (Kali Mirch, Milagu)
10. honey - Floral varieties (Shahad, Miel)

### Pros:
✅ No AWS account needed
✅ No API costs
✅ Instant responses
✅ Works offline
✅ Perfect for demos
✅ Predictable results

### Cons:
❌ Limited to 10 ingredients
❌ No AI-generated insights
❌ Can't analyze new ingredients
❌ Static responses

### Enable Mock Mode:
```env
# In .env file
USE_MOCK_LINTER=true
```

---

## 🤖 Bedrock Mode (AWS AI)

### What It Is:
- Real AI using Amazon Bedrock's Claude 3 Sonnet
- Dynamic analysis of any natural ingredient
- AI-powered cultural insights
- Unlimited ingredient coverage

### How It Works:
- `linter.py` connects to AWS Bedrock API
- Sends text to Claude 3 with specialized prompt
- AI acts as "Indigenous Linguist and Brand Anthropologist"
- Returns JSON with indigenous synonyms, context, and insights
- Analyzes ANY natural ingredient, not just predefined ones

### AI Persona:
The AI operates as an expert in:
- Traditional ecological knowledge
- Ethnobotany and cultural food systems
- Linguistic anthropology
- Brand storytelling through cultural authenticity

### Capabilities:
- Identifies ANY natural ingredient (fruits, herbs, spices, plants, minerals)
- Generates indigenous synonyms from global cultures
- Provides ripeness/preparation context
- Explains cultural significance
- Offers brand authenticity insights
- Suggests traditional uses

### Pros:
✅ Unlimited ingredient coverage
✅ AI-generated cultural insights
✅ Analyzes new/rare ingredients
✅ Deep cultural context
✅ Adapts to any text
✅ Production-ready

### Cons:
❌ Requires AWS account
❌ Requires Bedrock access
❌ API costs (~$0.003 per request)
❌ 2-5 second response time
❌ Needs valid credentials

### Enable Bedrock Mode:

1. **Configure AWS Credentials**
   ```bash
   # Ensure ~/.aws/credentials has valid credentials
   [default]
   aws_access_key_id = YOUR_KEY
   aws_secret_access_key = YOUR_SECRET
   ```

2. **Enable Bedrock Access**
   - Log into AWS Console
   - Navigate to Amazon Bedrock
   - Request access to Claude 3 Sonnet model
   - Wait for approval (usually instant)

3. **Update .env**
   ```env
   USE_MOCK_LINTER=false
   BEDROCK_REGION=us-east-1
   ```

4. **Restart App**
   ```bash
   python3.10 app.py
   ```

5. **Verify**
   - Should see: "✅ Using Real Bedrock Linter"
   - Try any ingredient (not just the 10 predefined ones)

---

## 🔄 Switching Between Modes

### Current Mode: Mock (Local Agent)
To switch to Bedrock:
1. Edit `.env`: `USE_MOCK_LINTER=false`
2. Ensure AWS credentials are valid
3. Restart: `python3.10 app.py`

### To Switch Back to Mock:
1. Edit `.env`: `USE_MOCK_LINTER=true`
2. Restart: `python3.10 app.py`

---

## 📊 Comparison

| Feature | Mock Mode | Bedrock Mode |
|---------|-----------|--------------|
| **Cost** | Free | ~$0.003/request |
| **Speed** | Instant | 2-5 seconds |
| **Ingredients** | 10 predefined | Unlimited |
| **AI Insights** | Static | Dynamic |
| **AWS Account** | Not needed | Required |
| **Offline** | Yes | No |
| **Production** | Demo only | Production-ready |
| **Customization** | Edit Python | AI adapts |

---

## 🎯 Which Mode to Use?

### Use Mock Mode For:
- Initial testing and demos
- Development without AWS
- Showing the interface
- Cost-free exploration
- Offline work
- Known ingredients only

### Use Bedrock Mode For:
- Production deployment
- Analyzing any ingredient
- Deep cultural insights
- Brand research
- Real-world applications
- Unlimited coverage

---

## 🔧 Troubleshooting

### Mock Mode Not Working?
- Check `.env` has `USE_MOCK_LINTER=true`
- Verify ingredient is in supported list
- Check console for errors

### Bedrock Mode Failing?
- Verify AWS credentials: `aws sts get-caller-identity`
- Check Bedrock access in AWS Console
- Ensure Claude 3 model is enabled
- Check region is `us-east-1`
- Review app logs for specific errors

### Authentication Errors?
- AWS credentials may be expired
- Use `aws configure` to update
- Or edit `~/.aws/credentials` directly
- Ensure IAM user has Bedrock permissions

---

## 💡 Recommendation

**For Development/Demo**: Use Mock Mode (current setup)
**For Production**: Switch to Bedrock Mode with valid credentials

The app automatically falls back to Mock Mode if Bedrock credentials fail, so you always have a working demo!
