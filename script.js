const imageInput = document.getElementById('image-input');
const previewImg = document.getElementById('preview-img');
const laser = document.getElementById('laser');
const actionBtn = document.getElementById('action-btn');
const gallery = document.getElementById('protected-gallery');
const nizhalToggle = document.getElementById('nizhal-toggle');

// 1. Show Preview when file is picked
imageInput.onchange = () => {
    const file = imageInput.files[0];
    if (file) {
        previewImg.src = URL.createObjectURL(file);
        previewImg.style.display = "block";
        document.getElementById('placeholder').style.display = "none";
        actionBtn.innerText = "Scan & Upload";
        actionBtn.style.background = "#ff5a5f";
    }
};

// 2. Handle Scan and Upload
actionBtn.onclick = async () => {
    if (!imageInput.files[0]) return;

    // Start Scan Animation
    laser.style.display = "block";
    laser.style.animation = "scanning 2s linear infinite";
    actionBtn.innerText = "Verifying Identity...";
    actionBtn.disabled = true;

    // Simulate 2 second delay for "Verification"
    await new Promise(r => setTimeout(r, 2000));

    // Finish Scan
    laser.style.display = "none";
    actionBtn.disabled = false;
    actionBtn.innerText = "Uploaded Successfully";
    actionBtn.style.background = "#28a745";

    // CHECK THE TOGGLE: Is protection ON?
    const isProtected = nizhalToggle.checked;

    addToVault(previewImg.src, isProtected);
};

// 3. Add to Vault function
function addToVault(url, shouldProtect) {
    const div = document.createElement('div');
    div.className = "vault-item";
    
    // Logic: If shouldProtect is true, add the tag. If false, add empty string.
    const tagHtml = shouldProtect ? `<div class="nizhal-tag">✓ Protected by Nizhal</div>` : "";

    div.innerHTML = `
        ${tagHtml}
        <img src="${url}" class="vault-img">
    `;
    
    gallery.prepend(div);
}