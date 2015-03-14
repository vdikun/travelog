/*
 *  functions for search page display logic
 *  and possibly the most rambling JS class i've ever written
 *  may the Lord have mercy on my soul
 */

 var ViewManager = (function() {
 
 	var that = this; // ??!!

	img_mosaic = "../static/img/mosaic.png";
	img_globe = "../static/img/globe.png";
	img_marker = "../static/img/point.png";

	that.mapview_id = "mapView";
	that.mosaicview_id = "mosaicView";
	that.mapview_toggle_id = "mapToggle";
	that.mosaicview_toggle_id = "mosaicToggle";


	var PhotoManager = (function() {

		var photoUrlBase = "../photo/";
		var photoSrcBase = "../static/img/"; //TODO change to '/img/photo/'

		var publicfunc = {

			// TODO
			getCenter: function(photos) {
				return new google.maps.LatLng(18, 32);
			},

			// TODO
			getZoom: function(photos) {
				return 9;
			},
            
			getPhotoUrl: function(photo) {
				return photoUrlBase + photo.id;
			},

			getPhotoSrc: function(photo) {
				return photoSrcBase + photo.id + "." + photo.ext;
			}
		};
		return publicfunc;

	});

	var PathManager = (function() {
		var publicfunc = {
			getPathColor: function(i, len) {
				return "red";
			},
			getPathOpacity: function(i, len) {
				return 1 - (i/len);
			}
		};
		return publicfunc;
	});

 	goto = function(url) {
 		window.location.href = url;
 	};

	display_view = function() {

	    if(that.map_view) {
	        $('#' + that.mapview_id).show();
			$('#' + that.mosaicview_toggle_id).show();
			$('#' + that.mosaicview_id).hide();
			$('#' + that.mapview_toggle_id).hide();
	    } else {
	        $('#' + that.mosaicview_id).show();
			$('#' + that.mapview_toggle_id).show();
	        $('#' + that.mapview_id).hide();
			$('#' + that.mosaicview_toggle_id).hide();
	    }
	};

 	init_toggle_icons = function() {
		// toggle map icon
		$('<img/>', {
		    id: that.mapview_toggle_id,
		    src: img_globe,
		    onClick: toggle,
		    position: "absolute",
		    left: "50px",
		    bottom: "50px"
		}).appendTo(that.selector);

		// toggle mosaic icon
		$('<img/>', {
		    id: that.mosaicview_toggle_id,
		    src: img_mosaic,
		    onClick: toggle,
		    position: "absolute",
		    left: "50px",
		    bottom: "50px"
		}).appendTo(that.selector);

		// hide newly created elements until they are needed
		$("#" + that.mosaicview_toggle_id).hide();
		$("#" + that.mapview_toggle_id).hide();	
 	};

 	init_map_view = function() {

		var myDiv = document.createElement('div');
		myDiv.id = that.mapview_id;
		document.body.appendChild(myDiv);

		map = new google.maps.Map(document.getElementById(that.mapview_id), {
			center: that.pm.getCenter(that.photos),
			zoom: that.pm.getZoom(that.photos),
			mapTypeId: 'roadmap'
			});

		var markers = [];
		var locations = [];

		$( that.photos ).each(function( index, value ) {
		  var location = new google.maps.LatLng(value.lat,value.lng);
		  locations.push(location);
		  var marker = new google.maps.Marker({
						map: map,
						position: location,
						icon: img_marker
					});
		  google.maps.event.addListener(marker, 'click', function() {
		    goto(that.pm.getPhotoUrl(photo.id));
		  });
		  markers.push(marker);
		});

		var path = [];

		for (var i=0; i++; i<locations.length-1) {
			var line = new google.maps.Polyline({
			    path: [locations[i], locations[i+1]],
			    geodesic: true,
			    strokeColor: that.pathManager.getPathColor(i, locations.length),
			    strokeOpacity: that.pathManager.getPathOpacity(i, locations.length),
			    strokeWeight: 2
			  });
			line.setMap(map);
			path.push(line);
		} 		
 	};

	init_mosaic_view = function() {

		container = $('<div/>', {
		    id: that.mosaicview_id
		});

		if (that.photos) {
			$( that.photos ).each(function( index, photo ) {
				$("<img />")
				 .attr({
				   "src": that.pm.getPhotoSrc(photo),
				   "class": 'photo_thumb float'
				 })
				 .wrap('<a href="' + that.pm.getPhotoUrl(photo) + '"/>')
				 .parent()
				 .appendTo(container);
			});
		} else {
			(container).append("<p>No photos found.<\p>");
		}	

		container.appendTo("#" + that.selector);
	};

	var toggle = function(map_view) {
		alert("toggle");
		that.map_view = map_view;
		display_view();
	};
	that.toggle = toggle;

	var init = function(selector, photos, map_view) {

 		that.selector = selector;
 		that.photos = photos;
 		that.map_view = map_view;
 		that.pm = new PhotoManager();
 		that.pathManager = new PathManager();

 		$("#" + that.selector).empty();
 		init_map_view();
		init_mosaic_view();
		init_toggle_icons();

		display_view();
	};
	that.init = init;

	that.display_photos = function (photos) {
		that.init(that.selector, photos, that.map_view);
	}

});