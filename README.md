# CAPTCHA Detection using Deep Learning

This project aims to detect and recognize CAPTCHA images using deep learning techniques.

## About the Project

Breaking human interaction proofs are pure recognition tasks which can be broken down using machine learning. The complicated Human Interaction proofs (HIPs) can use a combination of segmentation and recognition task. Breaking Human Interaction proofs (HIPs) is an important prerequisite to actualize natural human-computer interaction where CAPTCHA is an integral part of artificial intelligence.

This project uses deep learning techniques to automatically detect and recognize the characters in CAPTCHA images. The model is trained on a dataset of CAPTCHA images and is able to achieve high accuracy in recognizing the characters in unseen images.

## Problems and Weakness of Current System

Recognizing CAPTCHAs generated using the CAPTCHA library in Python is a challenging task for machine learning models. While the current system can achieve high accuracy in recognizing 5-character CAPTCHAs with an image size of 100x120, there are still some problems and weaknesses. These include the inability to recognize CAPTCHAs generated using other libraries or software, difficulty in handling variations in CAPTCHA designs, and susceptibility to attacks by adversaries. Addressing these issues will require further research and development in CAPTCHA recognition.

## Requirements

To run this project, you will need the following:

- Python 3.6 or later
- TensorFlow 2.4 or later
- OpenCV 4.0 or later
- Numpy

## Installation

1. Clone the repository: 

```git
 git clone https://github.com/HRAmbalia/CAPTCHA-detection-BISAG.git
 ```

2. Install the required packages using pip:

```python
pip install -r requirements.txt
```

3. Download the pre-trained model from the following link for the app `home`: 
 - [Model1 Link](https://drive.google.com/file/d/1L3KnTb1TvhID_bcyGU5OodpVi39Nn_So/view?usp=sharing) naming it m1.h2,
 - [Model2 Link](https://drive.google.com/file/d/1H1WPEWtnnsEPb7KZv4o-Iz0xNdza2vTf/view?usp=sharing) naming it m2.h2,
 - [Model3 Link](https://drive.google.com/file/d/1j063VdhWN-2bkA36eNalmptHQKOI57PS/view?usp=sharing) naming it m3.h2.

4. Place the downloaded model file in the `home/static/models/` directory of the project.

5. Download the pre-trained model from the following link for the app `textCaptcha`: 
 - [Model1 Link](https://drive.google.com/file/d/1j063VdhWN-2bkA36eNalmptHQKOI57PS/view?usp=sharing) naming it m1.h2.

6. Place the downloaded model file in the `textCaptcha/static/model/` directory of the project.

## Usage

To run the application, run the following command:

```python
python3 manage.py runserver
```

## Contributors

Contributions are welcome! If you'd like to contribute to this project, please contact contributors.
1. Chandresh Gohel
2. Riddhi Chaudhary
3. Samruddhi Thakor

## Contact

Author: HRAmbalia

Email: ambaliaharshit25@gmail.com
