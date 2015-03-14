function show_thumb(element, photo) {
    $(element).append(
    "<div class=thumb>\
      <a href='/photo/" + photo.id + "'>\
      <img src='" + photo.img_uri + "' class=thumb_img></img>\
      </a>\
    </div>"
    )
}

function get_photo_success(response) {
    $('#photos').empty();
    if (response.length === 0) {
        $('#photos').text("No photos found.");
    } else {
        $('#photos').append(response.length + " photos found.<p>");
        $(response).each(function( index ) {
            var obj = response[index];
            show_thumb('#photos', obj);
        });
    }
}

function redirect_to_index() {
  console.log("redirect to index");
  window.location.replace("/");
  return false;
}

$(function() {

    // get photos
    jQuery('#photoform').submit( function() {
        
        $.ajax({
            url     : $(this).attr('action'),
            type    : $(this).attr('method'),
            data    : $(this).serialize(),
            success : function( response ) { get_photo_success( response ) }
        });

        return false;
    });
    
    // autoload
    // TODO restrict to specific pages/contexts
    /*
    $.get( "/photos/", function( response ) {
      get_photo_success( response );
    });
    */
    
    // upload photos
    /*
    jQuery('#uploadform').submit( function() {
        
        $.ajax({
            url     : $(this).attr('action'),
            type    : $(this).attr('method'),
            success : function( response ) { 
                console.log ( response );
                alert( response )
            }
        });

        return false;
    }); 
    */
    $('#uploadform').attr('onsubmit', 'redirect_to_index()');
});
