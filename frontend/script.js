let compareList = [];
let cropper;

// -------------------------------
// UNIFIED UI RENDERER
// -------------------------------
// 💡 We use one function for both Search and OCR to keep the UI perfectly consistent!
function generateMedicineCardHTML(med, source, index = 0) {
    let badge = "";
    if (source === "database" && index === 0) badge = `<span class="badge">Top Match</span>`;
    if (source === "database" && index === -1) badge = `<span class="badge">OCR Match</span>`;
    if (source === "ai") badge = `<span class="badge" style="background:#888; color:white;">AI Generated</span>`;

    let safeMed = encodeURIComponent(JSON.stringify(med));

    return `
    <div class="card">
        <div class="card-header">
            <h2>${med.name}</h2>
            ${badge}
        </div>
        <p><b>Price:</b> ₹${med.price || "N/A"}</p>
        <p><b>Composition:</b><br>${med.composition || "Not Available"}</p>
        <p><b>Uses:</b><br>${med.uses || "Not Available"}</p>
        <p><b>Side Effects:</b><br>${med.side_effects || "Not Available"}</p>
        ${med.precautions ? `<p><b>Precautions:</b><br>${med.precautions}</p>` : ""}
        
        <button class="compare-btn" onclick='toggleCompare(decodeURIComponent("${safeMed}"), this)'>
            + Add to Compare
        </button>
    </div>`;
}

// -------------------------------
// SEARCH
// -------------------------------
async function searchMedicine() {
    let query = document.querySelector(".search-box input").value;

    if (!query) {
        alert("Please enter a medicine name");
        return;
    }

    let resultsDiv = document.getElementById("results");
    let loader = document.getElementById("loader");

    loader.style.display = "block";
    resultsDiv.style.display = "block"; // Ensure container is visible
    resultsDiv.innerHTML = "";

    try {
        let response = await fetch(`http://127.0.0.1:8000/search?query=${query}`);
        let data = await response.json();

        loader.style.display = "none";

        if (data.results && data.results.length > 0) {
            data.results.forEach((med, index) => {
                // Call our unified renderer
                resultsDiv.innerHTML += generateMedicineCardHTML(med, med.source, index);
            });
        } else {
            resultsDiv.innerHTML = "<p>❌ No results found</p>";
        }
    } catch (error) {
        console.error(error);
        loader.style.display = "none";
        resultsDiv.innerHTML = "<p>⚠️ Error fetching data</p>";
    }
}

// -------------------------------
// COMPARE LOGIC
// -------------------------------
function toggleCompare(encodedMed, button) {
    let med = JSON.parse(encodedMed);
    let index = compareList.findIndex(m => m.name === med.name);

    if (index !== -1) {
        compareList.splice(index, 1);
        button.innerText = "+ Add to Compare";
        button.style.background = "linear-gradient(135deg, #0a66c2, #28a745)";
    } else {
        if (compareList.length >= 4) {
            alert("Maximum 4 medicines allowed");
            return;
        }
        compareList.push(med);
        button.innerText = "Remove ✖";
        button.style.background = "#dc3545";
    }
    updateFloatingBar();
}

// -------------------------------
// COMPARE PAGE WITH INPUTS
// -------------------------------
function goToCompare() {
    hideAll();
    document.getElementById("compare-section").style.display = "block";
    renderCompareSlots();
}

function renderCompareSlots() {
    let grid = document.getElementById("compare-grid");
    if (!grid) return;

    grid.innerHTML = "";

    for (let i = 0; i < 4; i++) {
        let med = compareList[i];

        if (med) {
            grid.innerHTML += `
            <div class="compare-slot filled">
                <h3>${med.name}</h3>
                <p>₹${med.price || "N/A"}</p>
                <button onclick="removeFromCompare(${i})">Remove</button>
            </div>`;
        } else {
            grid.innerHTML += `
            <div class="compare-slot empty">
                <input 
                    type="text" 
                    placeholder="Search medicine..." 
                    class="compare-input"
                    onkeypress="handleCompareSearch(event, ${i})"
                />
            </div>`;
        }
    }
}

// -------------------------------
// SEARCH INSIDE COMPARE
// -------------------------------
async function handleCompareSearch(event, index) {
    if (event.key !== "Enter") return;

    let query = event.target.value.trim();
    if (!query) return;

    try {
        let res = await fetch(`http://127.0.0.1:8000/search?query=${query}`);
        let data = await res.json();

        if (data.results && data.results.length > 0) {
            let med = data.results[0];
            compareList[index] = med;
            renderCompareSlots();
        } else {
            alert("No medicine found");
        }
    } catch (err) {
        console.error(err);
        alert("Error fetching medicine");
    }
}

function removeFromCompare(index) {
    compareList.splice(index, 1);
    renderCompareSlots();
}

// -------------------------------
// FINAL COMPARISON VIEW
// -------------------------------
function showComparison() {
    if (compareList.length < 2) {
        alert("Select at least 2 medicines");
        return;
    }

    hideAll();
    let resultsDiv = document.getElementById("results");
    resultsDiv.style.display = "block";

    let html = `
    <button onclick="goToCompare()" class="back-btn">← Back</button>
    <div class="compare-container">`;

    compareList.forEach(med => {
        html += `
        <div class="compare-card">
            <h2>${med.name}</h2>
            <p><b>Price:</b> ₹${med.price || "N/A"}</p>
            <p><b>Uses:</b> ${med.uses || "Not Available"}</p>
            <p><b>Side Effects:</b> ${med.side_effects || "Not Available"}</p>
        </div>`;
    });

    html += `</div>`;
    resultsDiv.innerHTML = html;
}

function updateFloatingBar() {
    let bar = document.getElementById("floating-bar");
    if (!bar) return;

    if (compareList.length > 0) {
        bar.style.display = "flex";
        bar.innerHTML = `
            <span>${compareList.length} selected</span>
            <button onclick="goToCompare()">Compare</button>
        `;
        setTimeout(() => bar.classList.add("show"), 10);
    } else {
        bar.classList.remove("show");
        setTimeout(() => bar.style.display = "none", 300);
    }
}

// -------------------------------
// NAVIGATION
// -------------------------------
function showHome() {
    hideAll();
    document.getElementById("hero-section").style.display = "block";
}

function showUpload() {
    hideAll();
    document.getElementById("upload-section").style.display = "block";
}

function showProfile() {
    hideAll();
    document.getElementById("profile-section").style.display = "block";
}

function showChat() {
    hideAll();
    document.getElementById("chat-section").style.display = "block";
}

function hideAll() {
    let sections = [
        "hero-section",
        "upload-section",
        "profile-section",
        "chat-section",
        "compare-section"
    ];

    sections.forEach(id => {
        let el = document.getElementById(id);
        if (el) el.style.display = "none";
    });
}

function processOCRText(rawText) {
    let lines = rawText.split("\n")
        .map(l => l.trim())
        .filter(l => l.length > 2);

    if (lines.length === 0) {
        alert("No medicine detected.");
        return;
    }

    document.querySelector(".search-box input").value = lines[0];
    showHome();
    searchMedicine();
}

// -------------------------------
// 📤 IMAGE UPLOAD (FIXED DOM STATE)
// -------------------------------
async function uploadImage() {
    const input = document.getElementById("imageInput");

    if (!input.files.length) {
        alert("Please choose an image first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", input.files[0]);

    const loader = document.getElementById("loader");
    loader.style.display = "block";

    try {
        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        loader.style.display = "none";
        
        console.log("OCR Backend Response:", data);

        // 1. Handle Errors First
        if (data.source === "ocr_error" || data.source === "not_found" || data.source === "error") {
            alert(data.message || "No medicine detected. Please try a clearer image.");
            return; // Exit early, stay on upload page
        }

        // 2. Prepare the UI State
        hideAll(); // Hide upload page completely
        document.getElementById("hero-section").style.display = "block"; // Show main UI
        
        const results = document.getElementById("results");
        results.style.display = "block"; // 🚨 CRITICAL FIX: Ensure container is visible!
        results.innerHTML = ""; // Clear old results

        // 3. Render the exact same UI for DB or AI
        if (data.source === "database" || data.source === "ai") {
            // Index -1 tells our generator to render the specific "OCR Match" badge
            results.innerHTML = generateMedicineCardHTML(data.medicine, data.source, -1);
        } else {
            console.log(data);
            alert("Unexpected response format from server.");
        }

    } catch (err) {
        console.error("Upload Error:", err);
        loader.style.display = "none";
        alert("Error connecting to server. Is FastAPI running?");
    }
}

// -------------------------------
// IMAGE PREVIEW & CROP
// -------------------------------
document.addEventListener("DOMContentLoaded", () => {
    let input = document.getElementById("imageInput");
    if (!input) return;

    input.addEventListener("change", function () {
        let file = this.files[0];
        if (!file) return;

        let preview = document.getElementById("preview");
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";

        if (cropper) cropper.destroy();

        cropper = new Cropper(preview, {
            viewMode: 1
        });

        let cropBtn = document.getElementById("crop-btn");
        if (cropBtn) cropBtn.style.display = "inline-block";
    });
});

function cropImage() {
    if (!cropper) return;
    let canvas = cropper.getCroppedCanvas();

    canvas.toBlob(blob => {
        let file = new File([blob], "cropped.jpg");
        let dt = new DataTransfer();
        dt.items.add(file);

        document.getElementById("imageInput").files = dt.files;
        document.getElementById("preview").src = URL.createObjectURL(blob);
    });
}

// -------------------------------
// CAMERA
// -------------------------------
let cameraStream = null;

function openCamera() {
    let video = document.getElementById("camera");
    let box = document.getElementById("camera-box");
    if (box) box.style.display = "block";

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            cameraStream = stream;
            video.srcObject = stream;
            video.play();
        })
        .catch(err => {
            console.error(err);
            alert("Unable to access camera.");
        });
}

function captureImage() {
    let video = document.getElementById("camera");
    let canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    let ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    canvas.toBlob(blob => {
        let file = new File([blob], "camera.jpg");
        let dt = new DataTransfer();
        dt.items.add(file);

        document.getElementById("imageInput").files = dt.files;
        document.getElementById("preview").src = URL.createObjectURL(blob);
        document.getElementById("preview").style.display = "block";

        if (cropper) cropper.destroy();

        cropper = new Cropper(
            document.getElementById("preview"),
            { viewMode: 1 }
        );

        if (cameraStream) {
            cameraStream.getTracks().forEach(track => track.stop());
        }

        let box = document.getElementById("camera-box");
        if (box) box.style.display = "none";
    }, "image/jpeg");
}

// -------------------------------
// CHAT
// -------------------------------
function formatText(text) {
    if (!text) return "";
    return text
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/Uses:/g, "<br><br><b>💊 Uses:</b><br>")
        .replace(/Side Effects:/g, "<br><br><b>⚠️ Side Effects:</b><br>")
        .replace(/Precautions:/g, "<br><br><b>🛡️ Precautions:</b><br>")
        .replace(/-\s/g, "• ")
        .replace(/\n/g, "<br>");
}

function addMessage(text, type) {
    let chatBox = document.getElementById("chat-box");

    let wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.justifyContent = type === "user" ? "flex-end" : "flex-start";

    let msg = document.createElement("div");
    msg.className = type === "user" ? "user-message" : "bot-message";

    msg.style.maxWidth = "70%";
    msg.style.padding = "12px 16px";
    msg.style.borderRadius = "12px";
    msg.style.margin = "8px";
    msg.style.background = type === "user" 
        ? "linear-gradient(135deg, #0a66c2, #28a745)" 
        : "#f1f3f6";
    msg.style.color = type === "user" ? "white" : "#333";
    msg.innerHTML = formatText(text);

    wrapper.appendChild(msg);
    chatBox.appendChild(wrapper);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    let input = document.getElementById("chat-input");
    let message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    try {
        let res = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        let data = await res.json();
        addMessage(data.reply || "No response", "bot");
    } catch (err) {
        console.error(err);
        addMessage("⚠️ Server error", "bot");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    let input = document.getElementById("chat-input");
    if (input) {
        input.addEventListener("keypress", function(e) {
            if (e.key === "Enter") sendMessage();
        });
    }
});