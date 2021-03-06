/*
* Email module
*/
function sendRentEmail(pk){
    document.getElementById('eform'+pk).addEventListener('submit', event=>{
        event.preventDefault();

        const emailForm = document.getElementById('eform'+pk);
        let formData = new FormData(emailForm);
        let serialFormData = [];
        i=0;
        for (let [key, value] of formData) {
            serialFormData[i] = {[key]:value};
            i++;
        }

        fetch("{% url 'properties:ajax_rent_email_listview' %}", {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : '{{csrf_token}}',
        },
        body: JSON.stringify(serialFormData),
        })
        .then(response => response.json())
        .then(data => {
        emailForm.reset();
        s = document.getElementById('output'+pk)
        s.setAttribute("class", "alert_success");
        s.innerHTML = data.msg;
        s.style.display = 'block';
        s.style.opacity = 1;
        setTimeout(()=>{fade()}, 2500);
        function fade(){(s.style.opacity-=.1)<0?s.style.display="none":setTimeout(fade,40)};
        })
        .catch((error) => {
        console.trace(error);
        e = document.getElementById('output'+pk);
        e.setAttribute("class", "alert_danger");
        e.innerHTML = 'An error occurred, please refresh the page and try again.';
        e.style.display = 'block';
        e.style.opacity = 1;
        setTimeout(()=>{fade()}, 2500);
        function fade(){(e.style.opacity-=.1)<0?e.style.display="none":setTimeout(fade,40)};
        });
    });
}

function rentEmail(pk) {
    const map = document.querySelector('.emailForm'+pk);
    if (map.classList.contains('hidden')) {
        map.classList.remove('hidden');
    } else {
        map.classList.add('hidden');
    }
}