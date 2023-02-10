from math import nan
import requests
import cv2
import numpy as np
import time


class arucoDetection:

    def __init__(self, camUrl = "", arucoMarkerSize = 0.02, arucoMarkerType = cv2.aruco.DICT_4X4_50):
        self.arucoMarkerSize = arucoMarkerSize
        self.arucoMarkerType = arucoMarkerType
        # self.intrinsicCamera = np.array(((933.15867, 0, 657.59),(0,933.1586, 400.36993),(0,0,1)))
        # self.distortion = np.array((-0.43948,0.18514,0,0))
        self.camUrl = camUrl


        #paramters for mobile cam ------not working well :(
        # self.intrinsicCamera = np.array((( 2.9779541947587072e+03, 0., 2.0643284645488870e+03),( 0,2.8273594454649269e+03, 9.2793490978151192e+02),(0,0,1)))
        # self.distortion = np.array((1.6754717875327499e-01, -9.7578371736529701e-01,3.3799089890509605e-03, 5.7466626463058600e-03,2.0988545372834846e+00))

        #parameters for webcam
        # self.intrinsicCamera = np.array(((916.43246, 0, 318.554126),(0, 911.78896, 249.648667),(0,0,1)))
        # self.distortion = np.array((-0.069533, 0.979625, 0.005022, 0.008359999999999999, 0))

        # new webcam
        self.intrinsicCamera = np.array(((525.28433,0, 299.33435),(0, 505.07813, 253.2249), (0,0,1)))
        self.distortion = np.array((-0.312501, 0.074840, -0.007301, 0.002798, 0.000000))

        self.origin = None
        if(len(camUrl) == 0):
            self.cap =  cv2.VideoCapture(2)

    
    def setOrigin(self,arucoId):

        if(len(self.camUrl)):
            image = requests.get(self.camUrl)
            imgageArray = np.array(bytearray(image.content), dtype=np.uint8)
            image = cv2.imdecode(imgageArray, -1)
        else:
            ret, image = self.cap.read()


        estimatedPose = self.__estimatePose(image, arucoId)


        if(len(estimatedPose)):
            self.origin = estimatedPose
            return True
        
        print("No Aruco Marker detected with id : ",arucoId)
        return False

    # Changing coordinate system from camera to drone
    def _changeCoordinate(self, ori,x,y,z):
        return [ori,[-x*3.28084,-y*3.28084,-z*3.28084]]

    def getPose(self, arucoId):


        if(len(self.camUrl)):
            image = requests.get(self.camUrl)
            imgageArray = np.array(bytearray(image.content), dtype=np.uint8)
            image = cv2.imdecode(imgageArray, -1)
        else:
            ret, image = self.cap.read()
        
        # return -1

        cv2.imshow("image",image)
        cv2.waitKey(1)


        estimatedPose = self.__estimatePose(image, arucoId)



        # return estimatedPose
        
        if(len(estimatedPose) and self.origin != None):
            ori, (x,y,z) = self.__relativePosition(estimatedPose)
            return self._changeCoordinate(ori,x,y,z)

        print("No Aruco Marker detected with id : ",arucoId)
        return nan, (nan, nan, nan)



    
    def __estimatePose(self, image, arucoId):
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, grayImage = cv2.threshold(grayImage,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        cv2.aruco_dict = cv2.aruco.Dictionary_get(self.arucoMarkerType)
        parameters = cv2.aruco.DetectorParameters_create()

        corners, ids, rejectedImagePoints = cv2.aruco.detectMarkers(grayImage, cv2.aruco_dict, parameters=parameters,
			cameraMatrix=self.intrinsicCamera,
			distCoeff=self.distortion)
        
        if len(corners):
            for i in range(len(ids)):
                if(ids[i] == arucoId):
                    rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i],self.arucoMarkerSize, self.intrinsicCamera,self.distortion)
                    return [rvec, tvec]                                                     
        return []

    
    def __relativePosition(self, estimatedPose):
        rvec1, tvec1 = self.origin[0].reshape((3,1)), self.origin[1].reshape((3,1))
        rvec2, tvec2 = estimatedPose[0].reshape((3, 1)), estimatedPose[1].reshape((3, 1))

        invRvec, invTvec = self.inversePerspective(rvec2, tvec2)

        info = cv2.composeRT(rvec1, tvec1, invRvec, invTvec)
        composedRvec, composedTvec = info[0], info[1]
        composedRvec = composedRvec.reshape((1, 3))
        composedTvec = composedTvec.reshape((1, 3))
        return [composedRvec[0], composedTvec[0]]
    
    def inversePerspective(self,rvec, tvec):
        R, _ = cv2.Rodrigues(rvec)
        R = np.matrix(R).T
        invTvec = np.dot(R, np.matrix(-tvec))
        invRvec, _ = cv2.Rodrigues(R)
        return invRvec, invTvec



    def __del__(self):
        if(len(self.camUrl) == 0):
            self.cap.release()


# position = arucoDetection("")
# # time.sleep(5)
# position.setOrigin(1)
# while(1):

#     output = position.getPose(1)
#     if(len(output)):
#         ori, (x,y,z) = output
#         print(x,y,z,sep=",")

