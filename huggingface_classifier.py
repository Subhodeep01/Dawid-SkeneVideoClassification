"""
Video Classification using Hugging Face Inference Endpoint
Supports both Serverless API (free) and Dedicated Endpoints (paid)
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import time
import base64
from huggingface_hub import InferenceClient
import cv2

# Load environment variables
load_dotenv()

# Configuration
SAMPLED_VIDEOS_DIR = "sampled_videos"
OUTPUT_CSV = "huggingface_predictions.csv"

# Your 60 classes from metadata.txt
CLASSES = [
    "abseiling",
    "applauding",
    "applying cream",
    "baby waking up",
    "balloon blowing",
    "bandaging",
    "bench pressing",
    "blasting sand",
    "canoeing or kayaking",
    "capoeira",
    "changing oil",
    "changing wheel",
    "cooking on campfire",
    "dancing ballet",
    "dancing charleston",
    "dancing macarena",
    "doing nails",
    "driving car",
    "dunking basketball",
    "feeding goats",
    "fixing hair",
    "frying vegetables",
    "hurdling",
    "javelin throw",
    "jogging",
    "juggling soccer ball",
    "laughing",
    "laying bricks",
    "lunge",
    "making snowman",
    "moving furniture",
    "plastering",
    "playing badminton",
    "playing chess",
    "playing didgeridoo",
    "playing keyboard",
    "playing trombone",
    "playing xylophone",
    "pole vault",
    "pumping fist",
    "pushing wheelchair",
    "riding elephant",
    "riding mountain bike",
    "riding unicycle",
    "ripping paper",
    "sharpening knives",
    "shuffling cards",
    "sign language interpreting",
    "skateboarding",
    "snatch weight lifting",
    "snorkeling",
    "spray painting",
    "squat",
    "swinging legs",
    "tango dancing",
    "trimming or shaving beard",
    "tying bow tie",
    "unloading truck",
    "vault",
    "waiting in line"
]

def setup_huggingface_client(endpoint_url=None):
    """
    Setup Hugging Face Inference Client
    
    Args:
        endpoint_url: URL of your dedicated endpoint (e.g., "https://xxx.aws.endpoints.huggingface.cloud")
                     If None, uses serverless API (free tier)
    """
    hf_token = os.getenv('HUGGINGFACE_TOKEN')
    
    if not hf_token:
        raise ValueError(
            "HUGGINGFACE_TOKEN not found in .env file!\n"
            "Get your token from: https://huggingface.co/settings/tokens"
        )
    
    if endpoint_url:
        print(f"Using Dedicated Endpoint: {endpoint_url}")
        client = InferenceClient(model=endpoint_url, token=hf_token)
    else:
        print("Using Serverless API (Free Tier)")
        # Default to X-CLIP for zero-shot video classification
        client = InferenceClient(model="microsoft/xclip-base-patch32", token=hf_token)
    
    return client

def extract_video_frames(video_path, num_frames=8):
    """Extract evenly spaced frames from video"""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames == 0:
        raise ValueError(f"Could not read video: {video_path}")
    
    # Get evenly spaced frame indices
    frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]
    
    frames = []
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
    
    cap.release()
    return frames

def classify_video_xclip(client, video_path, classes, max_retries=3):
    """
    Classify video using X-CLIP (zero-shot classification)
    Works with both serverless and dedicated endpoints
    """
    print(f"  Classifying with X-CLIP...")
    
    for attempt in range(max_retries):
        try:
            # Read video file as bytes
            with open(video_path, 'rb') as f:
                video_bytes = f.read()
            
            # Use X-CLIP for zero-shot classification
            result = client.zero_shot_image_classification(
                image=video_bytes,
                labels=classes
            )
            
            # Get top prediction
            if result and len(result) > 0:
                predicted_class = result[0]['label']
                confidence = result[0]['score']
                print(f"  Predicted: {predicted_class} (confidence: {confidence:.3f})")
                return predicted_class, confidence
            else:
                raise ValueError("No prediction returned")
                
        except Exception as e:
            error_msg = str(e)
            
            # Check for rate limit errors
            if '429' in error_msg or 'rate limit' in error_msg.lower():
                wait_time = 60 * (attempt + 1)  # Exponential backoff
                print(f"  Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            
            # Check for network errors
            if attempt < max_retries - 1 and any(err in error_msg.lower() for err in ['timeout', 'connection', 'network']):
                print(f"  Network error (attempt {attempt + 1}/{max_retries}): {error_msg}")
                print(f"  Retrying in 10 seconds...")
                time.sleep(10)
                continue
            
            # Other errors
            print(f"  ERROR: {error_msg}")
            raise e
    
    raise Exception("Max retries exceeded")

def classify_video_custom(client, video_path, classes, max_retries=3):
    """
    Classify video using custom endpoint (VideoMAE, TimeSformer, etc.)
    This is for dedicated endpoints with specific models
    """
    print(f"  Classifying with custom model...")
    
    for attempt in range(max_retries):
        try:
            # Read video file
            with open(video_path, 'rb') as f:
                video_bytes = f.read()
            
            # Encode to base64 for API
            video_b64 = base64.b64encode(video_bytes).decode('utf-8')
            
            # Call endpoint with custom payload
            response = client.post(
                json={
                    "inputs": video_b64,
                    "parameters": {
                        "candidate_labels": classes,
                        "top_k": 1
                    }
                }
            )
            
            # Parse response (format depends on your model)
            if isinstance(response, list) and len(response) > 0:
                predicted_class = response[0]['label']
                confidence = response[0].get('score', 0.0)
                print(f"  Predicted: {predicted_class} (confidence: {confidence:.3f})")
                return predicted_class, confidence
            else:
                raise ValueError(f"Unexpected response format: {response}")
                
        except Exception as e:
            error_msg = str(e)
            
            if attempt < max_retries - 1:
                print(f"  Error (attempt {attempt + 1}/{max_retries}): {error_msg}")
                time.sleep(10)
                continue
            
            print(f"  ERROR: {error_msg}")
            raise e
    
    raise Exception("Max retries exceeded")

def classify_all_videos(client, video_dir, classes, output_csv, use_custom_endpoint=False, start_from=1, end_at=None):
    """Classify all videos in the directory"""
    video_files = sorted([f for f in os.listdir(video_dir) if f.endswith('.mp4')])
    
    if end_at:
        video_files = video_files[start_from-1:end_at]
    else:
        video_files = video_files[start_from-1:]
    
    total_videos = len(video_files)
    
    print("=" * 60)
    print(f"VIDEO CLASSIFICATION WITH HUGGING FACE")
    print("=" * 60)
    print(f"Total videos to classify: {total_videos}")
    print(f"Number of classes: {len(classes)}")
    print(f"Results will be saved incrementally to: {output_csv}")
    print("-" * 60)
    
    results = []
    
    # Load existing results if resuming
    if os.path.exists(output_csv):
        existing_df = pd.read_csv(output_csv)
        results = existing_df.to_dict('records')
        processed_files = set(existing_df['filename'].values)
        print(f"Resuming: {len(results)} videos already processed")
    else:
        processed_files = set()
    
    # Process videos
    for idx, video_file in enumerate(video_files, 1):
        if video_file in processed_files:
            print(f"[{idx}/{total_videos}] Skipping (already processed): {video_file}")
            continue
        
        print(f"\n[{idx}/{total_videos}] Processing: {video_file}")
        
        video_path = os.path.join(video_dir, video_file)
        video_id = int(Path(video_file).stem)
        
        try:
            # Classify video
            if use_custom_endpoint:
                predicted_class, confidence = classify_video_custom(client, video_path, classes)
            else:
                predicted_class, confidence = classify_video_xclip(client, video_path, classes)
            
            # Store result
            results.append({
                'video_id': video_id,
                'filename': video_file,
                'predicted_class': predicted_class,
                'confidence': confidence
            })
            
        except Exception as e:
            print(f"  ERROR: {e}")
            # Store error
            results.append({
                'video_id': video_id,
                'filename': video_file,
                'predicted_class': f"ERROR: {str(e)}",
                'confidence': 0.0
            })
        
        # Save incrementally every video
        df = pd.DataFrame(results)
        df.to_csv(output_csv, index=False)
        
        # Small delay to avoid rate limits (for free tier)
        if not use_custom_endpoint:
            time.sleep(1)  # 1 second delay between videos
    
    print("\n" + "=" * 60)
    print(f"Classification complete!")
    print(f"Results saved to: {output_csv}")
    print(f"Total videos processed: {len(results)}")
    print("=" * 60)

def main():
    """Main function"""
    
    # ========================================
    # CONFIGURATION - EDIT THESE
    # ========================================
    
    # Option 1: Use FREE Serverless API (X-CLIP)
    ENDPOINT_URL = None  # Keep as None for free tier
    USE_CUSTOM_ENDPOINT = False
    
    # Option 2: Use Dedicated Endpoint (uncomment and add your URL)
    # ENDPOINT_URL = "https://YOUR-ENDPOINT-ID.aws.endpoints.huggingface.cloud"
    # USE_CUSTOM_ENDPOINT = True  # Set to True if using VideoMAE/TimeSformer
    
    # Processing range (optional)
    START_FROM = 1      # Start from video number
    END_AT = None       # Process all videos (or set a number to limit)
    
    # ========================================
    # END CONFIGURATION
    # ========================================
    
    # Setup client
    client = setup_huggingface_client(ENDPOINT_URL)
    
    # Classify videos
    classify_all_videos(
        client=client,
        video_dir=SAMPLED_VIDEOS_DIR,
        classes=CLASSES,
        output_csv=OUTPUT_CSV,
        use_custom_endpoint=USE_CUSTOM_ENDPOINT,
        start_from=START_FROM,
        end_at=END_AT
    )

if __name__ == "__main__":
    main()
