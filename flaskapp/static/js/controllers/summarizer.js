App.controller('summarizerController', ['$scope','$http', function($scope,$http) {
	
	// Main Javascript function that gets the search Results
	$scope.getSearchResults= function()
	{
		$http({url:'/getSummarizedResults',method:"POST",params:{searchString:$scope.searchString}}).
				then(function successCallback(response) {
					//alert(response.data);
					$scope.nouns=response.data['impNouns'];
					$scope.searchResults=response.data['text'];
				}, function errorCallback(response) { });

	}

}]);
