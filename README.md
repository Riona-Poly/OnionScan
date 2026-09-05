<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />



# Savalagirigiri 🎯


## Basic Details
### Team Name: Java


### Team Members
- Team Lead: Riona Poly - Model Engineering College
- Member 2: Adwaitha P S - Model Engineering College


### Project Description
Savalagirigiri is a web application that detects and counts the visibly observable layers of an onion from an uploaded or captured image.

The application uses a Flask backend and Gemini 3.6 Flash to analyze the onion image and return the total number of visible layers across all onion pieces in the image.

### The Problem (that doesn't exist)
Ever wondered how many layers an onion has without actually counting them?

Apparently, manually counting onion layers is a serious problem that humanity desperately needed to solve.

### The Solution (that nobody asked for)
Savalagirigiri lets you capture or upload an image of a cut onion and automatically counts its visible layers.

The image is sent to the backend, processed, and analyzed using Gemini 3.6 Flash. The detected layer count is then displayed to the user.

## Technical Details
### Technologies/Components Used
**For Software:**

- Language: Python
- Framework: Flask
- AI Model: Gemini 3.6 Flash
- Libraries:
  - OpenCV
  - google-genai
  - python-dotenv
- Frontend:
  - HTML
  - CSS
  - JavaScript
- Tools:
  - VS Code
  - Git
  - GitHub


### Implementation
The application follows this pipeline:

```text
User
  ↓
Capture Image / Upload Image
  ↓
Frontend
  ↓
Image Preview
  ↓
Automatic Submission
  ↓
Flask Backend
  ↓
Image Validation & Processing
  ↓
Convert Image to Base64
  ↓
Gemini 3.6 Flash
  ↓
Analyze Visible Onion Layers
  ↓
Return Layer Count
  ↓
Display Result
```

# Installation
Clone the repository:

git clone https://github.com/Riona-Poly/OnionScan.git

cd OnionScan

Install the required Python packages:

pip install -r requirements.txt

# Run

Open your browser and visit:

https://savalagirigiri.onrender.com/

Upload a cut onion image and click Detect Layers.

### Project Documentation
For Software:

## Screenshots

### 1. Savalagirigiri Interface

![Savalagirigiri Interface](static/screenshots/Screenshot1.png)

*Main Savalagirigiri interface showing the image upload and camera options.*

### 2. Backend Code

![Backend Code](static/screenshots/Screenshot2.png)

*Backend implementation used for processing the uploaded image and detecting onion layers.*

### 3. Detection Result

![Detection Result](static/screenshots/Screenshot3.png)

*Example of the detected onion-layer count displayed by Savalagirigiri.*

## Diagrams

### Workflow

![Savalagirigiri Workflow](static/screenshots/workflow.png)

*Workflow of Savalagirigiri from image capture/upload to onion-layer detection and result display.*





## Project Demo

### Video

[Watch the Savalagirigiri Demo](static/Recording.mp4)

*This video demonstrates the complete Savalagirigiri workflow, including capturing or uploading an onion image, automatic image submission, AI-based onion layer detection using Gemini 3.6 Flash, and displaying the detected layer count.*


## Team Contributions
- Riona Poly:  Worked on backend testing and validation, verifying and correcting the detected onion layer counts to improve the accuracy of the system and contributed to the frontend development. 
- Adwaitha P S: Initial project setup and development, contributed to the development of the frontend interface and overall project structure.

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)



