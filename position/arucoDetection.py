import requests
import cv2
import numpy as np
import imutils
import time


class arucoDetection:

    def __init__(self, camUrl, arucoMarkerSize = 0.02, arucoMarkerType = cv2.aruco.DICT_4X4_50):
        self.arucoMarkerSize = arucoMarkerSize
        self.arucoMarkerType = arucoMarkerType
        self.intrinsicCamera = np.array(((933.15867, 0, 657.59),(0,933.1586, 400.36993),(0,0,1)))
        self.distortion = np.array((-0.43948,0.18514,0,0))
        self.camUrl = camUrl
        # self.intrinsicCamera = np.array(((916.43246, 0, 318.554126),(0, 911.78896, 249.648667),(0,0,1)))
        # self.distortion = np.array((-0.069533, 0.979625, 0.005022, 0.008359999999999999, 0))
        self.origin = None

        # self.cap =  cv2.VideoCapture(5)

    
    def setOrigin(self,arucoId):


        image = requests.get(self.camUrl)
        imgageArray = np.array(bytearray(image.content), dtype=np.uint8)
        image = cv2.imdecode(imgageArray, -1)
        # ret, image = self.cap.read()
        estimatedPose = self.__estimatePose(image, arucoId)


        if(len(estimatedPose)):
            self.origin = estimatedPose
            return True
        
        print("No Aruco Marker detected with id : ",arucoId)
        return False


    def getPose(self, arucoId):

        # ret, image = self.cap.read()
        image = requests.get(self.camUrl)
        imgageArray = np.array(bytearray(image.content), dtype=np.uint8)
        image = cv2.imdecode(imgageArray, -1)
        estimatedPose = self.__estimatePose(image, arucoId)



        # return estimatedPose
        
        if(len(estimatedPose) and self.origin != None):

            return self.__relativePosition(estimatedPose)

        print("No Aruco Marker detected with id : ",arucoId)
        return -1



    
    def __estimatePose(self, image, arucoId):
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.aruco_dict = cv2.aruco.Dictionary_get(self.arucoMarkerType)
        parameters = cv2.aruco.DetectorParameters_create()

        corners, ids, rejectedImagePoints = cv2.aruco.detectMarkers(grayImage, cv2.aruco_dict, parameters=parameters,
			cameraMatrix=self.intrinsicCamera,
			distCoeff=self.distortion)
        
        if len(corners):
            for i in range(len(ids)):
                if(ids[i] == arucoId):
                    rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i],self.arucoMarkerSize, self.intrinsicCamera,self.distortion)

                    return [tvec, rvec]                                                     
        return []

    
    def __relativePosition(self, estimatedPose):
        rvec1, tvec1 = self.origin[0].reshape((3,1)), self.origin[1].reshape((3,1))
        rvec2, tvec2 = estimatedPose[0].reshape((3, 1)), estimatedPose[1].reshape((3, 1))

        invRvec, invTvec = self.inversePerspective(rvec2, tvec2)

        info = cv2.composeRT(rvec1, tvec1, invRvec, invTvec)
        composedRvec, composedTvec = info[0], info[1]
        composedRvec = composedRvec.reshape((3, 1))
        composedTvec = composedTvec.reshape((3, 1))
        return [composedRvec, composedTvec]
    
    def inversePerspective(self,rvec, tvec):
        R, _ = cv2.Rodrigues(rvec)
        R = np.matrix(R).T
        invTvec = np.dot(R, np.matrix(-tvec))
        invRvec, _ = cv2.Rodrigues(R)
        return invRvec, invTvec

    # def __del__(self):
    #     self.cap.release()


position = arucoDetection("http://10.196.4.192:8080/shot.jpg")
position.setOrigin(1)
while(1):
    print(position.getPose(1))
    time.sleep(1)



