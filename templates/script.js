document.getElementById('brailleForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    let formData = new FormData();
    const option = document.querySelector('input[name="option"]:checked').value;

    if (option === '1') {
        alert("Recording speech will be handled on the server.");
        // Here you can send a request to the server to initiate speech recording.
        // If you want to implement this, you'll need to add the logic for handling
        // speech recording and submission via an API endpoint.

        const response = await fetch('/speech', {
            method: 'POST'
        });

        const result = await response.json();
        document.getElementById('brailleOutput').innerText = `Braille Output: ${result.braille}`;

    } else if (option === '2') {
        const imageInput = document.getElementById('imageInput').files[0];
        if (!imageInput) {
            alert("Please select an image to upload.");
            return;
        }
        formData.append('image', imageInput);

        const response = await fetch('/image', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (result.error) {
            alert(result.error);
        } else {
            document.getElementById('brailleOutput').innerText = `Braille Output: ${result.braille}`;
        }

    } else if (option === '3') {
        const textInput = document.getElementById('textInput').value;
        if (!textInput) {
            alert("Please enter some text.");
            return;
        }
        formData.append('text', textInput);

        const response = await fetch('/text', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (result.error) {
            alert(result.error);
        } else {
            document.getElementById('brailleOutput').innerText = `Braille Output: ${result.braille}`;
        }
    }

    formData.append('option', option);
});
