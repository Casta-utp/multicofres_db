document.addEventListener("DOMContentLoaded", function () {
    // Mensaje de confirmación antes de eliminar un empleado
    let deleteButtons = document.querySelectorAll(".delete-btn");
    deleteButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            let confirmDelete = confirm("¿Estás seguro de que deseas eliminar este empleado?");
            if (!confirmDelete) {
                event.preventDefault(); // Cancela la acción si el usuario presiona "Cancelar"
            }
        });
    });
});

document.querySelector("form").addEventListener("submit", function(event) {
    let inputs = document.querySelectorAll("input[type='number']");
    for (let input of inputs) {
        if (parseFloat(input.value) < 0) {
            alert("Error: No puedes ingresar números negativos.");
            event.preventDefault();
            return;
        }
    }
});


