(function () {

  class RecordingPageController {

    constructor($interval, store, recordingPageActions, networkService) {
      this.store = store;
      this.recordingPageActions = recordingPageActions;
      this.networkService = networkService;

      this.store.subscribe(({ recordingPage }) => {
        this.recordingPage = recordingPage;
      });

      this.networkService
        .getSettings()
        .then(cameraSettings => this.store.dispatch(this.recordingPageActions.setCameraSettings(cameraSettings)));

      const updateStatus = () => {
        this.networkService
          .status()
          .then(({ isUsbConnected, isRecording }) => {
            this.store.dispatch(this.recordingPageActions.setUsbMounted(isUsbConnected));
            this.store.dispatch(
              isRecording
                ? this.recordingPageActions.startRecording()
                : this.recordingPageActions.stopRecording()
            );
          });
      };
      updateStatus();
      $interval(() => updateStatus(), 5000);
    }

    onRecordClick() {
      console.log('onRecordClick()');
      this.store.dispatch(this.recordingPageActions.startRecording());
      this.networkService.recordingStart();
    }

    onStopClick() {
      console.log('onStopClick()');
      this.store.dispatch(this.recordingPageActions.stopRecording());
      this.networkService.recordingEnd();
    }

    onMountClick() {
      console.log('onMountClick()');
      this.store.dispatch(this.recordingPageActions.setUsbMounted(true));
      this.networkService.mountUsb();
    }

    onUnmountClick() {
      console.log('onUnmountClick()');
      this.store.dispatch(this.recordingPageActions.setUsbMounted(false));
      this.networkService.unmountUsb()
    }

    onSettingsSaveClick() {
      console.log('onSettingsSaveClick()');
      const cameraSettingsClone = JSON.parse(JSON.stringify(this.recordingPage.cameraSettings));
      this.networkService
        .patchSettings(cameraSettingsClone)
        .then(() => this.store.dispatch(this.recordingPageActions.setCameraSettings(cameraSettingsClone)));
    }

    onStreamShowClick() {
      console.log('onStreamShowClick');
      this.store.dispatch(this.recordingPageActions.setShowStream(true));
    }

    onStreamHideClick() {
      console.log('onStreamHideClick');
      this.store.dispatch(this.recordingPageActions.setShowStream(false));
    }

    onSnapshotShowClick() {
      console.log('onSnapshotShowClick');
      this.store.dispatch(this.recordingPageActions.setShowSnapshot(true));
    }

    onSnapshotHideClick() {
      console.log('onSnapshotHideClick');
      this.store.dispatch(this.recordingPageActions.setShowSnapshot(false));
    }

  }

  RecordingPageController.$inject = ['$interval', 'store', 'recordingPageActions', 'networkService'];

  angular.module('app')
    .component('recordingPage', {
      templateUrl: '/js/containers/recording-page/recording-page.template.html',
      controller: RecordingPageController
    });
})();