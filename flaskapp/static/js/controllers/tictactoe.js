App.controller('tictactoeController', ['$scope','$http', function($scope,$http) {

  $scope.board = [
    [ { value: '-' }, { value: '-' }, { value: '-' } ],
    [ { value: '-' }, { value: '-' }, { value: '-' } ],
    [ { value: '-' }, { value: '-' }, { value: '-' } ]
  ];

  $scope.reset = function() {
    // TODO: set each cell.value = '-'
    $scope.board = [
    [ { value: '-' }, { value: '-' }, { value: '-' } ],
    [ { value: '-' }, { value: '-' }, { value: '-' } ],
    [ { value: '-' }, { value: '-' }, { value: '-' } ]
  ];
    
    $scope.currentPlayer = 'X';
    $scope.winner = false;
    $scope.cat = false;
  };
  
  $scope.reset();
  
  $scope.isTaken = function(cell) {
    return cell.value !== '-';
  };
  
  var checkForMatch = function(cell1, cell2, cell3) {
    return cell1.value === cell2.value && 
           cell1.value === cell3.value &&
           cell1.value !== '-';
  };
  
  var checkForEndOfGame = function() {
    // TODO: check for a rowMatch, columnMatch, or diagonalMatch
    
    // $scope.winner = rowMatch || columnMatch || diagonalMatch;
    
    // TODO: if we don't have a winner, check for cat
    
    return $scope.winner || $scope.cat;
  };
  
  $scope.move = function(cell) {
    cell.value = $scope.currentPlayer;
    if (checkForEndOfGame() === false) {
      $scope.currentPlayer = $scope.currentPlayer === 'X' ? 'O' : 'X';
    }
  };
  
 


}]);
