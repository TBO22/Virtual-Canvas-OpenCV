<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <img src="drawing.jpg" alt="Virtual Canvas Preview" style="display: block; margin: 0 auto; max-width: 100%; height: auto;">
    <h1>Virtual Canvas</h1>
    <p>
        Welcome to the Virtual Canvas project! This project enables you to create a virtual drawing board controlled entirely by hand gestures using your webcam.
    </p>
    <h2>Features</h2>
    <ul>
        <li>Draw and erase on a virtual canvas using your hands.</li>
        <li>Select colors from a palette to create colorful drawings.</li>
        <li>Toggle between drawing and erasing modes seamlessly.</li>
        <li>Gesture-controlled functionality using MediaPipe's hand tracking.</li>
        <li>Real-time canvas updates and a live webcam feed for feedback.</li>
    </ul>
    <h2>Installation</h2>
    <p>Follow these steps to set up the project on your local machine:</p>
    <ol>
        <li>Clone this repository:</li>
        <pre><code>git clone https://github.com/TBO22/Virtual-Canvas-OpenCV.git</code></pre>
        <li>Navigate to the project directory:</li>
        <pre><code>cd Virtual-Canvas-OpenCV</code></pre>
        <li>Install the required dependencies:</li>
        <pre><code>pip install -r requirements.txt</code></pre>
        <li>Run the program:</li>
        <pre><code>python Virtual_Canvas.py</code></pre>
    </ol>
    <h2>How to Use</h2>
    <ol>
        <li>Ensure your webcam is connected and working.</li>
        <li>Run the program and allow it to access your webcam.</li>
        <li>Use hand gestures to draw or erase on the canvas:
            <ul>
                <li>Bring your thumb close to your index finger to start drawing. The thumb acts as a switch to enable or disable drawing</li>
                <li>Select a color by hovering your index finger over the color palette.</li>
                <li>Hover your index finger over the "Erase" button to toggle eraser mode.</li>
                <li>To clear the entire canvas, press the <strong>'C'</strong> key on your keyboard.</li>
                <li>Press the <strong>'Q'</strong> key to exit the program.</li>
            </ul>
        </li>
    </ol>
    <h2>Requirements</h2>
    <p>The following dependencies are required to run the project:</p>
    <ul>
        <li>Python 3.7 or higher</li>
        <li>opencv-python</li>
        <li>mediapipe</li>
        <li>numpy</li>
    </ul>
    <h2>Project Structure</h2>
    <ul>
        <li><strong>Virtual_Canvas.py</strong>: The main script that runs the virtual canvas.</li>
        <li><strong>requirements.txt</strong>: A file containing all required Python dependencies.</li>
    </ul>
    <h2>Contributing</h2>
    <p>Contributions are welcome! Feel free to fork this repository, create a new branch, and submit a pull request.</p>
    <ol>
        <li>Fork the repository.</li>
        <li>Create a new branch:</li>
        <pre><code>git checkout -b feature-branch</code></pre>
        <li>Make your changes and commit them:</li>
        <pre><code>git commit -m "Add new feature"</code></pre>
        <li>Push to the branch:</li>
        <pre><code>git push origin feature-branch</code></pre>
        <li>Submit a pull request.</li>
    </ol>
    <h2>License</h2>
    <p>This project is licensed under the MIT License. See the LICENSE file for details.</p>
    <h2>Acknowledgments</h2>
    <p>Thanks to the following libraries for making this project possible:</p>
    <ul>
        <li><a href="https://opencv.org/">OpenCV</a> for image and video processing.</li>
        <li><a href="https://mediapipe.dev/">MediaPipe</a> for advanced hand tracking.</li>
        <li><a href="https://numpy.org/">NumPy</a> for array manipulation.</li>
    </ul>
</body>
</html>
