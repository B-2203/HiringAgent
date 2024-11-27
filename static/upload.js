function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();

    if (fileInput.files.length === 0) {
        alert("Please select a file.");
        return;
    }

    formData.append("file", fileInput.files[0]);

    fetch('http://localhost:5000/upload', { // Replace with your Flask endpoint
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Upload failed');
        }
    })
    .then(data => {
        console.log('Success:', data);
        alert('File uploaded successfully');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('File upload failed');
    });
}
