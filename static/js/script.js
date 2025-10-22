// document.addEventListener('DOMContentLoaded', () => {

//     // --- 1. Navbar Toggler for Mobile View ---
//     const toggler = document.getElementById('navbar-toggler');
//     const navCollapse = document.getElementById('navbarNav');

//     if (toggler && navCollapse) {
//         toggler.addEventListener('click', () => {
//             // Toggle the 'show' class for mobile responsiveness
//             navCollapse.classList.toggle('show');
//         });
//     }

//     // --- 2. Dropdown Functionality (Profile and Post New) ---
//     const dropdownTriggers = document.querySelectorAll('.dropdown');

//     dropdownTriggers.forEach(dropdown => {
//         const toggleLink = dropdown.querySelector('.dropdown-toggle');
//         const menu = dropdown.querySelector('.dropdown-menu');

//         if (toggleLink && menu) {
//             toggleLink.addEventListener('click', (e) => {
//                 e.preventDefault();
//                 // Toggle display of the clicked dropdown menu
//                 const isHidden = window.getComputedStyle(menu).display === 'none';

//                 // Close all other open dropdowns
//                 dropdownTriggers.forEach(otherDropdown => {
//                     const otherMenu = otherDropdown.querySelector('.dropdown-menu');
//                     if (otherMenu && otherMenu !== menu) {
//                         otherMenu.style.display = 'none';
//                     }
//                 });
               
//                 // Show/Hide the current menu
//                 menu.style.display = isHidden ? 'block' : 'none';
//             });
//         }
//     });

//     // Close dropdowns when clicking outside
//     document.addEventListener('click', (e) => {
//         if (!e.target.closest('.navbar-content')) {
//             dropdownTriggers.forEach(dropdown => {
//                 const menu = dropdown.querySelector('.dropdown-menu');
//                 if (menu) {
//                     menu.style.display = 'none';
//                 }
//             });
//         }
//     });

//     // --- 3. Smooth Scrolling (Retained from original) ---
//     document.querySelectorAll('a[href^="#"]').forEach(anchor => {
//         anchor.addEventListener('click', function (e) {
//             e.preventDefault();
//             const targetId = this.getAttribute('href');
//             const targetElement = document.querySelector(targetId);
//             if (targetElement) {
//                 targetElement.scrollIntoView({ behavior: 'smooth' });
//             }
//         });
//     });
// });
