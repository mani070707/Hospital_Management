// JavaScript for Hospital Management Webpage

// Function to toggle the mobile menu
function toggleMenu() {
    const nav = document.querySelector('nav ul');
    nav.style.display = nav.style.display === 'block' ? 'none' : 'block';
}

// Event listener for the menu icon
document.querySelector('.menu-icon').addEventListener('click', toggleMenu);

// Function to navigate to the diagnosis page
// Event listener for the "Diagnose My Diseases" button
document.getElementById('diagnose-button').addEventListener('click', diagnoseMyDiseases);
function diagnoseMyDiseases() {
    window.location.href = 'diagnose.html';
}

