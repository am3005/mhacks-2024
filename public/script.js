(function() {
    var width = 320;
    var height = 0;
    var streaming = false;
    var video = null;
    var canvas = null;
    var photo = null;
    var startbutton = null;
    var sendbutton = null;

    // Array to hold captured image data
    var capturedImages = [];

    function startup() {
        video = document.getElementById('video');
        canvas = document.getElementById('canvas');
        photo = document.getElementById('photo');
        startbutton = document.getElementById('startbutton');
        sendbutton = document.getElementById('sendbutton');

        // Request access to the webcam
        navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false
            })
            .then(function(stream) {
                video.srcObject = stream;
                video.play();
            })
            .catch(function(err) {
                console.log("An error occurred: " + err);
            });

        // Handle the canplay event when the video stream is ready
        video.addEventListener('canplay', function(ev) {
            if (!streaming) {
                height = video.videoHeight / (video.videoWidth / width);

                if (isNaN(height)) {
                    height = width / (4 / 3);
                }

                video.setAttribute('width', width);
                video.setAttribute('height', height);
                canvas.setAttribute('width', width);
                canvas.setAttribute('height', height);
                streaming = true;
            }
        }, false);

        // Capture image when startbutton is clicked
        startbutton.addEventListener('click', function(ev) {
            takepicture();
            ev.preventDefault();
        }, false);

        // Send images to the server when sendbutton is clicked
        sendbutton.addEventListener('click', function() {
            sendPhotos();
        });

        clearphoto();
    }

    // Function to clear the photo canvas
    function clearphoto() {
        var context = canvas.getContext('2d');
        context.fillStyle = "#AAA";
        context.fillRect(0, 0, canvas.width, canvas.height);
        var data = canvas.toDataURL('image/png');
        photo.setAttribute('src', data);
    }

    // Function to take a picture and store the image
    function takepicture() {
        var context = canvas.getContext('2d');
        if (width && height) {
            canvas.width = width;
            canvas.height = height;
            context.drawImage(video, 0, 0, width, height);
            var data = canvas.toDataURL('image/png');
            photo.setAttribute('src', data);
            capturedImages.push(data); // Store the captured image in an array
        } else {
            clearphoto();
        }
    }

    // Function to send captured images to the server
    function sendPhotos() {
        if (capturedImages.length > 0) {
            fetch('/upload', { // Ensure the server endpoint is correct
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ images: capturedImages })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                // Redirect to results page
                window.location.href = '/results';
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        } else {
            alert("No photos to send!");
        }
    }

    // Start everything when the window loads
    window.addEventListener('load', startup, false);
})();
