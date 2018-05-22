(function () {

  class RootReducer {

    constructor(
      recordingPageReducer
    ) {
      this.recordingPageReducer = recordingPageReducer;
    }

    reduce(action, rootState) {
      return {
        recordingPage: this.recordingPageReducer.reduce(action, rootState.recordingPage),
      };
    }

    getDefaultRootState() {
      return {
        recordingPage: this.recordingPageReducer.getDefaultState(),
      };
    }

  }

  RootReducer.$inject = ['recordingPageReducer'];

  angular.module('app').service('rootReducer', RootReducer);

})();