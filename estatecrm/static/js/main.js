// Profile card
document.addEventListener("DOMContentLoaded", function() {
    var modals = document.querySelectorAll("[data-modal]");
    modals.forEach(function (trigger) {
    trigger.addEventListener("click", function (event) {
        event.preventDefault();
        var modal = document.getElementById(trigger.dataset.modal);
        modal.classList.add("open");
        var exits = modal.querySelectorAll(".modal-exit");
        exits.forEach(function (exit) {
        exit.addEventListener("click", function (event) {
            event.preventDefault();
            modal.classList.remove("open");
        });
        });
    });
    });
});
function pingEffect(button_id){
    const button = document.getElementById(button_id)
    button.classList.add("animate-ping");
    setTimeout(function(){ button.classList.remove("animate-ping"); }, 1000);

}


