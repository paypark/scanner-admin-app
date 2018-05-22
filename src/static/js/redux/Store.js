(function () {

  class Store {

    constructor($rootScope, rootReducer) {
      this.$rootScope = $rootScope;
      this.rootReducer = rootReducer;
      this._rootState = rootReducer.getDefaultRootState();
      this._previousRootState = this._rootState;
      this._pageLevelSubscriptions = [];
      this._appLevelSubscriptions = [];
      this._attachListeners();
    }

    getState() {
      return this._rootState;
    }

    getPreviousRootState() {
      return this._previousRootState;
    }

    dispatch(action) {
      this._previousRootState = this._rootState;
      this._rootState = this.rootReducer.reduce(action, this._previousRootState);
      [...this._appLevelSubscriptions, ...this._pageLevelSubscriptions]
        .forEach(subscription => subscription(this._rootState, this._previousRootState));

      console.log('--------------------------');
      console.log('action:', action);
      console.log('current state:', this._previousRootState);
      console.log('next    state:', this._rootState);
    }

    subscribe(callback, isApplicationLevel = false) {
      if (isApplicationLevel) {
        this._appLevelSubscriptions.push(callback);
      } else {
        this._pageLevelSubscriptions.push(callback);
      }
      callback(this._rootState, this._previousRootState);
    }

    _attachListeners() {
      this.$rootScope.$on('$stateChangeStart', () => this._unsubscribeAll());
    }

    _unsubscribeAll() {
      this._pageLevelSubscriptions = [];
    }

  }

  Store.$inject = ['$rootScope', 'rootReducer'];

  angular.module('app').service('store', Store);

})();