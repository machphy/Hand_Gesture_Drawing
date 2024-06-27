
# Interactive Hand Gesture Drawing Application

This is a real-time drawing application that uses OpenCV and MediaPipe for hand tracking. The application allows you to draw using your finger with multiple color options and a simple interface.

## Features

- **Real-Time Hand Tracking**: Utilizes MediaPipe to track hand movements accurately.
- **Multiple Colors**: Easily switch between blue, green, red, and yellow for your drawings.
- **Clear Canvas**: Clear the canvas with a simple gesture.
- **User-Friendly Interface**: Color selection buttons arranged vertically on the right side for easy access.

## Technologies Used

- **OpenCV**: For image processing and computer vision tasks.
- **MediaPipe**: For real-time hand tracking.
- **Python**: For overall application development.

## How It Works

1. **Hand Detection**: The app detects your hand and tracks the position of your fingers.
2. **Drawing**: Move your finger across the screen to draw. Select different colors by pointing to the corresponding color box on the right.
3. **Clear Canvas**: Clear your drawing by gesturing towards the 'CLEAR' box.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/hand-gesture-drawing.git
    cd hand-gesture-drawing
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Run the application**:
    ```bash
    python hand_gesture_drawing.py
    ```

2. **Usage Instructions**:
    - The webcam will open and start detecting your hand.
    - Move your finger to draw on the screen.
    - Select colors by pointing to the corresponding color box on the right side.
    - Clear the canvas by pointing to the 'CLEAR' box.

## Future Improvements

- Adding more colors and brush sizes.
- Implementing gesture recognition for additional commands.
- Enhancing the overall user experience with more intuitive controls.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome all improvements and new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or suggestions, please feel free to reach out to me at [your-email@example.com].

---

### Example Requirements File (`requirements.txt`)

```
opencv-python-headless
mediapipe
numpy
```

Make sure to replace placeholders like `yourusername`, `your-email@example.com`, and the repository URL with your actual details.
