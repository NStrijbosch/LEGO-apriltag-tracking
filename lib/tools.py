import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

CORNERS_STANDARD = np.array([[-1, 1, 1, -1], [1, 1, -1, -1], [1, 1, 1, 1]])
SELECT_POS = np.array([[1, 0, 0], [0, 1, 0]])

plt.style.use('_mpl-gallery')

class Tag:
    def __init__(
        self,
    ):
        self.id = -1

        self.position_pxl = np.zeros((2))
        self.corners_pxl = np.zeros((2, 4))
        self.homography_pxl = np.zeros((3, 3))

        self.position_real = np.ones((2)) * -1
        self.corners_real = np.zeros((2, 4)) * 10
        self.homography_real = np.zeros((3, 3)) * -1

    def set_real(self, position_real):
        self.position_real = position_real

        self.homography_real[0:2, 0:2] = np.eye(2) * 3
        self.homography_real[0:2, 2] = position_real
        self.homography_real[2, 2] = 1

        self.corners_real = SELECT_POS @ self.homography_real @ CORNERS_STANDARD


class Field(list):

    def append(self,element):
        if not isinstance(element,Tag):
            raise ValueError('Element is not a Tag')
        else:
            return list.append(self,element)

    def plot_real(self):
        fig, ax = plt.subplots()
        for i in range(len(self)):  
            ax.plot(self[i].corners_real[0,np.r_[:4,0]], self[i].corners_real[1,np.r_[:4,0]], linewidth=2.0)

        plt.show()

    def plot_pxl(self):
        fig, ax = plt.subplots()
        for i in range(len(self)):  
            ax.plot(self[i].corners_pxl[0,np.r_[:4,0]], self[i].corners_pxl[1,np.r_[:4,0]], linewidth=2.0)

        plt.show()

    def plot_corners_real_on_pxl(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        for i in range(len(self)):
            if self[i].corners_real[0,0]!=self[i].corners_real[1,1]:
                ax.scatter(self[i].corners_pxl[0,:], self[i].corners_pxl[1,:], self[i].corners_real[0,:],color = 'r')
                ax.scatter(self[i].corners_pxl[0,:], self[i].corners_pxl[1,:], self[i].corners_real[1,:],color = 'b')

        plt.show()

    def plot_real_on_pxl(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        for i in range(len(self)):
            if self[i].corners_real[0,0]!=self[i].corners_real[1,1]:
                ax.scatter(self[i].position_pxl[0], self[i].position_pxl[1], self[i].position_real[0],color = 'r')
                ax.scatter(self[i].position_pxl[0], self[i].position_pxl[1], self[i].position_real[1],color = 'b')

        plt.show()

        

    
