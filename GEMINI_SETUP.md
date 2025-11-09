# Gemini Video Classifier Setup

## Prerequisites

1. Python packages are already installed:
   - `google-generativeai`
   - `python-dotenv`

## Setup Instructions

### Step 1: Get Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key" or "Get API Key"
4. Copy your API key

### Step 2: Configure API Key

1. Copy the `.env.example` file to `.env`:
   ```
   copy .env.example .env
   ```

2. Open the `.env` file and replace `your_gemini_api_key_here` with your actual API key:
   ```
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

### Step 3: Run the Classifier

Run the script:
```
python gemini_classifier.py
```

You'll be prompted to enter:
- Starting video number (default: 1)
- Ending video number (default: all videos)

The script will:
1. Upload each video to Gemini
2. Classify it into one of the 30 action classes
3. Save predictions to `gemini_predictions.csv`
4. Clean up uploaded files automatically

## Output

The script creates `gemini_predictions.csv` with columns:
- `video_id`: Video number (1-500)
- `filename`: Video filename (e.g., 001.mp4)
- `predicted_class`: Predicted action class

## 30 Action Classes

1. applying cream
2. breading or breadcrumbing
3. building cabinet
4. changing wheel
5. chopping wood
6. climbing a rope
7. contact juggling
8. crying
9. dancing charleston
10. eating ice cream
11. garbage collecting
12. laughing
13. laying bricks
14. making tea
15. playing accordion
16. playing badminton
17. playing cricket
18. playing drums
19. playing xylophone
20. pumping gas
21. punching bag
22. shoveling snow
23. spraying
24. swinging legs
25. trapezing
26. trimming trees
27. water sliding
28. waxing chest
29. waxing eyebrows
30. weaving basket

## Tips

- The script includes rate limiting (1 second delay between videos)
- Videos are automatically deleted from Gemini after classification
- You can process videos in batches by specifying start and end numbers
- If classification fails for a video, it will be marked as 'ERROR'

## Model Used

- **Model**: `gemini-1.5-flash` (optimized for video understanding)
- Supports video input and can analyze video content
