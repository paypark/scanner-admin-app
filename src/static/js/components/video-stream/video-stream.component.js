(function() {

  class VideoStreamController {
    constructor() {
      console.log('[VideoStreamController] constructor(): this.url:', this.url);
    }
  }

  angular.module('app')
    .component('videoStream', {
      templateUrl: '/js/components/video-stream/video-stream.template.html',
      controller: VideoStreamController,
      bindings: {
        url: '<',
      }
    });

})();