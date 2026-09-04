<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />



# OnionScan 🎯


## Basic Details
### Team Name: Java


### Team Members
- Team Lead: Riona Poly - Model Engineering College
- Member 2: Adwaitha P S - Model Engineering College


### Project Description
OnionScan is a computer-vision based web application that detects and counts the visible layers of an onion from an uploaded image. It uses image processing techniques to identify onion rings and displays the estimated layer count.

### The Problem (that doesn't exist)
Ever wondered how many layers an onion has without actually counting them?

Apparently, manually counting onion layers is a serious problem that humanity desperately needed to solve.

### The Solution (that nobody asked for)
OnionScan lets you upload an image of a cut onion and does the counting for you.
It processes the image, detects circular onion rings using computer vision and gives you the estimated number of layers just because counting onions should be automated too.

## Technical Details
### Technologies/Components Used
For Software:
- Languages used: Python
- Frameworks used: Flask
- Libraries used: OpenCV, NumPy
- Tools used: VS Code, Git & GitHub

### Implementation
For Software:
The application follows this image-processing pipeline:

User
  ↓
Upload Onion Image
  ↓
Flask Web Application
  ↓
Image Preprocessing
  ├── Resize
  ├── Grayscale Conversion
  └── Gaussian Blur
  ↓
Hough Circle Detection
  ↓
Duplicate Detection Filtering
  ↓
Count Onion Rings
  ↓
Image + Layer Count
  ↓
Display Result

The uploaded image is processed using OpenCV. Hough Circle Transform is used to identify circular patterns corresponding to visible onion layers.

# Installation
Clone the repository:

git clone https://github.com/Riona-Poly/OnionScan.git
cd OnionScan

Install the required Python packages:

pip install -r requirements.txt

# Run
Start the Flask application:

python app.py

Open your browser and visit:

http://127.0.0.1:5000

Upload a cut onion image and click Detect Layers.

### Project Documentation
For Software:

# Screenshots (Add at least 3)
![Screenshot1](Add screenshot 1 here with proper name)
*Add caption explaining what this shows*

![Screenshot2](Add screenshot 2 here with proper name)
*Add caption explaining what this shows*

![Screenshot3](Add screenshot 3 here with proper name)
*Add caption explaining what this shows*

# Diagrams
![Workflow](Add your workflow/architecture diagram here)
*Add caption explaining your workflow*

For Hardware:

# Schematic & Circuit
![Circuit](Add your circuit diagram here)
*Add caption explaining connections*

![Schematic](Add your schematic diagram here)
*Add caption explaining the schematic*

# Build Photos
![Components](Add photo of your components here)
*List out all components shown*

![Build](Add photos of build process here)
*Explain the build steps*

![Final](Add photo of final product here)
*Explain the final build*

### Project Demo
# Video
[Add your demo video link here]
*Explain what the video demonstrates*

# Additional Demos
[Add any extra demo materials/links]

## Team Contributions
- Riona Poly:  Worked on backend testing and validation, verifying and correcting the detected onion layer counts to improve the accuracy of the system and contributed to the frontend development. 
- Adwaitha P S: Initial project setup and development, contributed to the development of the frontend interface and overall project structure.

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)



