# Video Classification with LLM APIs

This project implements video classification using multiple Large Language Model APIs, comparing their performance on action recognition tasks.

## Overview

Classifies 1000 videos across 60 action classes using:
- **Gemini API** (Google's multimodal LLM)
- **Twelve Labs API** (Specialized video understanding)
- **Hugging Face Inference API** (Open-source models)

## Dataset

- **Total Videos**: 1000 videos
- **Number of Classes**: 60 action classes
- **Source**: Kinetics-400 dataset
- **Resolution**: Upscaled to minimum 360x360 for API compatibility

### Action Classes

The 60 classes include: abseiling, applauding, applying cream, baby waking up, balloon blowing, bandaging, bench pressing, blasting sand, canoeing or kayaking, capoeira, changing oil, changing wheel, cooking on campfire, dancing ballet, dancing charleston, dancing macarena, doing nails, driving car, dunking basketball, feeding goats, fixing hair, frying vegetables, hurdling, javelin throw, jogging, juggling soccer ball, laughing, laying bricks, lunge, making snowman, moving furniture, plastering, playing badminton, playing chess, playing didgeridoo, playing keyboard, playing trombone, playing xylophone, pole vault, pumping fist, pushing wheelchair, riding elephant, riding mountain bike, riding unicycle, ripping paper, sharpening knives, shuffling cards, sign language interpreting, skateboarding, snatch weight lifting, snorkeling, spray painting, squat, swinging legs, tango dancing, trimming or shaving beard, tying bow tie, unloading truck, vault, waiting in line.

## Project Structure

```
DSforVidClassify/
├── dataset.py                    # FiftyOne dataset download script
├── prepare_dataset.py            # Select videos from Kinetics dataset
├── sample_videos.py              # Random sampling and anonymization
├── create_metadata.py            # Generate metadata files
├── upscale_videos.py             # Upscale low-resolution videos
├── gemini_classifier.py          # Gemini API classification
├── twelvelabs_classifier.py      # Twelve Labs API classification
├── huggingface_classifier.py     # Hugging Face API classification
├── metadata.txt                  # Dataset metadata
├── HUGGINGFACE_SETUP_GUIDE.md    # Detailed HF setup guide
├── QUICK_START_HF.md             # Quick reference for HF
└── .env                          # API keys (NOT in git)
```

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd DSforVidClassify
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies

```bash
pip install google-generativeai twelvelabs huggingface_hub opencv-python pandas python-dotenv fiftyone
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
TWELVELABS_API_KEY=your_twelvelabs_api_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here
```

**Get API Keys:**
- **Gemini**: https://aistudio.google.com/apikey
- **Twelve Labs**: https://playground.twelvelabs.io/
- **Hugging Face**: https://huggingface.co/settings/tokens

## Usage

### Prepare Dataset

```bash
# 1. Download videos from Kinetics (optional - requires FiftyOne)
python dataset.py

# 2. Select videos from local Kinetics dataset
python prepare_dataset.py

# 3. Sample and anonymize videos
python sample_videos.py

# 4. Upscale low-resolution videos
python upscale_videos.py

# 5. Generate metadata
python create_metadata.py
```

### Run Classification

#### Gemini API
```bash
python gemini_classifier.py
```
- **Cost**: ~$0.002-0.01 per video
- **Speed**: ~3-5 seconds per video
- **Best for**: Cost-effective, good accuracy

#### Twelve Labs API
```bash
python twelvelabs_classifier.py
```
- **Cost**: Variable (enterprise pricing)
- **Speed**: ~10-15 seconds per video
- **Best for**: Best accuracy, multimodal understanding

#### Hugging Face API
```bash
python huggingface_classifier.py
```
- **Cost**: Free tier available, ~$1-2 for dedicated endpoint
- **Speed**: Free tier: 2-3 hours | Endpoint: 1-2 hours
- **Best for**: Budget-conscious, open-source

See `HUGGINGFACE_SETUP_GUIDE.md` for detailed HF setup instructions.

## Features

- ✅ **Incremental Saving**: Results saved after each video (can resume if interrupted)
- ✅ **Error Handling**: Graceful handling of API errors and rate limits
- ✅ **Multiple APIs**: Compare performance across different models
- ✅ **Resume Support**: Continue from where you left off
- ✅ **Video Upscaling**: Automatic upscaling for API requirements
- ✅ **Anonymization**: Random filename generation for privacy

## Results

Classification results are saved as CSV files:
- `gemini_predictions.csv`
- `twelvelabs_predictions.csv`
- `huggingface_predictions.csv`

Each CSV contains:
- `video_id`: Numeric identifier
- `filename`: Original filename
- `predicted_class`: Predicted action class
- `confidence`: Prediction confidence (if available)

## API Comparison

| API | Cost/Video | Speed | Accuracy | Native Video | Audio Support |
|-----|-----------|-------|----------|--------------|---------------|
| **Gemini Flash** | $0.002-0.01 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ✅ |
| **Twelve Labs** | $$$ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ |
| **Hugging Face** | Free-$ | ⭐⭐⭐ | ⭐⭐⭐ | ✅ | ⚠️ |

## Requirements

- Python 3.9+
- FFmpeg (for video upscaling)
- Sufficient disk space for videos (~5-10GB)
- API keys for the services you want to use

## License

This project is for research and educational purposes.

## Acknowledgments

- Dataset: Kinetics-400
- APIs: Google Gemini, Twelve Labs, Hugging Face
- Framework: FiftyOne for dataset management
