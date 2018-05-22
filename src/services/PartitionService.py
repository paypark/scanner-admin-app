import os
import psutil

from CommandLineService import CommandLineService

class PartitionService(object):
    mountPath = "/media/usb"

    @staticmethod
    def getMountPath():
        # print('[PartitionService] getMountPath()')
        return PartitionService.mountPath

    @staticmethod
    def mount():
        # print('[PartitionService] getMountPath()')
        if not PartitionService.doesMountablePartitionExist():
            return 500, "No mountable partition exists"

        PartitionService.do_mount()
        if PartitionService.doesUnmountablePartitionExist():
            return 200, "Success"

        return 500, "Error during mounting"

    @staticmethod
    def ensureIsMounted():
        # print('[PartitionService] ensureIsMounted()')
        if PartitionService.doesUnmountablePartitionExist():
            return
        if PartitionService.doesMountablePartitionExist():
            PartitionService.do_mount()
            return
        else:
            raise Exception('no mountable partition!')

    @staticmethod
    def getPartitions():
        # print('[PartitionService] getPartitions()')
        command = "lsblk -l"
        output = CommandLineService.run_command(command)
        lines = PartitionService.getLines(output)
        partitions = []
        for line in lines:
            partitions.append(PartitionService.partitionFactory(line))
        return partitions

    @staticmethod
    def getLines(input):
        return input.splitlines()

    @staticmethod
    def getColumns(input):
        stranglyEncoded = input.split()
        columns = []
        for item in stranglyEncoded:
            columns.append(item.decode('utf-8').strip())
        return columns

    @staticmethod
    def partitionFactory(input):
        columns = PartitionService.getColumns(input)
        return dict(
            name = columns[0],
            size = columns[3],
            type = columns[5],
            path = "/dev/" + columns[0]
        )

    @staticmethod
    def getMountablePartition():
        partitions = PartitionService.getPartitions()
        for partition in partitions:
            if PartitionService.isValidPartition(partition) and not PartitionService.isMounted(partition['path']):
                return partition
        raise Exception('no mountable partition found!')

    @staticmethod
    def doesMountablePartitionExist():
        partitions = PartitionService.getPartitions()
        # print("##############################")
        # print("doesMountablePartitionExist()")
        for partition in partitions:
            # if partition['name'].startswith('sd'):
                # print("  partition => name: " + partition['name'] + ", path: " + partition['path'] + ", mounted: " + str(PartitionService.isMounted(partition['path'])))
            if PartitionService.isValidPartition(partition) and not PartitionService.isMounted(partition['path']):
                return True
        return False

    @staticmethod
    def doesUnmountablePartitionExist():
        partitions = PartitionService.getPartitions()
        for partition in partitions:
            # if partition['name'].startswith('sd'):
                # print("  partition => name: " + partition['name'] + ", path: " + partition['path'] + ", mounted: " + str(PartitionService.isMounted(partition['path'])))
            if PartitionService.isValidPartition(partition) and PartitionService.isMounted(partition['path']):
                return True
        return False

    @staticmethod
    def isLargerThan1GB(sizeString):
        return sizeString[-1:] == 'G'

    @staticmethod
    def isValidPartition(input):
        if not input['name'].startswith('sd'):
            return False
        if input['type'] != 'part':
            return False
        return PartitionService.isLargerThan1GB(input['size'])

    @staticmethod
    def isMounted(partitionPath):
        mountedPartitions = psutil.disk_partitions()
        for partition in mountedPartitions:
            # print("[PartitionService] isMounted(): [mounted: " + partition.device + "]")
            if partition.device == partitionPath:
                # print("[PartitionService] isMounted(): " + partitionPath + ": True")
                return True
        # print("[PartitionService] isMounted(): " + partitionPath + ": False")
        return False

    @staticmethod
    def do_mount():
        # print('[PartitionService] do_mount()')
        # print("mount(): " + PartitionService.mountPath)
        partition = PartitionService.getMountablePartition()

        if not os.path.exists(PartitionService.mountPath):
            os.makedirs(PartitionService.mountPath)

        command = "mount " + partition['path'] + " " + PartitionService.mountPath
        print(command)
        result = CommandLineService.run_command(command)
        print(result)

    @staticmethod
    def do_unmount():
        # print('[PartitionService] do_unmount()')
        # print("do_unmount(): " + PartitionService.mountPath)
        command = "umount " + PartitionService.mountPath
        print(command)
        result = CommandLineService.run_command(command)
        print(result)

    @staticmethod
    def getNumberOfFreeBytes():
        # print('[PartitionService] getNumberOfFreeBytes()')
        statvfs = os.statvfs(PartitionService.mountPath)
        return statvfs.f_frsize * statvfs.f_bavail

    @staticmethod
    def isSufficientDiskSpaceAvailable(filePath):
        # print('[PartitionService] isSufficientDiskSpaceAvailable()')
        numberOfFreeBytes = PartitionService.getNumberOfFreeBytes()
        fileSizeInBytes = os.path.getsize(filePath)
        # print("isSufficientDiskSpaceAvailable(): numberOfFreeBytes: " + str(numberOfFreeBytes))
        # print("isSufficientDiskSpaceAvailable(): fileSizeInBytes  : " + str(fileSizeInBytes))
        return numberOfFreeBytes > fileSizeInBytes