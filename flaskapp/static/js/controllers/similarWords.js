App.controller('similarWordsController', ['$scope','$http', function($scope,$http) {
	$scope.currentWordTag=0;
	$scope.getWordRelationships=function()
	{
		console.log($scope.inputText)
		$http({url:'/getWordSimilarity',method:"POST",params:{data:$scope.inputText}}).
		then(function successCallback(response) 
		{ 
			console.log(response);
			$scope.words=response.data.words;
			$scope.distances=response.data.distances;
			$scope.arrayList = [];
			for (var i = 0; i != $scope.words.length - 1; ++i) $scope.arrayList.push(i)
			
		}); 
	}

	$scope.getWordScores=function(curWord)
	{
		//document.getElementById('finalTable').DataTable();
		$('#finalTable').DataTable();
		$scope.curWord=curWord;
		console.log(curWord);
		console.log($scope.words.indexOf(curWord))
		$scope.currentWordTag=$scope.words.indexOf(curWord);
	}
}]);
