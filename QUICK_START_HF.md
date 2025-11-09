# 🚀 QUICK START GUIDE - Hugging Face Video Classification

## ⚡ FASTEST PATH (FREE - Start Here!)

### Step 1: Get Token (2 minutes)
1. Go to: https://huggingface.co/settings/tokens
2. Click "New token" → Name it → Click "Generate"
3. Copy the token (starts with `hf_`)

### Step 2: Add to .env (1 minute)
Open `.env` and add:
```
HUGGINGFACE_TOKEN=hf_your_token_here
```

### Step 3: Run Script (1 minute)
```powershell
python huggingface_classifier.py
```

**DONE! It's processing your 1000 videos for FREE!**

---

## 💰 COST COMPARISON

| Option | Time | Cost | Setup |
|--------|------|------|-------|
| **FREE Serverless** | 2-3 hours | **$0** | 5 min |
| **Dedicated Endpoint** | 1-2 hours | **$1-2** | 10 min |

---

## 🚀 UPGRADE TO FAST (If Needed)

### Only if you need it done in 1-2 hours:

1. **Go to**: https://ui.endpoints.huggingface.co/
2. **Click**: "+ New Endpoint"
3. **Model**: `microsoft/xclip-base-patch32`
4. **GPU**: T4 (small) - $0.60/hour
5. **Create** and wait 2-5 minutes
6. **Copy URL**: `https://xxx.aws.endpoints.huggingface.cloud`
7. **Update script**:
   ```python
   ENDPOINT_URL = "https://xxx.aws.endpoints.huggingface.cloud"
   ```
8. **Run**: `python huggingface_classifier.py`
9. **⚠️ PAUSE endpoint when done!** (or it keeps charging)

---

## 📊 EXPECTED OUTPUT

```
[1/1000] Processing: 001.mp4
  Classifying with X-CLIP...
  Predicted: skateboarding (confidence: 0.892)

[2/1000] Processing: 002.mp4
  Classifying with X-CLIP...
  Predicted: playing trombone (confidence: 0.756)
```

Results → `huggingface_predictions.csv`

---

## ❓ TROUBLESHOOTING

**"Rate limit exceeded"**
→ Wait 24 hours OR use Dedicated Endpoint

**"Invalid token"**
→ Check token in `.env` starts with `hf_`

**"Model is loading"**
→ Wait 1-2 minutes (first request is slow)

---

## 🎯 RECOMMENDATIONS

1. **Start with FREE** - Test quality first
2. **Compare** - See how it performs vs Gemini/Twelve Labs
3. **Upgrade if needed** - Only if you need speed

---

## 📁 FILES CREATED

- ✅ `huggingface_classifier.py` - Main script (ready to run!)
- ✅ `HUGGINGFACE_SETUP_GUIDE.md` - Full detailed guide
- ✅ This file - Quick reference

---

## 🏁 YOU'RE READY!

Just run:
```powershell
python huggingface_classifier.py
```

Good luck! 🎉
