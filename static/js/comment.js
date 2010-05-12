$(document).ready(function() {
    // Customize the location of the media to match your project structure
    media = 'http://127.0.0.1:8000/static';
    
    // Customize the selector for your project
    $('div.comment-form form').submit(function(e) {
        ajaxComment({'media': media}, $(this), e);
        return false;
    });
});
