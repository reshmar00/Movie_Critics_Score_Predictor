document.querySelector('.editable').addEventListener('keydown', function(event) {
    if (event.keyCode === 13) {
        this.insertAdjacentHTML('beforeend', '<br>');
        return false;
    }
});