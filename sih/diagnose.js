document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('diagnose-form');
    const resultDiv = document.getElementById('result');
    const selectedSymptomsContainer = document.getElementById('selected-symptoms');

    // Array of all symptoms
    const total_symptoms = [
        "Itching", "Skin Rash", "Nodal Skin Eruptions", "Continuous Sneezing", "Shivering",
        "Chills", "Joint Pain", "Stomach Pain", "Acidity", "Ulcers on Tongue", "Muscle Wasting",
        "Vomiting", "Burning Micturition", "Spotting Urination", "Fatigue", "Weight Gain",
        "Anxiety", "Cold Hands and Feets", "Mood Swings", "Weight Loss", "Restlessness",
        "Lethargy", "Patches in Throat", "Irregular Sugar Level", "Cough", "High Fever",
        "Sunken Eyes", "Breathlessness", "Sweating", "Dehydration", "Indigestion",
        "Headache", "Yellowish Skin", "Dark Urine", "Nausea", "Loss of Appetite",
        "Pain Behind the Eyes", "Back Pain", "Constipation", "Abdominal Pain", "Diarrhoea",
        "Mild Fever", "Yellow Urine", "Yellowing of Eyes", "Acute Liver Failure", "Fluid Overload",
        "Swelling of Stomach", "Swelled Lymph Nodes", "Malaise", "Blurred and Distorted Vision",
        "Phlegm", "Throat Irritation", "Redness of Eyes", "Sinus Pressure", "Runny Nose",
        "Congestion", "Chest Pain", "Weakness in Limbs", "Fast Heart Rate",
        "Pain During Bowel Movements", "Pain in Anal Region", "Bloody Stool",
        "Irritation in Anus", "Neck Pain", "Dizziness", "Cramps", "Bruising",
        "Obesity", "Swollen Legs", "Swollen Blood Vessels", "Puffy Face and Eyes",
        "Enlarged Thyroid", "Brittle Nails", "Swollen Extremeties", "Excessive Hunger",
        "Extra Marital Contacts", "Drying and Tingling Lips", "Slurred Speech",
        "Knee Pain", "Hip Joint Pain", "Muscle Weakness", "Stiff Neck", "Swelling Joints",
        "Movement Stiffness", "Spinning Movements", "Loss of Balance", "Unsteadiness",
        "Weakness of One Body Side", "Loss of Smell", "Bladder Discomfort", "Foul Smell of Urine",
        "Continuous Feel of Urine", "Passage of Gases", "Internal Itching", "Toxic Look (Typhos)",
        "Depression", "Irritability", "Muscle Pain", "Altered Sensorium", "Red Spots Over Body",
        "Belly Pain", "Abnormal Menstruation", "Dischromic Patches", "Watering from Eyes",
        "Increased Appetite", "Polyuria", "Family History", "Mucoid Sputum", "Rusty Sputum",
        "Lack of Concentration", "Visual Disturbances", "Receiving Blood Transfusion",
        "Receiving Unsterile Injections", "Coma", "Stomach Bleeding", "Distention of Abdomen",
        "History of Alcohol Consumption"
    ];

    // Generate checkboxes for symptoms
    const dropdownMenu = document.querySelector('.dropdown-menu');
    
    if (dropdownMenu) {
        total_symptoms.forEach(symptom => {
            const checkboxDiv = document.createElement('div');
            checkboxDiv.classList.add('checkbox');
            checkboxDiv.innerHTML = `<input type="checkbox" value="${symptom}"> ${symptom}`;
            dropdownMenu.appendChild(checkboxDiv);
        });
    } else {
        console.error('Dropdown menu container not found.');
    }

    // Function to update selected symptoms display
    const updateSelectedSymptoms = () => {
        const selectedSymptoms = [];
        document.querySelectorAll('.dropdown-menu .checkbox input:checked').forEach(function(checkedBox) {
            selectedSymptoms.push(checkedBox.value);
        });
        selectedSymptomsContainer.innerHTML = selectedSymptoms.map(symptom => `<span>${symptom}</span>`).join(', ');
    };

    // Attach event listeners to checkboxes
    document.addEventListener('change', function(event) {
        if (event.target.matches('.dropdown-menu .checkbox input')) {
            updateSelectedSymptoms();
        }
    });

    // Form submission event handler
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const symptoms = [];
            const daysInput = document.querySelector('.days-input-container input');
            const days = daysInput ? daysInput.value : 1;

            document.querySelectorAll('.dropdown-menu .checkbox input:checked').forEach(function(checkedBox) {
                symptoms.push(checkedBox.value);
            });
            console.log(symptoms)
            if (symptoms.length === 0) {
                if (resultDiv) {
                    resultDiv.textContent = 'Please select at least one symptom.';
                }
                return;
            }
            const payload = { symptoms, days };
            console.log(payload)
            fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (resultDiv) {
                    const predictedDisease = data.predicted_disease || 'No disease prediction available';
                    const description = data.description || 'No description available';
                    const precautions = data.precautions && data.precautions.length > 0
                        ? `You can take the following precautions: ${data.precautions.join(', ')}.`
                        : 'No precautions available.';
                    
            
                    resultDiv.innerHTML = `
                        <h2>Diagnosis Result</h2>
                        <br>
                        <p>By our diagnosis, you may have ${predictedDisease}. ${description} ${precautions}</p>
                    `;
                    resultDiv.style.display = 'block';
                    const submitButton = document.querySelector('button[type="submit"]');
                    submitButton.textContent = 'Reload';
                    submitButton.type = 'button'; // Change type to button
                    submitButton.onclick = () => location.reload(); // Set onclick to reload the page
                } else {
                    console.error('Result div is not found.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (resultDiv) {
                    resultDiv.textContent = 'An error occurred. Please try again.';
                    resultDiv.style.display = 'block'; 
                }
            });
        });
    }
});
