class EnvironmentService(object):

    @staticmethod
    def isPi():
        return os.environ.get('CAMERA') == 'pi'
