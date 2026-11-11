# GreenCure AI: Plant Disease Detection and Treatment Advisor

GreenCure AI is a web app that detects plant leaf diseases from a photo. Users upload a leaf image or capture one with their device camera. A MobileNetV2 deep learning model classifies it, and the app shows the diagnosis, a confidence score and a treatment and prevention plan.

## Features

- Upload a leaf image or capture one with the device camera
- Diagnosis with confidence score and top 3 predictions
- Low-confidence warning: below 85% confidence the app asks for a clearer photo and shows no treatment advice
- Treatment plan (about, treatment, prevention) for all 38 classes. This is general guidance only.
- Plant Care Blog with live Wikipedia articles and search
- Leaf Hopper mini game
- Responsive layout for mobile, tablet and desktop

## Model and Results

| Item | Value |
|---|---|
| Dataset | PlantVillage (color images), 38 classes, 54,305 images |
| Split | 80/10/10 stratified: 43,444 train, 5,430 validation, 5,431 test |
| Architecture | MobileNetV2 (ImageNet pretrained), custom head Dropout(0.2) + Linear(1280 to 38) |
| Training | 3 epochs on the new head (lr 1e-3), then 14 epochs fine-tuning the full network (lr 1e-4) |
| Loss / Optimizer | Cross-Entropy / Adam, weight decay 1e-4 |
| Hardware | Kaggle notebook, Tesla T4 GPU |
| Test accuracy | 99.45% |
| Macro F1 / Weighted F1 | 0.9904 / 0.9945 |

## Supported Plants

Apple, Blueberry, Cherry, Corn (maize), Grape, Orange, Peach, Pepper (bell), Potato, Raspberry, Soybean, Squash, Strawberry, Tomato.

## Tech Stack

- **Model:** Python, PyTorch, torchvision
- **Backend:** FastAPI, Uvicorn
- **Frontend:** HTML, CSS, JavaScript (Fetch API)
- **Training environment:** Kaggle notebook

## Project Structure

```
plant-disease-app/
├── backend/
│   ├── main.py            # FastAPI app and /predict endpoint
│   ├── model_utils.py     # model loading and prediction
│   └── treatments.json    # treatment info for all 38 classes
├── frontend/
│   ├── index.html         # scan and detect page
│   ├── blog.html          # plant care blog
│   ├── game.html          # mini game
│   ├── layout.js          # shared header and footer
│   └── style.css
├── model/
│   ├── best_model.pt      # trained weights
│   └── class_names.json
└── requirements.txt
```

## Run Locally

```powershell
git clone https://github.com/Urvi-18/greencure-ai.git
cd greencure-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Then open http://localhost:8000/app/ in your browser. The API documentation is at http://localhost:8000/docs.

## API

`POST /predict` accepts a JPEG or PNG image (max 5 MB) as multipart form data in the field `file`. The response contains: `plant`, `condition`, `confidence`, `is_confident`, `message`, `is_healthy`, `treatment` and `top_3`.

## Limitations

- Only the 14 plants listed above are supported. Other plants get forced into the nearest known class.
- The model has no "not a plant" class, so non-leaf images can still receive a guess. The 85% confidence threshold filters many but not all of these.
- PlantVillage contains lab-style photos, so accuracy on cluttered field photos is expected to be lower. This was not tested.
- Treatment text is general guidance. For serious cases, consult a local agriculture expert.

## Acknowledgements

- PlantVillage dataset (Kaggle upload by abdallahalidev)
- MobileNetV2 ImageNet weights from torchvision
- Blog articles and images come from Wikipedia under CC BY-SA

## Authors

- Urvi Pal: [GitHub](https://github.com/Urvi-18) | [LinkedIn](https://www.linkedin.com/in/urvipal18)
- Vindhya Raj: [GitHub](https://github.com/Vindhya110603) | [LinkedIn](https://www.linkedin.com/in/vindhya-raj-b4b400301)