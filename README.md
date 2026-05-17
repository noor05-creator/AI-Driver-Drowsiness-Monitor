<div align="center">

# 🚗 Driver Drowsiness Monitor
### Real-time drowsiness detection using OpenCV, dlib, and Deep Learning

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-green?style=flat-square&logo=opencv)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange?style=flat-square&logo=tensorflow)
![Pygame](https://img.shields.io/badge/Pygame-2.5-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

</div>

---

## 📌 Overview

Driver Drowsiness Monitor is a real-time AI-powered safety system that detects driver fatigue through webcam feed analysis. It combines geometric eye tracking (Eye Aspect Ratio) with a trained Convolutional Neural Network to accurately identify drowsiness and trigger an audio alert before an accident can occur.

This project was developed as a final exam submission for Semester 5, covering Python data science libraries, OpenCV, deep learning, data visualization, an AI-based game, and version control with Git.

---

## 🎯 Features

- Real-time face and eye detection using dlib's 68-point facial landmark model
- Eye Aspect Ratio (EAR) calculation for geometric drowsiness detection
- CNN trained on the MRL Eye Dataset for learned eye state classification
- Dual-confirmation alert system (EAR + CNN must both agree)
- Audio alarm that triggers on drowsy confirmation and stops on recovery
- Professional HUD overlay showing live EAR, CNN confidence, and session timer
- Session event logging to CSV using Pandas
- Analytics dashboard with 3 Matplotlib charts generated from session data
- Pygame reaction-time mini game with scoring and performance analysis
- Full Git workflow with branching, PRs, and documented contributions

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.9+ |
| Computer Vision | OpenCV 4.9, dlib 19.24 |
| Deep Learning | TensorFlow 2.15, Keras |
| Data Analysis | NumPy, Pandas |
| Visualization | Matplotlib |
| Game | Pygame |
| Version Control | Git, GitHub |

---

## 📁 Project Structure
```
drowsiness_monitor/
├── main.py                   # Entry point — live detection pipeline
├── detector.py               # EAR calculation and face/eye detection
├── model_train.py            # CNN architecture and training
├── analytics.py              # Pandas analysis and Matplotlib dashboard
├── game.py                   # Pygame reaction time mini-game
│
├── model/
│   └── drowsiness_cnn.h5    # Saved trained model (generated after training)
│
├── data/
│   ├── open/                 # Training images — eyes open
│   └── closed/               # Training images — eyes closed
│
├── logs/
│   ├── session_log.csv       # Alert events from live sessions
│   └── game_results.csv      # Reaction game scores
│
├── assets/
│   ├── alarm.wav             # Audio alert file
│   ├── training_curves.png   # Generated after model training
│   ├── session_report.png    # Generated after running analytics
│   └── game_analysis.png     # Generated after game analysis
│
├── CONTRIBUTING.md
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### Prerequisites
- Python 3.9 or 3.10
- A working webcam
- Git

### Step 1 — Clone the repository
```bash
git clone https://github.com/noor05-creator/AI-Driver-Drowsiness-Monitor.git
cd drowsiness-monitor
```

### Step 2 — Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```


### Step 4 — Download dlib landmark predictor
Download `shape_predictor_68_face_landmarks.dat` from:
https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2

Download the pre-trained 68-point facial landmark model:

1. Go to this URL and download the file:
   https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2

2. The file is compressed (.bz2 format). Extract it using:
   - Windows: Right-click → Extract All
   - Linux/Mac: run `bzip2 -d shape_predictor_68_face_landmarks.dat.bz2`

3. After extraction you will have:
   `shape_predictor_68_face_landmarks.dat` (95MB)

4. Place this file in the root project folder:
AI-Driver-Drowsiness-Monitor/
└── shape_predictor_68_face_landmarks.dat
> ⚠️ This file is 95MB and is listed in .gitignore.
> Never commit it to the repository.



### Step 5 — Download the dataset
## Dataset

This project uses the MRL Eye Dataset for training the CNN model.

| Class | Images |
|---|---|
| Eyes Open | [24000] |
| Eyes Closed | [24000] |
| Total | [48000] |

### Download instructions
1. Go to https://www.kaggle.com/datasets/kutaykutlu/drowsiness-detection
2. Download and extract the zip file
3. Place open eye images in `/data/open/`
4. Place closed eye images in `/data/closed/`
5. Run `python preprocess.py` to resize all images to 24x24 grayscale

Note: Images are not committed to this repository.
Download the dataset manually before running any scripts.

---

## 🚀 How to Run

### Train the model (run once)
```bash
python model_train.py
```
This saves the trained model to `/model/drowsiness_cnn.h5` and training curves to `/assets/training_curves.png`.

### Run the live drowsiness detector
```bash
python main.py
```
Press `Q` to quit. Session events are logged to `/logs/session_log.csv`.

### Generate analytics dashboard
```bash
python analytics.py
```
Reads session log and saves a 3-chart dashboard to `/assets/session_report.png`.

### Run the reaction time game
```bash
python game.py
```
10 trials. Press `SPACE` when the red circle appears. Results saved to `/logs/game_results.csv`.

---

## 📊 Model Performance

The CNN was trained on the MRL Eye Dataset for 20 epochs.

| Metric | Value |
|---|---|
| Training Accuracy | ~99.49% |
| Validation Accuracy | ~91.45% |
| EAR Threshold | 0.25 |
| Consecutive Frame Threshold | 20 frames |

![Training Curves](assets/training_curves.png)

---

## 👥 Team Members

| Name | Role | Issues |
|---|---|---|
| [Your Name] | Team Lead — Integration & Setup | #1 #2 #8 #10 #14 #16 |
| [Member 2] | Detection & Model | #3 #4 #5 #6 #7 |
| [Member 3] | Analytics & Game | #9 #11 #12 #13 #15 |

---

## 📄 License

This project is licensed under the MIT License.

MIT License
Copyright (c) 2026 [Your Team Name]
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
