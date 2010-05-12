$(document).ready(function() {
    previewed = false;
    
    commentBusy = false;
});

function ajaxComment(args, form, e) {
    // TODO: if the media variable ends in a forward slash, remove it.
    var media = args.media;
    
    $('div.comment-error').remove();
    
    if (commentBusy) {
        form.before('\
            <div class="comment-error">\
                Your comment is currently in the process of posting.\
            </div>\
        ');
        $('div.comment-error').fadeOut(2000);
        
        return false;
    }
    
    comment = form.serialize();
   
    // Add a wait animation
    $('input.submit-post', form).after('\
        <img src="' + media + '/img/ajax-wait.gif" alt="Please wait..."\
            class="ajax-loader" />\
    ');
    
    // Indicate that the comment is being posted
    $('p.submit').after('\
        <div class="comment-waiting" style="display: none;">\
            One moment while the comment is posted. . .\
        </div>\
    ');
    $('div.comment-waiting').fadeIn(1000);
    
    commentBusy = true;
    
    url = form.attr('action');
    
    // Use AJAX to post the comment.
    $.ajax({
        type: 'POST',
        url: url,
        data: comment,
        success: function(data) {
            commentBusy = false;
        
            removeWaitAnimation();
            console.log(data.success);
            if (data.success == true) {
                commentSuccess(data,form,e);
            } else {
                commentFailure(data,form,e);
            }
        },
        error: function(data) {
            commentBusy = false;
            
            removeWaitAnimation(form);
            form.unbind('submit');
            $('.submit-post', form).click();
        },
        dataType: 'json'
    });
    
    return false;
}

function commentSuccess(data,form,e) {
    
    console.log("inside success");
    console.log($('input[type=text]',form));
    $('input[type=text]',form)[0].value = "";
    console.log(form.parents(".comments"));
    form.parents(".comments").prepend(data["html"]);
    form.parents(".comments .comment:first").show('slow');

}

function commentFailure(data) {
    removeWaitAnimation(form);
    form.unbind('submit');
    $('.submit-post', form).click();
    return true;
}

function removeWaitAnimation() {
    // Remove the wait animation and message
    $('.ajax-loader').remove();
    $('div.comment-waiting').stop().remove();
}
