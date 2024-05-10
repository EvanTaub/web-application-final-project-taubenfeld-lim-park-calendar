const add_single = document.querySelector('.add-individual')
const upload_cycle = document.querySelector('.upload-cycle')
const add_single_form = document.querySelector('.form-add-individual')
const upload_cycle_form = document.querySelector('.form-upload-cycle')

function show_add(){
    add_single_form.style.display = 'block'
    upload_cycle_form.style.display = 'none'
}

function show_upload(){
    add_single_form.style.display = 'none'
    upload_cycle_form.style.display = 'block'
}

add_single.addEventListener("click", show_add)
upload_cycle.addEventListener("click", show_upload)