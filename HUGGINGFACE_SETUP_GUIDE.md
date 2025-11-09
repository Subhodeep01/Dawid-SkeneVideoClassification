# HUGGING FACE INFERENCE ENDPOINT - COMPLETE SETUP GUIDE

## STEP 1: Get Your Hugging Face Token

### 1.1 Create Account (if you don't have one)
- Go to: https://huggingface.co/join
- Sign up with email or GitHub

### 1.2 Generate Access Token
1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: "video-classification-api"
4. Type: Select "Read" (or "Write" if you plan to save models)
5. Click "Generate"
6. **COPY THE TOKEN** (you won't see it again!)

### 1.3 Add Token to .env File
Open your `.env` file and add:
```
HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## STEP 2: Choose Your Approach

### OPTION A: FREE Serverless API (Recommended to Start)
- **Cost**: $0
- **Speed**: 2-3 hours for 1000 videos
- **Rate Limit**: 1000 requests/day
- **Setup Time**: 5 minutes
- **Best for**: Testing, small batches

### OPTION B: Dedicated Inference Endpoint (For Fast Processing)
- **Cost**: $0.60-1.00/hour (~$1-2 total for 1000 videos)
- **Speed**: 1-2 hours for 1000 videos
- **Rate Limit**: None
- **Setup Time**: 10 minutes
- **Best for**: Production, fast batches

---

## STEP 3A: Setup for FREE Serverless API (Easy!)

### 3A.1 Install Package
Already done, but if needed:
```powershell
pip install huggingface_hub
```

### 3A.2 Edit the Script
In `huggingface_classifier.py`, keep these settings:
```python
ENDPOINT_URL = None  # Use free serverless API
USE_CUSTOM_ENDPOINT = False
```

### 3A.3 Run the Script
```powershell
python huggingface_classifier.py
```

**That's it! The free tier is ready to use.**

---

## STEP 3B: Setup for Dedicated Inference Endpoint (Fast!)

### 3B.1 Go to Hugging Face Endpoints Dashboard
- Visit: https://ui.endpoints.huggingface.co/

### 3B.2 Create New Endpoint
1. Click **"+ New Endpoint"**
2. Choose a model:
   - **Recommended**: `microsoft/xclip-base-patch32` (best for your 60 classes)
   - Alternative: `MCG-NJU/videomae-base-finetuned-kinetics` (good for actions)
   - Alternative: `facebook/timesformer-base-finetuned-k400` (Kinetics-400)

### 3B.3 Configure Endpoint Settings

**Model Repository:**
```
microsoft/xclip-base-patch32
```

**Cloud Provider:**
- Choose: AWS (recommended) or Azure

**Region:**
- Choose: US East (cheaper) or your closest region

**Instance Type:**
- For X-CLIP: **GPU [small] - 1x Nvidia T4** (~$0.60/hour) ✅ CHEAPEST
- For VideoMAE: **GPU [medium] - 1x Nvidia A10G** (~$1.00/hour)

**Advanced Configuration:**
- Min Replicas: 1
- Max Replicas: 1
- Task: "Zero-Shot Image Classification" (for X-CLIP)

### 3B.4 Create Endpoint
1. Review costs (should be ~$0.60/hour)
2. Click **"Create Endpoint"**
3. Wait 2-5 minutes for deployment
4. Status will change from "Building" → "Running"

### 3B.5 Get Your Endpoint URL
Once running, you'll see:
```
https://abc123xyz.aws.endpoints.huggingface.cloud
```
**COPY THIS URL!**

### 3B.6 Update the Script
In `huggingface_classifier.py`, change:
```python
# Replace this line
ENDPOINT_URL = None

# With your endpoint URL
ENDPOINT_URL = "https://abc123xyz.aws.endpoints.huggingface.cloud"

# Keep this as False for X-CLIP
USE_CUSTOM_ENDPOINT = False
```

### 3B.7 Run the Script
```powershell
python huggingface_classifier.py
```

### 3B.8 **IMPORTANT: Pause Endpoint When Done!**
After your 1000 videos are processed:
1. Go back to: https://ui.endpoints.huggingface.co/
2. Find your endpoint
3. Click **"Pause"** or **"Delete"**
4. This stops billing!

**If you forget to pause, you'll be charged $0.60/hour continuously!**

---

## STEP 4: Monitor Progress

The script will show:
```
[1/1000] Processing: 001.mp4
  Classifying with X-CLIP...
  Predicted: skateboarding (confidence: 0.892)

[2/1000] Processing: 002.mp4
  Classifying with X-CLIP...
  Predicted: playing cello (confidence: 0.756)
```

Results are saved incrementally to `huggingface_predictions.csv`

---

## STEP 5: Cost Estimation

### FREE Serverless API:
- **Cost**: $0
- **Time**: 2-3 hours (with rate limits)
- **Total**: **$0**

### Dedicated Endpoint (T4 GPU @ $0.60/hour):
- **Time**: 2 hours for 1000 videos
- **Cost**: $0.60/hour × 2 hours = **$1.20**
- **Total**: **~$1-2**

---

## TROUBLESHOOTING

### Issue: "Rate limit exceeded"
**Solution**: You hit the free tier limit (1000/day)
- Wait 24 hours, or
- Upgrade to PRO ($9/month), or
- Use Dedicated Endpoint

### Issue: "Token is invalid"
**Solution**: 
1. Check your token in `.env` file
2. Make sure it starts with `hf_`
3. Regenerate token at: https://huggingface.co/settings/tokens

### Issue: "Model is loading"
**Solution**: Wait 1-2 minutes for serverless models to load (cold start)

### Issue: Endpoint not found
**Solution**: 
1. Make sure endpoint is "Running" (not Paused/Building)
2. Double-check the URL in your script
3. Verify your token has access

### Issue: Low accuracy
**Solution**: 
- X-CLIP works best with clear, simple actions
- Try adding more descriptive class names
- Consider fine-tuning a VideoMAE model

---

## WHICH OPTION SHOULD YOU CHOOSE?

### Choose FREE Serverless API if:
- ✅ You have 1-2 days to process videos
- ✅ You want $0 cost
- ✅ You're testing/experimenting
- ✅ You have <1000 videos per day

### Choose Dedicated Endpoint if:
- ✅ You need results in 1-2 hours
- ✅ You have >1000 videos
- ✅ You can spend $1-2
- ✅ You want guaranteed performance

---

## NEXT STEPS

1. **Start with FREE Serverless API** to test quality
2. If accuracy is good → continue with free tier
3. If you need speed → upgrade to Dedicated Endpoint
4. Compare results with Gemini and Twelve Labs
5. Choose the best API for your final classification

---

## QUICK START CHECKLIST

- [ ] Get Hugging Face token
- [ ] Add token to `.env` file
- [ ] Install `huggingface_hub` package
- [ ] Choose: Serverless (free) or Endpoint (fast)
- [ ] Update script configuration
- [ ] Run: `python huggingface_classifier.py`
- [ ] Monitor progress
- [ ] (If using Endpoint) PAUSE endpoint when done!

---

## SUPPORT

- Hugging Face Docs: https://huggingface.co/docs/api-inference
- Endpoints Pricing: https://huggingface.co/pricing#endpoints
- Community Forum: https://discuss.huggingface.co/
