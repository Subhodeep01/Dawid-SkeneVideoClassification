# Twelve Labs Video Classifier Setup

## About Twelve Labs

Twelve Labs is a specialized video understanding API that excels at action recognition and video analysis. It uses the Marengo 2.6 model which is optimized for:
- Visual understanding
- Action detection
- Text in video analysis
- Conversation/audio analysis

## Prerequisites

- Python package `twelvelabs` is already installed
- `python-dotenv` is already installed

## Setup Instructions

### Step 1: Get Twelve Labs API Key

1. Go to [Twelve Labs Playground](https://playground.twelvelabs.io/)
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy your API key

### Step 2: Configure API Key

Add your Twelve Labs API key to the `.env` file:

```bash
TWELVELABS_API_KEY=tlk_XXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 3: Run the Classifier

```bash
python twelvelabs_classifier.py
```

You'll be prompted to enter:
- Starting video number (default: 1)
- Ending video number (default: all videos)

## How It Works

1. **Index Creation**: The script creates or uses an existing index called `video_classification_index`
2. **Video Upload**: Each video is uploaded to Twelve Labs
3. **Classification**: Uses the Generate API to classify the video into one of 30 action classes
4. **Incremental Saving**: Results are saved after each video to prevent data loss
5. **Video Tracking**: Each result includes the Twelve Labs video ID for reference

## Output

The script creates `twelvelabs_predictions.csv` with columns:
- `video_id`: Video number (1-500)
- `filename`: Video filename (e.g., 001.mp4)
- `predicted_class`: Predicted action class
- `twelvelabs_video_id`: Twelve Labs internal video ID

## 30 Action Classes

1. assembling computer
2. beatboxing
3. climbing ladder
4. drumming fingers
5. long jump
6. making pizza
7. marching
8. news anchoring
9. parasailing
10. picking fruit
11. playing cello
12. playing keyboard
13. presenting weather forecast
14. riding or walking with horse
15. riding scooter
16. riding unicycle
17. shaking hands
18. shaving legs
19. shining shoes
20. sign language interpreting
21. situp
22. skateboarding
23. snowmobiling
24. tickling
25. tobogganing
26. trapezing
27. tying knot (not on a tie)
28. using computer
29. using remote controller (not gaming)
30. water sliding

## Features

✅ **Incremental saving** - Results saved after each video
✅ **Resume capability** - Can restart from any video number
✅ **Error handling** - Handles quota limits, rate limits, and errors gracefully
✅ **Progress tracking** - Shows detailed progress for each video
✅ **Video indexing** - All videos are stored in a Twelve Labs index for future queries

## Key Differences from Gemini

| Feature | Twelve Labs | Gemini |
|---------|-------------|--------|
| **Video Processing** | Native, full video analysis | Frame-based sampling |
| **Specialization** | Purpose-built for video | General multimodal AI |
| **Indexing** | Videos stored for reuse | One-time analysis |
| **Multimodal** | Visual + Audio + Text | Visual + Text |
| **Pricing** | Higher, but more features | Lower, simpler |

## Tips

- Videos are stored in the index - you can query them later
- The `marengo2.6` engine is used for best video understanding
- Upload time depends on video length and size
- Rate limiting is built-in (2 second delay between videos)
- You can delete the index later to free up storage

## Troubleshooting

**Index already exists**: The script will reuse it - no problem!

**Upload fails**: Check video format (MP4 is recommended)

**Rate limit hit**: The script will save progress and tell you where to resume

**Quota exhausted**: Results are saved, resume later from the suggested video number

## Cost Considerations

Twelve Labs pricing is based on:
- Video indexing (storage)
- API requests (classification)

Check [Twelve Labs Pricing](https://www.twelvelabs.io/pricing) for current rates.

## Model Used

- **Engine**: `marengo2.6`
- **Features**: Visual, Conversation, Text in Video
- **Optimized for**: Action recognition, video understanding
