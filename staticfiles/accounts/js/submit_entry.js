document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('id_media_files');
    const previewContainer = document.getElementById('media-preview');
    const previewGrid = document.getElementById('preview-grid');
    let selectedFiles = [];
    
    fileInput.addEventListener('change', function(e) {
        const files = Array.from(e.target.files);
        selectedFiles = files;
        updatePreview();
    });
    
    function updatePreview() {
        if (selectedFiles.length === 0) {
            previewContainer.style.display = 'none';
            return;
        }
        
        previewContainer.style.display = 'block';
        previewGrid.innerHTML = '';
        
        selectedFiles.forEach((file, index) => {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            
            const removeBtn = document.createElement('button');
            removeBtn.className = 'remove-file';
            removeBtn.innerHTML = '×';
            removeBtn.type = 'button';
            removeBtn.onclick = function() {
                removeFile(index);
            };
            
            const fileInfo = document.createElement('div');
            fileInfo.className = 'file-info';
            fileInfo.textContent = file.name + ' (' + formatFileSize(file.size) + ')';
            
            if (file.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.src = URL.createObjectURL(file);
                img.onload = function() {
                    URL.revokeObjectURL(img.src);
                };
                previewItem.appendChild(img);
            } else if (file.type.startsWith('video/')) {
                const video = document.createElement('video');
                video.src = URL.createObjectURL(file);
                video.controls = false;
                video.muted = true;
                previewItem.appendChild(video);
            }
            
            previewItem.appendChild(removeBtn);
            previewItem.appendChild(fileInfo);
            previewGrid.appendChild(previewItem);
        });
    }
    
    function removeFile(index) {
        selectedFiles.splice(index, 1);
        updateFileInput();
        updatePreview();
    }
    
    function updateFileInput() {
        const dt = new DataTransfer();
        selectedFiles.forEach(file => {
            dt.items.add(file);
        });
        fileInput.files = dt.files;
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    document.getElementById('submission-form').addEventListener('submit', function(e) {
        if (selectedFiles.length === 0) {
            e.preventDefault();
            alert('Veuillez sélectionner au moins un fichier média.');
            return false;
        }
    });
});