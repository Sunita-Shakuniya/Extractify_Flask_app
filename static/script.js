function previewImage(input) {
    var preview = document.getElementById('imagePreview');
    var uploadIcon = document.getElementById('uploadIcon');

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            preview.style.display = 'block';
            uploadIcon.style.display = 'none';
            preview.setAttribute('src', e.target.result);
            // Enable the "Extract Text" button
            extractButton.disabled = false;
        }

        reader.readAsDataURL(input.files[0]); // Read the image file as a data URL
    }
}



function scrollToBottom() {
    // Scroll to the bottom of the page
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
}

// Scroll to the bottom when the page loads or content changes
window.onload = scrollToBottom;









