/* defines functionality of photo search form */
 
  var map_view_selected = true;
  var photos = [];

  /* what do with photos */

  var search_tags = [];

  function refresh_tags() {
    $( ".search_tag" ).remove();
    $.each( search_tags, function(index, value) {
        display_tag(value);
    });
    $('#tags').val(search_tags.join());
  }

  function display_tag(value) {
    $( "#search_tags" ).append( "<div class='search_tag float'>" 
        + value +
        "<div class='search_tag_close button float'>X</div></div>" );
  }

  // triggered by user action
  function add_tags(tagstring) {
    tags = tagstring.split(",");
    $.each( tags, function( index, value ) {
        tag = value.trim();
        search_tags.push(tag);
        display_tag(tag);        
    });
    $('#tags').val(search_tags.join());
  }

    /* mappicker */
  function showMap() {
    $("#latlngpicker").show();
    var center = map.getCenter();
    google.maps.event.trigger(map, 'resize');
    map.setCenter(center); 
  }

  function hideMap() {
    $("#latlngpicker").hide();
  }


  $(function() {

    /* initialize tags in form */
    refresh_tags();
    $('#tag_submit').click(function() {
        // get tags from tag_input
        // run add_tags
        input = $('#tag_input').val();
        console.log(input);
        if (input) {
            add_tags(input);
        }
        // clear input
        $('#tag_input').val('');
    });

    /* initialize zebra datepicker */
    $('#date_from').Zebra_DatePicker({
      direction: -1
    });
    $('#date_to').Zebra_DatePicker({
      direction: -1
    });

    /* toggle search form */
    $( "#search_bar" ).click(function() {
      if ($('#search_content').css('visibility') == 'hidden') {
        $('#search_content').css('visibility', 'visible');
      } else {
        $('#search_content').css('visibility', 'hidden');
      }
    });

    /* remove search tags */
    $('#search_tags').on('click', '.search_tag_close', function () {
        tag = $(this).parent().contents().get(0).nodeValue;
        $(this).parent().remove();               
          var index = search_tags.indexOf(tag);
          if (index != -1) {
              search_tags.splice(index, 1);
          }
          $('#tags').val(search_tags.join());
    });

    /* implements hover on buttons */
    // TODO make this work for dynamically generated elements >:(
  $(".button").bind({
    mouseenter: function () {
      $( this ).removeClass("button");
      $( this ).addClass("button_hover");
    },
    mouseleave: function () {
      $( this ).removeClass("button_hover");
      $( this ).addClass("button");
    }
  });

  // solution from http://stackoverflow.com/a/7385673
  $(document).mouseup(function (e)
  {
    //alert(map);
      var container = $("#latlngpicker");

      if (!container.is(e.target) // if the target of the click isn't the container...
          && container.has(e.target).length === 0) // ... nor a descendant of the container
      {
          container.hide();
      }
  });

  hideMap(); 

  /* AJAX */

    $('#searchForm').submit( function() {

        $.ajax({
            url     : $(this).attr('action'),
            type    : $(this).attr('method'),
            data    : $(this).serialize(),
            success : function( photos ) {
                viewManager.reload(photos);
              }
        });

        return false;
    });

    /* view handler */
    viewManager = new ViewManager();
    viewManager.init(photos, map_view_selected);

});