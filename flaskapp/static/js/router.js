App.config(function($routeProvider) {
  $routeProvider
	.when('/', {
	templateUrl: 'static/views/about.html',
	controller: 'aboutController'
	})
	.when('/about', {
	templateUrl: 'static/views/about.html',
	controller: 'aboutController'
	})
	.when('/tictactoe', {
	templateUrl: 'static/views/tictactoe.html',
	controller: 'tictactoeController'
	})
	.when('/summarizer', {
	templateUrl: 'static/views/summarizer.html',
	controller: 'summarizerController'
	})
	.when('/similarWords', {
	templateUrl: 'static/views/similarWords.html',
	controller: 'similarWordsController'
	})
	.when('/contact', {
	templateUrl: 'static/views/contact.html',
	controller: 'contactController'
	})
/*
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
