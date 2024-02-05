// chờ document load xong
document.addEventListener('DOMContentLoaded', function () { 

    
    document.getElementById('uploadBtn').onclick = function () {
        document.getElementById('uploaded_img').click();
    };
    document.getElementById('uploaded_img').onchange = function () {
        document.getElementById('uploading_img').src = URL.createObjectURL(this.files[0]);
        document.getElementById('submitBtn').hidden = false;
        if (this.files[0] !== null) {
            console.log('file uploaded');
        }
        else {
            console.log('file not uploaded');
        }
        
    };
    
});
