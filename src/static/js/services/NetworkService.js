(function () {

  const SETTINGS_PATH = '/settings';
  const INSCREASE_PATH = '/increase';
  const DECREASE_PATH = '/decrease';
  const RECORDING_PATH = '/recording';
  const USB_PATH = '/usb';

  class NetworkService {

    constructor($http) {
      this.$http = $http;

    }

    recordingStart() {
      const options = {
        method: 'GET',
        url: RECORDING_PATH + '/start',
      };
      return this._executeAndUnpack(options);
    }

    recordingEnd() {
      const options = {
        method: 'GET',
        url: RECORDING_PATH + '/stop',
      };
      return this._executeAndUnpack(options);
    }

    status() {
      const options = {
        method: 'GET',
        url: '/status',
      };
      return this._executeAndUnpack(options);
    }

    increase() {
      const options = {
        method: 'GET',
        url: INSCREASE_PATH,
      };
      return this._executeAndUnpack(options);
    }

    decrease() {
      const options = {
        method: 'GET',
        url: DECREASE_PATH,
      };
      return this._executeAndUnpack(options);
    }

    getSettings() {
      const options = {
        method: 'GET',
        url: SETTINGS_PATH,
      };
      return this._executeAndUnpack(options);
    }

    patchSettings(settings) {
      const options = {
        method: 'POST',
        url: SETTINGS_PATH,
        data: settings,
      };
      return this._executeAndUnpack(options);
    }

    mountUsb() {
      const options = {
        method: 'GET',
        url: USB_PATH + '/mount',
      };
      return this._executeAndUnpack(options);
    }

    unmountUsb() {
      const options = {
        method: 'GET',
        url: USB_PATH + '/unmount'
      };
      return this._executeAndUnpack(options);
    }

    _executeAndUnpack(options) {
      return this
        .$http(options)
        .then(response => response.data);
    }

  }

  NetworkService.$inject = ['$http'];

  angular.module('app').service('networkService', NetworkService);

})();