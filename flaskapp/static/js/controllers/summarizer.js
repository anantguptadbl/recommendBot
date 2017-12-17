App.controller('summarizerController', ['$scope','$http','$compile', function($scope,$http,$compile) {
	
$scope.myCtrl1=function()
{
	$scope.markerTextArray=[]
	var layer = new ol.layer.Tile({
        source: new ol.source.OSM()
      });

      var map = new ol.Map({
        layers: [layer],
        target: 'map',
        view: new ol.View({
          center: [0, 0],
          zoom: 2
        })
      });

      a1={'name1':{'lat':16,'lon':17},'name2':{'lat':19,'lon':20}}
	counter=1;
	for(var key in a1)
	{
	      var pos = ol.proj.fromLonLat([a1[key]['lat'],a1[key]['lon']]);		
      // Markers1
      var marker = new ol.Overlay({
        position: pos,
        positioning: 'center-center',
        element: document.getElementById('marker' + counter),
        stopEvent: false
      });
      map.addOverlay(marker);
	//$scope.markerText[counter-1]=key;
	$scope.markerTextArray.push(key);
	var markerText = new ol.Overlay({
	position: pos,
	element: document.getElementById('textmarker' + counter)
	});
	map.addOverlay(markerText);

	counter = counter + 1;

	}



      // Popup showing the position the user clicked
      var popup = new ol.Overlay({
        element: document.getElementById('popup')
      });
      map.addOverlay(popup);

      map.on('click', function(evt) {
        var element = popup.getElement();
        var coordinate = evt.coordinate;
        var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
            coordinate, 'EPSG:3857', 'EPSG:4326'));

        $(element).popover('destroy');
        popup.setPosition(coordinate);
        // the keys are quoted to prevent renaming in ADVANCED mode.
        $(element).popover({
          'placement': 'top',
          'animation': false,
          'html': true,
          'content': '<p>The location you clicked was:</p><code>' + hdms + '</code>'
        });
        $(element).popover('show');
      });
};

	// Main Javascript function that gets the search Results
	$scope.getSearchResults= function()
	{	
		$scope.markerTextArray=[];
		$scope.showSummarizerWaitingDiv=1;
		$http({url:'/getSummarizedResults',method:"POST",params:{searchString:$scope.searchString}}).
				then(function successCallback(response) {
					//alert(response.data);
					$scope.nouns=response.data['impNouns'];
					$scope.searchResults=response.data['text'];
					// The following section is for marking it on the MAP
					latLongDict=response.data['placeDict'];
					
					// Latest OpenLayers
					var layer = new ol.layer.Tile({
					source: new ol.source.OSM()
				      });

				      var map = new ol.Map({
					layers: [layer],
					target: 'map',
					view: new ol.View({
					  center: [0, 0],
					  zoom: 2
					})
				      });
					counter=1
					for (var key in latLongDict) 
					{
						if(latLongDict[key]['class']=='place')
						{
						     var pos = ol.proj.fromLonLat([latLongDict[key]['lat'],latLongDict[key]['lon']]);		
						      // Markers1
						      var marker = new ol.Overlay({
							position: pos,
							positioning: 'center-center',
							element: document.getElementById('marker' + counter),
							stopEvent: false
						      });
						      map.addOverlay(marker);
							//$scope.markerText[counter-1]=key;
							$scope.markerTextArray.push(key);
							var markerText = new ol.Overlay({
							position: pos,
							element: document.getElementById('textmarker' + counter)
							});
							map.addOverlay(markerText);

							counter = counter + 1;
						}
					}
					      map.on('click', function(evt) {
						var element = popup.getElement();
						var coordinate = evt.coordinate;
						var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
						    coordinate, 'EPSG:3857', 'EPSG:4326'));

						$(element).popover('destroy');
						popup.setPosition(coordinate);
						// the keys are quoted to prevent renaming in ADVANCED mode.
						$(element).popover({
						  'placement': 'top',
						  'animation': false,
						  'html': true,
						  'content': '<p>The location you clicked was:</p><code>' + hdms + '</code>'
						});
						$(element).popover('show');
					      });
					
				$scope.showSummarizerWaitingDiv=0;				
				}, function errorCallback(response) {
						$scope.showSummarizerWaitingDiv=0;				
					 });

	}

}]);
    
