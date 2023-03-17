// Example starter JavaScript for disabling form submissions if there are invalid fields
// function submitForm(event) {
//     event.preventDefault(); // Prevent default form submission
    
//     const form = document.getElementById("weird-form");
//     const formData = new FormData(form); // Get form data
    
//     const jsonObject = {}; // Create empty object
    
//     for (const [key, value] of formData.entries()) {
//         jsonObject[key] = value; // Add form data to object
//     }
    
//     const jsonPayload = JSON.stringify(jsonObject); // Convert object to JSON
    
//     console.log(jsonPayload); // Log JSON payload (for testing)
    
//     // Send JSON payload to server using fetch
//     fetch("/paper/submit", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: jsonPayload
//     })
//     .then(response => {
//         if (response.ok) {
//             window.location.href = "https://app.prolific.co/submissions/complete?cc=C157221E"; // Redirect on success
//         } else {
//             alert("Something went wrong when submitting the data"); // Throw error on failure
//         }
//     })
//     .catch(error => console.error(error));
// }

(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})()