// JavaScript for Hospital Management Webpage

// Function to toggle the mobile menu
function toggleMenu() {
    const nav = document.querySelector('nav ul');
    nav.style.display = nav.style.display === 'block' ? 'none' : 'block';
}

// Event listener for the menu icon
document.querySelector('.menu-icon').addEventListener('click', toggleMenu);

// Placeholder function for "Diagnose My Diseases" button
function diagnoseMyDiseases() {
    alert('This feature will diagnose your diseases based on your input.');
}

// Event listener for the "Diagnose My Diseases" button
document.querySelector('.hero-content a').addEventListener('click', diagnoseMyDiseases);