App.controller('tictactoeController', ['$scope','$http', function($scope,$http) {
	
	// Init stuff
	$scope.boardHistory=[];
	$scope.currentWinner=999;
	$scope.board = [
	[ { value: '-' }, { value: '-' }, { value: '-' } ],
	[ { value: '-' }, { value: '-' }, { value: '-' } ],
	[ { value: '-' }, { value: '-' }, { value: '-' } ]
	];

	$scope.reset = function() {
		// At this point, we will send over new data for training
		$http({url:'/reTrainModel',method:"POST",params:{allSteps:JSON.stringify($scope.boardHistory),label:$scope.currentWinner}}).
		then(function successCallback(response) { }); 
		
		$scope.board = [
		[ { value: '-' }, { value: '-' }, { value: '-' } ],
		[ { value: '-' }, { value: '-' }, { value: '-' } ],
		[ { value: '-' }, { value: '-' }, { value: '-' } ]
		];
		//$scope.currentPlayer = 'X';
		//$scope.winner = false;
		//$scope.cat = false;
		$scope.boardHistory=[];
		$scope.currentWinner=999;
	};

	$scope.isTaken = function(cell) 
	{
		return cell.value !== '-';
	};

	var checkForMatch = function(cell1, cell2, cell3) 
	{
		return cell1.value === cell2.value && cell1.value === cell3.value &&  cell1.value !== '-';
	};

	//return $scope.winner || $scope.cat;
	//};


	
	// Function to check whether somebody has won
	$scope.checkWinner = function()
	{
		$http({url:'/checkWinner',method:"POST",params:{currentState:JSON.stringify($scope.board)}}).
			then(function successCallback(response) 
			{
			$scope.currentWinner=response.data;
			if($scope.currentWinner[0]==-1) 
			{ 
				alert("X wins"); 
				$scope.currentWinner=-1;
			};
			if($scope.currentWinner[0]==1) 
			{ 
				alert("O wins"); 
				$scope.currentWinner=1;
			};
			if($scope.currentWinner[0]==0) 
			{ 
				alert("No one wins"); 
				$scope.currentWinner=999;
			};
			if($scope.currentWinner[0]=999)
			{
				console.log("Game continues");
			};
	})};

	$scope.move = function(cell) {
		
	// This will get activated only when the current state is 999 state
	if($scope.currentWinner==999)
	{

		// Update  the boardHistory
		$scope.boardHistory.push($scope.board);
		cell.value = 'X';
			
		// Check if anybody is winning at this point
		$scope.checkWinner();

		if($scope.currentWinner==999)
		{
			// Update the next computer move
			$http({url:'/getNextMove',method:"POST",params:{currentState:JSON.stringify($scope.board)}}).
			then(function successCallback(response) {
				//alert(response.data);
				$scope.board=response.data;
				// Update  the boardHistory
				$scope.boardHistory.push($scope.board)
	
			// Check if anybody is winning at this point
			$scope.checkWinner();

			}, function errorCallback(response) { });

		};		
			
		//if (checkForEndOfGame() === false) {
		//$scope.currentPlayer = $scope.currentPlayer === 'X' ? 'O' : 'X';
		//}
	}; // End of the valid 999 function
  
	}; // End of the move function


}]);
