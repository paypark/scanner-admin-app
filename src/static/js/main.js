// handlers

function onIncreaseButtonClick() {
    increase();
}

function onDecreaseButtonClick() {
    decrease();
}

function onShowStreamButtonClick() {
    showStream(); 
}

function onHideStreamButtonClick() { 
    hideStream();
}

function onSaveSettingsButtonClick() { 
    saveSettings();
}

// controllers

const increase = () => {
    console.log('increase()');
    NetworkService.increase();
};

const decrease = () => {
    console.log('decrase()');
    NetworkService.decrease();
};

const getSettings = () => {
    NetworkService.getSettings()
        .then(settings => showUpdatedSettings(settings));
};

const startRecording = () => {
    console.log('startRecording()');
    showRecording();
    hideUnmount();
    NetworkService.recordingStart();
};

const stopRecording = () => {
    console.log('stopRecording()');
    showNotRecording();
    showRecording();
    NetworkService.recordingEnd();
};

const updateStatus = () => {
    console.log('updateStatus()');
    NetworkService.status()
        .then(({ isRecording, isUsbConnected }) => {
            window.isRecording
                ? showRecording()
                : showNotRecording();
            window.isUsbConnectedisUsbConnected
                ? showUsbConnected()
                : showUsbNotConnected();
            window.isUsbConnected && !isRecording
                ? showUnmount()
                : hideUnmount();
            setTimeout(() => updateStatus(), 2000);
        });
};

function saveSettings() {
    console.log('saveSettings()');
    const shutterSpeedInputElement = document.querySelector('.shutter-speed');
    const frameRateInputElement = document.querySelector('.frame-rate');
    const isoInputElement = document.querySelector('.iso');
    const heightInputElement = document.querySelector('.height');
    const widthInputElement = document.querySelector('.width');

    const settings = {
        shutterSpeed: parseInt(shutterSpeedInputElement.value, 10),
        frameRate: parseInt(frameRateInputElement.value, 10),
        iso: parseInt(isoInputElement.value, 10),
        height: parseInt(heightInputElement.value, 10),
        width: parseInt(widthInputElement.value, 10),
    };

    NetworkService.patchSettings(settings)
        .then(() => console.log('success!!!'));
}

// network calls

const SETTINGS_PATH = '/settings';
const INSCREASE_PATH = '/increase';
const DECREASE_PATH = '/decrease';
const RECORDING_PATH = '/recording';

class NetworkService {

    static recordingStart() {
        return fetch(RECORDING_PATH + '/start');
    }

    static recordingEnd() {
        return fetch(RECORDING_PATH + '/stop');
    }

    static status() {
        return fetch('/status')
            .then(response => response.json());
    }

    static increase() {
        return fetch(INSCREASE_PATH);
    }

    static decrease() {
        return fetch(DECREASE_PATH);
    }

    static getSettings() {
        return fetch(SETTINGS_PATH)
            .then(response => response.json());
    }

    static patchSettings(settings) {
        const options = { 
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        };
        return fetch(SETTINGS_PATH, options);
    }
    
}

// view manipulators

function showStream() {
    const streamContainerElement = document.querySelector('.stream-container');
    streamContainerElement.innerHTML = '<img class="video-stream" src="/video_feed" >';
}

function hideStream() {
    const streamContainerElement = document.querySelector('.stream-container');
    streamContainerElement.innerHTML = '';
}

function showUpdatedSettings(settings) {
    const shutterSpeedInputElement = document.querySelector('.shutter-speed');
    shutterSpeedInputElement.value = settings.shutterSpeed;

    const frameRateInputElement = document.querySelector('.frame-rate');
    frameRateInputElement.value = settings.frameRate;

    const isoInputElement = document.querySelector('.iso');
    isoInputElement.value = settings.iso;

    const widthInputElement = document.querySelector('.width');
    widthInputElement.value = settings.width;

    const heightInputElement = document.querySelector('.height');
    heightInputElement.value = settings.height;
}

function showRecording() {
    console.log('showRecording()');
    const recordingContainerElement = document.querySelector('.recording-container');
    recordingContainerElement.innerHTML = '';

    const imageElement = document.createElement('img');
    imageElement.src = '/assets/icons/stop.svg';
    const buttonElement = document.createElement('button');
    buttonElement.addEventListener('click', () => stopRecording());
    buttonElement.classList.add('recording-button');
    buttonElement.classList.add('fab-button');
    buttonElement.appendChild(imageElement);

    recordingContainerElement.appendChild(buttonElement);
}

function showNotRecording() {
    console.log('showNotRecording()');
    const recordingContainerElement = document.querySelector('.recording-container');
    recordingContainerElement.innerHTML = '';

    const imageElement = document.createElement('img');
    imageElement.src = '/assets/icons/record.svg';
    const buttonElement = document.createElement('button');
    buttonElement.addEventListener('click', () => startRecording());
    buttonElement.classList.add('recording-button');
    buttonElement.classList.add('fab-button');
    buttonElement.appendChild(imageElement);

    recordingContainerElement.appendChild(buttonElement);
} 

function showUsbConnected() {
    const usbIconSvgElement = document.querySelector('.usb-connected');
    usbIconSvgElement.classList.remove('inactive-icon');
}

function showUsbNotConnected() {
    const usbIconSvgElement = document.querySelector('.usb-connected');
    usbIconSvgElement.classList.add('inactive-icon');
}

function showUnmount() {
    const unmountContainerElement = document.querySelector('.unmount-container');
    unmountContainerElement.innerHTML = '';

    const imageElement = document.createElement('img');
    imageElement.src = '/assets/icons/eject.svg';
    const buttonElement = document.createElement('button');
    buttonElement.addEventListener('click', () => console.log('unmount...'));
    buttonElement.classList.add('unmount-button');
    buttonElement.classList.add('fab-button');
    buttonElement.appendChild(imageElement);

    unmountContainerElement.appendChild(buttonElement);
}

function hideUnmount() {
    const unmountContainerElement = document.querySelector('.unmount-container');
    unmountContainerElement.innerHTML = '';
}

function initialize() {
    getSettings();
    showNotRecording();
    updateStatus();
    showUsbNotConnected();

    //
    showUnmount();
}

initialize();
