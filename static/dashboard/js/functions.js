function isResponseOk(response) {
    if (!response.ok) {
        return response.json()
            .then(data => {
                let errorMessage = data.message || response.statusText;
                throw new Error(errorMessage);
            });
    }
    return response.json();
}

//-----------------------------------------------------------------
function copyImageUrl(secureUrl) {
    navigator.clipboard.writeText(secureUrl)
        .then(() => alert("Image URL copied to clipboard!"))
        .catch((error) => console.error("Failed to copy image URL: ", error));
}
//--------------------------------------------------------------------

function createDeleteBtn(imagePk, postPk) {
    const deleteButton = document.createElement("button");
    deleteButton.className = "delete-image-btn";
    deleteButton.textContent = "delete";
    deleteButton.onclick = () => deleteImage(deleteButton, imagePk, postPk);
    return deleteButton
}
function createImg(secureUrl) {
    const img = document.createElement('img');
    img.src = secureUrl;
    return img;
}

function createCopyBtn(secureUrl) {
    const copyButton = document.createElement("button");
    copyButton.className = "copy-image-url";
    copyButton.textContent = "< >";
    // copyButton.onClick = `copyImageUrl(${secureUrl})`        
    copyButton.onclick = () => copyImageUrl(secureUrl);
    return copyButton;
}

function createImageDiv(obj) {
    const imagesContainer = document.getElementById("all-images");

    var deleteButton = createDeleteBtn(obj.image_pk, obj.post_pk);
    var img = createImg(obj.secure_url)
    var copyButton = createCopyBtn(obj.secure_url)

    var imageContainer = document.createElement('div');
    imagesContainer.appendChild(imageContainer);

    imageContainer.appendChild(img);
    imageContainer.appendChild(deleteButton);
    imageContainer.appendChild(copyButton);
}