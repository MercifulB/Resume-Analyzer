const inpFile = document.getElementById("inpFile");
const btnUpload = document.getElementById("btnUpload");
const btnCompare = document.getElementById("btnCompare");
const resultText = document.getElementById("resultText");
const jobDescription = document.getElementById("jobDescription");

/* Extract text button functionality */
btnUpload.addEventListener("click", () => {
    const formData = new FormData();

    formData.append("pdfFile", inpFile.files[0]);

    fetch("/extract-text", {
        method: "post",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        resultText.value = data.extractedText.trim();
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

/* Compare text button functionality:
- connects to Flask backend to  compare job desc to 
  extracted or inserted resume text returning a similarity score

- repeats the same process for common skills and frequent words 
 */
btnCompare.addEventListener("click", () => {
    const formData = new FormData();

    formData.append("pdfText", resultText.value);
    formData.append("jobDescription", jobDescription.value);

    fetch("/extract-text", {
        method: "post",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.hasOwnProperty("similarityScore")) {
            alert(`Similarity Score: ${data.similarityScore}%`);
        } else {
            alert("Error calculating similarity.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });

    fetch("/common-skills", {
        method: "post",
        body: formData
    })

    .then(response => response.json())
    .then(data => {
        if (data.hasOwnProperty("commonSkills")) {
            displayCommonSkills(data.commonSkills);
        } else {
            console.log("Error fetching common skills.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });

    fetch("/frequent-nouns", {
        method: "post",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.hasOwnProperty("frequentNouns")) {
            displayFrequentNouns(data.frequentNouns);
        } else {
            console.log("Error fetching frequent nouns.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

/* Display common skills functionality:
   - connects to html skill container element
   - removes duplicates from the Flask commonskills
   - lists each word out in by appending them to list
     */

   function displayCommonSkills(commonSkills) {
    const commonSkillsContainer = document.getElementById("commonSkillsContainer");
    commonSkillsContainer.innerHTML = "<h3>Common Technical Skills:</h3>";

    // Remove duplicates from the skills list
    const uniqueSkills = [...new Set(commonSkills)];

    const skillsList = document.createElement("ul");
    skillsList.classList.add("horizontal-list"); // Add a class for styling

    uniqueSkills.forEach(skill => {
        const listItem = document.createElement("li");
        listItem.textContent = skill;
        skillsList.appendChild(listItem);
    });

    commonSkillsContainer.appendChild(skillsList);
}


/* Display Frequent Words functionality:
   - connects to html skill container element
   - recives common nouns from the Flask frequentNouns
   - lists each word out in by appending them to list
     */

function displayFrequentNouns(frequentNouns) {
    const frequentNounsContainer = document.getElementById("frequentNounsContainer");
    frequentNounsContainer.innerHTML = "<h3>Frequently Used Words:</h3>";

    const nounsList = document.createElement("ul");
    nounsList.classList.add("horizontal-list");

    frequentNouns.forEach(([noun, count]) => {
        const listItem = document.createElement("li");
        listItem.textContent = `${noun} (${count})`;
        nounsList.appendChild(listItem);
    });

    frequentNounsContainer.appendChild(nounsList);
}