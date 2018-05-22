import subprocess

class CommandLineService(object):

    @staticmethod
    def run_command(command):
        # start = time.time()
        ret_code, output = subprocess.getstatusoutput(command)
        if ret_code == 1:
            raise Exception("FAILED: %s" % command)
        # end = time.time()
        # print "Finished in %s seconds" % (end - start)
        return output
