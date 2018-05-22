(function () {

  class RecordingPageReducer {

    constructor(recordingPageActions) {
      this.recordingPageActions = recordingPageActions;
    }

    getDefaultState() {
      return {
        isUsbMounted: true,
        isRecording: false,
        isStreamShowing: false,
        isSnapshotShowing: false,
        cameraSettings: {
          frameRate: null,
          height: null,
          iso: null,
          shutterSpeed: null,
          width: null,
        },
      };
    }

    reduce(action, state) {
      switch (action.type) {
        case this.recordingPageActions.START_RECORDING:
          return Object.assign({}, state, { isRecording: true });

        case this.recordingPageActions.STOP_RECORDING:
          return Object.assign({}, state, { isRecording: false });

        case this.recordingPageActions.SET_USB_MOUNTED:
          return Object.assign({}, state, { isUsbMounted: action.payload.isUsbMounted });

        case this.recordingPageActions.SET_CAMERA_SETTINGS:
          return Object.assign({}, state, { cameraSettings: action.payload.cameraSettings });

        case this.recordingPageActions.SET_SHOW_STREAM:
          return Object.assign({}, state, { isStreamShowing: action.payload.isStreamShowing });

        case this.recordingPageActions.SET_SNAPSHOW_SHOW:
          return Object.assign({}, state, { isSnapshotShowing: action.payload.isSnapshotShowing });

        default:
          return state;
      }
    }

  }

  RecordingPageReducer.$inject = ['recordingPageActions'];

  angular.module('app').service('recordingPageReducer', RecordingPageReducer);
})();