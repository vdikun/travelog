/*

the order of things.

page load: create container divs in divs. (do this in html).


#searchResults
  #mapView
  #mosaicView
  
 
initialization:
load #mapView and #mosaicView with photos array. (do this on form return.)

toggle.


toggle:
    hide one of the divs. show the other div.
    
the end


*/

var ViewManager = (function() {

	img_mosaic = "../static/img/mosaic.png";
	img_globe = "../static/img/globe.png";
	img_marker = "../static/img/point.png";

	var photoUrlBase = "../photo/";
	var photoSrcBase = "../static/img/"; 	

	var getPhotoUrl = function(photo) {
		return photoUrlBase + photo.id;
	};

	var getPhotoSrc = function(photo) {
		return photoSrcBase + photo.id + "." + photo.ext;
	};

	var getCenter = function(photos) {
		var latitudes = [],
			longitudes = [];

		$(photos).each(function(index, photo) {
			latitudes.push(photo.lat);
			longitudes.push(photo.lon);
		});

		var minLat = Math.min.apply(null, latitudes),
   			maxLat = Math.max.apply(null, latitudes),
			minLon = Math.min.apply(null, longitudes),
			maxLon = Math.max.apply(null, longitudes);

		return new google.maps.LatLng((minLat + maxLat)/2,(minLon + maxLon)/2);
	};

	var PathManager = (function() {
		var publicfunc = {
			getPathColor: function(i, len) {
				return tinycolor("#000000").lighten(25*i/len).toString();
			},
			getPathOpacity: function(i, len) {
				console.log(1 - (i/len));
				return 1 - (i/len);
			}
		};
		return publicfunc;
	});

	var that = this;

	var init = function(photos, map_view) {
		that.map_view = map_view;
		reload(photos);
	};

	that.init = init;

	var reload = function(photos) {
		console.log("displaying " + photos.length + " photos");
		init_map_view(photos);
		init_mosaic_view(photos);
		display_view();
	}

	that.reload = reload;

	var init_map_view = function(photos) {
		$("#map-canvas").remove();
		$('<div/>', {
		    id: 'map-canvas',
		    class: "map test",
		    height: "400px",
		    width: "700px"
		}).appendTo('#mapView');

		if (photos.length > 0) {
		  var mapOptions = {
		    zoom: 1,
		    center: getCenter(photos)
		  };
		  map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

			var markers = [];
			var locations = [];

			$( photos ).each(function( index, photo ) {
			  var location = new google.maps.LatLng(photo.lat,photo.lon);
			  locations.push(location);
			  var marker = new google.maps.Marker({
							map: map,
							position: location,
							icon: img_marker,
							size: new google.maps.Size(32, 32),
							origin: new google.maps.Point(0,0),
							anchor: new google.maps.Point(16,16)
						});
			  google.maps.event.addListener(marker, 'click', function() {
			    window.location.href = getPhotoUrl(photo);
			  });
			  markers.push(marker);
			 });

			var path = [];
			var pm = new PathManager();

			for (var i=0; i<locations.length-1; i++) {
				var line = new google.maps.Polyline({
				    path: [locations[i], locations[i+1]],
				    geodesic: true,
				    strokeColor: pm.getPathColor(i, locations.length),
				    strokeOpacity: pm.getPathOpacity(i, locations.length),
				    //strokeOpacity: 0.1,
				    strokeWeight: 2
				  });
				line.setMap(map);
				path.push(line);
			}


		} else {
			$("#map-canvas").text("no photos!");
		}
		$("#mapView").append("Map view is initalized");
	}

	var init_mosaic_view = function(photos) {
		$("#mosaicView").text("Mosaic view is initalized");	
	}

	var display_view = function() {
		if (that.map_view) {
			$("#mapView").show();
			$("#mosaicView").hide();
			$("#toggleMosaic").show();
			$("#toggleMap").hide();
		} else {
			$("#mapView").hide();
			$("#mosaicView").show();
			$("#toggleMosaic").hide();
			$("#toggleMap").show();
		}
	}

	var toggle = function() {
		that.map_view = !that.map_view;
		display_view();
	}
	that.toggle = toggle;

});