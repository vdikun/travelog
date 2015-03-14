/* defines functionality of photo search form */

  search_tags = [];

  function refresh_tags() {
    $( ".search_tag" ).remove();
    $.each( search_tags, function(index, value) {
        display_tag(value);
    });
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
    $( ".search_tag_close" ).click(function() {
      // selects tag value
      tag = $(this).parent().contents().get(0).nodeValue;
      $(this).parent().remove();               
        var index = search_tags.indexOf(tag);
        if (index != -1) {
            search_tags.splice(index, 1);
        }
    });

    /* implements hover on buttons */
    $( ".button" ).hover(
      function() {
        $( this ).removeClass("button");
        $( this ).addClass("button_hover");
      }, function() {
        $( this ).removeClass("button_hover");
        $( this ).addClass("button");
      }
    );

    /* mappicker */
	map = getMap();

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


});