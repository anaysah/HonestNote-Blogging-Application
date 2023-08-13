class CustomUploadAdapter {
    constructor(loader, uploadUrl, crsfToken, postId) {
        this.loader = loader;
        this.uploadUrl = uploadUrl;
        this.crsfToken = crsfToken;
        this.postId = postId;
        this.createImageDiv = createImageDiv;
    }
    upload() {
        return this.loader.file.then(file => {
            return new Promise((resolve, reject) => {
                // Create a FormData object and append the file to it
                const formData = new FormData();
                formData.append('upload', file);
                formData.append('post_id', this.postId);

                fetch(this.uploadUrl, {  // Make a fetch request to your backend API to upload the file
                    method: 'POST',
                    headers: { 'X-CSRFToken': this.crsfToken, },
                    body: formData
                })
                    .then(response => isResponseOk(response))
                    .then(data => {
                        const obj = data.uploaded_images_data[0];
                        const imageUrl = obj.secure_url; // Process the response data (e.g., extract URL)
                        if (this.createImageDiv) {
                            this.createImageDiv(obj);
                        }
                        resolve({ default: imageUrl }); // Resolve the promise with the image URL
                    })
                    .catch(error => {
                        reject(error); // Reject the promise with an error message
                    });
            });
        });
    }

    abort() {
        if (this.controller) {
            this.controller.abort();
        }
    }
}