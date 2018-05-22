(function() {
    const appModule = angular.module('app', ['ngMaterial', 'ui.router']);

    appModule
        .config(($stateProvider, $urlRouterProvider) => {
            $stateProvider
                .state({
                    name: 'recording-page',
                    url: '/',
                    template: '<recording-page></recording-page>'
                });
            
            $urlRouterProvider.otherwise('/');
        });

})();
