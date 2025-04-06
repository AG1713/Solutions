document.addEventListener('DOMContentLoaded', () => {
    console.log("Script loaded");

    // const landingPage = document.getElementById('landing-page');
    const searchPage = document.getElementById('search-page');
    const resultsTable = document.getElementById("results-table");

    // Global variable to store the current video ID and URL
    let currentVideoId = "";
    let currentVideoUrl = null;

    // startButton.addEventListener("click", function (event) {
    //     event.preventDefault();
    //     load_content()
    // });

    load_content()
    function load_content(){
        // landingPage.classList.add('hidden');
        searchPage.classList.remove('hidden');
        console.log("Entered fetch function");
        fetch("/start_scan/")
            .then(response => {
                if (!response.ok) throw new Error("Failed to fetch videos");
                return response.json();
            })
            .then(data => {
                const progressContainer = document.querySelector(".progress-container");
                if (progressContainer) {
                    progressContainer.remove();
                }
                resultsTable.innerHTML = "";
                data.videos.forEach(video => {
                    const row = document.createElement("tr");
                    console.log("Video object:", video);
                    let reviewButtonHtml = `<td style="text-align: center; font-weight: bold; color: green;">No action required</td>`;
                    // Show Review button if classification is not "Authentic"
                    if (video.classification !== "Authentic") {
                        reviewButtonHtml = `
                            <td>
                                <button class="action-button review" data-id="${video.id}" data-title="${video.title}" data-url="${video.url}">
                                    Review
                                </button>
                            </td>
                        `;
                    }
                    row.innerHTML = `
                        <td>
                            <a href="${video.url}" target="_blank" class="video-title">
                                ${video.title}
                            </a>
                        </td>
                        <td><span class="status-badge authentic">${video.classification}</span></td>
                        ${reviewButtonHtml}
                    `;
                    resultsTable.appendChild(row);
                });
            })
            .catch(error => console.error("Error fetching videos:", error));
    }

    // Event delegation for review buttons
    resultsTable.addEventListener("click", function (event) {
        const reviewBtn = event.target.closest("button.review");
        if (reviewBtn) {
            console.log("Review button clicked. Found button:", reviewBtn);
    
            // Retrieve the video details from the button's data attributes
            const videoTitle = reviewBtn.getAttribute("data-title");
            currentVideoId = reviewBtn.getAttribute("data-id");
            currentVideoUrl = reviewBtn.getAttribute("data-url");
    
            console.log("Current Video ID:", currentVideoId);
            document.getElementById("review-video-title").textContent = videoTitle;
    
            // Reset email fields and hide the email content container
            document.getElementById("sender-email").value = "";
            document.getElementById("receiver-email").value = "";
            document.getElementById("email-content-container").classList.add("hidden");
            document.getElementById("review-email-content").value = "";
    
            // Show the review section
            const reviewSection = document.getElementById("review-section");
            reviewSection.classList.remove("hidden");
            reviewSection.scrollIntoView({ behavior: "smooth" });
        }
    });
    
    // Event listener for the Generate Email button
    document.getElementById("generate-email-button").addEventListener("click", function () {
        const senderEmail = document.getElementById("sender-email").value.trim();
        const receiverEmail = document.getElementById("receiver-email").value.trim();
        console.log("Generating email for Video ID:", currentVideoId);

        if (!senderEmail || !receiverEmail) {
            alert("Please provide both sender and receiver email addresses.");
            return;
        }

        document.getElementById("review-email-content").value = "Generating email content, please wait...";
        const url = `/generate_email_content/?sender=${encodeURIComponent(senderEmail)}&receiver=${encodeURIComponent(receiverEmail)}&video_url=${encodeURIComponent(currentVideoUrl)}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                document.getElementById("review-email-content").value = data.email_content;
                document.getElementById("email-content-container").classList.remove("hidden");
            })
            .catch(error => {
                console.error("Error generating email content:", error);
                document.getElementById("review-email-content").value = "Error generating email content. Please try again.";
                document.getElementById("email-content-container").classList.remove("hidden");
            });
    });

    // Single event listener for the Send button using mailto
    document.getElementById("send-email-button").addEventListener("click", function () {
        const senderEmail = document.getElementById("sender-email").value.trim();
        const receiverEmail = document.getElementById("receiver-email").value.trim();
        const emailBody = document.getElementById("review-email-content").value;
        const subject = encodeURIComponent("Copyright Infringement - Request for Removal");
        const body = encodeURIComponent(`From: ${senderEmail}\n\n${emailBody}`);
        const mailtoUrl = `mailto:${receiverEmail}?subject=${subject}&body=${body}`;
        window.location.href = mailtoUrl;
    });

});
