App.config(function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'static/views/welcome.html',
      controller: 'View1Controller'
    })
    .when('/tictactoe', {
      templateUrl: 'static/views/tictactoe.html',
      controller: 'tictactoeController'
    })/*
    .when('/movierecommender', {
      templateUrl: 'static/views/movieRecommendation.html',
      controller: 'controller2'
    })
    .when('/greencover', {
      templateUrl: 'static/views/greenCover.html',
      controller: 'controller3'
    })
    .when('/wikitrivia', {
      templateUrl: 'static/views/wikiTrivia.html',
      controller: 'controller4'
    })*/
    .otherwise({
      redirectTo: '/404'
    });
});
